# Proposal audit records

These records document the current research plan. They do not contain benchmark results. The local checker validates structure and selected declarations; it does not conduct literature searches, verify citations, run optimizers, or establish statistical validity.

| File | Record |
|---|---|
| [project.json](project.json) | Scope, software-performance profile, required controls, and prohibited claims |
| [claims.csv](claims.csv) | Candidate claims and evidence still required |
| [hypotheses.csv](hypotheses.csv) | Rivals, discriminating tests, and falsification conditions |
| [nearest_work.csv](nearest_work.csv) | Closest methods and explicit overlap |
| [search_log.csv](search_log.csv) | Earlier searches and outstanding work; missing historical counts remain blank |
| [experiments.csv](experiments.csv) | Planned baseline, proposed, ablation, and final untouched evaluation families |
| [risks.csv](risks.csv) | Open research, measurement, and implementation risks |
| [Generated report](generated-audit-report.md) | Latest structural results |

## Run

From the workspace root:

```powershell
python research-audit-harness/scripts/audit.py research-directions/llm-optimization-validation
python research-audit-harness/scripts/audit.py research-directions/llm-optimization-validation --strict --no-write
```

PASS means a supported structural condition or declaration was found. WARN marks unresolved information or decisions. FAIL marks missing or invalid required structure/protocol. Default mode returns 0 with warnings; strict mode returns 1 with warnings; failures return 2. Generated reports are replaced on each writing run; source documents and CSVs are not changed.

## Interpretation for this proposal

- `audit_profile` is `software_performance`. Finance declarations are not applicable and are not asserted.
- Protocol booleans mean controls are required, not implemented or validated.
- Novelty remains `candidate_not_established`; unresolved novelty and critical overlap warnings are intentional.
- Literature was reviewed through 7 September 2026. The 9 September documentation work is not a new search. Unavailable historical result counts are left empty.
- `forward_test` means a frozen, untouched task/workload evaluation in this domain; all experiments remain planned and their results are not visible.
- A required two-year plan is provided. The checker also supports existing three-year packages.
- Thresholds, sample size, artifact reproduction, and departmental expectations remain open.

See [the harness reference](../../../research-audit-harness/docs/reference.md) and [the review of its limitations](../../../research-audit-harness/docs/2026-09-09-review.md).
