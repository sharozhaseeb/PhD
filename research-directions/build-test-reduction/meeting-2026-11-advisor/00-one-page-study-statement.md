# Study 1: one-page statement

**Status:** 2026-11-21, updated 2026-11-22 with W3's PRELIMINARY pilot results ([results summary](03-results-summary.md)). **No AI is used in the method.**

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
- **Optimized (performance):** a regression is a slowdown beyond a stated threshold relative to the **original** code and to the previous accepted state, above the measured noise floor. The decision rule is the asv rule (ratio above 1.1 and Mann-Whitney p below 0.002, and above 1 + 3 sigma of the noise floor), fixed before runs; the 1 + 3 sigma part could not be applied to any reported verdict, because sigma exists for only 23 of 171 cases (deviation recorded) ([readiness](../03-experiment/readiness.md) sections 4.2, 5; asv defaults still to be verified by file and commit).

## What the study contributes (as measurements)

*Original framing, from W1. The preliminary results below may shift the lead to the oracle gap (B1); see ask A13.*

Where existing deterministic reduction becomes unsafe for performance-motivated, accumulating edits: native-extension boundary (C5), stale dependency data (C7), dropped benchmarks (C11), incremental-rebuild correctness (C8). The RQ3 policy follows from these. Details and searches: [claims](../01-literature/beyond-literature-claims.md), [one-pager](../01-literature/literature-in-one-page.md). Not claimed: a better test selector, per-edit selection in optimization loops (PerfAgent), periodic full runs, batching.

## Preliminary results (pilot; details and labels in the [results summary](03-results-summary.md))

- **Benchmarks dominate cost:** the stable parts are timing loops of 132–171 s per pass and tests of 71–89 s per edit; on top comes setup that is large, volatile and cacheable. Whole passes took 659–2444 s (the 659–751 s passes are the fastest machine state seen), about 8–28× build plus serial tests; 87–96% of a pass is one module's 49 cases (including their loops; 80–94% of a pass is outside the timing loops), mostly setup, which caching, not selection, would reduce (cached estimate about 1.5–2×, not measured). Build is 1.19–2.11% of test time on networkx and about 16–18% of clean build plus full tests on bottleneck (noisy).
- **The oracle gap, coverage and power, not the selection rule, limits regression detection on networkx:** for 9 of 15 true optimizations (about 60%, Wilson 36–80%; 4 of 15 by static call graph; 3 of the 18 replayed edits are not optimizations) and 7 of 10 frozen slowdowns are executed by no benchmark (S0 profiles); FULL detects at most 3 of 10 slowdowns (2 on target, 0 in the pre-set bands). Pre-registered result: regression safety is not measurable with the frozen set. B1 is a networkx-only finding; it was not validly tested elsewhere (W3 Q3). A pre-registered replication is proposed as the first step after the meeting.
- **Functional selection:** testmon is 3.5–4× cheaper than FULL end to end (mixed load) and misses 0/20 frozen mutants (95% Wilson 0–16.1%; frozen mutants filtered by FULL; simulated; caught almost by construction; not a safety guarantee). 
- **Policy (A4):** the functional fault model cannot tell selection rules apart (design limitation); A4 as implemented costs more than testmon and, with benchmarks counted, about 2× batching (depends on unfinished checkpoint re-profiling, B2). Latent fault class empty (0/5); the pre-registered null for accumulation stands.
- **Build:** reduced build is a minor lever here. Harness lesson: an incremental tree hid a failed compile on one replayed state (a replay artefact); rule B0 (a failed build is a reject) is kept.
- **Noise:** the benchmark A/A floor gives 0 false verdicts in 46 A/A comparisons (Wilson upper bound 7.7%, optimistic), noise close to the threshold, only about 2× slowdowns reliably caught on 2 of the 3 sampled `benchmark_algorithms` cases (3 of the module's 49; optimistic bootstrap), and one module's per-process setup (`benchmark_algorithms`) drifted about 1.7–3× within a protocol during the day (about 10× only across protocols), while timing loops, timed samples and tests stayed stable; cause unknown, so benchmark verdicts stay provisional. The profile-completeness check flags 1 of 50 out-of-reach comparisons (#9); a re-check did not confirm it, and the flag stands.

## What Study 1 hands to Study 2

[CHARTER](../pm/CHARTER.md): AI-based selection is a later study; Study 1 "sets the deterministic baseline and its limits". The concrete hand-off is **not decided**. An AI-written proposal exists (rules, benchmark harness and a measured cost/safety frontier; [review-charter](../pm/advisor/review-charter.md) section 2, Q10). Open: a question for the advisor ([asks](01-agenda-and-asks.md), A9).

## Status

W1 final, W2 final draft, W3 PRELIMINARY pilot results. A benchmark A/A noise floor exists, with limits; what is shown follows the [TPM go/no-go rule](../pm/tpm-log.md) and the PM rulings recorded in the [results summary](03-results-summary.md).
