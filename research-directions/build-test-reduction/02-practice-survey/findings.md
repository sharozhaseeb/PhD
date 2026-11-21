# W2-PRACTICE findings: how optimization systems validate each candidate edit (RQ1)

Status: **draft 2026-11-21**. Built from 24 core per-system notes plus 4 late-search notes (F7), each re-checked by a fresh critic who re-opened every cited file and paper section (logs: `critic-log-A.md` … `critic-log-E.md`; final pass over this file: `critic-log-final.md`). Labels: **[src]** read in source (the per-system note gives file:lines @ commit or paper section), **[inf]** our inference, **[unk]** not found. The evidence boundary is in `README.md`.

Every finding links the per-system note that holds the exact citation.

---

## F1. No iterative optimizer in this sample decides by rule what to rebuild for an edit. Benchmark harnesses re-install per patch, which is an isolation choice and not an optimization loop.

**Optimizers** (they generate and accept edits, so per-edit build cost is theirs to pay):

| Optimizer | Build per candidate | Label |
|---|---|---|
| SemOpt | Full compile (C/C++) or install (Python) per candidate. In the C/C++ projects, 73.7% of 8,082 candidates compile | [src] [semopt](per-system/semopt.md) |
| PerfAgent | Rebuilds via `/build.sh` after every submitted patch. The agent prompt warns rebuilds "may take time". Incremental or full: [unk] | [src] [perfagent §2](per-system/perfagent.md) |
| SysLLMatic | `make compile` in the app's module directory per candidate (module-scoped; what the Makefile runs is [unk], template missing) | [src] [sysllmatic §2](per-system/sysllmatic.md) |
| Codeflash | No build: source-text swap, then pytest. Pure Python targets | [src] [codeflash](per-system/codeflash.md) |
| OpenEvolve / AlphaEvolve | No build step in the framework; the user's evaluator decides | [src] [openevolve](per-system/openevolve.md), [alphaevolve](per-system/alphaevolve.md) |
| Google ECO | Relies on existing CI (v2: all monorepo tests affected by the edit). Build details [unk] | [src] [google-eco](per-system/google-eco.md) |

**Benchmark harnesses** (score one submitted patch per task in a fresh or reset container, for reference):
- SWE-bench classic re-runs the install inside the eval script for every prediction. [src] [swe-bench-harness §0](per-system/swe-bench-harness.md)
- SWE-Perf runs `pip install -e .` twice per prediction. [src] [swe-perf](per-system/swe-perf.md)
- GSO re-runs the instance `install_commands` after the patch and again for the reference commit. [src] [gso §2](per-system/gso.md)
- SWE-fficiency's 5 scripts per candidate each start with the install. [src] [swe-fficiency §2](per-system/swe-fficiency.md)
- FormulaCode never rebuilds; the agent must. [src] [formulacode §2](per-system/formulacode.md)
- Function-level benchmarks have no build or compile one file. [src]

