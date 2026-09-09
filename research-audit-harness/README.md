# PhD Research Audit Harness

The current worked example is the [Python optimization proposal](../research-directions/llm-optimization-validation/README.md). This CLI audits proposal documentation; it does not run optimization experiments. Python 3.10 or newer is required; verification used Python 3.12.10. No external packages are required.

See the [schema and behavior reference](docs/reference.md) and [9 September harness review](docs/2026-09-09-review.md) for exact checks and limitations.

## Purpose

This is a local, transparent harness for checking whether a proposed PhD direction has documented:

- a precise question and bounded contribution;
- claims separated from evidence;
- rival hypotheses and falsification tests;
- a reproducible novelty-search boundary;
- a closest-work comparison;
- baselines, ablations, and a forward test;
- validity, data, statistical, and feasibility risks;
- a negative-result path; and
- controls against leakage, attribution errors, and unfair comparisons.

It does not prove novelty, judge scientific truth, perform investment research, or certify that an experiment is statistically valid. It makes missing evidence and unresolved decisions visible.

## Design principles

- Local-only: Python standard library; no network calls.
- Evidence-bounded: unresolved novelty remains unresolved.
- Falsification-first: every primary hypothesis needs a rival and a condition that would count against it.
- Negative results are valid: the project need not assume an agent wins.
- Domain profiles: shared checks are supplemented with finance or software-performance protocol declarations.
- Non-destructive: project initialization refuses to overwrite existing audit files unless explicitly requested.

## Audit an existing direction

From the repository root:

```powershell
python research-audit-harness/scripts/audit.py research-directions/llm-optimization-validation
```

This writes:

- `research-directions/llm-optimization-validation/audit/generated-audit-report.md`
- `research-directions/llm-optimization-validation/audit/generated-audit-report.json`

Reports are replaced on each writing run. Source documents and audit tables are not modified. A missing or non-directory target produces a failure report without creating a direction.

Run without writing:

```powershell
python research-audit-harness/scripts/audit.py research-directions/llm-optimization-validation --no-write
```

Treat warnings as a failing exit status in CI:

```powershell
python research-audit-harness/scripts/audit.py research-directions/llm-optimization-validation --strict --no-write
```

## Initialize another research direction

The initializer creates the direction and audit directories if needed:

```powershell
python research-audit-harness/scripts/init_audit.py research-directions/example-direction --profile software_performance
```

The initializer uses [`templates/audit`](templates/audit) to create `project.json` and six CSV templates. It does not create narrative documents or diagrams. Protocol values start as `false`. Existing files are skipped; `--force` replaces the seven template-managed files, including populated CSV records. Changing `--profile` without `--force` does not migrate existing metadata. Generated reports and unrelated files are not template-managed.

## Required direction structure

```text
research-direction/
├── README.md
├── 01-layman-explanation.md
├── 02-research-proposal.md
├── 03-literature-novelty-map.md
├── 04-architecture-methodology.md
├── 05-advisor-questions.md
├── 06-evaluation-protocol.md
├── 07-two-year-plan.md         # or 07-three-year-plan.md
├── figures/
│   └── *.mmd
└── audit/
    ├── project.json
    ├── claims.csv
    ├── hypotheses.csv
    ├── nearest_work.csv
    ├── search_log.csv
    ├── experiments.csv
    └── risks.csv
```

## What the automated checks mean

- **PASS:** the expected artifact or field exists. It does not certify its scientific quality.
- **WARN:** unresolved information, weak coverage, or a decision needing human review.
- **FAIL:** a required artifact, schema, or critical protocol declaration is absent.

The generated report should be reviewed by the student and advisor. A passing automated report is not proposal approval.

| Exit code | Meaning |
|---|---|
| `0` | No FAIL findings; default mode permits WARN findings |
| `1` | Strict mode with WARN findings and no FAIL |
| `2` | FAIL findings, or an argparse usage error |

## Software-performance profile

Set `audit_profile` to `software_performance` in `audit/project.json`. This requires declarations for a valid workload domain, original-baseline checks, behavioral validation, noise controls, protected final evaluation, equal-information comparisons, full cost accounting, and a negative-result path. Every required flag must be the JSON boolean `true`, not a string. A declaration is a commitment, not completed validation.

Unknown profiles fail. Existing projects without `audit_profile` retain the original finance checks. The initializer defaults to finance for compatibility.

## Finance-specific checks

The stock direction additionally requires declarations for:

- point-in-time data;
- survivorship-aware universe construction;
- purging and embargo;
- a frozen test;
- prospective shadow evaluation;
- transaction costs;
- factor attribution;
- equal-information baselines;
- identifier/date masking if an LLM is used; and
- a negative-result path.

Future extensions should add explicit registries for experiment-family multiplicity, financial reality checks, PBO, deflated Sharpe, capacity assumptions, and data licensing.

## Run verification

```powershell
python -m unittest discover -s research-audit-harness/tests -v
```

## Relationship to Scientific Agent Skills

The original design drew on general evidence-boundary, rival-hypothesis, and pre-experiment design principles from an earlier inspection of Scientific Agent Skills. This harness contains local code and templates with finance and software-performance profiles; it does not install or execute third-party agent skills.

