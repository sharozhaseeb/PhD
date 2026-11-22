"""Post-hoc re-check of spot-check #9 (plan: results/raw/networkx/slowdowns/recheck9/plan.md; PM 12:31).

Usage (WSL): PYTHONPATH=harness ~/bt-lab/exp/venvs/nx/bin/python scripts/recheck9_nx.py
"""
import json, os, re, subprocess, sys, tempfile, time
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(exp / "harness")); sys.path.insert(0, str(exp / "scripts"))
from bth import stats  # noqa: E402
import spotcheck_powered_nx as SP  # noqa: E402

out = exp / "results/raw/networkx/slowdowns/recheck9"; out.mkdir(parents=True, exist_ok=True)
SP.LOG = out / "driver.log"
CASE = "benchmark_algorithms.UndirectedAlgorithmBenchmarks.time_louvain_communities('Erdos Renyi (100, 0.9)')"
C = SP.HOME / "bt-lab/exp/work/nx-slow-C"
sd = SP.slows[9]

SP.log(f"recheck9 start: {CASE}; states base/slow/base2; 5x3, 2 repeats")
SP.clone(SP.A, sd["state_sha"]); SP.clone(SP.B, sd["state_sha"], sd["patch"]); SP.clone(C, sd["state_sha"])
g = SP.gate()
t0, l0 = time.time(), SP.load1()
SP.log(f"block recheck9 start load={l0}")
with tempfile.TemporaryDirectory() as td:
    o = Path(td) / "i.json"
    env = {**os.environ, "PYTHONPATH": str(exp / "harness"), "OMP_NUM_THREADS": "1"}
    subprocess.run([SP.PY, "-m", "bth.benchrun", "interleave", "--state", f"base={SP.A}", "--state", f"slow={SP.B}",
                    "--state", f"base2={C}", "--python", SP.PY, "--bench-dir", "benchmarks/benchmarks",
                    "--filter", "^" + re.escape(CASE) + "$", "--repeats", "2", "--processes", "5", "--values", "3",
                    "--cpus", "2-5", "--out", str(o), "--checkpoint", str(out / "runs.partial.jsonl")], env=env, check=True)
    runs = json.loads(o.read_text())
S = {}
for r in runs:
    S.setdefault((r["label"], r["repeat"]), []).extend(r.get("samples") or [])
def verdict(a, b):
    v = stats.asv_rule(a, b)
    return {"ratio": v.ratio, "p": v.p, "status": v.status, "n": [len(a), len(b)]}
pool = lambda lab: S.get((lab, 0), []) + S.get((lab, 1), [])
res = {"plan": "results/raw/networkx/slowdowns/recheck9/plan.md", "label": "POST HOC (context only; C11 flag stands)",
       "case": CASE, "gate_at_start": g, "load_start": l0, "wall_s": time.time() - t0,
       "peak_run_load": max(max(r.get("loadavg_before") or 0, r.get("loadavg_after") or 0) for r in runs),
       "slow_vs_base": {"pooled": verdict(pool("base"), pool("slow")),
                        **{f"rep{k}": verdict(S[("base", k)], S[("slow", k)]) for k in (0, 1)}},
       "base2_vs_base": {"pooled": verdict(pool("base"), pool("base2")),
                         **{f"rep{k}": verdict(S[("base", k)], S[("base2", k)]) for k in (0, 1)}},
       "order": [(r["repeat"], r["label"], r.get("t_start"), round(r["wall_s"])) for r in runs]}
(out / "result.json").write_text(json.dumps(res, indent=1))
SP.log(f"recheck9 done: slow/base {res['slow_vs_base']['pooled']['status']} {res['slow_vs_base']['pooled']['ratio']:.3f} "
       f"p={res['slow_vs_base']['pooled']['p']:.2g}; base2/base {res['base2_vs_base']['pooled']['status']} "
       f"{res['base2_vs_base']['pooled']['ratio']:.3f}")
SP.log("driver exit 0 (recheck9)")
