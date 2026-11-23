"""E3 tier 2 morning analysis (PM 02:37): new non-'same' verdicts, 1 + 3 sigma floors where sigma exists, and whether
flips concentrate in high-load runs. Compute only. Usage: PYTHONPATH=harness python scripts/tier2_flips.py
Writes results/raw/networkx/slowdowns/repeat/flips_tier2.json (name chosen so the frozen analysis glob t*_*.json does not match it).
"""
import json, statistics as st
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
import sys; sys.path.insert(0, str(exp / "harness"))
from bth import stats  # noqa: E402

R = exp / "results/raw/networkx/slowdowns/repeat"
sig23 = json.loads((exp / "results/raw/networkx/bench/aa/sigma_noise.json").read_text())
load = lambda r: max(r.get("loadavg_before") or 0, r.get("loadavg_after") or 0)
out = {"blocks": {}, "flips": []}
for i in (3, 4, 2):
    rec = json.loads((R / f"t2_{i:02d}.json").read_text())
    runs = rec["raw_runs"]
    S = {}
    for r in runs:
        S.setdefault(r["id"], {}).setdefault((r["label"], r["repeat"]), []).extend(r["samples"])
    n_case = len(rec["cases"]); flips = []
    for b, v in rec["cases"].items():
        d = S[b]
        a = d.get(("base", 0), []) + d.get(("base", 1), []); s = d.get(("slow", 0), []) + d.get(("slow", 1), [])
        ex = stats.asv_rule(a, s, method="exact")
        o = (v["original"] or {}).get("status")
        if ex.status != o:
            cr = [r for r in runs if r["id"] == b]
            sg = sig23.get(b)
            fl = {"slowdown": i, "case": b, "original": o, "now_exact": ex.status, "ratio": ex.ratio, "p_exact": ex.p,
                  "pairs": [v.get("pair0", {}).get("status")],
                  "case_run_loads": [round(load(r), 2) for r in cr], "case_max_load": max(load(r) for r in cr),
                  "case_gate_not_ok": sum(1 for r in cr if r.get("pre_gate") and not r["pre_gate"].get("ok")),
                  "sigma_source": "aa/sigma_noise.json (S0, 2 repeats)" if sg else None,
                  "floor_rep": 1 + 3 * sg["sigma_rep"] if sg else None, "floor_boot": 1 + 3 * sg["sigma_boot"] if sg else None}
            r_ = ex.ratio
            if sg:
                dev = r_ - 1 if r_ >= 1 else 1 / r_ - 1     # symmetric floor test for slower and faster
                fl["clears_floor_rep"] = dev > 3 * sg["sigma_rep"]; fl["clears_floor_boot"] = dev > 3 * sg["sigma_boot"]
            flips.append(fl)
    allmax = [load(r) for r in runs]
    case_hi = {}
    for r in runs:
        case_hi.setdefault(r["id"], 0)
        case_hi[r["id"]] = max(case_hi[r["id"]], load(r))
    flip_ids = {f["case"] for f in flips}
    hi_cases = {b for b, m in case_hi.items() if m > 1.5}
    out["blocks"][i] = {"n_cases": n_case, "m5_label": rec["m5_label"], "n_runs": len(runs), "peak": max(allmax),
                        "runs_gt_1_5": sum(x > 1.5 for x in allmax), "cases_with_a_run_gt_1_5": len(hi_cases),
                        "flips": len(flips), "flips_in_cases_with_run_gt_1_5": len(flip_ids & hi_cases),
                        "median_case_max_load_flips": st.median([case_hi[b] for b in flip_ids]) if flip_ids else None,
                        "median_case_max_load_all": st.median(case_hi.values()),
                        "transitions": {}}
    for f in flips:
        k = f"{f['original']}->{f['now_exact']}"; out["blocks"][i]["transitions"][k] = out["blocks"][i]["transitions"].get(k, 0) + 1
    out["flips"] += flips
(R / "flips_tier2.json").write_text(json.dumps(out, indent=1))
for i, b in out["blocks"].items():
    print(i, b)
for f in out["flips"]:
    print(f["slowdown"], f["case"][-60:], f["original"], "->", f["now_exact"], round(f["ratio"], 3), "%.1e" % f["p_exact"],
          "maxload", f["case_max_load"], "floor_rep", f["floor_rep"] and round(f["floor_rep"], 3), f.get("clears_floor_rep"), f.get("clears_floor_boot"))
