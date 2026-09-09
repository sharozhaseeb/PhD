# Research proposal

**Working title:** Understanding and Detecting Workload Regressions in Iterative Python Code Optimization.\
**Stage:** pre-pilot; novelty unresolved.\
**Duration:** two years, conditional on the six-week feasibility decision.

## Problem and boundary

Investigate which workload-related failures remain during repeated Python optimization after sound measurement, behavioral validation, and checks against the original baseline. Distinguish a slowdown from a violation of declared performance requirements. The project concerns preservation of tested behavior and performance over a defined workload domain; finite tests cannot establish universal equivalence or arbitrary-distribution robustness.

Existing systems already implement iterative optimization, profiling, adaptive measurement, workload variation, and performance regression diagnosis. Their existence motivates strong comparisons and limits our novelty claim. The candidate gap is a mechanism-specific empirical finding and, conditionally, an effective response beyond established safeguards. See [the literature map](03-literature-novelty-map.md).

## Questions

- **RQ1:** How often do accepted optimizations violate a declared performance policy on independently assessed workloads, and how do those outcomes evolve across a session?
- **RQ2:** Which mechanisms explain the violations after controlling timing noise, permitted workload trade-offs, and cumulative-baseline effects?
- **RQ3:** Which existing safeguards prevent them at acceptable cost, and does a focused new selector improve the trade-off?

## Candidate contributions

1. An auditable corpus of code snapshots, parent relationships, visible feedback, selected workloads, decisions, and independent measurements.
2. Verified explanations and controlled comparisons that distinguish measurement artifacts, input specialization, cumulative tolerances, and interactions among edits.
3. If justified, a workload selector using input characteristics and earlier regression evidence, evaluated against a strong combination of existing methods.

These are planned outputs. Neither a dataset nor a taxonomy automatically establishes a publishable contribution. Avoid claims based only on more iterations, a new pipeline name, or translation of an existing method to Python.

## Hypotheses and rivals

| ID | Hypothesis | Main rival | Test that could count against it |
|---|---|---|---|
| H01 | Consequential violations remain after standard safeguards. | Apparent failures are noise, permitted specialization, or cumulative losses removed by an original-baseline check. | Independent measurements and the strongest conventional policy remove most practical impact. |
| H02 | Earlier regression evidence helps select useful workloads for later changes. | Static input diversity and simple failure replay are sufficient. | A matched-cost comparison and removal of history show no practical advantage. |
| H03 | Some violations depend on interactions among edits. | One edit or measurement drift explains the outcome. | Valid reversions or controlled alternatives explain the cases without interactions. |

H03 is an exploratory diagnosis question, not a promised third paper. Numerical effect thresholds and main-study sample sizes remain pending pilot variance, costs, and advisor review. Register them before exposing the final evaluation results.

## Scope

- Python-source edits to deterministic CPU-oriented operations; native library calls may occur, but native-source edits are initially excluded and reported.
- Several open-source repositories, with documented valid input families.
- FormulaCode-V as the primary candidate source and suitable SWE-Pro tasks as a secondary source, subject to reproduction and deduplication.
- A fixed behavioral gate for initial selector comparisons.
- One reproducible optimizer for the first pilot; another configuration and human patches before broad generalization.

## Reasons to redirect

Redirect the method if broad fixed testing is already inexpensive, conventional safeguards resolve the failures, or proposed selection only gains by rejecting useful optimizations. Redirect the empirical claim if observed examples are largely invalid inputs, expected objective specialization, or already-characterized effects without additional explanatory value.

A rigorous negative result may contribute knowledge, but publication and PhD sufficiency remain subject to novelty, evidence quality, and departmental requirements.
