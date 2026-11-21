"""Fault-injection replay (readiness 4.1, 4.1b, 4.2, 4.4). Rule IDs: F1-F5, C1, C3, W3-new.

Step numbering matches select.py: steps[i] is step t = i + 1; the last step is n = len(steps).
Kill/regress sets are either a frozenset (constant from `visible_from` on) or a dict
{step: set}, in which case the value at step u is that of the latest key <= u.
"""
from __future__ import annotations

import dataclasses
import statistics
from dataclasses import dataclass
from typing import Mapping, Optional

from bth.select import Ours, Outcome, Periodic  # noqa: F401
from bth.stats import wilson


@dataclass(frozen=True)
class Fault:
    id: str
    kind: str                      # mutant | latent | caller | slowdown
    step: int                      # s: step at which the fault enters the code
    visible_from: Optional[int] = None   # v (= s unless latent)
    extra_changed: frozenset = frozenset()
    kill_tests: object = frozenset()
    regress_benches: object = frozenset()

    @property
    def v(self) -> int:
        return self.step if self.visible_from is None else self.visible_from

    @staticmethod
    def from_dict(d: Mapping) -> "Fault":
        return Fault(**{k: d[k] for k in d if k in {f.name for f in dataclasses.fields(Fault)}})


@dataclass(frozen=True)
class Detection:
    step: Optional[int]
    delay: Optional[int]
    by: str                        # selection | full_check | final | missed


def _at(spec, u):
    if isinstance(spec, Mapping):
        ks = [k for k in spec if k <= u]
        return frozenset(spec[max(ks)]) if ks else frozenset()
    return frozenset(spec)


def simulate(arm_factory, steps, ctx, fault) -> Detection:
    if isinstance(fault, Mapping):
        fault = Fault.from_dict(fault)
    arm = arm_factory(ctx)
    st = arm.new_state()
    n = len(steps)
    quar = frozenset(ctx.quarantine)
    for t in range(1, n + 1):
        ch = steps[t - 1]
        if t == fault.step and fault.extra_changed:
            ch = dataclasses.replace(ch, functions=frozenset(ch.functions) | frozenset(fault.extra_changed))
        d = arm.decide(t, ch, st)
        if t >= fault.v:
            kill = _at(fault.kill_tests, t) - quar
            reg = _at(fault.regress_benches, t)
            if d.full_check:
                if kill or reg:
                    return Detection(t, t - fault.step, "final" if t == n else "full_check")
            elif (d.tests & kill) or (d.benches & reg):
                return Detection(t, t - fault.step, "selection")
        arm.observe(t, d, Outcome(green=True), st)  # undetected so far: the check is green
    return Detection(None, None, "missed")


def summarise(detections) -> dict:
    ds = list(detections)
    n = len(ds)
    k = sum(1 for d in ds if d.by == "missed")
    delays = [d.delay for d in ds if d.delay is not None]
    by = {key: 0 for key in ("selection", "full_check", "final", "missed")}
    for d in ds:
        by[d.by] += 1
    return {"k_missed": k, "n": n, "wilson": wilson(k, n),
            "mean_delay": statistics.fmean(delays) if delays else None,
            "median_delay": statistics.median(delays) if delays else None,
            "by": by}
