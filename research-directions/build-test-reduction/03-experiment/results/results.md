# W3 results — PRELIMINARY

> **Costs come from counts and estimated seconds. Functional misses are measured on 20 frozen mutants; performance-regression misses are pending. Benchmarks are not yet included in the per-arm totals.** (Benchmark cost is reported separately in RQ1, where it dominates.)

**Status: PRELIMINARY, 2026-11-21 20:00 PKT. Partial data; numbers change as runs finish.** Every number links to a raw file under `results/raw/`. Each raw JSON carries the target state SHA and the harness tree hash in its `meta` block. Design: `../readiness.md` (v1.1). Rules: `../rules.md`.

**Platform:** WSL2 Ubuntu 24.04 on an i5-12400F (6 cores / 12 threads, 7 GB), CPython 3.12.16 (uv-managed), packages in `raw/networkx/env-freeze.txt`. The CPU governor cannot be pinned in WSL (T4). Times are wall-clock from single runs; repeats come later.

## Status of each piece

| Piece | networkx | bottleneck |
|---|---|---|
| Edit list frozen | ✅ 20 commits (subject rule; see the readiness §1.3 correction) | ✅ window amended by the general reformat rule (readiness §1.3, Deviation 2; PM-approved 18:11) |
| Replay states | ✅ 18 applied, 2 dropped (apply conflicts) | ✅ 13 of 16 applied on the amended window (base `f51ed86`); the 5-edit replay is kept as a sensitivity row |
| RQ1 FULL cost per state | ✅ tests + build, 19 states; ⚠ FULL benchmark pass stopped as infeasible (8/171 cases in 2360 s); import-based lower bound reported; measured pass scheduled (`OVERNIGHT.md` item 4) | ✅ build probes (`rq1_bottleneck_build.md`); idle re-time scheduled (item 1b) |
| RQ2 counts per arm | ✅ test counts + test-seconds + end-to-end (18 steps, 16 arms); ✅ benchmark-selection counts (S0 profiles); ✅ functional safety; 🟡 benchmark seconds and regression safety (overnight) | — |
| Injected faults | ✅ 25 mutants frozen, 20 killed by FULL, detection simulated; ✅ latent re-check done: **0 of 5** survivors become detectable later (pre-registered null stands); 🟡 slowdowns (overnight item 2) | — |

## RQ1 headline — benchmarks dominate per-edit validation cost

On networkx, **one FULL benchmark pass costs at least 0.9–4.5 h per edit**, against **≈ 87 s for build + serial tests**. That makes benchmarks about **40–180×** the rest of FULL validation, so **benchmark cost, not build or test cost, is the dominant per-edit cost** on this project.

