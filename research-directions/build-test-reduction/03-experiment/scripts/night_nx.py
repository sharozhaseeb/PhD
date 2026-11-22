"""Night queue 2026-11-22 (PM 15:20, paper phase). Plans: results/raw/night-2026-11-22/PLAN.md and each item's plan.md.

Usage (WSL): PYTHONPATH=harness ~/bt-lab/exp/venvs/nx/bin/python scripts/night_nx.py <item>
  gate      block-level idle gate (WSL load <= 1.0 and Windows CPU <= 20 % for 3 x 60 s); returns when open
  aa        (b)  A/A at each flagged verdict's own state, verdict protocol, 5 repeats, alternating order
  rep1      (E3 tier 1) slowdown oracle repeat on flagged + S0-profile-reached cases, 4 repeats (AB BA AB BA)
  drift     (d)  3 FULL passes at S0 (2 x 3) with a 3-case canary before, between and after
  bn        (c)  2 FULL asv passes of bottleneck at f51ed86 (2 x 3)
  rep2      (E3 tier 2) slowdown oracle repeat on all remaining time cases, 2 repeats (AB BA)
Every benchrun call: per-run checkpoint (resume = rerun the same command), per-run postponing gate (bth.benchrun
make_gate: WSL load1 <= 1.5 and Windows CPU <= 20 % from the telemetry file; waits up to 10 min, then runs and
records ok=False), CPUs 2-5, OMP_NUM_THREADS=1. Results are written per block as soon as the block ends.
"""
import glob, json, os, re, subprocess, sys, tempfile, time
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(exp / "harness")); sys.path.insert(0, str(exp / "scripts"))
from bth import stats  # noqa: E402
import spotcheck_powered_nx as SP  # noqa: E402

HOME = Path.home()
NX = SP.PY
BN_PY = str(HOME / "bt-lab/exp/venvs/bn38/bin/python")
BN_STATE = HOME / "bt-lab/exp/work/bn-bench"
S0 = "181f295117f7f7488644c87f04699290f8e49188"
RAW = exp / "results/raw"
slows = SP.slows
prof = json.loads((RAW / "networkx/profile/S0_181f2951.json").read_text())["profiles"]
CANARY = ["benchmark_classes.GraphBenchmark.time_to_undirected('DiGraph')",
          "benchmark_classes.GraphBenchmark.time_add_edges_from('MultiDiGraph')",
          "benchmark_algorithms.UndirectedAlgorithmBenchmarks.time_connected_components('Erdos Renyi (100, 0.9)')"]
OUT = {"aa": RAW / "networkx/bench/aa_flagged", "rep1": RAW / "networkx/slowdowns/repeat",
       "rep2": RAW / "networkx/slowdowns/repeat", "drift": RAW / "networkx/bench/drift", "bn": RAW / "bottleneck/bench"}


def win_telemetry():
    fs = sorted(glob.glob(str(RAW / "telemetry/win-*.jsonl")), key=os.path.getmtime)
    return fs[-1] if fs else None


def orig(i):
    return json.loads((RAW / f"networkx/slowdowns/{i:02d}.json").read_text())


def flagged(i):
    return [b for b, v in orig(i)["verdicts"].items() if v["status"] == "slower"]


def reached(i):
    fid = orig(i)["function"]
    return [b for b in prof if fid in set(prof[b])]


def interleave(states, ids, repeats, processes, ck, py=NX, worker_py=None, bench_dir="benchmarks/benchmarks"):
    filt = "^(" + "|".join(re.escape(b) for b in ids) + ")$" if ids is not None else None
    with tempfile.TemporaryDirectory() as td:
        o = Path(td) / "i.json"
        env = {**os.environ, "PYTHONPATH": str(exp / "harness"), "OMP_NUM_THREADS": "1"}
        cmd = [py, "-m", "bth.benchrun", "interleave", "--python", worker_py or py, "--bench-dir", bench_dir,
               "--repeats", str(repeats), "--processes", str(processes), "--values", "3", "--cpus", "2-5",
               "--out", str(o), "--checkpoint", str(ck), "--run-gate", "--gate-log", str(SP.LOG)]
        for lab, d in states:
            cmd += ["--state", f"{lab}={d}"]
        if filt:
            cmd += ["--filter", filt]
        if win_telemetry():
            cmd += ["--gate-win-telemetry", win_telemetry()]
        subprocess.run(cmd, env=env, check=True)
        return json.loads(o.read_text())


def verdict(a, b):
    v = stats.asv_rule(a, b)
    return {"ratio": v.ratio, "p": v.p, "status": v.status, "n": [len(a), len(b)]}


