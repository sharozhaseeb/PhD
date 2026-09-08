# Generated Research Audit Report

- Direction: `C:\Users\pc\study\PhD\research-directions\stock-feedback-calibration`
- Generated: 2026-09-05T14:26:17+00:00
- Result: 32 pass, 5 warning, 0 fail
- Meaning: structural audit only; not scientific or advisor approval

## Project summary

- Title: Daily-feedback-assisted calibration of five-day return prediction intervals
- Stage: pre-pilot
- Novelty status: candidate_not_established

## Findings

| Status | Category | Check | Detail |
|---|---|---|---|
| PASS | structure | `README.md` | Present and non-trivial |
| PASS | structure | `01-layman-explanation.md` | Present and non-trivial |
| PASS | structure | `02-research-proposal.md` | Present and non-trivial |
| PASS | structure | `03-literature-novelty-map.md` | Present and non-trivial |
| PASS | structure | `04-architecture-methodology.md` | Present and non-trivial |
| PASS | structure | `05-advisor-questions.md` | Present and non-trivial |
| PASS | structure | `06-evaluation-protocol.md` | Present and non-trivial |
| PASS | structure | `07-three-year-plan.md` | Present and non-trivial |
| PASS | structure | `editable_figures` | Found 3 Mermaid sources |
| PASS | metadata | `project.json` | Valid JSON |
| PASS | schema | `claims.csv` | Valid schema with 6 record(s) |
| PASS | schema | `hypotheses.csv` | Valid schema with 4 record(s) |
| PASS | schema | `nearest_work.csv` | Valid schema with 9 record(s) |
| PASS | schema | `search_log.csv` | Valid schema with 7 record(s) |
| PASS | schema | `experiments.csv` | Valid schema with 9 record(s) |
| PASS | schema | `risks.csv` | Valid schema with 10 record(s) |
| PASS | protocol | `point_in_time_data_required` | Explicitly required |
| PASS | protocol | `survivorship_aware_universe_required` | Explicitly required |
| PASS | protocol | `purge_and_embargo_required` | Explicitly required |
| PASS | protocol | `frozen_test_required` | Explicitly required |
| PASS | protocol | `prospective_shadow_test_required` | Explicitly required |
| PASS | protocol | `transaction_costs_required` | Explicitly required |
| PASS | protocol | `factor_attribution_required` | Explicitly required |
| PASS | protocol | `equal_information_baselines_required` | Explicitly required |
| PASS | protocol | `identifier_date_masking_required_for_llm` | Explicitly required |
| PASS | protocol | `negative_result_path_defined` | Explicitly required |
| PASS | claims | `novelty_language` | Appropriately bounded: candidate_not_established |
| PASS | claims | `unsupported_claims` | No claim is labelled as established without evidence |
| WARN | claims | `unresolved_novelty` | 1 novelty claim(s) remain unresolved, as expected at this stage |
| PASS | hypotheses | `falsification_ready` | Every hypothesis has a rival, test, metric, and falsification condition |
| PASS | novelty | `nearest_work_depth` | 9 closest works recorded |
| WARN | novelty | `critical_overlap` | 9 critical overlap record(s); contribution wording requires human review |
| WARN | novelty | `reproducible_searches` | Fewer than three searches record result, screened, and included counts |
| WARN | novelty | `pending_searches` | 3 search record(s) remain pending |
| PASS | experiments | `experiment_families` | Baselines, proposed method, ablations, and forward test are registered |
| PASS | experiments | `confirmatory_result_visibility` | No registered confirmatory result is marked visible |
| WARN | risks | `open_critical_risks` | 6 critical risk(s) remain open |

## Human decisions still required

Warnings are intentionally retained. Novelty, finance-specific statistical validity, data licensing, and proposal approval require documented human review.
