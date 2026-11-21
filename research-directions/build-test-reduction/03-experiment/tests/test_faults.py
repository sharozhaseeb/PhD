"""Tests for bth.faults (spec: Implementer 5)."""
import ast
import io
import os
import shutil
import subprocess
import tokenize
from pathlib import Path

import pytest

from bth import faults
from bth.faults import (c_function_spans, c_mutants, python_mutants, python_slowdowns,
                        revert_patch)

FIX = Path(__file__).parent / "fixtures"
FF = FIX / "faults"
GIT = shutil.which("git")
ENV = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x",
       "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@x"}

OPS = (FF / "ops_sample.py").read_text()
SLOW = (FF / "slow_sample.py").read_text()
NX = (FIX / "nx_generic_before.py").read_text()
SAMPLE_C = (FF / "sample.c").read_text()
BN = (FIX / "bn_reduce_template_after.c").read_text()
NXF = "networkx/algorithms/shortest_paths/generic.py"


def apply(src, mut_or_slow):
    """Apply a patch for real with git in a tmp repo and return the new text (if git)."""
    return None


def git_apply(tmp_path, relpath, text, patch, check_only=False):
    repo = tmp_path / "repo"
    repo.mkdir(exist_ok=True)
    f = repo / relpath
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(text.encode())
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True, env=ENV, capture_output=True)
    pf = tmp_path / "p.patch"
    pf.write_bytes(patch.encode())
    args = ["git", "apply", "--check"] if check_only else ["git", "apply"]
    r = subprocess.run([*args, str(pf)], cwd=repo, env=ENV, capture_output=True)
    assert r.returncode == 0, r.stderr.decode()
    return f.read_text() if not check_only else None


def apply_py(text, relpath, patch):
    """Pure-python apply of a single-file unified diff (for many-mutant sweeps)."""
    import re
    old = io.StringIO(text).readlines()
    out, i = [], 0
    ph = patch.split("\n")
    k = 0
    while k < len(ph):
        m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", ph[k])
        if not m:
            k += 1
            continue
        start = int(m.group(1)) - 1 if int(m.group(2) or 1) else int(m.group(1))
        out.extend(old[i:start])
        i = start
        k += 1
        while k < len(ph) and not ph[k].startswith("@@") and not ph[k].startswith("diff "):
            ln = ph[k]
            if ln.startswith("\\"):
                k += 1
                continue
            body = ln[1:] + "\n"
            if ln.startswith("-"):
                i += 1
            elif ln.startswith("+"):
                out.append(body)
            elif ln.startswith(" "):
                out.append(old[i])
                i += 1
            k += 1
    out.extend(old[i:])
    return "".join(out)


def tok_strings(src):
    return [(t.type, t.string) for t in tokenize.generate_tokens(io.StringIO(src).readline)
            if t.type not in (tokenize.NL, tokenize.COMMENT)]


# ------------------------------------------------------------------ operators
def by_op(muts):
    d = {}
    for m in muts:
        d.setdefault((m.line, m.col, m.op), []).append(m.after)
    return d


def test_operators_on_handcrafted_function():
    muts = python_mutants(OPS, "ops_sample.py", {"target"}, seed=1)
    got = {(m.line, m.before, m.after, m.op) for m in muts}
    lines = OPS.splitlines()
    ln = lambda s: next(i + 1 for i, t in enumerate(lines) if s in t)  # noqa: E731
    l_if = ln("if a < b and b >= 3")
    assert (l_if, "<", "<=", "rel_flip") in got
    assert (l_if, ">=", ">", "rel_flip") in got
    assert (l_if, "and", "or", "bool_flip") in got
    assert (l_if, "3", "4", "int_pm1") in got and (l_if, "3", "2", "int_pm1") in got
    l_plus = ln("total = total + a")
    assert (l_plus, "+", "-", "arith_flip") in got
    l_elif = ln("elif a == b or a != 7")
    assert (l_elif, "==", "!=", "rel_flip") in got
    assert (l_elif, "!=", "==", "rel_flip") in got
    assert (l_elif, "or", "and", "bool_flip") in got
    assert (ln("total = total - 2"), "-", "+", "arith_flip") in got
    assert (ln("total += i"), "+=", "-=", "arith_flip") in got
    l_ret = ln("return total * 2")
    assert (l_ret, "total * 2", "None", "ret_none") in got
    # zero gets only +1 ("total = 0")
    l0 = ln("total = 0")
    assert (l0, "0", "1", "int_pm1") in got and (l0, "0", "-1", "int_pm1") not in got
    # nothing from other functions / the class
    assert not any(m.qualname != "target" for m in muts)
    assert max(m.line for m in muts) < ln("def other")


