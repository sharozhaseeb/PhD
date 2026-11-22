"""C5 batching comparators (PM 2026-11-22 06:27): cap-only and additive-budget, with no per-edit check."""
from dataclasses import dataclass

from bth import orchestrate as O
from bth.safety import Fault, simulate
from bth.select import Batch, Context, Outcome

FS = frozenset


@dataclass(frozen=True)
class CS:
    functions: frozenset = FS()
    files: frozenset = FS()
    module_level_files: frozenset = FS()
    native_files: frozenset = FS()
    header_edits: frozenset = FS()
    build_config_changed: bool = False
    unmapped_native: frozenset = FS()


def ctx(last=10):
    deps = {"t1": FS({"a"}), "t2": FS({"b"})}
    return Context(all_tests=sorted(deps), all_benches=["b1"], depmap_at=lambda t, k: deps.get(t),
                   bench_profile_at=lambda b, k: FS({"a"}), last_step=last)


def run(arm, steps):
    st, out = arm.new_state(), []
    for t, ch in enumerate(steps, start=1):
        d = arm.decide(t, ch, st)
        out.append(d)
        arm.observe(t, d, Outcome(True), st)
    return out


def test_cap_only_full_every_k_and_nothing_between():
    c = ctx(last=7)
    ds = run(Batch(c, cap=3), [CS(functions=FS({"a"}))] * 7)
    assert [d.full_check for d in ds] == [False, False, True, False, False, True, True]
    for d in ds:
        if not d.full_check:   # no per-edit tier: nothing runs, no build
            assert d.tests == FS() and d.benches == FS() and d.build == "none"
            assert "batch_wait" in d.fallback_reasons


def test_cap_counts_from_last_full_check_not_step_number():
    c = ctx(last=20)
    # budget fires at step 2 (score 2 funcs >= 2); cap 3 then counts from step 2
    steps = [CS(functions=FS({"a"})), CS(functions=FS({"b"}))] + [CS()] * 6
    ds = run(Batch(c, budget=2, cap=3), steps)
    full = [t for t, d in enumerate(ds, start=1) if d.full_check]
    assert full[:3] == [2, 5, 8]


def test_additive_budget_uses_ours_score_and_resets_after_green_full():
    c = ctx(last=99)
    steps = [CS(functions=FS({"a"}))] * 3 + [CS(functions=FS({"b"}))] + [CS(functions=FS({"a"}))]
    ds = run(Batch(c, budget=2), steps)
    # |A_t|: {a}=1, {a}=1, {a}=1, {a,b}=2 -> full at 4; reset; {a}=1
    assert [d.full_check for d in ds] == [False, False, False, True, False]
    assert "score" in ds[3].fallback_reasons


def test_header_edit_weight_counts_in_budget():
    c = ctx(last=99)
    ds = run(Batch(c, budget=5), [CS(header_edits=FS({"x.h"}))])
    assert ds[0].full_check   # 0 funcs + 5 * 1 header >= 5


def test_final_step_always_full():
    c = ctx(last=2)
    ds = run(Batch(c, budget=1000), [CS(), CS()])
    assert [d.full_check for d in ds] == [False, True]
    assert "final" in ds[1].fallback_reasons


def test_fault_found_only_at_next_full_check():
    c = ctx(last=6)
    steps = [CS(functions=FS({"a"}))] * 6
    f = Fault(id="m", kind="mutant", step=2, kill_tests=FS({"t1"}))
    det = simulate(lambda cx: Batch(cx, cap=3), steps, c, f)
    assert det.step == 3 and det.delay == 1 and det.by == "full_check"


def test_parse_arm_batch_specs():
    _, fac = O.parse_arm("BATCH:cap=5")
    a = fac(ctx())
    assert isinstance(a, Batch) and a.cap == 5 and a.budget is None
    _, fac = O.parse_arm("BATCH:budget=10,cap=8")
    a = fac(ctx())
    assert a.budget == 10 and a.cap == 8
