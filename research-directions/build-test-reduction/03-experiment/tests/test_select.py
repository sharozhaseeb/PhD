from dataclasses import dataclass

from bth.select import (ChangedModule, Context, Full, Inc, Ours, Outcome, Periodic,
                        StaticBench, Testmon)

FS = frozenset


@dataclass(frozen=True)
class CS:  # duck-typed ChangeSet
    functions: frozenset = FS()
    files: frozenset = FS()
    module_level_files: frozenset = FS()
    native_files: frozenset = FS()
    header_edits: frozenset = FS()
    build_config_changed: bool = False
    unmapped_native: frozenset = FS()


def ctx_from(deps, **kw):
    """deps: {test: frozenset}, the same at every observed step."""
    base = dict(all_tests=sorted(deps), all_benches=[],
                depmap_at=lambda test, k: deps.get(test), last_step=99)
    base.update(kw)
    return Context(**base)


# ---------- simple arms
def test_full_inc_testmon_changedmodule_staticbench():
    ctx = Context(all_tests=["t1", "t2"], all_benches=["b1", "b2"],
                  module_of_test={"t1": "a.py", "t2": "b.py"}, module_of_bench={"b1": "a.py", "b2": "b.py"},
                  static_reach={"b1": FS({"a.py::f"}), "b2": FS({"b.py::g"})},
                  module_functions={"a.py": FS({"a.py::f", "a.py::h"})},
                  testmon_selection={1: FS({"t2"})})
    ch = CS(functions=FS({"a.py::<module>"}), files=FS({"a.py"}))
    d = Full(ctx).decide(1, ch)
    assert d.build == "clean" and d.full_check and d.tests == FS({"t1", "t2"})
    d = Inc(ctx).decide(1, ch)
    assert d.build == "incremental" and not d.full_check and d.benches == FS({"b1", "b2"})
    assert Testmon(ctx).decide(1, ch).tests == FS({"t2"})
    d = ChangedModule(ctx).decide(1, ch)
    assert d.tests == FS({"t1"}) and d.benches == FS({"b1"})
    d = StaticBench(ctx).decide(1, ch)   # module-level expansion reaches a.py::f
    assert d.tests == FS({"t2"}) and d.benches == FS({"b1"})


# ---------- (1) hindsight rule
def test_hindsight_decide_uses_only_earlier_observations():
    calls = []

    def depmap_at(test, k):
        calls.append(k)
        return FS({"new"}) if k >= 3 else FS({"old"})   # a step-3 observation would differ

    ctx = Context(all_tests=["t1"], all_benches=[], depmap_at=depmap_at, last_step=99)
    arm = Ours(ctx, trigger=("score", 100))
    # t1 has only its baseline observation; at t=3 the edit touches "new"
    d = arm.decide(3, CS(functions=FS({"new"})))
    assert d.tests == FS()                      # chosen from the older map ("old"), not step 3's
    assert calls and all(k < 3 for k in calls)
    # control: had decide read the step-3 map, t1 would have been selected
    assert FS({"new"}) & depmap_at("t1", 3)
    # after the test is observed at step 3, a later decision legitimately sees that map
    arm.observe(3, Full(ctx).decide(3, CS()), Outcome(True))
    calls.clear()
    d4 = arm.decide(4, CS(functions=FS({"new"})))
    assert d4.tests == FS({"t1"}) and calls == [3]


def test_hindsight_unrun_tests_keep_old_observation_step():
    seen = []
    ctx = Context(all_tests=["t1"], all_benches=[],
                  depmap_at=lambda test, k: (seen.append(k), FS({"f"}))[1], last_step=99)
    arm = Ours(ctx, trigger=("score", 100))
    d = arm.decide(1, CS(functions=FS({"g"})))
    assert d.tests == FS()
    arm.observe(1, d, Outcome(True))            # t1 not run -> still observed at 0
    arm.decide(2, CS(functions=FS({"g"})))
    assert seen == [0, 0]


# ---------- (2) accumulation resets only after a GREEN full check
def mk_acc_ctx(**kw):
    deps = {"tf1": FS({"f1"}), "tf2": FS({"f2"}), "tf3": FS({"f3"})}
    return ctx_from(deps, **kw)