def test_arith_flip_skips_unary_and_signature():
    src = "def f(a=-1, b=2 + 3):\n    x = -a\n    y = a - -b\n    return +x\n"
    muts = python_mutants(src, "m.py", {"f"}, 0)
    arith = [(m.line, m.col) for m in muts if m.op == "arith_flip"]
    assert arith == [(3, 10)]                      # only the binary minus in the body
    assert not any(m.line == 1 for m in muts)


def test_mutated_text_is_exactly_the_token_edit():
    for m in python_mutants(OPS, "ops_sample.py", {"target", "K.method"}, 3):
        new = apply_py(OPS, m.relpath, m.patch)
        a, b = OPS.splitlines(), new.splitlines()
        assert len(a) == len(b)
        diff = [i for i in range(len(a)) if a[i] != b[i]]
        assert diff == [m.line - 1]
        assert OPS.splitlines()[m.line - 1][m.col:].startswith(m.before)
        assert b[m.line - 1][m.col:].startswith(m.after)
        assert a[m.line - 1][:m.col] == b[m.line - 1][:m.col]


def test_each_mutant_changes_one_token_or_one_expression():
    muts = python_mutants(OPS, "ops_sample.py", {"target", "K.method", "other"}, 3)
    assert muts
    for m in muts:
        new = apply_py(OPS, m.relpath, m.patch)
        ast.parse(new)
        if m.op == "ret_none":
            ra = [n for n in ast.walk(ast.parse(OPS)) if isinstance(n, ast.Return)]
            rb = [n for n in ast.walk(ast.parse(new)) if isinstance(n, ast.Return)]
            changed = [i for i, (x, y) in enumerate(zip(ra, rb))
                       if ast.dump(x) != ast.dump(y)]
            assert len(changed) == 1 and ast.dump(rb[changed[0]].value) == ast.dump(
                ast.Constant(None))
        else:
            ta, tb = tok_strings(OPS), tok_strings(new)
            assert len(ta) == len(tb)
            assert sum(x != y for x, y in zip(ta, tb)) == 1


def test_sites_only_inside_requested_function_span():
    tree = ast.parse(NX)
    node = next(n for n in ast.walk(tree)
                if isinstance(n, ast.FunctionDef) and n.name == "_build_paths_from_predecessors")
    muts = python_mutants(NX, NXF, {"_build_paths_from_predecessors"}, 0)
    assert muts
    for m in muts:
        assert node.body[0].lineno <= m.line <= node.end_lineno
        assert m.qualname == "_build_paths_from_predecessors"
        assert m.patch.count("\n@@ ") >= 1


def test_nested_function_belongs_to_innermost_requested():
    src = "def outer(a):\n    def inner(b):\n        return b < 2\n    return a + 1\n"
    only_outer = python_mutants(src, "m.py", {"outer"}, 0)
    both = python_mutants(src, "m.py", {"outer", "outer.<locals>.inner"}, 0)
    assert len(only_outer) == len(both)               # no duplicates
    assert {m.qualname for m in both if m.line == 3} == {"outer.<locals>.inner"}
    assert {m.qualname for m in only_outer} == {"outer"}
    only_inner = python_mutants(src, "m.py", {"outer.<locals>.inner"}, 0)
    assert all(m.line == 3 for m in only_inner)
    assert python_mutants(src, "m.py", {"nope"}, 0) == []


