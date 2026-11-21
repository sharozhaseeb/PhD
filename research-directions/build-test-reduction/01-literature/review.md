# Reduced build and test validation: methods review

**Status:** draft v3, 2026-11-21 (§5 updated with full reads of Fallahzadeh 2025 and Sayedsalehi 2026). Synthesised from five researcher source-card files (`notes/T1`–`T5`), a W2 intake note, and eight gap searches run by the architect. A critic pass checks every citation against its source.\
**Evidence boundary:** this is a targeted primary-source review, not a systematic review. Papers and documentation were read; no result was reproduced. Section and page locations come from the source cards in `notes/`. The card holds the exact passage.

**Labels.** Each claim carries one of these tags:

| Tag | Meaning |
|---|---|
| **[R]** | Read in the source, at the location given. |
| **[F]** | Read through a web-fetch extract. The fetch tool returns a summary, so treat any quotation as a paraphrase. |
| **[A]** | Only the abstract, a landing page or a search snippet was read. |
| **[I]** | Our own inference. |
| **[U]** | Unknown. |

Citation keys refer to `references.bib`.

The question this review serves is: **which deterministic techniques can reduce the build, test and benchmark work done for each optimization edit, and what has to hold for them to stay safe?** Section 6 summarises the answer. Two files take it further: `assumptions-under-iterative-optimization.md` covers what breaks in our setting, and `candidate-rules.md` gives the rules W3 can run.

---

## 1. Reduced and incremental builds

### 1.1 What "correct" means
- Mokhov, Mitchell and Peyton Jones define a correct build: after it runs, every non-input key equals what recomputing its task on the result would give. In other words, an incremental build is correct when it equals a build from scratch. This holds for acyclic tasks and is relaxed for non-determinism and cloud builds. [R] `mokhov2020buildsystems` §3.6 pp.15–16, §8.3–8.4
- Their definition of minimality: rebuild only tasks that transitively depend on changed inputs. Make reaches this only if file timestamps are not tampered with. [R] `mokhov2020buildsystems` §2.1 p.4, fn.5 p.5
- Forward build systems are correct if they "produce the same result as running the commands in order, or report an error". Rattle assumes that tracing data is complete. [R] `spall2022forward` §1, §2
- Pluto: sound means the generated files reflect the latest sources. It argues that declaring dependencies statically forces over-approximation, because "a missing dependency makes the build script unsound". [R] `erdweg2015pluto` §1–2
- LaForge also takes "same output as a full build" as the key correctness property. [A] arXiv 2108.12469, found in gap search G6, not read

### 1.2 Why incremental builds go wrong
- **Missing or unspecified dependencies.** Bezemer et al. found more than 1.2 M unspecified dependencies in four Make projects, from six causes. The industry workaround is a clean full build, or repeating the build until nothing changes. [R] `bezemer2017unspecified` Abstract, §1
- **Generator scripts.** Licker and Rice found incorrect rules in 30 projects by build fuzzing. One case is a generator script whose Python imports were not declared, so editing the script did not regenerate the output. [R] `licker2019incorrect` Abstract, §I, results table
- **Timestamps, the untracked environment and non-determinism.** These include compiler version and flags, environment variables, `__TIME__` and absolute paths. [R] `mokhov2020buildsystems` §8.3; [F] `bazelhermeticity`, `bazelremotecaching`, `ccachemanual`, `sccacheREADME`
- **Cache hits on stale actions.** Bazel's remote cache lets users with different compilers "wrongly share cache hits" when tools outside the workspace are not tracked. [F] `bazelremotecaching`
- **ccache direct mode** can miss new header files. [F] `ccachemanual`
- **Changes to graph structure.** Kotinos skips its acceleration entirely for commits likely to change the build dependency graph, such as added or renamed files. [R] `gallaba2020kotinos` §4

