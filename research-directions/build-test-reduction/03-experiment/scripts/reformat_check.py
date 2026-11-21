"""List whole-file reformat commits between <base> and <last-edit> (read-only git).

Usage: python3 reformat_check.py <clone> <rev> <base> <last-edit>
Rule: non-merge commit (first-parent walk of <rev> restricted to base..last-edit) whose subject matches
(?i)\b(STY|style|format|black|ruff|cpplint|clang-format|reformat|lint)\b and that changes >=50% of the
lines of at least one package source file. ratio = max(added, deleted) / max(lines_before, lines_after).
Package source = .py/.c/.h/.pyx/.pxd/.cpp/.hpp, excluding tests, benchmark(s), asv_bench, doc*, .github, tools, setup/versioneer.
The window should start after the last such commit: prints that commit as `last_reformat`.
"""
import re, subprocess, sys
clone, rev, base, last = sys.argv[1:5]
clone = clone.replace("~", __import__("os").path.expanduser("~"), 1)
def git(*a):
    return subprocess.run(["git", "-c", "core.quotepath=false", "-C", clone, *a], capture_output=True, text=True, check=True).stdout
PAT = re.compile(r"\b(STY|style|format|black|ruff|cpplint|clang-format|reformat|lint)\b", re.I)
EXT = (".py", ".c", ".h", ".pyx", ".pxd", ".cpp", ".hpp")
def is_src(p):
    if not p.endswith(EXT): return False
    parts = p.split("/")
    if any(x in ("tests", "test", "benchmark", "benchmarks", "asv_bench", ".github", "tools", "docs", "doc") or x.startswith("doc") for x in parts[:-1]): return False
    return parts[-1] not in ("setup.py", "versioneer.py", "conftest.py", "_version.py")
def nlines(sha, p):
    r = subprocess.run(["git", "-C", clone, "show", f"{sha}:{p}"], capture_output=True)
    return r.stdout.count(b"\n") if r.returncode == 0 else 0
# first-parent chain of rev, restricted to commits in base..last (topologically)
inrange = set(git("rev-list", "--no-merges", f"{base}..{last}").split())
chain = [s for s in git("rev-list", "--first-parent", "--no-merges", rev).split() if s in inrange]
chain.reverse()
print(f"# reformat_check clone={clone} rev={rev[:10]} base={base[:10]} last={last[:10]}; {len(chain)} non-merge commits in range (first-parent, oldest first)")
hits = []
for sha in chain:
    subj = git("show", "-s", "--format=%s", sha).strip()
    if not PAT.search(subj): continue
    rows = []
    for l in git("diff-tree", "--no-commit-id", "--numstat", "-r", "--no-renames", sha).splitlines():
        a, d, p = l.split("\t", 2)
        if a == "-" or not is_src(p): continue
        a, d = int(a), int(d)
        tot = max(nlines(sha, p), nlines(sha + "^", p), 1)
        rows.append((p, a, d, tot, max(a, d) / tot))
    big = [r for r in rows if r[4] >= 0.5]
    print(f"{sha[:8]} {git('show','-s','--format=%ad',  '--date=short', sha).strip()} {'REFORMAT' if big else 'no'} {subj}")
    for p, a, d, tot, ratio in sorted(rows, key=lambda r: -r[4])[:6]:
        print(f"    {ratio:5.2f}  +{a} -{d} / {tot}  {p}")
    if big: hits.append(sha)
print("reformat_commits:", " ".join(h[:8] for h in hits) or "none")
if hits:
    print("last_reformat:", hits[-1])
    print("first commit after it in chain:", chain[chain.index(hits[-1]) + 1] if chain.index(hits[-1]) + 1 < len(chain) else "-")
