# W3 results — PRELIMINARY

> **Costs come from counts and estimated seconds. Functional misses are measured on 20 frozen mutants. The slowdown oracle is measured (10 frozen slowdowns; FULL itself detects few of them, see "Slowdown oracle"). Regression detection is not yet fed into the per-arm simulation. Benchmarks are not yet included in the per-arm totals.** (Benchmark cost is reported separately in RQ1, where it dominates.)
>
> **Update 2026-11-22 06:00 PKT:** overnight items 2 (slowdowns) and 3 (bottleneck `iterators.h` hazard, `build-hazard-iterators-h.md`) are written up below. Item 4 (measured FULL benchmark pass) finished at 05:58: **1668 s**, labelled **noisy** under M5. It **corrects** the earlier "≥ 0.9 h" lower bound (see RQ1 headline).

**Status: PRELIMINARY, 2026-11-21 20:00 PKT. Partial data; numbers change as runs finish.** Every number links to a raw file under `results/raw/`. Each raw JSON carries the target state SHA and the harness tree hash in its `meta` block. Design: `../readiness.md` (v1.1). Rules: `../rules.md`.

**Platform:** WSL2 Ubuntu 24.04 on an i5-12400F (6 cores / 12 threads, 7 GB), CPython 3.12.16 (uv-managed), packages in `raw/networkx/env-freeze.txt`. The CPU governor cannot be pinned in WSL (T4). Times are wall-clock from single runs; repeats come later.

## Status of each piece

