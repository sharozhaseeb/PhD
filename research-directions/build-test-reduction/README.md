# Study 1: reduced build and test validation for iterative code optimization

**Status:** 2026-11-21, updated 2026-11-23. W1 literature v3.2 is final for the meeting. W2 practice survey is a final draft, critic-checked. W3 experiment has readiness v1.1 and PRELIMINARY pilot results ([results.md](03-experiment/results/results.md)); W3's night runs are done (noise floor applied, oracle repeatability, drift passes, bottleneck cost); a directory A/A and the setup-cached pass E5 run tonight. Advisor meeting about 2026-11-23/24. Nothing in this folder is advisor-approved; the latest edits are not committed.

**Evidence boundary.** W1 and W2 are targeted primary-source reviews, not systematic reviews; their claims carry [R]/[src] read in source, [I]/[inf] inferred, [U]/[unk] unknown labels. W3 numbers exist only with a command, raw file, target repo SHA and harness SHA ([readiness](03-experiment/readiness.md)). Statements about the advisor use the persona labels (REAL, OWNER, AI-SIM, INFER, UNKNOWN; [persona](pm/advisor/persona.md)). All advisor "reviews" in `pm/advisor/` are AI-written rehearsals, not the advisor's opinion. Novelty means only "not found in our recorded searches".

## The study in one paragraph

When code is optimized through many small edits, each edit is re-validated: build, tests, and a check that the speed-up is real and nothing regressed. A full build plus full tests plus full benchmarks after every edit is slow. Study 1 asks how to validate each edit with a **reduced build** and a **reduced test/benchmark set**, chosen by **deterministic rules, with no AI**, and how far that can be trusted. AI-based selection is a later study ([CHARTER](pm/CHARTER.md), "Problem").

## Research questions (revised 2026-11-21)

From [CHARTER](pm/CHARTER.md). The older four-question list in that file is history only. Background chapters, not RQs: how optimization systems validate candidates (W2) and what deterministic reduction techniques exist (W1).

- **RQ1 Cost.** On real projects, what share of per-edit validation time goes to build, tests and benchmarks, and how does it accumulate over a sequence of optimization edits?
- **RQ2 Existing techniques, unchanged.** Applied to optimization edit sequences, how much end-to-end time do incremental builds and regression test selection (pytest-testmon, changed-module rule) save, including their own overhead, and how many functional failures and performance regressions do they miss, and why?
- **RQ3 New deterministic policy.** Does a policy using (a) changes accumulated since the last full check, (b) profile/call-graph-based benchmark selection, and (c) a full check triggered by accumulated change, miss fewer failures and regressions than the best existing combination at matched cost? Ablate each part.

**Definitions fixed before runs:** a *performance regression* is a slowdown beyond a stated threshold relative to the **original** code (and to the previous accepted state), above the measured noise floor. *Safe* means k of N frozen injected faults or regressions detected, reported with a confidence interval, never a general guarantee.

## How to read

1. [W1 one-pager](01-literature/literature-in-one-page.md): what the literature says and the four mechanisms Study 1 measures (about 5 minutes).
2. [W1 README](01-literature/README.md): the answer to "what is new compared with Ekstazi, STARTS, testmon and incremental builds?"
3. [W2 README](02-practice-survey/README.md): the at-a-glance table of how optimizers validate each candidate.
4. [W3 readiness](03-experiment/readiness.md): experiment design, arms, safety measurement, threats, schedule.
5. W3 results (PRELIMINARY draft): [results.md](03-experiment/results/results.md), condensed with the PM's show rules in [03-results-summary.md](meeting-2026-11-advisor/03-results-summary.md).

For the meeting itself, start at the [meeting pack](meeting-2026-11-advisor/README.md).

## Folder map

| Folder | Content | State |
|---|---|---|
| [`01-literature/`](01-literature/README.md) | W1: methods literature, closest works, beyond-literature claims, search log, 138 references (W1 README still says 136) and 72 open-access PDFs | v3.2, final for the meeting |
| [`02-practice-survey/`](02-practice-survey/README.md) | W2: how 28 systems build and verify each candidate; findings F1–F7; per-system notes; critic logs | Final draft (its README still says "draft 2026-11-21") |
| [`03-experiment/`](03-experiment/readiness.md) | W3: [readiness](03-experiment/readiness.md), [rules](03-experiment/rules.md), [harness spec](03-experiment/docs/harness-spec.md), configs, frozen edit lists, scripts, tests, [raw outputs](03-experiment/results/raw/), [results.md](03-experiment/results/results.md) | PRELIMINARY pilot results; noise floor applied (FULL detects 1 of 10), 12/14 verdicts repeat, 2.2% off-target flips with a directory confound open |
| [`pm/`](pm/CHARTER.md) | [Charter](pm/CHARTER.md), [TPM log](pm/tpm-log.md), advisor model and reviews in [`pm/advisor/`](pm/advisor/persona.md), [working notes](pm/working-notes/README.md) | Live |
| [`meeting-2026-11-advisor/`](meeting-2026-11-advisor/README.md) | Meeting pack: study statement, agenda and asks, predicted questions, W3 results summary, paper draft | Written 2026-11-21, updated 2026-11-23 |

## What is claimed and not claimed

