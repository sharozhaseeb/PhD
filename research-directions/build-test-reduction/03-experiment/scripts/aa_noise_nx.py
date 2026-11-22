"""Benchmark A/A noise floor + repeatability (plan: results/raw/networkx/bench/aa/aa_noise.plan.md; PM 06:27 Q2).

Usage (WSL, idle machine): PYTHONPATH=harness ~/bt-lab/exp/venvs/nx/bin/python scripts/aa_noise_nx.py
S0 in two clones (A, B; no patch), frozen 40-case sample, interleaved, 5 processes x 3 values x 2 repeats, CPUs 2-5.
"""
import json, os, re, statistics as stt, subprocess, sys, tempfile, time
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(exp / "harness")); sys.path.insert(0, str(exp / "scripts"))
from bth import stats  # noqa: E402
import spotcheck_powered_nx as SP  # noqa: E402  (gate, clone, log helpers; module runs nothing at import? see guard)

out = exp / "results/raw/networkx/bench/aa"; out.mkdir(parents=True, exist_ok=True)
SP.LOG = out / "driver.log"
S0 = "181f295117f7f7488644c87f04699290f8e49188"
SAMPLE_FILE = os.environ.get("AA_SAMPLE", "frozen/networkx.aa_noise_sample_cut26.json")
sample = json.loads((exp / SAMPLE_FILE).read_text())["sample"]

def analyse(S, reps):
    """Amendment 1: order arm, spread of 'same' ratios, power from measured noise."""
    import random
    out = {}
    first = runs_order[0] if runs_order else None
    order = {}
    for b, d in S.items():
        r0 = d.get(("A", 0)), d.get(("B", 0))
        r1 = d.get(("A", 1)), d.get(("B", 1))
        if all(r0) and all(r1):
            q0 = stt.median(r0[1]) / stt.median(r0[0])   # B/A, A ran first
            q1 = stt.median(r1[1]) / stt.median(r1[0])   # B/A, B ran first
            order[b] = {"BA_rep0_A_first": q0, "BA_rep1_B_first": q1,
                        "first_over_second": ((1 / q0) * q1) ** 0.5}   # geometric mean of first/second in both reps
    fos = [v["first_over_second"] for v in order.values()]
    out["order"] = {"per_case": order, "median_first_over_second": stt.median(fos) if fos else None,
                    "n_first_slower": sum(1 for x in fos if x > 1), "n": len(fos), "first_case_of_run": first,
                    "first_case_first_over_second": order.get(first, {}).get("first_over_second")}
    def spread(key):
        rs = sorted(c[key]["ratio"] for c in res["cases"].values() if key in c and c[key]["status"] == "same")
        if not rs:
            return None
        q = lambda f: rs[min(len(rs) - 1, int(f * (len(rs) - 1) + 0.5))]
        return {"n": len(rs), "min": rs[0], "p05": q(0.05), "p50": q(0.5), "p95": q(0.95), "max": rs[-1]}
    out["same_ratio_spread"] = {"fixed_order_rep0": spread("rep0"), "abba_pooled": spread("pooled")}
    def counts(key):
        c = {}
        for v in res["cases"].values():
            if key in v:
                c[v[key]["status"]] = c.get(v[key]["status"], 0) + 1
        return c
    out["verdicts"] = {"fixed_order_rep0": counts("rep0"), "rep1_reversed": counts("rep1"), "abba_pooled": counts("pooled")}
    rng = random.Random(20261122)
    power = {}
    for b, d in S.items():
        A_all = sum((d.get(("A", rp), []) for rp in reps), []); B_all = sum((d.get(("B", rp), []) for rp in reps), [])
        if len(A_all) < 5 or len(B_all) < 5 or min(A_all + B_all) <= 0:
            continue
        power[b] = {}
        for sh in (1.12, 1.2, 1.5, 2.0):
            hit = 0
            for _ in range(200):
                x = [rng.choice(A_all) for _ in range(15)]; y = [rng.choice(B_all) * sh for _ in range(15)]
                hit += stats.asv_rule(x, y).status == "slower"
            power[b][str(sh)] = hit / 200
    def med(keys):
        return {sh: (stt.median(power[b][sh] for b in keys) if keys else None) for sh in ("1.12", "1.2", "1.5", "2.0")}
    alg = [b for b in power if b.startswith("benchmark_algorithms.")]; oth = [b for b in power if b not in alg]
    out["power_measured_noise"] = {"per_case": power, "median_all": med(list(power)), "median_algorithms": med(alg),
                                   "median_other": med(oth), "n_cases": len(power),
                                   "note": "bootstrap 15 vs 15 from each case's pooled A and B samples; B scaled by the shift"}
    return out


