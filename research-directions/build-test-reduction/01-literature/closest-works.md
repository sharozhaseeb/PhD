# Closest works

**Status:** v3.2, 2026-11-21 (rows 21–22 from the ACM DL / IEEE Xplore searches, `database-search-2026-11-21.md`). Rows 1, 8 and 17 come from full reads of PerfAgent, Fallahzadeh 2025 and Sayedsalehi 2026 (`notes/R1`, `notes/R2`). Forward citations of PerfAgent and NameRTS were screened (`notes/R3`).

**What the works are compared against.** Study 1 first *measures* where existing deterministic reduction becomes unsafe for performance-motivated, accumulating edits (claims C5, C7, C8, C11 in `beyond-literature-claims.md`). The RQ3 policy follows from those findings. It has three parts:
- (a) track the change accumulated since the last full check;
- (b) select benchmarks from profiles or call graphs;
- (c) trigger a full check when the accumulated change crosses a threshold.

**Labels:** [R] read in full source · [F] read through a web-fetch summary · [A] abstract only · [W2] W2 survey. Overlap and difference are our judgement.

**Figure:** [figures/positioning.svg](figures/positioning.svg) places these works on a grid. The rows are per-revision decisions versus decisions across edits. The columns are build, tests and benchmarks.

| # | Work | What it does | Overlap | What differs |
|---|---|---|---|---|
| 1 | **PerfAgent** (`deng2026perfagent`, arXiv 2607.19653 v1) [R, full read] | LLM agent for repository-level Python optimization. Each iteration builds via `/build.sh` and runs only the tests pytest-testmon selects (§III-D: 66–99% fewer tests on GSO, 47–98% on SWE-fficiency-Lite; for example numpy 34,458 → 109 tests, App. B Tables X–XI). The best patch is the fastest of up to 5 submissions. | Per-edit coverage-based test selection inside an optimization loop. **Not new.** | It never runs the full suite, and reports **no misses or safety evaluation** of testmon (§III-D, §VI). The authors say native-extension regressions "can slip between iterations" (§VI) and list native coverage as future work (§VII). How the testmon database is seeded and refreshed, and whether the build is incremental, are not stated [U]. It selects no benchmarks and has no checkpoints. No code is linked. **This is the gap Study 1 measures (C5, C7).** |
| 2 | **pytest-testmon** [F] | Selects tests by the checksums of the code blocks they executed (coverage.py). | Baseline selector (F6). | Decides per change against the last recorded run. Python lines only. |
| 3 | **Ekstazi** (`gligoric2015ekstazi`) [R] | Dynamic RTS from file and class dependencies with checksums. | F1 baseline; end-to-end time accounting. | Dependencies come from one observed run and are refreshed only for tests that ran (§3.3, §5). Staleness over several revisions is not measured (C7). |
| 4 | **STARTS / static class-level RTS** (`legunsen2016static`, `LegunsenShiMarinov2017`) [R/A] | Static type-dependency selection. | Alternative selector. | Per revision. Unsafe under reflection. Java. |
| 5 | **NameRTS** (`WangPradelLiu2026`, preprint) [R] | Python RTS at name level: −45.6% time, safe on 99.6% of 500 commits. | The strongest Python selector found. | Per commit. Commits that change only non-Python files are excluded (§4.1). **Code exists:** github.com/ZJU-CTAG/NameRTS, Apache-2.0, a replication package with no documented command for arbitrary repositories (`notes/R3`). One forward citation: FastCI, arXiv 2610.01967, for GPU training CI [A]. |
| 6 | **Elbaum, Rothermel, Penix** (`Elbaum2014`) [R] | Selects test suites by failure and execution windows. | Staleness guard per test (F4). | Counts time or commits per *test*, not accumulated *code change*. Not a full-run trigger. |
| 7 | **Google TAP milestones** (`memon2017taming`) [R] | Bundles changes and runs affected tests per milestone (about 45 min). | Window-based validation. | Milestone timing comes from resource heuristics. Independent human commits. Functional only. |
| 8 | **Batching vs selection at scale** (`fallahzadeh2025contrasting`, EMSE 30, 2025) [R, full read]; also `najafi2019bisecting` [R], `beheshtian2022batch` [A], `fallahzadeh2023parallel` [F] | Compares RTS, prioritization and batching on 285 M test results. BatchAll is a *variable*, queue-driven batch of all waiting changes (§4.5, p.19). Selection misses up to 55% of failures; batching misses none by its simulation assumption. | A variable batch size is already studied head to head with selection. Our fixed-k cap is their constant batching. | No per-change reduced check *before* the batch; selection and batching are alternatives, and combining them is future work (p.54). Commits are independent, not a sequence of dependent edits. Functional only. |
| 9 | **Meta stabilization** [W2] | Selects tests per diff; all tests on master every few hours. | Reduced check per change plus periodic full runs. | The full run is time-triggered. Selection is learned. |
| 10 | **Perphecy / PerfRanker / microbenchmark prioritization** (`deoliveira2017perphecy` [A], `mostafa2017perfranker` [R], `laaber2021tcp` [R]) | Choose or order performance tests per commit. | Part (b). | Mostly ordering, not dropping, so no miss rate (C11). Java/C++. |
| 11 | **Grambow et al.** (`grambow2022microbenchmark`) [R] | Reduced microbenchmark suite plus a daily application benchmark as backstop. On InfluxDB it missed a trend and raised 17 false alarms. | A precedent for dropping benchmarks (C11). | Fixed suite, time-triggered backstop. Go. |
| 12 | **µOpTime** (`japke2025uoptime`) [R] | Fewer repetitions per benchmark, configured from an old full run. | P4. | Configuration never refreshed. Java/Go. |
| 13 | **MongoDB change-point CI** (`daly2020changepoint`) [R] | An earlier threshold system compared runs with the previous run, a week-old run and the last stable release. It gave up to 99% false positives and was replaced by change-point detection. | P5 drift guard. | Detects drift after the fact. No selection. |
| 14 | **Kotinos** (`gallaba2020kotinos`) [R] | Skips unaffected build steps; bypassed for graph-structure changes. | B3 change-type trigger. | Per commit. Build only. Not Python-specific. |
| 15 | **SysLLMatic** [W2] | Accumulated accepted optimizations; final rebuild and re-measure. | Final full validation (C3 rule). | No intermediate checks, no selection. |
| 16 | **Jin & Servant** (`jin2021helped`) [F] | CI techniques compared on cost, missed failures and delayed feedback. | Evaluation dimensions. | No periodic full runs studied. |
| 17 | **Risk-aware batch testing of performance tests** (`sayedsalehi2026riskaware`, arXiv 2604.00222 v1, Mozilla) [R, full read] | Batches commits for performance jobs. Strategies are fixed-size (FSB), time-window (TWB) and risk-adaptive (RASB/RAPB/RATB). The "-la" variants keep a **cumulative risk sum and flush when it exceeds a threshold**, with time caps (§VI-A). Backfilling finds the culprit. RAPB-la: −32.4% tests, −26.2% maximum time-to-culprit (Table IV). "-s" variants combine a subset with batching. Learned per-commit risk (ROC-AUC 0.694). | **Our full-check trigger (candidate rule C5) is a deterministic variant of RASB-la**: an additive budget, flushed at a threshold, with a cap. | Our risk input is measured and model-free (diff size, native edits, benchmark drift), not learned. Every edit gets an immediate reduced check; the full check validates the *accumulated state* of a dependent edit chain, not independent commits. There is no matched-cost comparison with fixed-size batching in either paper. Only 15 regressing commits in its test split. |
| 18 | **Ekelund & Engström** (`ekelund2015history`, ICSME 2015) [A] | History-based recommendation (about 4% of the suite, about 80% of relevant tests). | F4. | Calendar- or rule-based full runs. |
| 19 | **RTSLinux** (`celik2017rtslinux`, ESEC/FSE 2017) [A] | RTS across the JVM boundary (spawned processes, native code): 74.17% of tests skipped. | Shows that a native boundary breaks language-level RTS (C5). | JVM only, not Python extensions. |
| 20 | **Agentic issue-resolution survey** (`jiang2026agenticsurvey`, arXiv 2512.22256 v2) [R, targeted read] | Reports that agent scaffolds select regression tests by LLM judgement, "unsound in both directions" (§5.1.1 D, p.13). Program-analysis RTS "has not been integrated", and Python techniques "remain unsafe" (§7.3, p.23). | Independent support that validation in LLM edit loops lacks sound selection. | A survey; it does not measure. Nothing on batching or triggers. |
| 21 | **Chittimalli & Harrold** (`chittimalli2009recomputing`, TSE 35(4) 2009; ICSM 2007) [A] | RECOVER recomputes accurate coverage for P(i+1) without rerunning tests that do not reach the changes. They argue against estimating coverage and against reusing outdated coverage from P(i). | C7: shows that stale coverage harms selection; recompute vs reuse is our F3 refresh question. | One version step, not a growing refresh interval over dependent edits. Abstract only (full text needs institutional access). |
| 22 | **Elsner et al.** (`elsner2022buildaware`, ICSE-SEIP 2022) [A] | Industrial multi-language (Java, C/C++, non-code) RTS through the build system. Compiles only affected modules; up to 75% of tests excluded, no escaped failures on 397 PRs. | C5 (native boundary), C8 (selective compilation). | Not Python. Does not measure misses on native edits or the correctness of incremental builds. |

