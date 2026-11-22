"""Per-edit time share of the changed functions in each reaching case (advisor draft review via PM 16:44). Compute
only, NOT timing: cProfile overhead inflates call-heavy code, so shares are approximate (same method as slow_share.py).

Usage (WSL, low priority): PYTHONPATH=harness nice -n 19 taskset -c 0,1 ~/bt-lab/exp/venvs/nx/bin/python scripts/edit_share.py
For each of the 14 agent-OPT replayed networkx edits (results/q3/b1_construct.json): reaching cases = cases whose S0
profile contains any changed function (module-level excluded). In a separate clone at the edit's PARENT state (the code
the edit optimizes), one process per benchmark module imports once and profiles each reaching case (setup, then calls
under cProfile for >= 3 calls and >= 0.5 s). Per case: share = max over changed functions of inclusive time / total
(a lower bound on the union); share_sum = min(1, sum over changed functions) (an upper bound). Expected ratio for a
uniform slowdown f of the changed functions: 1 + share * (f - 1). Edits not executed by any S0-profiled case: share 0.
Writes results/raw/networkx/edit_share.json.
"""
import cProfile, json, os, pstats, subprocess, sys, time
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
CLONE = Path.home() / "bt-lab/exp/work/nx-share"
PY = str(Path.home() / "bt-lab/exp/venvs/nx/bin/python")

if len(sys.argv) > 1 and sys.argv[1] == "_group":
    sys.path.insert(0, str(exp / "harness"))
    from bth import benchrun
    a = json.loads(Path(sys.argv[2]).read_text())
    for c in a["cases"]:
        call, teardown = benchrun._prepare({"state": a["state"], "case": c})
        pr = cProfile.Profile(); n = 0; t0 = time.perf_counter()
        pr.enable()
        while n < 3 or time.perf_counter() - t0 < 0.5:
            call(); n += 1
        pr.disable(); teardown()
        st = pstats.Stats(pr); tot = st.total_tt; per = {}
        for f in a["fns"]:
            rel, qual = f.split("::"); leaf = qual.split(".")[-1]
            per[f] = max([ct for (fn, _l, name), (_cc, _nc, _tt, ct, _c) in st.stats.items()
                          if fn.endswith(rel) and name == leaf] or [0.0])
        print("RESULT" + json.dumps({"id": c["id"], "calls": n, "total_s": tot, "fn_cum_s": per,
                                     "share": max(per.values()) / tot if tot else None,
                                     "share_sum": min(1.0, sum(per.values()) / tot) if tot else None}), flush=True)
    sys.exit(0)

steps = json.loads((exp / "results/q3/b1_construct.json").read_text())["steps"]
states = [s for s in json.loads((exp / "edits/networkx.states.json").read_text())["states"] if s["status"] == "applied"]
S0 = "181f295117f7f7488644c87f04699290f8e49188"
prof = json.loads((exp / "results/raw/networkx/profile/S0_181f2951.json").read_text())["profiles"]
env = {**os.environ, "PYTHONPATH": str(exp / "harness"), "OMP_NUM_THREADS": "1"}
out = {}
for r in steps:
    if r["agents"] != "OPT":
        continue
    k = r["step"]; fns = [f["fn"] for f in r["functions"]]
    cases = [b for b in prof if set(fns) & set(prof[b])]
    parent = S0 if k == 1 else states[k - 2]["state_sha"]
    rec = {"step": k, "parent": parent, "changed_functions": fns, "executed_S0_profile": bool(cases), "cases": {}}
    if not cases:
        rec.update({"max_share": 0.0, "note": "not executed by any S0-profiled case"}); out[k] = rec; continue
    subprocess.run(["git", "-C", str(CLONE), "checkout", "-q", "-f", "--detach", parent], check=True)
    subprocess.run(["git", "-C", str(CLONE), "clean", "-fdxq"], check=True)
    dj = Path("/tmp/edit_share_disc.json")
    subprocess.run([PY, "-m", "bth.benchrun", "discover", "--state", str(CLONE), "--bench-dir", "benchmarks/benchmarks",
                    "--python", PY, "--out", str(dj)], env=env, check=True, capture_output=True)
    cmap = {c["id"]: c for c in json.loads(dj.read_text())}
    for mod in sorted({b.split(".")[0] for b in cases}):
        pj = Path(f"/tmp/edit_share_{k}_{mod}.json")
        pj.write_text(json.dumps({"state": str(CLONE), "fns": fns, "cases": [cmap[b] for b in cases if b.startswith(mod + ".")]}))
        p = subprocess.run([PY, __file__, "_group", str(pj)], env=env, cwd=str(CLONE), capture_output=True, text=True, timeout=1800)
        for line in p.stdout.splitlines():
            if line.startswith("RESULT"):
                x = json.loads(line[6:]); rec["cases"][x.pop("id")] = x
        if p.returncode:
            rec.setdefault("errors", []).append(p.stderr[-400:])
    sh = [c["share"] for c in rec["cases"].values() if c.get("share") is not None]
    rec["max_share"] = max(sh) if sh else None
    rec["max_share_sum"] = max([c["share_sum"] for c in rec["cases"].values()] or [None])
    out[k] = rec
    print(k, len(cases), "cases; max share", rec["max_share"], flush=True)
for rec in out.values():
    s = rec.get("max_share") or 0.0
    rec["expected_ratio_at_1.2x"] = 1 + 0.2 * s; rec["expected_ratio_at_2x"] = 1 + s
(exp / "results/raw/networkx/edit_share.json").write_text(json.dumps(out, indent=1))
