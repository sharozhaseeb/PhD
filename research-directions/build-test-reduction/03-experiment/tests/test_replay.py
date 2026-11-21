"""Tests for bth.replay on a throwaway git repo (spec: Implementer 1)."""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from bth.mine import mine
from bth.replay import build_states

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git missing")

REGEX = r"(\bperf\b|speed ?up|faster)"
SRC = ["pkg"]


def git(cwd, *args, date="2020-01-01T12:00:00+00:00"):
    env = {**os.environ, "GIT_AUTHOR_NAME": "A", "GIT_AUTHOR_EMAIL": "a@x.invalid",
           "GIT_COMMITTER_NAME": "A", "GIT_COMMITTER_EMAIL": "a@x.invalid",
           "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
    r = subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=cwd, env=env,
                       check=True, capture_output=True)
    return r.stdout.decode().strip()


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
    (repo / "pkg").mkdir(parents=True)
    (repo / "tests").mkdir()
    git(repo, "init", "-q", "-b", "main")
    body = ("\n".join(f"line{i}" for i in range(1, 9)) + "\n").encode()
    for f in ("pkg/mod.py", "pkg/other.py", "pkg/third.py", "tests/test_x.py"):
        (repo / f).write_bytes(body)
    s = {"c0": commit(repo, "initial", 1)}
    edit_line(repo, "pkg/mod.py", 2, "fast2")
    edit_line(repo, "tests/test_x.py", 2, "t2")
    s["c1"] = commit(repo, "perf: speed up foo", 2)
    edit_line(repo, "pkg/mod.py", 6, "REFACTORED")
    s["c2"] = commit(repo, "refactor: tidy", 3)
    edit_line(repo, "pkg/other.py", 3, "opt3")
    s["c3"] = commit(repo, "perf: bar", 4)
    edit_line(repo, "pkg/mod.py", 6, "FASTER6")
    s["c4"] = commit(repo, "perf: faster, depends on refactor", 5)
    edit_line(repo, "pkg/other.py", 5, "BAD")
    s["c5"] = commit(repo, "perf: speedup that breaks the check", 6)
    edit_line(repo, "pkg/third.py", 2, "t2fast")
    s["c6"] = commit(repo, "perf: faster third", 7)
    return repo, s


def check(wd: Path):
    ok = b"BAD" not in (wd / "pkg/other.py").read_bytes()
    return ok, "contains BAD"


def snapshot(repo):
    return (git(repo, "rev-parse", "HEAD"), git(repo, "status", "--porcelain"),
            git(repo, "branch", "--list"),
            {p.relative_to(repo).as_posix(): p.read_bytes()
             for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts})


def edits_of(repo):
    return [r for r in mine(repo, regex=REGEX, src_globs=["pkg/*.py"], exclude_globs=["tests/*"],
                            max_lines=50, before="2021-01-01") if r["qualifies"]]


def test_statuses_contents_and_source_untouched(tmp_path):
    repo, s = build_repo(tmp_path)
    (repo / "dirty.txt").write_text("uncommitted")
    snap = snapshot(repo)
    wd = tmp_path / "work"
    recs = build_states(repo, wd, s["c0"], edits_of(repo), SRC, check)
    assert snapshot(repo) == snap                       # source repo never modified
    assert [r["orig_sha"] for r in recs] == [s[k] for k in ("c1", "c3", "c4", "c5", "c6")]
    assert [r["status"] for r in recs] == ["applied", "applied", "dropped", "dropped", "applied"]
    assert recs[2]["reason"] == "dropped: conflict"
    assert recs[3]["reason"] == "dropped: check failed: contains BAD"
    assert all(r["state_sha"] for r in recs if r["status"] == "applied")
    assert all(r["state_sha"] is None for r in recs if r["status"] == "dropped")
    # workdir is a separate clone, clean, on branch bth-replay, head == last state
    assert wd.resolve() != repo.resolve() and (wd / ".git").exists()
    assert git(wd, "rev-parse", "--abbrev-ref", "HEAD") == "bth-replay"
    assert git(wd, "rev-parse", "HEAD") == recs[-1]["state_sha"]
    assert git(wd, "status", "--porcelain") == ""
    mod = (wd / "pkg/mod.py").read_text().split("\n")
    assert mod[1] == "fast2" and mod[5] == "line6"      # c1 in, conflicting c4 out, no markers
    assert "<<<<" not in (wd / "pkg/mod.py").read_text()
    assert b"BAD" not in (wd / "pkg/other.py").read_bytes()
    assert (wd / "pkg/third.py").read_text().split("\n")[1] == "t2fast"
    assert not (wd / "tests/test_x.py").read_text().split("\n")[1] == "t2"   # tests not replayed
    log = git(wd, "log", "--format=%s", f"{s['c0']}..HEAD").split("\n")
    assert log == [f"bth step 4: {s['c6']}", f"bth step 1: {s['c3']}", f"bth step 0: {s['c1']}"]


def test_state_shas_reproducible(tmp_path):
    repo, s = build_repo(tmp_path)
    a = build_states(repo, tmp_path / "w1", s["c0"], edits_of(repo), SRC, check)
    b = build_states(repo, tmp_path / "w2", s["c0"], edits_of(repo), SRC, check)
    assert a == b and a[0]["state_sha"]


def test_no_check_and_nonempty_workdir(tmp_path):
    repo, s = build_repo(tmp_path)
    recs = build_states(repo, tmp_path / "w", s["c0"], edits_of(repo), SRC, None)
    assert [r["status"] for r in recs] == ["applied", "applied", "dropped", "applied", "applied"]
    with pytest.raises(Exception):
        build_states(repo, tmp_path / "w", s["c0"], edits_of(repo), SRC, None)   # already exists


def test_invariant_rejects_missing_blob_base(tmp_path):
    """A base whose blobs are absent in the clone must raise, not silently commit deletions."""
    import subprocess as sp
    from bth import replay
    src = tmp_path / "src"; src.mkdir()
    g = lambda *a, cwd=src: sp.run(["git", "-c", "core.autocrlf=false", *a], cwd=cwd, check=True, capture_output=True)
    g("init", "-q"); (src / "a.txt").write_text("a\n"); (src / "b.txt").write_text("b\n")
    g("add", "-A"); g("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base")
    base = sp.run(["git", "rev-parse", "HEAD"], cwd=src, capture_output=True, text=True).stdout.strip()
    wd = tmp_path / "wd"
    g("clone", "-q", "--no-hardlinks", str(src), str(wd), cwd=tmp_path)
    blob = sp.run(["git", "rev-parse", "HEAD:b.txt"], cwd=wd, capture_output=True, text=True).stdout.strip()
    (wd / ".git" / "objects" / blob[:2] / blob[2:]).unlink()   # simulate a blob the partial clone lacks
    with pytest.raises(RuntimeError, match="blobs missing"):
        replay._assert_complete_checkout(wd, base)