def test_accumulation_and_reset_only_on_green_full():
    ctx = mk_acc_ctx()
    arm = Ours(ctx, trigger=("score", 100))
    d1 = arm.decide(1, CS(functions=FS({"f1"})))
    arm.observe(1, d1, Outcome(True))
    d2 = arm.decide(2, CS(functions=FS({"f2"})))
    assert d2.tests == FS({"tf1", "tf2"})        # f1 still accumulated
    arm.observe(2, d2, Outcome(True))
    assert arm.st.acc == FS({"f1", "f2"})
    full = Full(ctx).decide(3, CS())
    arm.decide(3, CS())
    arm.observe(3, full, Outcome(False))         # red full check: no reset
    assert arm.st.acc == FS({"f1", "f2"})
    arm.decide(4, CS())
    arm.observe(4, full, Outcome(True))          # green full check: reset
    assert arm.st.acc == FS()
    d5 = arm.decide(5, CS(functions=FS({"f3"})))
    assert d5.tests == FS({"tf3"})


def test_no_accumulation_uses_current_only():
    arm = Ours(mk_acc_ctx(), accumulate=False, trigger=("score", 100))
    d1 = arm.decide(1, CS(functions=FS({"f1"})))
    arm.observe(1, d1, Outcome(True))
    d2 = arm.decide(2, CS(functions=FS({"f2"})))
    assert d2.tests == FS({"tf2"})


# ---------- (3) triggers
def test_score_trigger_at_T():
    funcs = [f"f{i}" for i in range(10)]
    deps = {f"t{i}": FS({f}) for i, f in enumerate(funcs)}
    arm = Ours(ctx_from(deps, last_step=50), trigger=("score", 10))
    fulls = []
    for t in range(1, 11):
        d = arm.decide(t, CS(functions=FS({funcs[t - 1]})))
        fulls.append(d.full_check)
        arm.observe(t, d, Outcome(True))
    assert fulls == [False] * 9 + [True]          # score reaches 10 at step 10
    assert arm.st.acc == FS()
    assert not arm.decide(11, CS(functions=FS({"f0"}))).full_check   # counter restarted


def test_last_step_always_full_for_ours_and_periodic():
    ctx = Context(all_tests=["t"], all_benches=["b"], depmap_at=lambda t, k: FS({"x"}),
                  bench_profile_at=lambda b, k: FS({"x"}), last_step=7)
    o = Ours(ctx, trigger=("score", 1000))
    assert o.decide(7, CS()).full_check and not o.decide(6, CS()).full_check
    o2 = Ours(ctx, trigger=("periodic", 5))
    assert o2.decide(5, CS()).full_check and o2.decide(7, CS()).full_check
    assert not o2.decide(6, CS()).full_check
    p = Periodic(Inc(ctx), 3)
    assert [p.decide(t, CS()).full_check for t in range(1, 8)] == [False, False, True, False, False, True, True]
    assert p.decide(3, CS()).build == "clean"
    pt = Periodic(Testmon(ctx), 4)
    assert pt.decide(7, CS()).full_check and not pt.decide(5, CS()).full_check


def test_periodic_inner_ours_resets_on_green_full():
    ctx = Context(all_tests=["t"], all_benches=[], depmap_at=lambda t, k: FS({"x"}), last_step=9)
    p = Periodic(Ours(ctx, trigger=("score", 1000)), 2)
    d = p.decide(1, CS(functions=FS({"a"})))
    p.observe(1, d, Outcome(True))
    d = p.decide(2, CS(functions=FS({"b"})))
    assert d.full_check
    p.observe(2, d, Outcome(True))
    assert p.inner.st.acc == FS()


def test_header_weight_in_score():
    ctx = Context(all_tests=["t"], all_benches=[], depmap_at=lambda t, k: FS({"x"}),
                  native_ext_funcs={"bn.reduce": FS()}, last_step=99)
    arm = Ours(ctx, trigger=("score", 10))
    d = arm.decide(1, CS(header_edits=FS({"bn.h"})))   # 5 per header
    assert not d.full_check
    arm.observe(1, d, Outcome(True))
    assert arm.decide(2, CS(header_edits=FS({"bn2.h"}))).full_check   # 2 headers = 10


# ---------- (4) F2 fallbacks
def test_f2_unknown_native_selects_ext_tests():
    deps = {"t_ext": FS({"native::bn.reduce.nanmax"}), "t_py": FS({"a.py::f"})}
    ctx = ctx_from(deps, native_ext_funcs={"bn.reduce": FS({"native::bn.reduce.nanmax",
                                                           "native::bn.reduce.nansum"})})
    d = Ours(ctx, trigger=("score", 100)).decide(1, CS(functions=FS({"native::bn.reduce.nansum"})))
    assert d.tests == FS({"t_ext"}) and not d.full_check
    assert "f2_fallback" in d.fallback_reasons


