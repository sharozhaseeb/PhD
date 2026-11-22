"""Power at the paper's verdict design (PM 16:55 for W6). Compute only.
Same bootstrap as aa_power_exact.py (A/A re-run raw samples, seed 20261122, 200 draws, B scaled by the shift), but
18 v 18 resamples (2 processes x 3 values x 3 repeats pooled, the slowdown-oracle design), exact two-sided MWU,
and the verdict "slower" additionally needs ratio > 1 + 3 sigma(b), with sigma from aa/sigma_noise.json
(sigma_rep: 2 repeats only, rough; sigma_boot: sensitivity). Shifts 1.1, 1.2, 1.5, 2.0.
Usage (WSL, low priority): PYTHONPATH=harness nice -n 19 taskset -c 0,1 ~/bt-lab/exp/venvs/nx/bin/python scripts/aa_power_design.py
"""
import json, random, statistics as stt
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
import sys; sys.path.insert(0, str(exp / "harness"))
from bth import stats  # noqa: E402

runs = json.loads((exp / "results/raw/networkx/bench/aa/raw_runs.json").read_text())["runs"]
sig = json.loads((exp / "results/raw/networkx/bench/aa/sigma_noise.json").read_text())
S = {}
for r in runs:
    if not (r.get("error") or r.get("skipped")):
        S.setdefault(r["id"], {}).setdefault(r["label"], []).extend(r["samples"])
SH = (1.1, 1.2, 1.5, 2.0); N = 18
res = {}
for floor in ("none", "sigma_rep", "sigma_boot"):
    rng = random.Random(20261122); power = {}
    for b, d in S.items():
        A, B = d.get("A", []), d.get("B", [])
        if len(A) < 5 or len(B) < 5 or min(A + B) <= 0:
            continue
        fl = 1.0 if floor == "none" else 1 + 3 * sig[b][floor]
        power[b] = {}
        for sh in SH:
            hit = 0
            for _ in range(200):
                x = [rng.choice(A) for _ in range(N)]; y = [rng.choice(B) * sh for _ in range(N)]
                v = stats.asv_rule(x, y, method="exact")
                hit += v.status == "slower" and v.ratio > fl
            power[b][str(sh)] = hit / 200
    med = lambda ks: {str(sh): (stt.median(power[b][str(sh)] for b in ks) if ks else None) for sh in SH}
    alg = [b for b in power if b.startswith("benchmark_algorithms.")]; oth = [b for b in power if b not in alg]
    res[floor] = {"median_all": med(list(power)), "median_algorithms": med(alg), "median_other": med(oth),
                  "n": len(power), "n_algorithms": len(alg), "per_case": power}
(exp / "results/raw/stats_exact/aa_power_design18.json").write_text(json.dumps(res, indent=1))
for f, v in res.items():
    print(f, "all", v["median_all"], "| alg", v["median_algorithms"], "| other", v["median_other"])
