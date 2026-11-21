import pytest

from bth.cost import cost_at_detection, estimate, matched_cost, session_cost
from bth.select import Decision

BS = {"clean": 100.0, "incremental": 10.0, "none": 0.0}


def test_estimate_sums():
    d = Decision("incremental", frozenset({"a", "b"}), frozenset({"x"}))
    r = estimate(d, {"a": 1.0, "b": 2.0, "c": 99.0}, {"x": 5.0}, BS, 0.5)
    assert r == {"build": 10.0, "tests": 3.0, "benches": 5.0, "overhead": 0.5, "total": 18.5}
    full = Decision("clean", frozenset(), frozenset(), True)
    assert estimate(full, {}, {}, BS, 0.0)["total"] == 100.0


def test_estimate_unknown_test_raises():
    with pytest.raises(KeyError):
        estimate(Decision("clean", frozenset({"z"}), frozenset()), {}, {}, BS, 0.0)


def test_session_cost():
    assert session_cost([1.0, 2.0, {"total": 3.0}]) == [1.0, 3.0, 6.0]
    assert session_cost([]) == []


FR = [(10.0, 0.2), (30.0, 0.6), (50.0, 1.0)]


def test_matched_cost_interpolates_and_clamps():
    assert matched_cost(FR, 20.0) == pytest.approx(0.4)
    assert matched_cost(FR, 30.0) == pytest.approx(0.6)
    assert matched_cost(FR, 5.0) == 0.2 and matched_cost(FR, 99.0) == 1.0


def test_cost_at_detection():
    assert cost_at_detection(FR, 0.4) == pytest.approx(20.0)
    assert cost_at_detection(FR, 1.0) == pytest.approx(50.0)
    assert cost_at_detection(FR, 0.1) == 10.0
    assert cost_at_detection(FR, 1.01) is None
    # unsorted / non-monotone input is normalised
    assert cost_at_detection([(50.0, 1.0), (10.0, 0.2), (30.0, 0.1)], 0.6) == pytest.approx(40.0)