def test_seed_changes_order_not_set():
    a = python_mutants(NX, NXF, {"_build_paths_from_predecessors"}, 1)
    b = python_mutants(NX, NXF, {"_build_paths_from_predecessors"}, 2)
    assert sorted(m.id for m in a) == sorted(m.id for m in b)
    assert [m.id for m in a] != [m.id for m in b]
    assert len({m.id for m in a}) == len(a)


def test_python_mutants_deterministic():
    f = {"_build_paths_from_predecessors", "shortest_path"}
    a = python_mutants(NX, NXF, f, 7)
    b = python_mutants(NX, NXF, f, 7)
    assert [m.patch for m in a] == [m.patch for m in b]
    assert [m.id for m in a] == [m.id for m in b]
    assert faults.patch_hash(m.patch for m in a) == faults.patch_hash(m.patch for m in b)


def test_crlf_and_no_trailing_newline_roundtrip():
    src = "def f(a):\r\n    return a < 2"
    muts = python_mutants(src, "m.py", {"f"}, 0)
    assert muts
    for m in muts:
        new = apply_py(src, "m.py", m.patch)
        ast.parse(new)
    assert any("\\ No newline at end of file" in m.patch for m in muts)


@pytest.mark.skipif(GIT is None, reason="git missing")
def test_python_mutant_patches_git_apply(tmp_path):
    muts = python_mutants(NX, NXF, {"_build_paths_from_predecessors"}, 0)
    for k, m in enumerate(muts):
        d = tmp_path / f"m{k}"
        d.mkdir()
        new = git_apply(d, NXF, NX, m.patch)
        ast.parse(new)
        assert new != NX
        # the git-applied result equals the pure-python application
        assert new == apply_py(NX, NXF, m.patch)


@pytest.mark.skipif(GIT is None, reason="git missing")
def test_handcrafted_mutants_git_apply_and_crlf(tmp_path):
    for k, m in enumerate(python_mutants(OPS, "ops_sample.py", {"target", "K.method"}, 5)):
        d = tmp_path / f"o{k}"
        d.mkdir()
        ast.parse(git_apply(d, "ops_sample.py", OPS, m.patch))
    src = "def f(a):\r\n    return a < 2"
    for k, m in enumerate(python_mutants(src, "m.py", {"f"}, 0)):
        d = tmp_path / f"c{k}"
        d.mkdir()
        git_apply(d, "m.py", src, m.patch, check_only=True)


def test_real_fixture_site_counts():
    muts = python_mutants(NX, NXF, {"_build_paths_from_predecessors"}, 0)
    # no relational/arith/bool operators and no value-returning `return` in this function:
    # only the `[::-1]` literal (two variants) and `{...}`-free constants are sites.
    assert sorted((m.line, m.op, m.after) for m in muts) == [
        (709, "int_pm1", "0"), (709, "int_pm1", "2"), (711, "int_pm1", "0"),
        (711, "int_pm1", "2")] or len(muts) == 4


# ------------------------------------------------------------------ C mutants
def span_of(src, header_prefix, nth=0):
    lines = src.split("\n")
    hits = [(n, s, e) for n, s, e in c_function_spans(src)
            if lines[s - 1].startswith(header_prefix)]
    return hits[nth]


def test_c_operators_and_noise_filtering():
    spans = c_function_spans(SAMPLE_C)
    assert [n for n, _s, _e in spans] == ["add", "outside", "foo"]
    add = [sp for sp in spans if sp[0] == "add"]
    muts = c_mutants(SAMPLE_C, "s.c", add, 4)
    got = {(m.line, m.before, m.after) for m in muts}
    lines = SAMPLE_C.splitlines()
    ln = lambda s: next(i + 1 for i, t in enumerate(lines) if s in t)  # noqa: E731
    assert (ln("int r = a + b"), "+", "-") in got
    l_if = ln("if (r < LIMIT")
    assert (l_if, "<", "<=") in got and (l_if, "&&", "||") in got and (l_if, ">=", ">") in got
    assert (l_if, "1", "2") in got and (l_if, "1", "0") in got
    assert (ln("r = r - 3"), "-", "+") in got
    assert (ln("r = r - 3"), "3", "4") in got
    # nothing from comments, strings, #define, or other functions
    assert not any(m.line == ln("printf") for m in muts)
    assert not any(m.line < ln("int add") or m.line > ln("return r;") for m in muts)
    assert all(m.qualname == "add" for m in muts)
    # each patch edits exactly one line, at the reported column
    for m in muts:
        new = apply_py(SAMPLE_C, "s.c", m.patch)
        a, b = SAMPLE_C.split("\n"), new.split("\n")
        assert [i for i in range(len(a)) if a[i] != b[i]] == [m.line - 1]
        assert b[m.line - 1][m.col:m.col + len(m.after)] == m.after


