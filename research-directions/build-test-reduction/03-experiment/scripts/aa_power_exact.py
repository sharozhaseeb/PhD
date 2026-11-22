"""A/A bootstrap power under the exact MWU (PM 15:57). Same procedure as aa_noise_nx.analyse (seed 20261122,
15 v 15 resamples of each case's pooled A and B, B scaled by the shift, 200 draws), run for both methods.
Usage (WSL, low priority): PYTHONPATH=harness nice -n 19 taskset -c 0,1 ~/bt-lab/exp/venvs/nx/bin/python scripts/aa_power_exact.py
"""
import json, random, statistics as stt
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
import sys; sys.path.insert(0, str(exp / "harness"))
from bth import stats  # noqa: E402

runs = json.loads((exp / "results/raw/networkx/bench/aa/raw_runs.json").read_text())["runs"]
S = {}
for r in runs:
    if not (r.get("error") or r.get("skipped")):
        S.setdefault(r["id"], {}).setdefault(r["label"], []).extend(r["samples"])
res = {}
for method in ("scipy_auto", "exact"):
    rng = random.Random(20261122); power = {}
    for b, d in S.items():   # same iteration order and rng use as the original
        A, B = d.get("A", []), d.get("B", [])
        if len(A) < 5 or len(B) < 5 or min(A + B) <= 0:
            continue
        power[b] = {}
        for sh in (1.12, 1.2, 1.5, 2.0):
            hit = 0
            for _ in range(200):
                x = [rng.choice(A) for _ in range(15)]; y = [rng.choice(B) * sh for _ in range(15)]
                hit += stats.asv_rule(x, y, method=method).status == "slower"
            power[b][str(sh)] = hit / 200
    med = lambda ks: {sh: (stt.median(power[b][sh] for b in ks) if ks else None) for sh in ("1.12", "1.2", "1.5", "2.0")}
    alg = [b for b in power if b.startswith("benchmark_algorithms.")]; oth = [b for b in power if b not in alg]
    res[method] = {"median_all": med(list(power)), "median_algorithms": med(alg), "median_other": med(oth), "n": len(power), "per_case": power}
orig = json.loads((exp / "results/raw/networkx/bench/aa/aa_result.json").read_text())["power_measured_noise"]
res["original_reported"] = {k: orig[k] for k in ("median_all", "median_algorithms", "median_other")}
(exp / "results/raw/stats_exact/aa_power_exact.json").write_text(json.dumps(res, indent=1))
for k in ("original_reported", "scipy_auto", "exact"):
    v = res[k]; print(k, {g: v[g] for g in ("median_all", "median_algorithms", "median_other")})
