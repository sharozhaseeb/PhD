"""Mine (F8 self-check against the frozen first-pass list) and build replay states for networkx.

Run in WSL:  PYTHONPATH=<03-experiment>/harness python3 scripts/replay_nx.py <03-experiment>
Stdlib only (WSL system python has no venv yet). check=None: FULL-test drop rule is applied later.
"""
import json, os, subprocess, sys, tomllib
from pathlib import Path

exp = Path(sys.argv[1])
cfg = tomllib.loads((exp / "configs/networkx.toml").read_text())
repo = Path(os.path.expanduser(cfg["repo"]["clone"]))
from bth.mine import mine
from bth.replay import build_states

m = cfg["mine"]
recs = mine(repo, regex=m["regex"], src_globs=m["src_globs"], exclude_globs=m["exclude_globs"],
            max_lines=m["max_lines"], before=m["before"], limit=m["limit"], first_parent=m["first_parent"],
            rev=cfg["repo"]["head_at_mining"])
q = [r for r in recs if r["qualifies"]]
print(f"mined: {len(recs)} records, {len(q)} qualifying")

# F8: compare with the frozen first-pass list (latest 20 'Y' lines)
fp = [l.split()[0] for l in (exp / "results/raw/networkx_mining_subject_rule.txt").read_text().splitlines()[3:23]]
mine_short = sorted(r["sha"][:8] for r in q)
ok = sorted(fp) == mine_short
print("F8 mine reproduces frozen subject-rule list:", ok)
if not ok:
    print("first-pass only:", sorted(set(fp) - set(mine_short)), "mine only:", sorted(set(mine_short) - set(fp)))
    sys.exit(2)

out = exp / "edits"; out.mkdir(exist_ok=True)
(out / "networkx.candidates.json").write_text(json.dumps(recs, indent=1))
base = cfg["replay"]["base"]
parent = subprocess.run(["git", "-C", str(repo), "rev-parse", q[0]["sha"] + "^"], capture_output=True, text=True).stdout.strip()
assert parent == base, (parent, base)
work = Path(os.path.expanduser("~/bt-lab/exp/work/networkx-replay"))
if work.exists():
    sys.exit(f"workdir exists: {work} (refusing to overwrite)")
states = build_states(repo, work, base, [{"sha": r["sha"], "date": r["date"]} for r in q],
                      cfg["replay"]["src_pathspec"], None)
(out / "networkx.states.json").write_text(json.dumps({"repo": "networkx", "base": base, "workdir": str(work), "states": states}, indent=1))
for s in states:
    print(s["orig_sha"][:8], s["status"], (s.get("state_sha") or "")[:8], s.get("reason") or "")
