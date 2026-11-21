from dataclasses import dataclass

import pytest

from bth.safety import Detection, Fault, simulate, summarise
from bth.select import (ChangedModule, Context, Full, Inc, Ours, Periodic, Testmon)

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


DEPS = {"t1": FS({"f1"}), "t2": FS({"f1"}), "t3": FS({"f3"}), "t4": FS({"f4"})}


def mkctx(n, **kw):
    base = dict(all_tests=sorted(DEPS), all_benches=["b1"], depmap_at=lambda t, k: DEPS[t],
                bench_profile_at=lambda b, k: FS({"f1"}), last_step=n,
                module_of_test={t: f"{t}.py" for t in DEPS}, module_of_bench={"b1": "b1.py"})
    base.update(kw)
    return Context(**base)


def steps(n, per=None):
    per = per or {}
    return [CS(functions=FS(per.get(i, {f"f{i}"})), files=FS({f"m{i}.py"})) for i in range(1, n + 1)]


def ours(**kw):
    kw.setdefault("trigger", ("score", 100))
    return lambda ctx: Ours(ctx, **kw)


def fault(**kw):
    d = dict(id="x", kind="mutant", step=1, extra_changed=FS(), kill_tests=FS({"t1"}))
    d.update(kw)
    return Fault(**d)


def test_caught_at_s_by_selection():
    n = 4
    r = simulate(ours(), steps(n), mkctx(n), fault(step=1))   # step 1 changes f1 -> t1 selected
    assert r == Detection(1, 0, "selection")


def test_caught_at_later_full_check():
    n = 5
    ctx = mkctx(n)
    # fault at step 2, kills t4 only (not selected: f4 never changed before the full check)
    f = fault(step=2, kill_tests=FS({"t4"}))
    r = simulate(lambda c: Periodic(Inc(c), 4), steps(n, {i: {"fz"} for i in range(1, 6)}), ctx, f)
    # Inc runs all tests every step -> selection at s
    assert r.by == "selection"
    r = simulate(lambda c: Periodic(ChangedModule(c), 4), steps(n), ctx, f)
    assert r == Detection(4, 2, "full_check")


def test_caught_at_final():
    n = 4
    f = fault(step=2, kill_tests=FS({"t4"}))
    r = simulate(ours(), steps(n), mkctx(n), f)   # t4 never selected; final full check at 4
    assert r == Detection(4, 2, "final")


def test_missed_without_final_check():
    n = 4
    f = fault(step=2, kill_tests=FS({"t4"}))
    ctx = mkctx(n, testmon_selection={1: FS(), 2: FS(), 3: FS(), 4: FS()})
    assert simulate(Testmon, steps(n), ctx, f) == Detection(None, None, "missed")
    assert simulate(ChangedModule, steps(n), ctx, f).by == "missed"


def test_full_arm_every_step():
    n = 3
    r = simulate(Full, steps(n), mkctx(n), fault(step=2, kill_tests=FS({"t4"})))
    assert r == Detection(2, 0, "full_check")


def test_latent_accumulating_vs_not():
    n = 4
    # fault enters at step 1 (f1 changed), only visible from step 3; t2 kills from then on
    f = fault(kind="latent", step=1, visible_from=3, kill_tests={3: FS({"t2"})})
    sts = steps(n)
    acc = simulate(ours(), sts, mkctx(n), f)
    assert acc == Detection(3, 2, "selection")          # f1 still accumulated at step 3
    noacc = simulate(ours(accumulate=False), sts, mkctx(n), f)
    assert noacc == Detection(4, 3, "final")            # only the last-step full check catches it


def test_full_check_before_visibility_is_green_and_resets():
    n = 6
    f = fault(kind="latent", step=1, visible_from=5, kill_tests={5: FS({"t2"})})
    # periodic full at 2 resets accumulation (green: fault invisible), so f1 is forgotten
    r = simulate(ours(trigger=("periodic", 2)), steps(n), mkctx(n), f)
    # step 4 is a periodic full check (visible only from 5), step 6 full again: caught there
    assert r == Detection(6, 5, "final")


def test_extra_changed_merged_at_step_s():
    n = 3
    f = fault(step=2, extra_changed=FS({"f3"}), kill_tests=FS({"t3"}))
    r = simulate(ours(), steps(n, {1: {"fa"}, 2: {"fb"}, 3: {"fc"}}), mkctx(n), f)
    assert r == Detection(2, 0, "selection")


def test_quarantined_never_count():
    n = 4
    f = fault(step=1, kill_tests=FS({"t1"}))
    r = simulate(ours(), steps(n), mkctx(n, quarantine=FS({"t1"})), f)
    assert r.by == "missed"
    r = simulate(Full, steps(n), mkctx(n, quarantine=FS({"t1"})), f)
    assert r.by == "missed"


def test_benchmark_regression_detection():
    n = 3
    f = fault(kind="slowdown", step=1, kill_tests=FS(), regress_benches=FS({"b1"}))
    assert simulate(ours(), steps(n), mkctx(n), f) == Detection(1, 0, "selection")
    # profile-less bench rule: changed module b1.py not touched -> final check catches it
    st = [CS(functions=FS({"f1"}), files=FS({"m1.py"}))] * n
    r = simulate(ours(profile=False), st, mkctx(n), f)
    assert r == Detection(3, 2, "final")


def test_dict_fault_accepted():
    n = 2
    r = simulate(ours(), steps(n), mkctx(n), {"id": "d", "kind": "mutant", "step": 1,
                                              "extra_changed": FS(), "kill_tests": FS({"t1"})})
    assert r.by == "selection"


def test_summarise():
    ds = [Detection(1, 0, "selection"), Detection(3, 2, "final"), Detection(None, None, "missed"),
          Detection(2, 4, "full_check")]
    s = summarise(ds)
    assert s["n"] == 4 and s["k_missed"] == 1
    assert s["by"] == {"selection": 1, "full_check": 1, "final": 1, "missed": 1}
    assert s["mean_delay"] == pytest.approx(2.0) and s["median_delay"] == 2
    lo, hi = s["wilson"]
    assert 0 <= lo < 0.25 < hi <= 1
    assert summarise([])["mean_delay"] is None
