"""Tests for bth.staticgraph (A5 STATIC-BENCH; W3-new 'static benchmark RTS')."""
from pathlib import Path

import pytest

from bth.staticgraph import build

ROOT = Path(__file__).resolve().parent / "fixtures" / "toystatic"
P = "toystatic/"


@pytest.fixture(scope="module")
def reach():
    return build(ROOT, ["toystatic"], ROOT / "benchmarks")


def test_keys(reach):
    assert set(reach) == {
        "bench_toy.TimeX.time_foo",
        "bench_toy.TimeX.time_run",
        "bench_toy.TimeX.time_dyn",
        "bench_toy.time_bar",
    }


def test_two_hop_chain_through_reexport(reach):
    r = reach["bench_toy.TimeX.time_foo"]
    assert P + "a.py::foo" in r
    assert P + "b.py::bar" in r  # bench -> foo -> bar
    assert P + "a.py::unrelated" not in r
    assert P + "b.py::lonely" not in r


def test_module_level_nodes_of_imported_modules(reach):
    r = reach["bench_toy.TimeX.time_foo"]
    assert P + "__init__.py::<module>" in r
    assert P + "a.py::<module>" in r and P + "b.py::<module>" in r


def test_self_method_and_instance_calls(reach):
    r = reach["bench_toy.TimeX.time_run"]
    assert P + "util.py::Engine.run" in r
    assert P + "util.py::Engine.step" in r  # via self.step()
    assert P + "util.py::leaf" in r  # step -> leaf
    assert P + "util.py::make_and_run" not in r


def test_dynamic_getattr_is_conservative_module_edge(reach):
    r = reach["bench_toy.TimeX.time_dyn"]
    assert P + "dyn.py::dispatch" in r
    assert {P + "targets.py::t1", P + "targets.py::t2"} <= r


def test_function_level_bench_with_local_import(reach):
    r = reach["bench_toy.time_bar"]
    assert P + "b.py::bar" in r
    assert P + "b.py::lonely" not in r
    assert P + "a.py::unrelated" not in r


def test_non_bench_helper_not_a_key(reach):
    assert not any("helper" in k for k in reach)
    # the helper's call to util.leaf must not leak into other benchmarks
    assert P + "util.py::leaf" not in reach["bench_toy.TimeX.time_foo"]


def test_deterministic(reach):
    assert build(ROOT, ["toystatic"], ROOT / "benchmarks") == reach


def test_bench_files_not_in_reach(reach):
    for s in reach.values():
        assert not any(x.startswith("benchmarks/") for x in s)


def test_star_reexport_respects_all(tmp_path):
    pk = tmp_path / "pk"
    pk.mkdir()
    (pk / "__init__.py").write_text("from .impl import *\n")
    (pk / "impl.py").write_text(
        "__all__ = ['pub']\n\ndef pub():\n    return _hid()\n\ndef _hid():\n    return 1\n\ndef other():\n    return 2\n"
    )
    bd = tmp_path / "bm"
    bd.mkdir()
    (bd / "b.py").write_text("import pk\n\ndef time_x():\n    pk.pub()\n")
    r = build(tmp_path, ["pk"], bd)["b.time_x"]
    assert {"pk/impl.py::pub", "pk/impl.py::_hid"} <= r
    assert "pk/impl.py::other" not in r
