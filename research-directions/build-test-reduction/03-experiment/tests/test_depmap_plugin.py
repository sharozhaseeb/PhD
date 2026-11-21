"""Tests for bth.depmap_plugin (per-test dependency maps; F1*, F3, W3-new)."""
import json
import sys
from pathlib import Path

pytest_plugins = ["pytester"]

FIX = Path(__file__).resolve().parent / "fixtures"
HARNESS = str(Path(__file__).resolve().parent.parent / "harness")

INNER = '''
import sys, time
import pytest
sys.path.insert(0, r"{fix}")
from toypkg import core

def test_a():
    core.f()

def test_b():
    core.h()

def test_native():
    core.root_of(4.0)

def test_fail():
    core.g()
    assert False

def test_slow():
    time.sleep(0.05)
    core.h()

@pytest.fixture
def fx():
    core.Box(1)
    yield
    core.outer()

def test_fixture(fx):
    pass

@pytest.mark.skip
def test_skipped():
    pass
'''


def _run(pytester, *extra):
    pytester.syspathinsert(HARNESS)
    pytester.makepyfile(test_inner=INNER.format(fix=str(FIX)))
    out = pytester.path / "dm.json"
    res = pytester.runpytest_inprocess(
        "-p", "bth.depmap_plugin", "--rootdir", str(pytester.path), "--bth-depmap-out", str(out), "--bth-root", str(FIX), *extra
    )
    return res, out


def test_depmap_and_outcomes(pytester):
    res, out = _run(pytester, "--bth-native-prefix", "math")
    assert out.exists()
    dm = json.loads(out.read_text())
    C = "toypkg/core.py::"
    assert dm["test_inner.py::test_a"] == sorted([C + "f", C + "g"])
    assert dm["test_inner.py::test_b"] == [C + "h"]
    assert "native::math.sqrt" in dm["test_inner.py::test_native"]
    assert dm["test_inner.py::test_fail"] == [C + "g"]
    # fixture setup and teardown are attributed to the test
    assert {C + "Box.__init__", C + "outer", C + "outer.<locals>.inner"} <= set(
        dm["test_inner.py::test_fixture"]
    )
    # h ran in test_b first (and was DISABLEd) and must still be recorded for test_slow
    assert C + "h" in dm["test_inner.py::test_slow"]
    for deps in dm.values():
        assert deps == sorted(deps)

    oc = json.loads(Path(str(out) + ".outcomes.json").read_text())
    assert oc["test_inner.py::test_a"]["outcome"] == "passed"
    assert oc["test_inner.py::test_fail"]["outcome"] == "failed"
    assert oc["test_inner.py::test_skipped"]["outcome"] == "skipped"
    assert oc["test_inner.py::test_slow"]["duration"] >= 0.05
    assert all(isinstance(v["duration"], float) for v in oc.values())
    assert sys.monitoring.get_tool(sys.monitoring.PROFILER_ID) is None


def test_no_native_without_prefix(pytester):
    res, out = _run(pytester)
    dm = json.loads(out.read_text())
    assert dm["test_inner.py::test_native"] == ["toypkg/core.py::root_of"]
    assert sys.monitoring.get_tool(sys.monitoring.PROFILER_ID) is None


def test_inactive_without_out_option(pytester):
    pytester.syspathinsert(HARNESS)
    pytester.makepyfile(test_x="def test_x():\n    pass\n")
    res = pytester.runpytest_inprocess("-p", "bth.depmap_plugin")
    res.assert_outcomes(passed=1)
    assert sys.monitoring.get_tool(sys.monitoring.PROFILER_ID) is None
