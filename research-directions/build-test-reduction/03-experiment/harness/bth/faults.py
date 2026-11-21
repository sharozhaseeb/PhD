"""Frozen fault generators: functional mutants, algorithmic slowdowns, revert patches.

Rules: W3-new (injected faults, readiness.md section 4.1 / 4.1b / 4.2). Every function is
deterministic: sites are enumerated in source order and ordered by a seeded
``random.Random(seed)`` shuffle; callers take a prefix. All edits are in-place text edits at
exact token / expression positions (the file is never reformatted). Standard library only.

Conventions resolved here (spec ambiguities):
  * ``+=``/``-=`` count as the ``+``/``-`` operator pair; unary ``+``/``-`` are never touched.
  * Integer literal edit: ``n`` -> ``n+1`` and ``n-1`` (``0`` only gets ``+1``); decimal
    literals only (no hex, floats, underscores).
  * ``return <expr>`` -> ``return None`` replaces the value expression (not for ``return None``).
  * Tokens in the ``def`` signature and decorators are never mutated; nested functions of a
    requested function are part of its span (site goes to the innermost requested qualname).
  * Unknown qualnames are ignored by ``python_mutants`` and give ``[]`` from
    ``python_slowdowns``.
"""
from __future__ import annotations

import ast
import hashlib
import io
import keyword
import random
import re
import subprocess
import tokenize
from dataclasses import dataclass

from .changed_fns import _c_functions, _strip_c

__all__ = ["Mutant", "Slowdown", "python_mutants", "c_mutants", "c_function_spans",
           "python_slowdowns", "revert_patch", "patch_hash"]


@dataclass(frozen=True)
class Mutant:
    id: str
    relpath: str
    qualname: str
    op: str
    line: int
    col: int
    before: str
    after: str
    patch: str


@dataclass(frozen=True)
class Slowdown:
    id: str
    relpath: str
    qualname: str
    kind: str
    line: int
    before: str
    after: str
    patch: str


