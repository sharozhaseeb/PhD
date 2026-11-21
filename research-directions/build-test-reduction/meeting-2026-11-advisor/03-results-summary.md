# W3 results summary (PRELIMINARY)

**Status:** 2026-11-21, filled from W3's draft results ([results.md](../03-experiment/results/results.md), status line "PRELIMINARY, 2026-11-21 19:40 PKT. Partial data; numbers change as runs finish"). Every number below is copied from the W3 file cited next to it. W3's labels are kept: **PRELIMINARY**, **concurrent**, **noisy**, **lower bound**, **estimate**. Nothing here is new analysis. Overnight runs ([OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md)) will replace several of these numbers.

**Evidence boundary.** One pure-Python project (networkx, 18 replayed edits) and one C-extension project (bottleneck, setup probes only). Single runs on one laptop: WSL2 Ubuntu 24.04, i5-12400F, 7 GB, CPython 3.12.16 for networkx and 3.8.20 for bottleneck ([results.md](../03-experiment/results/results.md) "Platform"; [rq1_bottleneck_build.md](../03-experiment/results/rq1_bottleneck_build.md)). Costs are counts and estimated seconds; wall times are single runs. Each raw JSON carries the target state SHA and the harness tree hash ([results.md](../03-experiment/results/results.md) status line).

## Do-not-show rule (TPM go/no-go): current state

The TPM rule: do not show any W3 number without the A/A noise floor and the injection-based miss counts ([TPM log, go/no-go](../pm/tpm-log.md)).

| Requirement | State now | Source |
|---|---|---|
| Injection-based miss counts, functional | **Present:** 20 frozen mutants killed by FULL, misses per arm with Wilson CI | [results.md](../03-experiment/results/results.md) "Fault detection" |
| Injection-based miss counts, performance | **Pending:** 10 frozen slowdowns queued overnight | [OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md) item 2 |
| A/A noise floor, benchmarks | **Not yet.** No A/A benchmark noise-floor run exists or is queued; the oracle-repeatability rule is also "not in this queue" | [OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md) (queue items 1-4 and last line) |
| Timing noise, tests | Partial: a post-hoc `timing_label` rule marks S16 noisy and S17 borderline. It was **written after the first look at S16/S17**, so it is not pre-registered | [results.md](../03-experiment/results/results.md) "timing_label rule" |

The TPM rule as written is not met for any W3 number, because the A/A noise floor does not exist. The PM made the following exception.

**PM ruling (2026-11-21, applied here):**
- Functional miss counts may be shown as k/N with the Wilson CI, labelled "frozen mutants filtered by FULL; not a safety guarantee", together with W3's honest reading (construction bias M2).
- No benchmark A/A noise floor exists yet, so this pack makes **no speed-up, slowdown or regression-detection claim from benchmarks**. Benchmark numbers appear only as a **cost lower bound** (import-only, concurrent).
- Slowdown detection stays "pending ([OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md))".

All W3 numbers here are a **pilot**: networkx n = 18 replayed edits, 20 frozen mutants; bottleneck setup probes only.

Also not to be claimed ([TPM log, "Must not be claimed"](../pm/tpm-log.md)): "safe" or "no misses" as a general property; generalisation beyond the 1-2 repos, the edit sample or the laptop hardware; wall-clock speed-ups or perf-regression detection below the measured noise floor; confirmation of the historical commits' speed-ups unless re-measured; build-time savings for Python unless build was defined and measured as non-negligible; novelty for the accumulation, profile or checkpoint ideas before W1's recorded search; an iterative-session effect from replay of non-adjacent commits; anything about AI-based selection.

## Headline findings (W3's wording, condensed)

1. **B1: most replayed optimizations are not executed by any benchmark** (counts from S0 profiles; not a timing). For **12 of the 18 edits** (steps 1, 2, 5–8, 11–13, 15, 17, 18), the S0 profile of no benchmark case executes any function the edit changed (module-level lines excluded); the other 6 edits are executed by 1–8 cases. W3's reading: "even FULL benchmarking cannot confirm the claimed speed-up of most of these commits with the project's own suite". No speed-up or regression verdict is implied (no A/A noise floor yet) ([results.md](../03-experiment/results/results.md) "Finding B1"; raw `results/raw/networkx/profile/S0_181f2951.json`).

