"""C5 comparators vs A4 at matched cost (pre-registered plan: results/sim/networkx/c5_plan.md).

Usage (WSL; loads the 299 MB depmaps):  PYTHONPATH=harness ~/bt-lab/exp/venvs/nx/bin/python scripts/c5_compare.py
Writes results/sim/networkx/c5_steps.csv{,.faults.csv,.summary.csv}, c5_compare.csv, c5_compare.json.
"""
import csv, json, sys
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(exp / "harness"))
from bth import orchestrate as O, cost  # noqa: E402
from bth.stats import wilson  # noqa: E402

INP = exp / "results/sim/networkx/inputs"
OUT = exp / "results/sim/networkx"
STARTUP = 13.587   # results/sim/networkx/e2e.json startup_median_s
CAP = [f"BATCH:cap={k}" for k in (2, 3, 5, 8)]
BUD = [f"BATCH:budget={T}" for T in (5, 10, 20)]
ARMS = CAP + BUD + ["BATCH:budget=10,cap=5", "OURS", "OURS:T=5", "OURS:T=20"] + \
       [f"PERIODIC:inner=TESTMON,k={k}" for k in (2, 3, 5, 8)] + ["TESTMON", "FULL"]

O.simulate(INP, OUT / "c5_steps.csv", ARMS)
ctx, steps, dur, faults = O.load_sim_inputs(INP)
bw = {r["id"]: r["wall_s"] for r in json.loads((exp / "results/raw/networkx/bench/S0_181f2951.idle.json").read_text())["results"]}

rows_s = list(csv.DictReader(open(OUT / "c5_steps.csv", encoding="utf-8")))
rows_f = list(csv.DictReader(open(OUT / "c5_steps.csv.faults.csv", encoding="utf-8")))

# secondary cost: benchmark seconds with S0 item-4 weights; recompute decisions (cost only)
bench_s = {}
for spec in ARMS:
    _, fac = O.parse_arm(spec)
    arm = fac(ctx); st = arm.new_state(); tot = 0.0
    from bth.select import Outcome
    for t, ch in enumerate(steps, start=1):
        d = arm.decide(t, ch, st)
        tot += sum(bw[b] for b in d.benches)
        arm.observe(t, d, Outcome(green=True), st)
    bench_s[spec] = tot

res = {}
for spec in ARMS:
    rs = [r for r in rows_s if r["arm"] == spec]
    fulls = [int(r["step"]) for r in rs if r["full_check"] == "1"]
    e2e = sum(float(r["build_s"]) + float(r["tests_s"]) + (STARTUP if int(r["n_tests"]) > 0 else 0) for r in rs)
    fs = [r for r in rows_f if r["arm"] == spec and r["by"] != ""]
    det = [r for r in fs if r["detected_step"] != ""]
    # only faults FULL detects count (N = 20), as in the draft fault table
    full_det = {r["fault_id"] for r in rows_f if r["arm"] == "FULL" and r["detected_step"] != ""}
    fs = [r for r in fs if r["fault_id"] in full_det]
    det = [r for r in fs if r["detected_step"] != ""]
    wins = []
    for r in det:
        u = int(r["detected_step"])
        if r["by"] == "selection":
            wins.append(1)
        else:
            prev = max([s for s in fulls if s < u], default=0)
            wins.append(u - prev)
    n, k = len(fs), len(fs) - len(det)
    res[spec] = {"n_full_checks": len(fulls), "full_check_steps": fulls, "e2e_nobench_s": round(e2e, 1),
                 "bench_s_item4_weights": round(bench_s[spec], 1), "e2e_with_bench_s": round(e2e + bench_s[spec], 1),
                 "n": n, "missed": k, "wilson_miss": wilson(k, n),
                 "caught_at_injection": sum(1 for r in det if int(r["delay"]) == 0),
                 "mean_delay": round(sum(int(r["delay"]) for r in det) / len(det), 3) if det else None,
                 "mean_window": round(sum(wins) / len(wins), 3) if wins else None, "max_window": max(wins) if wins else None}


def interp(family, x, key):
    pts = sorted((res[a]["e2e_nobench_s"], res[a][key]) for a in family)
    if x < pts[0][0] or x > pts[-1][0]:
        return None
    for (c0, v0), (c1, v1) in zip(pts, pts[1:]):
        if c0 <= x <= c1:
            return v0 if c1 == c0 else round(v0 + (v1 - v0) * (x - c0) / (c1 - c0), 3)
    return pts[-1][1]


a4 = res["OURS"]
match = {}
for fam, members in (("cap-only", CAP), ("additive-budget", BUD), ("fixed-k + per-edit (PERIODIC TESTMON)",
                                                                     [f"PERIODIC:inner=TESTMON,k={k}" for k in (2, 3, 5, 8)])):
    m = {key: interp(members, a4["e2e_nobench_s"], key) for key in ("mean_delay", "caught_at_injection", "mean_window")}
    eq = [a for a in sorted(members, key=lambda a: res[a]["e2e_nobench_s"])
          if res[a]["caught_at_injection"] >= a4["caught_at_injection"]]
    m["cheapest_reaching_A4_caught_at_injection"] = eq[0] if eq else None
    m["its_cost"] = res[eq[0]]["e2e_nobench_s"] if eq else None
    m["cost_range"] = [min(res[a]["e2e_nobench_s"] for a in members), max(res[a]["e2e_nobench_s"] for a in members)]
    match[fam] = m

json.dump({"plan": "results/sim/networkx/c5_plan.md", "startup_s": STARTUP, "arms": res,
           "matched_at_A4_cost": {"A4_cost_s": a4["e2e_nobench_s"], **match}},
          open(OUT / "c5_compare.json", "w"), indent=1)
with open(OUT / "c5_compare.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["arm", "full_checks", "e2e_nobench_s", "bench_s_item4", "e2e_with_bench_s", "missed_of_N", "caught_at_injection",
                "mean_delay", "mean_window", "max_window"])
    for a in ARMS:
        r = res[a]
        w.writerow([a, r["n_full_checks"], r["e2e_nobench_s"], r["bench_s_item4_weights"], r["e2e_with_bench_s"],
                    f'{r["missed"]}/{r["n"]}', r["caught_at_injection"], r["mean_delay"], r["mean_window"], r["max_window"]])
print(open(OUT / "c5_compare.csv", encoding="utf-8").read())
print(json.dumps(match, indent=1))
