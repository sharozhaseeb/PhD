"""RQ1 aggregation: FULL per-state cost split (build / tests / benchmarks) from raw oracle outputs.

Usage: python scripts/aggregate_rq1.py <repo-raw-dir-name> [--out results/rq1_<name>.csv]
Reads results/raw/<name>/{build,oracle-tests,bench}/S<i>_<sha8>.json. Missing parts are left blank (partial OK).
Every row carries the state SHA and the harness tree hash of the run that produced the test numbers.
"""
import csv, json, re, sys
from datetime import datetime
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
name = sys.argv[1]
out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else exp / f"results/rq1_{name}.csv"
raw = exp / "results/raw" / name


def load(sub):
    d = {}
    for p in sorted((raw / sub).glob("S*_*.json")):
        if p.name.endswith(".outcomes.json"):
            continue
        d[p.stem] = json.loads(p.read_text())
    return d


build, tests, bench = load("build"), load("oracle-tests"), load("bench")
_cl = exp / "results/raw/concurrency_log.json"
INTERVALS = [(datetime.fromisoformat(i["start"]), datetime.fromisoformat(i["end"]), i["level"])
             for i in json.loads(_cl.read_text())["intervals"]] if _cl.exists() else []


def concurrency(meta):
    """'heavy'/'light' if the run overlapped a logged concurrent-activity interval, else 'none-logged'."""
    a, b = datetime.fromisoformat(meta["started"]), datetime.fromisoformat(meta["ended"])
    lv = [lvl for s, e, lvl in INTERVALS if a < e and s < b]
    return "heavy" if "heavy" in lv else ("light" if lv else "none-logged")
labels = sorted(set(build) | set(tests) | set(bench), key=lambda s: int(re.match(r"S(\d+)_", s).group(1)))

# timing_label (deterministic): a run is "noisy" if its tests slowed down UNIFORMLY, i.e. the median over
# tests (reference duration > 50 ms) of duration / cross-state median duration exceeds 1.10. An edit to one
# module cannot slow thousands of unrelated tests, so a uniform shift indicates external load.
import statistics as _st
_ref = {}
if tests:
    _all = {}
    for t in tests.values():
        for k, v in t["tests"].items():
            _all.setdefault(k, []).append(v["duration"])
    _ref = {k: _st.median(v) for k, v in _all.items() if _st.median(v) > 0.05}


# Criterion 2: tests that reach NO function changed by ANY edit (S0 depmap) run identical code in every
# state; if their summed duration exceeds 1.15x its cross-state median, the run was disturbed.
_untouched = set()
_dm, _ch = raw / "depmap", raw / "changes/changes.json"
if _ch.exists() and list(_dm.glob("S0_*.json")):
    _changed = {f for st in json.loads(_ch.read_text())["steps"] for f in st["functions"]}
    _changed_mods = {f.split("::")[0] for f in _changed if f.endswith("::<module>")}
    _d0 = json.loads((_dm / "S0_181f2951.json").read_text())["deps"]   # exact first-run file
    _untouched = {k for k, fs in _d0.items()
                  if not (set(fs) & _changed) and not any(f.split("::")[0] in _changed_mods for f in fs)}
_usum = {lab: sum(t["tests"][k]["duration"] for k in _untouched if k in t["tests"]) for lab, t in tests.items()}
_umed = _st.median(_usum.values()) if _usum else 0


def timing_label(t):
    r = [t["tests"][k]["duration"] / m for k, m in _ref.items() if k in t["tests"]]
    med = _st.median(r) if r else 1.0
    u = (sum(t["tests"][k]["duration"] for k in _untouched if k in t["tests"]) / _umed) if _umed else 1.0
    return ("noisy" if (med > 1.10 or u > 1.15) else "clean"), round(med, 3), round(u, 3)
rows = []
for lab in labels:
    b, t, bb = build.get(lab), tests.get(lab), bench.get(lab)
    r = {"state": lab, "step": int(lab[1:].split("_")[0]), "state_sha": None, "harness_tree_hash": None,
         "build_s": None, "tests_wall_s": None, "tests_sum_durations_s": None, "n_tests": None,
         "n_failed": None, "tests_exit": None, "tests_started": None, "tests_concurrent_load": None, "timing_label": None, "uniform_shift_median_ratio": None, "untouched_tests_sum_ratio": None, "bench_wall_s": None, "n_bench_cases": None, "n_bench_ok": None}
    if b:
        r["build_s"], r["state_sha"] = b["wall_s"], b["state_sha"]
    if t:
        tt = t["tests"]
        r.update(state_sha=t["meta"]["state_sha"], harness_tree_hash=t["meta"]["harness_tree_hash"],
                 tests_wall_s=round(t["wall_s"], 3), n_tests=len(tt), tests_exit=t["exit_code"],
                 tests_sum_durations_s=round(sum(v["duration"] for v in tt.values()), 3),
                 n_failed=sum(v["outcome"] == "failed" for v in tt.values()),
                 tests_started=t["meta"]["started"], tests_concurrent_load=concurrency(t["meta"]))
        r["timing_label"], r["uniform_shift_median_ratio"], r["untouched_tests_sum_ratio"] = timing_label(t)
    if bb:
        cases = bb.get("results") or bb.get("cases") or []
        r["bench_wall_s"] = round(sum(c.get("wall_s") or 0 for c in cases), 3)
        r["n_bench_cases"] = len(cases)
        r["n_bench_ok"] = sum(1 for c in cases if not c.get("skipped") and not c.get("error"))
    parts = [r["build_s"], r["tests_wall_s"], r["bench_wall_s"]]
    r["full_total_s"] = round(sum(p for p in parts if p is not None), 3) if all(p is not None for p in parts) else None
    rows.append(r)

out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["state"])
    w.writeheader(); w.writerows(rows)
print(f"{len(rows)} states -> {out}")
for r in rows:
    print(r["state"], r["build_s"], r["tests_wall_s"], r["bench_wall_s"], r["n_tests"], r["n_failed"])
