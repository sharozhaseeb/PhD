"""Pre-registered analysis for night 2026-11-22 (written and frozen before any data; plan results/raw/night-2026-11-22/PLAN.md).

Usage: python scripts/night_analyse.py  -> results/raw/night-2026-11-22/analysis.json (+ printed summary)
(b)  sigma_rep(b) = sample SD (n-1) of the 5 per-repeat A/A ratios median(B)/median(A) at the verdict's own state and
     protocol. Floor(b) = 1 + 3 sigma_rep(b). An original "slower" verdict SURVIVES iff its original ratio > floor.
     Sensitivity: sigma_boot = bootstrap SD of the median ratio, 15 v 15 (5 x 3 protocol) or 6 v 6 (2 x 3) resamples of the
     pooled A and B samples, 300 draws, seed 20261122 (as aa/sigma_noise.json). A/A false verdicts (pooled) are counted.
(E3) per case: pooled verdict (all repeats) vs the original verdict; "agree" = same status. Also each order-balanced pair
     (rep 2k + rep 2k+1). Reported per slowdown and tier; floors from (b) applied where they exist.
(d)  per pass: sum of run wall times, split benchmark_algorithms / other; canary wall per case; telemetry covariates over
     each block (Windows CPU mean / max, % Processor Performance mean / min, WSL load1 mean / max). Descriptive only.
(c)  per pass: sum of run wall times and per module; compared with build 4.7-5.4 s and tests ~24 s (results.md RQ1).
Amendment 2 (2026-11-22 15:50, PM 15:46; before any analysis ran): p-values from the exact two-sided MWU are PRIMARY
(stats.mwu_p method="exact"); the earlier scipy "auto" test (normal approximation above n = 8) is reported next to it.
A block counts only if complete (all its planned runs present). Partial blocks are reported as partial, never pooled.
"""
import glob, json, random, statistics as st
from datetime import datetime
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
RAW = exp / "results/raw"
import sys; sys.path.insert(0, str(exp / "harness"))
from bth import stats  # noqa: E402


def load(p):
    p = Path(p)
    return json.loads(p.read_text()) if p.exists() else None


def orig(i):
    return load(RAW / f"networkx/slowdowns/{i:02d}.json")


def ratio(a, b):
    return st.median(b) / st.median(a)


def analyse_aa():
    out = {}
    s9 = load(RAW / "networkx/slowdowns/spotcheck_powered/09.json")
    for i in (2, 8, 1, 9):
        rec = load(RAW / f"networkx/bench/aa_flagged/s{i:02d}.json")
        if rec is None:
            out[i] = {"status": "missing"}; continue
        n_s = 6 if rec["protocol"]["processes"] == 2 else 15
        rng = random.Random(20261122)
        S = {}
        for r in rec["raw_runs"]:
            if not (r.get("error") or r.get("skipped")):
                S.setdefault(r["id"], {}).setdefault((r["label"], r["repeat"]), []).extend(r["samples"])
        cases = {}
        ov = (s9["verdicts"] if i == 9 else orig(i)["verdicts"])
        for b, d in S.items():
            rs = [ratio(d[("A", k)], d[("B", k)]) for k in range(5) if d.get(("A", k)) and d.get(("B", k))]
            A = sum((d.get(("A", k), []) for k in range(5)), []); B = sum((d.get(("B", k), []) for k in range(5)), [])
            boot = [ratio([rng.choice(A) for _ in range(n_s)], [rng.choice(B) for _ in range(n_s)]) for _ in range(300)]
            sr = st.stdev(rs) if len(rs) >= 2 else None; sb = st.stdev(boot)
            o = ov.get(b) or {}
            fr = 1 + 3 * sr if sr is not None else None; fb = 1 + 3 * sb
            cases[b] = {"n_repeats": len(rs), "complete": len(rs) == 5, "ratios": rs, "sigma_rep": sr, "sigma_boot": sb,
                        "floor_rep": fr, "floor_boot": fb,
                        "aa_pooled": {m: stats.asv_rule(A, B, method=m).status for m in METHODS},
                        "original": o, "survives_rep": (o.get("status") == "slower" and fr is not None and o["ratio"] > fr) if len(rs) == 5 else None,
                        "survives_boot": o.get("status") == "slower" and o["ratio"] > fb}
        out[i] = {"m5_label": rec.get("m5_label"), "cases": cases}
    return out


PRIMARY = "exact"          # amendment 2 (PM 15:46): exact MWU primary; scipy_auto (the earlier test) shown too
METHODS = ("exact", "scipy_auto")


def rescore(rec, la, lb, reps):
    """Re-test a block's pooled and per-pair verdicts from its raw runs under every method."""
    S = {}
    for r in rec["raw_runs"]:
        if not (r.get("error") or r.get("skipped")):
            S.setdefault(r["id"], {}).setdefault((r["label"], r["repeat"]), []).extend(r["samples"])
    out = {}
    for b, d in S.items():
        a = sum((d.get((la, k), []) for k in range(reps)), []); s = sum((d.get((lb, k), []) for k in range(reps)), [])
        out[b] = {m: stats.asv_rule(a, s, method=m).status for m in METHODS} if a and s else None
        for k in range(0, reps - 1, 2):
            a2 = d.get((la, k), []) + d.get((la, k + 1), []); s2 = d.get((lb, k), []) + d.get((lb, k + 1), [])
            if a2 and s2 and out[b] is not None:
                out[b].update({f"pair{k // 2}_{m}": stats.asv_rule(a2, s2, method=m).status for m in METHODS})
    return out


