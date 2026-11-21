"""Map a git diff between two revisions to the set of changed functions.

Rules: W3-new (change-set extraction feeding B*/F* selection rules, F2 native
fallback, header/build-config escalation). Deterministic, standard library only.
"""
from __future__ import annotations

import ast
import fnmatch
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["ChangeSet", "Config", "changed_functions", "parse_unified_diff"]


@dataclass(frozen=True)
class ChangeSet:
    functions: frozenset
    files: frozenset
    module_level_files: frozenset
    native_files: frozenset
    header_edits: frozenset
    build_config_changed: bool
    unmapped_native: frozenset


@dataclass
class Config:
    native_sources: dict = field(default_factory=dict)   # glob -> extension module name
    native_headers: list = field(default_factory=list)   # globs
    build_config: list = field(default_factory=list)     # globs
    native_name_regex: str | None = None                 # group 1 = python name


# ---------------------------------------------------------------- helpers
def _glob_match(path: str, patterns) -> bool:
    base = path.rsplit("/", 1)[-1]
    for pat in patterns:
        pats = {pat, pat.replace("**/", "")}
        if any(fnmatch.fnmatchcase(path, p) or ("/" not in p and fnmatch.fnmatchcase(base, p))
               for p in pats):
            return True
    return False


def _git(cwd, *args) -> bytes:
    return subprocess.run(
        ["git", "-c", "core.autocrlf=false", "-c", "core.quotepath=false", *args],
        cwd=str(cwd), check=True, capture_output=True,
    ).stdout


def _git_show(cwd, rev, path) -> str:
    r = subprocess.run(
        ["git", "-c", "core.autocrlf=false", "show", f"{rev}:{path}"],
        cwd=str(cwd), capture_output=True,
    )
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else ""


_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def parse_unified_diff(text: str) -> dict:
    """Return {path: (old_changed_lines, new_changed_lines)} (1-based line numbers).

    Removed lines are numbered on the old side, added lines on the new side."""
    out: dict = {}
    cur = None
    old_no = new_no = 0
    old_path = None
    in_hunk = False
    for line in text.splitlines():
        if line.startswith("diff --git "):
            in_hunk = False
            cur = None
            continue
        if not in_hunk:
            if line.startswith("--- "):
                old_path = line[4:].split("\t")[0]
                continue
            if line.startswith("+++ "):
                new_path = line[4:].split("\t")[0]
                p = new_path if new_path != "/dev/null" else old_path
                if p and p != "/dev/null" and p[:2] in ("a/", "b/"):
                    p = p[2:]
                cur = p
                out.setdefault(cur, (set(), set()))
                continue
        m = _HUNK.match(line)
        if m and cur is not None:
            old_no, new_no = int(m.group(1)), int(m.group(3))
            in_hunk = True
            continue
        if not in_hunk or cur is None:
            continue
        if line.startswith("\\"):
            continue
        if line.startswith("-"):
            out[cur][0].add(old_no)
            old_no += 1
        elif line.startswith("+"):
            out[cur][1].add(new_no)
            new_no += 1
        else:
            old_no += 1
            new_no += 1
    return out


# ---------------------------------------------------------------- python
def _py_spans(source: str):
    """[(qualname, start, end)] for all (async) functions, decorators included."""
    tree = ast.parse(source)
    spans = []

    def visit(node, prefix, in_func):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qn = prefix + child.name
                start = min([child.lineno] + [d.lineno for d in child.decorator_list])
                spans.append((qn, start, child.end_lineno))
                visit(child, qn + ".<locals>.", True)
            elif isinstance(child, ast.ClassDef):
                visit(child, prefix + child.name + ".", in_func)
            else:
                visit(child, prefix, in_func)

    visit(tree, "", False)
    return spans


def _significant(lines, no: int) -> bool:
    if no < 1 or no > len(lines):
        return True
    s = lines[no - 1].strip()
    return bool(s) and not s.startswith("#")


def _py_side(rel, source, changed, funcs, module_files):
    lines = source.splitlines()
    try:
        spans = _py_spans(source)
    except SyntaxError:
        spans = None
    for no in sorted(changed):
        if not _significant(lines, no):
            continue
        if spans is None:
            funcs.add(f"{rel}::<module>")
            module_files.add(rel)
            continue
        hit = [qn for qn, s, e in spans if s <= no <= e]
        if hit:
            funcs.update(f"{rel}::{qn}" for qn in hit)
        else:
            funcs.add(f"{rel}::<module>")
            module_files.add(rel)


# ---------------------------------------------------------------- C
def _strip_c(src: str) -> str:
    """Blank out comments, string and char literals; keep newlines/length."""
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ""
        if c == "/" and nxt == "*":
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append("".join(ch if ch == "\n" else " " for ch in src[i:j]))
            i = j
        elif c == "/" and nxt == "/":
            j = src.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i))
            i = j
        elif c in "\"'":
            j = i + 1
            while j < n and src[j] != c and src[j] != "\n":
                j += 2 if src[j] == "\\" else 1
            j = min(j + 1, n)
            out.append("".join(ch if ch == "\n" else " " for ch in src[i:j]))
            i = j
        else:
            out.append(c)
            i += 1
    return "".join(out)


