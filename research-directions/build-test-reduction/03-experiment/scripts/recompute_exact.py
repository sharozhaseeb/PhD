"""Recompute every existing performance verdict with an exact Mann-Whitney test (PM 15:46, after W1's asv source check).

Usage (WSL, low priority): PYTHONPATH=harness nice -n 19 taskset -c 0,1 ~/bt-lab/exp/venvs/nx/bin/python scripts/recompute_exact.py
For each verdict family, the same pooled samples are re-tested with bth.stats.mwu_p methods:
  scipy_auto (what was reported), exact (scipy exact at every size; PRIMARY from now on), asv (exact if max(m,n) <= 20,
  else asv's uncorrected normal approximation). Ratio and the 1.1 factor are unchanged; alpha 0.002.
Writes results/raw/stats_exact/recompute.json and prints every verdict whose status changes under exact or asv.
"""
import json
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
import sys; sys.path.insert(0, str(exp / "harness"))
from bth import stats  # noqa: E402

RAW = exp / "results/raw"
M = stats.MWU_METHODS


def group(runs, key_label="label"):
    S = {}
    for r in runs:
        if r.get("error") or r.get("skipped"):
            continue
        S.setdefault(r["id"], {}).setdefault((r.get(key_label) or r.get("state"), r.get("repeat", 0)), []).extend(r.get("samples") or [])
    return S


def judge(a, b):
    out = {m: stats.asv_rule(a, b, method=m) for m in M}
    return {"n": [len(a), len(b)], "ratio": out["exact"].ratio, "ties": stats.n_ties(a, b),
            **{m: {"p": v.p, "status": v.status} for m, v in out.items()}}


def pooled(d, lab, reps):
    return sum((d.get((lab, r), []) for r in reps), [])


fam = {}
# 1. A/A noise floor (23 cases): per-repeat (15 v 15) and pooled (30 v 30)
aa = json.loads((RAW / "networkx/bench/aa/raw_runs.json").read_text())["runs"]
S = group(aa); f = {}
for b, d in S.items():
    for r in (0, 1):
        if d.get(("A", r)) and d.get(("B", r)):
            f[f"{b} | rep{r}"] = judge(d[("A", r)], d[("B", r)])
    f[f"{b} | pooled"] = judge(pooled(d, "A", (0, 1)), pooled(d, "B", (0, 1)))
fam["aa_noise_floor"] = f
# 2. slowdown oracle (reach / FULL, 2 x 3 x 3 repeats pooled = 18 v 18) and its 6 v 6 out-of-reach spot check
for i in range(10):
    p = RAW / f"networkx/slowdowns/{i:02d}.json"
    rec = json.loads(p.read_text())
    for key, runs_key, reps in (("oracle", "raw_runs", (0, 1, 2)), ("spot6v6", "spotcheck_raw_runs", (0, 1))):
        runs = rec.get(runs_key) or []
        if not runs:
            continue
        S = group(runs); f = {}
        for b, d in S.items():
            a, s = pooled(d, "base", reps), pooled(d, "slow", reps)
            if a and s:
                f[b] = judge(a, s)
        fam[f"slowdown{i:02d}_{key}"] = f
# 3. powered profile-completeness check (15 v 15)
for i in (0, 5, 6, 7, 9):
    rec = json.loads((RAW / f"networkx/slowdowns/spotcheck_powered/{i:02d}.json").read_text())
    S = group(rec["raw_runs"]); f = {}
    for b, d in S.items():
        a, s = pooled(d, "base", (0,)), pooled(d, "slow", (0,))
        if a and s:
            f[b] = judge(a, s)
    fam[f"powered{i:02d}"] = f
# 4. #9 post-hoc re-check (partial; pooled over the repeats present)
ck = RAW / "networkx/slowdowns/recheck9/runs.partial.jsonl"
if ck.exists():
    runs = [json.loads(l) for l in ck.read_text().splitlines() if l.strip()]
    S = group(runs); f = {}
    for b, d in S.items():
        for other in ("slow", "base2"):
            a, s = pooled(d, "base", (0, 1)), pooled(d, other, (0, 1))
            if a and s:
                f[f"{other}_vs_base"] = judge(a, s)
    fam["recheck9"] = f

changes, counts = [], {}
for name, f in fam.items():
    c = counts.setdefault(name, {m: {} for m in M})
    for k, v in f.items():
        for m in M:
            c[m][v[m]["status"]] = c[m].get(v[m]["status"], 0) + 1
        if len({v[m]["status"] for m in M}) > 1:
            changes.append({"family": name, "case": k, "n": v["n"], "ratio": v["ratio"], "ties": v["ties"],
                            **{m: v[m] for m in M}})
mins = {f"{m}x{n}": {meth: stats.min_attainable_p(m, n, meth) for meth in M} for m, n in ((6, 6), (12, 12), (15, 15), (18, 18), (24, 24), (30, 30))}
out = RAW / "stats_exact"; out.mkdir(parents=True, exist_ok=True)
(out / "recompute.json").write_text(json.dumps({"methods": M, "alpha": 0.002, "factor": 1.1, "counts": counts,
                                                "changes": changes, "min_attainable_p": mins, "families": fam}, indent=1))
for name, c in counts.items():
    print(name, {m: c[m] for m in M})
print("CHANGES:", len(changes))
for ch in changes:
    print(" ", ch["family"], ch["case"][:90], ch["n"], round(ch["ratio"], 3), "ties", ch["ties"],
          {m: (ch[m]["status"], f"{ch[m]['p']:.2e}") for m in M})
print("min p:", json.dumps(mins))