### 1.3 How faults are detected
| Method | Source |
|---|---|
| Change an input, build incrementally, compare outputs with what the traced graph predicts (build fuzzing) | [R] `licker2019incorrect` §III; ptrace costs about 2× on clean builds (§V-E) |
| Check one traced full build against the declared specification (BuildFS): 237 issues confirmed and fixed in the body (§1, §5), 247 in the abstract | [R] `sotiropoulos2020buildfs` Abstract |
| Infer dependencies per commit without a clean build (C/C++ and Make only) | [R] `lyu2024echecker` (v1); venue [U] |
| Sandbox each task so a missed dependency becomes a runtime error | [R] `esfahani2016cloudbuild` §3.4 |
| Null-build check, comparing cache hits across machines, building in a clean container | [F] `bazelhermeticity` |
| Compare a clean build with the incremental build | Practised [R] `bezemer2017unspecified` §1; the formal criterion is [R] `mokhov2020buildsystems` §3.6. **No source gives a schedule for running it.** [U] |

### 1.4 Build avoidance and caching at scale
- **CloudBuild** decides whether to reuse a build from the content of its inputs. It notes that wrong dependencies "lead to false cache fingerprints and hence false cache hits". [R] `esfahani2016cloudbuild` §1–2, §3.4. Its 1.3–10× speed-up figure is [A].
- **Kotinos** speeds up at least 87.9% of builds, and 74% of those run at least 2× faster. Its stated preconditions are pinned locks, isolated tests and little conditional build behaviour. [R] `gallaba2020kotinos` Abstract, §9 (threats to validity)
- **CI caching in practice.** About 30% of projects adopt caching, and 27% cache unused dependencies. [R] `ghaleb2026cicaching` Obs. 1.1, 4.3 (EASE 2026 per the PDF header)

### 1.5 Python build mechanisms
- **setuptools.** `build_ext` skips an extension unless its `sources + depends` are newer (by mtime) than the `.so`, or unless `force` is set. Headers are tracked only if listed in `depends`. [F] `distutilsbuildext` (source file)
- **Cython.** `cythonize` regenerates the `.c` file by comparing the timestamps of the `.pyx` and the `.pxd`/include files it transitively cimports. In the code read, it did not use `Extension.depends` or directive changes in that decision. [F] `cythondependencies`; verify empirically.
- **Bytecode.** PEP 552 offers three `.pyc` modes: timestamp (the default; it stores source mtime and size), checked-hash and unchecked-hash. [F] `pep552`
- **meson-python editable installs.** A stub rebuilds compiled parts on first import. The build directory and build dependencies must remain, and new entry points or metadata need a reinstall. [F] `mesonpythoneditable`
- **scikit-build-core.** Rebuild-on-import is experimental. A loaded extension cannot be reloaded in the same process. [F]/[A]
- **uv cache.** For directory dependencies, the cache keys on the mtime of `pyproject.toml`, `setup.py` and `setup.cfg`. [F] `uvcache`
- **Gap search G6.** No empirical study of stale `.so` files or rebuild correctness for Python extension modules was found. [searched, not found]

## 2. Functional regression test selection (RTS)

### 2.1 Foundations
- **Safe selection.** A technique is safe if it selects every test that can reveal a fault. That is achievable under controlled regression testing: all factors other than the code are held constant. Selecting every test that traverses the modified code is then safe. Selection that is both safe and fully precise is undecidable. [R] `rothermel1997safe` §3.1.2, §4.1 pp.194–195
- **Four evaluation categories** (introduced in the TSE 1996 paper): inclusiveness, precision, efficiency and generality. [R] as summarised in `rothermel1997safe` §4.1. The TSE 1996 text itself was not read: `rothermel1996analyzing` [U].

### 2.2 Dynamic and static tools
- **Ekstazi** works at file and class level. It records every file a test reads, including attempts to read files that do not exist, and reruns a test when a checksum changes.
  - Collecting only classes is unsafe when tests read external files. [R] `gligoric2015ekstazi` §2–3
  - End-to-end time (analysis + execution + collection) averaged 68% of RetestAll and 46% for suites longer than a minute. Short suites can get slower. [R] §4.3
  - Dependencies come from one observed run only. [R] §5
