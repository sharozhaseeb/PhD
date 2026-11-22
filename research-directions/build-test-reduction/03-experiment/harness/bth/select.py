"""Selection arms (readiness 3). Rule IDs: B1, B2, F1, F2, F3, F4, F5, P1, C1, C3, W3-new.

Pure functions over data, no I/O. Step numbering: S_0 is the baseline (fully observed),
steps are t = 1..ctx.last_step.

Observation model / hindsight rule: `ctx.depmap_at(test, k)` is the recorded dependency set of
`test` when it was run at state S_k. An arm only ever asks for k = `st.observed[test]` (default 0),
the last step < t at which *this arm* ran the test. `decide` at step t therefore never reads
step-t observations; `observe(t, ...)` records what the decision actually ran.

State: each arm owns a default `ArmState` (`arm.st`); `decide(t, changes, st=None)` and
`observe(t, decision, outcome, st=None)` use it unless an explicit state is passed.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:  # pragma: no cover
    from bth.changed_fns import ChangeSet  # noqa: F401

MODULE_SUFFIX = "::<module>"


@dataclass
class Context:
    all_tests: list
    all_benches: list
    depmap_at: Callable = lambda test, k: None        # (test, observed_step) -> frozenset|None
    bench_profile_at: Callable = lambda bench, k: None
    static_reach: dict = field(default_factory=dict)
    module_of_test: dict = field(default_factory=dict)
    module_of_bench: dict = field(default_factory=dict)
    module_functions: dict = field(default_factory=dict)
    native_ext_funcs: dict = field(default_factory=dict)
    quarantine: frozenset = frozenset()
    testmon_selection: Optional[dict] = None
    last_step: Optional[int] = None                   # n; the C3 final check happens here
    header_ext: dict = field(default_factory=dict)    # header file -> extensions (optional)
    # W3-new "F6-order": functions whose test attribution differed between two same-state depmap runs
    # (first-call / lazy-import code). A change to one selects ALL tests (like F6 import-time code).
    order_dependent: frozenset = frozenset()


@dataclass(frozen=True)
class Decision:
    build: str
    tests: frozenset
    benches: frozenset
    full_check: bool = False
    fallback_reasons: tuple = ()


@dataclass(frozen=True)
class Outcome:
    green: bool
    failed_tests: frozenset = frozenset()


@dataclass
class ArmState:
    observed: dict = field(default_factory=dict)    # test -> last step it was run
    bobserved: dict = field(default_factory=dict)   # bench -> last step it was run
    failed: set = field(default_factory=set)        # F4: tests failing at their last run
    acc: frozenset = frozenset()                    # accumulated changed funcs since green full
    headers: frozenset = frozenset()
    fallbacks: frozenset = frozenset()
    pending: Optional[tuple] = None                 # (acc, headers, fallbacks) of the open decision


def expand_module_level(funcs, module_functions) -> frozenset:
    out = set()
    for f in funcs:
        out.add(f)
        if f.endswith(MODULE_SUFFIX):
            out |= set(module_functions.get(f[: -len(MODULE_SUFFIX)], ()))
    return frozenset(out)


def _full(ctx: Context, reasons=()) -> Decision:
    return Decision("clean", frozenset(ctx.all_tests), frozenset(ctx.all_benches), True, tuple(reasons))


class Arm:
    name = "arm"

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.st = ArmState()

    def new_state(self) -> ArmState:
        return ArmState()

    def observe(self, t, decision, outcome, st=None) -> None:
        return None

    def _testmon(self, t):
        sel = self.ctx.testmon_selection
        if sel is None:
            return frozenset(self.ctx.all_tests)
        return frozenset(sel.get(t, frozenset()))

    def _module_benches(self, changes):
        mob = self.ctx.module_of_bench
        return frozenset(b for b in self.ctx.all_benches if mob.get(b) in changes.files)


class Full(Arm):
    name = "FULL"

    def decide(self, t, changes, st=None):
        return _full(self.ctx, ("every_step",))


class Inc(Arm):
    name = "INC"

    def decide(self, t, changes, st=None):
        return Decision("incremental", frozenset(self.ctx.all_tests), frozenset(self.ctx.all_benches))


class Testmon(Arm):
    __test__ = False  # not a pytest class
    name = "TESTMON"

    def decide(self, t, changes, st=None):
        return Decision("incremental", self._testmon(t), frozenset(self.ctx.all_benches))


class ChangedModule(Arm):
    name = "CHANGED_MODULE"

    def decide(self, t, changes, st=None):
        mot = self.ctx.module_of_test
        tests = frozenset(x for x in self.ctx.all_tests if mot.get(x) in changes.files)
        return Decision("incremental", tests, self._module_benches(changes))


class StaticBench(Arm):
    name = "STATIC_BENCH"

    def decide(self, t, changes, st=None):
        cur = expand_module_level(changes.functions, self.ctx.module_functions)
        benches = frozenset(b for b in self.ctx.all_benches
                            if self.ctx.static_reach.get(b, frozenset()) & cur)
        return Decision("incremental", self._testmon(t), benches)


class Periodic(Arm):
    """Wrapper adding a full check every k steps and at the last step (C1, C3)."""

    def __init__(self, inner: Arm, k: int):
        super().__init__(inner.ctx)
        self.inner, self.k = inner, k
        self.name = f"{inner.name}+k{k}"
        self.st = inner.st

    def new_state(self):
        return self.inner.new_state()

    def decide(self, t, changes, st=None):
        d = self.inner.decide(t, changes, st)
        reasons = []
        if t % self.k == 0:
            reasons.append("periodic")
        if self.ctx.last_step is not None and t == self.ctx.last_step:
            reasons.append("final")
        if reasons and not d.full_check:
            return _full(self.ctx, d.fallback_reasons + tuple(reasons))
        return d

    def observe(self, t, decision, outcome, st=None):
        self.inner.observe(t, decision, outcome, st)


class Batch(Arm):
    """C5 batching comparators (W1 candidate-rules C5; R2 notes): NO per-edit check.

    Between full checks nothing runs and nothing is built (build "none"); edits accumulate as a batch.
    A full check (the batch flush) happens when
      - cap:    steps since the last full check >= cap  (FSB / TWB-like cap; cap-only when budget is None), or
      - budget: OURS' additive score (|A_t| + w_header*headers + w_fallback*fallbacks) >= budget
                (risk-mass "-la" batching with the learned r_i replaced by our measured score), or
      - the last step, or OURS' mandatory triggers (build-config edit, unknown native extension).
    The score bookkeeping is delegated to an inner OURS arm so both use identical accumulation.
    """

    def __init__(self, ctx: Context, budget=None, cap=None, w_header=5, w_fallback=5):
        super().__init__(ctx)
        if budget is None and cap is None:
            raise ValueError("Batch needs budget and/or cap")
        self.budget, self.cap = budget, cap
        self.name = "BATCH" + (f":budget={budget}" if budget is not None else "") + (f":cap={cap}" if cap is not None else "")
        trig = ("score", budget) if budget is not None else ("none", 0)
        self.inner = Ours(ctx, trigger=trig, w_header=w_header, w_fallback=w_fallback)

    def new_state(self):
        st = self.inner.new_state()
        st.last_full = 0
        return st

    def decide(self, t, changes, st=None):
        st = st if st is not None else self.st
        d = self.inner.decide(t, changes, st)
        reasons = list(d.fallback_reasons) if d.full_check else []
        if self.cap is not None and t - getattr(st, "last_full", 0) >= self.cap:
            reasons.append("cap")
        if d.full_check or "cap" in reasons:
            return _full(self.ctx, tuple(reasons))
        return Decision("none", frozenset(), frozenset(), False, ("batch_wait",))

    def observe(self, t, decision, outcome, st=None):
        st = st if st is not None else self.st
        if decision.full_check:
            st.last_full = t
        self.inner.observe(t, decision, outcome, st)


class Ours(Arm):
    name = "OURS"

    def __init__(self, ctx: Context, accumulate=True, profile=True, trigger=("score", 10),
                 w_header=5, w_fallback=5, f6order=True):
        super().__init__(ctx)
        self.accumulate, self.profile, self.trigger = accumulate, profile, trigger
        self.f6order = f6order   # W3-new F6-order on/off (reported both ways)
        self.w_header, self.w_fallback = w_header, w_fallback

    def _all_native(self):
        out = set()
        for v in self.ctx.native_ext_funcs.values():
            out |= set(v)
        return out

    def _header_funcs(self, changes):
        out, unmapped = set(), set()
        for h in changes.header_edits:
            exts = self.ctx.header_ext.get(h)
            if exts is None:
                out |= self._all_native()
            else:
                for e in exts:
                    out |= set(self.ctx.native_ext_funcs.get(e, ()))
        for name in changes.unmapped_native:
            out |= self._all_native()
            unmapped.add("unmapped:" + name)
        return out, unmapped

    @staticmethod
    def _ext_of(func):  # "native::ext.mod.name" -> "ext.mod"
        return func[len("native::"):].rsplit(".", 1)[0]

    def _dep(self, t, test, st):
        k = st.observed.get(test, 0)
        assert k < t, "hindsight violation"
        return self.ctx.depmap_at(test, k)

    def _prof(self, t, bench, st):
        k = st.bobserved.get(bench, 0)
        assert k < t, "hindsight violation"
        return self.ctx.bench_profile_at(bench, k)

    def decide(self, t, changes, st=None):
        st = st if st is not None else self.st
        ctx = self.ctx
        reasons = []
        cur = set(expand_module_level(changes.functions, ctx.module_functions))
        hdr_funcs, unmapped = self._header_funcs(changes)
        cur |= hdr_funcs
        deps = {x: self._dep(t, x, st) for x in ctx.all_tests}

        # F2: changed native funcs that appear in no observed depmap
        known = set()
        for d in deps.values():
            if d:
                known |= d
        cur_fb = {f for f in cur if f.startswith("native::") and f not in known and f not in hdr_funcs}
        unknown_ext = any(self._ext_of(f) not in ctx.native_ext_funcs for f in cur_fb)
        if changes.build_config_changed:
            cur_fb.add("build_config")
        cur_fb |= unmapped

        acc = st.acc | cur
        hdrs = st.headers | set(changes.header_edits)
        fbs = st.fallbacks | cur_fb
        sel = acc if self.accumulate else frozenset(cur)
        fb_for_sel = fbs if self.accumulate else frozenset(cur_fb)
        score = len(acc) + self.w_header * len(hdrs) + self.w_fallback * len(fbs)

        full = False
        if changes.build_config_changed:
            full = True
            reasons.append("build_config")
        if unknown_ext:
            full = True
            reasons.append("f2_unknown_ext")
        kind, val = self.trigger
        if kind == "score" and score >= val:
            full = True
            reasons.append("score")
        if kind == "periodic" and t % val == 0:
            full = True
            reasons.append("periodic")
        if ctx.last_step is not None and t == ctx.last_step:
            full = True
            reasons.append("final")
        if any(f.startswith("native::") for f in cur_fb):
            reasons.append("f2_fallback")

        st.pending = (frozenset(acc), frozenset(hdrs), frozenset(fbs))
        if full:
            return _full(ctx, reasons)

        prefixes = tuple("native::" + self._ext_of(f) + "." for f in fb_for_sel if f.startswith("native::"))
        f4_mods = set(changes.files)

        def hit(d):
            return any(g.startswith(p) for g in d for p in prefixes)

        od = ctx.order_dependent if self.f6order else frozenset()
        if sel & od:                       # W3-new F6-order: attribution unreliable -> all tests
            reasons.append("f6_order_dependent")
            tests = set(ctx.all_tests)
        else:
            tests = set()
        for x in ([] if sel & od else ctx.all_tests):
            d = deps[x]
            if (d is None or d & sel or x in st.failed
                    or ctx.module_of_test.get(x) in f4_mods or hit(d)):
                tests.add(x)

        if self.profile:
            benches = set()
            for b in ctx.all_benches:
                p = self._prof(t, b, st)
                if p is None or p & sel or hit(p):
                    benches.add(b)
            benches = frozenset(benches)
        else:
            benches = self._module_benches(changes)
        return Decision("incremental", frozenset(tests), benches, False, tuple(reasons))

    def observe(self, t, decision, outcome, st=None):
        st = st if st is not None else self.st
        ctx = self.ctx
        ran_t = ctx.all_tests if decision.full_check else decision.tests
        ran_b = ctx.all_benches if decision.full_check else decision.benches
        for x in ran_t:  # F3: refresh dependency observations
            st.observed[x] = t
            st.failed.discard(x)
        for b in ran_b:
            st.bobserved[b] = t
        # F4 re-run set; quarantined (flaky) tests are excluded for decision purposes (F5)
        st.failed |= set(getattr(outcome, "failed_tests", ())) - set(ctx.quarantine)
        if decision.full_check and outcome.green:
            st.acc, st.headers, st.fallbacks = frozenset(), frozenset(), frozenset()
        elif st.pending is not None:
            st.acc, st.headers, st.fallbacks = st.pending
        st.pending = None
