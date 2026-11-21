"""Tests for bth.orchestrate (CLI wrappers) and the xdist worker-file change in depmap_plugin."""
import csv
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from bth import orchestrate as O

pytest_plugins = ["pytester"]

FIX = Path(__file__).resolve().parent / "fixtures" / "toyrepo"
HARNESS = str(Path(__file__).resolve().parent.parent / "harness")
HAVE_GIT = shutil.which("git") is not None

TOML = """
[repo]
clone = "{clone}"
[replay]
base = "{base}"
src_pathspec = ["toylib"]
[tests]
cmd = ["python", "-m", "pytest", "tests/fx_core.py", "-p", "no:cacheprovider", "-q"]
[bench]
dir = "benchmarks"
[native]
sources = {{}}
build_config = ["setup.py"]
"""


@pytest.fixture
def toy(tmp_path):
    d = tmp_path / "state"
    shutil.copytree(FIX, d)
    cfg = tmp_path / "toy.toml"
    cfg.write_text(TOML.format(clone="x", base="x"))
    exp = tmp_path / "exp"
    return d, cfg, exp


def run_cli(exp, *args):
    return O.main(["--exp-root", str(exp), *map(str, args)])


def load(exp, *parts):
    return json.loads(Path(exp, "results", "raw", "toy", *parts).read_text(encoding="utf-8"))


def check_meta(m):
    assert set(m) >= {"repo", "state_sha", "harness_tree_hash", "cmd", "python", "platform", "started", "ended"}
    assert m["repo"] == "toy" and len(m["harness_tree_hash"]) == 64


def test_harness_tree_hash_is_sorted_path_content_hash():
    h = hashlib.sha256()
    for p in sorted((Path(HARNESS) / "bth").glob("*.py")):
        h.update(f"{p.name}\0{hashlib.sha256(p.read_bytes()).hexdigest()}\n".encode())
    assert O.harness_tree_hash() == h.hexdigest()
    assert O.harness_tree_hash() == O.harness_tree_hash()


def test_oracle_tests(toy):
    d, cfg, exp = toy
    assert run_cli(exp, "oracle-tests", "--config", cfg, "--state-dir", d, "--label", "S0", "--junit") == 0
    r = load(exp, "oracle-tests", "S0.json")
    check_meta(r["meta"])
    assert r["exit_code"] == 1 and r["wall_s"] > 0 and "-n" not in r["test_cmd"]
    t = r["tests"]
    assert t["tests/fx_core.py::test_add"]["outcome"] == "passed"
    assert t["tests/fx_core.py::TestAcc::test_push[2]"]["outcome"] == "passed"
    assert t["tests/fx_core.py::test_bad"]["outcome"] == "failed"
    assert len(t) == 4
    assert Path(exp, "results", "raw", "toy", "oracle-tests", "S0.junit.xml").exists()


def test_oracle_tests_drops_xml_without_flag(toy):
    d, cfg, exp = toy
    run_cli(exp, "oracle-tests", "--config", cfg, "--state-dir", d, "--label", "S1")
    assert not Path(exp, "results", "raw", "toy", "oracle-tests", "S1.junit.xml").exists()


def test_depmap(toy):
    d, cfg, exp = toy
    assert run_cli(exp, "depmap", "--config", cfg, "--state-dir", d, "--label", "S0") == 0
    r = load(exp, "depmap", "S0.json")
    check_meta(r["meta"])
    assert "toylib/core.py::add" in r["deps"]["tests/fx_core.py::test_add"]
    assert "toylib/core.py::total" in r["deps"]["tests/fx_core.py::test_bad"]
    assert "toylib/core.py::total" not in r["deps"]["tests/fx_core.py::test_add"]
    assert r["outcomes"]["tests/fx_core.py::test_bad"]["outcome"] == "failed"
    assert not (Path(exp, "results", "raw", "toy", "depmap", "S0.parts")).exists()


def test_merge_depmap_parts_xdist_worker_files(tmp_path):
    out = tmp_path / "dm.json"
    out.write_text(json.dumps({}))
    Path(str(out) + ".outcomes.json").write_text(json.dumps({}))
    for w, n in (("gw0", "a"), ("gw1", "b")):
        Path(f"{out}.{w}").write_text(json.dumps({n: ["f::x"]}))
        Path(f"{out}.{w}.outcomes.json").write_text(json.dumps({n: {"outcome": "passed", "duration": 0.1}}))
    deps, outc = O.merge_depmap_parts(out)
    assert deps == {"a": ["f::x"], "b": ["f::x"]} and set(outc) == {"a", "b"}


