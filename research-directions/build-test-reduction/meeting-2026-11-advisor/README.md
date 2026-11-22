# Advisor meeting pack, about 2026-11-23/24

**Status:** 2026-11-21, updated 2026-11-22 13:29 PKT against W3's final results.md (completed queue: A/A, profile-completeness 5/5, Q3). `03-results-summary.md` holds W3's PRELIMINARY pilot results, ordered cost → oracle gap (B1) → testmon → A4 negatives. The latest edits are not committed.

**Left to do:**
- A measured setup-cached benchmark pass is not scheduled (the pack uses W3's estimate).

**Evidence boundary.** Every statement in this pack is condensed from a file in this repository and links to it. Where evidence does not exist, the text says so (pending, not measured, not validly tested). Predicted questions come from an AI model of the advisor ([persona](../pm/advisor/persona.md)); they are rehearsal, not the advisor's views.

## Changes from the advisor-persona review of the new results

Applied from [review-new-results](../pm/advisor/review-new-results.md) section (c) (AI-SIM), 2026-11-22.

| Action | Change | Where | State |
|---|---|---|---|
| Drop | "No benchmark A/A noise floor yet" and "A/A running", replaced by the A/A numbers (0/46, limits) | 03 S2, S7; 00 Noise; Q&A Q4, P20 | applied |
| Drop | "B1 replication in progress", replaced by the Q3 outcome ("not validly tested") | 03 S2; 00; Q&A Q1, N1; A13 | applied |
| Drop | "Completeness check 3 of 5, 0 slower in 30", replaced by 5 of 5, 1 slower in 50, flag stands, re-check not confirmed | 03 S2; Q&A P04, N4 | applied |
| Drop | "88–94% is import-time setup" as a setup share; it is the `benchmark_algorithms` share including loops | 03 S1 and story; 00 | applied |
| Soften | "most optimizations" to "about 60% (9 of 15, CI 36–80%)"; 12/18 only as the replayed-sequence figure | 03; 00; Q&A | applied |
| Soften | "the suite, not the selection rule, limits detection" to "coverage and oracle power" | 03 S2; 00 | applied |
| Soften | "Windows host load is the likely cause" to "cause unknown" | 03 S1 | applied |
| Soften | R1 given as stable loops plus tests, with setup volatile; 659–751 s is the fastest machine state seen | 03 story and S1; 00 | applied |
| Add | A/A power table summary, 3 of 49 heavy cases sampled, 1 + 3σ condition computed but not applicable to any reported verdict (deviation) | 03 S2, S7; A3 | applied |
| Add | Machine drift stated narrowly (one module's setup; about 1.7–3× within a protocol, about 10× only across protocols; cause unknown) | 03 S1, S7; 00; A12; Q&A N5 | applied |
| Add | Mining precision: 15 of 18 replayed edits are optimizations by subject (post hoc, one reader, not diff-checked), three routes named | 03 S2; Q&A N2 | applied |
| Add | Five likely questions on the new results (N1–N5) | Q&A | applied |
| Add | A13 rewritten (not validly tested; keep RQs; replication first, pivot decided after); A3 and A12 lines | 01 | applied |
| Sync | `knowledge-base/findings.md` rows B1, P3, P4, P5, S3, N7 | PM-owned, not this folder | for the PM |

## Reading order

| # | File | Use |
|---|---|---|
| 0 | [00-one-page-study-statement.md](00-one-page-study-statement.md) | Hand-out: problem, three RQs, scope, definitions, no AI |
| 1 | [01-agenda-and-asks.md](01-agenda-and-asks.md) | About 40-minute agenda and the decisions we need |
| 2 | [02-predicted-questions-and-answers.md](02-predicted-questions-and-answers.md) | N1–N5 (new results), Q1–Q5 (first five), P01–P20; each with a short answer, evidence links and a status |
| 3 | [03-results-summary.md](03-results-summary.md) | W3 PRELIMINARY draft results with W3 labels, the PM ruling on what may be shown, and what is still open |

## Background to bring

- [W1 one-pager](../01-literature/literature-in-one-page.md) and [closest works](../01-literature/closest-works.md)
- [W2 at-a-glance table](../02-practice-survey/README.md)
- [W3 readiness](../03-experiment/readiness.md)
- [Study 1 README](../README.md)
- [Advisor-meeting checklist](../pm/advisor/review-charter.md) (section 5) and the [TPM go/no-go rule](../pm/tpm-log.md)