**How the number was obtained.**
- *Observed:* the asv-compatible runner (`bth.benchrun`, 5 processes × 3 values + 1 warmup, a fresh process per case, as asv isolates benchmarks) completed **8 of 171 cases in 2360 s**, ≈ 295 s per case. The run was **concurrent (CPU-pinned)**: CPUs 2–5, beside the RQ2 chain on 6–11. It was stopped as infeasible (`raw/networkx/bench/LABELS.md`).
- *Cause, measured:* importing `benchmarks/benchmark_algorithms.py` takes **65–71 s** (two runs, CPUs 0–1), because it builds all its graphs at import time. The other 7 modules import in ≈ 0.1 s (`raw/networkx/bench/import_times_S0.txt`). That module holds **49 of the 171 cases**, and process isolation repeats the import for every case and process.
- *Estimate (lower bound, import cost only):* Σ over cases of processes × import time = **0.89 h (1 process), 1.78 h (2 processes, asv's default), 4.45 h (5 processes, our protocol)** per FULL benchmark pass. Timing loops come on top. This is an estimate, not a measured full pass; the measured full pass needs an idle machine for hours and is scheduled.
- *Consequence:* benchmark **selection** (P1 profile reach, A5 static reach) and amortising module setup are where the savings can be large. Test selection saves at most ≈ 87 s per edit here.

**Bottleneck (C extension), for contrast:** a clean build is 9.9 s, which is **≈ 22 % of clean build + full tests, before benchmarks** (34.4 s of tests, 168 pass; single noisy runs; `rq1_bottleneck_build.md`). For networkx the build is 1.19–2.11 %.

## RQ1 — cost of FULL validation per edit (networkx)

Raw: `raw/networkx/{build,oracle-tests}/S<k>_<sha8>.json`. Table: `rq1_networkx.csv` (from `python scripts/aggregate_rq1.py networkx`).

**Definitions:**
- **Build** = `pip install -e . --no-deps --no-build-isolation`. This is the per-candidate build step that SWE-Perf, GSO and SWE-fficiency run (W2).
- **Tests** = the full pytest suite, run **serially** (no xdist, per M1), wall time.
- **Benchmarks** = the full asv suite (171 cases) through our asv-compatible runner, with 5 processes × 3 values and 1 warmup. This pass was stopped as infeasible; see the RQ1 headline. A measured pass with 2 processes is scheduled (`OVERNIGHT.md` item 4).

| State | SHA | Build (s) | Tests wall (s) | Σ test durations (s) | Tests | Failed | timing_label (rule below) |
|---|---|---|---|---|---|---|---|
| S0 | `181f2951` | 1.34 | 88.0 | 71.0 | 6771 | 0 | clean |
| S1 | `345a46c0` | 1.19 | 82.2 | 69.6 | 6771 | 0 | clean |
| S2 | `867fda8d` | 1.09 | 79.4 | 66.9 | 6771 | 0 | clean |
| S3 | `d3d79cc8` | 1.04 | 85.4 | 73.0 | 6771 | 0 | clean |
| S4 | `e773a6af` | 1.23 | 88.6 | 74.6 | 6771 | 0 | clean |
| S5 | `33152ccb` | 1.17 | 88.6 | 75.1 | 6771 | 0 | clean |
| S6 | `2aa848c0` | 1.06 | 89.5 | 76.8 | 6771 | 0 | clean |
| S7 | `ad6fed45` | 1.23 | 85.3 | 71.5 | 6771 | 0 | clean |
| S8 | `447e59df` | 1.14 | 89.5 | 75.5 | 6771 | 0 | clean |
| S9 | `eaa48be2` | 1.18 | 88.2 | 74.2 | 6771 | 0 | clean |
| S10 | `52b7255a` | 1.25 | 86.1 | 72.4 | 6771 | 0 | clean |
| S11 | `b85a9986` | 1.19 | 83.0 | 69.4 | 6771 | 0 | clean |
| S12 | `650ed52f` | 1.14 | 86.2 | 72.8 | 6771 | 0 | clean |
| S13 | `2bfab216` | 1.21 | 83.4 | 69.9 | 6771 | 0 | clean |
| S14 | `8a875737` | 1.04 | 79.7 | 67.4 | 6771 | 0 | clean |
| S15 | `20d0487d` | 1.34 | 75.4 | 62.5 | 6771 | 0 | clean |
| S16 | `17976a4f` | 1.06 | 142.2 | 126.5 | 6771 | 0 | **noisy** by rule (median per-test shift 1.57×, untouched-tests ratio 1.84) |
| S17 | `a9910480` | 2.52 | 119.2 | 97.8 | 6771 | 0 | clean by rule, **borderline** (untouched-tests ratio 1.147 vs 1.15 cut); re-time idle |
| S18 | `5eb50b60` | 1.28 | 80.0 | 66.0 | 6771 | 0 | clean |

**timing_label rule** (`scripts/aggregate_rq1.py`; **written after the first look at S16/S17**, so it is not pre-registered). A run is *noisy* if either:
- the median over tests (cross-state median duration > 50 ms) of duration / cross-state median exceeds **1.10** (uniform shift); or
- the summed duration of the tests that reach **no function changed by any of the 18 edits** (S0 depmap) exceeds **1.15×** its cross-state median. Those tests run identical code in every state.

The thresholds were not adjusted to change any label. The `tests_concurrent_load` column separately records overlap with logged concurrent activity (`raw/concurrency_log.json`).

**Reading (measured; single runs; 18 clean, 1 noisy):**
- **Tests.** Serial FULL tests take a median of **85.7 s** per edit (range 75.4–119.2 s over the clean states). That is 6771 tests, all passing at every state (no replayed edit broke a test). About 13–21 s of each run is collection/startup (wall minus Σ durations).
- **Build.** `pip install -e` takes a median of 1.19 s. That is **1.19–2.11 % of serial test time** over the clean states, so it is **negligible** for pure Python (ruling 1) and reported as such, not as a saving.
- **Over a session.** The base plus the 18-edit session spends **1700 s (≈ 28 min) on serial tests alone** (sum of all 19 runs), before any benchmark.
- **S16 is noisy:** a uniform 1.57× per-test shift across unrelated tests. S16 edits only `cluster.py::_triangles_and_degree_iter`, so the cause is external load.
- **S17 is borderline clean:** wall time 119 s, but by the rule its slowdown is partial (1.075 median shift, untouched-tests ratio 1.147). Its top slowed tests (gomory_hu, traveling_salesman, kcutsets) do not reach its edit (`structuralholes.py::effective_size`).
- **Re-timing.** All states will be re-timed on an idle machine and both values reported (PM request).
- **Benchmarks.** The FULL benchmark pass at S0 was stopped as infeasible (8/171 cases in 2360 s). The cost is reported as an import-based lower bound in the RQ1 headline, and a measured pass is scheduled overnight (`OVERNIGHT.md` item 4).

## RQ2/RQ3 — selection counts per arm over the 18-edit networkx session (DRAFT: tests only)

> Cost from counts and estimated seconds; functional misses on the frozen mutant set are below. Benchmarks **not** included in these totals (see the RQ1 headline).

**Inputs:** `sim/networkx/inputs/`, assembled by `scripts/assemble_inputs.py` from `raw/networkx/{changes,depmap,oracle-tests,testmon}/` and the base static analysis (`scripts/build_inputs.py`).
- **Command:** `python -m bth.orchestrate simulate --config configs/networkx.toml --inputs results/sim/networkx/inputs --out results/sim/networkx/rq2_steps.csv`.
- **Outputs:** **every number in the table below comes from `rq2_networkx.csv`** (`python scripts/rq2_table.py`), which documents each column. Per step: `sim/networkx/rq2_steps.csv`.
- **Note on `sim/networkx/rq2_steps.csv.summary.csv`:** its `total_cost_s` is the simulator's build + est. test-s + est. bench-s, with bench-s still 0. It **excludes pytest startup**, so it is *not* the end-to-end number (that is `est_end_to_end_s` in `rq2_networkx.csv`).
- **TESTMON** uses **real `pytest --testmon` selections**, chained over the states and unchanged (PerfAgent-style per-edit RTS).
- **Est. test-s** = Σ serial S0 per-test durations of the tests run (M1).
- **Est. end-to-end s** = est. test-s + build + **13.6 s pytest startup** per step that runs ≥ 1 test. The startup figure is the median of wall − Σ durations over the 18 clean serial runs.
- **Calibration:** est. end-to-end for FULL is 1548 s, vs **1634 s measured** (Σ serial wall + build, S1–S18).
- **Measured** end-to-end is given where it exists. For testmon it includes testmon's own analysis (Ekstazi end-to-end view).

| Arm (rules.md) | Tests run (Σ 18 steps) | Est. test-s | **Est. end-to-end s** | **Measured end-to-end s** | Full checks | Bench cases selected (Σ) |
|---|---|---|---|---|---|---|
| A0 FULL | 121 824 | 1278.8 | 1548 | **1634** (serial) | 18 | 3078 |
| A1 INC | 121 824 | 1278.8 | 1524 | — | 0 | 3078 |
| A2 TESTMON (PerfAgent-style) | 3 583 | 85.3 | 330 | **404** (concurrent, pinned) | 0 | 3078 |
| A3 CHANGED_MODULE | 461 | 3.6 | 221 | — | 0 | 0 |
| A5 STATIC_BENCH | 3 583 | 85.3 | 330 | — | 0 | 1893 |
| A2 + full every k=3 | 43 217 | 482.5 | 735 | — | 6 | 3078 |
| A2 + full every k=5 | 29 762 | 344.0 | 594 | — | 4 | 3078 |
| A3 + full every k=3 | 40 967 | 426.7 | 666 | — | 6 | 1026 |
| A3 + full every k=5 | 27 477 | 285.3 | 508 | — | 4 | 684 |
| A5 + full every k=3 | 43 217 | 482.5 | 735 | — | 6 | 2402 |
| A5 + full every k=5 | 29 762 | 344.0 | 594 | — | 4 | 2235 |
| **A4 OURS** (score trigger T=10 + final) | 35 742 | 403.2 | 655 | — | 5 | 2736 (as specified; see below) |
| A4 − F6-order | 35 742 | 403.2 | 655 | — | 5 | 2736 |
| A4 − accumulation | 35 248 | 400.0 | 652 | — | 5 | 2736 |
| A4 − profile (A3 bench rule) | 35 742 | 403.2 | 655 | — | 5 | 855 |
| A4 with periodic k=5 | 31 136 | 382.8 | 633 | — | 4 | 2413 |

**Reading (draft; no safety numbers yet, so nothing here ranks the arms):**
- **Headline ratio, end-to-end where measured.** testmon took **404 s measured** for S1–S18, vs **1634 s measured** for FULL serial tests + build: about **4× cheaper**, not the 15× that test-seconds alone suggest (85 vs 1279). Startup and testmon's own analysis dominate its real cost. Its first run (DB build at S0) took 279.7 s vs 88.0 s plain, 3.2×.
- **A4 currently behaves like periodic full checks at k ≈ 4.** Its score trigger fired at steps 3, 5, 8 and 13, plus the final check: 5 full checks, each caused by a **module-level edit**. Module-level edits expand A_t to every function of the module under F6, which pushes the score past T = 10.
  - Its cost (655 s est. end-to-end) sits **between A2 + k=5 (594 s) and A2 + k=3 (735 s)**.
  - On the frozen mutants, its extra selections buy no extra functional detection (see the fault-detection table). Regression detection is pending (overnight).
  - T is not retuned; this is a design finding about the pre-registered score.
- **Benchmarks.** A5's static reach selects 61 % of cases (1893 / 3078) and all 171 on the worked edit. The changed-module benchmark rule selects 0, since only 1 of 8 bench files maps to a module.
- **Accumulation** adds 494 test runs (35 742 vs 35 248). They are spread over steps 2, 7, 10–12 and 15–17; the largest is step 12 (421 vs 140), because the accumulated set still holds step 9–11 functions. That is +3 est. test-s. No detection benefit was found: the latent-fault class is empty on networkx (0 of 5 survivors become detectable later), so the pre-registered null stands.
- **F6-order changes nothing on this session** (identical counts with and without it): the 62 flagged functions are touched by no replayed edit and no frozen mutant (C7 finding below).

### Benchmark selection (counts; S0 profiles now measured, 171/171, 0 errors)

**Finding B1 — most replayed optimizations are not executed by any benchmark.**
- **The number:** for **12 of the 18 edits**, the S0 profile of **no** benchmark case executes any function the edit changed (module-level lines excluded). The steps are 1, 2, 5–8, 11–13, 15, 17 and 18.
- **The other 6 edits:** 1–8 cases execute at least one changed function (steps 3: 8, 4: 3, 9: 4, 10: 1, 14: 1, 16: 4).
- **Consequence:** *even FULL benchmarking cannot confirm the claimed speed-up of most of these commits with the project's own suite.* This bears on the RQ1 benchmark headline: FULL pays ≥ 0.9 h per edit largely for benchmarks that do not touch the edit.
- **Source:** `raw/networkx/profile/S0_181f2951.json` (merged from 5 parallel parts; not a timing).

**Finding B2 — A4's profile selection, as specified, collapses to "all benchmarks" after its first full check.**
- The P8 rule says profiles are refreshed at each full check and never used once older than the last checkpoint. **Only S0 profiles are measured**, so from step 3 on every profile counts as unknown, and the conservative default selects the benchmark: 171/171 at steps 3–18.
- That is the rule working as written with a missing input, not a selection result. Checkpoint re-profiling (S3, S5, S8, S13) is not yet done.
- A **labelled variant that violates P8** reuses the S0 profiles at every state (`sim/networkx/inputs_stale_s0_profiles/`, output `sim/networkx/variant_stale_s0_profiles.csv`). In it A4 selects **889 cases in total: 855 at its 5 full checks and 34 outside them** (ablation without accumulation: 13 outside). For comparison:
  - A5 static reach, no checkpoints: 1893 cases.
  - A5 + k=5: 2235.
  - FULL: 3078.
- **Static reach (A5)** selects all 171 cases on 11 steps (1–7, 10, 12–14) and 0–7 on the other 7. It selects all 171 on steps 1 and 2, where profile reach finds 0, because of module-level edits and import-closure edges.
- **Safety:** whether any of these selections misses a regression is the overnight slowdown oracle: within reach, plus the out-of-reach spot check.

### Fault detection on the frozen mutant set (networkx, functional)

**Set:** 25 frozen mutants (`frozen/networkx.mutants.json`, sha256 in `frozen/FROZEN.md`), placed in functions changed at their step, round-robin over the 18 steps.
- **20 are killed by FULL** at their state. That makes N = 20 (raw `raw/networkx/faults/killsets.json`; full suite, `-n 5`, counts only).
- **5 survive FULL** (`floyd_warshall_tree` ×2, `DiGMState.__init__`, `rich_club_coefficient`, `_triangles_and_degree_iter`). They are not counted as misses.
- **Latent re-check (§4.1b):** each survivor was re-applied at every later state and run against the tests whose depmap reaches it (`raw/networkx/faults/latent.json`). **None becomes detectable at any later state, so there are 0 latent faults, fewer than 3.**
  - **The pre-registered null stands:** on networkx the accumulation component (ablation a) is *expected to show no effect*, because every frozen fault is visible at the step that introduces it or never.
  - This is reported as such, not as evidence for or against accumulation. Caller faults (§4.1b, class 2) were not generated in this draft.
- **Detection:** an arm detects a mutant at step u ≥ s if the tests it runs at u intersect the mutant's kill set, or u is a full check (`bth.safety.simulate`). Raw `sim/networkx/rq2_steps.csv.faults.csv`.

| Arm | Missed (k / N) | 95 % Wilson CI of miss rate | Caught by selection / full check / final | Mean delay (steps) |
|---|---|---|---|---|
| A0 FULL, A1 INC | 0 / 20 | 0–16.1 % | (every step is full / all tests) | 0 |
| A2 TESTMON (PerfAgent-style) | 0 / 20 | 0–16.1 % | 20 / 0 / 0 | 0 |
| A5 STATIC_BENCH (testmon tests) | 0 / 20 | 0–16.1 % | 20 / 0 / 0 | 0 |
| **A3 CHANGED_MODULE** | **2 / 20** | **2.8–30.1 %** | 18 / 0 / 0, **2 missed** | 0 |
| A3 + full every k=3 / k=5 | 0 / 20 | 0–16.1 % | 13 / 6 / 1 | 0.05 / 0.15 |
| A2 or A5 + full every k=3 / k=5 | 0 / 20 | 0–16.1 % | 14–15 / 4–5 / 1 | 0 |
| A4 OURS and all its ablations | 0 / 20 | 0–16.1 % | 14 / 5 / 1 (k=5 variant: 15 / 4 / 1) | 0 |

**Why missed (A3, changed-module rule):** both misses come from the **name rule failing to map test files to modules**.
- `isomorph.py::fast_could_be_isomorphic` (step 8): its killing tests live in `tests/test_isomorphism.py`.
- `katz.py::katz_centrality_numpy` (step 9): its killing tests live in `tests/test_katz_centrality.py`.
- Neither test file's name matches its module, so the rule selects no test for either edit.
- With any periodic full check, both are caught at the next checkpoint (delay 1–3 steps).

**Reading (honest):**
- **On this fault class, selection catches almost everything by construction (M2).** The mutants sit in the edited functions, so every dependency-based arm catches all 20 at the injection step, and the arms differ only in cost.
- **Cost at equal detection (20 / 20): plain testmon is the cheapest** (330 s est. end-to-end, 404 s measured), ahead of A4 (655 s est.). On this evidence, **our policy's extra cost buys no extra functional detection**. The latent class is empty on networkx (0 / 5), so accumulation shows no benefit here, as pre-registered. Its possible value is in benchmark selection (regression safety overnight) and as a safety backstop for weak rules like A3.
- **testmon caveat:** at the injection step the simulation uses testmon's *clean-replay* selection ∩ kill set (readiness §4.1). Real testmon runs with each mutant present are not done yet; it re-selects on changed blocks, so the result is expected to match, but that is unverified.
- **N = 20 is small.** "0 / 20" means a miss rate below 16.1 % at 95 %, **not** "safe".

### C7 finding — function-level dependency data is partly nondeterministic (networkx)

**Measurement:** the same state was depmapped twice with identical settings (`-n 5`): S0 ×2 and S18 ×3. Raw: `raw/networkx/depmap/S0_181f2951{,.rep2}.json`, `S18_5eb50b60{,.rep2,.rep3}.json`; lists in `raw/networkx/order_dependent_S0pair.json` and `…_S18triple.json`.

- **62 of 2589 functions (2.4 %)** at S0, and 96 across the S18 triple, are attributed to **different test sets in runs of the same code**.
- **Causes:**
  - Some are first-call/lazy code charged to whichever test runs first on an xdist worker (`coreviews.AdjacencyView.__getitem__`, cache resetters).
  - Others are data-dependent, e.g. `vf2pp._restore_Tinout`, reached only for some randomised inputs.
- **Size:** the per-function swing is small, a handful of tests out of thousands.
- **Consequence:** a function-level map can, for these functions, select a test set that misses a test reaching the function in another run.
- **Rule (W3-new "F6-order", rules.md §3):** functions flagged by the S0 repeat pair select **all tests** when changed. The list comes from S0 only, so there is no hindsight.
- **In this session:** no replayed edit or frozen mutant touches a flagged function, so the rule costs and changes nothing (A4 with and without F6-order give identical counts and detection).
- A first, cruder pass, comparing consecutive states, over-counted (176): edits legitimately change callers' reach. One such case (`edmonds_karp_impl`) does not appear in the clean same-state lists.
- **Threat for the depmap-based arms:** S0's original depmap ran with `-n 6` and was re-run with `-n 5` for consistency; the `-n 6` file is kept as `.bak`.

## Harness self-checks (F8) that fired

- **Mining reproduces the frozen list:** `bth.mine` vs the shell probe. It caught a probe that matched commit bodies instead of subjects, and the written rule was kept (readiness §1.3).
- **Replay invariant:** a blobless source clone silently produced states that deleted 124 files. `replay.py` now asserts that every base blob is present and that each step touches only its edit's paths. After the fix, base → last state differs in exactly 18 modified files.
- **Test-ID agreement:** junit (oracle) and depmap test IDs agree on 6768 tests. The 3 junit-only entries are module-level skips with 0 s duration.

## Provenance note

The harness tree hash differs between S0 (`c02203a8…`) and S1+ (`ec7dba4c…`). In between, `replay.py` got the blob invariant and `benchrun.py` got the asv package import. Neither file is on the `oracle-tests` code path.