def test_plugin_writes_worker_file_under_xdist_env(pytester, monkeypatch):
    monkeypatch.setenv("PYTEST_XDIST_WORKER", "gw3")
    pytester.syspathinsert(HARNESS)
    pytester.makepyfile(test_w="def test_x():\n    pass\n")
    out = pytester.path / "dm.json"
    pytester.runpytest_inprocess("-p", "bth.depmap_plugin", "--bth-depmap-out", str(out),
                                 "--bth-root", str(pytester.path))
    assert Path(str(out) + ".gw3").exists() and Path(str(out) + ".gw3.outcomes.json").exists()
    assert not out.exists()


def test_bench_and_profile(toy):
    d, cfg, exp = toy
    assert run_cli(exp, "bench", "--config", cfg, "--state-dir", d, "--label", "b0", "--filter",
                   r"time_add|TimeTotal\.time_total\(10\)", "--processes", "1", "--values", "2",
                   "--min-value-time", "0.0005") == 0
    r = load(exp, "bench", "b0.json")
    check_meta(r["meta"])
    assert sorted(x["id"] for x in r["results"]) == ["bench_core.TimeTotal.time_total(10)", "bench_core.time_add"]
    assert all(len(x["samples"]) == 2 for x in r["results"])
    assert run_cli(exp, "profile", "--config", cfg, "--state-dir", d, "--label", "p0", "--filter",
                   r"time_push|time_boom|time_add") == 0
    p = load(exp, "profile", "p0.json")
    assert "toylib/core.py::Acc.push" in p["profiles"]["bench_other.TimeAcc.time_push"]
    assert "bench_other.TimeAcc.time_boom" in p["errors"]


def _git(cwd, *a):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@x"}
    return subprocess.run(["git", "-c", "commit.gpgsign=false", *a], cwd=cwd, env=env, check=True,
                          capture_output=True, text=True).stdout.strip()


@pytest.mark.skipif(not HAVE_GIT, reason="git missing")
def test_states_then_changes(tmp_path):
    src = tmp_path / "src"
    shutil.copytree(FIX / "toylib", src / "toylib")
    _git(src, "init", "-q")
    _git(src, "add", "-A")
    _git(src, "commit", "-qm", "base")
    base = _git(src, "rev-parse", "HEAD")
    core = src / "toylib" / "core.py"
    core.write_text(core.read_text().replace("return sum(i for i in range(n))", "return n * (n - 1) // 2"))
    _git(src, "commit", "-qam", "perf: faster total")
    sha1 = _git(src, "rev-parse", "HEAD")
    core.write_text(core.read_text().replace("self.v = 0", "self.v = 0  # init\n        self.w = 1"))
    _git(src, "commit", "-qam", "perf: acc")
    sha2 = _git(src, "rev-parse", "HEAD")
    cfg = tmp_path / "toy.toml"
    cfg.write_text(TOML.format(clone=str(src).replace("\\", "/"), base=base))
    exp = tmp_path / "exp"
    (exp / "edits").mkdir(parents=True)
    (exp / "edits" / "toy.candidates.json").write_text(json.dumps([
        {"sha": sha1, "date": "2026-01-01T00:00:00+00:00", "qualifies": True},
        {"sha": sha2, "date": "2026-01-02T00:00:00+00:00", "qualifies": True},
        {"sha": "0" * 40, "qualifies": False}]))
    wd = tmp_path / "wd"
    assert run_cli(exp, "states", "--config", cfg, "--workdir", wd) == 0
    st = json.loads((exp / "edits" / "toy.states.json").read_text())
    check_meta(st["meta"])
    assert [r["status"] for r in st["records"]] == ["applied", "applied"]
    assert run_cli(exp, "changes", "--config", cfg, "--workdir", wd) == 0
    ch = load(exp, "changes", "changes.json")
    assert [s["functions"] for s in ch["steps"]] == [["toylib/core.py::total"], ["toylib/core.py::Acc.__init__"]]
    assert ch["steps"][0]["from"] == base and ch["steps"][1]["from"] == ch["steps"][0]["to"]


