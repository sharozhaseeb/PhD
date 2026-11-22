"""RQ1: first-run vs idle re-run (overnight item 1) of build + serial FULL tests, per networkx state.

Usage: python scripts/idle_compare.py   -> results/rq1_networkx_idle.csv + markdown table on stdout.
Load at start of each idle test run = the `loadavg=` line printed by oracle_nx.sh just before it (results/raw/overnight.log).
Overlap with this session's profile job (19:38:13-19:46:30 PKT, results/raw/concurrency_log.json) is flagged.
"""
import csv, json, re, statistics as st
from datetime import datetime, timezone, timedelta
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
raw = exp / "results/raw/networkx"
rq1 = {r["state"]: r for r in csv.DictReader(open(exp / "results/rq1_networkx.csv", encoding="utf-8"))}
log = (exp / "results/raw/overnight.log").read_text(encoding="utf-8", errors="replace").splitlines()
load_before = {}
last = None
for ln in log:
    m = re.match(r"loadavg=([\d.]+)", ln)
    if m:
        last = float(m.group(1))
    m = re.search(r"oracle-tests: .*/(S\d+_\w+)\.idle\.json", ln)
    if m:
        load_before[m.group(1)] = last
PKT = timezone(timedelta(hours=5))
prof = (datetime(2026, 11, 21, 19, 38, 13, tzinfo=PKT), datetime(2026, 11, 21, 19, 46, 30, tzinfo=PKT))
rows = []
for k in range(19):
    p = next(raw.glob(f"oracle-tests/S{k}_*.idle.json"))
    lab = p.name.replace(".idle.json", "")
    o = json.loads(p.read_text())
    b = json.loads(next(raw.glob(f"build/S{k}_*.idle.json")).read_text())
    t0 = datetime.fromisoformat(o["meta"]["started"]); t1 = datetime.fromisoformat(o["meta"]["ended"])
    overlap = t0 < prof[1] and t1 > prof[0]
    first = rq1[lab]
    lb = load_before.get(lab)
    rows.append({"state": lab, "step": k,
                 "first_wall_s": round(float(first["tests_wall_s"]), 1), "first_label": first["timing_label"],
                 "idle_wall_s": round(o["wall_s"], 1), "idle_build_s": round(b["wall_s"], 3),
                 "first_build_s": float(first["build_s"]),
                 "ratio_first_over_idle": round(float(first["tests_wall_s"]) / o["wall_s"], 3),
                 "idle_load_before": lb, "idle_m5": "noisy" if (lb is not None and lb > 1.5) or overlap else "ok",
                 "idle_overlaps_profile_job": overlap,
                 "idle_n_tests": len(o["tests"]), "idle_exit": o["exit_code"]})
out = exp / "results/rq1_networkx_idle.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("| State | First run wall s (label) | Idle re-run wall s | First / idle | Idle load at start | Idle M5 |")
print("|---|---|---|---|---|---|")
for r in rows:
    print(f"| {r['state']} | {r['first_wall_s']} ({r['first_label']}) | {r['idle_wall_s']} | {r['ratio_first_over_idle']} | "
          f"{r['idle_load_before']} | {r['idle_m5']}{' (profile overlap)' if r['idle_overlaps_profile_job'] else ''} |")
ok = [r for r in rows if r["idle_m5"] == "ok"]
print("\nmedian first", st.median(r["first_wall_s"] for r in rows), "median idle", st.median(r["idle_wall_s"] for r in rows),
      "| idle-ok states", len(ok), "median idle-ok", st.median(r["idle_wall_s"] for r in ok) if ok else None,
      "| ratio range", min(r["ratio_first_over_idle"] for r in rows), max(r["ratio_first_over_idle"] for r in rows),
      "| idle build range", min(r["idle_build_s"] for r in rows), max(r["idle_build_s"] for r in rows),
      "| exits", {r["idle_exit"] for r in rows}, "| n_tests", {r["idle_n_tests"] for r in rows})
