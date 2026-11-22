"""(e) Agent-labelling input (owner decision 15:43 via PM): frozen/labelling/sheet.jsonl, one row per mined commit.

Usage (WSL, low priority): nice -n 19 taskset -c 0,1 python3 scripts/labelling_jsonl.py
Rows: every mined commit record (qualifying or not) of networkx, bottleneck, geopandas, pvlib-python, in a seeded
shuffle (20261122). Fields: id, repo, sha, date, subject, body, diffstat, diff (first 300 lines of `git show --format=`,
truncated flag), link. Deliberately absent: rule output, reach, replay status, earlier labels.
"""
import json, random, subprocess
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
REPOS = Path.home() / "bt-lab/exp/repos"
SRC = [("networkx", "networkx/networkx", "edits/networkx.candidates.json"),
       ("bottleneck", "pydata/bottleneck", "edits/bottleneck.candidates.json"),
       ("geopandas", "geopandas/geopandas", "edits/geopandas.q3.candidates.json"),
       ("pvlib-python", "pvlib/pvlib-python", "edits/pvlib-python.q3.candidates.json")]
MAXL = 300


def git(repo, *a):
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, errors="replace").stdout


rows = []
for proj, gh, f in SRC:
    d = json.loads((exp / f).read_text())
    for r in (d["records"] if isinstance(d, dict) else d):
        sha, repo = r["sha"], REPOS / proj
        diff = git(repo, "show", "--format=", "--no-color", sha).splitlines()
        rows.append({"repo": gh, "sha": sha, "date": r.get("date", "")[:10], "subject": r["subject"],
                     "body": git(repo, "show", "-s", "--format=%b", sha).strip(),
                     "diffstat": git(repo, "show", "--format=", "--stat=120", sha).strip(),
                     "diff": "\n".join(diff[:MAXL]), "diff_lines_total": len(diff), "diff_truncated": len(diff) > MAXL,
                     "link": f"https://github.com/{gh}/commit/{sha}"})
random.Random(20261122).shuffle(rows)
out = exp / "frozen/labelling"; out.mkdir(parents=True, exist_ok=True)
with open(out / "sheet.jsonl", "w", encoding="utf-8") as fh:
    for k, r in enumerate(rows, 1):
        fh.write(json.dumps({"id": k, **r}, ensure_ascii=False) + "\n")
print(len(rows), "rows", {g: sum(r["repo"] == g for r in rows) for _, g, _ in SRC},
      "truncated", sum(r["diff_truncated"] for r in rows), "empty diffs", sum(not r["diff"] for r in rows))