- **Static RTS (Legunsen et al.).** Class-level static selection is comparable to Ekstazi but unsafe in 0.2% of revisions on average, relative to Ekstazi. Method-level static selection is unsafe in 10.6%. Reflection is the main cause. [R] `legunsen2016static` §4.2–4.3
- **STARTS** (tool paper): about 35% of tests selected and about 81% of RetestAll end-to-end time. [A] `LegunsenShiMarinov2017`
- **HyRTS** (hybrid file and method level). [A] `Zhang2018HyRTS`
- **RTS in cloud CI.** Total build time with RTS was 76.0% of RetestAll. Class-level selection misses changes to non-source files, so the hybrid falls back to module level. RTS missed 39 failures, 38 of them flaky. [R] `ShiZhaoMarinov2019` Abstract, §I. Venue not confirmed from the text [U].
- **When RTS pays off.** Static method-level RTS was slower than RetestAll in 97.3% of Java projects, and 62.2% of projects have test time at most 25% of the interval between commits. [R] `WangYu2018` Abstract
- **Semantics-aware RTS** skips changes that cannot alter test behaviour. [R/A] `Liu2023`
- **Checking RTS tools (RTSCheck).** Seven rules found 27 bugs in Clover, Ekstazi and STARTS. Safety rule R1: a test that newly fails under RetestAll must be selected. The rules assume no flaky tests and no order dependence. [R] `zhu2019rtscheck` §I, §III-A, Table I

### 2.3 Python
- **NameRTS** (arXiv preprint, May 2026) is the only *Python-specific, fine-grained* RTS study found. Otherwise Python is covered by the polyglot, file-level BabelRTS (TSE 2025, `MaurinaCazzolaGhosh2025`, which NameRTS calls the state of the art) and by tool papers (pytest-rts).
  - **Why file level fails in Python.** Eager imports make file-level selection nearly useless. A safe file-level baseline (EkstaP) saves 3.10% of time, because one test file imports 83% of source files on average. [R] `WangPradelLiu2026` §1, §4.2
  - **Name-level results.** Selection at name/function level skips 69.9% of test files, cuts end-to-end time by 45.6%, and selects every affected test in 99.6% of 500 commits. [R] Abstract, §4.2
  - **Misses.** The misses came from shared global state and an external-library callback. eval and exec are not modelled. [R] §3.4, §4.2, §5
  - **Overhead.** About 10% of full-suite time, paying off after about 5 commits. [R] §4.3
  - **Excluded commits.** Commits that change only non-Python files were left out of the evaluation. [R] §4.1