2. **Build is negligible in networkx, not in bottleneck.** networkx `pip install -e` is 1.19–2.11% of serial test time over the clean states. A bottleneck clean build is about 22% of clean build plus full tests, before benchmarks (**noisy** single runs; [results.md](../03-experiment/results/results.md); [rq1_bottleneck_build.md](../03-experiment/results/rq1_bottleneck_build.md)).
3. **Benchmarks dominate cost** (cost lower bound only; import-only, concurrent). An import-only **lower bound** puts one FULL benchmark pass on networkx at 0.89–4.45 h, against about 87 s for build plus serial tests: about **40–180×** ([results.md](../03-experiment/results/results.md) "RQ1 headline").
4. **End to end, testmon is about 4× cheaper than FULL**: 404 s measured (**concurrent, pinned**) against 1634 s measured for FULL serial tests plus build over S1–S18 (serial, 17 clean + 1 noisy state). Test-seconds alone suggest 15× (85 against 1279) ([results.md](../03-experiment/results/results.md) "RQ2/RQ3").
5. **Functional detection** (frozen mutants filtered by FULL; not a safety guarantee; simulated; selection catches these almost by construction (M2); N = 20 means a miss rate below 16.1% at 95%, not "safe"): 0/20 missed by every arm except the changed-module rule (2/20). At equal detection plain testmon is the cheapest; "our policy's extra cost buys no extra functional detection". Its possible value is in the pending items ([results.md](../03-experiment/results/results.md) "Fault detection"; [rq2_steps.csv.summary.csv](../03-experiment/results/sim/networkx/rq2_steps.csv.summary.csv)).
6. **Latent faults: 0/5.** None of the 5 mutants that survive FULL becomes detectable at any later state, so the **pre-registered null stands**: on networkx the accumulation component is expected to show no effect, reported as such, not as evidence for or against accumulation ([results.md](../03-experiment/results/results.md) "Latent re-check").
7. **B2: profile selection collapses to all benchmarks without checkpoint re-profiling** (a design gap, not a selection result). See S3.
8. **C7:** 62 of 2589 functions (2.4%) at S0 are attributed to different test sets in repeat runs of the same code ([results.md](../03-experiment/results/results.md) "C7 finding").

## S1. RQ1: cost split per edit

**networkx (pure Python), FULL, 19 states** ([rq1_networkx.csv](../03-experiment/results/rq1_networkx.csv); [results.md](../03-experiment/results/results.md) "RQ1"):

| Component | Value | Label |
|---|---|---|
| Build (`pip install -e . --no-deps --no-build-isolation`) | median 1.19 s; 1.19–2.11% of serial test time | measured, single runs |
| Tests (6771, serial, no xdist) | median 85.7 s per edit, range 75.4–119.2 s over clean states; all pass at every state | measured, single runs; 18 clean, 1 noisy (S16) |
| pytest collection/startup | about 13–21 s of each run | measured |
| Benchmarks (171 asv cases, 5 processes × 3 values + 1 warmup), **cost only** | at least 0.89 h (1 process), 1.78 h (2, asv default), 4.45 h (5, our protocol) per pass | **estimate, lower bound** (import cost only); the run completed 8 of 171 cases in 2360 s **concurrent (CPU-pinned)** and was stopped |
| Session total, tests only | 1700 s (about 28 min) for base plus 18 edits | measured |

Cause of benchmark cost: importing `benchmarks/benchmark_algorithms.py` takes 65–71 s and holds 49 of the 171 cases; asv-style process isolation repeats the import ([results.md](../03-experiment/results/results.md); raw `results/raw/networkx/bench/import_times_S0.txt`).

**bottleneck (C extension), build probes** ([rq1_bottleneck_build.md](../03-experiment/results/rq1_bottleneck_build.md); labelled **noisy**, single runs under `nice -n 19` beside other timing runs):

| Probe | Rebuilt | Wall (s) |
|---|---|---|
| Clean build | all 4 `.so` | 9.90 |
| One template edit (`reduce_template.c`) | `reduce.so` | 2.64 |
| Shared header in `depends=` (`bottleneck.h`) | all 4 `.so` | 4.86 |
| Header not in `depends=` (`iterators.h`) | **nothing** | 0.20 |
| Null rebuild | nothing | 0.20 |
| Full test suite, same state | 168 passed | 34.4 |