_MACRO_HDR = re.compile(r"^[A-Z_][A-Z0-9_]*\(\s*(\w+)\s*,")
_PLAIN_HDR = re.compile(r"^[\w\s\*]*?\b(\w+)\s*\([^;]*\)\s*\{?$")
_MACRO_ONLY = re.compile(r"^[A-Z_][A-Z0-9_]*(\(.*\))?;?$")
_NOT_FUNCS = {"if", "while", "for", "switch", "return", "else", "do", "sizeof"}


def _c_functions(source: str, name_re):
    """-> (spans [(cname_or_pyname|None, raw_name, start, end)], stripped_lines)."""
    stripped = _strip_c(source)
    lines = stripped.split("\n")
    flat_starts = []
    pos = 0
    for ln in lines:
        flat_starts.append(pos)
        pos += len(ln) + 1
    spans = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if not ln or ln[0].isspace() or ln.startswith("#"):
            i += 1
            continue
        kind = name = None
        m = _MACRO_HDR.match(ln)
        if m:
            kind, name = "macro", m.group(1)
        else:
            m = _PLAIN_HDR.match(ln.rstrip())
            if m and m.group(1) not in _NOT_FUNCS:
                kind, name = "plain", m.group(1)
        if kind is None:
            i += 1
            continue
        if "{" in ln:
            brace_line = i
        elif i + 1 < len(lines) and lines[i + 1].strip().startswith("{"):
            brace_line = i + 1
        else:
            i += 1
            continue
        start_off = flat_starts[brace_line] + lines[brace_line].index("{")
        depth, k = 0, start_off
        while k < len(stripped):
            ch = stripped[k]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        end_line = stripped.count("\n", 0, k)
        pyname = name
        if kind == "plain":
            mm = re.search(name_re, name) if name_re else None
            pyname = mm.group(1) if mm else None
        spans.append((pyname, name, i + 1, end_line + 1))
        i = end_line + 1
    return spans, lines


def _c_side(source, changed, name_re, ext, funcs, unmapped, header_flag):
    spans, slines = _c_functions(source, name_re)
    for no in sorted(changed):
        if no < 1 or no > len(slines) or not slines[no - 1].strip():
            continue          # blank or comment-only
        inside = [s for s in spans if s[2] <= no <= s[3]]
        if inside:
            targets = inside
        else:
            targets = []
            txt = slines[no - 1].strip()
            if _MACRO_ONLY.match(txt):
                nxt = [s for s in spans if 0 < s[2] - no <= 3]
                if nxt:
                    targets = [min(nxt, key=lambda s: s[2])]
            if not targets:
                header_flag.append(True)
                continue
        for pyname, raw, _s, _e in targets:
            if pyname is None:
                unmapped.add(raw)
            else:
                funcs.add(f"native::{ext}.{pyname}")


# ---------------------------------------------------------------- main
def changed_functions(workdir, rev_a: str, rev_b: str, cfg) -> ChangeSet:
    """Change set between two revisions of the git repo at `workdir`."""
    native_sources = getattr(cfg, "native_sources", None) or {}
    native_headers = getattr(cfg, "native_headers", None) or []
    build_config = getattr(cfg, "build_config", None) or []
    name_re = getattr(cfg, "native_name_regex", None)

    diff = _git(workdir, "diff", "--no-color", "--no-renames", "-U0", rev_a, rev_b).decode(
        "utf-8", "replace")
    per_file = parse_unified_diff(diff)

    functions, native_files, module_files = set(), set(), set()
    header_edits, unmapped = set(), set()
    build_changed = False

    for rel in sorted(per_file):
        old_lines, new_lines = per_file[rel]
        if _glob_match(rel, build_config):
            build_changed = True
            continue
        ext = next((e for g, e in native_sources.items() if _glob_match(rel, [g])), None)
        if ext is not None:
            native_files.add(rel)
            flag: list = []
            old_src, new_src = _git_show(workdir, rev_a, rel), _git_show(workdir, rev_b, rel)
            _c_side(old_src, old_lines, name_re, ext, functions, unmapped, flag)
            _c_side(new_src, new_lines, name_re, ext, functions, unmapped, flag)
            if flag:
                header_edits.add(rel)
        elif _glob_match(rel, native_headers):
            header_edits.add(rel)
        elif rel.endswith(".py"):
            old_src, new_src = _git_show(workdir, rev_a, rel), _git_show(workdir, rev_b, rel)
            _py_side(rel, old_src, old_lines, functions, module_files)
            _py_side(rel, new_src, new_lines, functions, module_files)

    return ChangeSet(
        functions=frozenset(functions),
        files=frozenset(per_file),
        module_level_files=frozenset(module_files),
        native_files=frozenset(native_files),
        header_edits=frozenset(header_edits),
        build_config_changed=build_changed,
        unmapped_native=frozenset(unmapped),
    )
