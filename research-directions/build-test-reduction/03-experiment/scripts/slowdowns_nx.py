"""Slowdown oracle for the frozen networkx slowdown candidates (readiness §4.2), in WSL, idle machine only.

Usage: ~/bt-lab/exp/venvs/nx/bin/python scripts/slowdowns_nx.py
For each frozen slowdown (frozen/networkx.slowdowns.json): two clones at its state S_s, one with the slowdown
patch applied. The measured benchmarks are those that can execute the slowed function: S0 profile ∪ static
reach ("reach-restricted oracle"; a benchmark that never runs the function cannot be slowed by it, except via
import-time code, a stated assumption). Interleaved A/B with bth.benchrun (2 processes × 3 values, 3 repeats,
CPUs 2-5); verdict = bth.stats.asv_rule (ratio > 1.1, MWU p < 0.002) on pooled samples.
OUT-OF-REACH SPOT CHECK (PM 19:27, against circularity): the frozen seeded sample of 10 cases
(frozen/networkx.slowdown_spotcheck.json) minus this slowdown's reach is measured too (1 process x 3 values x
2 repeats) and reported separately. Any out-of-reach "slower" verdict means reach-based selection is unsafe for
that slowdown (C11). Results are "detection within reach" + "out-of-reach spot check", never a plain miss rate.
A candidate enters the regression set only if >= 1 benchmark is "slower" with ratio >= 2.0 (ruling 2), or
1.2-1.5 for the moderate class. Each slowdown writes its own file results/raw/networkx/slowdowns/<i>.json.
"""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(exp / "harness"))
from bth import stats  # noqa: E402

HOME = Path.home()
SRC = HOME / "bt-lab/exp/work/networkx-replay"
PY = str(HOME / "bt-lab/exp/venvs/nx/bin/python")
out = exp / "results/raw/networkx/slowdowns"; out.mkdir(parents=True, exist_ok=True)
slows = json.loads((exp / "frozen/networkx.slowdowns.json").read_text())
prof = json.loads((exp / "results/raw/networkx/profile/S0_181f2951.json").read_text()).get("profiles", {})
static = json.loads((exp / "results/sim/networkx/inputs/static_reach_methods.json").read_text())
cases = json.loads(Path("/tmp/disc.json").read_text())
cases = cases["cases"] if isinstance(cases, dict) else cases
ids = [c["id"] for c in cases if c["kind"] == "time"]
spot = json.loads((exp / "frozen/networkx.slowdown_spotcheck.json").read_text())["sample"]


def clone(dst, sha, patch=None):
    if not dst.exists():
        subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(SRC), str(dst)], check=True)
    subprocess.run(["git", "-C", str(dst), "checkout", "-q", "-f", "--detach", sha], check=True)
    subprocess.run(["git", "-C", str(dst), "clean", "-fdxq"], check=True)
    if patch:
        r = subprocess.run(["git", "-C", str(dst), "apply", "-"], input=patch.encode(), capture_output=True)
        if r.returncode:
            raise RuntimeError(r.stderr.decode())


A, B = HOME / "bt-lab/exp/work/nx-slow-A", HOME / "bt-lab/exp/work/nx-slow-B"


def measure(benches, repeats, processes):
    """Interleaved base/slow measurement of `benches`; returns ({bench: verdict}, raw runs)."""
    filt = "^(" + "|".join(re.escape(b) for b in benches) + ")$"
    with tempfile.TemporaryDirectory() as td:
        o = Path(td) / "i.json"
        env = {**os.environ, "PYTHONPATH": str(exp / "harness"), "OMP_NUM_THREADS": "1"}
        subprocess.run([PY, "-m", "bth.benchrun", "interleave", "--state", f"base={A}", "--state", f"slow={B}",
                        "--python", PY, "--bench-dir", "benchmarks/benchmarks", "--filter", filt, "--repeats", repeats,
                        "--processes", processes, "--values", "3", "--cpus", "2-5", "--out", str(o)], env=env, check=True)
        runs = json.loads(o.read_text())
    runs = runs.get("results", runs) if isinstance(runs, dict) else runs
    samples, verdicts = {}, {}
    for r in runs:
        lab = r.get("state") or r.get("label")
        samples.setdefault(r["id"], {}).setdefault(lab, []).extend(r.get("samples") or [])
    for b, d in samples.items():
        if d.get("base") and d.get("slow"):
            v = stats.asv_rule(d["base"], d["slow"])
            verdicts[b] = {"ratio": v.ratio, "p": v.p, "status": v.status}
    return verdicts, runs
for i, sd in enumerate(slows):
    res_p = out / f"{i:02d}.json"
    if res_p.exists():
        continue
    fid = f'{sd["relpath"]}::{sd["qualname"]}'
    sel = [b for b in ids if fid in set(prof.get(b, [])) or fid in set(static.get(b.split("(")[0], []))]
    rec = {"slowdown": {k: sd[k] for k in ("step", "relpath", "qualname", "kind")}, "function": fid,
           "benches_measured": sel, "oracle": "within reach (S0 profile ∪ static reach) + out-of-reach spot check (frozen seeded sample)", "verdicts": {}}
    if not sel:
        rec["note"] = "no benchmark reaches the function per S0 profile/static reach; only the spot check is measured"
    clone(A, sd["state_sha"]); clone(B, sd["state_sha"], sd["patch"])
    out_of_reach = [b for b in spot if b not in set(sel)]
    rec["spotcheck_out_of_reach"] = out_of_reach
    res_p.with_suffix(".plan.json").write_text(json.dumps({"reach": sel, "spotcheck_out_of_reach": out_of_reach}, indent=1))
    rec["verdicts"], rec["raw_runs"] = measure(sel, "3", "2") if sel else ({}, [])
    rec["spotcheck_verdicts"], rec["spotcheck_raw_runs"] = measure(out_of_reach, "2", "1") if out_of_reach else ({}, [])
    sp = [b for b, v in rec["spotcheck_verdicts"].items() if v["status"] == "slower"]
    rec["spotcheck_detects"] = sp
    rec["reach_selection_unsafe_for_this_slowdown"] = bool(sp)
    rs = [v["ratio"] for v in rec["verdicts"].values() if v["status"] == "slower"]
    rec["max_slower_ratio"] = max(rs) if rs else None
    rec["class"] = ("strong (>=2x)" if rs and max(rs) >= 2.0 else "moderate (1.2-1.5x)" if rs and 1.2 <= max(rs) <= 1.5
                    else "other-slower" if rs else "not detected by FULL (excluded)")
    res_p.write_text(json.dumps(rec, indent=1))
    print(i, fid, rec["class"], len(sel), "benches", flush=True)
