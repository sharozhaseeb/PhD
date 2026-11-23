"""Night queue 2026-11-23 -> 24 (PM ruling 06:32). Plan: results/raw/night-2026-11-23/PLAN.md.

Usage (WSL): PYTHONPATH=harness ~/bt-lab/exp/venvs/nx/bin/python scripts/night2_nx.py <item>
  gate     block gate (as night 1, telemetry Windows CPU)
  diraa    DIRECTORY A/A: identical code (state of slowdown #3, e773a6af) in nx-slow-A and nx-slow-B, the same 168-case
           set and design as tier-2 block #3 (2 x 3, 2 repeats, order rotated), fixed directories as in every earlier A/B run
  cached   E5: STD (asv protocol, interleave one state) and CACHED (measure-cached) alternated x3 at S0, both in nx-slow-A
  rep2s    E3 tier-2 resume with DIRECTORY SWAP: #8 (fresh; the fixed-dir partial is archived) then #1.
           repeat 0: base@A, slow@B, base first; repeat 1: base@B, slow@A, slow first.
Per-run gate, per-run checkpoints, CPUs 2-5, OMP_NUM_THREADS=1, as night 1.
"""
import json, os, re, subprocess, sys, tempfile, time
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(exp / "harness")); sys.path.insert(0, str(exp / "scripts"))
import night_nx as N  # noqa: E402  (helpers; its __main__ block does not run on import)
import spotcheck_powered_nx as SP  # noqa: E402

RAW = exp / "results/raw"
OUT = {"diraa": RAW / "networkx/bench/dir_aa", "cached": RAW / "networkx/bench/setup_cached",
       "rep2s": RAW / "networkx/slowdowns/repeat_swap"}
S0 = N.S0
FROZEN = json.loads((exp / "frozen/night-2026-11-23.cases.json").read_text())


def bench(cmd_op, states, ids, repeats, ck, extra=()):
    filt = "^(" + "|".join(re.escape(b) for b in ids) + ")$" if ids else None
    with tempfile.TemporaryDirectory() as td:
        o = Path(td) / "o.json"
        env = {**os.environ, "PYTHONPATH": str(exp / "harness"), "OMP_NUM_THREADS": "1"}
        cmd = [N.NX, "-m", "bth.benchrun", cmd_op, "--python", N.NX, "--bench-dir", "benchmarks/benchmarks",
               "--repeats", str(repeats), "--processes", "2", "--values", "3", "--cpus", "2-5", "--out", str(o),
               "--checkpoint", str(ck), "--run-gate", "--gate-log", str(SP.LOG), *extra]
        for lab, d in states:
            cmd += ["--state", f"{lab}={d}"]
        if filt:
            cmd += ["--filter", filt]
        if N.win_telemetry():
            cmd += ["--gate-win-telemetry", N.win_telemetry()]
        subprocess.run(cmd, env=env, check=True)
        return json.loads(o.read_text())


def item_diraa():
    out = OUT["diraa"]; out.mkdir(parents=True, exist_ok=True)
    res_p = out / "s03.json"
    if res_p.exists():
        return
    sha = N.slows[3]["state_sha"]
    SP.clone(SP.A, sha); SP.clone(SP.B, sha)
    ids = FROZEN["diraa"]["cases"]
    t0 = time.time(); SP.log(f"block diraa-s03 start: {len(ids)} cases, identical code at {sha[:8]} in A and B, 2 x 3, 2 repeats")
    runs = bench("interleave", [("A", SP.A), ("B", SP.B)], ids, 2, out / "s03.partial.jsonl")
    rec = {"plan": "results/raw/night-2026-11-23/PLAN.md", "state_sha": sha, "dirs": {"A": str(SP.A), "B": str(SP.B)},
           **N.block_meta(runs, t0), "raw_runs": runs}
    res_p.write_text(json.dumps(rec, indent=1))
    SP.log(f"block diraa-s03 done in {rec['wall_s']:.0f}s")


