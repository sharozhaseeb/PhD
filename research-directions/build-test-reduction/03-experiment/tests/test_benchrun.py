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


def test_run_interleaved_checkpoints_and_resumes(tmp_path, monkeypatch):
    """Each finished (case, state, repeat) run is appended to a JSONL checkpoint; a resume skips them."""
    from types import SimpleNamespace
    calls = []

    def fake_measure(case, sd, py, **kw):
        calls.append((case.id, str(sd)))
        return {"id": case.id, "samples": [1.0], "error": None, "skipped": False}

    monkeypatch.setattr(benchrun, "measure", fake_measure)
    cs = [SimpleNamespace(id="c1"), SimpleNamespace(id="c2")]
    st = [("A", "a", "py"), ("B", "b", "py")]
    ck = tmp_path / "ck.jsonl"
    full = benchrun.run_interleaved(cs, st, 2, checkpoint=ck)
    assert len(full) == 8 and len(ck.read_text().splitlines()) == 8
    # simulate a kill after 3 runs: keep 3 lines, resume
    lines = ck.read_text().splitlines()[:3]
    ck.write_text("\n".join(lines) + "\n")
    calls.clear()
    res = benchrun.run_interleaved(cs, st, 2, checkpoint=ck)
    assert len(calls) == 5 and len(res) == 8
    assert [(r["id"], r["label"], r["repeat"]) for r in res] == [(r["id"], r["label"], r["repeat"]) for r in full]


def test_make_gate_postpones_then_passes(tmp_path):
    """Night plan 2026-11-22: the per-run gate waits while load or Windows CPU is high, logs each postponement."""
    import time as _t
    loads = iter([3.0, 2.0, 1.2])
    clock = {"t": 0.0}
    tel = tmp_path / "win.jsonl"
    tel.write_text(json.dumps({"epoch": _t.time(), "cpu": 5.0}) + "\n")
    log = tmp_path / "driver.log"
    g = benchrun.make_gate(1.5, 20, str(tel), max_wait_s=600, poll_s=20, log=str(log),
                           _load=lambda: next(loads), _sleep=lambda s: clock.__setitem__("t", clock["t"] + s),
                           _now=lambda: clock["t"])
    r = g()
    assert r["ok"] and r["load1"] == 1.2 and r["wincpu"] == 5.0 and r["waited_s"] == 40
    assert log.read_text().count("gate: run postponed") == 2


def test_make_gate_gives_up_and_labels(tmp_path):
    import time as _t
    clock = {"t": 0.0}
    tel = tmp_path / "win.jsonl"
    tel.write_text(json.dumps({"epoch": _t.time(), "cpu": 55.0}) + "\n")
    g = benchrun.make_gate(1.5, 20, str(tel), max_wait_s=60, poll_s=20, _load=lambda: 0.5,
                           _sleep=lambda s: clock.__setitem__("t", clock["t"] + s), _now=lambda: clock["t"])
    r = g()
    assert r["ok"] is False and r["wincpu"] == 55.0 and r["waited_s"] >= 60
    # stale telemetry is ignored (no Windows reading -> load only)
    tel.write_text(json.dumps({"epoch": _t.time() - 3600, "cpu": 99.0}) + "\n")
    assert benchrun.make_gate(1.5, 20, str(tel), _load=lambda: 0.5)()["ok"] is True


def test_run_interleaved_records_pre_gate(monkeypatch):
    from types import SimpleNamespace
    monkeypatch.setattr(benchrun, "measure", lambda c, sd, py, **kw: {"id": c.id, "samples": [1.0]})
    res = benchrun.run_interleaved([SimpleNamespace(id="c")], [("A", "a", "py"), ("B", "b", "py")], 2,
                                   pre_run=lambda: {"ok": True, "load1": 0.3})
    assert len(res) == 4 and all(r["pre_gate"]["ok"] for r in res)


def test_measure_cached_one_worker_per_module_and_samples(state, cases, tmp_path, monkeypatch):
    """E5 CACHED mode: one worker (one import) per module, `values` samples per case, phase timings recorded."""
    calls = []
    real = benchrun._run_worker

    def spy(python, op, payload, sd, timeout, cpus=None):
        calls.append((op, len(payload.get("cases", []))))
        return real(python, op, payload, sd, timeout, cpus)

    monkeypatch.setattr(benchrun, "_run_worker", spy)
    cs = [c for c in cases.values() if c.kind == "time"]
    res = benchrun.measure_cached(cs, state, sys.executable, values=4, min_value_time=0.0005)
    mods = {c.module for c in cs}
    assert len(calls) == len(mods) and all(op == "measure_group" for op, _ in calls)
    assert len(res) == len(cs)
    ok = [r for r in res if not r.get("error") and not r.get("skipped")]
    assert ok and all(len(r["samples"]) == 4 and r["number"] >= 1 for r in ok)
    assert all(r["module_import_s"] is not None and "setup_s" in r and "loop_s" in r for r in ok)


def test_measure_cached_checkpoint_resume(state, cases, tmp_path, monkeypatch):
    cs = [c for c in cases.values() if c.kind == "time"]
    ck = tmp_path / "cached.jsonl"
    full = benchrun.measure_cached(cs, state, sys.executable, values=2, min_value_time=0.0005, checkpoint=ck)
    lines = ck.read_text().splitlines()
    assert len(lines) == len({c.module for c in cs})
    ck.write_text(lines[0] + "\n")                       # keep only the first module, as after a kill
    calls = []
    real = benchrun._run_worker
    monkeypatch.setattr(benchrun, "_run_worker", lambda *a, **k: (calls.append(1), real(*a, **k))[1])
    res = benchrun.measure_cached(cs, state, sys.executable, values=2, min_value_time=0.0005, checkpoint=ck)
    assert len(calls) == len({c.module for c in cs}) - 1 and len(res) == len(full)