**PerfAgent's forward citations** (7 papers, `notes/R3`, abstract-only):
- Three concern validating optimization edits: Dr. Greens (arXiv 2611.23203, a behaviour-preservation verifier), FrontierRefactor (2610.25834, a behaviour plus runtime-regression benchmark) and DuoDiscover (2610.17184, cheap proxy evaluators).
- **None selects tests or benchmarks, or reduces the build.**

## Answer to "what's new compared with Ekstazi, STARTS, testmon and incremental builds?"

**Short answer.** Those tools are not new to us, and we do not claim a better selector. What we found missing is *evidence of where they become unsafe* when the edits are performance optimizations that build on each other. The closest system, PerfAgent, uses testmon on every iteration, but never measures what it misses and names native extensions as a hole. Study 1 measures four things:

1. **The native-extension boundary (C5).** Python coverage-based selection cannot see C/Cython edits. PerfAgent §VI names this; RTSLinux shows the JVM analogue matters. No Python measurement was found.
2. **Dependency and profile data going stale across edits (C7).** Ekstazi §5 and testmon refresh only the tests that ran. In a chain of edits, unselected tests' maps age. Chittimalli & Harrold (TSE 2009, #21) show that outdated coverage makes selection inaccurate for one version step. No study measures misses as the refresh interval grows.
3. **Dropped benchmarks (C11).** Performance-test work mostly *orders* benchmarks (#10). The partial precedents for *dropping* them report misses (#11; Ding et al.). No per-edit miss rate for Python, including native code, was found.
4. **Incremental-rebuild correctness for Python extensions (C8).** setuptools and Cython decide by timestamps and miss flag changes [F]. No empirical study was found.

The RQ3 policy follows from these: rules aimed at each mechanism (B2–B4, F2–F3, P1/P7/P8), plus a full check when accumulated change crosses a threshold.

**We concede that the trigger is a variant of risk-mass batching** (#17, RASB-la). The claim is only about its deterministic form in this setting, compared with fixed-k at matched cost (C1).

**Not claimed:**
- per-edit test selection in optimization loops (PerfAgent);
- a two-sided performance gate (SemOpt, PerfAgent);
- periodic full runs (Meta, Google);
- batching, bisection, or variable and risk-based batch size (#8, #17);
- comparison against a stable baseline (MongoDB);
- culprit finding (out of Study 1 scope).