def samples(runs):
    S = {}
    for r in runs:
        if r.get("error") or r.get("skipped"):
            continue
        S.setdefault(r["id"], {}).setdefault((r["label"], r["repeat"]), []).extend(r.get("samples") or [])
    return S


def block_meta(runs, t0):
    pk = max([max(r.get("loadavg_before") or 0, r.get("loadavg_after") or 0) for r in runs] or [0])
    pg = [r.get("pre_gate") or {} for r in runs]
    return {"wall_s": time.time() - t0, "n_runs": len(runs), "n_errors": sum(1 for r in runs if r.get("error") or r.get("skipped")),
            "peak_run_load": pk, "n_pre_gate_not_ok": sum(1 for g in pg if g and not g.get("ok")),
            "pre_gate_waited_s": sum(g.get("waited_s") or 0 for g in pg),
            "m5_label": "noisy" if pk > 1.5 or any(g and not g.get("ok") for g in pg) else "measured-window",
            "t_first": min((r.get("t_start") for r in runs if r.get("t_start")), default=None),
            "t_last": max((r.get("t_end") for r in runs if r.get("t_end")), default=None)}


def two_state(i, patch):
    sd = slows[i]
    SP.clone(SP.A, sd["state_sha"]); SP.clone(SP.B, sd["state_sha"], sd["patch"] if patch else None)
    return sd["state_sha"]


def item_aa():
    out = OUT["aa"]; out.mkdir(parents=True, exist_ok=True)
    blocks = [(2, flagged(2), 2), (8, flagged(8), 2), (1, flagged(1), 2),
              (9, ["benchmark_algorithms.UndirectedAlgorithmBenchmarks.time_louvain_communities('Erdos Renyi (100, 0.9)')"], 5)]
    for i, ids, procs in blocks:
        res_p = out / f"s{i:02d}.json"
        if res_p.exists():
            continue
        sha = two_state(i, patch=False)
        t0 = time.time(); SP.log(f"block aa-s{i:02d} start: {len(ids)} cases at state {sha[:8]}, {procs} x 3, 5 repeats")
        runs = interleave([("A", SP.A), ("B", SP.B)], ids, 5, procs, out / f"s{i:02d}.partial.jsonl")
        S = samples(runs); cases = {}
        for b, d in S.items():
            per = {f"rep{r}": verdict(d.get(("A", r), []), d.get(("B", r), [])) for r in range(5) if d.get(("A", r)) and d.get(("B", r))}
            A_all = sum((d.get(("A", r), []) for r in range(5)), []); B_all = sum((d.get(("B", r), []) for r in range(5)), [])
            cases[b] = {**per, "pooled": verdict(A_all, B_all)}
        rec = {"plan": "results/raw/networkx/bench/aa_flagged/plan.md", "slowdown": i, "state_sha": sha,
               "protocol": {"processes": procs, "values": 3, "repeats": 5, "order": "rotated per repeat: AB BA AB BA AB"},
               **block_meta(runs, t0), "cases": cases, "raw_runs": runs}
        res_p.write_text(json.dumps(rec, indent=1))
        SP.log(f"block aa-s{i:02d} done in {rec['wall_s']:.0f}s; label {rec['m5_label']}")


def item_rep(tier):
    out = OUT["rep1"]; out.mkdir(parents=True, exist_ok=True)
    order = [2, 8, 3, 1] if tier == 1 else [3, 4, 2, 8, 1]
    all_ids = [r["id"] for r in orig(2)["raw_runs"]]
    all_ids = list(dict.fromkeys(all_ids))
    for i in order:
        t1 = list(dict.fromkeys(flagged(i) + reached(i)))
        ids = t1 if tier == 1 else [b for b in all_ids if b not in set(t1)]
        reps = 4 if tier == 1 else 2
        res_p = out / f"t{tier}_{i:02d}.json"
        if res_p.exists() or not ids:
            continue
        sha = two_state(i, patch=True)
        t0 = time.time(); SP.log(f"block rep{tier}-{i:02d} start: {len(ids)} cases at state {sha[:8]}, 2 x 3, {reps} repeats")
        runs = interleave([("base", SP.A), ("slow", SP.B)], ids, reps, 2, out / f"t{tier}_{i:02d}.partial.jsonl")
        S = samples(runs); cases = {}
        ov = orig(i)["verdicts"]
        for b, d in S.items():
            c = {f"rep{r}": verdict(d.get(("base", r), []), d.get(("slow", r), [])) for r in range(reps)
                 if d.get(("base", r)) and d.get(("slow", r))}
            for k in range(0, reps, 2):
                a = d.get(("base", k), []) + d.get(("base", k + 1), []); s = d.get(("slow", k), []) + d.get(("slow", k + 1), [])
                if a and s:
                    c[f"pair{k // 2}"] = verdict(a, s)
            a = sum((d.get(("base", r), []) for r in range(reps)), []); s = sum((d.get(("slow", r), []) for r in range(reps)), [])
            c["pooled"] = verdict(a, s); c["original"] = ov.get(b)
            c["agree"] = (ov.get(b) or {}).get("status") == c["pooled"]["status"]
            cases[b] = c
        rec = {"plan": "results/raw/networkx/slowdowns/repeat/plan.md", "slowdown": i, "tier": tier, "state_sha": sha,
               "function": orig(i)["function"], "protocol": {"processes": 2, "values": 3, "repeats": reps,
                                                            "order": "rotated per repeat: base-first, slow-first, ..."},
               **block_meta(runs, t0), "cases": cases, "raw_runs": runs}
        res_p.write_text(json.dumps(rec, indent=1))
        SP.log(f"block rep{tier}-{i:02d} done in {rec['wall_s']:.0f}s; agree {sum(c['agree'] for c in cases.values())}/{len(cases)}")


