"""Pre-registered analysis for night 2 (2026-11-23 -> 24; plan results/raw/night-2026-11-23/PLAN.md). Frozen before data.

Usage: PYTHONPATH=harness python scripts/night2_analyse.py -> results/raw/night-2026-11-23/analysis.json
DIRAA (directory A/A, the decisive confound test):
  per case: pooled 12 v 12 exact-MWU verdict of B vs A (asv rule), and the per-repeat ratios median(B)/median(A).
  rate = non-'same' / complete cases, Wilson 95 %; compared with tier-2 block t2_03 (6 of 166 under exact).
  RECURRENCE of the 6 t2_03 flips (slow ran in B there): a flip "recurs" if the dir-A/A pooled ratio B/A lies on the same
  side of 1 as the t2_03 ratio slow/base AND |log ratio| >= half of the t2_03 |log ratio|.
  DECISION (fixed now):
    - bias SUPPORTED if >= 4 of 6 recur, or the dir-A/A rate's Wilson lower bound exceeds 0.5 %;
    - bias NOT SUPPORTED if <= 1 of 6 recur and the dir-A/A rate is <= 1 / 166-equivalent (at most 1 non-same);
    - otherwise INCONCLUSIVE.
E5: per pass: total = sum of run wall (STD) or sum of module walls (CACHED); CACHED split import / setup / calib /
  warm-up / loops / other; median STD / median CACHED; per-case sample-shift ratio CACHED/STD of pooled medians, count
  outside [0.8, 1.25] (plan raw/networkx/bench/setup_cached/plan.md).
REP2S: as night-1 E3 (agreement with the original verdict, exact primary), plus per-case directory-consistency:
  ratio in rep0 (slow@B) vs rep1 (slow@A); a "slower" verdict whose two repeat ratios disagree in sign is flagged.
"""
import json, math, statistics as st
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
import sys; sys.path.insert(0, str(exp / "harness"))
from bth import stats  # noqa: E402

RAW = exp / "results/raw"


def wilson(k, n, z=1.96):
    if not n:
        return None
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [(c - h) / d, (c + h) / d]


def group(runs):
    S = {}
    for r in runs:
        if r.get("error") or r.get("skipped") or not r.get("samples"):
            continue
        S.setdefault(r["id"], {}).setdefault((r["label"], r["repeat"]), []).extend(r["samples"])
    return S


def diraa():
    p = RAW / "networkx/bench/dir_aa/s03.json"
    if not p.exists():
        return {"status": "missing"}
    rec = json.loads(p.read_text()); S = group(rec["raw_runs"])
    cases = {}
    for b, d in S.items():
        if not all((l, k) in d for l in ("A", "B") for k in (0, 1)):
            continue
        a = d[("A", 0)] + d[("A", 1)]; bb = d[("B", 0)] + d[("B", 1)]
        v = stats.asv_rule(a, bb, method="exact")
        cases[b] = {"status": v.status, "ratio": v.ratio, "p": v.p,
                    "rep_ratios": [st.median(d[("B", k)]) / st.median(d[("A", k)]) for k in (0, 1)]}
    k = sum(c["status"] != "same" for c in cases.values()); n = len(cases)
    flips = json.loads((RAW / "networkx/slowdowns/repeat/flips_tier2.json").read_text())["flips"]
    rec3 = {}
    for f in [f for f in flips if f["slowdown"] == 3]:
        c = cases.get(f["case"])
        if c is None:
            rec3[f["case"]] = None; continue
        same_side = (c["ratio"] - 1) * (f["ratio"] - 1) > 0
        big = abs(math.log(c["ratio"])) >= 0.5 * abs(math.log(f["ratio"]))
        rec3[f["case"]] = {"t2_ratio": f["ratio"], "diraa_ratio": c["ratio"], "diraa_status": c["status"], "recurs": same_side and big}
    nrec = sum(1 for x in rec3.values() if x and x["recurs"])
    w = wilson(k, n)
    decision = ("bias SUPPORTED" if (nrec >= 4 or (w and w[0] > 0.005)) else
                "bias NOT SUPPORTED" if (nrec <= 1 and k <= 1) else "INCONCLUSIVE")
    return {"m5_label": rec.get("m5_label"), "n_complete": n, "non_same": k, "rate": k / n if n else None, "wilson95": w,
            "non_same_cases": {b: c for b, c in cases.items() if c["status"] != "same"},
            "t2_03_flips_recurrence": rec3, "n_recur": nrec, "decision": decision}


