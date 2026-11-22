"""(e) Mining-precision labelling sheet (PM 15:20; TPM (e)). No timing; reads git history only.

Usage (WSL): python3 scripts/labelling_sheet.py  -> results/labelling/mining_precision_sheet.csv (+ README.md)
One row per mined commit record of the 4 already-mined projects (qualifying or not), in a seeded random order
(seed 20261122) so that raters do not see projects in blocks. Columns: what a rater needs to judge "is this commit an
optimization (intended to make code faster or use fewer resources)?" from its subject, diff summary and link, and two
empty rater blocks. Deliberately NOT included: benchmark reach, replay status, or any earlier label (raters stay blind).
"""
import csv, json, random, subprocess
from pathlib import Path

exp = Path(__file__).resolve().parents[1]
REPOS = Path.home() / "bt-lab/exp/repos"
SRC = [("networkx", "networkx/networkx", "edits/networkx.candidates.json"),
       ("bottleneck", "pydata/bottleneck", "edits/bottleneck.candidates.json"),
       ("geopandas", "geopandas/geopandas", "edits/geopandas.q3.candidates.json"),
       ("pvlib-python", "pvlib/pvlib-python", "edits/pvlib-python.q3.candidates.json")]


def git(repo, *a):
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True).stdout


rows = []
for proj, gh, f in SRC:
    d = json.loads((exp / f).read_text())
    recs = d["records"] if isinstance(d, dict) else d
    repo = REPOS / proj
    for r in recs:
        sha = r["sha"]
        num = [ln.split("\t") for ln in git(repo, "show", "--numstat", "--format=", sha).splitlines() if ln.count("\t") == 2]
        add = sum(int(a) for a, _, _ in num if a.isdigit()); rem = sum(int(b) for _, b, _ in num if b.isdigit())
        files = [p for _, _, p in num]
        hunks = sorted({h.split("@@")[-1].strip()[:60] for h in git(repo, "show", "--format=", "-U0", sha).splitlines()
                        if h.startswith("@@") and h.split("@@")[-1].strip()})
        body = " ".join(git(repo, "show", "-s", "--format=%b", sha).split())[:300]
        rows.append({"project": proj, "sha": sha[:12], "date": r.get("date", "")[:10], "subject": r["subject"],
                     "body_first_300_chars": body, "files_changed": "; ".join(files[:8]) + (" …" if len(files) > 8 else ""),
                     "lines_added": add, "lines_removed": rem, "hunk_contexts": " | ".join(hunks[:6]),
                     "link": f"https://github.com/{gh}/commit/{sha}",
                     "rater1_is_optimization": "", "rater1_reason": "", "rater2_is_optimization": "", "rater2_reason": ""})
random.Random(20261122).shuffle(rows)
for k, r in enumerate(rows, 1):
    r["row"] = k
out = exp / "results/labelling"; out.mkdir(parents=True, exist_ok=True)
cols = ["row"] + [c for c in rows[0] if c != "row"]
with open(out / "mining_precision_sheet.csv", "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
print(len(rows), "rows ->", out / "mining_precision_sheet.csv", {p: sum(r["project"] == p for r in rows) for p, _, _ in SRC})
