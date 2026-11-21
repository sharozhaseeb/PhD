"""RQ2/RQ3 headline table for networkx: every number quoted in results.md's RQ2 table comes from here.

Usage: python scripts/rq2_table.py   ->  results/rq2_networkx.csv
Columns (all per arm, summed over the 18 replayed steps):
  tests_run, est_test_s           Σ selected tests; Σ their serial S0 durations (M1)
  build_s                         Σ build seconds charged (FULL / full checks: measured S0 pip install -e)
  sim_total_cost_s                = the simulator's total_cost_s = build_s + est_test_s + est_bench_s (bench s are 0 while pending)
  pytest_startup_s                13.6 s (median wall − Σ durations over clean serial runs) per step running ≥ 1 test
  est_end_to_end_s                = build_s + est_test_s + pytest_startup_s   (benchmarks excluded)
  measured_end_to_end_s           FULL: Σ serial wall + build, S1–S18 (rq1_networkx.csv); TESTMON: Σ real testmon wall S1–S18
  measured_label                  timing label of the measured value
  full_checks, bench_cases_selected, n_faults, k_missed, wilson_lo, wilson_hi, mean_delay
"""
import csv, collections, glob, json, os, statistics as st
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
sim = exp / "results/sim/networkx"
rq1 = list(csv.DictReader(open(exp / "results/rq1_networkx.csv")))
first = [r for r in rq1 if "." not in r["state"]]
clean = [r for r in first if r.get("timing_label") == "clean"]
startup = round(st.median(float(r["tests_wall_s"]) - float(r["tests_sum_durations_s"]) for r in clean), 1)
full_meas = sum(float(r["tests_wall_s"]) + float(r["build_s"]) for r in first if r["step"] != "0")
tm = [json.load(open(p)) for p in glob.glob(str(exp / "results/raw/networkx/testmon/S*_*.json"))
      if not os.path.basename(p).startswith("S0_")]
tm_meas = sum(x["wall_s"] for x in tm)

steps = collections.defaultdict(list)
for r in csv.DictReader(open(sim / "rq2_steps.csv")):
    steps[r["arm"]].append(r)
summ = {r["arm"]: r for r in csv.DictReader(open(sim / "rq2_steps.csv.summary.csv"))}
rows = []
for arm, rs in steps.items():
    b = sum(float(r["build_s"]) for r in rs); t = sum(float(r["tests_s"]) for r in rs)
    su = startup * sum(1 for r in rs if int(r["n_tests"]) > 0)
    m, lab = (full_meas, "serial, 17 clean + 1 noisy state (rq1_networkx.csv)") if arm == "FULL" else \
             (tm_meas, "concurrent (CPU-pinned beside S0 bench)") if arm == "TESTMON" else (None, "")
    s = summ.get(arm, {})
    rows.append({"arm": arm, "tests_run": sum(int(r["n_tests"]) for r in rs), "est_test_s": round(t, 1),
                 "build_s": round(b, 2), "sim_total_cost_s": round(float(s.get("total_cost_s", "nan")), 1),
                 "pytest_startup_s": round(su, 1), "est_end_to_end_s": round(b + t + su),
                 "measured_end_to_end_s": None if m is None else round(m), "measured_label": lab,
                 "full_checks": sum(int(r["full_check"]) for r in rs),
                 "bench_cases_selected": sum(int(r["n_benches"]) for r in rs),
                 **{k: s.get(k) for k in ("n_faults", "k_missed", "wilson_lo", "wilson_hi", "mean_delay")}})
out = exp / "results/rq2_networkx.csv"
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(f"startup {startup}s; FULL measured {full_meas:.0f}s; testmon measured {tm_meas:.0f}s -> {out}")
for r in rows:
    print(r["arm"][:34].ljust(34), r["tests_run"], r["est_test_s"], r["est_end_to_end_s"], r["measured_end_to_end_s"], r["k_missed"])