# ---------------------------------------------------------------- simulate
def _write_inputs(d: Path):
    d.mkdir()
    A, B = "m.py::a", "m.py::b"

    def w(name, obj):
        (d / name).write_text(json.dumps(obj))
    w("changes.json", {"steps": [{"functions": [A], "files": ["m.py"]},
                                 {"functions": [B], "files": ["n.py"]},
                                 {"functions": [], "files": ["z.py"]}]})
    w("durations.json", {"tests": {"t1": 2.0, "t2": 3.0}, "benches": {"b1": 5.0},
                         "build": {"clean": 10.0, "incremental": 1.0}, "overhead": {"OURS": 0.5}})
    w("depmaps.json", {"0": {"t1": [A], "t2": [B]}})
    w("profiles.json", {"0": {"b1": [A]}})
    w("static_reach.json", {"b1": [A]})
    w("modules.json", {"module_of_test": {"t1": "m.py", "t2": "n.py"}, "module_of_bench": {"b1": "m.py"},
                       "module_functions": {"m.py": [A], "n.py": [B]},
                       "testmon_selection": {"1": ["t1"], "2": ["t2"], "3": []}})
    w("faults.json", [
        {"id": "f_a", "kind": "mutant", "step": 1, "extra_changed": [], "kill_tests": ["t1"]},
        {"id": "f_latent", "kind": "latent", "step": 1, "visible_from": 2, "extra_changed": [A],
         "kill_tests": {"2": ["t2"]}},
        {"id": "f_slow", "kind": "slowdown", "step": 1, "extra_changed": [], "regress_benches": ["b1"]},
    ])


def test_simulate(tmp_path):
    inp = tmp_path / "in"
    _write_inputs(inp)
    out = tmp_path / "o" / "sim.csv"
    arms = ["FULL", "INC", "TESTMON", "CHANGED_MODULE", "STATIC_BENCH", "OURS", "OURS:T=1,accumulate=false",
            "PERIODIC:inner=INC,k=2"]
    paths = O.simulate(inp, out, arms)
    rows = list(csv.DictReader(open(paths[0], encoding="utf-8")))
    assert {r["arm"] for r in rows} == set(arms) and len(rows) == 3 * len(arms)
    full = [r for r in rows if r["arm"] == "FULL"]
    assert all(r["full_check"] == "1" and r["n_tests"] == "2" and float(r["build_s"]) == 10.0 for r in full)
    assert float(full[0]["total_s"]) == 10 + 5 + 5 and float(full[2]["cumulative_s"]) == 60
    ours = [r for r in rows if r["arm"] == "OURS"]
    assert [r["n_tests"] for r in ours[:2]] == ["1", "2"]       # accumulation: step 2 re-selects t1 as well
    assert ours[2]["full_check"] == "1"                          # C3 final check
    assert float(ours[0]["overhead_s"]) == 0.5
    faults = {(r["arm"], r["fault_id"]): r for r in csv.DictReader(open(paths[1], encoding="utf-8"))}
    assert faults[("FULL", "f_a")]["by"] == "full_check" and faults[("FULL", "f_a")]["delay"] == "0"
    assert faults[("OURS", "f_a")]["by"] == "selection"
    assert faults[("INC", "f_a")]["by"] == "selection"
    assert faults[("TESTMON", "f_a")]["by"] == "selection"
    assert faults[("CHANGED_MODULE", "f_slow")]["by"] == "selection"
    assert faults[("OURS", "f_slow")]["by"] == "selection"
    assert faults[("OURS", "f_latent")]["detected_step"] == "2"
    assert faults[("PERIODIC:inner=INC,k=2", "f_a")]["by"] == "selection"
    summ = {r["arm"]: r for r in csv.DictReader(open(paths[2], encoding="utf-8"))}
    assert summ["FULL"]["k_missed"] == "0" and summ["FULL"]["n_faults"] == "3"
    assert float(summ["FULL"]["total_cost_s"]) == 60


def test_simulate_cli_and_config_arms(tmp_path):
    inp = tmp_path / "in"
    _write_inputs(inp)
    cfg = tmp_path / "c.toml"
    cfg.write_text('[simulate]\narms = ["FULL", "INC"]\n')
    out = tmp_path / "sim.csv"
    assert O.main(["--exp-root", str(tmp_path), "simulate", "--config", str(cfg), "--inputs", str(inp),
                   "--out", str(out)]) == 0
    assert {r["arm"] for r in csv.DictReader(open(out, encoding="utf-8"))} == {"FULL", "INC"}
    assert Path(str(out) + ".faults.csv").exists() and Path(str(out) + ".summary.csv").exists()


def test_parse_arm_rejects_unknown():
    with pytest.raises(ValueError):
        O.parse_arm("NOPE")
