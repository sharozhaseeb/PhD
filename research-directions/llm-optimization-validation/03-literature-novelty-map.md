# Literature and novelty map

**Evidence boundary:** this document consolidates the targeted primary-source review conducted on 7 September 2026. Documentation was organized on 9 September; that is not a new literature search. Papers and public artifacts were inspected, but results were not reproduced. Publication status refers to what that review verified.

The machine-readable [nearest-work register](audit/nearest_work.csv) records comparisons. Detailed discussion remains in the [pivot review](2026-09-07-pivot-advisor-review.md) and [methods map](2026-09-07-methods-map.md).

| Work | Existing method or resource | Implication |
|---|---|---|
| [PerfAgent](https://arxiv.org/html/2607.19653v1) | Iterative profiling, selective validation, and best-patch selection; July 2026 preprint | Particularly close overlap. Complete public implementation was not located in the review. |
| [FormulaCode](https://arxiv.org/html/2603.16011v1) | Real repository tasks and multiple performance workloads | Workload trade-off analysis is already a benchmark feature. |
| [SWE-Pro](https://arxiv.org/html/2606.25530v1) | Structured input variation and adaptive, noise-aware runtime/memory measurement | Diverse workloads plus adaptive timing are established. |
| [WEDGE](https://arxiv.org/abs/2505.23471) | Performance constraints guide input generation | Generating performance-revealing inputs requires strong comparisons. |
| [Perun](https://github.com/Perfexionists/perun) | Version-linked profiles, degradation detection, modeling, and fuzzing | Performance history infrastructure is established. |
| [APOLLO](https://github.com/sslab-gatech/apollo) | Regression query generation, reduction, and diagnosis | Small reproducers and diagnosis have substantial precedent. |
| [Performance evolution study](https://link.springer.com/article/10.1007/s10664-023-10338-3) | Configuration-dependent performance across releases | Longitudinal performance analysis predates agents. |
| [SlopCodeBench](https://arxiv.org/abs/2603.24755) | Quality outcomes over iterative coding tasks | Iteration alone does not establish a new question. |
| [Rethinking performance benchmarks](https://arxiv.org/html/2607.07619v1) | Benchmark re-evaluation and test generation/diagnosis/repair | Exposing weak tests alone is a crowded contribution. |
| [Microbenchmark prioritization](https://link.springer.com/article/10.1007/s10664-021-10037-x) | Coverage-based and change-aware ordering | Relevant-test selection needs an advantage beyond conventional ordering. |
| [irace](https://github.com/MLopez-Ibanez/irace) | Racing among candidate configurations | Candidate elimination and budget allocation are established. |
| [TT-MDE artifact](https://github.com/chenzongxiong/ASE-2026) | Detectability-oriented measurement procedures | The full method remains a required follow-up before a competing statistical claim. |

## Search boundary and outstanding work

Earlier web queries and fixed-page inspections are recorded in [search_log.csv](audit/search_log.csv). Historical result counts were not consistently captured. Those fields remain blank; do not reconstruct counts or describe the review as systematic. Source-inspection notes and remaining database searches are kept distinct.

Before claiming novelty, archive query strings, search dates, databases, inclusion/exclusion rules, returned records, deduplication decisions, and screened/included counts. Perform backward and forward citation screening around the closest methods. Confirm artifact access and practical adaptation costs. Update this map and the CSV together when evidence changes.

## Candidate differentiation

The empirical study must explain which failures survive sound measurement, declared workload requirements, and original-baseline checks. The candidate selector must beat a diverse static suite plus change-aware selection and historical failure replay at matched total cost. These remain hypotheses rather than verified absences in the literature.

No claim of novelty, superiority, universal reliability, or a numerical publication probability is supported by the current review.
