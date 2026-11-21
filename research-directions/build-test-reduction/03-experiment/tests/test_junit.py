"""Tests for bth.junit using a real junit file produced by an inner pytester run."""
import pytest

from bth import junit

pytest_plugins = ["pytester"]

BODY = '''
import pytest

def test_a():
    pass

class TestC:
    def test_b(self):
        assert 0

@pytest.mark.parametrize("x", [1, "a.b"])
def test_p(x):
    pass

@pytest.fixture
def bad():
    raise ValueError

def test_err(bad):
    pass

@pytest.mark.skip
def test_sk():
    pass
'''


@pytest.fixture
def real(pytester):
    sub = pytester.mkpydir("pkg")
    (sub / "sub").mkdir()
    (sub / "sub" / "__init__.py").write_text("")
    (sub / "sub" / "test_m.py").write_text(BODY)
    pytester.runpytest_subprocess("pkg", "--junitxml=o.xml", "-p", "no:cacheprovider")
    return pytester.path


def test_real_file_with_rootdir(real):
    got = junit.parse(real / "o.xml", rootdir=real)
    m = "pkg/sub/test_m.py"
    assert set(got) == {f"{m}::test_a", f"{m}::TestC::test_b", f"{m}::test_p[1]",
                        f"{m}::test_p[a.b]", f"{m}::test_err", f"{m}::test_sk"}
    assert got[f"{m}::test_a"]["outcome"] == "passed"
    assert got[f"{m}::TestC::test_b"]["outcome"] == "failed"
    assert got[f"{m}::test_err"]["outcome"] == "failed"       # fixture error
    assert got[f"{m}::test_sk"]["outcome"] == "skipped"
    assert all(isinstance(v["duration"], float) for v in got.values())


def test_real_file_heuristic_without_rootdir(real):
    assert junit.parse(real / "o.xml") == junit.parse(real / "o.xml", rootdir=real)


def test_accepts_xml_text_and_merges_duplicates():
    xml = ('<testsuites><testsuite>'
           '<testcase classname="a.test_x" name="test_1" time="0.5"/>'
           '<testcase classname="a.test_x" name="test_1" time="0.25"><error/></testcase>'
           '</testsuite></testsuites>')
    got = junit.parse(xml)
    assert got == {"a/test_x.py::test_1": {"outcome": "failed", "duration": 0.75}}


def test_heuristic_class_without_test_prefix_module():
    assert junit.nodeid_for("pkg.mod.Klass", "t") == "pkg/mod.py::Klass::t"
