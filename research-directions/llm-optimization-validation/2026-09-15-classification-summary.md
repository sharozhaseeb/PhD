# Can We Classify Whether a Code Change Is an Optimization?

**Research summary — 15 September 2026**

**Read the [full research report](2026-09-15-classification-full-research.md) for methods, classification rules, experiment design, datasets, 36 source-register entries, and the search trace.** Three research agents investigated complementary approaches; a coordinating review checked the main conclusions. This is a targeted literature review, with no experiments run and no established novelty claim.

## The answer

Yes: we can predict or experimentally assess whether **a modified Python program improves on its original version under specified conditions**. The conditions include valid inputs, required behavior, hardware/software environment, and the performance objective. The result can change with the workload.

Our recommended first study is:

> **When do existing code-efficiency judgments survive independent timing and workload validation, and what does reliable validation cost?**

This is a proposed empirical question. Its novelty and feasibility still need a focused pilot.

## What has already been done

Three findings substantially narrow the research opportunity:

1. **Learned code-pair classification exists.** Seo et al.'s _Rethinking Code Refinement: Learning to Judge Code Efficiency_ (2024) learns efficiency judgments and relative improvement prediction, including Python. [Paper](https://aclanthology.org/2024.findings-emnlp.645/).
2. **Execution-based multi-outcome classification exists.** SWE-Pro separates improved, regressed, conflicting, no-signal, and unmeasurable results. [Appendix E.5](https://arxiv.org/html/2606.25530v1#A5.SS5).
3. **Remeasuring optimization pairs and generating stronger tests exists.** The 2026 _Rethinking Code Performance Benchmarks for LLMs_ preprint directly investigates benchmark judgments and performance-test generation. [Paper](https://arxiv.org/html/2607.07619v1).

Consequently, a new classifier, extra output labels, or a testing pipeline alone would have weak originality. Our contribution would need to establish a consequential limitation that persists under credible existing methods.

## Which approaches should we consider?

The roles below are our recommendations; the linked full-report sections give the underlying research and limitations.

| Approach | Useful role in our study | Main caveat |
|---|---|---|
| Static/diff and complexity analysis | Cheap prediction and explanation | Input sizes, constants, state, and libraries matter |
| Prompted or trained code-efficiency judge | Predict direction or magnitude of change | Must be evaluated against independent measurements |
| Repeated comparative benchmarking | Establish an effect and its uncertainty | Evidence covers the measured conditions |
| Adaptive measurement | Spend more measurements on difficult cases | Requires an appropriate stopping/error policy |
| Multiple workload families | Find improvements that become regressions elsewhere | Finite coverage and chosen weights limit conclusions |
| Performance-guided input generation | Search for valid counterexamples | Failure discovery does not estimate production frequency |
| Change-aware selection and replay | Reduce work using affected code and previous failures | New behavior may be missed |
| Combined prediction and selective execution | Potentially reduce total cost | Must beat straightforward additional measurement |

See [method comparison](2026-09-15-classification-full-research.md#4-methods-available-for-classification) and [statistical rules](2026-09-15-classification-full-research.md#5-an-operational-classification-scheme-to-evaluate). Profiling is an additional diagnostic method, and behavioral testing is a prerequisite for accepting a speed improvement.

## What our classifier should output

Keep behavioral evidence, workload-specific performance, and the final accept/reject/defer action separate. Our proposed performance labels are **improved, regressed, practically equivalent, or inconclusive**, with **mixed** identifying supported gains and losses across workloads. A gain for small inputs and a loss for large inputs should remain visible.

Practical equivalence requires evidence inside a predeclared tolerance; failure to detect a difference is insufficient. Thresholds such as 5% in the full report are illustrative. [Equivalence-testing foundation](https://doi.org/10.1177/1948550617697177).

An isolated block should be extracted only when its context and effects can be preserved. Otherwise compare its enclosing function or repository patch. A candidate with changed required behavior fails the acceptance gate even if it runs faster.

## A manageable first study

Start with a small reproducibility pilot and approximately 20–30 feasible tasks across several Python projects; this is a planning estimate, not a statistically powered sample size. Use FormulaCode-V as the first repository source and suitable SWE-Pro tasks as a second source. PIE's earlier Python release provides simpler standalone pairs. [FormulaCode data](https://huggingface.co/datasets/formulacode/formulacode-all), [SWE-Pro data](https://huggingface.co/datasets/probench-swe/SWE-Pro), [PIE Python release](https://github.com/madaan/pie-perf).

Include failed candidate attempts, no-change controls, and near-neutral changes alongside successful human optimizations. Split by task/problem and, where feasible, repository. Freeze hidden workload evaluation separately from fresh timing repetitions.

Compare a small set of existing judges, repeated measurement, and strong combined validation. Report **harmful approvals, useful improvements retained, uncertainty/deferrals, and full cost**. Rejecting every change should not count as success. Extend into a new method only if those comparisons reveal a useful unresolved problem.

Read the [full study design](2026-09-15-classification-full-research.md#7-a-first-study-that-compares-the-methods-fairly), [novelty assessment](2026-09-15-classification-full-research.md#8-novelty-assessment-and-possible-directions), and [six-week pilot](2026-09-15-classification-full-research.md#9-feasible-next-steps) before choosing the implementation scope. Artifact reproducibility and the complete TT-MDE method remain among the [open checks](2026-09-15-classification-full-research.md#11-search-trace-and-unresolved-checks).
