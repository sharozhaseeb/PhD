"""Tests for bth.benchrun (asv-compatible runner; P1, P5, P6, W3-new)."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from bth import benchrun

FIX = Path(__file__).resolve().parent / "fixtures" / "toyrepo"
BD = "benchmarks"
FAST = dict(processes=1, values=2, min_value_time=0.0005, warmup_values=1)


@pytest.fixture(scope="module")
def state(tmp_path_factory):
    d = tmp_path_factory.mktemp("state") / "toyrepo"
    shutil.copytree(FIX, d)
    return d


@pytest.fixture(scope="module")
def cases(state):
    return {c.id: c for c in benchrun.discover(BD, state, sys.executable)}


def test_discover_ids_params_kinds(cases):
    ids = set(cases)
    assert "bench_core.TimeTotal.time_total(10)" in ids
    assert "bench_core.TimeTotal.time_total(100)" in ids
    assert "bench_core.TimeGrid.time_pair(1, 'a')" in ids       # cartesian, repr of values
    assert "bench_core.TimeGrid.time_pair(2, 'b')" in ids
    assert "bench_core.time_add" in ids                          # plain function, no params
    assert "bench_core.time_k(3)" in ids and "bench_core.time_k(4)" in ids  # function attribute params
    assert "bench_other.TimeAcc.time_push" in ids
    assert not any("helper" in i for i in ids)
    c = cases["bench_core.TimeTotal.time_total(100)"]
    assert (c.module, c.cls, c.name, c.kind) == ("bench_core", "TimeTotal", "time_total", "time")
    assert c.params == ["100"] and c.param_names == ["n"] and c.timeout == 30
    assert cases["bench_core.time_k(3)"].timeout == 5            # function attribute
    assert cases["bench_core.time_add"].timeout == benchrun.DEFAULT_TIMEOUT
    assert cases["bench_core.TimeTotal.track_size(10)"].kind == "track"
    assert cases["bench_core.TimeTotal.peakmem_total(10)"].kind == "peakmem"
    assert len(ids) == len(cases)


def test_discover_deterministic(state):
    a = [c.id for c in benchrun.discover(BD, state, sys.executable)]
    b = [c.id for c in benchrun.discover(BD, state, sys.executable)]
    assert a == b == sorted(a, key=lambda x: a.index(x))


def test_harness_process_never_imports_target(state, cases):
    assert "toylib" not in sys.modules and "bench_core" not in sys.modules


def test_measure_basic(state, cases):
    r = benchrun.measure(cases["bench_core.TimeTotal.time_total(100)"], state, sys.executable, **FAST)
    assert r["error"] is None and not r["skipped"]
    assert len(r["samples"]) == 2 and all(s > 0 for s in r["samples"])
    assert r["number"] >= 1 and r["wall_s"] > 0
    assert set(r) >= {"id", "samples", "number", "wall_s", "loadavg_before", "loadavg_after",
                      "skipped", "error"}


def test_measure_two_processes_reuse_number(state, cases):
    r = benchrun.measure(cases["bench_core.time_add"], state, sys.executable,
                         processes=2, values=2, min_value_time=0.0005, warmup_values=0)
    assert len(r["samples"]) == 4 and r["error"] is None


def test_setup_not_implemented_is_skip(state, cases):
    r = benchrun.measure(cases["bench_core.TimeSkip.time_never"], state, sys.executable, **FAST)
    assert r["skipped"] is True and r["samples"] == [] and r["error"] is None


def test_exception_is_error_not_crash(state, cases):
    r = benchrun.measure(cases["bench_other.TimeAcc.time_boom"], state, sys.executable, **FAST)
    assert "RuntimeError" in r["error"] and r["samples"] == []


def test_timeout_kills(state, tmp_path):
    d = tmp_path / "s"
    (d / "b").mkdir(parents=True)
    (d / "b" / "bench_slow.py").write_text(
        "import time\n\ndef time_sleep():\n    time.sleep(30)\n\ntime_sleep.timeout = 1\n")
    c = benchrun.discover("b", d, sys.executable)[0]
    t0 = __import__("time").time()
    r = benchrun.measure(c, d, sys.executable, **FAST)
    assert __import__("time").time() - t0 < 20
    assert "timeout" in r["error"]


def test_profile(state, cases):
    f = benchrun.profile(cases["bench_core.TimeTotal.time_total(10)"], state, sys.executable, root=state)
    assert "toylib/core.py::total" in f
    assert not any(x.startswith("benchmarks/") for x in f)
    f2 = benchrun.profile(cases["bench_other.TimeAcc.time_push"], state, sys.executable, root=state)
    assert {"toylib/core.py::Acc.push", "toylib/core.py::add"} <= f2
    f3 = benchrun.profile(cases["bench_core.TimeTotal.time_total(10)"], state, sys.executable,
                          root=state, native_prefixes=("builtins",))
    assert any(x.startswith("native::") for x in f3)


def test_run_interleaved_rotates(state, cases):
    s2 = state.parent / "other"
    shutil.copytree(state, s2)
    c = [cases["bench_core.time_add"]]
    res = benchrun.run_interleaved(c, [("A", state, sys.executable), ("B", s2, sys.executable)],
                                   repeats=2, **FAST)
    assert [(r["repeat"], r["label"]) for r in res] == [(0, "A"), (0, "B"), (1, "B"), (1, "A")]
    assert all(r["error"] is None and r["samples"] for r in res)


def test_cli_discover_measure_profile_interleave(state, tmp_path):
    def run(*args):
        r = subprocess.run([sys.executable, "-m", "bth.benchrun", *args], capture_output=True, text=True,
                           env={**__import__("os").environ, "PYTHONPATH": str(Path(benchrun.__file__).parents[1])})
        assert r.returncode == 0, r.stderr
    common = ["--state", str(state), "--python", sys.executable, "--bench-dir", BD, "--filter", r"time_add"]
    run("discover", *common, "--out", str(tmp_path / "d.json"))
    assert [c["id"] for c in json.loads((tmp_path / "d.json").read_text())] == ["bench_core.time_add"]
    run("measure", *common, "--out", str(tmp_path / "m.json"), "--processes", "1", "--values", "2",
        "--min-value-time", "0.0005")
    m = json.loads((tmp_path / "m.json").read_text())
    assert len(m) == 1 and len(m[0]["samples"]) == 2
    run("profile", *common, "--out", str(tmp_path / "p.json"))
    assert "toylib/core.py::add" in json.loads((tmp_path / "p.json").read_text())["bench_core.time_add"]
    run("interleave", "--state", f"A={state}", "--state", f"B={state}", "--python", sys.executable,
        "--bench-dir", BD, "--filter", "time_add", "--out", str(tmp_path / "i.json"), "--processes", "1",
        "--values", "2", "--repeats", "2", "--min-value-time", "0.0005")
    assert len(json.loads((tmp_path / "i.json").read_text())) == 4


def test_taskset_prefix(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda n: "/usr/bin/taskset")
    assert benchrun._worker_cmd("py", "measure", {}, cpus="2-5")[:3] == ["taskset", "-c", "2-5"]
    monkeypatch.setattr(shutil, "which", lambda n: None)
    assert benchrun._worker_cmd("py", "measure", {}, cpus="2-5")[0] == "py"
