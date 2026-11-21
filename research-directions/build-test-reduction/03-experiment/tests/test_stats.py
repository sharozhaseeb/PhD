import math

import numpy as np
import pytest

from bth.stats import asv_rule, noise_sigma, regressed, sweperf_rule, wilson


def _samples(seed, mean, n=30, sd=0.02):
    rng = np.random.default_rng(seed)
    return list(rng.normal(mean, sd, n))


def test_asv_same_distribution():
    assert asv_rule(_samples(1, 1.0), _samples(2, 1.0)).status == "same"


def test_asv_2x_slower_and_faster():
    v = asv_rule(_samples(1, 1.0), _samples(2, 2.0))
    assert v.status == "slower" and v.ratio > 1.9 and v.p < 0.002
    assert asv_rule(_samples(2, 2.0), _samples(1, 1.0)).status == "faster"


def test_asv_small_change_is_same():
    # 1.05x is significant statistically (tiny noise) but under the 1.1 factor
    v = asv_rule(_samples(1, 1.0, sd=0.005), _samples(2, 1.05, sd=0.005))
    assert v.p < 0.002 and v.status == "same"


def test_asv_identical_constant_samples():
    assert asv_rule([1.0] * 10, [1.0] * 10).status == "same"


def test_sweperf_basic():
    assert sweperf_rule(_samples(1, 1.0), _samples(2, 1.0)).status == "same"
    assert sweperf_rule(_samples(1, 1.0), _samples(2, 1.3)).status == "slower"
    assert sweperf_rule(_samples(1, 1.3), _samples(2, 1.0)).status == "faster"
    # 5 % rule: 2 % shift significant but too small
    assert sweperf_rule(_samples(1, 1.0, sd=0.003), _samples(2, 1.02, sd=0.003)).status == "same"


def test_sweperf_drops_outliers():
    ref = _samples(1, 1.0)
    new = _samples(2, 1.0) + [50.0]
    assert sweperf_rule(ref, new).status == "same"


def _wilson_ref(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def test_wilson_known_values():
    lo, hi = wilson(0, 25)
    assert lo == 0.0 and hi == pytest.approx(1.96**2 / (25 + 1.96**2))
    assert hi == pytest.approx(0.1332, abs=1e-3)
    lo, hi = wilson(3, 25)
    rlo, rhi = _wilson_ref(3, 25)
    assert (lo, hi) == (pytest.approx(rlo), pytest.approx(rhi))
    assert (lo, hi) == (pytest.approx(0.0416, abs=1e-3), pytest.approx(0.3000, abs=1e-3))
    assert wilson(0, 0) == (0.0, 1.0)


def test_noise_sigma_and_regressed():
    pairs = [([1.0, 1.0, 1.0], [1.0, 1.0, 1.0]), ([1.0, 1.0, 1.0], [1.1, 1.1, 1.1]),
             ([1.0, 1.0, 1.0], [0.9, 0.9, 0.9])]
    logs = [0.0, math.log(1.1), math.log(0.9)]
    assert noise_sigma(pairs) == pytest.approx(float(np.std(logs, ddof=1)))
    assert noise_sigma(pairs[:1]) == 0.0
    ref, new = _samples(1, 1.0), _samples(2, 1.3)
    assert regressed(ref, new, sigma=0.02)
    assert not regressed(ref, new, sigma=0.15)   # 1 + 3*0.15 = 1.45 > 1.3
    assert not regressed(ref, _samples(3, 1.0), sigma=0.0)
