# Understanding and Detecting Workload Regressions in Iterative Python Code Optimization

**Status:** provisional PhD direction; pre-pilot.\
**Planning horizon:** two years.\
**Documentation updated:** 9 September 2026.\
**Literature review boundary:** targeted review through 7 September 2026; systematic search and novelty assessment remain open.

The project investigates which workload-related failures persist when Python code is optimized repeatedly, and whether a small, adaptively selected workload suite can prevent them at acceptable cost. The first contribution is an empirical study. A new selector is conditional on finding an important limitation in strong existing safeguards.

No optimization benchmark has been executed for this project. No new selector, speedup, error guarantee, publication probability, or established novelty is claimed. The existing research audit harness checks this documentation; it is not the proposed runtime experiment harness.

## Read this package

| Document | Purpose |
|---|---|
| [Plain-language explanation](01-layman-explanation.md) | Problem, example, and intended outcome |
| [Research proposal](02-research-proposal.md) | Questions, candidate contribution, scope, and falsification |
| [Literature and novelty map](03-literature-novelty-map.md) | Existing methods, overlap, evidence boundary, and remaining searches |
| [Architecture and methodology](04-architecture-methodology.md) | Proposed experiment components and data flow |
| [Advisor decisions](05-advisor-questions.md) | Decisions needed before the main experiment |
| [Evaluation protocol](06-evaluation-protocol.md) | Comparison policies, measurements, splits, metrics, and controls |
| [Two-year plan](07-two-year-plan.md) | Six-week pilot and subsequent decision gates |
| [Audit records](audit/README.md) | Claims, hypotheses, experiments, risks, and report interpretation |
| [Editable diagrams](figures/README.md) | Study workflow, evidence separation, and feasibility decisions |

## Audit the documentation

From `C:\Users\pc\study\PhD` with Python available:

```powershell
python research-audit-harness/scripts/audit.py research-directions/llm-optimization-validation
```

Read [the generated report](audit/generated-audit-report.md). `--no-write` prints the report without changing files; `--strict` returns exit code 1 when warnings remain and there are no failures. Exit code 2 means a structural or protocol failure. Warnings about novelty, search completeness, and feasibility are expected at this stage.

## Relationship to earlier discussion

The initial acceptance-controller proposal remains in the dated [benchmark plan](2026-09-07-benchmark-plan.md). The [pivot advisor review](2026-09-07-pivot-advisor-review.md) explains why the empirical study takes priority. The [earlier review](2026-09-07-advisor-review.md) and [expanded methods map](2026-09-07-methods-map.md) remain as historical research notes. The numbered documents are the current operational proposal; they preserve the unresolved questions from those reviews.