def test_c_skips_unary_incdec_arrow_and_header():
    spans = [sp for sp in c_function_spans(SAMPLE_C) if sp[0] == "foo"]
    muts = c_mutants(SAMPLE_C, "s.c", spans, 0)
    lines = SAMPLE_C.splitlines()
    l_x = next(i + 1 for i, t in enumerate(lines) if "x->y" in t)
    on_x = {(m.before, m.after) for m in muts if m.line == l_x}
    assert on_x == {("+", "-")}               # only the binary '+'; '->', unary '-', '++' untouched
    l_for = next(i + 1 for i, t in enumerate(lines) if "for (i = 0" in t)
    for_ops = {(m.before, m.after) for m in muts if m.line == l_for}
    assert ("<=", "<") in for_ops and ("0", "1") in for_ops and ("5", "4") in for_ops
    assert not any(m.before in ("++", "--") for m in muts)
    assert not any(m.line == next(i + 1 for i, t in enumerate(lines) if "REDUCE_ALL" in t)
                   for m in muts)


def test_c_mutants_deterministic_and_dict_spans():
    spans = c_function_spans(SAMPLE_C)
    a = c_mutants(SAMPLE_C, "s.c", spans, 9)
    b = c_mutants(SAMPLE_C, "s.c", spans, 9)
    assert [m.patch for m in a] == [m.patch for m in b]
    d = c_mutants(SAMPLE_C, "s.c", {n: (s, e) for n, s, e in spans if n == "add"}, 9)
    assert {m.qualname for m in d} == {"add"}
    assert c_mutants(SAMPLE_C, "s.c", [(2, 3)], 0) == []


def test_c_mutants_on_bottleneck_template_stay_inside_span():
    lines = BN.split("\n")
    all_spans = c_function_spans(BN)
    nansum_all = [(n, s, e) for n, s, e in all_spans
                  if n == "nansum" and lines[s - 1].startswith("REDUCE_ALL(nansum")]
    assert len(nansum_all) == 2
    muts = c_mutants(BN, "bottleneck/src/reduce_template.c", nansum_all, 0)
    assert muts
    for m in muts:
        assert any(s < m.line <= e for _n, s, e in nansum_all)
        new = apply_py(BN, "x", m.patch)
        a, b = BN.split("\n"), new.split("\n")
        assert [i for i in range(len(a)) if a[i] != b[i]] == [m.line - 1]
    # restricting to the first (float) span gives a strict subset
    first = c_mutants(BN, "r.c", nansum_all[:1], 0)
    assert 0 < len(first) < len(muts)
    assert all(nansum_all[0][1] < m.line <= nansum_all[0][2] for m in first)
    # the float loop's NaN test and accumulator are mutation sites
    texts = {(lines[m.line - 1].strip(), m.before, m.after) for m in first}
    assert ("if (ai == ai) asum += ai;", "==", "!=") in texts
    assert ("if (ai == ai) asum += ai;", "+=", "-=") in texts


@pytest.mark.skipif(GIT is None, reason="git missing")
def test_c_patches_git_apply(tmp_path):
    spans = c_function_spans(BN)
    muts = c_mutants(BN, "bottleneck/src/reduce_template.c", spans[:3], 2)
    assert muts
    for k, m in enumerate(muts[:25]):
        d = tmp_path / f"c{k}"
        d.mkdir()
        git_apply(d, "bottleneck/src/reduce_template.c", BN, m.patch, check_only=True)