| Piece | networkx | bottleneck |
|---|---|---|
| Edit list frozen | ✅ 20 commits (subject rule; see the readiness §1.3 correction) | ✅ window amended by the general reformat rule (readiness §1.3, Deviation 2; PM-approved 18:11) |
| Replay states | ✅ 18 applied, 2 dropped (apply conflicts) | ✅ 13 of 16 applied on the amended window (base `f51ed86`); the 5-edit replay is kept as a sensitivity row |
| RQ1 FULL cost per state | ✅ tests + build, 19 states; ✅ measured FULL benchmark pass at S0: 1668 s, 2 processes, noisy (`OVERNIGHT.md` item 4); the earlier import-based bound is superseded | ✅ build probes (`rq1_bottleneck_build.md`); idle re-time done (item 1b; still noisy under M5) |
| RQ2 counts per arm | ✅ test counts + test-seconds + end-to-end (18 steps, 16 arms); ✅ benchmark-selection counts (S0 profiles); ✅ functional safety; 🟡 benchmark seconds and regression safety (overnight) | — |
| Injected faults | ✅ 25 mutants frozen, 20 killed by FULL, detection simulated; ✅ latent re-check done: **0 of 5** survivors become detectable later (pre-registered null stands); ✅ slowdown oracle measured: FULL detects at most **3 of 10** (2 on target, 0 in the pre-set bands), so regression safety is **not measurable** with the frozen set (pre-registered primary result); the first out-of-reach spot check had no power (6 vs 6) and is withdrawn; the powered re-run, relabelled a **profile-completeness check** (not safety evidence), finds **1 slower in 50** out-of-reach comparisons over all 5 slowdowns (#9, louvain 1.13×, p = 0.0019; flagged by the pre-registered rule; a post-hoc re-check with a base-vs-base control, **not order-balanced** (partial run), **did not reproduce it**, 0.97–1.01×, partial 5/6 runs; the flag stands; #0 is labelled concurrent and #7 noisy) | ✅ `iterators.h` hazard study (`build-hazard-iterators-h.md`): the stale-header hazard did not reproduce; **measured false pass** of an incremental tree after a failed compile (`98b59df2`); states 9–13 held out; main result = amended window, states 1–8 |

## RQ1 headline — benchmarks dominate per-edit validation cost, and most of that cost is import-time setup

On networkx, **one FULL benchmark pass (all 171 cases, asv's default 2 processes × 3 values) cost 659–2444 s across 6 measured passes on the night of 21–22 Nov.** The median is ≈ 730 s (≈ 12 min). Build + serial tests take **≈ 87 s**, so benchmarks are about **8–28×** the rest of FULL validation (≈ 8× at the median). **Benchmark cost, not build or test cost, is the dominant per-edit cost** on this project.

**Most of the benchmark cost is setup (advisor review, 07:50):**
- **86.9–95.5 % of a pass is spent in one module's 49 cases (`benchmark_algorithms`)**, over the 6 passes (Σ run wall of its cases ÷ Σ run wall of the pass: item 4 94.1 %, `bench/S0_181f2951.idle.json`; base side of `slowdowns/0{1,2,3,4,8}.json` 95.5 / 88.5 / 86.9 / 86.9 / 87.6 %; recomputed 16:20 after W6, earlier text said 87–96 %). Their time includes their timing loops, but **79.9–94.8 % of a pass lies outside the timing loops over all 9 passes** (1 − Σ samples × number ÷ Σ run wall; 6 earlier passes 79.9–94.1 %: item 4 89.8 %, base sides of slowdowns 01/02/03/04/08 94.1 / 82.4 / 79.9 / 80.1 / 81.3 %; tonight's (d) passes 94.8 / 91.4 / 88.2 %; recomputed 23:50 from the same raw files; earlier text said 80–94 % over 6 passes), mostly per-process start-up and import-time setup: they rebuild all their graphs at module import, once per process.
- **The benchmarks' timing loops take only 132–171 s per pass** (Σ samples × number). Measured: 171 s in item 4; 132–144 s on the base side of the slowdown-oracle passes (`raw/networkx/slowdowns/0{1,2,3,4,8}.json`).
- **Superseded by the E5 measurement (24 Nov, 01:47; section "E5: measured setup-cached pass"): a cached pass measured 189–201 s, ≈ 2.2–2.3× build + tests.** Earlier estimate, kept for the record: **Estimate, not measured — "setup cached":** if the import-time setup were built once and reused, a FULL pass would cost roughly its timing loops, **≈ 130–170 s, about 1.5–2× build + tests (≈ 87 s)** instead of 8–28×.
  - This is a lower bound. It leaves out per-process start-up and warm-up values.
  - So benchmarks would still be the largest single part, but no longer dominant by an order of magnitude.
  - Selection would still matter, at a much smaller scale.
- **Build share including benchmarks:** ≈ 1.2 s of ≈ 820 s at the median pass, **≈ 0.15 %**.

**The 6 passes (all noisy-labelled or concurrent; single passes):**
- **Dedicated S0 pass (overnight item 4):** 1668 s, `raw/networkx/bench/S0_181f2951.idle.json`. 171/171 cases, 0 errors. Labelled **noisy** (M5: load 1.63 at start; 1 of 171 cases > 1.5).
- **Slowdown-oracle base side, per pass:** the mean over its 3 interleaved passes of the unpatched clone, from `raw/networkx/slowdowns/0{1,2,3,4,8}.json`.
  - #3: 659 s; #4: 665 s; #8: 708 s (all its base-side runs at load ≤ 1.45); #2: 751 s. Base-side runs with load > 1.5, of 513 each: #2 6, #3 81, #4 15, #8 0.
  - #1: 2444 s, with 88/513 base-side runs > 1.5 (177/1026 over both sides).
  - These are at states S2–S10 rather than S0, but with the same benchmark code.
- **Finding (benchmark-cost noise): the spread is ≈ 3.7× under one protocol on one machine in one night.** So a single FULL benchmark pass is a noisy cost unit. Per-edit benchmark cost should be reported as a range, and any cost-matched arm comparison (RQ3) has to use per-case cost weights from one pass, not wall time from separate passes. WSL load does not explain it: item 4 had only 1 case > 1.5 yet took 1668 s. The cause is **unknown**. The later per-run data (machine-state finding) show the variation sits in one module's per-process setup, not in the timed samples. Host-side load is one candidate, but it was not measured, and at 10:42 Windows CPU read 11 %. M5 should also gate on Windows CPU, as the overnight start gate did.
- **Where the time goes:** `benchmark_algorithms` (49 cases) is 1570 s of the 1668 s pass and ≈ 620 s of the 708 s pass (#8). Its per-case median is 8.7–8.8 s in the fast passes and 27 s in item 4, which is roughly 4–13 s per import for 2 processes. Timing loops are only ≈ 171 s per pass. The rest is process start-up and import-time graph construction.

**Finding (machine state, 2026-11-22): `benchmark_algorithms` per-process setup drifts across the day.** It was ≈ 1.6× slower after the PC restart than in the morning, part of a day-long drift (≈ 4 → 40 s per process; see the A/A section), while the timed samples did not change. **The cause is unknown.**

| | Before the restart (spot check #0, #5, #6; 06:19–07:28) | After the restart (spot check #7; 10:13–10:44) |
|---|---|---|
| `benchmark_algorithms` run wall time (5 processes × 3 values; one case-state) | median **114 s**, 70–183 s (n = 30) | median **177 s**, 135–239 s (n = 10) |
| Same case, after / before | — | **1.08–1.96×**, median ≈ 1.6× (each #7 run's wall ÷ the median of the same case's morning runs, both labels; the critic's alternative methods give ≈ 1.41–1.80×, median ≈ 1.5×) |
| Timed samples (base side, same cases), after / before | — | **0.92–1.16×**, median ≈ 0.96× (median of the #7 base run's samples ÷ the median of the morning base runs' sample medians; includes 5 cheap cases; the critic gets 0.92–1.03× for the algorithm cases) |
| Cheap cases (other modules) | median ≈ 1 s | median ≈ 1 s |
| WSL 1-minute load at each run | ≤ 1.10 | 0.14–0.43; 1.62 once |
| Windows CPU at the gate | ≤ 20 % (gate) | ≤ 20 % (gate); 11 % at a spot reading at 10:42 |
| Power plan | not recorded | Balanced (read 10:43) |
| Memory | not recorded | WSL: 5.2 GB available, no swap use, PSI memory/io 0; Windows: 2.5 of 15.8 GB free (10:45) |

**Raw files:** `raw/networkx/slowdowns/spotcheck_powered/{00,05,06,07}.json`; per-run `t_start`/`t_end` are in `07.partial.jsonl`.

**Reading:**
- The extra time is in **per-process setup**: process start, imports, and `benchmark_algorithms`' import-time graph construction. The timing loops did not slow.
- **The cause is unknown.** Candidates, none verified:
  - host memory pressure, which would slow the WSL VM's allocation-heavy setup;
  - the power or boost state after boot;
  - a cold page cache.
- The likely link: **the same effect probably explains the failed A/A run's 2–3× overrun** (07:49–09:14). That run is not verified: no per-run data survived.
- **Consequences:**
  - (1) **Per-pass benchmark cost**, which is dominated by setup, varies with machine state beyond the 3.7× already seen. This adds to the benchmark-cost noise finding.
  - (2) The asv verdicts compare **timed samples**, and these did not move. Because A and B runs alternate, **slow drift** in machine state shifts both sides alike, so the ratio is shielded from it. It is **not** shielded from a **change in variance**: a noisier machine widens the "same" spread and lowers power. The A/A re-run measures the machine as it is now, overrun included, on purpose (PM 10:43).
- **No system setting was changed.** The power plan and other settings are the owner's call.

**Correction (2026-11-22 06:05, revised after the critic review at 06:06): the earlier "at least 0.9–4.5 h" lower bound was wrong, an over-estimate by ≈ 9×.** Derivation, like for like at 2 processes: bound 1.78 h = 6408 s against the median measured pass of ≈ 730 s gives 6408 / 730 ≈ 8.8×. Across all 6 passes the factor is 2.6–9.7×. It multiplied a 65–71 s import time measured at 19:18 under concurrent load (likely cause, **not verified**). The old figures stay below for the record and are struck from the headline.

**How the earlier (superseded) number was obtained.**
- *Observed:* the asv-compatible runner (`bth.benchrun`, 5 processes × 3 values + 1 warmup, a fresh process per case, as asv isolates benchmarks) completed **8 of 171 cases in 2360 s**, ≈ 295 s per case. The run was **concurrent (CPU-pinned)**: CPUs 2–5, beside the RQ2 chain on 6–11. It was stopped as infeasible (`raw/networkx/bench/LABELS.md`).
- *Cause, measured:* importing `benchmarks/benchmark_algorithms.py` takes **65–71 s** (two runs, CPUs 0–1), because it builds all its graphs at import time. The other 7 modules import in ≈ 0.1 s (`raw/networkx/bench/import_times_S0.txt`). That module holds **49 of the 171 cases**, and process isolation repeats the import for every case and process.
- *Estimate (lower bound, import cost only):* Σ over cases of processes × import time = **0.89 h (1 process), 1.78 h (2 processes, asv's default), 4.45 h (5 processes, our protocol)** per FULL benchmark pass. Timing loops come on top. This is an estimate, not a measured full pass.
- *Measured pass (overnight item 4, 05:30–05:58 PKT):* 1668 s, as above. It is **labelled noisy** under the pre-registered M5 rule: the 1-minute load was 1.63 > 1.5 at its start, left over from item 3's own benchmarks. The script's start gate only labels and does not postpone, which is a logged deviation (`raw/networkx/bench/LABELS.md`).
  - Used as a **noisy per-pass cost** and for per-case cost weights.
  - Not used for regression decisions or the noise floor. A re-run needs PM approval.
- *Consequence:* benchmark **selection** (P1 profile reach, A5 static reach) and amortising module setup are where the savings can be large: **86.9–95.5 % of a pass is the 49 `benchmark_algorithms` cases, mostly import-time graph construction repeated per process.** Test selection saves at most ≈ 87 s per edit here.

**Bottleneck (C extension), for contrast:** on the amended base `f51ed86`, a clean build takes **4.7–5.4 s** (item 1b, 3 repeats, `raw/bottleneck/retime-idle/repeat{1,2,3}.json`) and the full suite **≈ 24 s** (191 tests; `raw/bottleneck/hazard/*/f_test_{inc,stale}.log`, `raw/bottleneck/s0-junit.xml`). So the build is **≈ 16–18 % of clean build + full tests, before benchmarks**. All runs are **noisy** (load 1.46–2.35). For networkx the build is 1.19–2.11 %.
- The earlier figure (9.9 s, ≈ 22 %, 168 tests; `rq1_bottleneck_build.md`) was on the superseded base `22657ac` under concurrent load and is superseded.

**Bottleneck build hazards, measured (`build-hazard-iterators-h.md`):**
- **Harness/replay lesson H1, not a finding about reduced builds (advisor review): an incremental tree masks a failed compile, and RTS then passes.** Rejecting a failed build (rule B0, kept) is what any harness does. Observed on a replayed, non-compiling state (`98b59df2`). This is a replay artefact: a prerequisite commit is missing, so the state never existed upstream. The full suite passed on the stale binaries; testmon itself was not run on bottleneck.
  - What happened: replayed edit `98b59df2` (step 9 of 13) does not compile. The incremental tree kept the old `.so` files and **passed 191/191 tests**, while the clean build failed.
  - Rule B0 was adopted: a failed build is a reject, whatever the tests say (rules.md §2).
- **The `iterators.h` stale-header hazard did not reproduce at the natural edits.** The pre-fix probe leaves stale artefacts, but they are byte-identical to a correct rebuild.
- **B4 (`.so` hash differential) is invalid as specified,** because the build path is embedded in every `.so`. Fixing it is a post-meeting item.
- **Scope (PM ruling 05:50):** bottleneck states 9–13 are held out of benchmark runs and the headline. **The main bottleneck result is the amended pre-registered window (base `f51ed86`) truncated to states 1–8**, before the uncompilable state (PM clarification 06:10, superseding the 05:50 "5-edit window" wording). The 5-edit replay (`edits/bottleneck-5edit.*`) stays a sensitivity row. Limitation: the bottleneck evidence covers 8 edits.

## RQ1 — cost of FULL validation per edit (networkx)

Raw: `raw/networkx/{build,oracle-tests}/S<k>_<sha8>.json`. Table: `rq1_networkx.csv` (from `python scripts/aggregate_rq1.py networkx`).

**Definitions:**
- **Build** = `pip install -e . --no-deps --no-build-isolation`. This is the per-candidate build step that SWE-Perf, GSO and SWE-fficiency run (W2).
- **Tests** = the full pytest suite, run **serially** (no xdist, per M1), wall time.
- **Benchmarks** = the full asv suite (171 cases) through our asv-compatible runner, with 5 processes × 3 values and 1 warmup. That 5-process pass was stopped as infeasible. Six full passes were later measured with 2 processes × 3 values (659–2444 s, median ≈ 730 s, including `OVERNIGHT.md` item 4); see the RQ1 headline.

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
- **Benchmarks.** One FULL benchmark pass costs 659–2444 s (6 measured passes, 2 processes; median ≈ 730 s), see the RQ1 headline. The earlier import-based lower bound is superseded.

### RQ1 — idle re-timing (overnight item 1, 19:38–20:04 PKT)

**What:** build + serial FULL tests were re-run for all 19 states (`*.idle.json` in `raw/networkx/{build,oracle-tests}/`).
- Table: `rq1_networkx_idle.csv`, made by `scripts/idle_compare.py`.
- Load at start: the `loadavg=` line printed by `oracle_nx.sh` before each run, from `raw/overnight.log`.

| | First run | "Idle" re-run |
|---|---|---|
| Median tests wall time | 86.1 s | 77.2 s |
| Range | 75.4–142.2 s | 70.7–83.8 s |
| First / re-run ratio | 0.96–1.99 | |
| Re-run build (`pip install -e`) | | 0.95–1.75 s |
| Re-run tests | | all 6771 tests, exit 0 |

**Despite the name, none of the 19 re-runs is M5-clean.**
- S0–S6 overlapped this session's profile job (19:38–19:46, `concurrency_log.json`). Even so, the overnight gate had opened at 19:38: WSL load ≤ 1.0 and Windows CPU ≤ 20 % for 3 minutes.
- From S1 on, the 1-minute load at start was **1.54–2.95**, above the 1.5 gate.
- Part of that is self-inflicted: the gate reads the 1-minute average right after the previous serial run, which adds up to ≈ 1. That does not explain values of 2–3. The rest is unidentified, probably other sessions.
- So every re-run is labelled **noisy**, and the gate fix below (postpone, not label) applies.

**What the re-runs still show (direction, not precise values):**
- **S16 and S17 return to normal:** 71.5 s and 71.0 s, against 142.2 s and 119.2 s first time. That confirms their first-run slowness was external load, as the timing_label rule said for S16. S17 was borderline under that rule; it now looks load-affected too.
- **The other 17 states agree within 0.96–1.20×.** The re-runs are mostly a little faster.
- **RQ1's per-edit serial test cost is ≈ 71–89 s** across both runs, excluding the S16/S17 first runs. Build is 1–2 % of that.
- **The headline does not change:** about 85 s per edit for build + tests, against a 659–2444 s FULL benchmark pass.

## RQ2/RQ3 — selection counts per arm over the 18-edit networkx session (DRAFT: tests only; 18 replayed edits = 15 optimizations + 3 non-optimizations matched by the subject rule, see "networkx edit sets")

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

**Reading (draft).** What ranks the arms so far: **functional safety only.** Every arm misses 0/20 frozen mutants except A3 changed-module, which misses 2/20 (fault-detection table below). So among the arms with equal functional detection, cost decides. What does **not** rank them: **regression safety**, which is not measurable on networkx with the frozen slowdown set (FULL detects at most 2–3 of 10; see "Slowdown oracle"). Benchmark cost per arm is also not yet in the totals:
- **Headline ratio, end-to-end where measured.** testmon took **404 s measured** for S1–S18, vs **1634 s measured** for FULL serial tests + build: about **4× cheaper**. **This comparison mixes load conditions:** the 1634 s includes the noisy S16 run, and testmon was measured concurrently. The idle FULL re-runs (item 1, `*.idle.json`) give **1413 s, i.e. 3.5×**; the idle S0–S5 runs overlapped profiling (`concurrency_log.json`). So the ratio is 3.5–4×, not the 15× that test-seconds alone suggest (85 vs 1279). Startup and testmon's own analysis dominate its real cost. Its first run (DB build at S0) took 279.7 s vs 88.0 s plain, 3.2×.
- **A4 currently behaves like periodic full checks at k ≈ 4.** Its score trigger fired at steps 3, 5, 8 and 13, plus the final check: 5 full checks, each caused by a **module-level edit**. Module-level edits expand A_t to every function of the module under F6, which pushes the score past T = 10.
  - Its cost (655 s est. end-to-end) sits **between A2 + k=5 (594 s) and A2 + k=3 (735 s)**.
  - On the frozen mutants, its extra selections buy no extra functional detection (see the fault-detection table). Regression detection is measured for FULL only so far (see "Slowdown oracle"); it is not yet in the per-arm simulation.
  - T is not retuned; this is a design finding about the pre-registered score.
- **Benchmarks.** A5's static reach selects 61.5 % of cases (1893 / 3078) and all 171 on the worked edit. The changed-module benchmark rule selects 0, since only 1 of 8 bench files maps to a module.
- **Accumulation** adds 494 test runs (35 742 vs 35 248). They are spread over steps 2, 7, 10–12 and 15–17; the largest is step 12 (421 vs 140), because the accumulated set still holds step 9–11 functions. That is +3 est. test-s. No detection benefit was found: the latent-fault class is empty on networkx (0 of 5 survivors become detectable later), so the pre-registered null stands.
- **F6-order changes nothing on this session** (identical counts with and without it): the 62 flagged functions are touched by no replayed edit and no frozen mutant (C7 finding below).

### Benchmark selection (counts; S0 profiles now measured, 171/171, 0 errors)

**Finding B1 — many replayed optimizations are not executed by any benchmark** (12/18 replayed edits; **9/15 true optimizations, Wilson 36–80 %**, so "most" is not established; see "networkx edit sets").
- **The number:** for **12 of the 18 edits**, the S0 profile of **no** benchmark case executes any function the edit changed (module-level lines excluded). The steps are 1, 2, 5–8, 11–13, 15, 17 and 18.
- **Mining precision (post-hoc audit, ≈ 12:33):** 3 of the 18 replayed edits are not optimizations by their subject: step 8 `519e819f` (MAINT), step 13 `bf130bfe` ("coefficient"), step 17 `9f6079c0` (bug fix). **On the 15 true optimizations, 9/15 are unreached (60 %, Wilson 36–80 %).** B1 still points the same way, but "most" is not established. See Q3.
- **The other 6 edits:** 1–8 cases execute at least one changed function (steps 3: 8, 4: 3, 9: 4, 10: 1, 14: 1, 16: 4).
- **Consequence:** *even FULL benchmarking cannot confirm the claimed speed-up of many of these commits (9/15 true optimizations; CI 36–80 %) with the project's own suite.* This bears on the RQ1 benchmark headline: FULL pays 659–2444 s per edit (median ≈ 730 s; 6 measured passes, 2 processes) largely for benchmarks that do not touch the edit.
- **Source:** `raw/networkx/profile/S0_181f2951.json` (merged from 5 parallel parts; not a timing).

**Finding B2 — A4's profile selection, as specified, collapses to "all benchmarks" after its first full check.**
- The P8 rule says profiles are refreshed at each full check and never used once older than the last checkpoint. **Only S0 profiles are measured**, so from step 3 on every profile counts as unknown, and the conservative default selects the benchmark: 171/171 at steps 3–18.
- That is the rule working as written with a missing input, not a selection result. Checkpoint re-profiling (S3, S5, S8, S13) is not yet done.
- A **labelled variant that violates P8** reuses the S0 profiles at every state (`sim/networkx/inputs_stale_s0_profiles/`, output `sim/networkx/variant_stale_s0_profiles.csv`). In it A4 selects **889 cases in total: 855 at its 5 full checks and 34 outside them** (ablation without accumulation: 13 outside). For comparison:
  - A5 static reach, no checkpoints: 1893 cases.
  - A5 + k=5: 2235.
  - FULL: 3078.
- **Static reach (A5)** selects all 171 cases on 11 steps (1–7, 10, 12–14) and 0–7 on the other 7. It selects all 171 on steps 1 and 2, where profile reach finds 0, because of module-level edits and import-closure edges.
- **Safety:** see "Slowdown oracle" below. FULL itself detects at most 3 of the 10 frozen slowdowns, and the out-of-reach spot check could not detect anything (no power), so there is no regression-safety evidence for these selections.

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
- With any periodic full check, both are caught at the next checkpoint (delay 1–2 steps).

**Reading (honest):**
- **On this fault class, selection catches almost everything by construction (M2).** The mutants sit in the edited functions, so every dependency-based arm catches all 20 at the injection step, and the arms differ only in cost.
- **Cost at equal detection (20 / 20): plain testmon is the cheapest** (330 s est. end-to-end, 404 s measured), ahead of A4 (655 s est.). On this evidence, **our policy's extra cost buys no extra functional detection**. The latent class is empty on networkx (0 / 5), so accumulation shows no benefit here, as pre-registered. Its possible value is in benchmark selection (regression safety overnight) and as a safety backstop for weak rules like A3.
- **testmon caveat:** at the injection step the simulation uses testmon's *clean-replay* selection ∩ kill set (readiness §4.1). Real testmon runs with each mutant present are not done yet; it re-selects on changed blocks, so the result is expected to match, but that is unverified.
- **N = 20 is small.** "0 / 20" means a miss rate below 16.1 % at 95 %, **not** "safe".

### networkx edit sets — reconciliation (PM 12:35; text only)

**Three edit sets are in play:**
- **20 mined** commits (`edits/networkx.candidates.json`, subject rule).
- **18 replayed** states (steps 1–18): 2 mined commits, `675034ad` and `abf2feda`, were dropped on apply conflicts. Both are true optimizations.
- **15 true optimizations among the 18 replayed**, by a post-hoc manual reading of the subjects. Steps **8** (`519e819f`, MAINT), **13** (`bf130bfe`, rich_club "coefficient") and **17** (`9f6079c0`, bug fix in vectorized code) are not optimizations. Among the 20 mined, 17 are true optimizations.

**Every B1 figure is over the 18 replayed states** (module-level lines excluded):

| Reach measure | All 18 replayed | 15 true optimizations |
|---|---|---|
| S0 measured profile | 12/18, 67 % [44–84 %] | **9/15, 60 % [36–80 %]** |
| S0 static call graph | 7/18, 39 % [20–61 %] | **4/15, 27 % [11–52 %]** |

Static reach leaves fewer edits unreached than the profile does, on both sets.

**Other networkx results that include steps 8, 13 or 17, and whether they change:**
- **RQ1 cost per state** (S8, S13, S17) and the RQ1 table: **valid as written.** They are costs of validating a replayed edit sequence. S17's timing note (borderline, load-affected) is unchanged.
- **RQ2/RQ3 selection counts and costs, all arms including testmon and A4/C5:** **valid**, for the same reason. They cover all 18 replayed edits.
  - **A4's score trigger fired at steps 8 and 13**, both non-optimization edits; 13 is a module-level edit. So 2 of A4's 5 full checks come from non-optimization edits.
  - C5's additive budget shares those triggers.
  - The A4 ≈ "periodic k≈4" reading stays a property of this replayed sequence.
- **Frozen mutants:**
  - Step 8's mutant (`fast_could_be_isomorphic`) is killed by FULL. It is **one of A3's 2 misses**.
  - Step 13's (`rich_club_coefficient`) survived FULL, so it is not in N = 20.
  - Step 17's (`effective_size`) is killed.
  - Restricted to true-optimization steps: N = 18, A3 misses 1/18 (`katz`, step 9), and every other arm misses 0/18. **Conclusions unchanged.**
- **Slowdowns:** #6 (`could_be_isomorphic`, step 8) sits in a non-optimization edit's function.
  - It was undetected by FULL, unreached, and shows 10 same in the profile-completeness check.
  - Removing it leaves 9 slowdowns; FULL detection stays at most 3, and the profile-completeness check is 1 slower in 40.
- **Worked edit** (step 10, `c1c468d5`, a true optimization): unaffected.
- **C7 and F6-order:** not step-specific; unaffected.

**Wording rule applied:** where a result spans all 18 steps, "replayed edits" means the mined sequence: 15 optimizations plus 3 non-optimizations matched by the subject rule. Only B1, which is a claim about optimization edits, is also given on the 15.

### Q3 — Does B1 replicate? Optimization edits that no benchmark reaches (PM 07:50; no timing). Rewritten ≈ 12:33 after a critic review with 2 BLOCKING findings

**Rule, frozen before cloning:** `../frozen/q3_project_rule.md`, with an addendum.
- **Projects:** candidates tried in a fixed order: geopandas, pvlib-python, xarray. The first 2 that pass are used, which turned out to be geopandas and pvlib-python. xarray was not needed. Selection log: `q3/selection.json`.
- **Mining:** the same subject-only mining rule as networkx. The edit lists were frozen before any reach was computed; sha256 in `frozen/FROZEN.md`, verified.
- **Measure:** an edit is **unreached** when none of its changed functions (module-level lines excluded) is reached by any asv benchmark. Reach comes from the static call graph at the parent of the oldest edit.
- **Raw files:**
  - `q3/q3_b1_static.first_count.json` holds the **as-frozen** counts, including bottleneck 4/8.
  - `q3/q3_b1_static.json` holds the recount with the post-hoc bottleneck `NAME` interpretation (0/8). The networkx, geopandas and pvlib counts are identical in both.
  - `q3/q3_diag.json` holds the post-hoc heuristic.

**Primary result, as frozen:**

| Project | Unreached (static call graph, single base) | Note |
|---|---|---|
| networkx | 7/18, 39 % [20–61 %] | measured S0 profile: **12/18, 67 % [44–84 %]** (B1) |
| geopandas | 18/20, 90 % [70–97 %] | base 2017, edits 2017–2025 |
| pvlib-python | 14/14 | **invalid**: the 2014 base has no asv suite |
| bottleneck, states 1–8 | **4/8, 50 % [22–78 %]** | static Python + name-based native, as frozen |

**Why these numbers do not establish B1 outside networkx:**
1. **The mining regex has poor precision on some projects (post-hoc manual audit of the subjects).**
   - `efficien` matches "coefficient" and "efficiency"; `optimi[sz]` matches `scipy.optimize`; `faster` matches function names. For networkx, **only 1 of its 3 non-optimizations** (`bf130bfe`) matched via "coefficient". The other two matched via `faster` in function names (`519e819f`) and `vectoriz` in a bug-fix subject (`9f6079c0`).
   - **True optimizations by subject:** networkx **17/20**, bottleneck **16/16**, geopandas **19/20**, pvlib **≈ 4/14**.
     - networkx non-optimizations: `bf130bfe` rich_club_coefficient parameter; `9f6079c0` a bug fix in vectorized code; `519e819f` MAINT, matching through `fast_/faster_` names.
     - geopandas: `6286f13f` is a DOC commit.
     - pvlib: 9 of its 10 suite-era edits are not optimizations (coefficient or efficiency wording, a `scipy.optimize` API).
   - **So the pvlib count says nothing about B1.**
   - **networkx B1 on true optimizations only:** removing steps 8, 13 and 17 leaves **9/15, 60 % [36–80 %]**, against 12/18. The finding holds.
2. **Static reach from one old base is not a bound in either direction.**
   - Functions added after the base (geopandas 2017; e.g. `GeometryArray.to_crs`) are unreached by construction, which over-counts unreached edits.
   - Static reach can also over-reach: branch-insensitive edges, and benchmarks removed later, under-count unreached edits. networkx shows static reach covering more than the profile (7 vs 12).
   - The frozen addendum predicted that static reach would **under**-count unreached edits; for geopandas the effect of the old base may dominate the other way.
3. **The name heuristic (post hoc, `q3_diag.py`, written after the first count) is not an over-approximation of reach.**
   - It checks only whether a changed function's own name appears in the suite at the edit's parent. It does not follow calls.
   - It misses helpers reached through calls, e.g. geopandas `plotting.py::_flatten_multi_geoms`, which static reach does reach.
   - So it is **neither a lower nor an upper bound**. geopandas by this heuristic: 7/20 unreached. Reported as a heuristic only.
4. **Bottleneck `NAME` interpretation (post hoc, after the first count).**
   - The 4 "unreached" edits change `NAME`, the generic body of a C template. The commit subjects say they concern nanmin/nanmax/nanargmin.
   - These functions are named in the suite, so they are probably reached. But the code fix ("reached if any native function of the package is named") is **too broad**: it is always true for bottleneck, and it is not per extension.
   - A per-function expansion of the template blocks was not done. **As frozen: 4/8. Under the template interpretation: 0/8.** Both are reported.
5. **Smaller limits:**
   - The changed-function sets include test and benchmark functions: diffs are parent → commit with no source pathspec, whereas networkx's replay excluded tests.
   - Rule 2 was checked by file count, not lines (pvlib: 1 native file vs 67 `.py`).
   - The rule file's header says "≈ 07:58", but its file time is 07:53.

**Deviations from the frozen rule:**
- pvlib was declared invalid and kept, not replaced by xarray.
- Post-hoc name heuristic and per-edit bases.
- Post-hoc bottleneck `NAME` rule.
- Manual precision audit of subjects.

**Reading, after the review:**
- **B1 is established on networkx only:** measured profiles, 9/15 true optimizations unreached.
- **geopandas:** the as-frozen static count (18/20) is consistent with B1, but the measure is biased by the old base. The name heuristic gives 7/20. Neither is a bound. **Consistent with B1 under a heuristic; not established.**
- **pvlib:** not informative; the mined sample is mostly not optimizations.
- **bottleneck:** 4/8 as frozen, 0/8 under the template interpretation. Its suite enumerates its functions by name.
- **What B1 replication would need:**
  - measured benchmark profiles (`sys.monitoring`, as for networkx) at each edit's parent;
  - a mining rule with better precision, e.g. excluding `coefficient`/`efficiency`, applied before mining. That is a rule change for any new study, not this one.

**Side finding (true at bottleneck base `f51ed862`):** in `asv_bench/benchmarks/reduce.py`, `time_nanmax` calls `bn.nanmin` (lines 44–45 and 90–91).
- The template code shared by nanmin and nanmax is still reached.
- Only nanmax-specific code paths are never benchmarked.

### RQ3 — C5 batching comparators at matched cost (networkx, simulation; PM 06:27 Q1)

**Summary (advisor review, 07:50). There is no "A4 beats batching" headline.**
1. **The design cannot tell selection rules apart.** Every arm with a per-edit tier catches every mutant at its injection step, **by construction of the mutant placement**: the mutants sit in the edited functions (M2). So caught-at-injection differences between per-edit arms and batching reflect the mutant model, not rule quality.
2. **A4 as implemented costs more.** On primary cost it is dominated by plain TESTMON. With benchmarks it costs ≈ 2× batching at matched cost, and that depends on finding B2: profile selection collapses to all 171 cases without checkpoint re-profiling. It is not intrinsic to the design.

**Plan, pre-registered before any output:** `sim/networkx/c5_plan.md` (file saved 06:29:51; its header says 06:35, which is wrong — the file time is the real one). The simulation ran at 07:39–07:40. Raw files: `sim/networkx/c5_steps.csv{,.faults.csv,.summary.csv}`, `c5_compare.{csv,json}`, `c5_run.log`. Script: `scripts/c5_compare.py`.

**Comparators** (`bth.select.Batch`, 7 unit tests in `tests/test_batch.py`, rules.md §6) are pure **batching**: nothing is built or run between full checks.
- **cap-only** `BATCH:cap=k` is FSB / a time cap.
- **additive-budget** `BATCH:budget=T` is risk-mass "-la" batching with A4's own score as the risk sum.
- Inputs are frozen: the same 18 steps and the same 20 mutants FULL kills. No T or k was tuned.

| Arm | Full checks | **Est. end-to-end s, no benchmarks** (primary) | + benchmarks (item-4 weights, noisy) | Missed (every arm: 0/20, 95 % Wilson CI 0–16.1 %) | Caught at injection step | Mean delay (steps) | Mean / max window |
|---|---|---|---|---|---|---|---|
| BATCH:cap=2 / 3 / 5 / 8 | 9 / 6 / 4 / 3 | 774 / 516 / 344 / 258 | 15 783 / 10 522 / 7 015 / 5 261 | 0/20 | 9 / 6 / 5 / 2 | 0.55 / 1.05 / 1.70 / 3.65 | 2.0 / 3.0 / 4.8 / 7.4 (max 2–8) |
| BATCH:budget=5 / 10 / 20 | 8 / 5 / 3 | 688 / 430 / 258 | 14 030 / 8 769 / 5 261 | 0/20 | 10 / 6 / 3 | 0.65 / 1.30 / 3.75 | 2.4 / 3.5 / 7.5 (max 3–12) |
| BATCH:budget=10,cap=5 | 5 | 430 | 8 769 | 0/20 | 6 | 1.30 | 3.5 (identical to budget=10: the cap never changes a decision; at step 13 it coincides with the budget trigger) |
| **A4 OURS (T = 10)** | 5 | **655** | 27 338 | 0/20 | **20** | **0** | 1.6 (max 5) |
| OURS T = 5 / T = 20 | 8 / 3 | 855 / 641 | 30 874 / 27 325 | 0/20 | 20 / 20 | 0 / 0 | 1.6 / 1.75 |
| TESTMON + k = 2 / 3 / 5 / 8 | 9 / 6 / 4 / 3 | 931 / 735 / 594 / 541 | ≈ 30 560–30 950 | 0/20 | 20 | 0 | 1.4–1.9 |
| TESTMON (no full check) / FULL | 0 / 18 | 330 / 1548 | 30 349 / 31 567 | 0/20 | 20 / 20 | 0 | 1.0 |

**Matched cost (the pre-registered comparison, at A4's 655 s, linear interpolation inside each family):**

| | Mean delay (steps) | Caught at injection | Mean window (edits to bisect) |
|---|---|---|---|
| A4 | **0** | **20 / 20** | 1.6 |
| cap-only, between cap = 3 and cap = 2 | 0.78 | 7.6 / 20 | 2.5 |
| additive-budget, between T = 10 and T = 5 | 0.73 | 9.5 / 20 | 2.5 |

**Equal detection:** **no batching member reaches A4's 20/20 caught at the injection step.** No batching arm run here reaches it; cap = 1, a full check at every step, would, but it was not run (inferred). Every arm with a per-edit tier does. The cheapest member of the fixed-k + per-edit family is TESTMON + k = 8 at 541 s, and plain TESTMON, with no full checks, gets there at 330 s.

**Reading:**
- **First, a construction caveat (M2).** The mutants sit in the edited functions, so **every arm with a per-edit tier gets delay 0 by construction.** The comparison below therefore shows what the mutant model allows, not evidence that A4's design is better.
- **On the primary cost (no benchmarks), A4 has more caught-at-injection than both batching families at matched cost (by construction, see summary point 1), and A4 is itself dominated** by plain TESTMON (330 s) and by TESTMON + k = 8 (541 s), both with 20/20 at injection.
  - At A4's cost, batching finds **half to about 60 %** of the mutants one step or more later: 12.4/20 late for cap-only, 10.5/20 for additive-budget.
  - Batching also leaves ≈ 2.5 candidate edits per failure.
- **The advantage comes from the per-edit tier, not from the trigger.**
  - Plain TESTMON, with no full checks, also gets 20/20 at injection at **330 s, half A4's cost**. That matches the RQ2 reading: on this mutant class the per-edit selection catches everything by construction (M2).
  - The additive-budget trigger fires at **exactly the same steps as A4** (3, 5, 8, 13, 18). So the trigger alone, without the per-edit tier, is what batching measures.
- **The secondary cost, with benchmarks, reverses the cost picture.**
  - Batching runs benchmarks only at its full checks: 5 300–15 800 s.
  - A4 runs about 27 300 s. Its profile selection collapses to all 171 cases after the first full check (finding B2), and TESTMON / FULL run all benchmarks every step (≈ 30 000 s).
  - **So once benchmark cost counts, every arm with a per-edit benchmark tier costs 1.7–6× more than batching**, ranging from 27 325 / 15 783 to 31 567 / 5 261.
  - **At A4's matched primary cost,** batching with benchmarks interpolates to ≈ 13 350 s for both families, so **A4 costs ≈ 2.0×.**
  - **Convention:** TESTMON and FULL have no benchmark selection and run all 171 cases every step. STATIC_BENCH was not in this arm set. On this evidence, A4's benchmark selection (P1 + P8) has to work, through checkpoint re-profiling, before A4 can compete on total cost.
  - The benchmark weights come from one noisy pass, and the cost varies ≈ 3.7× between passes.
- **Caveats:**
  - Only functional mutants are used, since regression detection is not measurable on networkx. Mutants sit in edited functions, which favours any per-edit tier.
  - Batching's bisection cost after a failing batch is **not** modelled (every check is green except the fault), so batching's cost is a lower bound.
  - Under the pre-registered window definition, a per-edit arm's full-check hit at the injection step counts the whole window since the previous full check. That is why A4 shows 1.6 rather than 1.0. The definition was kept as pre-registered.
  - T = 20 is cheaper than T = 10 with the same detection here. T was not retuned (rules.md).

### Slowdown oracle (networkx, performance; overnight item 2)

**Set:** 10 frozen synthetic slowdowns (`frozen/networkx.slowdowns.json`, sha256 in `frozen/FROZEN.md`), each placed in a function changed at its step. Nine call the function's body twice (`double_call`); #8 uses a list instead of a set for membership.

**Measurement** (`scripts/slowdowns_nx.py`; raw `raw/networkx/slowdowns/<i>.json`, with the plan written before each run as `<i>.plan.json`):
- Each slowdown has two clones at its state S_s, one patched. They are measured interleaved A/B with `bth.benchrun` on CPUs 2–5. The verdict is the asv rule (ratio > 1.1 and Mann-Whitney p < 0.002) on pooled samples.
- **Within reach:** the measured cases are those whose S0 profile or static reach includes the slowed function. They run 2 processes × 3 values × 3 repeats.
- **Out-of-reach spot check:** the frozen seeded sample of 10 cases (`frozen/networkx.slowdown_spotcheck.json`, seed 20261121), minus the reach. They run 1 process × 3 values × 2 repeats. **This gives 6 vs 6 samples, too few for the test: see "Safety of reach-based selection"; the column below is not evidence.**
- **On target:** "on target" below means the flagged case executes the slowed function in its S0 profile.

| # | Step | Slowed function (kind) | Reach: profile / static → measured | Within-reach verdict (FULL) | Out-of-reach spot check | Class (script) |
|---|---|---|---|---|---|---|
| 0 | 1 | `distance_regular.global_parameters` | 0 / 0 → 0 | not measurable: no case reaches it | 10 cases, 0 slower | not detected |
| 1 | 2 | `weighted.bidirectional_dijkstra` | 0 / 171 → 171 | 1 slower, **off target**: `time_connected_components('Erdos Renyi (100, 0.1)')` 1.245×, p = 0.0018 (exact: 1.27e-3); this case is in static reach (as all 171 are) but not in the S0 profile reach of `bidirectional_dijkstra`. Also 1 "faster" off target (`time_average_clustering`, 0.858×). | none left (reach = all 171) | moderate (1.2–1.5×) — **judged noise, see below** |
| 2 | 3 | `weighted._dijkstra_multisource` | 8 / 171 → 171 | **9 slower:** all **8 profiled** `time_multi_source_dijkstra` cases at **1.81–1.90×** (p = 3.2e-7), plus 1 off target (`NonNeighbors.time_complete(100)`, 1.14×) | none left | other-slower (max 1.90×) |
| 3 | 4 | `components.connected.is_connected` | 3 / 171 → 171 | 0 slower (171 same) | none left | not detected |
| 4 | 5 | `unweighted._single_shortest_path` | 0 / 171 → 171 | 0 slower (171 same) | none left | not detected |
| 5 | 6 | `dense.floyd_warshall_tree` | 0 / 0 → 0 | not measurable | 10 cases, 0 slower | not detected |
| 6 | 8 | `isomorph.could_be_isomorphic` | 0 / 0 → 0 | not measurable | 10 cases, 0 slower | not detected |
| 7 | 9 | `katz.katz_centrality_numpy` | 0 / 0 → 0 | not measurable | 10 cases, 0 slower | not detected |
| 8 | 10 | `generic._build_paths_from_predecessors` (list membership) | 1 / 171 → 171 | **1 slower, on target:** `ManyComponentsBenchmark.time_single_source_all_shortest_paths` **1.116×** (p = 4.5e-7) | none left | other-slower (max 1.12×) |
| 9 | 11 | `isomorphvf2.DiGMState.__init__` | 0 / 0 → 0 | not measurable | 10 cases, 0 slower | not detected |

**What "other-slower" means.** FULL's asv rule did flag the slowdown: at least one case is significantly slower. But the largest slowdown falls in neither strength band pre-registered for the regression set: "strong" is ≥ 2×, "moderate" is 1.2–1.5× (readiness §4.2, ruling 2). #2 peaks at 1.90×, between the bands. #8 peaks at 1.12×, below the moderate band. So "other-slower" is a real detection whose size the pre-registered bands did not foresee. It is not a miss and not noise.

**Detection by FULL.**
- **As classified by the script:** FULL detects **3 of 10** (30 %; 95 % Wilson CI **10.8–60.3 %**). These are #1, #2 and #8.
- **On target:** **2 of 10** (Wilson **5.7–51.0 %**), #2 and #8.
- **#1 is judged an oracle false positive.** Its only "slower" case never executes `bidirectional_dijkstra` in its S0 profile, and the patch only touches that function's body. Its p = 0.0018 sits just under the 0.002 threshold. The same run also produced an off-target "faster" verdict. 177 of its 1026 runs (88 of 513 on the base side) had a 1-minute load above 1.5.
  - Across the whole oracle there are **843 off-target comparisons that can yield a verdict**, plus 50 spot-check comparisons (6 v 6) that cannot: 893 in all (earlier text said "about 890"; reconciled in "W6 hostile-review checks"). Three of them gave a non-"same" verdict. That is in line with chance at α = 0.002 with many comparisons, especially since samples from one process are not independent, which makes Mann-Whitney p optimistic.
  - This is a reading, not a re-measurement. Oracle repeatability (readiness §5) would settle it.
- **The 7 slowdowns FULL misses:** 5 (#0, 5, 6, 7, 9) are reached by **no** benchmark case, by profile or by static reach. The other 2 are reached in different ways. **#3** (`is_connected`) is reached by 3 profiled cases; its ratios are 0.95–1.01. **#4** (`_single_shortest_path`) is reached **only by static reach** (profile reach 0), so it is a coverage miss. *Wording note (16:35, PM):* static reach covers **all 171 cases** for #1, #2, #3, #4 and #8 alike (the S0 static call graph over-approximates), so "reached" for #1 and #4 means statically reachable only, and is uninformative; by measured S0 profile, #1 and #4 are **not reached**. "The 5 reached slowdowns" (E3) means profile ∪ static. Double-calling either function moves no case past the asv rule.

**Safety of reach-based selection.**
- **The out-of-reach spot check has no power, and its result is withdrawn (critic review, 2026-11-22 06:06).**
  - The 50 comparisons (5 slowdowns × 10 cases) are 1 process × 3 values × 2 repeats, which gives **6 vs 6 samples**. The smallest possible two-sided exact Mann-Whitney p for 6 vs 6 is 2/924 = **0.00216, above α = 0.002**. So `bth.stats.asv_rule` cannot return "slower" however large the slowdown. Checked: fully separated samples at 3× give p = 0.00216, "same".
  - The observed spot-check p-values are multiples of 1/462; the smallest is 0.015.
  - So "0 of 50 slower" holds **by construction** and says nothing about reach safety. It is also a protocol deviation: readiness §5 asks for ≥ 5 processes.
  - **Powered re-run (PM-approved 06:10).** It is reported below.

**Profile-completeness check (powered out-of-reach spot check) (2026-11-22 06:10–07:40, 10:09–11:04 and 12:03–12:25 PKT; **complete, 5 of 5 slowdowns**).**

**What it is (relabelled per advisor review):**
- It covers only slowdowns that **no** benchmark reaches. It asks whether anything **outside the measured reach** slows down, which tests whether the S0 profiles are complete. **It is not evidence that selection is safe.**
- The #5 order effect below motivated the order arm in the A/A run.
- **Plan:** `raw/networkx/slowdowns/spotcheck_powered.plan.md`, written before measuring. It uses the same frozen 10-case sample.
- **Protocol:** 5 processes × 3 values × 1 repeat, giving **15 vs 15 samples**. The smallest attainable p is 3.4e-6 under the normal approximation used at the time (scipy 'auto'); under the **exact** test it is **1.3e-8** (corrected 2026-11-22 15:55, see "Exact-test recompute"). The #5 "faster" case reached that minimum (fully separated samples).
  - **Power:** 1.00 at 1.2× and 0.81 at 1.12×, but simulated **at 5 % noise**. The observed spread is much larger (below), so real power is lower, and only large slowdowns would reliably be caught.
  - **Fixed order:** with 1 repeat, every case ran **base first, then slowed**, with no order rotation. "Interleaved" here means alternating per case, not counterbalanced.
- **Gate:** checked before each slowdown block: WSL load ≤ 1.0 and Windows CPU ≤ 20 % for 3 × 60 s, postponing rather than labelling. It is not re-checked at the moment the block starts.
  - #5's record shows a Windows CPU reading of 21 % taken just after the gate passed.
  - #7 started at load 0.72, one check after a gate reading of 0.33.
- **Cap:** the 1.5 h cap includes driver start-up, so it fired at 07:39:32, before 06:10:22 + 5400 s.
- **Plan deviation:** the plan's "nothing else concurrently" rule was broken once, during #0 (see the table).
- **Raw files:** `raw/networkx/slowdowns/spotcheck_powered/{00,05,06,07,09}.json`, `{07,09}.partial.jsonl` and `driver.log`.

| # | Slowed function | Out-of-reach cases (all 10) | Smallest p | Ratio range | Peak load (M5) |
|---|---|---|---|---|---|
| 0 | `distance_regular.global_parameters` | **10 same, 0 slower** | 3.7e-3 | 0.75–1.15 | 0.88 (below the 1.5 noisy threshold); labelled **concurrent**, because 06:28–06:29 this session ran unit tests on Windows (`CONCURRENCY.md`). The JSON's `m5_label` was not relabelled. |
| 5 | `dense.floyd_warshall_tree` | **9 same, 0 slower**, 1 faster | 3.4e-6 (exact: 1.3e-8) | 0.63–1.24 | 1.10 |
| 6 | `isomorph.could_be_isomorphic` | **10 same, 0 slower** | 7.8e-4 | 0.94–1.21 | 0.92 |
| 7 | `katz.katz_centrality_numpy` | **10 same, 0 slower**. Measured in the top-up, 10:13–10:44, after the PC restart; the first attempt at 07:30 was cut off by the cap and nothing was saved. | 0.051 | see `07.json` | 1.62, so **noisy** (M5) |
| 9 | `isomorphvf2.DiGMState.__init__` | **9 same, 1 slower**: `time_louvain_communities('Erdos Renyi (100, 0.9)')`, **1.13×, p = 0.0019**. Measured in two parts: runs 1–4 at 10:51–11:04 (cut by the cap), runs 5–20 at 12:03–12:25 after the A/A, resumed from the checkpoint. The louvain case's base and slowed runs (runs 7–8, 12:12–12:18) both fall in the second part; no case is split. | **9.7e-5** (`time_remove_nodes_from('MultiDiGraph')`, ratio 1.099; only the ratio condition kept it "same") | 0.89–1.37 | 0.72 peak; the block started at 0.76; the second session's gate saw Windows CPU 100 % at 11:59 |

**Reading:**
- **Over all 5 slowdowns: 1 "slower" in 50 out-of-reach comparisons.**
- **By the pre-registered rule (C11), this flags #9: reach-based selection would be unsafe for it.** Reported as such.
- **Reading — possibly a false positive, not verified. The C11 flag stands; a post-hoc re-measurement (below) adds context only:**
  - `DiGMState.__init__` is in neither the static nor the S0 profile reach of the louvain case. The profile holds no `isomorphism` function at all.
  - p = 0.0019 is just under α = 0.002, and the ratio of 1.13 is just over 1.1.
  - The A/A run shows noise this close to the threshold: in repeat 0 two A/A cases had p < 0.002 and were held back only by the ratio condition. In the same #9 block a second case also reached p < 0.002 with ratio 1.099.
  - The louvain case leans slower in other blocks too: #0 1.13× (p = 0.43), #6 1.21× (p = 0.046).
  - **Against the false-positive reading:** the A/A run itself gave 0 false verdicts in 46.
  - **Post-hoc re-check (PM-approved 12:31; plan `raw/networkx/slowdowns/recheck9/plan.md`, written before measuring; PARTIAL):**
    - **Setup:** the same case at #9's state, with three clones: **base**, **slow** (#9 patch) and **base2**, a second unpatched control in the same block. 5 × 3, two rotated repeats, measured 12:37–12:54; the cap hit at 12:57. The Q3 critic subagent ran alongside (read-only; `recheck9/CONCURRENCY.md`).
    - **Cut short:** the 25 min cap stopped it after **5 of 6 runs**. Repeat 1's base run is missing, so base has 15 samples instead of 30.
    - **Consequence:** base was measured once, first in the block, so **comparisons against base are not order-balanced**. Slow vs base2 is not balanced either: slow ran before base2 in both repeats. **No comparison in the partial data is order-balanced.** Repeat 0 has the same order as the original block (base, then slow) and still reads "same". Raw: `recheck9/runs.partial.jsonl`, `recheck9/result_partial.json`.
    - **Verdicts:**

      | Comparison | Ratio | p | Verdict |
      |---|---|---|---|
      | slow vs base, repeat 0 (15 vs 15) | 0.985 | 0.59 | same |
      | slow vs base, pooled (15 base vs 30 slow) | 0.981 | 0.51 | same |
      | slow vs base2, pooled (30 vs 30) | 1.008 | 0.81 | same |
      | **control:** base2 vs base, repeat 0 | 0.978 | 0.97 | same |
      | **control:** base2 vs base, pooled (15 vs 30; the plan's rule) | 0.973 | 0.66 | same |

    - **Sample medians:** slowed-clone medians 0.0123–0.0126 s; base 0.0128 s; base2 0.0123–0.0125 s. In the original #9 block they were slow 0.01385 s against base 0.01225 s.
    - **Plan outcome "same / same": the re-check fails to confirm the original "slower" verdict.**
    - **The pre-registered C11 flag for #9 still stands as the primary result.** The re-check adds context only: the 1.13× was not reproduced, under a stable control. It is consistent with the original being 1 false positive among 50 comparisons at α = 0.002 (under 50 nulls the chance of ≥ 1 false "slower" is ≈ 5 %, from 1 − 0.999⁵⁰ for one-sided "slower" at two-sided α. ≈ 9.5 % is the upper bound for either direction. Both ignore the ratio condition and the shared base runs), but does not prove it.
  - #7 was measured after the PC restart, with ≈ 1.6× slower per-process setup.
  - The A/A power figures below apply: for 2 of the 3 sampled `benchmark_algorithms` cases (of 49), only ≈ 2× slowdowns are reliably detectable.
  - This is a spot check over 5 slowdowns × 10 seeded cases = 50 comparisons, not a miss rate.
  - The A/A noise floor (Q2) gives the false-verdict rate against which it is read.
- **One strong off-target verdict:**
  - **What:** in #5, `time_eigenvector_centrality_numpy('Erdos Renyi (100, 0.5)')` was **faster** in the slowed clone, 0.628×, with fully separated samples (p = 3.4e-6 by the normal approximation; 1.3e-8 exact).
  - **Why it is not a slowdown effect:** a double call inside `floyd_warshall_tree` cannot speed up eigenvector centrality.
  - **Evidence for an order or warm-up effect:** it was the **first case of its block** and ran base first.
    - The base side took 183 s of wall time against 100 s for the slowed side.
    - The base samples include two outliers (0.0119, 0.0128 s), and even the rest sit at ≈ 0.0035 s against ≈ 0.0022 s for the slowed side.
    - Load rose to 1.10 during the base run, the block's peak.
    - A cold-start effect on the first case, combined with the fixed order, is the likely cause. That is not verified. The A/A run (Q2) has the same fixed A-then-B order, so it will show whether such an order effect exists.
  - **Why it matters:** the oracle can return confident off-target verdicts. That is why the A/A run matters before any slowdown verdict is trusted. It is not a safety failure: "faster" is not a missed slowdown.
- **Also noted:**
  - "Same" verdicts span ratios **0.755–1.236**: per-case medians move by up to ±24 % between two clones with no relevant change.
  - In #6, two cases had p below α but small ratios (`harmonic_centrality` 0.95, p = 7.8e-4; `multi_source_dijkstra` 1.034, p = 1.2e-3). Only the asv rule's ratio > 1.1 condition kept them "same". So the p-test alone flags small off-target shifts.
  - **No CI-based M5 label** ("measured", CI < 10 %) is applied to these timings. They are used only for verdicts, which are labelled by load.
- **Also:** for the other 5 slowdowns, static reach covered all 171 cases, so there was nothing outside reach to spot-check. This is an over-approximation: `benchmark_algorithms` imports everything.
- **Within-reach caveat (first oracle run):** the two off-target "slower" verdicts (#1, #2's `NonNeighbors`) lie **outside profile reach but inside static reach**. If they were real, a profile-based selection (A4/P1) would have missed them. We judge them noise because a benchmark that never runs the function cannot be slowed by a change in its body. This rests on the stated assumption that import-time code is unaffected.

**Tie to B1: this is a benchmark-coverage finding.**
- **7 of the 10 slowed functions are executed by no benchmark case in its S0 profile:** #0, 1, 4, 5, 6, 7, 9. Excluding #6, which sits on the non-optimization step 8: 6 of 9.
- This matches B1, where 9 of 15 true optimizations (12 of 18 replayed edits) are executed by no benchmark.
- On networkx, **two limits come before any selection rule** (advisor review 13:05). No selection can beat FULL, and FULL sees 2–3 of these 10 slowdowns.
  - **(a) Coverage (B1):** 7 of 10 slowed functions are executed by no benchmark: #0, 1, 4, 5, 6, 7 and 9. #4 (`_single_shortest_path`) is one of these, so it is a **coverage miss, not a power miss**.
  - **(b) Oracle power (A/A):** for 2 of the 3 sampled `benchmark_algorithms` cases, only ≈ 2× slowdowns are reliably detected.
    - #3 (`is_connected`) is reached by 3 profiled `eigenvector_centrality_numpy` cases in that module. Their ratios are 0.95–1.01, p ≥ 0.22.
    - So a large hidden slowdown is unlikely, but a small real one (< ≈ 1.1×) cannot be excluded: #3 may be a **power miss of a small effect**. **Superseded (16:30):** the slowed function is ≈ 0.5 % of its reaching cases' time, so the expected effect is ≈ 1.005×: #3 is a **dilution miss** (see "W6 hostile-review checks").
- Selection safety can therefore only be judged on #2 and #8:
  - Both are inside profile reach (8/8 and 1/1 cases) and inside static reach.
  - A changed-module benchmark rule (A3) selects 0 cases and would miss both.
  - **The per-arm regression simulation is not yet run.**

**Primary, pre-registered result (PM ruling 2026-11-22 05:50).**
**Regression safety of reduced selection is not measurable on networkx with the frozen set.**
- By the frozen entry rule (≥ 1 case ≥ 2×, or 1.2–1.5× for moderate), the only candidate is #1, and #1 is off target and judged noise. So there are **0 on-target detections in the pre-set bands**, and the pre-registered regression set is empty.
- **The slowdown result in its own right:** FULL itself detects **at most 2–3 of 10** frozen slowdowns. On networkx, the project's benchmark coverage (B1) and the oracle's power (A/A) both limit regression detection, ahead of any selection rule.

**Post-hoc exploratory analysis — NOT pre-registered, never merged into the headline** (logged in `raw/networkx/bench/LABELS.md`).
- #2 (1.90×, 8/8 profiled cases) and #8 (1.12×, 1/1 profiled case) are real on-target FULL detections outside the pre-set bands.
- Both lie inside the profile reach and the static reach. So A4/P1 (profile), A5 (static) and every arm that runs all benchmarks would select the slowed cases. A3 (changed-module benchmark rule, 0 cases) would miss both.
- This is a reach argument on 2 slowdowns. The per-arm regression simulation is not run.

**Load labels (M5).**
- 410 of 5330 benchmark runs (7.7 %) had a 1-minute load > 1.5 at the before or after sample. Per M5 those runs are **noisy**: #1 177, #3 160, #4 29, #7 21, #2 12, #5 11; #0, 6, 8 and 9 had none.
- The two on-target verdicts have p ≈ 1e-7, far from the threshold.
- The runs for #8 never exceeded 1.45.

### Benchmark A/A noise floor and order effect (networkx; Q2, re-run 11:05–11:53 PKT)

**Plan:** `raw/networkx/bench/aa/aa_noise.plan.md`, with amendments 1 and 2, all written before the measurement. The first 26-case run (07:49–09:14) hit its cap and **saved nothing**; that is the reason for amendment 2 and the per-run checkpoints.
- **Design:** S0 against S0 in two independent clones, so any verdict is a false one.
- **Cases:** the frozen 23-case subset (`frozen/networkx.aa_noise_sample_cut23.json`: 3 `benchmark_algorithms` + 20 others, seeded).
- **Protocol:** 5 processes × 3 values, 15 vs 15 samples per repeat.
  - Repeat 0 runs **A first** (the oracle's fixed order); repeat 1 runs **B first**. Pooling both gives ABBA.
- **Load:** the gate passed at 11:10:49 (load 0.37, Windows CPU 9 %). Peak run load was 1.06, below the 1.5 noisy threshold. Nothing else ran.
- **Raw files:** `aa/runs.partial.jsonl` (92 runs, with `t_start`/`t_end`), `aa/raw_runs.json`, `aa/aa_result.json`.

| | Fixed order (repeat 0) | Reversed (repeat 1) | ABBA (pooled, 30 vs 30) |
|---|---|---|---|
| False "slower" / false "faster" | **0 / 0 of 23** | **0 / 0 of 23** | **0 / 0 of 23** |
| Ratio spread of the "same" verdicts: min / p05 / median / p95 / max | 0.87 / 0.96 / 1.01 / 1.09 / **1.77** | 0.76 / 0.93 / 1.00 / 1.05 / **1.49** (computed 12:27 from `aa_result.json`, linear percentile) | 0.98 / 0.98 / 1.01 / 1.08 / 1.12 |

**Reading:**
- **Noise floor:** the asv rule gave **0 false verdicts in 46 per-repeat A/A comparisons** (95 % Wilson upper bound 7.7 %; 0/23 per arm, upper bound 14.3 %).
  - The 46 comparisons are the same 23 cases twice, not independent, so 7.7 % is optimistic.
  - Repeatability (plan item 3) is trivial: 0 non-"same" verdicts in either repeat.
  - This fits the slowdown oracle's 3 off-target non-"same" verdicts in 843 comparisons that can yield a verdict. It cannot separate a 0.3 % false rate from zero.
- **The A/A noise sits close to the threshold** (critic review, 11:58):
  - In repeat 0, two cases passed p < 0.002 and were stopped only by the ratio condition: `CommonNeighbors.time_complete(100)` (p = 9.7e-5, ratio 1.094) and a `k_factor` case (p = 0.0014, ratio 1.032).
  - Repeat 1 also shows large ratios: `CommonNeighbors.time_complete(100)` 0.761 and `time_star_center_rim(100)` 1.485, both p = 0.007.
  - So "0/46" means no false verdict, but the noise is not far from producing one.
- **The ratio part of the rule passes large A/A differences.** In the fixed order, `time_tarjan_scc('Erdos Renyi (1000, 0.01)')` had a **1.77× ratio** with p = 0.051, so it stayed "same". Its sample coefficient of variation is 0.63.
  - With ABBA pooling the spread narrows to 0.98–1.12.
  - So under a fixed order a single noisy case can show a large spurious ratio. Only the p-value keeps it from a false verdict, and the same p-value hides real slowdowns of that size (see power).
- **No order effect:**
  - Per case, first-run / second-run time has median **0.99**. The first run was slower in only 10 of 23 cases (sign test p = 0.68).
  - The first case of the run (`tarjan_scc`) showed the opposite direction to #5: its first run was *faster* (0.75).
  - **No order effect was detected across cases, but this test has low power:**
    - 23 cases, only 3 of them `benchmark_algorithms`.
    - The first case of the run is a single observation (n = 1).
    - Samples cluster by process: `tarjan_scc` A had one process at ≈ 7 ms against ≈ 2 ms for the others.
  - **#5's cause is unresolved.** #5 was a run-level shift, not scatter: all 15 base samples sat at 3.3–4.8 ms against ≈ 2.2 ms, fully separated. A first-in-block effect is consistent with it. Here the first A/A run likewise took longer in wall time (196 s against 132 s), but not in its samples.
- **Power from measured noise** replaces the assumed 5 % noise. It is a bootstrap of 15 vs 15 from each case's pooled samples, seed 20261122.
  - It ignores within-process correlation, so these figures are **optimistic**.

  | Slowdown | 1.12× | 1.2× | 1.5× | 2.0× |
  |---|---|---|---|---|
  | all 23 cases (median) | 0.48 | 0.91 | 1.00 | 1.00 |
  | 3 `benchmark_algorithms` cases (median) | **0.27** | **0.35** | **0.73** | 0.96 |
  | — per case, at 1.2× | | 0.13 / 0.345 / 1.00 | | |
  | 20 other cases | 0.48 | 0.92 | 1.00 | 1.00 |

  - Per-case sample CV: median 0.11 on the A side, 0.097 on B, 0.104 pooled; max 0.63.
  - **Consequence:**
    - For **2 of the 3** sampled `benchmark_algorithms` cases (the module most edits and slowdowns sit behind), the oracle reliably catches only about 2× slowdowns; the third case is fine at 1.12×. These are **3 sampled cases out of 49** `benchmark_algorithms` cases, so this is indicative, not a module-wide estimate.
    - The bootstrap mixes A/B clone differences and ignores process clustering.
    - A "not detected by FULL" on a moderate slowdown there can be a power failure of the oracle, not absent coverage. #3 may be such a miss, of a small effect only (its 3 profiled cases read 0.95–1.01). **#4 is a coverage miss:** no benchmark executes it.
    - This qualifies the slowdown-oracle reading. It does not change the B1 coverage count, which is about reach, not power.
- **Overrun again, now measured per run (PM 10:09: report it as a finding).**
  - The 92 runs took **2483 s** against **753 s expected**. The expectation is the item-4 pass's per-case wall time × 2.5 for 5 processes.
  - **The whole excess is in the `benchmark_algorithms` runs:** 132–235 s each, **2.6–5.9× expected** (median 4.0×). The cheap cases ran at 0.74–1.14× (median 0.90×).
  - **Per-process `benchmark_algorithms` cost across the day** (derivation: per-case wall ÷ processes, ignoring the timing loops, which are < 1 s; this assumes cost is linear in the number of processes):
    - overnight: ≈ 4.4 s (slowdown base passes #2, #3, #4, #8: medians 8.6–8.8 s ÷ 2), but **≈ 18 s for #1** (36.4 s ÷ 2, under load > 1.5);
    - item 4 (05:30): ≈ 13 s (27 s ÷ 2; load 1.63 at start);
    - morning spot check: ≈ 23 s (114 s ÷ 5);
    - now: **26–47 s, median 40 s.**
  - So **one module's per-process setup cost** (`benchmark_algorithms`) varies about 10× across the day and protocols, and does **not** rise monotonically.
    - Within one protocol the spread is smaller: ≈ 1.7× for 5 × 3 (morning vs now) and ≈ 3× for 2 × 3 (overnight vs item 4), or ≈ 4.2× including #1's loaded overnight pass (4.3 → 18.2 s).
    - The **timed samples stayed stable** (machine-state finding).
    - Serial test timings were stable between the first runs and the overnight re-runs (0.96–1.20×, excluding S16/S17). Tests were **not** re-timed after the restart. Load stayed below 1.1 **during this run**; item 4 and #1 ran above 1.5. The cause is still **unknown** (see the machine-state finding in RQ1). The asv verdicts use the timing samples, which this does not inflate. What it inflates is the **cost** of a FULL benchmark pass.

### Pre-registered noise floor (1 + 3·σ_noise) — applied where σ exists (advisor review 13:05; computed, no new timing)

**The rule** (readiness §4.2 and §5, rules.md §5): a regression additionally needs **ratio > 1 + 3·σ_noise(b)**. σ_noise(b) comes from the per-benchmark A/A ratio distribution of an S0-vs-S0 control with **5 repeats**. Cases where the asv rule fires but the ratio is below the floor are counted and reported.

**Until now this rule was applied nowhere.** That is a gap: every slowdown and spot-check verdict above uses the asv rule alone.

**What exists:** σ_noise for **23 of 171 cases** only, from the A/A re-run (`raw/networkx/bench/aa/`), with **2 repeats, not 5**. Two estimates are in `aa/sigma_noise.json`:
- **σ_rep:** the standard deviation of the two per-repeat A/A ratios. It follows the plan's definition, but with n = 2 it is very rough.
- **σ_boot:** the bootstrap standard deviation of the median ratio, 15 vs 15 from the pooled samples, 300 draws, seed 20261122.
- **Resulting floors 1 + 3σ:** median 1.07 (σ_rep) and 1.09 (σ_boot). Range 1.02–2.64 and 1.04–1.48. Highest: `tarjan_scc` 2.64 / 1.48, `CommonNeighbors.time_star_center_rim(100)` 1.97 / 1.41.

**Verdicts it would decide:** **none of the flagged "slower" cases is among the 23 cases with σ.** These are #1 `connected_components('ER (100, 0.1)')`, #2's 8 `multi_source_dijkstra` cases and `NonNeighbors.time_complete(100)`, #8 `ManyComponentsBenchmark.time_single_source_all_shortest_paths`, and #9 `louvain_communities('ER (100, 0.9)')`. **So the pre-registered rule cannot be applied to any of them.**

**Labelled proxy only, not the pre-registered rule:** the floors of A/A cases from the same benchmark class.

| Verdict | Ratio | Proxy floor (same class): σ_rep / σ_boot | Reading |
|---|---|---|---|
| #1 off-target (ER (100, **0.1**)) | 1.245 | sibling `connected_components('ER (100, **0.9**)')` 1.28 / 1.22 | **ambiguous:** below the σ_rep floor, above the σ_boot floor |
| #9 out-of-reach (C11 flag) | 1.130 | UndirectedAlgorithmBenchmarks 1.05–1.28 / 1.04–1.22 | inside the band for one sibling, above it for the other: ambiguous |
| #2 off-target `NonNeighbors` | 1.140 | `NonNeighbors.time_star_center(10)` 1.03 / 1.08; CommonNeighbors up to 1.97 / 1.41 | ambiguous |
| #2 on-target (8 cases) | 1.81–1.90 | no `benchmark_shortest_path` case in the A/A | above every A/A floor except `tarjan_scc` (σ_rep) and one CommonNeighbors case |
| #8 on-target | 1.116 | no `benchmark_many_components` case in the A/A | above the median floors (1.07 / 1.09), below many individual floors |

**Reading:**
- #2's on-target detection (≈ 1.85×) would very likely survive the noise floor.
- #1, #8 and #9 sit **inside or at the edge of the noise band** of comparable cases. Under the pre-registered floor they might not count as regressions, but this cannot be decided without σ for those cases.
- The **C11 flag for #9 stands**: the floor cannot be applied to its case.

**Deviation (recorded):**
- The noise-floor control was run on **23 of 171 cases with 2 repeats**, not on all cases with 5 repeats as pre-registered. The cause: the 1.5 h caps, and the failed first A/A run.
- So σ_noise is **missing for 148 cases**, including every case with a "slower" verdict. The 1 + 3σ condition is therefore **not applied** to any reported verdict. The proxy table above is post hoc.
- **Two further departures:**
  - Readiness §5 asks for a FULL interleaved control; the A/A covered a subset.
  - σ comes from **S0**, while the verdicts were made at states S1–S11.
- `aa/sigma_noise.json` has **no `meta` block**, unlike the other raw files.

### (b) σ_noise for the 12 flagged verdicts, and the pre-registered 1 + 3σ floor applied (night item 1, 15:37–16:42)

- **Plan:** written 15:32, hashed in `FROZEN.md` at 15:33: `raw/networkx/bench/aa_flagged/plan.md`. Analysis frozen in `scripts/night_analyse.py`.
  - Amendment 1 (15:35, before any run): the gate's Windows-CPU probe now reads the telemetry file.
  - Amendment 2 (15:50, before any analysis): the exact test is primary.
- **Time:** planned 35–55 min. Actual 65 min: ≈ 43 min of runs plus 21 min of per-run gate waits.
- **Raw data:** `raw/networkx/bench/aa_flagged/s{02,08,01,09}.json`. The result is `analysis_aa.json`.
- **Design:** an A/A at **each verdict's own state and protocol**, 5 repeats, with the order rotated every repeat:
  - #2's 9 cases, #8 and #1 at 2 processes × 3 values;
  - #9 at 5 × 3.
- **Run conditions:**
  - 120 runs, 0 errors, all 4 blocks labelled **measured-window**.
  - Peak run load 0.46–0.80. No run had `pre_gate.ok = False`. The per-run gate postponed for 1,285 s in total.
  - W3's concurrent compute (`night-2026-11-22/CONCURRENCY.md`) ran at nice 19 on CPUs 0–1. The benchmark processes' affinity (2–5) comes from the protocol and was not re-verified per run.
  - The `find /` mistake (15:45:30–15:47:25) fell between blocks s08 and s01 (s08 ended 15:43:31, s01 started 15:48:12), so it overlaps no run.
  - The slow_share job (16:26:40–16:30:38) fell between s09's runs B2 and B3.
  - **One overlap:** run s01 B repeat 0 (15:50:08–15:51:07) overlapped W3's 15:49–15:51 compute (unit tests, the exact recompute). That repeat has s01's largest ratio (1.56).
    - Dropping it gives σ ≈ 0.23 and a floor of ≈ 1.69. The verdict is unchanged (1.245 < 1.69).
- **Rule:** σ_rep = the SD of the 5 per-repeat A/A ratios; floor = 1 + 3σ_rep. A verdict survives iff its original ratio > floor. σ_boot is the sensitivity check.

| Verdict | Original ratio | σ_rep | Floor 1 + 3σ_rep | Survives? | Floor (σ_boot) | A/A pooled verdict |
|---|---|---|---|---|---|---|
| #2 on target, 8 `multi_source_dijkstra` atlas cases | 1.81–1.90 | 0.025–0.109 | 1.08–1.33 | **yes, 8/8** | 1.15–1.31: yes, 8/8 | same (8/8) |
| #2 off target, `NonNeighbors.time_complete(100)` | 1.140 | 0.076 | 1.228 | **no** | 1.194: no | same |
| #8 on target, `ManyComponents...time_single_source_all_shortest_paths` | 1.116 | **0.393** | **2.18** | **no** | 1.52: no | **slower** (A/A pooled ratio 1.129) |
| #1 off target, `connected_components('ER (100, 0.1)')` | 1.245 | 0.271 | 1.81 | **no** | 1.61: no | same |
| #9 profile-completeness flag, `louvain('ER (100, 0.9)')` | 1.130 | 0.047 | **1.140** | **no** (narrowly) | 1.22: no | same |

**What changes (pre-registered rule, now applicable to every flagged verdict):**
- **Only #2's 8 on-target verdicts clear the noise floor.** Counting slowdowns, with the 10 frozen slowdowns as the denominator, FULL detects on target and above 1 + 3σ **1 of 10 (#2)**. The Wilson 95 % CI is 1.8–40.4 %, treating the slowdowns as independent.
  - #2 counts once, although it survives on 8 cases. Those 8 atlas cases share one code path.
  - For #8 and #1 the floors (2.18 and 1.81) mean those cases **cannot detect** a slowdown of the size seen. That is "not detectable at this noise", not "not a regression".
  - It was 2 of 10 by the asv rule alone. The asv-rule figures stay reported for continuity.
- **#8's original verdict (1.116×) is indistinguishable from A/A behaviour.** Its own A/A pooled test also says "slower", with an A/A pooled ratio of 1.129, which is above the original 1.116. The noise comes from 2 of the 5 repeats (1.34 and 1.96).
  - This is 1 false verdict among the 12 pooled A/A tests here, against 0 of 46 earlier.
  - **No false-positive rate is estimated from these 12**: 9 of them share one code path, and the cases were chosen because they were flagged.
- **#1, #2's `NonNeighbors` and #9 fall within the noise floor.** That matches the earlier reading of #1 and NonNeighbors as noise (off target). #9's 1.130 is just below its floor of 1.140.
  - So the **C11 flag for #9 does not survive its floor.** The profile-completeness check reads: **1 of 50 asv-rule flags, and it does not survive its floor (1.130 vs 1.140).** The other 49 cases were not asv-slower, so the floor was not applied to them.
  - The post-hoc re-check (0.97–1.01) is a separate measurement and also did not reproduce the flag.
  - This is still **not** a safety claim: the check has the power limits stated in its section.
- **Deviation N8 is closed for the 12 flagged cases only.** The other 159 cases still have no σ.
- **Stated deviation from §5:** the A/A ran at the verdicts' own states, not at S0 (plan).
- **Caveat, for every row:** σ_rep rests on 5 ratios (4 df), so its 95 % CI is roughly 0.6–2.9× the estimate, and every floor is uncertain.
  - #2's 8 survivals are robust: they also pass under σ_boot, and the lowest floor is 1.075 against ratios ≥ 1.81.
  - For #9 the margin (1.130 vs 1.140) is far smaller than that uncertainty. The verdict follows the frozen rule, but #9 should be read as "at the noise floor".
- **Order:** the order was rotated per repeat, so A ran first in repeats 0, 2 and 4. An order effect is therefore not excluded for the noisy cases (#8, #1).

### E3 tier 1: slowdown-oracle repeatability on the 14 verdict-relevant cases (night item 2; 16:45–17:59 and 21:10–21:13)

- **Plan** (frozen 15:33): `raw/networkx/slowdowns/repeat/plan.md`.
- **Raw data:** `repeat/t1_{02,08,03,01}.json`. The frozen analysis output is `repeat/analysis_rep.json` (exact test primary; the old test gives identical statuses here).
- **Design:** each slowdown at its own state, base vs base + patch, 2 × 3, **4 repeats** in the order base-first, slow-first, base-first, slow-first. The pooled sample is 24 v 24, against the original 18 v 18.
- **Run conditions:**
  - 112 runs, all 4 blocks **measured-window**, no run with `pre_gate.ok = False`. Peak run load 0.55–1.41. The per-run gate waited 1,928 s in total.
  - **#1's block spans the cap and the restart:** 6 runs at 17:45–17:59, then the item's 75-min cap expired (≈ 18:00).
    - The 17:59–21:10 gap was block-gate starvation (Windows CPU > 20 %, from the owner's other project; queue.log), then the 19:50 stop (amendment 4).
    - The last 2 runs (repeat 3) ran at 21:10–21:13, after the automatic restart.
    - Its second order-balanced pair (repeats 2 + 3) therefore mixes runs 3 hours apart. That pair's ratio (0.965) matches pair 0's, so there is no visible effect. The gap does not touch any other block.

| Slowdown: case(s) | Original verdict | Now, pooled 24 v 24 (exact) | The two order-balanced pairs | Agree |
|---|---|---|---|---|
| #2 on target, 8 atlas `multi_source_dijkstra` cases | slower, 1.81–1.90× | **slower, 1.76–1.90×**, p ≈ 3e-9 | slower, slower (8/8) | **8/8** |
| #2 off target, `NonNeighbors.time_complete(100)` | slower, 1.14× | **same, 0.977×** | same, same | no |
| #8 on target, `ManyComponents...all_shortest_paths` | slower, 1.116× | **slower, 1.202×**, p = 1.3e-3 | same, same (p = 0.004 and 0.078) | same status, but uninformative (see below) |
| #3 on target, 3 `eigenvector_centrality_numpy` cases | same | **same** (0.97–1.24×; the 1.24× case has p = 0.012) | same, same | **3/3** |
| #1 off target, `connected_components('ER (100, 0.1)')` | slower, 1.245× | **same, 0.966×** | same, same | no |

**Reading** (the pre-registered E3 questions):
- **#2's on-target detection repeats** at the same size (8/8). It also clears its (b) floors (1.08–1.33).
- **#1's and NonNeighbors' off-target "slower" verdicts do not repeat.** Both are now "same", at ≈ 0.97×. That is consistent with their being noise, as judged before and as their (b) floors already showed.
- **#8's repeated "slower" is no evidence of a real effect.** The (b) A/A at the same state, with no patch, also gave "slower" (1.129×), so agreement is uninformative here.
  - Each order-balanced 12 v 12 pair is "same", and the ratio (1.20×) is far below its (b) floor of 2.18.
  - **It does not clear the noise floor**, the same reading as (b).
- **#3: no evidence of a detectable effect at this protocol** (3/3 same at 24 v 24). This fits the dilution finding: ≈ 0.5 % share, so ≈ 1.005× expected.
  - A null on the heavy `benchmark_algorithms` module is weak evidence: the A/A power at 1.2× is only ≈ 0.4 (15 v 15, exact).
  - On `ER (100, 0.1)`, pair 0 gave 1.36× (p = 0.03) and the pooled 1.24× has p = 0.012, so a 1.2× effect there is not excluded. No σ exists for these 3 cases.
- **Overall:** 12 of 14 verdicts agree with the original. The 2 disagreements are the two off-target flags, which turn into "same". Transition counts per block are in `analysis_rep.json`.
  - The "1 of 10 above the noise floor (#2)" result from (b) is **unchanged by this repeat**. The repeat covered only #1, #2, #3 and #8; #4 has no case in tier 1, and #0, #5, #6, #7 and #9 were not repeated.
- **Not done yet:** tier 2 (the other cases, 2 repeats) runs later tonight, if time allows.

### (d) Three repeated FULL networkx passes with machine telemetry (night item 3; 19:07–23:42, with the 19:50–21:22 stop)

- **Plan** (frozen 15:33): `raw/networkx/bench/drift/plan.md`.
- **Raw data:** `drift/{canary0..3,pass0..2}.json`. The frozen analysis output is `drift/analysis_drift.json`; telemetry is in `raw/telemetry/{win,wsl}-20261122.jsonl`.
- **Protocol:** state S0, 171 cases, 2 processes × 3 values, CPUs 2–5, a 3-case canary before, between and after the passes.
- **Descriptive only (no root-cause hunting, per plan).**

| Block | Time | Σ run wall | `benchmark_algorithms` (49 cases) | Other 7 modules (122 cases) | Timed loops (Σ samples × number) | Median `benchmark_algorithms` run | M5 label |
|---|---|---|---|---|---|---|---|
| pass 0 | 19:10–22:34 ¹ | **2,984 s** | 2,888 s | 96 s | 155 s | 58.8 s | noisy ² |
| pass 1 | 22:38–23:14 | **1,694 s** | 1,601 s | 93 s | 146 s | 27.6 s | noisy ² |
| pass 2 | 23:15–23:41 | **1,217 s** | 1,125 s | 93 s | 144 s | 20.6 s | noisy ² |

¹ Pass 0 spans the stop: its first 7 runs (19:10–19:49) mostly ran after full 10-min gate waits, and the remaining 164 ran 21:22–22:34. The Σ run wall excludes the gate waits and the stop.

² Each pass has 1 run with load > 1.5 (1.61, 1.68 and 1.56). Pass 0 also has 3 runs with `pre_gate.ok = False`, each started after the full 601 s wait with gate Windows CPU at 26–28 %: runs 1 and 2 (19:21 and 19:32, in the 19:10–19:49 starvation) and run 14 (21:40, after the restart). These are reported, not dropped.

| Canary (the same 3 cases) | Time | `connected_components('ER (100, 0.9)')` run | 2 cheap `GraphBenchmark` cases |
|---|---|---|---|
| canary 0 | 19:07 | 98.2 s | 0.53 + 0.56 s |
| canary 1 | 22:35 | 38.1 s | 0.47 + 0.56 s |
| canary 2 | 23:14 | 26.8 s | 0.53 + 0.52 s |
| canary 3 | 23:41 | 9.6 s | 0.45 + 0.60 s |

**Reading** (descriptive):
- **The FULL-pass cost moved 2.5× in one evening** (2,984 → 1,217 s, 2.45×). **1,763 s of the 1,767 s drop is in `benchmark_algorithms`'s per-run cost** (median run 58.8 → 20.6 s; the canary's algorithm case went 98 → 10 s).
  - The other 122 cases stayed at 93–96 s per pass (95.9, 92.6, 92.8).
  - The **timed loops stayed at 144–155 s**, and the cheap canary cases stayed at ≈ 0.5 s.
  - This repeats, within one night and with telemetry, the earlier machine-state finding. **The movement is in wall time outside the timed loops** (that module's setup and other per-run overhead), not in the loops. Which part of that overhead moved was not measured.
- **Telemetry shows no obvious covariate that moves with the drift; no test was run:**
  - Mean Windows CPU per block was 14–22 %. The per-run gate held run starts to ≤ 20 % except for the 3 `ok = False` runs, with excursions up to 94 % during runs.
  - **`% Processor Performance`:** pass means 151 / 156 / 159, so it rose slightly as the cost fell; canary means 139–164. Its minimum reads 0 one to three times per pass (2 of pass 0's zeros fall inside the stop), which looks like a counter glitch and is not interpreted.
  - WSL load averaged 0.4–0.8.
  - **Pass 0's telemetry window (19:10–22:34) spans the 19:50–21:22 stop**, which is 45 % of its samples. Split: before the stop 31 % CPU, perf 158; during the stop 17.6 %, 144; after it 21.5 %, 156. So pass 0's means are not comparable with passes 1 and 2. The canary windows hold only 1–12 samples.
  - **The cause stays unknown**, as the plan allows.
- **R1 update (a range over passes, never one pass):**
  - The 9 measured FULL networkx passes (6 earlier + 3 tonight) give a Σ run wall of **659–2,984 s**.
  - The timed loops give **132–171 s** across all of them.
  - `benchmark_algorithms` share tonight: 92.4–96.8 %. Together with the earlier 86.9–95.5 %, the range is 86.9–96.8 %.
  - So benchmarks are ≈ **8–34×** build + tests (≈ 87 s). Most of the spread is wall time outside the timed loops in one module.
- **What E5 (setup-cached, next night) must answer:** what is left when that setup is paid once. The timed loops (144–155 s tonight) are the lower bound.

### Pass labels for the 9 FULL networkx passes: single source of truth (PM 23:52; `scripts/pass_labels.py` → `raw/networkx/bench/pass_labels.json`)

- **One uniform rule** (the M5 run-level rule, as frozen for the night queue): a pass is **noisy** if any of its runs has load > 1.5 (max of before and after) or `pre_gate.ok = False`.
- Recorded labels are shown next to it. **Cite the rule label.** This supersedes the "5 of 9" count given at 23:50 and the corrected LABELS.md line.

| Pass | Kind | Runs | Max run load | Runs > 1.5 | Gate not ok | Wall (s) | Rule label | Recorded label (source) |
|---|---|---|---|---|---|---|---|---|
| item4-S0 | dedicated FULL pass, S0 | 171 | 1.58 | 1 | 0 | 1668 | **noisy** | noisy (LABELS.md: load 1.63 at start) |
| oracle01-base | base side of the #1 oracle ¹ | 513 | 1.99 | 88 | 0 | 2444 | **noisy** | noisy (results.md RQ1) |
| oracle02-base | base side of the #2 oracle ¹ | 513 | 2.10 | 6 | 0 | 751 | **noisy** | none recorded |
| oracle03-base | base side of the #3 oracle ¹ | 513 | 2.20 | 81 | 0 | 659 | **noisy** | none recorded |
| oracle04-base | base side of the #4 oracle ¹ | 513 | 1.62 | 15 | 0 | 665 | **noisy** | none recorded |
| oracle08-base | base side of the #8 oracle ¹ | 513 | 1.45 | 0 | 0 | 708 | **measured-window** | none recorded |
| drift-pass0 | dedicated FULL pass, S0 | 171 | 1.61 | 1 | 3 | 2984 | **noisy** | noisy (driver) |
| drift-pass1 | dedicated FULL pass, S0 | 171 | 1.68 | 1 | 0 | 1694 | **noisy** | noisy (driver) |
| drift-pass2 | dedicated FULL pass, S0 | 171 | 1.56 | 1 | 0 | 1218 | **noisy** | noisy (driver) |

¹ 3 interleaved A/B passes of the unpatched clone. Runs are counted over all 3; wall is per pass (Σ / 3).

- **The gate column can be measured only for the drift passes.** The S0 and oracle runs recorded no `pre_gate`, so their 0 means "not recorded". Their rule labels rest on load alone.
- **Wall is run time only**, excluding gate waits: drift pass 0's total wall was 4,290 s against a run sum of 2,984 s.

- **By the uniform rule, 8 of 9 passes are noisy.** The only measured-window pass is the #8 base side, which is one side of an interleaved A/B oracle, not a dedicated FULL pass.
- Item 4 and drift passes 1–2 are noisy because of a single run. Item 4 also had a start load of 1.63, and drift pass 0 has 3 gate failures besides. The R1 cost range (659–2,984 s, run time only, excluding gate waits) is therefore a range over noisy-labelled passes. The paper must say so.

### (c) Two FULL asv benchmark passes for bottleneck (night item 4; 23:44–00:23)

- **Plan** (frozen 15:33): `raw/bottleneck/bench/plan.md`.
- **Raw data:** `raw/bottleneck/bench/pass{0,1}.json`. The frozen analysis output is `analysis_bn.json`.
- **Protocol:** state `f51ed862`, 840 time cases, 2 processes × 3 values, CPUs 2–5, the `bn38` venv.

| Pass | Time | Σ run wall | move | reduce | nonreduce_axis | nonreduce | Timed loops | Runs > 1.5 / gate not ok | Label |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 23:44–00:03 | **544 s** | 183 s | 256 s | 102 s | 3.4 s | 146 s | 1 / 0 | noisy (1 run) |
| 1 | 00:03–00:23 | **547 s** | 176 s | 261 s | 107 s | 3.5 s | 149 s | 1 / 0 | noisy (1 run) |

- 0 errors. The per-run gate waited 580 s and 641 s per pass. Mean Windows CPU was 18.8 % and 17.7 %.
- **The two passes agree within 0.5 %** (544 vs 547 s), unlike networkx's `benchmark_algorithms`-dominated passes.
  - Per-run wall is 0.65 s on average, 27 % of it in timed loops.
  - The setup content was not examined.
- **R1 second-project row (C extension):**
  - benchmarks ≈ 545 s;
  - clean build 4.7–5.4 s and full tests ≈ 24 s (results.md RQ1; noisy-labelled);
  - so **benchmarks ≈ 18.5–19× build + tests** (545 / 28.7–29.4 s; one state, two passes, both labelled noisy).
  - About 27 % of the benchmark wall is in timed loops (146–149 s). The non-loop time was not decomposed.
- **Reading:** on this C-extension project too, benchmarks dominate per-edit validation cost. The observed ratio is ≈ 18.5–19×: 840 cases at ≈ 0.65 s each. What drives the non-loop time was not measured.
- **Not claimed:** anything beyond one state. The build share for this project stays ≈ 16–18 % of build + tests, and is ≈ 0.8–0.9 % once benchmarks count.

### E3 tier 2: slowdown-oracle repeat on the remaining cases (night item 5; 00:25–06:25, hard stop)

- **Plan** (frozen 15:33): `raw/networkx/slowdowns/repeat/plan.md`, tier 2. Two repeats (base-first, slow-first), 2 × 3, pooled 12 v 12.
- **Raw data:** `repeat/t2_{03,04,02}.json`.
  - Frozen analysis: `repeat/analysis_rep.json`, exact test primary.
  - Post-hoc analysis (PM 02:37): `scripts/tier2_flips.py` → `repeat/flips_tier2.json`.
- **Coverage:**
  - **Complete:** #3 (168 cases, 166 complete), #4 (171) and #2 (162).
  - **#8 was cut by the 06:25 hard stop** (partial, not reported).
  - **#1 never started.**
- **#3's 2 incomplete cases:** one `time_pagerank('ER (100, 0.5)')` run timed out (120 s), and one `time_pagerank('ER (100, 0.9)')` run failed with `URLError: Connection reset by peer` (see the note at the end).
- **M5 labels:** #3 noisy (3 runs > 1.5) and #4 noisy (2 runs) by load. **#2 is measured-window** (peak 1.49).
- **The frozen metric "pairs agree with each other"** reads 0 for tier 2 because tier 2 has only one order-balanced pair. It is not meaningful here.

**Result: 488 of 499 complete off-target verdicts agree with the original ("same"). 11 are new non-"same" verdicts (exact test).**

| Slowdown | Case | Now | Ratio | Exact p | Repeat 0 / repeat 1 ratio | Max run load (case) | σ (S0 A/A, 2 repeats) |
|---|---|---|---|---|---|---|---|
| #3 | `greedy_modularity_communities('Drug Interaction network')` | faster | 0.845 | 1.1e-3 | 0.910 / 0.786 | 1.52 | none |
| #3 | `k_core('ER (100, 0.1)')` | slower | 1.430 | 1.4e-5 | 1.413 / 1.372 | 1.03 | none |
| #3 | `louvain_communities('ER (100, 0.9)')` | faster | 0.829 | 6.6e-4 | 0.853 / 0.797 | 0.77 | none |
| #3 | `GraphBenchmark.time_to_undirected('MultiDiGraph')` | faster | 0.873 | 1.0e-4 | 0.892 / 0.822 | 0.75 | floor 1.029: **clears** |
| #3 | `harmonic_centrality('directed_wheel(10)')` | slower | 1.211 | 2.0e-4 | 1.245 / 1.162 | 0.77 | none |
| #3 | `k_factor(…, 4)` | faster | 0.859 | 2.2e-5 | 0.866 / 0.860 | 0.68 | none |
| #4 | `kosaraju_scc('ER (100, 0.1)')` | slower | 1.200 | 3.3e-5 | 1.184 / 1.231 | 1.05 | none |
| #2 | `tarjan_scc('ER (1000, 0.05)')` | slower | 1.171 | 3.7e-4 | 1.126 / 1.266 | 0.84 | none |
| #2 | `connected_components('ER (100, 0.9)')` | slower | 1.288 | 7.4e-7 | 1.222 / 1.316 | 1.08 | floor 1.278: **clears (narrowly)** |
| #2 | `GraphBenchmark.time_subgraph_large('MultiGraph')` | slower | 1.173 | 1.8e-3 | 1.163 / 1.163 | 1.27 | none |
| #2 | `…time_multi_instance(DiGraph)` | slower | 1.170 | 8.9e-6 | 1.142 / 1.203 | 0.79 | none |

- **Rate:** 11 / 499 = **2.2 %**, against ≈ 0.2 % nominal at α = 0.002 (≈ 1 expected). Under the old normal-approximation test it is 9.
  - That is **about 11× the nominal rate of the test as applied**. The nominal α assumes exchangeable samples, but the 12 per side come from 2 processes × 2 repeats, so they are correlated, which makes the test anti-conservative.
  - The Wilson interval (1.2–3.9 %) treats cases as independent, although they share runs and blocks, so it is too narrow.
  - No correction for 499 tests was applied. The 11 still clearly exceed the ≈ 1 expected.
  - Two flips are borderline: p = 1.1e-3, and p = 1.8e-3, which is 2.9e-3 under the old test.
- **The earlier A/A results do not contradict a ≈ 2 % rate.** The 23-case S0 A/A did run in the same two directories (A in `nx-slow-A`, B in `nx-slow-B`). Its 0 of 46 is consistent with 2.2 % (P ≈ 0.36). It covered only 2 of the 11 flipped cases, and it ran at S0 only, not at #3's, #4's or #2's states. Tonight's directory A/A at #3's state is the decisive test (night-2 PLAN).
  - 0 of 46 per-repeat verdicts in the quiet S0 A/A, and 0 of its 69 verdicts overall, are consistent with 2.2 % (P(0 of 46) ≈ 0.36).
  - The (b) A/A's "1 of 12" comes from a preselected set of flagged cases, not a sample.
- **The noise floor (PM item 1):** σ exists for only 2 of the 11 cases, from the 2-repeat S0 A/A, so it is rough.
  - `to_undirected('MultiDiGraph')` (faster) clears its floor: 0.873 < 0.972, which is 1/(1 + 3σ) = 1/1.029.
  - `connected_components('ER (100, 0.9)')` clears narrowly (1.288 vs 1.278).
  - The other 9 have no σ.
- **Machine state (PM item 2): this data cannot test it.**
  - Only 5 of the 1,356 runs in the noisy blocks exceeded load 1.5, and only 1 of the 11 flips is in a case with such a run.
  - The measured-window block (#2) has 4 flips in 162; the noisy blocks have 6 in 166 and 1 in 171.
  - WSL load (1 min) is also a weak proxy for interference.
- **Interpretation. The edit and the clone directory are fully confounded:** in all 1,332 runs, base ran in `nx-slow-A` and slow ran in `nx-slow-B`.
  - All 11 flips have the same sign in both repeats. That is expected for any pooled result with p < 0.002, so it is weak evidence by itself: 262 of the 488 non-flips are same-sign too. Order-balancing rules out only a run-order artefact.
  - **(i) An effect of the patch on these cases** (via paths the S0 profile did not record) **cannot explain the 4 "faster" flips**, because the patch only adds work.
    - The #3 patch touches only `is_connected`. No call path from it to `to_undirected`, `k_factor` or `harmonic_centrality` has been shown.
    - Each patch renames the original function and adds a wrapper; for #1 and #3 this also moves the `@nx._dispatchable` decorator.
  - **(ii) Directory, layout, import or setup differences between the two clones** (measurement bias) can produce both signs.
    - The S0 A/A used the same two directories, with identical code, and showed no case beyond ±10 % in both repeats. That is a real control, but it covers only 2 of the 11 flipped cases, and 4 of its 23 cases exceeded ±10 % in one repeat.
    - In the (b) A/A, 3 of 12 cases have all 5 repeat ratios on one side (P(≥ 3) ≈ 0.04 if independent), but the atlas cases share a setup, so the effective n is smaller.
  - **Not separable with this design.** Swapping the directories between sides was not done. **Update (24 Nov, 00:12):** see "Directory A/A". Identical code gives the same ≈ 2 % rate, so these flips need no edit effect; the cause (directory vs test) is still unresolved.
- **Implication for the paper** (PM item 3, reworded to fit the data):
  - An A/B benchmark oracle that runs each side in one fixed clone directory gave **direction-consistent off-target "changes" on ≈ 2 % of cases**. That is well above the test's nominal rate, but the nominal rate itself assumes exchangeable samples.
  - The "faster" flips show that at least part of this is not caused by the edit.
  - Oracle designs should **swap or rotate clone directories between sides** (or use several clones per side) and test at the process level. *(Update 24 Nov: the swap was tested on #8 and #1 and does not remove the flips; see "E3 tier 2 resumed with DIRECTORY SWAP".)*
  - This weakens any reading of single off-target flags, including the profile-completeness flag (#9), which is consistent with noise.
- **N14 (KB, provisional)** should say "off-target false verdicts ≈ 2 % in a fixed-directory A/B design; source unresolved (clone or layout confound vs unprofiled effects; the faster flips favour the former); load could not be tested", not "depends on machine state". *(Superseded: see the N14 wording in "Directory A/A" and the swap section; the "faster flips favour the clone/layout confound" reading is withdrawn, because identical code and the swapped design give the same rate.)*
- **#3's incomplete cases:** the URLError hit `time_pagerank('ER (100, 0.9)')`. A network dependency in its setup is likely but not verified from the raw files.

### E5: measured setup-cached networkx pass (night 2, item 2; 00:17–01:47)

- **Plan** (frozen 16:52 on 22 Nov; cap amended to 3 h in the night-2 PLAN): `raw/networkx/bench/setup_cached/plan.md`.
- **Raw data:** `setup_cached/{std,cached}{0,1,2}.json`. The frozen analysis (`scripts/night2_analyse.py`) output is `setup_cached/analysis_e5.json`.
- **Design:** S0, all 171 cases, one directory (`nx-slow-A`) for both arms, alternated STD, CACHED ×3.
  - **STD** = the asv protocol (2 processes × 3 values per case, one process per case-run).
  - **CACHED** = `bth.benchrun measure-cached`: one process per module, imports once, then per case setup, calibration, 1 warm-up and 6 values. That is the same 6 samples per case.
- **Run conditions:** 0 errors in all 6 passes. M5 labels: std0 noisy (3 runs > 1.5, 3 gate-not-ok), std1 measured-window, std2 noisy (1 run), cached0 and cached1 measured-window, cached2 noisy (one module run, `benchmark_shortest_path`, load 1.59 after; counted as 8 case rows).

| Pass | Total ¹ | `benchmark_algorithms` ² | Timed loops | Imports (all modules, once) | Setup | Calibration | Warm-up | Other |
|---|---|---|---|---|---|---|---|---|
| std0 | **705 s** | 606 s | 152 s | (per process) | | | | |
| cached0 | **201 s** | 159 s | 142 s | 4.7 s | 2.7 s | 25.3 s | 24.4 s | 1.3 s |
| std1 | **691 s** | 601 s | 142 s | | | | | |
| cached1 | **189 s** | 148 s | 134 s | 4.9 s | 2.6 s | 24.1 s | 21.9 s | 1.2 s |
| std2 | **679 s** | 590 s | 134 s | | | | | |
| cached2 | **195 s** | 154 s | 139 s | 4.5 s | 2.6 s | 25.7 s | 22.2 s | 1.3 s |

¹ Total: STD is the sum of run walls (process start included); CACHED is the sum of module walls (`module_wall_s`; the raw `sum_run_wall_s` of CACHED sums case walls, 182.7–194.9 s, and leaves out imports). Gate waits are excluded from both (std0 waited 2,371 s).

² STD: sum of the 49 cases' run walls. CACHED: the module wall, import included.

**Primary result (frozen rule):**
- Median STD pass **691 s**; median CACHED pass **195 s**. **STD / CACHED = 3.54×.**
- **Against build + tests (≈ 87 s; RQ1): a setup-cached FULL benchmark pass costs ≈ 2.2–2.3× build + tests (188.5–200.7 s / 87 s; 2.1–2.8× over the 71–89 s range of build + tests), against ≈ 7.8–8.1× for STD on the same night.** This replaces the "≈ 1.5–2× (estimate)" in the RQ1 headline.
- **Validity check: 1 of 171 cases is sample-shifted** outside [0.8, 1.25] (`kosaraju_scc('ER (1000, 0.01)')`, 1.28, where the calibrated `number` is 5 against 10).
  - Median samples agree within ±25 % on 170 of 171 cases (median CACHED/STD ratio 0.987; 13 cases outside ±10 %).
  - The calibrated `number` differs between arms in 73 of 513 case-passes. The tolerance is wide, so "what is timed" is similar, not identical.
- **Where the cached pass's time goes:**
  - timed loops 70–71 %;
  - calibration and warm-up ≈ 24–25 % (STD calibrates once per case, but sets up and warms up in both of its processes);
  - module imports ≈ 2.4 % (4.5–4.9 s for all modules);
  - per-case setup ≈ 1.4 %.
  - So in STD, **≈ 484–504 s of each pass (STD minus the paired CACHED) is, by inference, per-process start-up and re-import overhead** (342 processes per pass). STD has no phase timers.
    - The arithmetic supports it: ≈ 452 s of that difference is in `benchmark_algorithms` (98 processes × ≈ 4.6 s), against a measured one-time import of ≈ 4 s for that module in CACHED.
- **Machine state:** tonight's STD passes (679–705 s) sit at the fast end of the 9 earlier passes (659–2,984 s). `benchmark_algorithms` import cost was low tonight (4.5–4.9 s for all modules at once). So for slow-import states such as 22 Nov (STD up to 2,984 s) the ratio is expected to be typical or higher, but that is not measured. One earlier STD pass (659 s) was faster than tonight's, so 3.54× is not a strict lower bound.
- **Not claimed:** CACHED is a cost lower bound for a suite with module-level setup caching (as asv's `setup_cache` would allow). It is not an asv replacement; the process isolation differs.
- **Implication for RQ1 and K1:**
  - On networkx, **benchmarks dominate per-edit validation cost (≈ 8× build + tests), by inference mostly because of per-process overhead** rather than the timed work.
  - With module-level setup reuse they cost ≈ 2.2–2.3×: still the largest single part, but no longer dominant by an order of magnitude.
  - So "your suite is just badly set up" is partly true, and the paper should say so with these numbers.

### Directory A/A: the decisive test of the directory confound (night 2, item 1; 22:43–00:09)

- **Plan** (frozen 06:36 on 23 Nov): `raw/night-2026-11-23/PLAN.md`; frozen analysis `scripts/night2_analyse.py` → `raw/night-2026-11-23/analysis.json`. Raw data: `raw/networkx/bench/dir_aa/s03.json`.
- **Design:** identical code (#3's state `e773a6af`, unpatched) in `nx-slow-A` (label A) and `nx-slow-B` (label B). The case set and design are those of tier-2 block t2_03: 168 cases, 2 × 3, 2 repeats, order rotated.
- **Run conditions:** 672 runs, 0 errors, no gate-not-ok run, 1,823 s of per-run gate waits. One run exceeds load 1.5 (1.58, a loadavg-after value; the before-load maximum is 1.45), so the block is labelled **noisy** under the run-level rule.

**Result (frozen rule):**
- **Non-"same" verdicts with identical code: 4 of 168 = 2.4 %** (Wilson 95 % 0.9–6.0 %), against 6 of 166 (3.6 %) in t2_03 with the patch.
- **Recurrence of the 6 t2_03 flips: 1 of 6.** Only `to_undirected('MultiDiGraph')` recurs, at the same ratio (0.875 vs 0.873). The other 5 are "same". 4 of them lie on the other side of 1; `k_factor` is on the same side (0.983 vs 0.859).
- **Frozen decision: "bias SUPPORTED"**, reached through the rate branch (Wilson lower bound 0.9 % > 0.5 %), **not** through recurrence (1 < 4).
  - Under the frozen rule this label means only that non-"same" verdicts without an edit occur at a rate above 0.5 %. It does **not** mean a stable, case-specific bias.

| Non-"same" case (identical code) | Verdict | B/A ratio | Exact p | Repeat 0 / repeat 1 |
|---|---|---|---|---|
| `GraphBenchmark.time_subgraph_large('DiGraph')` | faster | 0.904 | 8.9e-6 | 0.922 / 0.903 |
| `CommonNeighbors.time_star_rim_rim(10)` | slower | 1.308 | 3.0e-6 | 1.252 / 1.363 |
| `NonNeighbors.time_complete(100)` | faster | 0.725 | 1.1e-3 | 0.818 / 0.696 |
| `…time_multi_source_dijkstra_over_atlas('increasing')` | slower | 1.176 | 1.8e-3 | 1.122 / 1.258 |

**Reading:**
- **Off-target flips do not require an edit.** Identical code gives non-"same" verdicts at 2.4 % (Wilson 0.9–6.0 %), which is compatible with tier 2's 2.2 % (the intervals cannot distinguish the two rates).
  - So tier 2's off-target flips, including the "faster" ones, need no effect of the slowdown patches to explain them.
  - **This A/A is itself fixed-directory** (A in `nx-slow-A`, B in `nx-slow-B`). It cannot say whether the cause is the directories or the test, and no same-directory A/A was run.
- **Directory bias vs test:**
  - Which cases flip did not reproduce: 1 of 6 recurred, and the 4 cases flagged here differ from tier 2's.
  - That is compatible with an anti-conservative test (12 v 12 samples from 4 processes per side, so correlated samples), but **this is a candidate explanation, not tested here**.
  - The evidence against a fixed directory effect is weak:
    - all 4 cases here have both repeat ratios on the same side;
    - the 1 recurring case is the one that cleared its floor;
    - the recurrence test has low power, because tier-2 flips might include real patch effects.
- **Two cases are notable:**
  - `NonNeighbors.time_complete(100)` gives a 0.725× "faster" verdict with identical code. It is the same case as #2's off-target "slower" flag (1.14×), which tier 1 did not repeat.
  - An atlas `multi_source_dijkstra` case gives 1.18× with identical code, here at #3's state.
- **Consequences:**
  - **Single A/B verdicts of ≤ ≈ 1.4× in either direction are not evidence of an edit effect in this design.** The identical-code deviations reach 1.308× slower and 0.725× faster (≈ 1.38×), and tier-2's `k_core` flip was 1.43×. This covers the #1, NonNeighbors and #9 flags, all tier-2 flips, and #8's 1.12–1.20×.
  - **#2's on-target detection stands.** At 1.76–1.90× it is clearly above the largest identical-code deviation (≤ 1.38×), it cleared its own (b) floors (1.08–1.33), and it repeated in tier 1. The A/A here is at #3's state, not #2's.
  - **N14 (KB) should read:** "≈ 2 % non-same verdicts per off-target comparison in the 12 v 12 fixed-directory A/B design, **also with identical code** (directory A/A 4/168). Cause unresolved (directory vs anti-conservative test; no same-directory control). Low case recurrence (1/6). Load not testable." *(24 Nov, 03:25: with the directory swap the rate is 1.8 % and no flip reverses sign, so a directory effect alone is not the cause; see the swap section.)*
- **For the paper (K3):** at the 12 v 12 tier-2 design, ≈ 2.4 % per case (Wilson 0.9–6.0 %) means **≈ 4 false "changes" per 171-case comparison** (1.6–10 across the bounds), assuming independent cases. The 18 v 18 slowdown-oracle design was not A/A-tested at this scale, so its rate is not known; the earlier 843 off-target comparisons gave 3.
- **Caveats:**
  - One state (#3's), 168 cases, one night.
  - The block is labelled noisy (1 run > 1.5).

### E3 tier 2 resumed with DIRECTORY SWAP: #8 and #1 (night 2, item 3; 01:49–03:22)

- **Plan:** night-2 PLAN.
- **Raw data:** `raw/networkx/slowdowns/repeat_swap/t2s_{08,01}.json`. The frozen analysis output is `raw/night-2026-11-23/analysis.json` (rep2s).
- **Design:** the frozen tier-2 case sets (170 each), 2 × 3, 2 repeats.
  - Repeat 0: base@A, slow@B, base first. Repeat 1: base@B, slow@A, slow first.
  - So the edit is balanced across both directories and both orders. #8 started fresh; night 1's fixed-directory partial is archived.
- **Run conditions:**
  - #8: 680 runs, measured-window (peak 1.45), 157 s of gate waits.
  - #1: 680 runs, noisy (3 runs > 1.5, peak 1.98), 137 s of gate waits.
  - 0 errors, no gate-not-ok run.
- **Both slowdowns finished.** E3 tier 2 is now complete for all five reached slowdowns: #3, #4 and #2 in the fixed-directory design (night 1), #8 and #1 with the swap (night 2).

| Slowdown | Agree with the original | New non-"same" (off target) | Directory-inconsistent |
|---|---|---|---|
| #8 | 165 / 170 | 5: `square_clustering ER(100, 0.1)` 1.129, `betweenness ER(100, 0.5)` 1.178, `connected_components ER(100, 0.9)` 1.175, `harmonic_centrality_node_subset wheel(1000)` 1.111 (all slower); `connected_components Drug` 0.901 (faster) | 0 of 5 |
| #1 | 168 / 170 | 1: `connected_components ER(100, 0.5)` 0.884 (faster). The other disagreement is the original off-target "faster" (`average_clustering ER(100, 0.1)`, 0.858), now "same". | 0 of 1 |

- **Rate with the swap:** 6 of 340 off-target comparisons = **1.8 %** (the frozen tier-2 sets exclude the on-target cases), against 2.2 % fixed-directory (11 of 499) and 2.4 % identical code (directory A/A). **The swap does not remove the off-target flips.**
- **All 6 keep their sign** although slow ran in B and then in A. No flip reverses sign, so **a directory effect alone does not produce them**.
  - A directory effect of a few percent on top of another effect is not excluded (repeat ratios such as 1.20 / 1.084 leave room for it).
  - The swap also reverses run order (repeat 1 is slow-first), so directory and order are balanced together and cannot be separated.
  - The "directory-inconsistent" column is 0 by the flag's definition (a sign disagreement between repeats), not as an independent check.
- **That sign consistency does not show a real edit effect either (PM 02:37, item (b)):** all 4 identical-code directory-A/A flips also kept their sign, and selection on pooled p < 0.002 produces same-sign repeats by construction. So 6 of 6 consistent signs here (and 4 of 4 in the directory A/A) is not evidence of an effect after that selection.
- **Cross-night check (PM item (c)):** night 1's fixed-directory #8 partial (repeat 0 only) has 4 of the 5 #8 cases.
  - **Only `connected_components('ER (100, 0.9)')` agrees** (1.251, then 1.175). The others disagree: `square_clustering` 0.929 → 1.129, `betweenness` 1.002 → 1.178, `connected_components Drug` 1.175 → 0.901.
  - So **3 of 4 do not reproduce across nights**. Night 1 has only repeat 0 (6 v 6), and night 2's repeat 0 has the identical configuration (base@A, slow@B, base first), with ratios 1.110 / 1.200 / 1.128 / 0.944 against night 1's 0.929 / 1.002 / 1.251 / 1.175. That is **per-night variation under the same setup**. A stable edit effect on these cases is **not shown** (one repeat per night is weak evidence).
  - `connected_components('ER (100, 0.9)')` is "slower" under unrelated slowdowns (#2 at 1.288 and #8). It is a noisy or sensitive case to flag; in the original #8 oracle it was "same" (0.955).
- **Independence of the repeats (PM item (a)):** separate processes ≈ 20 min apart. `number` is calibrated per run (often identical). The repeats are not independent of machine-state drift within a night.
- **Reading, cause unresolved:**
  - Off-target non-"same" verdicts occur at ≈ 2 % per comparison in this 12 v 12 oracle: with the edit fixed to one directory (2.2 %), with identical code (2.4 %), and with the directory swapped (1.8 %).
  - **A directory effect alone does not produce them** (the swap does not reverse them). **A stable edit effect is not shown** for the cases checked across nights (3 of 4 vary between nights).
  - Candidates left, none tested here:
    - per-night or per-run variation on these cases;
    - an anti-conservative test (correlated samples);
    - for `connected_components ER(100, 0.9)`, which recurs, an edit or case-specific effect.
  - **This design cannot separate them.**
  - A process-level analysis, or more processes per side, would be the next test.
- **Consequence (unchanged):** single A/B verdicts of ≤ ≈ 1.4× in either direction are not evidence of an edit effect in this design. All 6 flips here are ≤ 1.18×.

### Exact-test recompute of every performance verdict (PM 15:46, after W1 read the asv source; compute only, 15:50)

- **Why:**
  - `bth.stats.asv_rule` used scipy's `mannwhitneyu(method="auto")`. That is exact only for n < 8 with no ties, and otherwise a normal approximation with tie and continuity corrections.
  - asv itself (`asv/_stats.py`, `main`, read 2026-11-22 via a fetch agent; nothing downloaded or run) uses an **exact** two-sided test when max(m, n) ≤ 20. Above that it uses an uncorrected normal approximation. Below a minimum attainable p it falls back to a 99 % CI check, and with repeat = 1 it skips the statistics.
- **What:** `scripts/recompute_exact.py` re-tested **1,026 verdicts** from their raw samples under three methods: the old test, scipy exact at every size, and asv's rule. Output in `raw/stats_exact/recompute.json`.
  - The A/A: 69 = 23 cases × (rep0, rep1, pooled).
  - The reach oracles of #1–#4 and #8: 5 × 171.
  - The 6v6 spot checks of #0, #5, #6, #7 and #9: 50.
  - The powered profile-completeness check: 50.
  - The #9 re-check: 2.
- **Result: 0 of 1,026 verdicts change** under exact or asv. (The PM's 15:57 note says "2,094"; that was my uncounted first figure, corrected to 1,026 at 15:51.)
- **The borderline p-values get stronger, not weaker:**

| Verdict | Old p | Exact p |
|---|---|---|
| #9 louvain | 1.87e-3 | 1.19e-3 |
| #1 `connected_components ER(100, 0.1)` | 1.83e-3 | 1.27e-3 |
| #2 `NonNeighbors.time_complete(100)` | 2.3e-4 | 9.6e-5 |

  The closest non-flagged case with ratio > 1.1 has exact p = 0.0057.
- **Minimum attainable p** (`stats.min_attainable_p`):
  - **6 v 6: 0.00216** under every method (2/924). The "6 v 6 cannot reach α" result stands.
  - **15 v 15:** 3.4e-6 was the normal approximation; the **exact value is 1.3e-8** (corrected above in the profile-completeness section).
  - Exact values for the other sizes: 12 v 12: 7.4e-7; 18 v 18: 2.2e-10.
- **From now on:** the exact test is primary (`stats.mwu_p(method="exact")`), and the old test is shown next to it for continuity. This is amendment 2 of the night analysis. `asv_rule`'s default is unchanged, so earlier scripts reproduce.
- **A/A bootstrap power under the exact test** (15:55; `scripts/aa_power_exact.py` → `raw/stats_exact/aa_power_exact.json`):
  - Same seed and procedure; the old-test run reproduces the reported medians exactly.
  - The exact test gives slightly **more** power: at 1.2×, **0.93** overall (was 0.905), **0.415** for the 3 `benchmark_algorithms` cases (was 0.345), 0.94 for the others.
  - At 1.12× the values are 0.515 / 0.335; at 2× they are 1.0 / 0.975.
  - The reading is unchanged: the heavy-module cases need ≈ 2× for reliable detection.

### Power at the verdict design (18 v 18, exact test + 1 + 3σ floor) (PM 16:55 for W6; compute only)

- **Method:** the same bootstrap as `aa_power_exact.json`: A/A re-run samples from the 23-case A/A, seed 20261122, 200 draws per case and shift, with B scaled by the shift.
  - Resamples are **18 v 18**: the slowdown-oracle design of 2 processes × 3 values × 3 repeats, pooled.
  - Test: exact two-sided MWU, p < 0.002, ratio > 1.1, **and** ratio > 1 + 3σ(b).
  - σ(b) comes from `aa/sigma_noise.json` (σ_rep from only 2 repeats, which is rough; σ_boot as a sensitivity check).
  - Script `scripts/aa_power_design.py`, output `raw/stats_exact/aa_power_design18.json`.
- **Result** (median detection probability over cases; 23 cases, 3 of them `benchmark_algorithms`):

| Shift | All cases: no floor | All: + floor σ_rep | All: + floor σ_boot | `benchmark_algorithms`: no floor | Alg: + floor σ_rep | Alg: + floor σ_boot |
|---|---|---|---|---|---|---|
| 1.1× | 0.37 | 0.25 | 0.25 | 0.28 | **0.00** | 0.03 |
| 1.2× | 0.97 | 0.96 | 0.96 | 0.49 | **0.035** | 0.13 |
| 1.5× | 1.00 | 1.00 | 1.00 | 0.865 | 0.84 | 0.845 |
| 2× | 1.00 | 1.00 | 1.00 | 0.985 | 0.985 | 0.985 |

- **Reading:**
  - For the cheap modules, the verdict design detects a 1.2× slowdown almost surely (0.96–0.97), with or without the floor.
  - For the sampled `benchmark_algorithms` cases, the floor removes almost all power at 1.2× (0.035–0.13), and only ≈ 1.5× or more is reliably detected (0.84–0.99).
  - At 1.1× nothing is reliable: a true 1.1× shift sits at the asv factor itself.
- **Limitations:**
  - Only 3 `benchmark_algorithms` cases; σ_rep from 2 repeats.
  - The bootstrap resamples pooled samples and so ignores between-process and between-repeat structure, which makes it optimistic.
  - (b)'s 5-repeat floors for the flagged cases (1.08–2.18) show that per-case floors vary widely.

### Mining precision by agent labelling (D26, PM 15:55; computed 15:52 by `scripts/labels_b1.py` → `results/labelling/precision_b1.json`)

- **Labelling:** codebook v1 (frozen 15:44). Two agent raters agreed on 79 of 81 rows, κ = 0.948. **Same-model raters:** a threat; κ is likely inflated. The adjudicator decided ids 18 (OPT), 33 (NOT_OPT) and 67 (NOT_OPT).
- **v1 regex rule precision** (rule-qualified ∩ OPT / rule-qualified, Wilson 95 %):

| Project | Precision | 95 % CI |
|---|---|---|
| networkx | 15/20 | 53–89 % |
| bottleneck | 15/16 | 72–99 % |
| geopandas | 17/20 | 64–95 % |
| pvlib-python | 3/14 | 8–48 % |
| **pooled** | **50/70, 71 %** | 60–81 % |

- **Against the earlier manual reading of subjects** (networkx 17/20, geopandas 19/20):
  - The agents agree that networkx steps 8, 13 and 17 are not optimizations.
  - They label **two more networkx commits NOT_OPT:**
    - step 6 `0d3fe6ac` (id 25), "a new API `floyd_warshall_tree`; existing functions unchanged";
    - the dropped `675034ad` (id 39), "mainly an ISMAGS bug fix".
  - For geopandas they agree on `6286f13f` (DOC) and add two:
    - `6802f43e` (id 9), "mainly a multipoint-clipping bug fix";
    - `7d503802` (id 67), adjudicated NOT_OPT.
  - **Caveat on id 67:** both raters said UNSURE because the decisive `overlay.py` diff was truncated and the link returned 503. The adjudicator's reason cites details (`buffer(0)` inputs, column suffixes) that are not visible in the sheet's truncated diff.
    - **Checked by the PM (16:03) against the full commit `.diff` (1,072 lines):** the adjudicator evidently used the full diff, a source outside the sheet.
    - Most cited details are confirmed: the old function renamed `_overlay_old`, a new implementation, tests re-based on QGIS fixtures (`tests/data/overlay/nybb_qgis/`), and `use_sindex` handling.
    - One is wrong: "make_valid" does not appear in the diff.
    - **The NOT_OPT label stands.** Codebook v2's "sheet only, cite sources" rule covers this from now on.
- **B1 restated on agent-labelled optimizations** among the 18 replayed networkx edits (S0 reach, module-level lines excluded; reproduces 12/18 and 9/15 exactly):

| Edit set | Profile unreached | Static unreached |
|---|---|---|
| all 18 | 12/18, 67 % [44–84 %] | 7/18, 39 % [20–61 %] |
| manual OPT (15) | **9/15**, 60 % [36–80 %] | 4/15, 27 % [11–52 %] |
| agent OPT (14) | **8/14**, 57 % [33–79 %] | 3/14, 21 % [8–48 %] |

  Step 6 is unreached under both measures, so dropping it lowers both counts by one. **The B1 reading does not change:** "many, not most" (the CI spans 50 %), on networkx only.
- **Codebook v2** (`frozen/labelling/codebook-v2.md`, frozen 15:53) adopts the adjudicator's four rules for the replication sheet: bug fix plus speed-up, opt-in backends, output order, and link fields. It also requires full source diffs in the sheet.

### W6 hostile-review checks (PM 16:25; compute only, nice 19 on CPUs 0–1, concurrent with night item (b) and logged)

**1. B1 construct check: is any edit unreached by construction?** (`scripts/b1_construct.py` → `results/q3/b1_construct.json`; git and AST only)
- **Method:** each changed function (module-level lines excluded) was looked up by qualname at S0 and at the step's parent state in the replayed sequence.
- **Result:** **no agent-OPT edit is unreached by construction.** Every one of the 14 has at least one changed function that exists at S0. All changed functions exist at their parent.
  - Only partial absence: step 2's nested `bidirectional_dijkstra.<locals>.path` is new in that edit. Its outer function exists at S0 and is not in the S0 profile either.
- **B1 stays 8/14** (S0 profile), so there is nothing to split out.
- **Not done:** profiling at each edit's parent. Reach is still from S0. That is a stated limitation, and the replication protocol (a) profiles at each parent.

**2. Dilution: the time share of the slowed function in each profile-reaching case** (`scripts/slow_share.py` → `raw/networkx/slowdowns/share.json`)
- **Method:** cProfile at the slowdown's own state, unpatched. Share = the slowed function's inclusive time ÷ the case's total profiled time.
- **This is approximate, not a timing result:** cProfile overhead inflates call-heavy code.
- For a `double_call` slowdown, the expected timing ratio is about **1 + share**.

| Slowdown (kind) | Reaching cases (S0 profile) | Share | Expected ratio | Observed (oracle) |
|---|---|---|---|---|
| #2 `_dijkstra_multisource` (double_call) | 8 atlas multi-source cases | **0.84–0.86** | ≈ 1.84–1.86 | **1.81–1.90, slower** ✓ |
| #3 `is_connected` (double_call) | 3 `time_eigenvector_centrality_numpy` cases | **0.004–0.005** | **≈ 1.005** | same |
| #8 `_build_paths_from_predecessors` (list_membership) | 1 case | 0.57 | not 1 + share; the slowed operation is one membership test inside the function | 1.116, slower |
| #1, #4 | none by S0 profile (static reach = all 171 cases, uninformative) | — | — | same (both on-target candidates unreached by profile) |

- **#3 is a dilution miss, not a power miss.** The slowed function is ≈ 0.5 % of its reaching cases. A doubling would change them by ≈ 0.5 %, far below the 1.1 factor and any noise floor.
- So the earlier wording "#3 may be a power miss" is **replaced:** #3 is reached, but the edit's effect on the benchmark is diluted to ≈ 1.005.
- **Practical point for the coverage leg:** "executed by a benchmark" is not "visible to a benchmark". Here the share is the third factor, next to coverage and power.
- **#2's on-target ratios match the share prediction.** That supports reading the share as the expected effect for double_call slowdowns.

**2b. Per-edit time share of the changed functions, for the 14 agent-OPT edits** (advisor draft review via PM 16:44; `scripts/edit_share.py` → `raw/networkx/edit_share.json`)

- **Method:** the same as 2: cProfile, approximate, not timing. Each edit is profiled at its **parent state**, the code it optimizes.
  - Reaching cases are those whose S0 profile contains a changed function.
  - The share is the largest inclusive time of any changed function ÷ the case total, taking the maximum over cases. Here the upper bound (sum over changed functions) equals it on every row.
- **Expected ratio** if the changed functions were uniformly slower by a factor f: 1 + share·(f − 1).

| Step | Changed functions | Executed (S0 profile) | Reaching cases | Max share | Expected ratio, f = 1.2 | Expected ratio, f = 2 |
|---|---|---|---|---|---|---|
| 1 | `global_parameters`, `intersection_array` | not executed | 0 | 0 | 1.000 | 1.000 |
| 2 | `bidirectional_dijkstra` (+ nested `path`) | not executed | 0 | 0 | 1.000 | 1.000 |
| 3 | `_dijkstra_multisource` | yes | 8 (atlas multi-source) | 0.864 | 1.173 | 1.864 |
| 4 | `is_connected`, `number_connected_components` | yes | 3 (`eigenvector_centrality_numpy`) | **0.021** | **1.004** | **1.021** |
| 5 | `_single_shortest_path` and 3 more | not executed | 0 | 0 | 1.000 | 1.000 |
| 7 | `kruskal_mst_edges` | not executed | 0 | 0 | 1.000 | 1.000 |
| 9 | `katz_centrality_numpy`, `_pagerank_scipy` | yes | 4 (`time_pagerank`) | 0.998 | 1.200 | 1.998 |
| 10 | `_build_paths_from_predecessors` | yes | 1 (`ManyComponents`) | 0.502 | 1.100 | 1.502 |
| 11 | `DiGMState.__init__`, `GMState.__init__` | not executed | 0 | 0 | 1.000 | 1.000 |
| 12 | `edmonds_karp_impl`, `minimum_cut` | not executed | 0 | 0 | 1.000 | 1.000 |
| 14 | `_build_paths_from_predecessors` | yes | 1 (`ManyComponents`) | 0.565 | 1.113 | 1.565 |
| 15 | `lattice_reference`, `random_reference` | not executed | 0 | 0 | 1.000 | 1.000 |
| 16 | `_triangles_and_degree_iter` | yes | 4 (`time_average_clustering`) | 0.999 | 1.200 | 1.999 |
| 18 | `chain_decomposition` (+ 2 nested) | not executed | 0 | 0 | 1.000 | 1.000 |

- **Summary:** of the 14 agent-OPT edits, **8 are not executed** by any benchmark (B1). **1 is executed but diluted**: step 4, ≈ 2 % share, so even a 2× slowdown moves its benchmarks by ≈ 2 %.
  - **5 are executed with a large share** (0.50–1.00): steps 3, 9, 10, 14 and 16.
  - At f = 1.2, the expected ratio of those 5 is 1.10–1.20. Step 10 is exactly at the asv factor (1.100, not above it), step 14 is just above it (1.113), and all are inside or near the A/A floors of 1.08–2.18 seen in (b).
  - So **at a 1.2× slowdown of the changed code, at most 4 of the 14 edits (steps 3, 9, 14, 16) could clear the asv factor at all, before noise.** At 2×, 5 of 14 could.
- **Limitations:**
  - These are shares, not detections; power comes from the A/A floors.
  - The profile is from S0 and the shares are from each parent state.
  - Step 4's share (2 %) differs from slowdown #3's (0.5 %, `is_connected` alone at the slowdown's state), because step 4 has two functions and a different state.

**3. The 890 vs 843 + 50 reconciliation** (slowdown oracle section above, L441 and L569)
- **Within-oracle comparisons:** 5 reached slowdowns × 171 cases = 855. Minus the 12 on-target, profile-reached cases (#2: 8, #3: 3, #8: 1) leaves **843 off-target**.
- **Spot check:** the 50 comparisons (6 v 6) **cannot produce a verdict**, since the minimum attainable p is 0.00216 > α.
- **So the total is 893, not "≈ 890".** Only **843 off-target comparisons can produce a verdict.** At α = 0.002 that gives an expected ≈ 1.7 false non-"same" verdicts (two-sided).
- **Observed: 3** — #1 slower `connected_components ER(100, 0.1)`, #1 one faster, #2 `NonNeighbors.time_complete(100)`. That is consistent with chance (Poisson(1.7): P(≥ 3) ≈ 0.24).
- **Wording to use:** "843 off-target comparisons that can yield a verdict (plus 50 spot-check comparisons that cannot)".

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

- **S0 profile, part 1 (24 `UndirectedAlgorithmBenchmarks.time_[a-l]` cases): provenance problem found and checked (13:11–13:28).**
  - **What happened:** part 1 ran 19:23–19:46 in the shared `networkx-replay` work tree. From 19:38 the overnight re-timing checked that tree out through later states, so `meta.state_sha` records S6.
  - **Check:** an isolated re-profile at S0 (`raw/networkx/profile/S0_181f2951.part1.reprofile.json`) gives **identical executed-function sets for all 24 cases**. No reach-based claim (B1, the spot-check reach, #3, #9) changes.
  - **Lesson:** profiling and timing jobs must not share a work tree. Details in `raw/networkx/bench/LABELS.md`.

The harness tree hash differs between S0 (`c02203a8…`) and S1+ (`ec7dba4c…`). In between, `replay.py` got the blob invariant and `benchrun.py` got the asv package import. Neither file is on the `oracle-tests` code path.
