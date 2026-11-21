"""Replay mined edits onto a base state in a separate clone (readiness.md section 2; W3-new).

The source repo is only read (clone + `git diff`). All mutating git commands run
inside `workdir`. State SHAs are reproducible: fixed identity, original commit date.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Callable

BRANCH = "bth-replay"
_BASE_ENV = {
    "GIT_AUTHOR_NAME": "bth", "GIT_AUTHOR_EMAIL": "bth@example.invalid",
    "GIT_COMMITTER_NAME": "bth", "GIT_COMMITTER_EMAIL": "bth@example.invalid",
}
_CFG = ["-c", "core.autocrlf=false", "-c", "core.safecrlf=false", "-c", "commit.gpgsign=false",
        "-c", "core.quotepath=false", "-c", "core.longpaths=true"]


def _run(cwd, *args, env=None, inp=None, check=True):
    e = {**os.environ, **(env or {})}
    r = subprocess.run(["git", *_CFG, *args], cwd=str(cwd), env=e, input=inp,
                       capture_output=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {cwd}: "
                           f"{r.stderr.decode('utf-8', 'replace').strip()}")
    return r


def _restore(workdir):
    """Discard any partial/conflicted state. Runs inside workdir only."""
    _run(workdir, "reset", "-q", "--hard", "HEAD")
    _run(workdir, "clean", "-fdq")


def _assert_complete_checkout(workdir, base_sha):
    """Invariant: every blob of the base tree is present and the checkout is clean.

    Guards against partial (blobless) source clones: a local clone of such a repo
    may lack blobs, the checkout then silently misses files, and `add -A` would
    commit them as deletions (found 2026-11-21 on networkx; 124 files)."""
    tree = _run(workdir, "ls-tree", "-r", base_sha).stdout.decode().splitlines()
    blobs = [ln.split()[2] for ln in tree if ln.split()[1] == "blob"]
    chk = _run(workdir, "cat-file", "--batch-check", inp=("\n".join(blobs) + "\n").encode())
    missing = [ln for ln in chk.stdout.decode().splitlines() if ln.endswith(" missing")]
    if missing:
        raise RuntimeError(f"base {base_sha}: {len(missing)} blobs missing in the replay clone "
                           f"(partial source clone?) e.g. {missing[:3]}")
    dirty = _run(workdir, "status", "--porcelain").stdout.decode().strip()
    if dirty:
        raise RuntimeError(f"base checkout not clean: {dirty.splitlines()[:5]}")


def build_states(repo, workdir, base_sha: str, edits, src_pathspec,
                 check: Callable[[Path], tuple] | None = None) -> list:
    """Replay `edits` (dicts with `sha`[, `date`] or bare shas) onto `base_sha`.

    Returns one record per edit: orig_sha, status ("applied"/"dropped"), state_sha
    (None when dropped), reason. Step labels in commit messages are the 0-based
    position of the edit in `edits`."""
    repo, workdir = Path(repo), Path(workdir)
    if workdir.exists() and any(workdir.iterdir()):
        raise FileExistsError(f"workdir not empty: {workdir}")
    workdir.parent.mkdir(parents=True, exist_ok=True)
    pathspec = [src_pathspec] if isinstance(src_pathspec, str) else list(src_pathspec)

    # separate clone; the source repo is only read
    _run(workdir.parent, "clone", "-q", "--no-checkout", "--no-hardlinks",
         str(repo), str(workdir))
    _run(workdir, "checkout", "-q", "-B", BRANCH, base_sha)
    _assert_complete_checkout(workdir, base_sha)

    records = []
    for i, edit in enumerate(edits):
        sha = edit if isinstance(edit, str) else edit["sha"]
        date = None if isinstance(edit, str) else edit.get("date")
        if not date:
            date = _run(workdir, "show", "-s", "--format=%aI", sha).stdout.decode().strip()
        rec = {"orig_sha": sha, "status": "dropped", "state_sha": None, "reason": ""}
        records.append(rec)

        diff = _run(workdir, "diff", "--binary", "--no-color", "--no-renames",
                    f"{sha}^", sha, "--", *pathspec).stdout
        if not diff:
            rec["reason"] = "dropped: empty diff"
            continue
        applied = _run(workdir, "apply", "--3way", "--index", "--whitespace=nowarn", "-",
                       inp=diff, check=False)
        if applied.returncode != 0:
            _restore(workdir)
            rec["reason"] = "dropped: conflict"
            continue
        if check is not None:
            try:
                ok, msg = check(workdir)
            except Exception as exc:          # a crashing check is a failed check
                ok, msg = False, f"{type(exc).__name__}: {exc}"
            if not ok:
                _restore(workdir)
                rec["reason"] = f"dropped: check failed: {msg}"
                continue
        _run(workdir, "add", "-A")
        if _run(workdir, "diff", "--cached", "--quiet", check=False).returncode == 0:
            _restore(workdir)
            rec["reason"] = "dropped: no-op"
            continue
        # invariant: a step may only touch paths that its own edit's source diff touches
        edit_paths = set(_run(workdir, "diff", "--name-only", "--no-renames", f"{sha}^", sha,
                              "--", *pathspec).stdout.decode().split("\n")) - {""}
        staged = set(_run(workdir, "diff", "--cached", "--name-only", "--no-renames")
                     .stdout.decode().split("\n")) - {""}
        if not staged <= edit_paths:
            raise RuntimeError(f"replay invariant violated at step {i} ({sha}): staged paths outside "
                               f"the edit: {sorted(staged - edit_paths)[:10]}")
        env = {**_BASE_ENV, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
        _run(workdir, "commit", "-q", "-m", f"bth step {i}: {sha}", env=env)
        rec["status"] = "applied"
        rec["state_sha"] = _run(workdir, "rev-parse", "HEAD").stdout.decode().strip()
    return records