The `iterators.h` probe is a stale-build mechanism (C8). It is a **historical upstream bug, fixed in 2019** (`52f6cd1`), not an open bug; the amended replay window's base already contains the fix. The consequence study is pending ([rq1_bottleneck_build.md](../03-experiment/results/rq1_bottleneck_build.md); [OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md) item 3).

**Still TODO (W3):** idle re-timing of all networkx states and bottleneck builds; the measured FULL benchmark pass at S0, which replaces the lower bound ([OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md) items 1, 1b, 4). The scikit-learn cost-only measurement in readiness §1.2 is not reported in these files.

Answers [P01](02-predicted-questions-and-answers.md), [P03](02-predicted-questions-and-answers.md).

## S2. RQ2: arms table (networkx, 18 edits, DRAFT: tests only)

Costs exclude benchmarks ("Benchmarks **not** included in these totals"). Est. end-to-end = est. test-s + build + 13.6 s pytest startup per step that runs a test. Calibration: est. 1548 s against 1634 s measured for FULL ([results.md](../03-experiment/results/results.md); table source `rq2_networkx.csv`).

| Arm | Tests run (Σ) | Est. test-s | Est. end-to-end s | Measured end-to-end s | Missed (k/N) | 95% Wilson CI |
|---|---|---|---|---|---|---|
| A0 FULL | 121 824 | 1278.8 | 1548 | 1634 (serial, 17 clean + 1 noisy state) | 0/20 | 0–16.1% |
| A1 incremental build | 121 824 | 1278.8 | 1524 | — | 0/20 | 0–16.1% |
| A2 testmon (PerfAgent-style) | 3 583 | 85.3 | 330 | 404 (**concurrent, pinned**) | 0/20 | 0–16.1% |
| A3 changed-module | 461 | 3.6 | 221 | — | **2/20** | 2.8–30.1% |
| A5 static benchmark rule (testmon tests) | 3 583 | 85.3 | 330 | — | 0/20 | 0–16.1% |

*Frozen mutants filtered by FULL; not a safety guarantee.* Miss counts: [rq2_steps.csv.summary.csv](../03-experiment/results/sim/networkx/rq2_steps.csv.summary.csv) and [results.md](../03-experiment/results/results.md). Note: that summary file's `total_cost_s` column is not the end-to-end figure (it excludes pytest startup and benchmarks); use the table above ([results.md](../03-experiment/results/results.md) "Note on `sim/networkx/rq2_steps.csv.summary.csv`").

- **Fault set.** 25 frozen mutants placed in the function each step changes; 20 killed by FULL, so N = 20. The 5 survivors are not counted as misses; the latent re-check found 0 of them detectable later (see S3).
- **Why missed (A3).** Both misses are the name rule failing to map test files to modules: `isomorph.py::fast_could_be_isomorphic` (tests in `test_isomorphism.py`) and `katz.py::katz_centrality_numpy` (tests in `test_katz_centrality.py`). Any periodic full check catches both at the next checkpoint.
- **Construction bias (TPM M2), stated by W3:** "On this fault class, selection catches almost everything by construction". The arms differ only in cost.
- **testmon caveat:** detection is simulated from testmon's clean-replay selection; real testmon runs with each mutant present are not done.
- **testmon's own overhead:** its first run at S0 (database build) took 279.7 s against 88.0 s plain (3.2×).
- **Performance-regression misses:** pending ([OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md); 10 frozen slowdowns, [OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md) item 2), reported as "within reach" plus an out-of-reach spot check, never as a plain miss rate.

Answers [P04](02-predicted-questions-and-answers.md), [P13](02-predicted-questions-and-answers.md).

## S3. RQ3: policy, checkpoints and ablation (networkx, DRAFT)

*Frozen mutants filtered by FULL; not a safety guarantee.* From [results.md](../03-experiment/results/results.md) and [rq2_steps.csv.summary.csv](../03-experiment/results/sim/networkx/rq2_steps.csv.summary.csv):

| Arm | Est. end-to-end s | Full checks | Missed (k/N) | Caught by selection / full check / final |
|---|---|---|---|---|
| A2 + full every k=5 | 594 | 4 | 0/20 | 15 / 4 / 1 |
| A2 + full every k=3 | 735 | 6 | 0/20 | 14 / 5 / 1 |
| A3 + full every k=5 | 508 | 4 | 0/20 | 13 / 6 / 1 (mean delay 0.15 steps) |
| **A4 ours** (score trigger T=10 + final) | 655 | 5 | 0/20 | 14 / 5 / 1 |
| A4 − accumulation | 652 | 5 | 0/20 | 14 / 5 / 1 |
| A4 − F6-order | 655 | 5 | 0/20 | 14 / 5 / 1 |
| A4 with periodic k=5 | 633 | 4 | 0/20 | 15 / 4 / 1 |

