"""Tests for bth.monitor (sys.monitoring recorder; rules F1*, W3-new)."""
import importlib
import sys
from pathlib import Path

import pytest

from bth.monitor import Recorder

FIX = Path(__file__).resolve().parent / "fixtures"
if str(FIX) not in sys.path:
    sys.path.insert(0, str(FIX))
from toypkg import core  # noqa: E402

CORE = "toypkg/core.py"


@pytest.fixture(autouse=True)
def _no_leak():
    yield
    # No tool id of ours may stay registered after a test.
    for i in range(6):
        assert sys.monitoring.get_tool(i) is None or i == sys.monitoring.COVERAGE_ID, (
            f"leaked tool id {i}: {sys.monitoring.get_tool(i)}"
        )


def test_records_python_functions():
    r = Recorder(FIX, ())
    r.start()
    try:
        core.f()
    finally:
        got = r.stop()
    assert got == {f"{CORE}::f", f"{CORE}::g"}


def test_method_and_nested_and_class_qualnames():
    r = Recorder(FIX, ())
    r.start()
    try:
        core.Box(3).size()
        core.outer()
    finally:
        got = r.stop()
    assert f"{CORE}::Box.__init__" in got
    assert f"{CORE}::Box.size" in got
    assert f"{CORE}::outer" in got
    assert f"{CORE}::outer.<locals>.inner" in got


def test_module_level_code():
    r = Recorder(FIX, ())
    r.start()
    try:
        importlib.reload(core)
    finally:
        got = r.stop()
    assert f"{CORE}::<module>" in got


def test_ignores_code_outside_root_and_excluded_dirs(tmp_path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "pkg").mkdir()
    ns = {}
    for rel, fn in (("tests/t_mod.py", "tf"), ("pkg/m.py", "pf")):
        p = tmp_path / rel
        p.write_text(f"def {fn}():\n    return 1\n")
        exec(compile(p.read_text(), str(p), "exec"), ns)
    r = Recorder(tmp_path, ())
    r.start()
    try:
        ns["tf"]()
        ns["pf"]()
        core.f()  # outside the tmp_path root
    finally:
        got = r.stop()
    assert got == {"pkg/m.py::pf"}


def test_native_call_with_prefix():
    r = Recorder(FIX, ("math",))
    r.start()
    try:
        core.root_of(4.0)
        len([1])  # builtins is not under the prefix
    finally:
        got = r.stop()
    assert "native::math.sqrt" in got
    assert not any(x.startswith("native::builtins") for x in got)
    assert f"{CORE}::root_of" in got


def test_no_native_without_prefix():
    r = Recorder(FIX, ())
    r.start()
    try:
        core.root_of(4.0)
    finally:
        got = r.stop()
    assert got == {f"{CORE}::root_of"}


def test_native_call_site_keeps_firing_after_reset():
    """CALL is never DISABLEd: the same call site reports again after reset."""
    r = Recorder(FIX, ("math",))
    r.start()
    try:
        core.root_of(4.0)
        r.reset()
        core.root_of(9.0)
        got = r.snapshot()
    finally:
        r.stop()
    assert "native::math.sqrt" in got


def test_native_bound_method_and_descriptor():
    r = Recorder(FIX, ("builtins",))
    r.start()
    try:
        "a,b".split(",")
        str.join(",", ["a"])
        len("x")
    finally:
        got = r.stop()
    assert "native::builtins.len" in got
    assert "native::builtins.str.split" in got
    assert "native::builtins.str.join" in got


def test_reset_between_tests_restart_events():
    """B must contain h even though h already ran (and was DISABLEd) during A."""
    r = Recorder(FIX, ())
    r.start()
    try:
        core.f()  # test A: f -> g
        core.h()  # h is also called during A
        a = r.snapshot()
        r.reset()
        core.h()  # test B
        b = r.snapshot()
    finally:
        r.stop()
    assert {f"{CORE}::f", f"{CORE}::g", f"{CORE}::h"} <= a
    assert f"{CORE}::h" in b
    assert f"{CORE}::f" not in b and f"{CORE}::g" not in b


def test_disabled_events_do_not_refire_without_restart():
    """Documents why reset() must call restart_events()."""
    r = Recorder(FIX, ())
    r.start()
    try:
        core.h()
        r._seen.clear()  # clear the set but do not restart events
        core.h()
        assert r.snapshot() == frozenset()
    finally:
        r.stop()


def test_stop_frees_tool_and_a_second_recorder_works():
    r1 = Recorder(FIX, ())
    r1.start()
    core.f()
    r1.stop()
    assert sys.monitoring.get_tool(sys.monitoring.PROFILER_ID) is None
    r2 = Recorder(FIX, ())
    r2.start()
    try:
        core.f()
    finally:
        got = r2.stop()
    assert got == {f"{CORE}::f", f"{CORE}::g"}


def test_falls_back_to_free_tool_id_when_profiler_taken():
    sys.monitoring.use_tool_id(sys.monitoring.PROFILER_ID, "squatter")
    try:
        r = Recorder(FIX, ())
        r.start()
        try:
            assert r.tool_id != sys.monitoring.PROFILER_ID
            core.f()
        finally:
            got = r.stop()
        assert f"{CORE}::f" in got
    finally:
        sys.monitoring.free_tool_id(sys.monitoring.PROFILER_ID)


def test_stop_without_start_is_safe():
    assert Recorder(FIX, ()).stop() == frozenset()
