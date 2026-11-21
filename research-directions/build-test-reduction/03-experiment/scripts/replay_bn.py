"""Mine bottleneck (window 2019-09-01..2020-12-31, explicit rev) and build replay states.

Run in WSL:  PYTHONPATH=<03-experiment>/harness python3 scripts/replay_bn.py <03-experiment>
Stdlib only. check=None: FULL-test drop rule is applied later (readiness 2).
Writes results/raw/bottleneck_mining.txt, edits/bottleneck.candidates.json, edits/bottleneck.states.json.
"""
import json, os, subprocess, sys, tomllib
from pathlib import Path

exp = Path(sys.argv[1])
cfg = tomllib.loads((exp / "configs/bottleneck.toml").read_text())
repo = Path(os.path.expanduser(cfg["repo"]["clone"]))
from bth.mine import mine
from bth.replay import build_states

m = cfg["mine"]
recs = mine(repo, regex=m["regex"], src_globs=m["src_globs"], exclude_globs=m["exclude_globs"],
            max_lines=m["max_lines"], before=m["before"], after=m["after"], limit=m.get("limit"),
            first_parent=m["first_parent"], rev=cfg["repo"]["head_at_mining"])
q = [r for r in recs if r["qualifies"]]
lines = [f"# bottleneck mining at {cfg['repo']['head_at_mining']}, window {m['after']}..{m['before']} (exclusive), max_lines={m['max_lines']}",
         f"# {len(recs)} subject matches, {len(q)} qualifying", "# sha8 date qualifies src_lines subject [files] reason"]
for r in recs:
    lines.append(f"{r['sha'][:8]} {r['date'][:10]} {'Y' if r['qualifies'] else 'N'} {r['src_lines']:4d} {r['subject']} {r['files']} {r['reason']}")
(exp / "results/raw/bottleneck_mining.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
if not q:
    sys.exit("no qualifying commits")

out = exp / "edits"; out.mkdir(exist_ok=True)
(out / "bottleneck.candidates.json").write_text(json.dumps(recs, indent=1))
parent = subprocess.run(["git", "-C", str(repo), "rev-parse", q[0]["sha"] + "^"], capture_output=True, text=True, check=True).stdout.strip()
base = cfg["replay"]["base"] or parent
assert base == parent, (base, parent)
print("base =", base)
work = Path(os.path.expanduser("~/bt-lab/exp/work/bottleneck-replay"))
if work.exists() and any(work.iterdir()):
    sys.exit(f"workdir exists: {work} (refusing to overwrite)")

# The source clone is blobless. bth.replay clones it locally WITHOUT promisor config, so any blob missing in the
# source ends up missing (-> silently deleted files in state commits). Hydrate every object needed first.
def hydrate(repo, base, last):
    def git(*a, inp=None):
        return subprocess.run(["git", "-C", str(repo), *a], input=inp, capture_output=True, text=True)
    def missing():
        objs = git("rev-list", "--objects", "--missing=print", "-1", base).stdout.splitlines()              + git("rev-list", "--objects", "--missing=print", f"{base}..{last}").stdout.splitlines()
        return sorted({l[1:] for l in objs if l.startswith("?")})
    miss = missing()
    print(f"hydrate: {len(miss)} missing objects to fetch")
    if miss:
        r = git("fetch", "origin", "--no-tags", "--no-write-fetch-head", "--filter=blob:none", "--stdin",
                inp=chr(10).join(miss) + chr(10))
        if r.returncode:
            sys.exit("hydrate failed: " + r.stderr)
    assert not missing()
hydrate(repo, base, q[-1]["sha"])
states = build_states(repo, work, base, [{"sha": r["sha"], "date": r["date"]} for r in q],
                      cfg["replay"]["src_pathspec"], None)
(out / "bottleneck.states.json").write_text(json.dumps({"repo": "bottleneck", "base": base, "workdir": str(work), "states": states}, indent=1))
for s in states:
    print(s["orig_sha"][:8], s["status"], (s.get("state_sha") or "")[:8], s.get("reason") or "")
print("applied", sum(s["status"] == "applied" for s in states), "dropped", sum(s["status"] != "applied" for s in states))