- **A4 currently behaves like periodic full checks at k ≈ 4.** The trigger fired at steps 3, 5, 8 and 13 plus the final check, each time from a module-level edit. Its cost sits between A2 + k=5 and A2 + k=3. T is not retuned.
- **At equal detection (20/20) plain testmon is cheapest** (330 s est., 404 s measured, **concurrent, pinned**) against A4's 655 s est.
- **Accumulation** adds 494 test runs (+3 est. test-s) and changes no detection on this fault class. **Latent re-check: 0 of the 5 FULL survivors becomes detectable later**, so the pre-registered null stands; caller faults (class 2) were not generated in this draft ([results.md](../03-experiment/results/results.md)).
- **F6-order** changes nothing in this session: none of the 62 flagged functions is touched by a replayed edit or a frozen mutant.
- **Benchmark selection (counts only; S0 profiles measured, 171/171):**
  - **B2:** A4's profile rule (P8) may not use a profile older than the last full check, and only S0 profiles exist, so from step 3 on it selects 171/171 at every step. W3: "the rule working as written with a missing input, not a selection result"; checkpoint re-profiling (S3, S5, S8, S13) is not done.
  - A **labelled variant that violates P8** (reuses S0 profiles): A4 selects 889 cases in total (855 at its 5 full checks, 34 outside them), against A5 static reach 1893, A5 + k=5 2235 and FULL 3078.
  - Whether any of these selections misses a regression is pending (overnight slowdown oracle, [OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md)).

**Still TODO (W3):** caller faults, slowdown detection, checkpoint re-profiling, cap-only and additive-budget comparators ([OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md)).

Answers [P11](02-predicted-questions-and-answers.md), [P14](02-predicted-questions-and-answers.md), [P15](02-predicted-questions-and-answers.md), [P16](02-predicted-questions-and-answers.md).

## S4. Worked edit (networkx step 10)

Source: [worked-edit.md](../03-experiment/results/worked-edit.md) (PRELIMINARY), with a diagram there.

- **Edit:** `c1c468d5`, "Optimize _build_paths_from_predecessors stack logic for 30-40% speedup (#8460)" (upstream commit subject; the speed-up is not re-measured here), S9 → S10 (`52b7255a`). One changed function: `shortest_paths/generic.py::_build_paths_from_predecessors`.
- **Build:** FULL runs `pip install -e` (about 1.35 s); reduced arms skip it because the edit is pure Python (rule B1).

| Arm | Tests run | Est. end-to-end tests s | Benchmarks run |
|---|---|---|---|
| A0 FULL | 6768 | 85.99 | 171 |
| A2 testmon | 20 | 13.61 | 171 |
| A3 changed-module | 28 | 13.61 | 0 |
| A4 ours | 38 | 13.62 | pending |

- **Reading (W3):** test execution drops from about 71 s to about 0.02 s, but end to end the drop is about 86 s to about 14 s (about 6×), because pytest startup remains. Benchmarks are pending and would dominate cost; no benchmark verdict is shown.
- **Gap:** this is a pure-Python edit, so it does not show a reduced build. The planned bottleneck worked edit is not in these files.

Answers [P05](02-predicted-questions-and-answers.md).

## S5. Oracle repeatability and noise floor (TODO (W3))

- **Done so far:** single-run test timings with the post-hoc `timing_label` rule (S16 noisy, S17 borderline) ([results.md](../03-experiment/results/results.md)). C7 repeat depmaps show 2.4% of functions with nondeterministic test attribution, which is a repeatability result for the dependency map, not for the benchmark verdict.
- **Not done:** the A/A benchmark noise floor and the agreement rate of the full benchmark decision over repeats. [OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md) lists the oracle-repeatability rule as "not in this queue" (it needs the measured benchmark protocol ×3).
- Context (not a W3 result): full-benchmark verdicts do not repeat across machines in the literature (W2 headline 5; arXiv 2607.01211; [W2 README](../02-practice-survey/README.md)).

Answers [P20](02-predicted-questions-and-answers.md). Until this slot is filled, no performance verdict is shown.