def test_f2_known_native_uses_normal_rule():
    deps = {"t_ext": FS({"native::bn.reduce.nanmax"}), "t_ns": FS({"native::bn.reduce.nansum"})}
    ctx = ctx_from(deps, native_ext_funcs={"bn.reduce": FS(set().union(*deps.values()))})
    d = Ours(ctx, trigger=("score", 100)).decide(1, CS(functions=FS({"native::bn.reduce.nansum"})))
    assert d.tests == FS({"t_ns"}) and "f2_fallback" not in d.fallback_reasons


def test_f2_unknown_extension_or_build_config_goes_full():
    deps = {"t1": FS({"a.py::f"}), "t2": FS()}
    ctx = ctx_from(deps, native_ext_funcs={"bn.reduce": FS()})
    d = Ours(ctx, trigger=("score", 100)).decide(1, CS(functions=FS({"native::other.mod.fn"})))
    assert d.full_check and d.tests == FS({"t1", "t2"}) and d.build == "clean"
    d = Ours(ctx, trigger=("score", 100)).decide(1, CS(build_config_changed=True))
    assert d.full_check and "build_config" in d.fallback_reasons


def test_header_edit_expands_to_ext_funcs():
    deps = {"t_ns": FS({"native::bn.reduce.nansum"}), "t_py": FS({"a.py::f"})}
    ctx = ctx_from(deps, native_ext_funcs={"bn.reduce": FS({"native::bn.reduce.nansum"})},
                   header_ext={"bn.h": FS({"bn.reduce"})})
    d = Ours(ctx, trigger=("score", 100)).decide(1, CS(header_edits=FS({"bn.h"})))
    assert d.tests == FS({"t_ns"})


# ---------- other rules
def test_f4_failed_and_changed_module_always_run_and_module_level_expansion():
    deps = {"t1": FS({"x"}), "t2": FS({"y"}), "t3": FS({"a.py::h"})}
    ctx = ctx_from(deps, module_of_test={"t2": "m.py"}, module_functions={"a.py": FS({"a.py::h"})})
    arm = Ours(ctx, trigger=("score", 100))
    d = arm.decide(1, CS(functions=FS({"a.py::<module>"}), files=FS({"m.py"})))
    assert d.tests == FS({"t2", "t3"})
    arm.observe(1, d, Outcome(False, FS({"t2", "t3"})))
    d = arm.decide(2, CS(functions=FS({"zzz"})))
    assert d.tests >= FS({"t2", "t3"}) and "t1" not in d.tests   # failed tests re-run (F4)


def test_quarantined_failures_do_not_drive_f4():
    ctx = ctx_from({"t1": FS({"x"})}, quarantine=FS({"t1"}))
    arm = Ours(ctx, trigger=("score", 100))
    d = arm.decide(1, CS(functions=FS({"q"})))
    arm.observe(1, d, Outcome(False, FS({"t1"})))
    assert arm.decide(2, CS(functions=FS({"zzz"}))).tests == FS()


def test_profile_vs_module_benches():
    ctx = Context(all_tests=[], all_benches=["b1", "b2"], depmap_at=lambda t, k: None,
                  bench_profile_at=lambda b, k: {"b1": FS({"f"}), "b2": FS({"g"})}[b],
                  module_of_bench={"b1": "m1.py", "b2": "m2.py"}, last_step=99)
    ch = CS(functions=FS({"f"}), files=FS({"m2.py"}))
    assert Ours(ctx, trigger=("score", 100)).decide(1, ch).benches == FS({"b1"})
    assert Ours(ctx, profile=False, trigger=("score", 100)).decide(1, ch).benches == FS({"b2"})


def test_f6_order_dependent_function_selects_all_tests():
    """W3-new F6-order: a changed function with order-dependent attribution selects every test."""
    deps = {"t1": FS({"m.py::lazy"}), "t2": FS({"m.py::g"}), "t3": FS({"n.py::h"})}
    ch = CS(functions=FS({"m.py::lazy"}), files=FS({"m.py"}))
    d = Ours(ctx_from(deps, order_dependent=FS({"m.py::lazy"}))).decide(1, ch)
    assert d.tests == FS({"t1", "t2", "t3"}) and not d.full_check and "f6_order_dependent" in d.fallback_reasons
    d = Ours(ctx_from(deps)).decide(1, ch)            # without the flag: normal function-level rule
    assert d.tests == FS({"t1"})


def test_f6_order_can_be_switched_off():
    deps = {"t1": FS({"m.py::lazy"}), "t2": FS({"m.py::g"})}
    ch = CS(functions=FS({"m.py::lazy"}), files=FS({"m.py"}))
    d = Ours(ctx_from(deps, order_dependent=FS({"m.py::lazy"})), f6order=False).decide(1, ch)
    assert d.tests == FS({"t1"})