def patch_hash(patches) -> str:
    """sha256 over the patches (freezing helper)."""
    h = hashlib.sha256()
    for p in patches:
        h.update(p.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


# ------------------------------------------------------------------ text helpers
def _lines(text: str) -> list[str]:
    return io.StringIO(text).readlines()          # splits on "\n" only, keeps endings


def _offsets(lines) -> list[int]:
    offs, pos = [], 0
    for ln in lines:
        offs.append(pos)
        pos += len(ln)
    offs.append(pos)
    return offs


def _make_patch(relpath: str, old: str, new: str) -> str:
    import difflib
    a, b = _lines(old), _lines(new)
    out = [f"diff --git a/{relpath} b/{relpath}\n", f"--- a/{relpath}\n", f"+++ b/{relpath}\n"]
    for ln in list(difflib.unified_diff(a, b, n=3))[2:]:
        if ln.endswith("\n"):
            out.append(ln)
        else:
            out.append(ln + "\n\\ No newline at end of file\n")
    return "".join(out)


def _apply_edits(text: str, edits) -> str:
    """edits: [(start_off, end_off, replacement)], non-overlapping."""
    out, pos = [], 0
    for s, e, r in sorted(edits):
        out.append(text[pos:s])
        out.append(r)
        pos = e
    out.append(text[pos:])
    return "".join(out)


def _ast_col(lines, lineno: int, byte_col: int) -> int:
    return len(lines[lineno - 1].encode("utf-8")[:byte_col].decode("utf-8", "ignore"))


_REL_FLIP = {"<": "<=", "<=": "<", ">": ">=", ">=": ">", "==": "!=", "!=": "=="}
_ARITH_FLIP = {"+": "-", "-": "+", "+=": "-=", "-=": "+="}
_BOOL_PY = {"and": "or", "or": "and"}
_BOOL_C = {"&&": "||", "||": "&&"}


def _int_variants(tok: str):
    if not re.fullmatch(r"[0-9]+", tok):
        return []
    n = int(tok)
    out = [str(n + 1)]
    if n >= 1:
        out.append(str(n - 1))
    return out


def _shuffled(sites, seed):
    sites = sorted(sites, key=lambda s: (s["line"], s["col"], s["after"], s["op"]))
    random.Random(seed).shuffle(sites)
    return sites


def _build_mutants(relpath, text, sites, seed):
    muts = []
    for s in _shuffled(sites, seed):
        new = _apply_edits(text, [(s["start"], s["end"], s["after"])])
        muts.append(Mutant(
            id=f'{relpath}::{s["qualname"]}@{s["line"]}:{s["col"]}:{s["op"]}:{s["after"]}',
            relpath=relpath, qualname=s["qualname"], op=s["op"], line=s["line"], col=s["col"],
            before=s["before"], after=s["after"], patch=_make_patch(relpath, text, new)))
    return muts


# ------------------------------------------------------------------ python functions
def _py_functions(tree):
    """qualname -> (node, prefix) in changed_fns style (``outer.<locals>.inner``)."""
    out = {}

    def visit(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qn = prefix + child.name
                out.setdefault(qn, (child, prefix))
                visit(child, qn + ".<locals>.")
            elif isinstance(child, ast.ClassDef):
                visit(child, prefix + child.name + ".")
            else:
                visit(child, prefix)

    visit(tree, "")
    return out


def _own_nodes(func):
    """Descendants of `func` (not entering nested defs/lambdas/classes), unordered."""
    stack = list(func.body)
    while stack:
        n = stack.pop()
        yield n
        for c in ast.iter_child_nodes(n):
            if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
                continue
            stack.append(c)


def _body_start(func) -> tuple[int, int]:
    first = func.body[0]
    line = min([first.lineno] + [d.lineno for d in getattr(first, "decorator_list", [])])
    return (line, first.col_offset if line == func.lineno else 0)


# ------------------------------------------------------------------ python mutants
_OPERAND_END = {")", "]", "}"}
_FSTRING_END = getattr(tokenize, "FSTRING_END", -1)


def _py_tokens(text):
    toks = []
    prev = None
    for t in tokenize.generate_tokens(io.StringIO(text).readline):
        if t.type in (tokenize.COMMENT, tokenize.NL):
            continue
        toks.append((t, prev))
        prev = t
    return toks


def _is_operand_end(prev) -> bool:
    if prev is None:
        return False
    if prev.type in (tokenize.NUMBER, tokenize.STRING, _FSTRING_END):
        return True
    if prev.type == tokenize.NAME:
        return (not keyword.iskeyword(prev.string)) or prev.string in ("None", "True", "False")
    return prev.type == tokenize.OP and prev.string in _OPERAND_END


def python_mutants(src_text: str, relpath: str, funcs, seed) -> list[Mutant]:
    """All mutation sites inside the requested functions (qualnames), seeded order."""
    tree = ast.parse(src_text)
    lines = _lines(src_text)
    offs = _offsets(lines)
    allfuncs = _py_functions(tree)
    toks = _py_tokens(src_text)

    chosen = []
    for qn in funcs:
        if qn in allfuncs:
            node = allfuncs[qn][0]
            chosen.append((node.end_lineno - node.lineno, qn, node))
    chosen.sort(key=lambda c: (-c[0], c[1]))      # outer first, inner overrides
    sites: dict = {}

    def off(line, col):
        return offs[line - 1] + col

    for _n, qn, node in chosen:
        start = _body_start(node)
        end = (node.end_lineno, _ast_col(lines, node.end_lineno, node.end_col_offset))
        for t, prev in toks:
            if t.start < start or t.start >= end:
                continue
            s, e, after, op = None, None, [], None
            if t.type == tokenize.OP and t.string in _REL_FLIP:
                op, after = "rel_flip", [_REL_FLIP[t.string]]
            elif t.type == tokenize.OP and t.string in _ARITH_FLIP:
                if _is_operand_end(prev):
                    op, after = "arith_flip", [_ARITH_FLIP[t.string]]
            elif t.type == tokenize.NAME and t.string in _BOOL_PY:
                op, after = "bool_flip", [_BOOL_PY[t.string]]
            elif t.type == tokenize.NUMBER:
                v = _int_variants(t.string)
                if v:
                    op, after = "int_pm1", v
            if op:
                s, e = off(*t.start), off(*t.end)
                for a in after:
                    sites[(t.start, op, a)] = dict(
                        qualname=qn, op=op, line=t.start[0], col=t.start[1], before=t.string,
                        after=a, start=s, end=e)
        for n in ast.walk(node):
            if isinstance(n, ast.Return) and n.value is not None:
                if isinstance(n.value, ast.Constant) and n.value.value is None:
                    continue
                v = n.value
                sl, sc = v.lineno, _ast_col(lines, v.lineno, v.col_offset)
                el, ec = v.end_lineno, _ast_col(lines, v.end_lineno, v.end_col_offset)
                s, e = off(sl, sc), off(el, ec)
                sites[((sl, sc), "ret_none", "None")] = dict(
                    qualname=qn, op="ret_none", line=sl, col=sc, before=src_text[s:e],
                    after="None", start=s, end=e)
    return _build_mutants(relpath, src_text, list(sites.values()), seed)


# ------------------------------------------------------------------ C mutants
def c_function_spans(src_text: str, name_re=None):
    """[(python_or_raw_name, start_line, end_line)] using changed_fns' brace scanner."""
    spans, _ = _c_functions(src_text, name_re)
    return [(py or raw, s, e) for py, raw, s, e in spans]


def _norm_spans(func_spans):
    if isinstance(func_spans, dict):
        func_spans = [(k, *v) for k, v in func_spans.items()]
    out = []
    for sp in func_spans:
        if len(sp) == 2:
            out.append(("", int(sp[0]), int(sp[1])))
        else:
            out.append((str(sp[0]), int(sp[1]), int(sp[2])))
    return out


_C_TOK = re.compile(r"""
  (?P<num>(?<![\w.])\d+(?![\w.]))
 |(?P<op>&&|\|\||<<=|>>=|<<|>>|<=|>=|==|!=|\+\+|--|\+=|-=|->|[<>+\-])
 |(?P<id>[A-Za-z_]\w*)
 |(?P<close>[)\]])
 |(?P<other>\S)
""", re.X)
_C_UNARY_KW = {"return", "case", "else", "do", "sizeof"}


def _blank_directives(stripped: str) -> str:
    out, cont = [], False
    for ln in stripped.split("\n"):
        if cont or ln.lstrip().startswith("#"):
            cont = ln.rstrip().endswith("\\")
            out.append(" " * len(ln))
        else:
            out.append(ln)
    return "\n".join(out)


def c_mutants(src_text: str, relpath: str, func_spans, seed) -> list[Mutant]:
    """Same operators on C tokens inside `func_spans` (1-based inclusive line ranges).

    `func_spans`: dict name -> (start, end), or iterable of (name, start, end) / (start, end).
    Only text after the first ``{`` of a span is mutated (never the header)."""
    text = src_text
    stripped = _blank_directives(_strip_c(text))
    lines = text.split("\n")
    offs, pos = [], 0
    for ln in lines:
        offs.append(pos)
        pos += len(ln) + 1
    sites: dict = {}
    for name, ls, le in sorted(_norm_spans(func_spans), key=lambda s: (-(s[2] - s[1]), s[0])):
        ls, le = max(ls, 1), min(le, len(lines))
        lo, hi = offs[ls - 1], offs[le - 1] + len(lines[le - 1])
        brace = stripped.find("{", lo, hi)
        if brace < 0:
            continue
        prev_kind, prev_txt = "other", ""
        for m in _C_TOK.finditer(stripped, brace + 1, hi):
            kind, tok = m.lastgroup, m.group()
            after, op = [], None
            if kind == "op":
                binary = prev_kind in ("num", "close") or (
                    prev_kind == "id" and prev_txt not in _C_UNARY_KW)
                if tok in _REL_FLIP:
                    op, after = "rel_flip", [_REL_FLIP[tok]]
                elif tok in _ARITH_FLIP and binary:
                    op, after = "arith_flip", [_ARITH_FLIP[tok]]
                elif tok in _BOOL_C:
                    op, after = "bool_flip", [_BOOL_C[tok]]
            elif kind == "num":
                v = _int_variants(tok)
                if v:
                    op, after = "int_pm1", v
            prev_kind, prev_txt = kind, tok
            if not op:
                continue
            s = m.start()
            line = stripped.count("\n", 0, s) + 1
            col = s - offs[line - 1]
            for a in after:
                sites[(line, col, op, a)] = dict(
                    qualname=name, op=op, line=line, col=col, before=tok, after=a,
                    start=s, end=m.end())
    return _build_mutants(relpath, text, list(sites.values()), seed)


# ------------------------------------------------------------------ slowdowns
def _has_yield(func) -> bool:
    return any(isinstance(n, (ast.Yield, ast.YieldFrom)) for n in _own_nodes(func))


def _set_like(value) -> bool:
    if isinstance(value, (ast.Set, ast.SetComp, ast.Dict, ast.DictComp)):
        return True
    return (isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
            and value.func.id in ("set", "dict"))


_LIST_LIKE_CALLS = {"list", "set", "dict", "tuple", "sorted", "range", "frozenset"}


def _sized_like(value) -> bool:
    if isinstance(value, (ast.List, ast.Tuple, ast.Set, ast.Dict, ast.ListComp, ast.SetComp,
                          ast.DictComp)):
        return True
    return (isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
            and value.func.id in _LIST_LIKE_CALLS)


def _bindings(func):
    """name -> list of (lineno, value-or-None) for every binding inside `func` (own scope)."""
    b: dict = {}
    a = func.args
    for arg in a.posonlyargs + a.args + a.kwonlyargs + [x for x in (a.vararg, a.kwarg) if x]:
        b.setdefault(arg.arg, []).append((0, None))
    for n in _own_nodes(func):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    b.setdefault(t.id, []).append((n.lineno, n.value))
                else:
                    for s in ast.walk(t):
                        if isinstance(s, ast.Name):
                            b.setdefault(s.id, []).append((n.lineno, None))
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            b.setdefault(n.target.id, []).append((n.lineno, n.value))
        elif isinstance(n, (ast.AugAssign,)) and isinstance(n.target, ast.Name):
            b.setdefault(n.target.id, []).append((n.lineno, None))
        elif isinstance(n, (ast.For, ast.AsyncFor, ast.comprehension)):
            for s in ast.walk(n.target):
                if isinstance(s, ast.Name):
                    b.setdefault(s.id, []).append((n.lineno if hasattr(n, "lineno") else 0, None))
        elif isinstance(n, ast.NamedExpr):
            b.setdefault(n.target.id, []).append((n.lineno, None))
        elif isinstance(n, (ast.With, ast.AsyncWith)):
            for it in n.items:
                if it.optional_vars is not None:
                    for s in ast.walk(it.optional_vars):
                        if isinstance(s, ast.Name):
                            b.setdefault(s.id, []).append((n.lineno, None))
    return b


def _slow(relpath, qn, kind, line, before, after, old, new, extra=""):
    return Slowdown(id=f"{relpath}::{qn}:{kind}@{line}{extra}", relpath=relpath, qualname=qn,
                    kind=kind, line=line, before=before, after=after,
                    patch=_make_patch(relpath, old, new))


def python_slowdowns(src_text: str, relpath: str, qualname: str) -> list[Slowdown]:
    """double_call, list_membership (one per site), sorted_copy for one function."""
    tree = ast.parse(src_text)
    allf = _py_functions(tree)
    if qualname not in allf:
        return []
    func, prefix = allf[qualname]
    lines = _lines(src_text)
    offs = _offsets(lines)
    out: list[Slowdown] = []

    # (a) double_call ------------------------------------------------------------
    parent_class = prefix[:-1] if prefix and not prefix.endswith(".<locals>.") else None
    if (isinstance(func, ast.FunctionDef) and not _has_yield(func)
            and not (parent_class and "<locals>" in parent_class)):
        m = re.compile(r"\bdef\s+(" + re.escape(func.name) + r")\b").search(lines[func.lineno - 1])
        if m:
            dec_start = min([d.lineno for d in func.decorator_list] + [func.lineno])
            indent = re.match(r"[ \t]*", lines[func.lineno - 1]).group()
            nl = "\r\n" if lines[func.lineno - 1].endswith("\r\n") else "\n"
            decos = lines[dec_start - 1:func.lineno - 1]
            def_line = lines[func.lineno - 1]
            new_def = def_line[:m.start(1)] + "_bth_orig_" + def_line[m.start(1):]
            callee = f"{parent_class}._bth_orig_{func.name}" if parent_class else f"_bth_orig_{func.name}"
            wrapper = [nl] * (1 if indent else 2)
            wrapper += decos
            wrapper += [f"{indent}def {func.name}(*a, **k):{nl}",
                        f"{indent}    {callee}(*a, **k){nl}",
                        f"{indent}    return {callee}(*a, **k){nl}"]
            new_lines = list(lines)
            end = func.end_lineno
            if not new_lines[end - 1].endswith("\n"):
                new_lines[end - 1] += nl
            new_lines = (new_lines[:dec_start - 1] + [new_def] + new_lines[func.lineno:end]
                         + wrapper + new_lines[end:])
            out.append(_slow(relpath, qualname, "double_call", func.lineno, func.name,
                             f"_bth_orig_{func.name}", src_text, "".join(new_lines)))

    # (b) list_membership --------------------------------------------------------
    binds = _bindings(func)
    setnames = {n for n, bs in binds.items()
                if bs and all(v is not None and _set_like(v) for _l, v in bs)}
    sites = []
    for n in _own_nodes(func):
        if isinstance(n, ast.Compare):
            for op, comp in zip(n.ops, n.comparators):
                if isinstance(op, (ast.In, ast.NotIn)) and isinstance(comp, ast.Name) \
                        and comp.id in setnames:
                    sites.append(comp)
    for comp in sorted(sites, key=lambda c: (c.lineno, c.col_offset)):
        sc = _ast_col(lines, comp.lineno, comp.col_offset)
        ec = _ast_col(lines, comp.end_lineno, comp.end_col_offset)
        s, e = offs[comp.lineno - 1] + sc, offs[comp.end_lineno - 1] + ec
        new = _apply_edits(src_text, [(s, s, "list("), (e, e, ")")])
        out.append(_slow(relpath, qualname, "list_membership", comp.lineno, comp.id,
                         f"list({comp.id})", src_text, new, extra=f":{sc}"))

    # (c) sorted_copy ------------------------------------------------------------
    fors = sorted((n for n in _own_nodes(func) if isinstance(n, ast.For)),
                  key=lambda n: (n.lineno, n.col_offset))
    if fors:
        loop = fors[0]
        body0 = loop.body[0]
        it = loop.iter
        ok = (isinstance(it, ast.Name) and body0.lineno > loop.lineno
              and any(l < loop.lineno and v is not None and _sized_like(v)
                      for l, v in binds.get(it.id, []))
              and all(v is not None and _sized_like(v) for _l, v in binds.get(it.id, [])))
        if ok:
            first = min([body0.lineno] + [d.lineno for d in getattr(body0, "decorator_list", [])])
            ind = re.match(r"[ \t]*", lines[first - 1]).group()
            nl = "\r\n" if lines[first - 1].endswith("\r\n") else "\n"
            ins = f"{ind}_bth_tmp = sorted(range(len({it.id}))){nl}"
            new_lines = lines[:first - 1] + [ins] + lines[first - 1:]
            out.append(_slow(relpath, qualname, "sorted_copy", first, "",
                             ins.strip(), src_text, "".join(new_lines)))
    return out


# ------------------------------------------------------------------ revert
def revert_patch(repo_workdir, step_state_sha: str, src_pathspec=None) -> str:
    """Reverse of the source diff that the replayed commit `step_state_sha` introduced.

    Applying the result on top of `step_state_sha` restores its parent's sources.
    Read-only git (``git diff``), run with cwd = `repo_workdir`."""
    cmd = ["git", "-c", "core.autocrlf=false", "diff", "--no-color", "--no-renames",
           step_state_sha, step_state_sha + "^"]
    if src_pathspec:
        cmd += ["--", *([src_pathspec] if isinstance(src_pathspec, str) else src_pathspec)]
    r = subprocess.run(cmd, cwd=str(repo_workdir), check=True, capture_output=True)
    return r.stdout.decode("utf-8", "replace")
