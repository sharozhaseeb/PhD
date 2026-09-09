# Generated Research Audit Report

- Direction: `C:\Users\pc\study\PhD\research-directions\llm-optimization-validation`
- Generated: 2026-09-09T04:42:49+00:00
- Result: 31 pass, 5 warning, 0 fail
- Meaning: structural audit only; not scientific or advisor approval

## Project summary

- Title: Understanding and Detecting Workload Regressions in Iterative Python Code Optimization
- Stage: pre-pilot
- Novelty status: candidate_not_established
- Audit profile: software_performance

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
| PASS | structure | `research_plan` | Present: 07-two-year-plan.md |
| PASS | structure | `editable_figures` | Found 3 Mermaid sources |
| PASS | metadata | `project.json` | Valid JSON |
| PASS | schema | `claims.csv` | Valid schema with 7 record(s) |
| PASS | schema | `hypotheses.csv` | Valid schema with 3 record(s) |
| PASS | schema | `nearest_work.csv` | Valid schema with 14 record(s) |
| PASS | schema | `search_log.csv` | Valid schema with 7 record(s) |
| PASS | schema | `experiments.csv` | Valid schema with 10 record(s) |
| PASS | schema | `risks.csv` | Valid schema with 10 record(s) |
| PASS | metadata | `audit_profile` | Using software_performance |
| PASS | protocol | `valid_workload_domain_defined` | Explicitly required |
| PASS | protocol | `original_baseline_comparison_required` | Explicitly required |
| PASS | protocol | `behavioral_validation_required` | Explicitly required |
| PASS | protocol | `noise_control_required` | Explicitly required |
| PASS | protocol | `frozen_test_required` | Explicitly required |
| PASS | protocol | `equal_information_baselines_required` | Explicitly required |
| PASS | protocol | `full_validation_cost_required` | Explicitly required |
| PASS | protocol | `negative_result_path_defined` | Explicitly required |
| PASS | claims | `novelty_language` | Appropriately bounded: candidate_not_established |
| PASS | claims | `unsupported_claims` | No rows use unsupported-status labels; evidence itself is not verified |
| WARN | claims | `unresolved_novelty` | 1 novelty claim(s) remain unresolved, as expected at this stage |
| PASS | hypotheses | `falsification_ready` | Every hypothesis has a rival, test, metric, and falsification condition |
| PASS | novelty | `nearest_work_depth` | 14 closest works recorded |
| WARN | novelty | `critical_overlap` | 12 critical overlap record(s); contribution wording requires human review |
| WARN | novelty | `reproducible_searches` | Fewer than three searches record result, screened, and included counts |
| WARN | novelty | `pending_searches` | 2 search record(s) remain pending |
| PASS | experiments | `experiment_families` | Baselines, proposed method, ablations, and forward test are registered |
| PASS | experiments | `confirmatory_result_visibility` | No registered confirmatory result is marked visible |
| WARN | risks | `open_critical_risks` | 4 critical risk(s) remain open |

## Human decisions still required

Warnings are intentionally retained. Novelty, domain-specific statistical validity, data licensing, and proposal approval require documented human review.
