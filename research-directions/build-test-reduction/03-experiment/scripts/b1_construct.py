"""B1 construct check (W6 hostile review via PM 16:25). Git + AST only, no execution.

Usage (WSL, low priority): nice -n 19 taskset -c 0,1 python3 scripts/b1_construct.py -> results/q3/b1_construct.json
For each replayed networkx step, each changed function (module-level excluded) is looked up by qualname in the AST of
its file at S0 and at the step's parent state (replayed sequence: parent of step k = state k-1, step 1 = S0).
A changed function absent at S0 cannot be in the S0 profile: such an edit is "unreached by construction" if none of
its changed functions exists at S0. Reach is the S0 measured profile (union over 171 cases), as in B1.
"""
import ast, json, subprocess
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
REPO = Path.home() / "bt-lab/exp/work/networkx-replay"
S0 = "181f295117f7f7488644c87f04699290f8e49188"
states = [s for s in json.loads((exp / "edits/networkx.states.json").read_text())["states"] if s["status"] == "applied"]
stat = json.loads((exp / "results/q3/q3_b1_static.json").read_text())["detail"][0]["edits"]
lab = {r["step"]: r for r in json.loads((exp / "results/labelling/precision_b1.json").read_text())["B1"]["per_step"]}
prof = json.loads((exp / "results/raw/networkx/profile/S0_181f2951.json").read_text())["profiles"]
reached = set().union(*map(set, prof.values()))
_cache = {}


def qualnames(sha, rel):
    k = (sha, rel)
    if k not in _cache:
        r = subprocess.run(["git", "-C", str(REPO), "show", f"{sha}:{rel}"], capture_output=True, text=True)
        names = set()
        if r.returncode == 0:
            def walk(node, pre):
                for ch in ast.iter_child_nodes(node):
                    if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        q = f"{pre}{ch.name}"
                        if not isinstance(ch, ast.ClassDef):
                            names.add(q)
                        walk(ch, q + ("." if isinstance(ch, ast.ClassDef) else ".<locals>."))
            walk(ast.parse(r.stdout), "")
        _cache[k] = (r.returncode == 0, names)
    return _cache[k]


rows = []
for e in stat:
    k = e["step"]; parent = S0 if k == 1 else states[k - 2]["state_sha"]
    fns = []
    for f in e["changed_functions"]:
        if f.endswith("::<module>"):
            continue
        rel, q = f.split("::", 1)
        f0, n0 = qualnames(S0, rel); fp, np_ = qualnames(parent, rel)
        fns.append({"fn": f, "file_at_S0": f0, "at_S0": q in n0, "at_parent": q in np_, "in_S0_profile": f in reached})
    exists0 = [x for x in fns if x["at_S0"]]
    rows.append({"step": k, "agents": lab[k]["agents"], "n_changed": len(fns), "n_at_S0": len(exists0),
                 "n_at_parent": sum(x["at_parent"] for x in fns),
                 "profile_unreached": lab[k]["profile_unreached"],
                 "unreached_by_construction": bool(fns) and not exists0, "functions": fns})
opt = [r for r in rows if r["agents"] == "OPT"]
constr = [r for r in opt if r["unreached_by_construction"]]
rest = [r for r in opt if not r["unreached_by_construction"]]
summ = {"agent_opt": len(opt), "profile_unreached": sum(r["profile_unreached"] for r in opt),
        "unreached_by_construction": [r["step"] for r in constr],
        "excluding_construction": {"k": sum(r["profile_unreached"] for r in rest), "n": len(rest)},
        "partial_absence": [{"step": r["step"], "absent_at_S0": [x["fn"] for x in r["functions"] if not x["at_S0"]]}
                            for r in opt if r["n_at_S0"] < r["n_changed"]]}
out = exp / "results/q3/b1_construct.json"
out.write_text(json.dumps({"summary": summ, "steps": rows}, indent=1))
print(json.dumps(summ, indent=1))
for r in opt:
    print(r["step"], "unreached" if r["profile_unreached"] else "reached", f"{r['n_at_S0']}/{r['n_changed']} at S0",
          f"{r['n_at_parent']}/{r['n_changed']} at parent", [x["fn"].split("::")[1] for x in r["functions"]][:4])