**Claimed (as measurements W3 must produce; PRELIMINARY measurements now exist for C7, C8 and B1/C11, see the [results summary](meeting-2026-11-advisor/03-results-summary.md)).** Study 1 measures where existing deterministic build and test reduction becomes unsafe when edits are performance-motivated and accumulate. Four suspected mechanisms ([one-pager](01-literature/literature-in-one-page.md), [claims](01-literature/beyond-literature-claims.md)):

| Claim | Mechanism | Search status in the claims file |
|---|---|---|
| C5 | Native-extension boundary: coverage sees Python lines only | No Python measurement found |
| C7 | Stale dependency data across a chain of edits | No measurement found; one 2009 paper narrows it (see open items) |
| C11 | Dropped benchmarks: coverage of the change is not enough | No per-edit miss rate for Python found |
| C8 | Incremental rebuild correctness for Python extensions | No Python-extension study found |

Supporting claims: C1 (narrowed), C6, C3, C2. Struck: C4, C9, C10 (reasons in the claims file). The RQ3 policy follows from the four mechanisms. Its trigger is conceded to be a model-free variant of risk-mass batching (Sayedsalehi et al. 2026).

**Not claimed** (from the [one-pager](01-literature/literature-in-one-page.md) and the [TPM log](pm/tpm-log.md), "Must not be claimed"):

- A better test selector. Per-edit test selection in optimization loops (PerfAgent). A two-sided "faster and no regression" gate (SemOpt, PerfAgent). Periodic full runs (Meta, Google). Batching, bisection, variable or risk-based batch size. Comparison against a stable baseline. Culprit finding (deferred).
- That reduced validation is "safe" or has "no misses" as a general property. Only "k of N injected faults missed (95% CI) on these repos".
- Generalisation beyond the 1–2 repos, the edit sample, or the laptop hardware.
- Wall-clock speed-ups, or regression detection below the measured noise floor. Confirmation of the historical commits' speed-ups unless re-measured.
- Build-time savings for Python unless the build was defined and measured as non-negligible.
- A "session" or iterative-accumulation effect from parent-to-child replay of non-adjacent commits.
- Anything about AI-based selection.
- Novelty beyond "not found in our recorded searches".

## Open items

| Item | State | Where |
|---|---|---|
| ACM DL and IEEE Xplore searches | Scripted access was blocked on 2026-11-21 (HTTP 403 / 418); the queries are recorded in [gap-and-search-log.md](01-literature/gap-and-search-log.md) for a manual run. A later manual run in the student's Chrome is recorded in [database-search-2026-11-21.md](01-literature/database-search-2026-11-21.md): 123 records screened, none anticipates C1, C5, C8 or C11 as stated, and Chittimalli and Harrold (TSE 2009) narrows C7. W1 v3.2 (README, one-pager, gap log) now records this run | Closed (W1 v3.2) |
| NameRTS comparator | Not run by anyone here. Public replication package; planned as a post-meeting comparator | [W1 README](01-literature/README.md), [readiness](03-experiment/readiness.md) section 3 |
| W3 results | PRELIMINARY pilot results for networkx (RQ1, RQ2, draft RQ3, slowdown oracle) and bottleneck (build cost, `iterators.h` hazard). Updated 2026-11-23: R1 on two projects, B1 8/14 on agent labels (networkx only), noise floor applied (FULL detects 1 of 10), 12/14 verdicts repeat, directory confound open; paper draft in [`04-paper/`](04-paper/README.md) ([PDF](04-paper/build/main.pdf)) | [results.md](03-experiment/results/results.md), [OVERNIGHT.md](03-experiment/results/OVERNIGHT.md) |
| W3 environment | The readiness v1.1 blocker (no `pip`, `venv` or `Python.h` in WSL) is superseded: results use uv-managed CPython 3.12.16 (networkx) and 3.8.20 (bottleneck) | [results.md](03-experiment/results/results.md) "Platform"; [rq1_bottleneck_build.md](03-experiment/results/rq1_bottleneck_build.md) |
| Compiled-project build cost | bottleneck clean build measured at about 16-18% of build plus tests on the amended base (noisy). The scikit-learn cost-only measurement planned in readiness is not reported in the results files | [readiness](03-experiment/readiness.md) section 1.2 |
| bottleneck on a 2019–20 toolchain | May need an older interpreter; compatibility patches would be logged (threat T7) | [readiness](03-experiment/readiness.md) section 1.2, 6 |
| Accumulation ablation may be null | Expected null unless at least 3 latent faults per repo exist | [readiness](03-experiment/readiness.md) section 4.1b |
| Oracle repeatability | Done in part: E3 tier 1 (4 repeats, 12/14 agree) and tier 2 (2 repeats); the directory confound needs the directory A/A (tonight) | [readiness](03-experiment/readiness.md) section 5 |
| BISCEPTER (culprit finding) | Not read; C10 struck, deferred out of Study 1 | [review-w1-v2](pm/advisor/review-w1-v2.md) |
| Advisor decisions | No first-hand advisor record exists; open decisions are listed in the [agenda and asks](meeting-2026-11-advisor/01-agenda-and-asks.md) | [persona](pm/advisor/persona.md) sections 5–7 |
| Venue, timeline, SPARK fit | UNKNOWN | [persona](pm/advisor/persona.md) sections 6–7 |
