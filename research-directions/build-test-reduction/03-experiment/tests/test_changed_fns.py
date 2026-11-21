"""Tests for bth.changed_fns (spec: Implementer 1)."""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from bth.changed_fns import ChangeSet, Config, changed_functions, parse_unified_diff

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git missing")

FIX = Path(__file__).parent / "fixtures"
ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x", "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@x", "GIT_AUTHOR_DATE": "2020-01-01T00:00:00+00:00",
    "GIT_COMMITTER_DATE": "2020-01-01T00:00:00+00:00",
}


def git(cwd, *args, inp=None):
    return subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=cwd, env=ENV,
                          input=inp, check=True, capture_output=True).stdout


def run(tmp_path, files, cfg=None):
    """files: relpath -> (old|None, new|None) as str or bytes. Commits old, then new."""
    repo = tmp_path / "r"
    repo.mkdir()
    git(repo, "init", "-q")
    for step in (0, 1):
        for rel, pair in files.items():
            p = repo / rel
            data = pair[step]
            if data is None:
                if p.exists():
                    p.unlink()
            else:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(data if isinstance(data, bytes) else data.encode())
        (repo / "keep.txt").write_text(str(step))
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", f"c{step}")
    return changed_functions(repo, "HEAD~1", "HEAD", cfg or Config())


NATIVE_CFG = Config(
    native_sources={"bottleneck/src/reduce_template.c": "bottleneck.reduce"},
    native_headers=["*.h", "bn_template.py"],
    build_config=["setup.py", "pyproject.toml", "meson.build"],
)


def test_parse_unified_diff_fixture():
    d = parse_unified_diff((FIX / "bn_0819d3a.diff").read_text())
    old, new = d["bottleneck/src/reduce_template.c"]
    assert 125 in new            # BN_OPT_3 added at new line 125
    assert all(isinstance(x, int) for x in old | new)
    assert old == {129, 130, 131} and len(new) == 18


def test_parse_pure_addition_and_zero_context():
    text = "--- a/x.py\n+++ b/x.py\n@@ -3,0 +4,2 @@\n+a\n+b\n@@ -10,1 +13,0 @@\n-gone\n"
    d = parse_unified_diff(text)
    assert d["x.py"] == ({10}, {4, 5})


def test_bottleneck_fixture_only_nansum(tmp_path):
    before = (FIX / "bn_reduce_template_before.c").read_bytes()
    after = (FIX / "bn_reduce_template_after.c").read_bytes()
    cs = run(tmp_path, {"bottleneck/src/reduce_template.c": (before, after)}, NATIVE_CFG)
    assert isinstance(cs, ChangeSet)
    assert cs.functions == frozenset({"native::bottleneck.reduce.nansum"})
    assert cs.header_edits == frozenset()
    assert cs.native_files == frozenset({"bottleneck/src/reduce_template.c"})
    assert not cs.build_config_changed and cs.unmapped_native == frozenset()


def test_networkx_fixture_only_one_function(tmp_path):
    rel = "networkx/algorithms/shortest_paths/generic.py"
    repo = tmp_path / "r"
    repo.mkdir()
    git(repo, "init", "-q")
    (repo / rel).parent.mkdir(parents=True)
    (repo / rel).write_bytes((FIX / "nx_generic_before.py").read_bytes())
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "a")
    git(repo, "apply", "-", inp=(FIX / "nx_7f7afab1.diff").read_bytes())
    git(repo, "commit", "-qam", "b")
    cs = changed_functions(repo, "HEAD~1", "HEAD", Config())
    assert cs.functions == frozenset({rel + "::_build_paths_from_predecessors"})
    assert cs.module_level_files == frozenset()
    assert cs.files == frozenset({rel})


OLD_PY = '''import os

X = 1


def a():
    # comment
    return 1


class K:
    attr = 1

    @staticmethod
    def m(x):
        def inner(y):
            return y
        return inner(x)

    def n(self):
        return 2


def gone():
    return 0
'''


def sub(tmp_path, name):
    d = tmp_path / name
    d.mkdir()
    return d


def test_python_comment_and_blank_changes_ignored(tmp_path):
    new = OLD_PY.replace("# comment", "# other comment").replace("\n\nX = 1", "\n\n\nX = 1")
    cs = run(tmp_path, {"p/m.py": (OLD_PY, new)})
    assert cs.functions == frozenset() and cs.module_level_files == frozenset()


