"""Kill sets for the frozen networkx mutants (readiness §4.1) and latent re-checks (§4.1b), in WSL.

Usage: ~/bt-lab/exp/venvs/nx/bin/python scripts/killsets_nx.py [--latent]
Own clone ~/bt-lab/exp/work/networkx-faults (never the oracle workdir). For each mutant: checkout its
state S_s, `git apply` the patch, run the FULL suite with -n 6 (counts only; not a timing), record the
failing node ids = K(m, S_s). Survivors (K empty) are candidates for the latent class: with --latent,
each survivor is re-applied at S_u for u = s+1..n (stops if the patch no longer applies) and re-run with
only the tests whose S_u depmap reaches the mutated function; the first u with failures is visible_from.
Writes results/raw/networkx/faults/killsets.json (+ latent.json).
"""
import json, os, subprocess, sys, tempfile, time
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(exp / "harness"))
from bth import junit  # noqa: E402

HOME = Path.home()
SRC, W = HOME / "bt-lab/exp/work/networkx-replay", HOME / "bt-lab/exp/work/networkx-faults"
PY = str(HOME / "bt-lab/exp/venvs/nx/bin/python")
out = exp / "results/raw/networkx/faults"; out.mkdir(parents=True, exist_ok=True)
if not W.exists():
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(SRC), str(W)], check=True)
git = lambda *a, **k: subprocess.run(["git", "-C", str(W), *a], capture_output=True, **k)
states = [s for s in json.loads((exp / "edits/networkx.states.json").read_text())["states"] if s["status"] == "applied"]
sha_at = {i + 1: s["state_sha"] for i, s in enumerate(states)}
muts = json.loads((exp / "frozen/networkx.mutants.json").read_text())
env = {**os.environ, "PYTHONPATH": str(W), "OMP_NUM_THREADS": "1"}


def run_tests(sha, patch, selected=None):
    git("checkout", "-q", "-f", "--detach", sha, check=True)
    git("clean", "-fdq", "-e", ".testmondata")
    ap = subprocess.run(["git", "-C", str(W), "apply", "-"], input=patch.encode(), capture_output=True)
    if ap.returncode != 0:
        return None, "patch does not apply"
    with tempfile.TemporaryDirectory() as td:
        jx = Path(td) / "j.xml"
        args = [PY, "-m", "pytest", "-p", "no:cacheprovider", "-q", "-x" if False else "-q", f"--junitxml={jx}", "-n", "5"]
        args += sorted(selected) if selected is not None else ["networkx"]
        if selected is not None and not selected:
            return set(), "no test reaches the function"
        t0 = time.time()
        subprocess.run(args, cwd=W, env=env, capture_output=True, timeout=1800)
        res = junit.parse(str(jx), rootdir=str(W)) if jx.exists() else {}
    failed = {t for t, v in res.items() if v["outcome"] == "failed"}
    return failed, f"{len(res)} tests in {time.time() - t0:.0f}s"


if "--latent" not in sys.argv:
    rec = []
    for m in muts:
        failed, note = run_tests(m["state_sha"], m["patch"])
        rec.append({"id": m["id"], "step": m["step"], "qualname": m["qualname"], "relpath": m["relpath"],
                    "op": m["op"], "kill_tests": sorted(failed or []), "note": note})
        print(m["step"], m["id"][-60:], "killed" if failed else "SURVIVED", len(failed or []), note, flush=True)
    (out / "killsets.json").write_text(json.dumps(rec, indent=1))
else:
    ks = json.loads((out / "killsets.json").read_text())
    dep_dir = exp / "results/raw/networkx/depmap"
    deps = {int(p.name[1:].split("_")[0]): json.loads(p.read_text())["deps"] for p in dep_dir.glob("S*_*.json")}
    lat = []
    for k in ks:
        if k["kill_tests"]:
            continue
        m = next(x for x in muts if x["id"] == k["id"])
        fid = f'{m["relpath"]}::{m["qualname"]}'
        vis = None
        for u in range(m["step"] + 1, len(states) + 1):
            sel = {t for t, fs in deps.get(u, {}).items() if fid in fs}
            failed, note = run_tests(sha_at[u], m["patch"], sel)
            if failed is None:
                print(k["id"][-50:], f"S{u}: {note}; stop"); break
            if failed:
                vis = {"visible_from": u, "kill_tests": sorted(failed)}; print(k["id"][-50:], f"LATENT visible at S{u}"); break
        lat.append({"id": k["id"], "step": m["step"], "latent": vis})
    (out / "latent.json").write_text(json.dumps(lat, indent=1))
