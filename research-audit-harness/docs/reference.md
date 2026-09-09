# Harness reference

This describes [audit.py](../scripts/audit.py) and [init_audit.py](../scripts/init_audit.py). The tool checks local documentation. It does not read paper contents, inspect datasets, execute code optimizers, or use external services.

## Commands and side effects

| Command | Reads | Writes |
|---|---|---|
| `audit.py DIRECTION` | Documents, Mermaid filenames, metadata, and CSVs | Replaces two `audit/generated-audit-report.*` files |
| `audit.py DIRECTION --no-write` | Same inputs | None; prints Markdown |
| `audit.py DIRECTION --strict` | Same inputs | Same reports; warnings change the exit code |
| `init_audit.py DIRECTION --profile PROFILE` | Shared templates and protocol registry | Missing template-managed files under `audit/` |
| `init_audit.py DIRECTION --profile PROFILE --force` | Same templates | Replaces template-managed metadata and CSVs |

Paths are resolved relative to the caller's working directory. The initializer locates templates relative to its script. Missing/non-directory audit targets produce a failure report and exit 2 without creating directories. `--no-write` and `--strict` are independent. Initialization returns 0 even when files are skipped; it does not run an audit.

## Metadata

`audit/project.json` must decode as a JSON object. UTF-8 with optional BOM is supported. Invalid JSON or a non-object value produces a metadata FAIL.

| Field | Use by checker |
|---|---|
| `project_id` | Report summary; defaults to direction name |
| `title` | Report summary; defaults to direction name |
| `stage` | Report summary; defaults to `unknown` |
| `novelty_status` | PASS for `candidate_not_established`, `unresolved`, or `under_review`; WARN otherwise |
| `audit_profile` | `finance` or `software_performance`; absent means legacy finance; other values fail |
| `protocol` | Selected profile's required boolean declarations |

Other fields, including `literature_cutoff`, `planning_horizon_months`, `prohibited_claims`, and `open_decisions`, are useful documentation but are not automatically validated. This is not a full JSON Schema validator and does not infer the scientifically appropriate profile.

## Protocol declarations

Software performance requires:

```text
valid_workload_domain_defined
original_baseline_comparison_required
behavioral_validation_required
noise_control_required
frozen_test_required
equal_information_baselines_required
full_validation_cost_required
negative_result_path_defined
```

Finance requires:

```text
point_in_time_data_required
survivorship_aware_universe_required
purge_and_embargo_required
frozen_test_required
prospective_shadow_test_required
transaction_costs_required
factor_attribution_required
equal_information_baselines_required
identifier_date_masking_required_for_llm
negative_result_path_defined
```

Every value must be JSON boolean `true`. False, absent, numeric, or string values fail. Extra protocol keys are ignored. Declarations do not prove controls were implemented; explain their applicability in the proposal's evaluation protocol.

## CSV schemas

Files use UTF-8 with optional BOM. Required headers are exact and case-sensitive; order is flexible and extra named columns are allowed. Duplicate/blank headers and rows with more fields than headers fail. Missing cells become empty strings. Empty tables warn. Nonempty tables with valid required headers enter downstream checks.

| File | Required columns |
|---|---|
| `claims.csv` | `claim_id`, `claim`, `claim_type`, `status`, `evidence_required`, `current_evidence`, `owner`, `next_action` |
| `hypotheses.csv` | `hypothesis_id`, `hypothesis`, `rival_explanation`, `discriminating_test`, `primary_metric`, `falsification_condition`, `status` |
| `nearest_work.csv` | `paper_id`, `year`, `title`, `authors`, `url`, `overlap`, `claimed_difference`, `status`, `last_checked` |
| `search_log.csv` | `search_id`, `date`, `database_or_source`, `query`, `filters`, `result_count`, `screened_count`, `included_count`, `notes` |
| `experiments.csv` | `experiment_id`, `name`, `family`, `confirmatory`, `primary_outcome`, `data_window`, `status`, `result_visible`, `notes` |
| `risks.csv` | `risk_id`, `category`, `risk`, `severity`, `likelihood`, `mitigation`, `trigger`, `status` |

Quote fields containing commas or newlines. Cell whitespace is trimmed. Record ID uniqueness, cross-file references, URLs, dates, authors, and all nonempty cell requirements are not validated.

## Exact checks

| Check | Behavior |
|---|---|
| Core documents | Seven named narrative files; more than 100 bytes passes, shorter warns, missing fails |
| Research plan | At least one of `07-two-year-plan.md` or `07-three-year-plan.md`, using the same size convention |
| Figures | At least three `.mmd` files directly in `figures/` passes; one/two warns; none fails; content is not checked |
| Claims | WARN for statuses `unsupported` or `claimed_without_evidence`; evidence itself is not verified |
| Novelty rows | WARN when `claim_type=novelty` and status differs from `established`; establishment is not verified |
| Hypotheses | Every row needs a nonblank rival, discriminating test, primary metric, and falsification condition |
| Closest work | Eight or more rows passes the depth convention; fewer nonzero rows warns; `critical` in a status warns |
| Search counts | Complete integer triples satisfying `0 <= included <= screened <= result` count; fewer than three complete searches warns |
| Invalid counts | Partial, nonnumeric, negative, or inconsistently ordered triples warn; all-blank triples remain uncounted |
| Pending searches | `pending` in source or notes produces WARN |
| Experiments | Families must include `baseline`, `proposed`, `ablation`, and `forward_test` |
| Confirmatory results | WARN when both `confirmatory` and `result_visible` contain `true` |
| Critical risks | WARN for critical severity unless status is `closed`, `mitigated`, or `accepted` |

Status/family checks are case-insensitive except metadata novelty values. Counts and row depth remain declarations, not verification of search provenance or scientific relevance. Zero-result searches can have valid counts.

`forward_test` is interpreted by the direction. Here it can mean a frozen evaluation on untouched tasks/workloads; finance may require chronological evaluation. Registering either does not mean it ran.

## Outputs and exits

Exit 2 indicates FAIL findings or argparse usage errors. Otherwise, strict mode returns 1 if warnings remain; default mode returns 0. Reports are written before those finding-based exit codes are returned unless `--no-write` is set or the target is not a directory.

Markdown reports contain the path, UTC generation time, totals, summary, findings, and human-review reminder. JSON contains `direction`, `generated_at`, `summary`, `result_counts`, and findings with `status`, `category`, `check`, and `detail`. Independently generated timestamps may differ slightly.

Reports are replaced snapshots. The CLI does not retain report history or sign evidence. Output permission and other filesystem errors can still produce Python exceptions.

## Limits and extension

A passing report cannot establish novelty, literature completeness, causal validity, data access, absence of leakage, appropriate sample size, or publication prospects. The checker does not inspect prose or enforce `prohibited_claims`. Keep uncertainty visible; never invent counts or irrelevant declarations to clear warnings.

The profile registry is in `audit.py` and is shared by the initializer. A new domain needs explicit rules, tests, and documentation. Older packages retain finance behavior by default.
