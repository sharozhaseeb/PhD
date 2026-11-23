# Study 1: one-page statement

**Status:** 2026-11-21, updated 2026-11-23 with W3's PRELIMINARY pilot results ([results summary](03-results-summary.md)). **No AI is used in the method.**

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
| Targets | Pilot: `networkx` (pure Python, asv benchmarks). C extension: `pydata/bottleneck` (four template-generated C extensions); main window = states 1–8 of the amended window (base `f51ed86`), states 9–13 held out because state 9 does not compile. One cost-only RQ1 measurement on scikit-learn was planned and is not reported | [readiness](../03-experiment/readiness.md) section 1.2; [W3 results](../03-experiment/results/results.md) |
| Edits | Real historical commits mined by a frozen regex rule, replayed one after another on one base tree. A replay, not a recorded session; no iterative-session effect is claimed | [readiness](../03-experiment/readiness.md) sections 1.3, 2 |
| "Build" | C or Cython extension compile, editable install and bytecode; dependency resolution excluded. The build share is measured per repo first; if it is under about 5%, report "build measured, negligible". Rule B0: a failed build is a reject, whatever the tests say | [TPM log](../pm/tpm-log.md), R1; [W3 results](../03-experiment/results/results.md) |
| Oracle | FULL validation (full build, tests, benchmarks) at every state | [readiness](../03-experiment/readiness.md) section 3 |

## What "valid" and "optimized" mean

- **Valid (functionally):** FULL validation is the oracle at every state ([readiness](../03-experiment/readiness.md) section 3). A reduced arm is judged by whether it catches what FULL catches. Safety is counted as **k of N frozen injected faults detected**, with a Wilson 95% interval, never as a general guarantee ([CHARTER](../pm/CHARTER.md) definitions; [readiness](../03-experiment/readiness.md) section 4.4).
- **Optimized (performance):** a regression is a slowdown beyond a stated threshold relative to the **original** code and to the previous accepted state, above the measured noise floor. The decision rule is the asv rule (ratio above 1.1 and Mann-Whitney p below 0.002, and above 1 + 3 sigma of the noise floor), fixed before runs; the 1 + 3 sigma part is now applied to the 12 flagged verdicts, where sigma was measured (σ exists only for those 12 and the 23 S0 A/A cases) ([readiness](../03-experiment/readiness.md) sections 4.2, 5; the asv source was read on 2026-11-22, see [results.md](../03-experiment/results/results.md) "Exact-test recompute").

## What the study contributes (as measurements)

*Original framing, from W1. The preliminary results below may shift the lead to the oracle gap (B1); see ask A13.*

Where existing deterministic reduction becomes unsafe for performance-motivated, accumulating edits: native-extension boundary (C5), stale dependency data (C7), dropped benchmarks (C11), incremental-rebuild correctness (C8). The RQ3 policy follows from these. Details and searches: [claims](../01-literature/beyond-literature-claims.md), [one-pager](../01-literature/literature-in-one-page.md). Not claimed: a better test selector, per-edit selection in optimization loops (PerfAgent), periodic full runs, batching.

## Preliminary results (pilot; details and labels in the [results summary](03-results-summary.md))

- **Benchmarks dominate per-edit cost on two projects.** networkx: 659–2,984 s per FULL benchmark pass over 9 passes, at least about 8×, median about 14×, up to about 34× build plus serial tests (8 of 9 passes noisy). The timing loops (132–171 s) are stable; most of a pass is per-process setup in one module, which caching, not selection, would reduce (setup-cached estimate about 1.5–2×, not measured; E5 runs the night of 23→24). bottleneck: about 18.5–19× (two passes, 0.5% apart). Build is a minor lever: 0.8–0.9% of bottleneck's total once benchmarks count.
- **The benchmark oracle often cannot see the edit (networkx): executed, visible, detectable.** 8 of 14 agent-labelled optimizations are executed by no benchmark (57%, Wilson 33–79%). At a 1.2× slowdown of the changed function at most 4 of 14 edits can even clear asv's 1.1 ratio (share of case time). Above the pre-registered noise floor FULL detects 1 of 10 frozen slowdowns (2 by asv's rule alone). Pre-registered result: regression safety of reduced selection is not measurable with the frozen set. B1 is a networkx-only finding; Traini et al. (2021) is the closest method precedent.
- **Functional selection:** testmon is 3.5–4× cheaper than FULL end to end (mixed load) and misses 0/20 frozen mutants (95% Wilson 0–16.1%; frozen mutants filtered by FULL; simulated; caught almost by construction; not a safety guarantee).
- **Policy (A4):** the fault model cannot tell selection rules apart (design limitation); A4 as implemented costs more than testmon and, with benchmarks counted, about 2× batching (finding B2).
- **Noise and repeatability:** σ measured for the 12 flagged verdicts; 12 of 14 verdicts repeat; a second repeat found 2.2% off-target flips with edit and clone directory confounded, so a directory A/A and directory rotation start tonight. Per-pass cost drifts for unknown reasons.
- **Labels:** the 14 optimization labels come from agents only (two raters plus an adjudicator; mining precision 71% pooled). Whether a human-labelled subset is needed is an open question for the meeting (ask A14).
- **Paper draft:** [main.pdf](../04-paper/build/main.pdf), 14 pages; advisor-persona verdict (AI-SIM): right story, wrong size (PM's summary, [WORKLOG](../knowledge-base/WORKLOG.md) 16:52) until the replication E1 reaches at least 4–5 projects and 50–60 true optimizations.

## What Study 1 hands to Study 2

[CHARTER](../pm/CHARTER.md): AI-based selection is a later study; Study 1 "sets the deterministic baseline and its limits". The concrete hand-off is **not decided**. An AI-written proposal exists (rules, benchmark harness and a measured cost/safety frontier; [review-charter](../pm/advisor/review-charter.md) section 2, Q10). Open: a question for the advisor ([asks](01-agenda-and-asks.md), A9).

## Status

W1 final, W2 final draft, W3 PRELIMINARY pilot results (2026-11-23); paper draft built 2026-11-23. The noise floor is applied to the flagged verdicts; what is shown follows the [TPM go/no-go rule](../pm/tpm-log.md) and the PM rulings recorded in the [results summary](03-results-summary.md).
