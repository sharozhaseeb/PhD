# Agenda and asks

**Status:** 2026-11-21. Proposed 40-minute agenda. The asks come from the advisor model's open questions ([persona](../pm/advisor/persona.md) section 6), the should-have "decisions needed" item in the [meeting checklist](../pm/advisor/review-charter.md) (section 5) and scope items in the [TPM log](../pm/tpm-log.md). "Current position" is our position, not an advisor decision; no advisor decision is recorded anywhere in the repository ([persona](../pm/advisor/persona.md) section 1).

## Agenda (about 40 minutes)

| Min | Item | Material |
|---|---|---|
| 0–5 | Problem and the three RQs; no AI in Study 1 | [statement](00-one-page-study-statement.md) |
| 5–12 | What is new compared with Ekstazi, STARTS, testmon and incremental builds; what we do not claim | [W1 one-pager](../01-literature/literature-in-one-page.md), [closest works](../01-literature/closest-works.md) |
| 12–17 | How optimizers validate each candidate today | [W2 at-a-glance table](../02-practice-survey/README.md) |
| 17–25 | Experiment design: targets, edits, oracle, arms, safety metric | [readiness](../03-experiment/readiness.md); results only if the go/no-go rule allows ([results summary](03-results-summary.md)) |
| 25–40 | Decisions below | This file |

## Decisions we need

| # | Question | Our current position (source) | Options |
|---|---|---|---|
| A1 | Language and project type: Python only, Python with compiled extensions, or include C/C++? | Python target, which is a charter choice and not an advisor decision. networkx (pure Python) plus bottleneck (C extension); one cost-only scikit-learn measurement for a heavy build ([persona](../pm/advisor/persona.md) section 5; [readiness](../03-experiment/readiness.md) section 1.2) | Python only (build share may be negligible); Python plus compiled extensions (current); add C/C++ projects where builds are expensive |
| A2 | Source of edit sequences | Real historical perf commits mined by a frozen rule and replayed in history order; not a real session ([readiness](../03-experiment/readiness.md) sections 1.3, 2; [persona](../pm/advisor/persona.md) section 6) | Current; decomposed commits applied hunk by hunk; recorded optimizer trajectories used as data, not as method |
| A3 | Definition of "stays optimized": oracle, threshold, baseline | Original code and previous accepted state, asv rule above the noise floor, fixed before runs ([CHARTER](../pm/CHARTER.md) definitions; [readiness](../03-experiment/readiness.md) section 4.2) | asv rule (current); SWE-Perf rule as a sensitivity check (planned); another threshold |
| A4 | Acceptable safety: zero missed failures, or a bounded miss rate caught by checkpoints | Report "k of N missed" with a Wilson interval; no general safety claim ([TPM log](../pm/tpm-log.md), "Must not be claimed") | Safe-RTS style zero misses; bounded misses between checkpoints with detection delay reported |
| A5 | What counts as Study 1's contribution | Lead with the empirical result on where existing reduction becomes unsafe (C5, C7, C11, C8); the policy follows from it ([W1 README](../01-literature/README.md); [review-w1-v2](../pm/advisor/review-w1-v2.md) reframing) | Empirical characterization; new deterministic technique; both |
| A6 | Scope of the pilot: 2 repos or 1 | Two repos. If networkx RQ1 plus RQ2 is not running end-to-end at hour 20, networkx only, labelled pilot; sqlglot is cut first ([readiness](../03-experiment/readiness.md) section 8; [TPM log](../pm/tpm-log.md)) | 2 repos; 1 repo labelled pilot; add a third |
| A7 | Is NameRTS a required baseline, and when? | Not run. Planned as a post-meeting comparator; testmon and a changed-module rule are the baselines now ([W1 README](../01-literature/README.md); [readiness](../03-experiment/readiness.md) section 3) | Require before any result is shown; after the meeting (current); cite only |
| A8 | Is the historical-replay limitation acceptable, or is a recorded optimizer session needed? | Replay is a sequence of independent commits re-based on one tree (threat T1); no session effect is claimed ([readiness](../03-experiment/readiness.md) sections 2, 6) | Accept as stated; add recorded sessions later |
| A9 | What Study 1 hands to Study 2 (AI) | Undecided. Charter: Study 1 sets the deterministic baseline and its limits. AI-written proposal: rules, harness and cost/safety frontier ([review-charter](../pm/advisor/review-charter.md) section 2, Q10) | Rules plus harness plus frontier; add a reusable benchmark of pinned projects and full-validation ground truth |
| A10 | Target venue and timeline for Study 1 | UNKNOWN; nothing recorded ([persona](../pm/advisor/persona.md) sections 6, 7). The W3 schedule covers the experiment only ([readiness](../03-experiment/readiness.md) section 8) | To be given by the advisor |
| A11 | Status of SPARK and whether Study 1 must fit it | UNKNOWN. The packet is ready for advisor discussion, not submission ([Spark Elevate README](../../../Spark%20Elevate/README.md); [persona](../pm/advisor/persona.md) section 6) | To be given by the advisor |
| A13 | Should Study 1's contribution pivot toward benchmark coverage of optimization edits (B1), given functional selection is solved by testmon on this data? | PM question raised by W3's PRELIMINARY results: 12 of 18 networkx edits are executed by no benchmark (S0 profiles); testmon missed 0/20 frozen mutants, which selection catches almost by construction (M2), with N = 20 ([results.md](../03-experiment/results/results.md) "Finding B1", "Fault detection") | Pivot toward benchmark coverage (B1); keep the three RQs and add B1 as an RQ1/RQ2 finding; wait for slowdown results |
| A12 | Compute and environment available | UNKNOWN beyond one laptop (WSL2, 6 cores, 7 GB RAM) ([persona](../pm/advisor/persona.md) section 7; [readiness](../03-experiment/readiness.md) sections 1.1, 5) | Laptop only (current); lab machine for timing-sensitive runs |

## Not for the advisor (owner items)

- W3 environment blocker: WSL needs `pip`, `venv` and `Python.h`; both options need the owner's approval ([readiness](../03-experiment/readiness.md) section 9). State after v1.1 is not recorded in this pack.
