"""Q3 diagnosis (post-hoc, labelled): why pvlib reached 0 and geopandas only 56 functions.

1. Per edit: does the asv benchmark dir exist at the edit's parent? (pvlib base 2014 predates its suite.)
2. Name-based reach bound (W3-new, OVER-approximation, the same rule used for bottleneck's C functions):
   a changed function counts as reached if its last qualname component appears as an identifier/attribute/
   string word in the benchmark sources at the edit's parent. Static reach (call graph) under-approximates
   for OO APIs (method calls on objects of unknown type, getattr(obj, name)); name-based over-approximates.
   The truth lies between the two.
Writes results/q3/q3_diag.json. No timing, no execution of project code.
"""
import json, re, subprocess
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
REPOS = Path.home() / "bt-lab/exp/repos"
res = json.loads((exp / "results/q3/q3_b1_static.json").read_text())
out = {}
for d in res["detail"]:
    proj = d["project"]
    if proj not in ("geopandas", "pvlib-python"):
        continue
    meta = json.loads((exp / f"edits/{proj}.q3.candidates.json").read_text())
    repo, bdir = REPOS / proj, meta["bench_dir"]
    rows = []
    for e in d["edits"]:
        par = e["sha"] + "^"
        files = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", par, "--", bdir],
                               capture_output=True, text=True).stdout.split()
        py = [f for f in files if f.endswith(".py")]
        src = "\n".join(subprocess.run(["git", "-C", str(repo), "show", f"{par}:{f}"], capture_output=True,
                                       text=True).stdout for f in py)
        names = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", src))
        date = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%ad", "--date=short", e["sha"]],
                              capture_output=True, text=True).stdout.strip()
        hit = sorted(f for f in e["changed_functions"] if f.split("::")[-1].split(".")[-1] in names)
        rows.append({"sha": e["sha"][:10], "date": date, "suite_at_parent": bool(py), "n_bench_files": len(py),
                     "static_unreached": e["unreached_edit"], "name_reached": hit,
                     "name_unreached": bool(py) and not hit})
    with_suite = [r for r in rows if r["suite_at_parent"]]
    out[proj] = {"n_edits": len(rows), "n_with_suite_at_parent": len(with_suite),
                 "static_unreached_among_with_suite": sum(r["static_unreached"] for r in with_suite),
                 "name_unreached_among_with_suite": sum(r["name_unreached"] for r in with_suite),
                 "edits": rows}
(exp / "results/q3/q3_diag.json").write_text(json.dumps(out, indent=1))
for p, v in out.items():
    print(p, {k: v[k] for k in v if k != "edits"})
    for r in v["edits"]:
        print("  ", r["date"], r["sha"], "suite" if r["suite_at_parent"] else "NO-SUITE", "static_unreached" if r["static_unreached"] else "static_reached",
              "name_hit" if r["name_reached"] else "name_miss")
