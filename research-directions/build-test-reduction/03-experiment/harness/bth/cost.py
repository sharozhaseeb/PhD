"""Estimated-seconds cost model and cost/detection frontier (readiness 3 RQ3, 5). Rule IDs: W3-new."""
from __future__ import annotations

from typing import Mapping, Sequence


def estimate(decision, test_secs: Mapping, bench_secs: Mapping,
             build_secs: Mapping, overhead_secs: float) -> dict:
    """Sum the four cost parts of one step. Unknown test/bench ids raise KeyError (no silent zeros)."""
    build = float(build_secs[decision.build])
    tests = float(sum(test_secs[t] for t in decision.tests))
    benches = float(sum(bench_secs[b] for b in decision.benches))
    overhead = float(overhead_secs)
    return {"build": build, "tests": tests, "benches": benches, "overhead": overhead,
            "total": build + tests + benches + overhead}


def session_cost(per_step: Sequence) -> list[float]:
    """Cumulative totals; each element is a number or an `estimate` dict."""
    out, acc = [], 0.0
    for s in per_step:
        acc += float(s["total"] if isinstance(s, Mapping) else s)
        out.append(acc)
    return out


def _pareto(frontier):
    pts = sorted((float(c), float(d)) for c, d in frontier)
    out, best = [], 0.0
    for c, d in pts:
        best = max(best, d)
        out.append((c, best))
    return out


def matched_cost(frontier: Sequence[tuple[float, float]], cost: float) -> float:
    """Detected fraction at `cost`, linear interpolation; clamped to the end points."""
    pts = _pareto(frontier)
    if cost <= pts[0][0]:
        return pts[0][1]
    if cost >= pts[-1][0]:
        return pts[-1][1]
    for (c0, d0), (c1, d1) in zip(pts, pts[1:]):
        if c0 <= cost <= c1:
            if c1 == c0:
                return d1
            return d0 + (d1 - d0) * (cost - c0) / (c1 - c0)
    return pts[-1][1]


def cost_at_detection(frontier: Sequence[tuple[float, float]], level: float):
    """Cheapest interpolated cost reaching `level`; None if the frontier never reaches it."""
    pts = _pareto(frontier)
    if pts[-1][1] < level:
        return None
    if pts[0][1] >= level:
        return pts[0][0]
    for (c0, d0), (c1, d1) in zip(pts, pts[1:]):
        if d0 < level <= d1:
            return c0 + (c1 - c0) * (level - d0) / (d1 - d0)
    return pts[-1][0]
