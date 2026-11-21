"""pytest plugin: per-test function dependency map (rules F1*, F3, W3-new).

Load with ``-p bth.depmap_plugin --bth-depmap-out PATH --bth-root ROOT
[--bth-native-prefix PFX ...]``.  Writes ``PATH`` = ``{nodeid: sorted FuncIDs}``
and ``PATH.outcomes.json`` = ``{nodeid: {"outcome", "duration"}}`` at session
end.  Under pytest-xdist each worker (env ``PYTEST_XDIST_WORKER``, e.g. ``gw0``) writes
``PATH.<worker_id>`` and ``PATH.<worker_id>.outcomes.json`` instead; the orchestrator merges
them.  Nothing is written per test; data stays in memory.  Without
``--bth-depmap-out`` the plugin is inert.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from bth.monitor import Recorder


def pytest_addoption(parser):
    g = parser.getgroup("bth")
    g.addoption("--bth-depmap-out", default=None, help="write per-test dependency map JSON here")
    g.addoption("--bth-root", default=None, help="source root for FuncIDs (default: rootdir)")
    g.addoption("--bth-native-prefix", action="append", default=[], help="native module prefix (repeatable)")


def pytest_configure(config):
    out = config.getoption("--bth-depmap-out")
    if not out:
        return
    root = config.getoption("--bth-root") or str(config.rootpath)
    worker = os.environ.get("PYTEST_XDIST_WORKER")
    config._bth = {
        "out": Path(out + "." + worker if worker else out),
        "rec": Recorder(Path(root), tuple(config.getoption("--bth-native-prefix"))),
        "deps": {},
        "outcomes": {},
    }


def pytest_sessionstart(session):
    st = getattr(session.config, "_bth", None)
    if st:
        st["rec"].start()


@pytest.hookimpl(wrapper=True)
def pytest_runtest_protocol(item, nextitem):
    st = getattr(item.config, "_bth", None)
    if not st:
        return (yield)
    rec = st["rec"]
    rec.reset()
    try:
        return (yield)
    finally:
        st["deps"][item.nodeid] = rec.snapshot()


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield
    st = getattr(item.config, "_bth", None)
    if st:
        o = st["outcomes"].setdefault(item.nodeid, {"outcome": "passed", "duration": 0.0})
        o["duration"] += float(report.duration)
        if report.outcome == "failed":
            o["outcome"] = "failed"
        elif report.outcome == "skipped" and o["outcome"] != "failed" and (
            report.when == "setup" or o["outcome"] == "passed"
        ):
            o["outcome"] = "skipped"
    return report


def pytest_sessionfinish(session, exitstatus):
    st = getattr(session.config, "_bth", None)
    if not st:
        return
    st["rec"].stop()
    out: Path = st["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({k: sorted(v) for k, v in sorted(st["deps"].items())}, indent=0), encoding="utf-8")
    Path(str(out) + ".outcomes.json").write_text(
        json.dumps(dict(sorted(st["outcomes"].items())), indent=0), encoding="utf-8"
    )
    session.config._bth = None


def pytest_unconfigure(config):
    st = getattr(config, "_bth", None)
    if st:
        st["rec"].stop()  # safety net: never leak the monitoring tool id
        config._bth = None
