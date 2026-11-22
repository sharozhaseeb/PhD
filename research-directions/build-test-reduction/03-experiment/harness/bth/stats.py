"""Statistical decision rules (readiness 4.2, 4.4, 5). Rule IDs: P2, P3, W3-new.

All functions are deterministic. asv rule = ratio threshold + Mann-Whitney U.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import median
from typing import Sequence

import numpy as np
try:  # scipy is preferred; a numpy fallback keeps the harness usable without it
    from scipy import stats as _st
except ImportError:  # pragma: no cover - exercised only when scipy is absent
    _st = None


@dataclass(frozen=True)
class Verdict:
    ratio: float
    p: float
    status: str  # "faster" | "slower" | "same"


def _ratio(ref: Sequence[float], new: Sequence[float]) -> float:
    mr, mn = float(median(ref)), float(median(new))
    if mr == 0.0:
        return 1.0 if mn == 0.0 else math.inf
    return mn / mr


def _mwu_fallback(x, y) -> float:
    """Two-sided Mann-Whitney U p-value, mirrors scipy method="auto": exact when both samples
    have <= 8 values and there are no ties, else normal approximation with tie and continuity
    correction."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    n1, n2 = len(x), len(y)
    allv = np.concatenate([x, y])
    ranks = _st_rank(allv)
    u1 = float(ranks[:n1].sum() - n1 * (n1 + 1) / 2)
    u = max(u1, n1 * n2 - u1)
    if max(n1, n2) <= 8 and len(set(allv.tolist())) == len(allv):
        # exact null distribution of U by DP over counts
        counts = [1]
        # number of ways: f(n1, n2, u) via recurrence on partitions
        from functools import lru_cache

        @lru_cache(None)
        def f(a, b, k):
            if k < 0:
                return 0
            if a == 0 or b == 0:
                return 1 if k == 0 else 0
            return f(a - 1, b, k - b) + f(a, b - 1, k)

        total = math.comb(n1 + n2, n1)
        tail = sum(f(n1, n2, k) for k in range(int(round(u)), n1 * n2 + 1))
        return min(1.0, 2.0 * tail / total)
    mu = n1 * n2 / 2.0
    _, tc = np.unique(allv, return_counts=True)
    n = n1 + n2
    s2 = n1 * n2 / 12.0 * ((n + 1) - (tc**3 - tc).sum() / (n * (n - 1)))
    if s2 <= 0:
        return 1.0
    z = (u - mu - 0.5) / math.sqrt(s2)
    return float(min(1.0, math.erfc(z / math.sqrt(2.0))))


