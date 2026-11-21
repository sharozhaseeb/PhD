# Advisor-persona review of W3 readiness (DRAFT v1, 2026-11-21 16:45)

Reviewed: `research-directions/build-test-reduction/03-experiment/readiness.md`. Reviewer: advisor-persona subagent (AI-SIM, not the advisor). Nothing has been run yet apart from the repository probes, so this reviews the design, not results.

## Verdict

**Approve with three changes before runs start.** This is the strongest document in the package. The oracle, the frozen fault sets, the miss statistics and the cherry-picking controls are what an advisor checks first, and they hold up. The weak points are elsewhere:
- **RQ1 may show that build cost is negligible** on all three chosen repositories.
- **The new benchmark-selection component is compared only with a naive baseline**, not with existing work.
- **The fault design gives the "accumulation" component almost no chance to matter.** Its ablation result is then fixed in advance.

## Does it answer predicted questions P01, P03, P04 and P05?

| Prediction | Answered? | Assessment |
|---|---|---|
| P01: cost of a full build plus a full test run per edit | **Planned, no numbers yet** | The RQ1 design is right: per-edit split into build, tests and benchmarks, plus the cumulative curve. However, networkx and sqlglot have no build step, and bottleneck has 4 small C extensions, so build will likely take seconds. If every target shows the build share near zero, the advisor will ask why "reduced build" is in the title. Benchmarks will probably dominate, which is a good answer, but it has to be framed that way on purpose. |
| P03: why Python, and what gets built | **Partly** | The answer is bottleneck, which is one small, old (2019–20) project that only builds with compatibility patches (T7). It is a convincing *story* because of its real burst of PERF commits. It is not convincing *build-cost* evidence. T5 honestly admits the gap for meson-heavy projects; the advisor will want at least one number from such a project. |
| P04: how do we know nothing was missed | **Yes, well answered** | Strong points: FULL is the oracle at every state; mutants only count if FULL kills them; survivors are reported separately. The regression definition is fixed in advance, with the original base B as reference. Results use "k of N" with Wilson CIs and never claim "0 misses = safe". Each miss gets a reason. Keep all of this. |
| P05: one worked edit, full against reduced | **Planned** (`results/worked-edit.md`) | Fine. Pick the worked edit from bottleneck: it shows the build, test and benchmark steps all at once. |

## Will the target repositories survive the meeting?

- **networkx (pilot, pure Python):** survives as a pilot. Expect the question "testmon already works on pure Python; what does your rule add here?" The answer has to come from the benchmark and checkpoint parts, not from test selection.
- **bottleneck (C extension):** survives as the realistic iterative case. The 17 PERF commits in one burst are the best "session-like" history in the package, so say so explicitly. The build-cost point fails, though, because it is tiny. The fallback in §1.2 is muddled. If the 2019 base does not build, choose "RQ1 cost only" rather than trying shapely in a hurry.
- **sqlglot:** fine to cut first. If it is kept, the AI-authored commits are correctly flagged.

## Will the comparison arms survive?

The structure is good: FULL, incremental build, testmon as shipped, a naive changed-module rule, periodic full checks with a sweep over k, the new policy (A4), three ablations, and a matched-cost frontier. That answers "compare against a strong combination at equal cost". Two gaps:

1. **No existing benchmark-selection baseline.** Benchmarks are either "all" (A1, A2) or chosen by file name (A3). A4's profile/call-graph benchmark selection (P1) is therefore only compared with a strawman. Dependency-based selection of performance tests already exists in the literature. So the advisor will say P1 is "coverage-based benchmark selection, already done".
2. **The accumulation ablation is likely null by construction.** Each mutant and synthetic slowdown sits *in a function changed by edit s*, so it is part of step s's change set. Any correct dependency selector picks the killing tests at step s itself. Re-selecting the accumulated set at later steps only adds redundancy. Two consequences:
   - "A4 − accum" will probably equal A4. That is a real result, but nobody should be surprised by it in the meeting.
   - Accumulation can only help when the dependency map at step s is stale or incomplete, or when a fault becomes visible only after a later edit. The kill-set reuse assumption (T3) hides the second case.

Minor points:
- The A4 bundle has about 15 rules. Report which few of them drive the result.
- The ≥2× injected slowdowns are easy to detect. Add some at about 1.2–1.5×, near the 1.10 threshold, so benchmark-selection misses can actually appear.

## Three changes that matter before runs start

1. **Add one RQ1 cost-only data point on a heavy compiled Python project** (for example scikit-learn or pandas with a meson build): a clean build against an incremental build after a single-file `.pyx`/C edit, plus the full test and benchmark times. Run it once, with no safety arm. Without it, "reduced build" has no evidence behind it.
2. **Add an existing dependency-based benchmark-selection arm.** Use the same test→function map applied to the asv benchmarks, for the current edit only, cite the literature, and compare P1 against it. Do the same in the matched-cost frontier.
3. **Make the accumulation hypothesis testable.** Write down the mechanism by which accumulated selection catches something that current-edit selection misses. Then add a small *latent* fault class (faults or slowdowns that tests can only see after a later replayed edit changes the call path), and measure the kill set again at each step for that class. If this is not feasible, state in advance that ablation (a) is expected to be null and say why.
