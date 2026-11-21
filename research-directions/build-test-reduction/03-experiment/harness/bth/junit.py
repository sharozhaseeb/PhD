"""pytest junitxml -> {nodeid: {"outcome", "duration"}} (oracle test results; W3-new).

junit stores ``classname`` = dotted module path (+ class names) and ``name`` = test function
with params; the original nodeid is rebuilt as ``<posix relpath>.py::<Class>::<name>``.
Resolution: with ``rootdir`` the dotted prefix is walked against the file system (dirs, then
``<seg>.py``; the remainder are classes).  Without it, a heuristic: the module is the first
segment named ``test_*``/``*_test``/``*_tests`` (else the last segment before the first
capitalised one).  Outcomes: passed | failed (failure or error) | skipped.  Several testcase
elements for one nodeid (setup error + teardown) are merged: durations sum, failed wins.
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

__all__ = ["parse", "nodeid_for"]

_MOD = re.compile(r"^(test_.*|.*_tests?)$")


def _split_classname(classname: str, rootdir):
    segs = classname.split(".") if classname else []
    if rootdir is not None:
        cur, parts = Path(rootdir), []
        for i, s in enumerate(segs):
            if (cur / (s + ".py")).is_file():
                return "/".join(parts + [s + ".py"]), segs[i + 1:]
            if (cur / s).is_dir():
                cur, parts = cur / s, parts + [s]
            else:
                break
    mod_i = next((i for i, s in enumerate(segs) if _MOD.match(s)), None)
    if mod_i is None:
        cap = next((i for i, s in enumerate(segs) if s[:1].isupper()), len(segs))
        mod_i = max(cap - 1, 0)
    return "/".join(segs[:mod_i + 1]) + ".py", segs[mod_i + 1:]


def nodeid_for(classname: str, name: str, rootdir=None) -> str:
    path, classes = _split_classname(classname, rootdir)
    return "::".join([path, *classes, name])


def parse(junit_xml, rootdir=None) -> dict:
    """`junit_xml`: path to a junit file or the XML text itself."""
    s = str(junit_xml)
    root = ET.fromstring(s) if s.lstrip().startswith("<") else ET.parse(s).getroot()
    out: dict = {}
    for tc in root.iter("testcase"):
        nid = nodeid_for(tc.get("classname", ""), tc.get("name", ""), rootdir)
        if tc.find("failure") is not None or tc.find("error") is not None:
            outcome = "failed"
        elif tc.find("skipped") is not None:
            outcome = "skipped"
        else:
            outcome = "passed"
        dur = float(tc.get("time") or 0.0)
        prev = out.get(nid)
        if prev is None:
            out[nid] = {"outcome": outcome, "duration": dur}
        else:
            prev["duration"] += dur
            if outcome == "failed" or (outcome == "skipped" and prev["outcome"] == "passed"):
                prev["outcome"] = outcome if prev["outcome"] != "failed" else "failed"
    return dict(sorted(out.items()))
