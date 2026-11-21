# Study 1: one-page statement

**Status:** 2026-11-21, for the advisor meeting. No W3 results yet. **No AI is used in the method.**

## Problem

Optimizing code through many small edits means re-validating every edit: build, tests, and a check that the speed-up is real and nothing regressed. Full build plus full tests plus full benchmarks per edit is slow ([CHARTER](../pm/CHARTER.md), "Problem"; relayed by the student, OWNER). Study 1 asks how to validate each edit with a **reduced build** and a **reduced test/benchmark set** chosen by **deterministic rules**, and how far the result can be trusted.

## Research questions (revised 2026-11-21)

- **RQ1 Cost.** What share of per-edit validation time goes to build, tests and benchmarks on real projects, and how does it accumulate over an edit sequence?
- **RQ2 Existing techniques, unchanged.** How much end-to-end time do incremental builds and regression test selection (pytest-testmon, changed-module rule) save, including their own overhead, and how many functional failures and performance regressions do they miss, and why?
- **RQ3 New deterministic policy.** Does a policy using (a) changes accumulated since the last full check, (b) profile/call-graph-based benchmark selection and (c) a full check triggered by accumulated change miss fewer failures and regressions than the best existing combination at matched cost? Ablate each part.

How optimizers validate candidates (W2) and what reduction techniques exist (W1) are background chapters, not RQs.

## Scope

| Item | Decision on paper | Source |
|---|---|---|
| Targets | Pilot: `networkx` (pure Python, asv benchmarks). C extension: `pydata/bottleneck` (17 `PERF:` commits in one burst 2019-09 to 2020-11; four template-generated C extensions). Third, cut first: `sqlglot`. One cost-only RQ1 measurement on scikit-learn is planned | [readiness](../03-experiment/readiness.md) section 1.2 |
| Edits | Real historical commits mined by a frozen regex rule, replayed one after another on one base tree. A replay, not a recorded session; no iterative-session effect is claimed | [readiness](../03-experiment/readiness.md) sections 1.3, 2 |
| "Build" | C or Cython extension compile, editable install and bytecode; dependency resolution excluded. The build share is measured per repo first; if it is under about 5%, report "build measured, negligible" | [TPM log](../pm/tpm-log.md), R1 |
| Oracle | FULL validation (full build, tests, benchmarks) at every state | [readiness](../03-experiment/readiness.md) section 3 |

## What "valid" and "optimized" mean

- **Valid (functionally):** FULL validation is the oracle at every state ([readiness](../03-experiment/readiness.md) section 3). A reduced arm is judged by whether it catches what FULL catches. Safety is counted as **k of N frozen injected faults detected**, with a Wilson 95% interval, never as a general guarantee ([CHARTER](../pm/CHARTER.md) definitions; [readiness](../03-experiment/readiness.md) section 4.4).
- **Optimized (performance):** a regression is a slowdown beyond a stated threshold relative to the **original** code and to the previous accepted state, above the measured noise floor. The decision rule is the asv rule (ratio above 1.1 and Mann-Whitney p below 0.002, and above 1 + 3 sigma of the noise floor), fixed before runs ([readiness](../03-experiment/readiness.md) sections 4.2, 5; asv defaults still to be verified by file and commit).

## What the study contributes (as measurements)

Where existing deterministic reduction becomes unsafe for performance-motivated, accumulating edits: native-extension boundary (C5), stale dependency data (C7), dropped benchmarks (C11), incremental-rebuild correctness (C8). The RQ3 policy follows from these. Details and searches: [claims](../01-literature/beyond-literature-claims.md), [one-pager](../01-literature/literature-in-one-page.md). Not claimed: a better test selector, per-edit selection in optimization loops (PerfAgent), periodic full runs, batching.

## What Study 1 hands to Study 2

[CHARTER](../pm/CHARTER.md): AI-based selection is a later study; Study 1 "sets the deterministic baseline and its limits". The concrete hand-off is **not decided**. An AI-written proposal exists (rules, benchmark harness and a measured cost/safety frontier; [review-charter](../pm/advisor/review-charter.md) section 2, Q10). Open: a question for the advisor ([asks](01-agenda-and-asks.md), A9).

## Status

W1 final, W2 final draft, W3 readiness v1.1 and harness in progress, results pending. Nothing below the [TPM go/no-go rule](../pm/tpm-log.md) is shown without a noise floor and injection-based miss counts.