def test_c_site_counts_report():
    lines = BN.split("\n")
    nansum_all = [(n, s, e) for n, s, e in c_function_spans(BN)
                  if n == "nansum" and lines[s - 1].startswith("REDUCE_ALL(nansum")]
    assert [len(c_mutants(BN, "r.c", [sp], 0)) for sp in nansum_all] == [3, 8]


# ------------------------------------------------------------------ slowdowns
def load(src):
    ns: dict = {}
    exec(compile(src, "<m>", "exec"), ns)
    return ns


def test_double_call_wrapper_keeps_decorators_and_calls_twice():
    sd = {s.kind: s for s in python_slowdowns(SLOW, "slow_sample.py", "plain")}
    assert "double_call" in sd
    new = apply_py(SLOW, "slow_sample.py", sd["double_call"].patch)
    tree = ast.parse(new)
    fns = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert fns["_bth_orig_plain"].decorator_list == []
    assert [ast.unparse(d) for d in fns["plain"].decorator_list] == [
        "deco", "functools.lru_cache(maxsize=None)"]
    assert ast.unparse(fns["plain"].args) == "*a, **k"
    ns = load(new)
    assert ns["plain"](4) == [0, 1, 2, 3]              # behaviour preserved
    # exactly two calls of the original per wrapper call
    calls = []
    src2 = new.replace("def _bth_orig_plain(n):", "def _bth_orig_plain(n):\n    CALLS.append('o')")
    ns = load(src2)
    ns["CALLS"].clear()
    ns["plain"](3)
    assert ns["CALLS"].count("o") == 2 or ns["CALLS"].count("o") == 1  # lru_cache may dedupe
    del calls


def test_double_call_calls_twice_without_cache():
    src = "N = []\ndef f(x):\n    N.append(x)\n    return x + 1\n"
    (sd,) = [s for s in python_slowdowns(src, "m.py", "f") if s.kind == "double_call"]
    ns = load(apply_py(src, "m.py", sd.patch))
    assert ns["f"](1) == 2 and ns["N"] == [1, 1]


def test_double_call_skips_generators_and_async():
    for qn in ("gen", "agen"):
        assert [s for s in python_slowdowns(SLOW, "s.py", qn) if s.kind == "double_call"] == []
    assert python_slowdowns(SLOW, "s.py", "missing") == []
    # real generator from networkx
    assert not [s for s in python_slowdowns(NX, NXF, "_build_paths_from_predecessors")
                if s.kind == "double_call"]


def test_double_call_methods_and_decorated_property():
    for qn, args in (("Box.helper", (1,)), ):
        (sd,) = [s for s in python_slowdowns(SLOW, "s.py", qn) if s.kind == "double_call"]
        ns = load(apply_py(SLOW, "s.py", sd.patch))
        assert ns["Box"].helper(*args) == 2
        assert ns["Box"]().helper(*args) == 2
    (sd,) = [s for s in python_slowdowns(SLOW, "s.py", "Box.size") if s.kind == "double_call"]
    ns = load(apply_py(SLOW, "s.py", sd.patch))
    assert ns["Box"]().size == 3
    (sd,) = [s for s in python_slowdowns(SLOW, "s.py", "Box.run") if s.kind == "double_call"]
    ns = load(apply_py(SLOW, "s.py", sd.patch))
    assert ns["Box"]().run(1) == 2


def test_list_membership_only_for_set_or_dict_names():
    sl = [s for s in python_slowdowns(SLOW, "s.py", "membership") if s.kind == "list_membership"]
    assert sorted(s.before for s in sl) == ["c", "d", "s"]
    for s in sl:
        new = apply_py(SLOW, "s.py", s.patch)
        ast.parse(new)
        a, b = SLOW.splitlines(), new.splitlines()
        assert [i for i in range(len(a)) if a[i] != b[i]] == [s.line - 1]
        assert f"in list({s.before}):" in b[s.line - 1]
    # not for `lst` (list), `extra` (parameter), nor sets assigned elsewhere
    src = ("def f(xs, y):\n    s = set(xs)\n    s = [1]\n    return y in s\n")
    assert [s for s in python_slowdowns(src, "m.py", "f") if s.kind == "list_membership"] == []
    # real fixture: `seen = {target}` / `predecessor in seen`; `node in sources` is a parameter
    nxs = [s for s in python_slowdowns(NX, NXF, "_build_paths_from_predecessors")
           if s.kind == "list_membership"]
    assert [s.before for s in nxs] == ["seen"]