def _st_rank(a):
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a))
    sa = a[order]
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and sa[j + 1] == sa[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return ranks


def _mwu_p(ref: Sequence[float], new: Sequence[float]) -> float:
    if _st is None:
        return _mwu_fallback(ref, new)
    try:
        p = float(_st.mannwhitneyu(ref, new, alternative="two-sided", method="auto").pvalue)
    except ValueError:  # e.g. all values identical
        return 1.0
    return 1.0 if math.isnan(p) else p


MWU_METHODS = ("scipy_auto", "exact", "asv")


def mwu_p(ref: Sequence[float], new: Sequence[float], method: str = "scipy_auto") -> float:
    """Two-sided Mann-Whitney U p-value.

    scipy_auto: the harness's original test (scipy method='auto': exact only if both n < 8 and no ties, else the
                normal approximation with tie and continuity corrections). Kept for continuity.
    exact:      scipy method='exact' at every size (PM 15:46, after W1's asv source check). Exact null distribution,
                which ignores ties (timing samples essentially never tie; ties are counted by `n_ties`).
    asv:        asv/_stats.py mann_whitney_u(method='auto') as read on GitHub main 2026-11-22: exact if
                max(m, n) <= 20, else normal z = (U - mn/2)/sqrt(mn(N+1)/12) with NO tie or continuity
                correction, two-sided. asv's conservative tie-break is not ported (ties flagged instead).
    """
    if method == "scipy_auto":
        return _mwu_p(ref, new)
    m, n = len(ref), len(new)
    if m == 0 or n == 0:
        return 1.0
    if method == "exact" or (method == "asv" and max(m, n) <= 20):
        if _st is None:  # pragma: no cover
            raise RuntimeError("scipy needed for the exact test")
        p = float(_st.mannwhitneyu(ref, new, alternative="two-sided", method="exact").pvalue)
        return 1.0 if math.isnan(p) else min(1.0, p)
    if method == "asv":
        a = np.asarray(ref, float); b = np.asarray(new, float)
        u = float((a[:, None] > b[None, :]).sum() + 0.5 * (a[:, None] == b[None, :]).sum())
        z = (u - m * n / 2) / math.sqrt(m * n * (m + n + 1) / 12)
        return min(1.0, math.erfc(abs(z) / math.sqrt(2)))
    raise ValueError(method)


def n_ties(ref: Sequence[float], new: Sequence[float]) -> int:
    a = np.asarray(ref, float); b = np.asarray(new, float)
    return int((a[:, None] == b[None, :]).sum())


def min_attainable_p(m: int, n: int, method: str = "exact") -> float:
    """Smallest two-sided p at U = 0: exact 2/C(m+n, m); asv-normal for max(m, n) > 20 under method='asv'."""
    if method == "asv" and max(m, n) > 20:
        return math.erfc((m * n / 2) / math.sqrt(m * n * (m + n + 1) / 12) / math.sqrt(2))
    if method == "scipy_auto":
        return _mwu_p([float(x) for x in range(m)], [float(x + m) for x in range(n)])
    return min(1.0, 2.0 / math.comb(m + n, m))


def asv_rule(ref: Sequence[float], new: Sequence[float], factor: float = 1.1,
             alpha: float = 0.002, method: str = "scipy_auto") -> Verdict:
    """asv `compare` default: ratio beyond `factor` AND two-sided MWU p < alpha (p from `mwu_p(method)`)."""
    r = _ratio(ref, new)
    p = mwu_p(ref, new, method)
    status = "same"
    if p < alpha:
        if r > factor:
            status = "slower"
        elif r < 1.0 / factor:
            status = "faster"
    return Verdict(r, p, status)


def _iqr_filter(x: Sequence[float]) -> list[float]:
    a = np.asarray(x, dtype=float)
    q1, q3 = np.percentile(a, [25, 75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return [float(v) for v in a if lo <= v <= hi]


def sweperf_rule(ref: Sequence[float], new: Sequence[float]) -> Verdict:
    """SWE-Perf rule: IQR outlier filter per side, MWU p < 0.1, |relative change| >= 5 %."""
    r_ref, r_new = _iqr_filter(ref), _iqr_filter(new)
    r = _ratio(r_ref, r_new)
    p = _mwu_p(r_ref, r_new)
    status = "same"
    if p < 0.1:
        if r >= 1.05:
            status = "slower"
        elif r <= 0.95:
            status = "faster"
    return Verdict(r, p, status)


def noise_sigma(pairs: Sequence[tuple[Sequence[float], Sequence[float]]]) -> float:
    """Sample std (ddof=1; 0.0 for < 2 pairs) of log(median ratio) over same-state pairs."""
    logs = [math.log(_ratio(a, b)) for a, b in pairs]
    if len(logs) < 2:
        return 0.0
    return float(np.std(logs, ddof=1))


def regressed(ref: Sequence[float], new: Sequence[float], sigma: float) -> bool:
    v = asv_rule(ref, new)
    return v.status == "slower" and v.ratio > 1.0 + 3.0 * sigma


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for k successes of n; (0,1) when n == 0."""
    if n <= 0:
        return (0.0, 1.0)
    ph = k / n
    z2 = z * z
    denom = 1.0 + z2 / n
    centre = (ph + z2 / (2 * n)) / denom
    half = z * math.sqrt(ph * (1 - ph) / n + z2 / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))