- **pytest-testmon** reruns a test when the checksum of a code block it executed changes, using coverage.py. Its docs say its "limits and reliability" equal coverage.py's. [F] `TestmonBlog`. Neither testmon's nor coverage.py's docs say anything about C extensions or data files. [F] `CoverageTrouble`; [U]
- **Cython coverage** needs the generated C sources and trace-enabled builds. [A] gap search G4 (Cython `Coverage.py`; meson coverage issue #6186)
- **Other Python tools.** pytest-rts uses coverage contexts per test [A]. pytest `--lf/--ff/--nf` and pytest-picked are heuristics, not safe RTS. [F]
- **BabelRTS** (polyglot, file level, regex rules) was safe on only 76.6% of commits in the NameRTS study. [R via `WangPradelLiu2026` §4.2]
- **RTS across native boundaries exists for the JVM.** RTSLinux tracks dependencies through spawned processes and native code: 74.17% of tests skipped and 52.83% of time saved in 21 Java projects. [A] `celik2017rtslinux`. BinaryRTS (Java and C++ via JNI) was found by the critic's search but not read [U].
- **Gap search G4.** Nothing was found on RTS through compiled *Python* extensions. One 2026 paper detects C extensions by file suffix (.so/.pyd) for test generation. [A] arXiv 2603.06107

### 2.4 History-based selection and prioritization
- **Google pre-submit selection (Elbaum et al.).** Select a test suite if it failed within a failure window, has not run within an execution window, or is new. No coverage is needed. [R] `Elbaum2014` §4.1, Alg. 1
- **Multi-revision RTS.** Selection over distributed histories (branches, merges) reasons over several old revisions. It does not address dependency data going stale. [A] `gligoric2014distributed` (CAV 2014)
- **History-based selection in industry.** Recommends about 4% of the suite and finds about 80% of relevant tests; periodic or rule-based full runs are treated as a policy choice. [A] `ekelund2015history`
- **Manual selection.** Developers' own test picks differed from automated selection in every one of 450 sessions, and picked fewer tests 27% of the time. [R] `GligoricNegaraLegunsenMarinov2014` Abstract
- **APFD.** The classical APFD paper (Rothermel et al., TSE 2001) was not obtained [U]. APFD-P, a performance variant, is defined in `laaber2021tcp` §4.4 [R].

### 2.5 Flaky and order-dependent tests
- Luo et al. treat deterministic outcomes as an important assumption of regression testing. Async wait, concurrency and test-order dependency make up 77% of the 161 studied commits. [R] `Luo2014` Abstract (the assumption); §3 (77%); F.1 names the categories
- In Python, 0.86% of tests are flaky and 59% of that flakiness is order dependence. [R] `Gruber2021` Abstract (59%), §IV (0.86%)
- iDFlakies: 50.5% of 422 flaky tests are order dependent. [R] `Lam2019iDFlakies` Abstract
- The flaky-test survey defines victim and brittle order-dependent tests. [R] `Parry2021` §3.2
- Learned predictive selection (`Machalica2019` [A]) and combining machine learning with analysis-based RTS (`ZhangLiuGligoricLegunsenShi2022` [R]) are **out of scope: a later AI study**.

## 3. Performance testing and benchmark selection

### 3.1 Selecting and prioritizing performance tests
- **PerfScope** (Huang et al., ICSE 2014) analyses each commit's risk of slowing things down. It is C/C++ only, and is described as trained, which makes it a learned model. [A] `huang2014perfscope`
- **Perphecy** (ICST 2017) predicts which commits and tests need performance testing, described as "simple". Its method details were not read [U]. PRICE calls it the state-of-the-art deterministic approach. [A] `deoliveira2017perphecy`, `alshoaibi2019price`
- **PerfRanker** ranks tests by the estimated performance impact of a revision. The three most-affected tests appear within the top 30–37% of the ranking, against 65–79% for the baselines. Java only. [R] `mostafa2017perfranker` Abstract, §1
- **Prioritizing microbenchmarks** (54 technique variants, 10 JMH projects). Mean APFD-P is 0.54–0.71. The three largest changes are found after running 29–66% of the suite, and the best overhead is 11%. Dynamic coverage beats static coverage. [R] `laaber2021tcp` Abstract, §4.2
- A greedy order based only on each benchmark's history of performance changes is as good or better, at under 1% overhead. [R] `laaber2022searchbased` Abstract, §1 (arXiv)
- **These are orderings, not selections.** No miss rate is reported for selecting benchmarks by coverage. [I]; T3 gap
- **A reduced microbenchmark suite as a proxy for an application benchmark** (Grambow et al.). On InfluxDB it found 4 true positives and raised false alarms on 17 commits, and it missed a regression trend. The authors keep a daily application benchmark as a backstop. [R] `grambow2022microbenchmark` results (Fig. 9), §7
- A companion paper uses application-benchmark call graphs to measure how relevant a microbenchmark suite is. [A] PeerJ CS 2021 (PMC8176533), found in gap search G2
- **Microbenchmarks can be the more sensitive instrument.** In a testbed, microbenchmarks caught three injected issues earlier than application benchmarks. [R] `japke2023early` §1

### 3.2 Reducing repetitions: dynamic reconfiguration and stopping criteria
- **Dynamic reconfiguration** (Laaber et al., FSE 2020) stops a benchmark once its results are stable, using one of three criteria: CV, RCIW or KLD. It saves 48.4–86.0% of time with the same result quality for 78.8–87.6% of benchmarks. [A] `laaber2020dynamic`. The criteria are described [R] in `traini2023steady`.
- **µOpTime** (TOSEM 2025) fixes the number of repetitions per benchmark from an earlier full run. [R] `japke2025uoptime` Abstract, §1 RQ1–4
  - Median reductions are 76.8% (Go) and 13.1–26.8% (Java).
  - Simulated over successive versions, it raised 3 and 29 false positives and missed 2 and 7 changes.
- **Steady state is not guaranteed.** Developer-set warmups are wrong in many forks [R] `traini2023steady`. At most 43.5% of VM–benchmark pairs consistently reach peak steady state [R] `barrett2017warmup` Abstract.

### 3.3 Measurement rigour and bias
- **Confidence intervals, not best-of-N.** Compare alternatives through the confidence interval of the difference, use multiple VM invocations, and detect steady state with a CoV threshold. [R] `georges2007rigorous` §2–4
- **Repetitions per level.** Kalibera and Jones choose how many repetitions to run at each level (process, iteration) for a target precision on a fixed budget, and give a confidence interval for the ratio between versions. [R] `kalibera2013rigorous` Abstract, §1; effect-size CI [A] `kalibera2020effectsize`
- **Environment size and link order bias results.** Mytkowicz et al. saw shifts of often about 33% and once almost 300%, and none of 133 surveyed papers handled this. [R] `mytkowicz2009wrong` §1
- **Re-randomising memory layout (Stabilizer)** makes t-tests and ANOVA valid at under 7% overhead. Link order alone can change performance by up to 57%. [R] `curtsinger2013stabilizer` §1–2
- **Cloud noise.** The coefficient of variation ranges from 0.03% to over 100%. Running both versions on the same instance in random order detects slowdowns of 10% or less. A/A runs measure the false-positive rate. [R] `laaber2019cloud` Abstract, §5.3
- **Duet benchmarking** runs both versions concurrently on one machine. Accuracy improves 2.3–12.5× (ScalaBench/DaCapo) and 23.8–82.4× (SPEC CPU 2017), assuming both versions see the same interference. [R] `bulej2020duet` Abstract, §4.2

### 3.4 Unit tests as performance tests
- Running existing tests before and after known performance fixes, 74.3–76.9% of tests that execute the changed code showed **no** improvement. Causes include small input sizes and too few repetitions. [R] `ding2020readily` §3–5
- Performance-regressing changes often come with improvements in other metrics, and developers may not notice them even while optimizing. [R] `chen2017exploratory` §1
- Performance tests are a small and rarely updated part of Java test suites. [A] `leitner2017state`, `stefan2017unit`

### 3.5 Detecting changes in CI
- **MongoDB's earlier system** compared each run with the previous run, a run a week earlier and the last stable release. It produced up to 99% false positives and named "multiple small changes over time causing a drift down" as a failure mode. The replacement uses change-point detection (E-Divisive means). [R] `daly2020changepoint` §1–2
- **Hunter** replaces the randomized permutation test with Student's t-test so that results are deterministic. [R] `fleming2023hunter` Abstract

### 3.6 Python tooling (documentation)
- **pyperf**
  - By default it runs 20 processes × 3 values with 1 warmup (CPython), each value at least 100 ms. [F] `pyperfdocs`
  - `compare_to` applies a two-sided t-test. [F]
  - `system tune` sets the CPU governor and similar settings. [F]
- **asv**
  - `continuous` compares two commits side by side and supports `--interleave-rounds` and `--bench`. [F] `asvdocs`
  - `compare` flags a change at `--factor`, which defaults to 1.1. [F]
  - `find` bisects for the commit with the largest regression and works best when runtimes are "mostly monotonic". [F]
- **CodSpeed** has a CPU-simulation instrument that counts weighted instructions and cache-miss penalties and excludes I/O and system calls. Its docs do not name Valgrind [U]. [F] `codspeeddocs`
- **pytest-benchmark** `--benchmark-compare-fail` uses a percentage threshold, with no statistical test. [F] `pytestbenchmarkdocs`
- **No peer-reviewed study of Python benchmark selection or stability was found.** T3 searches 27 and 36, gap search G2

## 4. Evaluating whether selection is safe

### 4.1 Metrics
| Metric | Definition (location) |
|---|---|
| Inclusiveness, precision, efficiency, generality | [R] `rothermel1997safe` §4.1, summarising TSE 1996 |
| Safety violation | \|E∖T\| / \|E∪T\| against a reference selection E; also the % of revisions with any violation [R] `legunsen2016static` §4.2.3 |
| Missed newly failing tests against RetestAll | RTSCheck rule R1 [R] `zhu2019rtscheck` Table I |
| End-to-end time | Analysis + execution + collection (+ build), reported both with and without collection (offline vs online) [R] `gligoric2015ekstazi` §1, §5; `legunsen2016static` §3 |
| Suite-size reduction and mutant-based fault-detection loss | [R] `shi2014balancing` §3 |
| Failed-build detection loss (FBDL) | Loss measured on *future* failed builds from a reduction point. Traditional metrics do not predict it. [R] `shi2018evaluating` §1, §3 |
| APFD-P and Top-N for benchmarks | [R] `laaber2021tcp` §4.4 |
| Delayed observation of failures | Jin and Servant evaluate CI techniques on cost saving, missed failure observation, and early or delayed feedback. [F] `jin2021helped` §III–IV; also gap search G7. **No named "detection delay in edits" metric exists for periodic full checks.** [searched, not found] |

### 4.2 Mutants and injected faults
- **Mutants are a partial proxy for real faults.**
  - Just et al.: 73% of real faults are coupled to mutants, 17% are not, and 10% need stronger operators. [R] `just2014mutants` §1
  - Andrews et al.: on one program with real faults, mutants predicted real-fault detection. [R] `andrews2006using` Abstract, §4 threats
  - Equivalent mutants are undecidable, and redundant mutants inflate scores. [R] `papadakis2019mutation` §5.3
- **Google** creates at most one mutant per changed line. Python mutants survive most often (14.7%). [R] `petrovic2018state` §3, §5
- **Commit-relevant mutants lie mostly outside the changed lines** (81%). [A] `ojdanic2021evolving`
- **Injected performance regressions (Peass).** Busy-waits were inserted into methods on a benchmark's call tree, one per commit, across 1,000 Jetty commits. 58.7% were detected, 26.7% were lost to noise and 14.6% were not covered. [R] `reichelt2023peass` §IV (QRS 2022)
- **Performance mutation operators** for C++. [A] `delgadoperez2021performance`
- **Real performance bugs.**
  - Jin et al.: simple, functionality-preserving changes give large speed-ups. [R] `jin2012understanding` §1
  - Zhao et al.: only 15% of performance fixes revise tests, 13% in Python. [R] `zhao2022largescale` §5

### 4.3 Datasets
- BugsInPy: 493 reproducible, isolated Python bugs. [R] `widyasari2020bugsinpy` §2
- Java only: RegMiner [R], RTPTorrent [R], Defects4J [A]. TravisTorrent [A].

## 5. Batching, checkpoints and culprit finding

- **Batch testing at Ericsson (Najafi et al.).** Bisecting a failing batch costs about 2·log2(n)+1 runs. [R] `najafi2019bisecting` §2, §4–5
  - The best batch size shrinks as the culprit rate and flake rate rise.
  - Most savings arrive by batch size 4.
  - Flaky batches add #Batches × FlakeRate × 2·log2(n) runs (Eq. 7–8).
  - Testing the riskiest commits first saves 7.6–9.0% more.
- **Batch testing on Travis.** Execution cuts of 46–50%. Every project with a failure rate below 40% benefits, and there are "no slip-throughs" because failing batches are retested. [A] `beheshtian2022batch`
- **Parallel batching** cuts Chrome test executions by 75% with Batch4. [F] `fallahzadeh2023parallel`
- **Selection vs batching (EMSE 2025, read in full).** Fallahzadeh, Rigby and Adams compare RTS, prioritization and batching on 285 M test results. [R] `fallahzadeh2025contrasting` §4.5, Abstract, p.54
  - BatchAll batches all waiting changes, so the batch size is variable.
  - Selection misses up to 55% of failures; batching misses none under the simulation assumption.
  - Combining selection and batching is left as future work.
- **Risk-aware batching of performance tests (Mozilla, read in full).** [R] `sayedsalehi2026riskaware` §VI–VII, Table IV
  - Fixed-size, time-window and risk-adaptive batches.
  - The "-la" variants flush when a cumulative learned-risk sum passes a threshold.
  - RAPB-la: −32.4% tests, −26.2% maximum time-to-culprit.
  - Only 15 regressing commits in the test split.
- **Google TAP milestones.** Commits are bundled and affected tests run per milestone, typically every 45 minutes. 1.23% of executions find a breakage. The culprit is certain only when no unexecuted outcome lies between pass and fail. [R] `memon2017taming` §I–IV
- **Flake-aware culprit finding.** A Bayesian noisy binary search that can return "no culprit". Plain bisection with reruns plateaus in accuracy while its cost grows linearly. [R] `henderson2023flake` §I–III
- **Culprit ranking at Google.** The culprit is in the top 5 for 82% of failures. [A] `ziftci2017who`
- **Uber.** Changes that each pass alone can break together ("real conflict"): 5% with 2 concurrent changes, 40% with 16. [R per the T5 card, not re-checkable] `ananthanarayanan2019keeping` §2.1–2.2. The PDF copy was removed: it came from a non-author host.
- **Delta debugging** isolates the failure-inducing subset of changes, including interfering ones. It needs monotone, unambiguous and consistent configurations, and untestable subsets give UNRESOLVED. [R] `zeller1999yesterday` §1, §4–5; `zeller2002simplifying` §III
- **Skipping CI.** Rule-based skipping saved a median 21% of build time but still missed failing builds. Skipped changes accumulate into the next build. [F] `jin2021helped`; CI-skip rules [A] `abdalkareem2021ciskip`
- **Impact analysis.**
  - Dynamic impact is safe only for the executions observed. [F] `orso2004empirical` §2.3 (read from a fetched copy; no local PDF)
  - Chianti decomposes a diff into atomic changes and their affected tests. [A] `ren2004chianti`
  - Python call graphs are incomplete. PyCG has 69.9% recall and does not handle eval, getattr or built-in flows [R] `salis2021pycg` Abstract; other limits [F] §III-C. Jarvis [F] `huang2023jarvis`.
- **Precedents in industry and optimization systems** (from W2). Meta runs all tests on master every few hours. SysLLMatic rebuilds and re-measures the final version. [`notes/W2-intake.md`]
- **Gap search G1.** No source sets the interval between full checks from the amount of change accumulated since the last full check. Practitioner blogs mention "after several accumulated changes" and scheduled nightly runs. [searched, not found in research literature; practitioner mentions only]

## 6. Synthesis: what the literature gives us and what it leaves open

1. **Every reduction is only conditionally safe.**
   - For builds, the condition is complete dependencies and deterministic tasks (§1.1).
   - For tests, it is controlled regression testing, deterministic tests, and dependencies observed on the *current* baseline (§2.1–2.2).
   - For benchmarks, it is that performance effects stay local to covered code, that steady state is reached, and that noise is known (§3).
   
   The literature's backstop for all three is a periodic or final full run (§1.3, §3.1 Grambow, §5 TAP and Meta). [R]/[I]
2. **Python is under-served.**
   - Fine-grained Python RTS research is a single 2026 preprint (NameRTS); beyond it there is only the polyglot, file-level BabelRTS and tool papers.
   - Python benchmark selection has no peer-reviewed study.
   - No study covers rebuild correctness for Python extensions.
   
   The existing tools (testmon, Cython dependency tracking, setuptools `build_ext`) rely on coverage.py or on file timestamps (§1.5, §2.3). [R]/[F]/[searched]
3. **Coverage is necessary but not sufficient for performance.** Most tests that cover changed code do not show a known speed-up (Ding), and reduced suites miss trends (Grambow). [R]
4. **Accumulation over many edits is studied only around its edges.**
   - Batching and culprit finding treat a batch of commits as a unit (§5).
   - Drift is named as a failure mode in MongoDB's CI, and change-point detection catches it after the fact (§3.5).
   - Risk-mass batching with threshold flushes exists (Sayedsalehi 2026), but its risk is learned, it covers independent commits, and it has no per-edit reduced check. No source evaluates a model-free trigger on top of a per-edit reduced check for chains of dependent edits.
   
   See `beyond-literature-claims.md`.