def analyse_rep():
    out = {}
    for p in sorted(glob.glob(str(RAW / "networkx/slowdowns/repeat/t*_*.json"))):
        rec = load(p)
        c = rec["cases"]; reps = rec["protocol"]["repeats"]
        rs = rescore(rec, "base", "slow", reps)
        for b, v in c.items():   # original verdicts did not change under exact (raw/stats_exact/recompute.json)
            v["pooled_by_method"] = rs.get(b)
            v["agree_exact"] = (v["original"] or {}).get("status") == (rs.get(b) or {}).get("exact")
        complete = {b: v for b, v in c.items() if all(f"rep{k}" in v for k in range(reps))}
        tab = {}
        for v in complete.values():
            key = f"{(v['original'] or {}).get('status', 'n/a')}->{v['pooled']['status']}"
            tab[key] = tab.get(key, 0) + 1
        out[Path(p).stem] = {"slowdown": rec["slowdown"], "tier": rec["tier"], "m5_label": rec["m5_label"],
                             "n_cases": len(c), "n_complete": len(complete), "transitions": tab,
                             "agree": sum(v["agree"] for v in complete.values()),
                             "agree_exact_PRIMARY": sum(v["agree_exact"] for v in complete.values()),
                             "transitions_exact": {t: sum(1 for v in complete.values() if f"{(v['original'] or {}).get('status', 'n/a')}->{(v['pooled_by_method'] or {}).get('exact')}" == t)
                                                   for t in {f"{(v['original'] or {}).get('status', 'n/a')}->{(v['pooled_by_method'] or {}).get('exact')}" for v in complete.values()}},
                             "pairs_agree_with_each_other": sum(1 for v in complete.values()
                                                                if v.get("pair0", {}).get("status") == v.get("pair1", {}).get("status")),
                             "slower_now": {b: v["pooled"] for b, v in complete.items() if v["pooled"]["status"] == "slower"}}
    return out


def telemetry(t0, t1):
    def rows(pat):
        r = []
        for f in glob.glob(str(RAW / f"telemetry/{pat}")):
            for ln in open(f, encoding="utf-8"):
                if ln.startswith("{"):
                    try:
                        r.append(json.loads(ln))
                    except ValueError:
                        pass
        return r
    if not (t0 and t1):
        return None
    a = datetime.strptime(t0, "%Y-%m-%dT%H:%M:%S%z").timestamp(); b = datetime.strptime(t1, "%Y-%m-%dT%H:%M:%S%z").timestamp()
    w = [x for x in rows("win-*.jsonl") if "cpu" in x and a <= x["epoch"] <= b]
    l = [x for x in rows("wsl-*.jsonl") if a <= x["epoch"] <= b]
    f = lambda xs, k, g: round(g(x[k] for x in xs), 1) if xs else None
    return {"n_win": len(w), "win_cpu_mean": f(w, "cpu", st.fmean), "win_cpu_max": f(w, "cpu", max),
            "perf_mean": f(w, "perf", st.fmean), "perf_min": f(w, "perf", min),
            "load1_mean": f(l, "load1", st.fmean), "load1_max": f(l, "load1", max)}


def analyse_passes(sub, names):
    out = {}
    for n in names:
        rec = load(RAW / sub / f"{n}.json")
        if rec is None:
            out[n] = {"status": "missing"}; continue
        runs = rec["raw_runs"]; mods = {}
        for r in runs:
            m = r["id"].split(".")[0]; mods[m] = mods.get(m, 0) + r["wall_s"]
        out[n] = {"n_runs": len(runs), "sum_run_wall_s": rec["sum_run_wall_s"], "wall_s": rec["wall_s"],
                  "per_module_s": {k: round(v, 1) for k, v in sorted(mods.items())}, "m5_label": rec["m5_label"],
                  "per_case_s": {r["id"]: round(r["wall_s"], 2) for r in runs} if len(runs) <= 5 else None,
                  "telemetry": telemetry(rec.get("t_first"), rec.get("t_last"))}
    return out


if __name__ == "__main__":
    res = {"aa": analyse_aa(), "repeat": analyse_rep(),
           "drift": analyse_passes("networkx/bench/drift", ["canary0", "pass0", "canary1", "pass1", "canary2", "pass2", "canary3"]),
           "bn": analyse_passes("bottleneck/bench", ["pass0", "pass1"])}
    o = RAW / "night-2026-11-22/analysis.json"; o.parent.mkdir(parents=True, exist_ok=True)
    o.write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps({k: (v if k != "aa" else {i: {b[:60]: {kk: x.get(kk) for kk in ("floor_rep", "survives_rep", "survives_boot")}
                                                    for b, x in (d.get("cases") or {}).items()} for i, d in v.items()})
                      for k, v in res.items()}, indent=1, default=str)[:6000])
