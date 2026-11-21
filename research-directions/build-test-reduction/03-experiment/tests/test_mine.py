"""Tests for bth.mine on a throwaway git repo (spec: Implementer 1)."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from bth.mine import mine

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git missing")

HARNESS = Path(__file__).resolve().parents[1] / "harness"
REGEX = r"(\bperf\b|speed ?up|faster|optimi[sz](e|ation|ing|ed)\b|performance|vectori[sz]|efficien)"
KW = dict(regex=REGEX, src_globs=["pkg/*.py"], exclude_globs=["tests/*", "docs/*"],
          max_lines=10, before="2021-01-01")


def git(cwd, *args, date="2020-01-01T12:00:00+00:00"):
    env = {**os.environ, "GIT_AUTHOR_NAME": "A", "GIT_AUTHOR_EMAIL": "a@x.invalid",
           "GIT_COMMITTER_NAME": "A", "GIT_COMMITTER_EMAIL": "a@x.invalid",
           "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
    r = subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=cwd, env=env,
                       check=True, capture_output=True)
    return r.stdout.decode().strip()


def put(repo, rel, text):
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode())


def edit_line(repo, rel, n, new):
    p = repo / rel
    lines = p.read_bytes().decode().split("\n")
    lines[n - 1] = new
    p.write_bytes("\n".join(lines).encode())


def commit(repo, msg, day):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", msg, date=f"2020-01-{day:02d}T12:00:00+00:00")
    return git(repo, "rev-parse", "HEAD")


def build_repo(tmp_path):
    repo = tmp_path / "src"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    body = "\n".join(f"line{i}" for i in range(1, 9)) + "\n"
    for f in ("mod", "other", "third"):
        put(repo, f"pkg/{f}.py", body)
    put(repo, "tests/test_x.py", body)
    put(repo, "docs/r.md", body)
    s = {"c0": commit(repo, "initial", 1)}
    edit_line(repo, "pkg/mod.py", 2, "fast2")
    edit_line(repo, "tests/test_x.py", 2, "t2")
    s["c1"] = commit(repo, "perf: speed up foo", 2)
    edit_line(repo, "pkg/mod.py", 6, "REFACTORED")
    s["c2"] = commit(repo, "refactor: tidy", 3)
    edit_line(repo, "pkg/other.py", 3, "opt3")
    s["c3"] = commit(repo, "PERF: optimise bar", 4)
    edit_line(repo, "pkg/mod.py", 6, "FASTER6")
    s["c4"] = commit(repo, "perf: faster loop on tidy code", 5)
    edit_line(repo, "pkg/other.py", 5, "BAD")
    s["c5"] = commit(repo, "perf: speedup that breaks [CLAUDE]", 6)
    edit_line(repo, "pkg/third.py", 2, "t2fast")
    s["c6"] = commit(repo, "perf: faster third\n\nCo-authored-by: Claude <noreply@anthropic.com>", 7)
    put(repo, "pkg/mod.py", (repo / "pkg/mod.py").read_bytes().decode() +
        "\n".join(f"x{i}" for i in range(30)) + "\n")
    s["c7"] = commit(repo, "perf: huge rewrite", 8)
    edit_line(repo, "docs/r.md", 1, "doc")
    s["c8"] = commit(repo, "perf: docs only", 9)
    git(repo, "checkout", "-q", "-b", "side", s["c8"])
    edit_line(repo, "pkg/third.py", 5, "side5")
    s["side"] = commit(repo, "perf: faster side branch", 10)
    git(repo, "checkout", "-q", "main")
    git(repo, "merge", "-q", "--no-ff", "-m", "Merge side", "side", date="2020-01-11T12:00:00+00:00")
    return repo, s


def test_candidates_flags_and_order(tmp_path):
    repo, s = build_repo(tmp_path)
    res = mine(repo, **KW)
    assert [r["sha"] for r in res] == [s[k] for k in ("c1", "c3", "c4", "c5", "c6", "c7", "c8")]
    by = {r["sha"]: r for r in res}
    assert all(set(r) >= {"sha", "date", "subject", "files", "src_lines", "ai_authored",
                          "qualifies", "reason"} for r in res)
    c1 = by[s["c1"]]
    assert c1["files"] == ["pkg/mod.py"] and c1["src_lines"] == 2 and c1["qualifies"]
    assert not c1["ai_authored"] and c1["subject"] == "perf: speed up foo"
    assert by[s["c5"]]["ai_authored"] and by[s["c6"]]["ai_authored"]
    assert not by[s["c7"]]["qualifies"] and by[s["c7"]]["src_lines"] > 10 and by[s["c7"]]["reason"]
    assert not by[s["c8"]]["qualifies"] and by[s["c8"]]["files"] == [] and by[s["c8"]]["reason"]
    assert s["c2"] not in by                       # subject does not match


def test_first_parent_toggle(tmp_path):
    repo, s = build_repo(tmp_path)
    assert s["side"] not in [r["sha"] for r in mine(repo, **KW)]
    allr = mine(repo, first_parent=False, **KW)
    assert s["side"] in [r["sha"] for r in allr]
    assert all("Merge" not in r["subject"] for r in allr)   # merges never listed


def test_deterministic_and_repo_untouched(tmp_path):
    repo, s = build_repo(tmp_path)
    (repo / "dirty.txt").write_text("x")
    before = git(repo, "status", "--porcelain")
    assert mine(repo, **KW) == mine(repo, **KW)
    assert git(repo, "status", "--porcelain") == before and (repo / "dirty.txt").exists()


def test_window_and_limit(tmp_path):
    repo, s = build_repo(tmp_path)
    kw = {**KW, "before": "2020-01-06"}
    res = mine(repo, after="2020-01-03", **kw)
    assert [r["sha"] for r in res] == [s["c3"], s["c4"]]      # after inclusive, before exclusive
    res = mine(repo, limit=2, **KW)
    assert [r["sha"] for r in res if r["qualifies"]] == [s["c5"], s["c6"]]


def test_cli(tmp_path):
    repo, s = build_repo(tmp_path)
    cfg = tmp_path / "cfg.toml"
    cfg.write_text(
        f'repo = "{repo.as_posix()}"\nregex = \'{REGEX}\'\nsrc_globs = ["pkg/*.py"]\n'
        'exclude_globs = ["tests/*", "docs/*"]\nmax_lines = 10\nbefore = "2021-01-01"\n')
    out = tmp_path / "out" / "c.json"
    env = {**os.environ, "PYTHONPATH": str(HARNESS)}
    subprocess.run([sys.executable, "-m", "bth.mine", "--config", str(cfg), "--out", str(out)],
                   check=True, env=env, cwd=tmp_path)
    assert json.loads(out.read_text()) == mine(repo, **KW)
