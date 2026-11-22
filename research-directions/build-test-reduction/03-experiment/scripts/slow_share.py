"""Time share of the slowed function in each reaching benchmark case (W6 hostile review via PM 16:25). Compute only,
NOT a timing result: cProfile overhead inflates call-heavy code, so shares are approximate.

Usage (WSL, low priority): PYTHONPATH=harness nice -n 19 taskset -c 0,1 ~/bt-lab/exp/venvs/nx/bin/python scripts/slow_share.py
For slowdowns #2, #3, #8 (the ones with S0-profile-reaching cases; #1 and #4 have none) in a separate clone at the
slowdown's state (unpatched): per case, one process imports the module, runs setup, then calls the benchmark repeatedly
under cProfile (>= 3 calls and >= 0.5 s). share = inclusive time (cumtime) of the slowed function / total profiled time.
For a double_call slowdown, the expected timing ratio is about 1 + share (an upper bound if part of the work is cached).
Writes results/raw/networkx/slowdowns/share.json.
"""
import cProfile, json, os, pstats, subprocess, sys, time
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
CLONE = Path.home() / "bt-lab/exp/work/nx-share"
SRC = Path.home() / "bt-lab/exp/work/networkx-replay"
PY = str(Path.home() / "bt-lab/exp/venvs/nx/bin/python")

if len(sys.argv) > 1 and sys.argv[1] == "_case":
    sys.path.insert(0, str(exp / "harness"))
    from bth import benchrun
    a = json.loads(sys.argv[2])
    call, teardown = benchrun._prepare(a)
    rel, qual = a["fn"].split("::")
    pr = cProfile.Profile(); n = 0; t0 = time.perf_counter()
    pr.enable()
    while n < 3 or time.perf_counter() - t0 < 0.5:
        call(); n += 1
    pr.disable(); teardown()
    st = pstats.Stats(pr); tot = st.total_tt; cum = 0.0
    for (f, line, name), (cc, nc, tt, ct, callers) in st.stats.items():
        if f.endswith(rel) and name == qual.split(".")[-1]:
            cum = max(cum, ct)
    print("RESULT" + json.dumps({"calls": n, "total_s": tot, "fn_cum_s": cum, "share": cum / tot if tot else None}))
    sys.exit(0)

slows = json.loads((exp / "frozen/networkx.slowdowns.json").read_text())
prof = json.loads((exp / "results/raw/networkx/profile/S0_181f2951.json").read_text())["profiles"]
disc = {}
if not CLONE.exists():
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(SRC), str(CLONE)], check=True)
out = {}
for i in (2, 3, 8, 1, 4):
    sd = slows[i]; fid = f"{sd['relpath']}::{sd['qualname']}"
    cases = [b for b in prof if fid in set(prof[b])]
    out[i] = {"function": fid, "kind": sd["kind"], "state_sha": sd["state_sha"], "cases": {}}
    if not cases:
        out[i]["note"] = "no S0-profile-reaching case (reach is static-only)"; continue
    subprocess.run(["git", "-C", str(CLONE), "checkout", "-q", "-f", "--detach", sd["state_sha"]], check=True)
    subprocess.run(["git", "-C", str(CLONE), "clean", "-fdxq"], check=True)
    env = {**os.environ, "PYTHONPATH": str(exp / "harness"), "OMP_NUM_THREADS": "1"}
    dj = Path("/tmp/share_disc.json")
    subprocess.run([PY, "-m", "bth.benchrun", "discover", "--state", str(CLONE), "--bench-dir", "benchmarks/benchmarks",
                    "--python", PY, "--out", str(dj)], env=env, check=True, capture_output=True)
    cmap = {c["id"]: c for c in json.loads(dj.read_text())}
    for b in cases:
        payload = {"state": str(CLONE), "case": cmap[b], "fn": fid}
        r = subprocess.run([PY, __file__, "_case", json.dumps(payload)], env=env, cwd=str(CLONE), capture_output=True, text=True, timeout=900)
        line = [l for l in r.stdout.splitlines() if l.startswith("RESULT")]
        out[i]["cases"][b] = json.loads(line[0][6:]) if line else {"error": r.stderr[-400:]}
        print(i, b[-70:], out[i]["cases"][b].get("share"), flush=True)
(exp / "results/raw/networkx/slowdowns/share.json").write_text(json.dumps(out, indent=1))
