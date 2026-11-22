# Study 1 knowledge base

**Last updated:** 2026-11-22 ~06:12 PKT (overnight queue done; synced with W3's critic pass, PM rulings D18–D20 and the item-1 write-up).

## What the study is

Study 1 asks how to validate each edit of an iterative code optimization with a **reduced build** and a **reduced test and benchmark set**, chosen by **deterministic rules with no AI**, and how far that can be trusted. AI-based selection is a later study. Source: [CHARTER](../pm/CHARTER.md).

Three research questions (revised 2026-11-21): RQ1 cost, RQ2 existing techniques unchanged, RQ3 a new deterministic policy. See [research.md](research.md).

Subjects: networkx (pure Python, 18 replayed edits) and bottleneck (C extension). Everything is a pilot on one laptop. Nothing has been approved by the real advisor; all advisor "reviews" are AI-written rehearsals ([persona](../pm/advisor/persona.md)).

## How this knowledge base is organised

| Page | What it holds |
|---|---|
| [WORKLOG.md](WORKLOG.md) | Dated log of everything that happened, newest at the bottom. Append here. |
| [decisions.md](decisions.md) | Decision register: what was decided, by whom, why, what was rejected. |
| [experiments.md](experiments.md) | One section per experiment or run: setup, command, status, result, caveats, raw data. |
| [findings.md](findings.md) | Current findings with status (measured / provisional / pending) and evidence. |
| [research.md](research.md) | Problem, RQs, literature map, prior work, practice survey, gap, claims, candidate rules. |
| [glossary.md](glossary.md) | Terms and arm names. |
| [open-questions-and-next.md](open-questions-and-next.md) | Pending work, advisor asks, future work. |

Rules for this folder: every number links to the file it came from. Inferred statements say "inferred". The knowledge base links to sources; it does not replace them.

## Main source folders

| Folder | Content |
|---|---|
| [`../pm/`](../pm/CHARTER.md) | Charter, [TPM log](../pm/tpm-log.md), [advisor persona and reviews](../pm/advisor/persona.md) |
| [`../01-literature/`](../01-literature/README.md) | W1: [review](../01-literature/review.md), [taxonomy](../01-literature/taxonomy.md), [candidate rules](../01-literature/candidate-rules.md), [closest works](../01-literature/closest-works.md), [claims](../01-literature/beyond-literature-claims.md), [search log](../01-literature/gap-and-search-log.md), [ACM/IEEE search](../01-literature/database-search-2026-11-21.md), [references.bib](../01-literature/references.bib) |
| [`../02-practice-survey/`](../02-practice-survey/README.md) | W2: [findings](../02-practice-survey/findings.md), [survey table](../02-practice-survey/survey-table.md), [per-system notes](../02-practice-survey/per-system/) |
| [`../03-experiment/`](../03-experiment/README.md) | W3: [readiness](../03-experiment/readiness.md), [rules](../03-experiment/rules.md), [frozen inputs](../03-experiment/frozen/FROZEN.md), [results](../03-experiment/results/results.md), [hazard study](../03-experiment/results/build-hazard-iterators-h.md), [overnight queue](../03-experiment/results/OVERNIGHT.md), [raw data](../03-experiment/results/raw/), [raw-data manifest](../03-experiment/results/RAW-DATA-MANIFEST.md) |
| [`../meeting-2026-11-advisor/`](../meeting-2026-11-advisor/README.md) | W4: meeting pack, [agenda and asks](../meeting-2026-11-advisor/01-agenda-and-asks.md), [results summary](../meeting-2026-11-advisor/03-results-summary.md) |
| [`../video/`](../video/shot-list.md) | W5: walkthrough video shot list (the video itself lives outside the repo) |

Study overview page: [../README.md](../README.md).

## Who is who

| Role | Who |
|---|---|
| Owner | The PhD student. Makes approvals. |
| PM | Main Claude session; orchestrates and rules. |
| W1 | Literature architect session |
| W2 | Practice-survey architect session |
| W3 | Experiment architect session (harness, runs, results) |
| W4 | Repo formatting and advisor meeting pack session |
| W5 | Walkthrough video session |
| TPM | Subagent for risk, feasibility and validity review |
| Advisor persona | Subagent simulating the advisor (AI-SIM, not the real advisor) |