SP.log(f"A/A start (amendment 1): {len(sample)} cases, 5 processes x 3 values x 2 repeats (rep0 A-first, rep1 B-first)")
SP.clone(SP.A, S0); SP.clone(SP.B, S0)
g = SP.gate()
t0, l0 = time.time(), SP.load1()
filt = "^(" + "|".join(re.escape(b) for b in sample) + ")$"
with tempfile.TemporaryDirectory() as td:
    o = Path(td) / "i.json"
    env = {**os.environ, "PYTHONPATH": str(exp / "harness"), "OMP_NUM_THREADS": "1"}
    subprocess.run([SP.PY, "-m", "bth.benchrun", "interleave", "--state", f"A={SP.A}", "--state", f"B={SP.B}",
                    "--python", SP.PY, "--bench-dir", "benchmarks/benchmarks", "--filter", filt, "--repeats", "2",
                    "--processes", "5", "--values", "3", "--cpus", "2-5", "--out", str(o),
                    "--checkpoint", str(out / "runs.partial.jsonl")], env=env, check=True)
    runs = json.loads(o.read_text())
runs = runs.get("results", runs) if isinstance(runs, dict) else runs
runs_order = []
for r in runs:
    if r["id"] not in runs_order:
        runs_order.append(r["id"])
(out / "raw_runs.json").write_text(json.dumps({"gate_at_start": g, "load_before": l0, "load_after": SP.load1(),
                                               "wall_s": time.time() - t0, "runs": runs}, indent=1))

S = {}
for r in runs:
    if r.get("error") or r.get("skipped"):
        continue
    S.setdefault(r["id"], {}).setdefault((r.get("label") or r.get("state"), r.get("repeat", 0)), []).extend(r["samples"])
reps = sorted({k[1] for d in S.values() for k in d})
res = {"plan": "results/raw/networkx/bench/aa/aa_noise.plan.md", "repeats": reps, "cases": {}}
for b, d in S.items():
    c = {}
    for rp in reps:
        a, bb = d.get(("A", rp), []), d.get(("B", rp), [])
        if a and bb:
            v = stats.asv_rule(a, bb)
            c[f"rep{rp}"] = {"ratio": v.ratio, "p": v.p, "status": v.status, "n": [len(a), len(bb)]}
    A_all = sum((d.get(("A", rp), []) for rp in reps), []); B_all = sum((d.get(("B", rp), []) for rp in reps), [])
    v = stats.asv_rule(A_all, B_all)
    c["pooled"] = {"ratio": v.ratio, "p": v.p, "status": v.status, "n": [len(A_all), len(B_all)]}
    c["cv_A"] = stt.pstdev(A_all) / stt.fmean(A_all) if len(A_all) > 1 else None
    c["cv_B"] = stt.pstdev(B_all) / stt.fmean(B_all) if len(B_all) > 1 else None
    res["cases"][b] = c
peak = max([max(r.get("loadavg_before") or 0, r.get("loadavg_after") or 0) for r in runs] or [0])
res["peak_run_load"] = peak
res["m5_label"] = "noisy" if peak > 1.5 else "measured-window"
res["n_errors"] = sum(1 for r in runs if r.get("error") or r.get("skipped"))
res.update(analyse(S, reps))
(out / "aa_result.json").write_text(json.dumps(res, indent=1))
SP.log(f"A/A done in {time.time() - t0:.0f}s; peak load {peak}; errors {res['n_errors']}")