def item_drift():
    out = OUT["drift"]; out.mkdir(parents=True, exist_ok=True)
    SP.clone(SP.A, S0)
    for k in range(4):
        for kind in ("canary", "pass"):
            if kind == "pass" and k == 3:
                break
            name = f"{kind}{k}"; res_p = out / f"{name}.json"
            if res_p.exists():
                continue
            ids = CANARY if kind == "canary" else None
            t0 = time.time(); SP.log(f"block drift-{name} start")
            runs = interleave([(name, SP.A)], ids, 1, 2, out / f"{name}.partial.jsonl")
            rec = {"plan": "results/raw/networkx/bench/drift/plan.md", "state_sha": S0, "kind": kind, "index": k,
                   "protocol": {"processes": 2, "values": 3}, **block_meta(runs, t0),
                   "sum_run_wall_s": sum(r["wall_s"] for r in runs), "raw_runs": runs}
            res_p.write_text(json.dumps(rec, indent=1))
            SP.log(f"block drift-{name} done in {rec['wall_s']:.0f}s (sum of runs {rec['sum_run_wall_s']:.0f}s)")


def item_bn():
    out = OUT["bn"]; out.mkdir(parents=True, exist_ok=True)
    for k in range(2):
        name = f"pass{k}"; res_p = out / f"{name}.json"
        if res_p.exists():
            continue
        t0 = time.time(); SP.log(f"block bn-{name} start")
        runs = interleave([(name, BN_STATE)], None, 1, 2, out / f"{name}.partial.jsonl", worker_py=BN_PY,
                          bench_dir="asv_bench/benchmarks")
        rec = {"plan": "results/raw/bottleneck/bench/plan.md", "state_sha": "f51ed862e619dcff7b7b3691e58d5fc6ead4076b",
               "protocol": {"processes": 2, "values": 3}, **block_meta(runs, t0),
               "sum_run_wall_s": sum(r["wall_s"] for r in runs), "raw_runs": runs}
        res_p.write_text(json.dumps(rec, indent=1))
        SP.log(f"block bn-{name} done in {rec['wall_s']:.0f}s (sum of runs {rec['sum_run_wall_s']:.0f}s)")


if __name__ == "__main__":
    item = sys.argv[1]
    # Amendment 1 (15:35, before any measurement): SP.wincpu's powershell call timed out (60 s) and returned 100,
    # so the block gate could never open. Windows CPU now comes from the telemetry file: mean of the samples in the
    # last 30 s (3 x 10 s), 100 if none is fresher than 60 s. Thresholds unchanged.
    def _wincpu_tel():
        f = win_telemetry(); now = time.time(); xs = []
        if f:
            for ln in open(f, encoding="utf-8").readlines()[-12:]:
                try:
                    r = json.loads(ln)
                except ValueError:
                    continue
                if "cpu" in r and now - r["epoch"] <= 30:
                    xs.append(r["cpu"])
        if not xs and f:
            last = [json.loads(ln) for ln in open(f, encoding="utf-8").readlines()[-3:] if ln.startswith("{")]
            xs = [r["cpu"] for r in last if "cpu" in r and now - r["epoch"] <= 60]
        return sum(xs) / len(xs) if xs else 100.0
    SP.wincpu = _wincpu_tel
    if item == "gate":
        SP.LOG = RAW / "night-2026-11-22/queue.log"
        SP.gate(); sys.exit(0)
    SP.LOG = OUT[item] / f"driver-{item}.log"
    OUT[item].mkdir(parents=True, exist_ok=True)
    {"aa": item_aa, "rep1": lambda: item_rep(1), "rep2": lambda: item_rep(2), "drift": item_drift, "bn": item_bn}[item]()
    SP.log(f"{item} finished")