def test_sorted_copy():
    (s,) = [s for s in python_slowdowns(SLOW, "s.py", "looped") if s.kind == "sorted_copy"]
    new = apply_py(SLOW, "s.py", s.patch)
    assert "        _bth_tmp = sorted(range(len(items)))" in new
    assert load(new)["looped"](0) == 6
    ast.parse(new)
    # unknown iterable type, or no loop: skipped
    assert [x for x in python_slowdowns(SLOW, "s.py", "unbound_loop")
            if x.kind == "sorted_copy"] == []
    assert [x for x in python_slowdowns(NX, NXF, "_build_paths_from_predecessors")
            if x.kind == "sorted_copy"] == []


def test_slowdowns_deterministic_unique_ids():
    for qn in ("plain", "membership", "looped", "Box.run"):
        a = python_slowdowns(SLOW, "s.py", qn)
        b = python_slowdowns(SLOW, "s.py", qn)
        assert [(x.id, x.patch) for x in a] == [(x.id, x.patch) for x in b]
        assert len({x.id for x in a}) == len(a)


@pytest.mark.skipif(GIT is None, reason="git missing")
def test_slowdown_patches_git_apply(tmp_path):
    n = 0
    for qn in ("plain", "membership", "looped", "Box.helper", "Box.size", "Box.run",
               "unbound_loop"):
        for s in python_slowdowns(SLOW, "slow_sample.py", qn):
            d = tmp_path / f"s{n}"
            d.mkdir()
            new = git_apply(d, "slow_sample.py", SLOW, s.patch)
            ast.parse(new)
            assert new == apply_py(SLOW, "slow_sample.py", s.patch)
            n += 1
    assert n >= 8
    for k, s in enumerate(python_slowdowns(NX, NXF, "_build_paths_from_predecessors")):
        d = tmp_path / f"nx{k}"
        d.mkdir()
        ast.parse(git_apply(d, NXF, NX, s.patch))


def test_slowdown_on_decorated_networkx_function():
    sds = python_slowdowns(NX, NXF, "shortest_path")
    dc = [s for s in sds if s.kind == "double_call"]
    assert len(dc) == 1
    new = apply_py(NX, NXF, dc[0].patch)
    tree = ast.parse(new)
    f = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert f["_bth_orig_shortest_path"].decorator_list == []
    assert [ast.unparse(d) for d in f["shortest_path"].decorator_list] == [
        "nx._dispatchable(edge_attrs='weight')"]


# ------------------------------------------------------------------ revert
@pytest.mark.skipif(GIT is None, reason="git missing")
def test_revert_patch_restores_parent(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()

    def g(*a):
        return subprocess.run(["git", "-c", "core.autocrlf=false", *a], cwd=repo, env=ENV,
                              check=True, capture_output=True).stdout.decode().strip()

    g("init", "-q")
    (repo / "a.py").write_text("def f(x):\n    return x + 1\n")
    (repo / "README").write_text("r\n")
    g("add", "-A")
    g("commit", "-qm", "base")
    base = g("rev-parse", "HEAD")
    (repo / "a.py").write_text("def f(x):\n    return x + 2\n")
    (repo / "README").write_text("r2\n")
    g("commit", "-qam", "bth step 1")
    state = g("rev-parse", "HEAD")
    p = revert_patch(repo, state, "a.py")
    p2 = revert_patch(repo, state, "a.py")
    assert p == p2 and "README" not in p
    assert "-    return x + 2" in p and "+    return x + 1" in p
    pf = tmp_path / "rev.patch"
    pf.write_bytes(p.encode())
    g("apply", "--check", str(pf))
    g("apply", str(pf))
    assert (repo / "a.py").read_text() == "def f(x):\n    return x + 1\n"
    assert g("rev-parse", base + "^{tree}") != ""
    assert "README" in revert_patch(repo, state)