def e5():
    out = {}
    d = RAW / "networkx/bench/setup_cached"
    med = {}
    for k in range(3):
        for arm in ("std", "cached"):
            p = d / f"{arm}{k}.json"
            if not p.exists():
                out[f"{arm}{k}"] = {"status": "missing"}; continue
            rec = json.loads(p.read_text()); runs = rec["raw_runs"]
            o = {"m5_label": rec.get("m5_label"), "n": len(runs)}
            if arm == "std":
                o["total_s"] = sum(r["wall_s"] for r in runs)
            else:
                mods = {}
                for r in runs:
                    mods.setdefault(r["module"], r)
                o["total_s"] = sum(r["module_wall_s"] for r in mods.values())
                o["import_s"] = sum((r.get("module_import_s") or 0) for r in mods.values())
                for key in ("setup_s", "calib_s", "warmup_s", "loop_s"):
                    o[key] = sum(r.get(key) or 0 for r in runs)
                o["other_s"] = o["total_s"] - o["import_s"] - sum(o[x] for x in ("setup_s", "calib_s", "warmup_s", "loop_s"))
            for r in runs:
                if r.get("samples"):
                    med.setdefault(r["id"], {}).setdefault(arm, []).extend(r["samples"])
            out[f"{arm}{k}"] = o
    std = [v["total_s"] for k_, v in out.items() if k_.startswith("std") and "total_s" in v]
    cac = [v["total_s"] for k_, v in out.items() if k_.startswith("cached") and "total_s" in v]
    shift = {b: st.median(v["cached"]) / st.median(v["std"]) for b, v in med.items() if v.get("cached") and v.get("std")}
    out["summary"] = {"std_median_s": st.median(std) if std else None, "cached_median_s": st.median(cac) if cac else None,
                      "std_over_cached": (st.median(std) / st.median(cac)) if std and cac else None,
                      "n_shift_cases": len(shift), "n_sample_shifted": sum(1 for x in shift.values() if not 0.8 <= x <= 1.25),
                      "sample_shifted": {b: x for b, x in shift.items() if not 0.8 <= x <= 1.25}}
    return out


def rep2s():
    out = {}
    for i in (8, 1):
        p = RAW / f"networkx/slowdowns/repeat_swap/t2s_{i:02d}.json"
        if not p.exists():
            out[i] = {"status": "missing"}; continue
        rec = json.loads(p.read_text()); S = group(rec["raw_runs"])
        orig = json.loads((RAW / f"networkx/slowdowns/{i:02d}.json").read_text())["verdicts"]
        cases = {}
        for b, d in S.items():
            if not all((l, k) in d for l in ("base", "slow") for k in (0, 1)):
                continue
            v = stats.asv_rule(d[("base", 0)] + d[("base", 1)], d[("slow", 0)] + d[("slow", 1)], method="exact")
            rr = [st.median(d[("slow", k)]) / st.median(d[("base", k)]) for k in (0, 1)]
            cases[b] = {"status": v.status, "ratio": v.ratio, "p": v.p, "rep_ratios": rr,
                        "original": (orig.get(b) or {}).get("status"),
                        "dir_inconsistent": v.status != "same" and (rr[0] - 1) * (rr[1] - 1) < 0}
        out[i] = {"m5_label": rec.get("m5_label"), "n_complete": len(cases),
                  "agree": sum(c["status"] == c["original"] for c in cases.values()),
                  "non_same": {b: c for b, c in cases.items() if c["status"] != "same"}}
    return out


if __name__ == "__main__":
    res = {"diraa": diraa(), "e5": e5(), "rep2s": rep2s()}
    o = RAW / "night-2026-11-23/analysis.json"; o.parent.mkdir(parents=True, exist_ok=True)
    o.write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps({"diraa": {k: v for k, v in res["diraa"].items() if k not in ("non_same_cases",)},
                      "e5": res["e5"].get("summary"), "rep2s": {i: {k: v for k, v in r.items() if k != "non_same"} for i, r in res["rep2s"].items()}},
                     indent=1, default=str))
