# PhD Research Audit Harness

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
- Domain extension: generic checks are supplemented with finance-specific protocol flags.
- Non-destructive: project initialization refuses to overwrite existing audit files unless explicitly requested.

## Audit an existing direction

From the repository root:

```powershell
python research-audit-harness/scripts/audit.py research-directions/stock-selective-routing
```

This writes:

- `research-directions/stock-selective-routing/audit/generated-audit-report.md`
- `research-directions/stock-selective-routing/audit/generated-audit-report.json`

Run without writing:

```powershell
python research-audit-harness/scripts/audit.py research-directions/stock-selective-routing --no-write
```

Treat warnings as a failing exit status in CI:

```powershell
python research-audit-harness/scripts/audit.py research-directions/stock-selective-routing --strict
```

## Initialize another research direction

Create the target direction folder and then run:

```powershell
python research-audit-harness/scripts/init_audit.py research-directions/example-direction
```

The initializer copies the files in [`templates/audit`](templates/audit). It will not replace existing files unless `--force` is supplied.

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
├── 07-three-year-plan.md
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

## Relationship to Scientific Agent Skills

The design borrows general principles—evidence boundaries, rival hypotheses, critical review, and pre-experiment design—from the inspected Scientific Agent Skills repository. No third-party skill or script has been copied, installed, or executed. This harness is a small finance-oriented implementation using original local files and standard-library code.