def item_cached():
    out = OUT["cached"]; out.mkdir(parents=True, exist_ok=True)
    SP.clone(SP.A, S0)
    for k in range(3):
        for arm in ("std", "cached"):
            name = f"{arm}{k}"; res_p = out / f"{name}.json"
            if res_p.exists():
                continue
            t0 = time.time(); SP.log(f"block e5-{name} start")
            if arm == "std":
                runs = bench("interleave", [(name, SP.A)], None, 1, out / f"{name}.partial.jsonl")
            else:
                runs = bench("measure-cached", [(name, SP.A)], None, 1, out / f"{name}.partial.jsonl",
                             extra=("--values", "6"))
            rec = {"plan": "results/raw/networkx/bench/setup_cached/plan.md", "state_sha": S0, "arm": arm, "index": k,
                   **N.block_meta(runs, t0), "sum_run_wall_s": sum(r.get("wall_s") or 0 for r in runs), "raw_runs": runs}
            res_p.write_text(json.dumps(rec, indent=1))
            SP.log(f"block e5-{name} done in {rec['wall_s']:.0f}s (sum of runs {rec['sum_run_wall_s']:.0f}s)")


def item_rep2s():
    out = OUT["rep2s"]; out.mkdir(parents=True, exist_ok=True)
    for i in (8, 1):
        res_p = out / f"t2s_{i:02d}.json"
        if res_p.exists():
            continue
        ids = FROZEN["rep2s"][f"{i:02d}"]
        sd = N.slows[i]
        t0 = time.time(); SP.log(f"block rep2s-{i:02d} start: {len(ids)} cases at {sd['state_sha'][:8]}, dir swap")
        allruns = []
        for rep, (base_dir, slow_dir, first) in enumerate(((SP.A, SP.B, "base"), (SP.B, SP.A, "slow"))):
            ck = out / f"t2s_{i:02d}_rep{rep}.partial.jsonl"
            SP.clone(base_dir, sd["state_sha"]); SP.clone(slow_dir, sd["state_sha"], sd["patch"])
            states = [("base", base_dir), ("slow", slow_dir)] if first == "base" else [("slow", slow_dir), ("base", base_dir)]
            runs = bench("interleave", states, ids, 1, ck)
            for r in runs:
                r["repeat"] = rep; r["dir"] = r.get("state_dir")
            allruns += runs
        rec = {"plan": "results/raw/night-2026-11-23/PLAN.md", "slowdown": i, "state_sha": sd["state_sha"],
               "design": "dir swap: rep0 base@A slow@B base-first; rep1 base@B slow@A slow-first",
               **N.block_meta(allruns, t0), "raw_runs": allruns}
        res_p.write_text(json.dumps(rec, indent=1))
        SP.log(f"block rep2s-{i:02d} done in {rec['wall_s']:.0f}s")


if __name__ == "__main__":
    item = sys.argv[1]
    def _wincpu_tel():   # as night 1 amendment 1: mean of telemetry samples in the last 30 s, else 100
        f = N.win_telemetry(); now = time.time(); xs = []
        if f:
            for ln in open(f, encoding="utf-8").readlines()[-12:]:
                try:
                    r = json.loads(ln)
                except ValueError:
                    continue
                if "cpu" in r and now - r["epoch"] <= 30:
                    xs.append(r["cpu"])
        return sum(xs) / len(xs) if xs else 100.0
    SP.wincpu = _wincpu_tel
    from bth.benchrun import top_process
    _log = SP.log
    SP.log = lambda m: _log(m + (f" top_win={top_process(N.win_telemetry())}" if m.startswith("gate:") and N.win_telemetry() else ""))
    if item == "gate":
        SP.LOG = RAW / "night-2026-11-23/queue.log"; SP.gate(); sys.exit(0)
    OUT[item].mkdir(parents=True, exist_ok=True)
    SP.LOG = OUT[item] / f"driver-{item}.log"
    {"diraa": item_diraa, "cached": item_cached, "rep2s": item_rep2s}[item]()
    SP.log(f"{item} finished")
