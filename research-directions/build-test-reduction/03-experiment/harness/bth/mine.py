"""Deterministic commit mining (rule 1.3 of readiness.md; W3-new).

Selects non-merge commits whose subject matches a regex, measures the package
source part of each commit, and flags AI-authored commits. Uses `git` through
subprocess (no shell); never modifies the repository.

CLI: python -m bth.mine --config configs/networkx.toml --out edits/networkx.candidates.json
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from datetime import date as _date
from pathlib import Path

_AI_TAG = re.compile(r"\[(CLAUDE|CODEX)\]", re.I)
_AI_TRAILER = re.compile(
    r"^co-authored-by:.*(claude|anthropic|codex|openai|chatgpt|copilot|gemini|cursor|aider|devin)",
    re.I | re.M)


def _git(repo, *args) -> bytes:
    return subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=str(repo),
                          check=True, capture_output=True).stdout


def _match(path: str, globs) -> bool:
    for g in globs:
        if fnmatch.fnmatchcase(path, g) or fnmatch.fnmatchcase(path, g.replace("**/", "")):
            return True
    return False


def _day(iso: str) -> _date:
    return _date.fromisoformat(iso[:10])    # author-local calendar date


def _numstat(repo, sha):
    raw = _git(repo, "diff-tree", "--no-commit-id", "--numstat", "-r", "-z", "--root",
               "--no-renames", sha).decode("utf-8", "replace")
    out = []
    for item in raw.split("\0"):
        if not item:
            continue
        a, d, path = item.split("\t", 2)
        out.append((path, 0 if a == "-" else int(a), 0 if d == "-" else int(d)))
    return out


def mine(repo, *, regex, src_globs, exclude_globs, max_lines, before, after=None,
         limit=None, first_parent=True, rev="HEAD") -> list:
    """Candidate commits, oldest first.

    `after` is inclusive, `before` exclusive (ISO dates, compared on the author's
    calendar date). Records cover every non-merge commit whose subject matches
    `regex`; `qualifies` applies the file/size rule. With `limit`, only the most
    recent `limit` *qualifying* commits (and the non-qualifying ones after the
    earliest of them) are kept."""
    pat = re.compile(regex, re.I)
    lo = _date.fromisoformat(after) if after else None
    hi = _date.fromisoformat(before)
    args = ["log", "--no-merges", "--topo-order", "--format=%H%x1f%aI%x1f%s%x1f%B%x1e"]
    if first_parent:
        args.append("--first-parent")
    args.append(rev)   # explicit revision: mining must not depend on where the clone's HEAD is
    raw = _git(repo, *args).decode("utf-8", "replace")
    records = []
    for entry in raw.split("\x1e"):
        entry = entry.strip("\n")
        if not entry:
            continue
        sha, iso, subject, body = entry.split("\x1f", 3)
        day = _day(iso)
        if day >= hi or (lo and day < lo) or not pat.search(subject):
            continue
        files, lines = [], 0
        for path, a, d in _numstat(repo, sha):
            if _match(path, src_globs) and not _match(path, exclude_globs):
                files.append(path)
                lines += a + d
        files.sort()
        if not files:
            qualifies, reason = False, "no package source files changed"
        elif lines > max_lines:
            qualifies, reason = False, f"{lines} source lines > {max_lines}"
        else:
            qualifies, reason = True, ""
        records.append({
            "sha": sha, "date": iso, "subject": subject, "files": files, "src_lines": lines,
            "ai_authored": bool(_AI_TAG.search(subject + "\n" + body) or _AI_TRAILER.search(body)),
            "qualifies": qualifies, "reason": reason,
        })
    records.reverse()          # git log is newest first
    if limit is not None:
        idx = [i for i, r in enumerate(records) if r["qualifies"]]
        keep = idx[-limit:] if limit > 0 else []
        records = records[keep[0]:] if keep else []
    return records


def _load_config(path: Path) -> dict:
    import tomllib
    cfg = tomllib.loads(path.read_text(encoding="utf-8"))
    return cfg.get("mine", cfg)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args(argv)
    cfgp = Path(ns.config)
    cfg = _load_config(cfgp)
    repo = Path(cfg["repo"]).expanduser()
    if not repo.is_absolute() and not repo.exists():
        repo = cfgp.parent / repo
    res = mine(repo, regex=cfg["regex"], src_globs=cfg["src_globs"],
               exclude_globs=cfg.get("exclude_globs", []), max_lines=cfg["max_lines"],
               before=cfg["before"], after=cfg.get("after"), limit=cfg.get("limit"),
               first_parent=cfg.get("first_parent", True))
    out = Path(ns.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(res)} candidates ({sum(r['qualifies'] for r in res)} qualify) -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