def test_python_nested_qualname(tmp_path):
    cs = run(tmp_path, {"p/m.py": (OLD_PY, OLD_PY.replace("return y", "return y + 1"))})
    assert cs.functions == {"p/m.py::K.m.<locals>.inner", "p/m.py::K.m"}


def test_python_decorator_counts(tmp_path):
    cs = run(tmp_path, {"p/m.py": (OLD_PY, OLD_PY.replace("@staticmethod", "@classmethod"))})
    assert cs.functions == {"p/m.py::K.m"}


def test_python_module_level_and_class_body(tmp_path):
    new = OLD_PY.replace("X = 1", "X = 2").replace("attr = 1", "attr = 3")
    cs = run(tmp_path, {"p/m.py": (OLD_PY, new)})
    assert cs.functions == {"p/m.py::<module>"}
    assert cs.module_level_files == {"p/m.py"}


def test_python_deleted_and_added_functions(tmp_path):
    new = OLD_PY.replace("def gone():\n    return 0\n", "def fresh():\n    return 5\n")
    cs = run(tmp_path, {"p/m.py": (OLD_PY, new)})
    assert cs.functions == {"p/m.py::gone", "p/m.py::fresh"}


def test_new_and_deleted_file(tmp_path):
    cs = run(tmp_path, {"p/new.py": (None, "def f():\n    return 1\n")})
    assert cs.functions == {"p/new.py::f"}
    cs = run(sub(tmp_path, "d"), {"p/old.py": ("def g():\n    return 1\n", None)})
    assert cs.functions == {"p/old.py::g"}


def test_build_config_headers_and_native_files(tmp_path):
    files = {
        "setup.py": ("a = 1\n", "a = 2\n"),
        "bottleneck/src/bottleneck.h": ("int x;\n", "int y;\n"),
        "bottleneck/src/bn_template.py": ("a = 1\n", "a = 2\n"),
    }
    cs = run(tmp_path, files, NATIVE_CFG)
    assert cs.build_config_changed
    assert cs.header_edits == {"bottleneck/src/bottleneck.h", "bottleneck/src/bn_template.py"}
    assert cs.functions == frozenset()
    assert "setup.py" in cs.files


C_OLD = """/* c */
#define FOO 1

BN_OPT_3
REDUCE_ALL(nansum, DTYPE0) {
    int a = 0;
    return a;
}

static PyObject *
helper_fn(int x)
{
    return x;
}

PyObject* py_other(int z) {
    if (z) {
        z++; /* } */
    }
    return z;
}
"""


def c_cfg(**kw):
    return Config(native_sources={"src/x.c": "ext.mod"}, **kw)


def test_c_macro_attach_vs_header_edit(tmp_path):
    new = C_OLD.replace("BN_OPT_3", "BN_OPT_2")
    cs = run(tmp_path, {"src/x.c": (C_OLD, new)}, c_cfg())
    assert cs.functions == {"native::ext.mod.nansum"} and not cs.header_edits
    cs = run(sub(tmp_path, "b"), {"src/x.c": (C_OLD, C_OLD.replace("FOO 1", "FOO 2"))}, c_cfg())
    assert cs.header_edits == {"src/x.c"} and not cs.functions


def test_c_plain_header_mapping_and_unmapped(tmp_path):
    new = C_OLD.replace("z++;", "z += 2;")
    cs = run(tmp_path, {"src/x.c": (C_OLD, new)}, c_cfg())          # no regex: unmapped
    assert cs.functions == frozenset() and cs.unmapped_native == {"py_other"}
    cs = run(sub(tmp_path, "b"), {"src/x.c": (C_OLD, new)}, c_cfg(native_name_regex=r"^py_(\w+)$"))
    assert cs.functions == {"native::ext.mod.other"} and not cs.unmapped_native
    new2 = C_OLD.replace("return x;", "return x + 1;")             # brace on the next line
    cs = run(sub(tmp_path, "c"), {"src/x.c": (C_OLD, new2)}, c_cfg(native_name_regex=r"^(\w+)$"))
    assert cs.functions == {"native::ext.mod.helper_fn"}


def test_changeset_frozen():
    cs = ChangeSet(frozenset(), frozenset(), frozenset(), frozenset(), frozenset(), False, frozenset())
    with pytest.raises(Exception):
        cs.functions = frozenset({"x"})