- **Cost is inferred, not measured.** "Repeated install = full build cost" is our inference. Whether `pip install -e .` recompiles only changed C/Cython sources depends on the backend (setuptools build dir, meson-python editable rebuilds), and no system measures or reports per-candidate build time. [inf]/[unk]
- **Build reuse in practice:**
  - caching of the environment (a Docker image per instance; asv's wheel cache keyed by commit hash) [src]
  - whatever the project's build system happens to reuse [inf]
  - industrial CI (Google TAP + Blaze/Bazel), which builds **affected targets** with hash-keyed action caching. That is a functional-CI practice. [src] [industrial-ci-test-selection](per-system/industrial-ci-test-selection.md)
- **Implication for W3.** The build control arm should be the optimizer case: rebuild after each accepted edit in one long-lived working tree (SemOpt/PerfAgent style). The harnesses' per-patch reinstall is a fallback reference. W3's measured build seconds per edit would be new numbers, because nobody in this sample reports them. [inf]

## F2. Test subsets are everywhere, but almost always *fixed per task by the dataset authors*, not chosen per edit.

Three regimes appear.

1. **Fixed per task, chosen at curation from the reference (expert) change.** This is already a form of test selection, but it is computed once from the *gold* diff and reused for every candidate:
   - SWE-bench runs only the test files touched by the gold test patch (`get_test_directives`), then grades fixed FAIL_TO_PASS/PASS_TO_PASS lists. [src] [swe-bench-harness §0]
   - SWE-Perf runs only the instance's `efficiency_test` ids: existing tests whose runtime fell >30% across 3 full-suite runs, then coverage-filtered. Correctness = those tests pass in every repeat, with no PASS_TO_PASS regression suite. [src] [swe-perf]
   - SWE-fficiency runs the `covering_tests` files: coverage.py + jedi over the **expert-modified** code, median about 7.7k tests per task. It grades PASS_TO_PASS only. [src] [swe-fficiency §3]
   - GSO has no unit tests. Correctness is output equivalence (`--eqcheck`) inside the same LLM-written perf scripts, and all of them run for every candidate. [src] [gso]
2. **Fixed per target (function/class), chosen by the tool.**
   - Codeflash discovers tests per target function (Jedi call resolution + import filter) and reruns that same set, plus generated regression tests, for each candidate. [src] [codeflash]
   - SysLLMatic picks test files per class by textual name match and stops at the first failure. Its coverage is weak (GraphChi ≈10%), and wrong-but-passing edits were found. [src] [sysllmatic §3]
   - Function-level benchmarks (PIE, ECCO, EffiBench(-X), Mercury, EvalPerf, COFFE, KernelBench) run their whole per-problem test list. Some exit early on the first failure (PIE, EvalPerf `fast_check`). [src]
3. **Per edit, from the candidate's own diff.** Only two systems do this:
   - **PerfAgent** uses pytest-testmon after each iteration and reports 66–99% fewer tests on GSO and 47–98% on SWE-fficiency-Lite. It states the limitation itself: testmon "tracks only Python coverage", so native-extension regressions can slip through. No public code was found. [src] [perfagent §3]
   - **FormulaCode** maps changed `.py` files to test files **by filename** (`test_<mod>.py`). It runs this **once on the final tree**, not per edit, and with no mapped tests it runs zero tests. [src] [formulacode §3]

**Implication for W3.** Per-edit deterministic RTS for optimization edits is *not* unoccupied: PerfAgent claims it, though no artifact was found, and only Python coverage and no miss-rate study is reported. These gaps remain open:
- (a) Measuring what per-edit selection **misses** (PerfAgent claims "without missing any correctness regressions" in §III-D but contradicts it for native code in §VI).
- (b) Selection that covers **native/compiled code**.
- (c) Comparison of selection rules: filename heuristic (FormulaCode) vs Python coverage (testmon) vs static dependency vs the curation-time expert-diff subsets.

[inf]

## F3. Benchmark subsets are picked by people or agents; no deterministic rule derived from the diff was found in this sample.

- **Fixed per task:**
  - SWE-Perf: the same `efficiency_test`s. [src]
  - GSO: <=20 LLM-written perf scripts, all run. [src]
  - SWE-fficiency: the task's workload script. [src]
  - FormulaCode: all ASV workloads (avg ~265 per task) at final measurement. [src]
  - EvalPerf: one "performance-exercising" input per task. [src]
  - PerfAgent: times the one workload the benchmark instance provides. [src]
- **Subsets picked by a human or an agent:**
  - asv `-b REGEX` (numpy/pandas). [src] [asv](per-system/asv-numpy-scipy-pandas.md)
  - FormulaCode's prompt tells agents to run `--bench=<regex>` and calls full-suite runs "discouraged". [src] [formulacode §4]
  - So benchmark *subsetting* is common practice; what is missing is a rule.
- **Per target:** Codeflash times the discovered tests of the target function. Those are chosen per function, not per diff. [src]
- **No deterministic diff-to-benchmark rule** was found in the repositories read. [unk]
- **Implication for W3.** The open question is a *deterministic* rule mapping an edit to workloads (e.g. via the coverage or call-graph profile of each workload), evaluated against running all workloads. Whether such rules have methods precedent is W1's question. [inf]

## F4. Speed-up confirmation: three schools, and no agreement on statistics.

| School | Systems | Rule (per the notes) |
|---|---|---|
| Repeated wall-time + hypothesis test | SWE-Perf; asv; FormulaCode (dataset curation only); pyperf | **SWE-Perf:** 3 warm-ups + 20 repeats, IQR outlier filter, one-sided Mann-Whitney U at p<0.1 (code and paper agree; the 0.001 seen in code is a search step). Curation also needs a ≥5% gain; one phase uses a plain mean ratio of 0.3 with no test.<br>**asv compare:** ratio >1.1 *and* Mann-Whitney p<0.002, with a fallback to non-overlapping 99% CIs.<br>**pyperf:** 20 processes × 3 values + 1 warm-up, t-test + 1% floor |
| Repeated wall-time, threshold only | GSO; SWE-fficiency; Codeflash; SemOpt; ECCO; SysLLMatic | **GSO:** fresh process, `number=1`, 5 repeats (1 for 3 repos), mean, a ≥~1.1× gate (geometric-mean speed-up over base, rounded to 1 decimal) before the harmonic-mean ratio vs reference >0.95 is checked, no pinning, no test.<br>**SWE-fficiency:** 2 warm-ups, pinned physical cores + NUMA.<br>**Codeflash:** min over loops within a 10 s budget, summed over tests, >5% floor, no pinning.<br>**SemOpt:** 6 runs, drop the first, mean of 5, >5% on one test and ≤2% regression elsewhere |
| Deterministic metric | PIE (gem5 simulated time, threshold 1.10); EvalPerf (instruction counts, one heavy input, CV ≤0.4%); COFFE (instruction counts, 12 trimmed repeats); CodSpeed (callgrind simulation, single run) | Repeats and statistics become unnecessary or minimal [inf] |

Single-run timing also appears: PerfAgent times only the first run and claims <3% variance; EffiBench and Mercury use a single run. [src] ECCO and SysLLMatic apply no acceptance threshold in code (SysLLMatic's ≥10% is a reporting metric only), so "threshold only" above means "threshold or none". [src]

- Per-candidate **noise control is mostly absent**:
  - GSO has no cpuset.
  - SWE-Perf's code gives 10 CPUs and no cpuset, while its paper says 1 core in collection and 5 cores in Phase 4 and evaluation.
  - Among the wall-time systems read, the exceptions are SWE-fficiency (whole-core pinning, NUMA), FormulaCode (dedicated 2-vCPU EC2 instance) and EffiBench-X (one physical core per worker container).

  [src] [swe-perf], [gso], [swe-fficiency], [formulacode]
- **Implication for W3.** A reduced benchmark set has to be judged against *some* acceptance rule, and practice disagrees on which. W3 should fix one rule (e.g. the SWE-Perf/asv-style MWU) and report agreement with a deterministic proxy (instruction counts, as EvalPerf/CodSpeed/COFFE use). [inf]

## F5. Cumulative re-validation of several accepted edits is rare. The functional-CI world has it; the optimization world mostly does not.

- **Benchmarks** score one final patch per task, so there is no sequence of accepted edits to re-check. [src] (SWE-Perf, GSO, SWE-fficiency, PIE, …)
- **Iterative optimizers:**
  - **Codeflash:** no combined re-run of the accepted edits across functions. In `--worktree` mode, edits stack; each next function's baseline is then taken on the modified tree [inf], and no full-suite run before the PR was found [inf]. [src]/[inf] [codeflash §6]
  - **SemOpt:** assembles the best variant per function into the final project and reports perf on it. A combined unit-test re-run is not stated. [src]/[unk] [semopt]
  - **PerfAgent:** keeps the best patch across ≤5 iterations. Only the benchmark's own suite runs afterwards. [src]/[inf] [perfagent §6]
  - **SysLLMatic:** the paper's Algorithm 1 ends with "BuildAndRun(A*); Measure(A*)", a final whole-app rebuild and re-measure. The artifact code never calls the function that would do it. [src] [sysllmatic §6]
  - **FormulaCode:** one correctness check on the final tree. In effect a single final cumulative check, using the filename-mapped test subset + snapshot verification. [src]/[inf]
- **Functional CI pairs reduced per-change checks with broader later runs:**
  - Meta PTS still runs **all tests on master every few hours** behind its learned selector (calibrated to 0.95 test recall / 0.999 change recall). [src] [industrial-ci-test-selection](per-system/industrial-ci-test-selection.md)
  - Google TAP does not run a full suite: it batches changes into milestones (cut about every 45 min at peak) and runs each affected target once, at the latest affecting change, with culprit finding afterwards. [src]
- **AlphaEvolve/OpenEvolve** use an *evaluation cascade*: cheap stages first, expensive ones only for promising candidates. That is ordering, not cumulative checking. [src] [alphaevolve](per-system/alphaevolve.md), [openevolve](per-system/openevolve.md)
- **Google ECO** says per-edit isolated performance tests are infeasible. It relies on existing CI for correctness and on fleet profiling after rollout for performance. Its v2 says all monorepo tests affected by an edit run. [src] [google-eco](per-system/google-eco.md)
- **Implication for W3.** "Reduced checks per edit + periodic full checkpoint + final full validation" has a clear precedent in functional CI (Meta runs all tests on master every few hours; Google TAP uses batched milestones with culprit finding, not a full re-run). In this sample it is **not** applied to performance-motivated edit sequences, and no one reports what a checkpoint schedule catches or costs in that setting. This is the most defensible gap for RQ4. [inf] It is subject to the search record below and to W1's methods review.

## F6. Cheap-first staging is common and is a deterministic reduction in its own right.

- PIE gates on native-binary accuracy before the gem5 run. [src]
- EvalPerf profiles only candidates that pass, with an early-exit correctness check. [src]
- PerfAgent skips profiling when the build or tests fail. [src]
- SysLLMatic runs compile → tests → measure and skips measurement on failure. [src]
- AlphaEvolve/OpenEvolve use cascades. [src]
- KernelBench and SWE-fficiency use anti-cheat guards. [src]
- **Implication for W3.** Stage ordering (build → selected tests → selected benchmarks → periodic full) is the natural experimental skeleton. The cost of each stage per edit is the missing measurement. [inf]

## F7. Oracle warning: the "full check" itself is weak. Full benchmark verdicts don't repeat across machines, and the tests let wrong edits through.

**Performance oracle (the full benchmark verdict) is not repeatable:**
- **Cross-machine replays.** An audit (arXiv 2607.01211) replayed the official reference patches of three benchmarks on 4 machine types x 3 rounds. Each patch counted only if it passed that benchmark's own speed-up rule in all 12 replays. [src] [perf-bench-reliability](per-system/perf-bench-reliability.md)
  - GSO: **39/102**
  - SWE-Perf: **11/140**
  - SWE-fficiency: **411/498**
- **No numeric advice.** The audit's advice is qualitative; it recommends no specific repeat count, statistic or test. [src] same note
- **SWE-Opt's gates.** Its acceptance gates are a 20% noise ceiling, SNR >= 2 and a >=5% minimum effect. RCIW 0.1 is only its sampling stop rule, and it pins via cpuset=2. [src] [swe-opt](per-system/swe-opt.md)
- **Unverified ordering.** That SWE-fficiency, which pins cores, is the most stable fits F4 by validity rate (411/498), but not by within-task noise (median std: SWE-Perf 1.41 pp < SWE-fficiency 2.41 pp < GSO 3.81 pp, Table V). The link is our inference, not the audit's claim. [inf]

**Correctness oracle (the tests) is weak:**
- **SemOpt's Python projects.** All 9,483 candidates pass the unit tests (100%, from 152 hotspot functions). The paper does not report test counts or coverage. A test set that rejects nothing cannot tell a reduced test set from the full one. [src] [semopt](per-system/semopt.md), Sec. 5.3, Table 16; [inf] for the consequence
- **SysLLMatic.** [src] [sysllmatic](per-system/sysllmatic.md)
  - GraphChi has ~10% coverage.
  - 1 of 145 "correct" HumanEval programs had its core removed.
  - Parallel races passed the tests.
- **PerfAgent.** Coverage-based selection misses native-code regressions (§VI). [src]
- **GSO and SWE-Perf.** Output-equivalence-only correctness (GSO) and perf-tests-only correctness (SWE-Perf) are weaker than a regression suite. [inf]

**Paper-vs-code mismatches are frequent. W3 should cite code, not only papers.** [src]
- SWE-fficiency installs (App. F.1)
- SWE-Perf core counts
- Mercury's Beyond metric (code does not clip runtime to [min,max]; scores can then exceed 1 [inf])
- COFFE timeouts (50 s in code vs 5 s in the paper)
- SysLLMatic's final rebuild

**Implication for W3** (the performance part has already gone to W3) [inf]:
- Before attributing a missed fault or a flipped accept/reject to the reduction, measure:
  - the repeatability of the full-benchmark decision (same edit, repeated runs, pinned cores or a deterministic proxy)
  - whether the full test suite rejects anything at all (mutation or injected faults)
- Otherwise "reduced ~ full" may only mean that both oracles are blind.

## What nobody in this sample does (with the search behind it)

1. **In an optimization loop, reduce or make incremental the build per candidate edit by an explicit rule.** Not found in 24 core notes (code read for 19 public artifacts; PerfAgent, SemOpt, AlphaEvolve, ECO, Meta PTS and TAP builds are [unk]), nor in the 12 discovery queries and late searches (a)–(d) in `per-system/_discovery-log.md`. [unk]→gap, conditional on W1.
2. **Select performance benchmarks per edit by a deterministic rule derived from the diff.** Not found (human/agent regex subsets exist, F3). [unk]→gap.
3. **Measure the miss rate of per-edit test selection on optimization edits.** PerfAgent reports only reduction %, and no artifact exists to reproduce it. [src]/[unk]
4. **Schedule periodic full ("checkpoint") validation across a sequence of accepted optimization edits, and measure what it catches.** Found only in functional CI (Meta, Google). [src]/[unk]
5. **Report per-candidate validation cost broken down as build / tests / benchmarks.** No system reports this. EvalPerf gives ≈15 min per model; FormulaCode an average of 38 min per task. [unk]

Search record: the discovery researcher's queries and the kept/dropped candidates are in `per-system/_discovery-log.md`. The architect's four late queries (2026-11-21) surfaced PerfAgent, SysLLMatic, FormulaCode, TDAD (arXiv 2603.17973, test-impact graph for *bug-fixing* agents: belongs to W1), TestPrune (2510.18270), PERFOPT-Bench, SWE-Opt, CodeEvolve, and a 2026 audit of performance-benchmark reliability (2607.01211). The last four have critic-checked notes (critic-log-E.md). "Not found" here means not found in this sample and these searches. It is not a proof of absence.

## Consequences for the experiment design (to W3, via PM)

1. **Control arm** = full validation per edit: rebuild of the working tree (full reinstall as the harness-style reference), the fixed per-task test set, all workloads, repeated timing + MWU. [src]
2. **Test-selection arms** to compare:
   - filename mapping (FormulaCode)
   - Python coverage / testmon (PerfAgent)
   - curation-time expert-diff subsets (SWE-fficiency/SWE-Perf), as an upper bound that uses future knowledge
3. **Build arm**: incremental rebuild (skip the rebuild when only `.py` files changed; otherwise rebuild only the changed extension) vs full reinstall. Report seconds per edit, which nobody publishes.
4. **Benchmark arm**: workloads selected by the coverage/profile of the changed functions vs all workloads. Report agreement of the accept/reject decision.
5. **Checkpoint arm**: full validation every k accepted edits + final. Report the faults/regressions caught at the checkpoint vs at the per-edit stage.
6. **Use native-extension repos** (numpy/pandas/scipy-like, as in SWE-fficiency/GSO) so the coverage-misses-native-code hole in F7 can be measured.
7. **Oracle checks first** (F7): repeatability of the full-benchmark verdict and fault-detection power of the full test suite, as the yardstick for every reduced arm.
