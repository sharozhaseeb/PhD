# N3 - Cost breakdown (R1) and stale-binary recheck (H1/C8)

Date of searches: 2026-11-22. Tools: WebSearch (standard mode) and WebFetch. WebFetch answers come from a small summarising model, so every claim from a fetch is labelled [fetch-summary] and is not byte-verified. Search-result snippets are labelled [snippet]. No PDFs were downloaded, so there is no N3-downloads.json. Verdict wording uses "not found in our recorded searches", never "nobody has done this".

Label key: [read-in-source] = full text read by us (none here), [abstract-only], [snippet], [fetch-summary], [unknown].

## 1. Query log

### WebSearch

| # | Query (exact) | Hits |
|---|---|---|
| S1 | Laaber Leitner MSR 2018 evaluation of open-source software microbenchmark suites for continuous performance assessment runtime | 10 |
| S2 | cost of performance testing in continuous integration breakdown build time test time benchmark time empirical study | 10 |
| S3 | Leitner Bezemer ICPE 2017 exploratory study performance testing open source Java projects | 10 |
| S4 | PerfScope Huang performance regression risk prediction commits cost of performance testing motivation | 10 |
| S5 | Ghaleb long CI builds empirical study duration breakdown build test | 10 |
| S6 | LLM code optimization agent evaluation cost benchmark execution time dominates per-candidate verification cost 2025 | 10 |
| S7 | editable install stale compiled extension .so tests pass after failed rebuild meson-python | 17 |
| S8 | setuptools build_ext failure leaves old .so in place develop mode stale extension imported | 19 |
| S9 | meson-python editable install rebuild on import failure behavior ImportError build failed | 18 |
| S10 | scikit-build-core editable redirect rebuild on import failure stale | 17 |
| S11 | incremental build correctness empirical study stale artifacts false pass tests build system "under-specified dependencies" Licker Rice | 10 |
| S12 | Cython stale extension module not rebuilt old .so tests pass pyx changed pip install -e | 17 |
| S13 | Daly Brown "Creating a virtuous cycle in performance testing at MongoDB" ICPE 2021 time to run performance tests | 10 |
| S14 | asv benchmark suite takes hours to run full pandas numpy benchmarks CI runtime documentation | 18 |
| S15 | Gallaba build failures CI time spent breakdown build vs test phases Travis job log analysis | 17 |
| S16 | SWE-Perf benchmark evaluation time per instance hours runtime measurement cost arXiv 2507.12415 | 9 |
| S17 | LLM performance optimization agent "evaluation cost" benchmark execution wall-clock bottleneck iterative profiling feedback loop 2026 | 10 |
| S18 | SWE-bench agent trajectory stale compiled extension tests pass without rebuilding C extension false resolved harness | 16 |
| S19 | empirical study Python C extension build systems incremental rebuild correctness setuptools Cython bugs | 10 |
| S20 | Does Using Bazel Help Speed Up Continuous Integration Builds incremental correctness stale | 10 |

### WebFetch

| # | URL | Result |
|---|---|---|
| F1 | https://mesonbuild.com/meson-python/how-to-guides/editable-installs.html | OK |
| F2 | https://scikit-build-core.readthedocs.io/en/stable/configuration/editable.html | OK |
| F3 | https://sources.debian.org/data/main/m/meson-python/0.19.0-1/mesonpy/__init__.py | 404 |
| F4 | https://arxiv.org/pdf/2212.09515.pdf | timeout (300 s) |
| F5 | https://raw.githubusercontent.com/mesonbuild/meson-python/main/mesonpy/_editable.py | OK |
| F6 | https://raw.githubusercontent.com/scikit-build/scikit-build-core/main/src/scikit_build_core/resources/_editable_redirect.py | OK |
| F7 | https://arxiv.org/abs/2212.09515 | OK, abstract only |
| F8 | https://github.com/pandas-dev/pandas/issues/23412 | OK |
| F9 | https://arxiv.org/html/2404.13295v2 | OK |

Not searched or not opened: the full text of Laaber and Leitner MSR 2018, Leitner and Bezemer ICPE 2017, PerfScope, Daly, Ghaleb, Gallaba, SWE-Perf, GSO, Codeflash docs, and the Hu and Zhang / 2608.29851 Python-C bug studies. For these we only have snippets, so any figure from them is unverified.

## 2. Finding R1 - per-candidate cost split (build vs tests vs benchmarks)

### 2a. Summary of the W2 per-system notes (not re-researched)

Source: `02-practice-survey/per-system/*.md`, section "Cost per candidate".

- Almost every system reports no per-candidate wall-clock split: ECCO, COFFE, PIE, EffiBench, EffiBench-X, Mercury, SemOpt, CodeEvolve, SWE-Opt, perf-bench-reliability, SWE-Perf, GSO, KernelBench and the SWE-bench harness are all [unk] or give structure only.
- Structure-only inferences (ours, not reported by the authors):
  - SWE-Perf: 2 x (install + 3 warm-ups + 20 repeats), with an 1800 s eval timeout.
  - GSO: at least 2 installs, plus N tests x 5 repeats for each of base, patch and reference.
  - SWE-fficiency: 4 perf.sh runs, one covering-test run (median 7,723 tests) and 5 installs, with a 7200 s timeout.
  - Codeflash: each candidate gets a behaviour pass plus a perf pass of up to 10 s of looping.
- Reported numbers, none of them a split:
  - AlphaEvolve: about 100 compute-hours per solution on expensive tasks.
  - EvalPerf: about 15 min per whole model.
  - PerfAgent: $2.88 to $4.25 average agent cost per task.
  - FormulaCode: $446 for environment synthesis; average 38 min per agent task.
  - COFFE: at most about 1 min per test case.
- Only one system reports a build-and-test cost: SysLLMatic reports end-to-end time per application including build and test (11 to 206 min). The authors say build and test overhead "can dominate". [src paper §7.5.1, Table 12, per W2]. That is the opposite of R1 (it is a Java setup with no benchmark split) and shows the split is setup-dependent.
- asv/numpy/scipy/pandas: cost "not reported in the repos [unk]". Structure is one wheel build per commit plus selected benchmarks x rounds x repeats. CI smoke runs use `--python=same --quick`.
- pyperformance: about 21 process launches per benchmark, estimated tens of minutes to hours per interpreter [inf, no figures in the repo].
- Industrial CI test selection (Meta, Google): reports execution counts and infrastructure cost, not a build/test/benchmark split.

### 2b. Fresh searches

Results by claim:

1. Benchmark suite runtimes are long.
   - Laaber and Leitner MSR 2018: ten Java and Go projects, suites of 16 to 983 benchmarks, runtimes 11 min to 8.75 h [snippet from the Chalmers listing; abstract-only, full text not read]. This gives absolute suite runtime, not a split against build or tests.
   - An arXiv paper (2212.09515, title not confirmed by us) states "extensive benchmarking studies usually take several hours" [abstract-only, F7].
   - pandas asv: in issue #23412 a maintainer wrote that 2,618 benchmarks "theoretically should take 45min, maybe double on Windows" and that this excludes setup [fetch-summary F8]. This is a theoretical estimate, not a measurement. The same issue's "6.5 h on a laptop" figure refers to the pytest test suite, not asv. An earlier search summary (S14) conflated the two and also quoted "about 2 hours" for pandas from an unspecified source; we did not verify that.
   - scikit-image / Quansight: asv suite up to about 2 h in CI with relative comparison [snippet only, S14].
2. Performance testing is described as costly.
   - PerfScope (ICSE 2014, Huang et al.): cost motivation (test 14-24% of commits to catch 87-95% of regressions) [snippet from the project page, S4]. Cost is stated qualitatively; no build/test split was seen.
   - Leitner and Bezemer ICPE 2017: 111 Java projects; performance tests are a small part of the suite and rarely updated [snippet S3]. It is about practice, not cost. We saw no timing data.
   - Ding et al. ICSE 2020 and the 2022 CI microbenchmark paper: "performance testing is expensive" statements [snippet S2]. No build/test/benchmark split seen.
   - Daly (MongoDB, ICPE 2021): no run-time split found in snippets [S13]; the paper was not opened.
3. CI build duration studies.
   - Ghaleb et al. (EMSE 2019): 104,442 builds from 67 projects; factors for long durations include test factors [snippet S5]. We did not see a phase-level build vs test vs benchmark breakdown. Performance benchmarks are not the subject.
   - Gallaba (TSE 2020 / ICSE 2022) and Beller (MSR 2017): failure causes and termination reasons, not time splits [snippet S15].
   - Zheng et al. (Bazel, arXiv 2405.00796): speedups from parallel and incremental builds, build-time centred [snippet S20].
4. LLM optimization agents 2025-2026.
   - S6, S17 found cost discussion for InferenceBench (API spend vs GPU time) and general eval-cost essays [snippets]. None gives a per-candidate build vs tests vs benchmark split for code-optimization agents.
   - SWE-Perf (2507.12415): a third-party summary mentions 1 CPU core and an average of 83.9 min per codebase for scikit-learn tests [snippet, unverified, not from the paper].
   - GSO, SWE-fficiency, PerfAgent, SemOpt, ECCO, EffiBench and PIE were not re-searched here. W2 found no split for them.

### 2c. Closest works for R1

| Work | What it gives | Why it falls short |
|---|---|---|
| Laaber and Leitner MSR 2018 | Suite runtimes 11 min to 8.75 h [abstract-only] | No build/test comparison; microbenchmark suites in Java/Go |
| SysLLMatic (W2 note) | End-to-end time incl. build and test per app; "build and test can dominate" | Java, no benchmark split |
| asv structure in W2 note | Per commit: build, then benchmarks x rounds x repeats | Structure only; no figures |
| pandas issue #23412 [fetch-summary] | 45 min theoretical for 2,618 benchmarks, excl. setup | Estimate; not a split |
| PerfScope / PerfRanker | Cost motivates prioritising commits | Qualitative |

### 2d. Verdict R1

**Partial.** The claims that performance suites are long and costly are well supported in the literature: Laaber and Leitner 2018 reports 11 min to 8.75 h suites, and PerfScope, Ding and the CI-microbenchmark paper call performance testing expensive. A published per-candidate (or per-commit) split of build vs tests vs benchmarks, with the finding that most benchmark time is per-process setup outside timing loops, was not found in our recorded searches (20 searches plus W2 notes on 30 systems).

Caveat: we did not read Laaber, Daly, Ghaleb or Gallaba in full, so a table inside one of them could contain a split we missed.

Safe wording: "Prior work reports that performance-test suites run from minutes to hours (Laaber and Leitner 2018, [abstract-only]) and calls them costly, but in our recorded searches we found no per-candidate breakdown of build, test and benchmark time for LLM code-optimization loops; we measure one on networkx (benchmarks about 8-28x build plus serial tests, one project)."

Also keep: the networkx numbers are a single-project measurement; the setup-outside-timing-loops mechanism is our own observation and is not backed by any source above.

## 3. Finding H1/C8 - stale extension binaries and false test passes

### 3a. What the docs and code say about rebuild failure

- meson-python docs [fetch-summary F1]:
  - Editable installs rebuild "when the package is imported the first time in a given Python interpreter instance".
  - The docs name build-isolation failures ("fail to rebuild when imported" unless build deps are installed).
  - The docs do not say what happens on a failed rebuild, and say nothing about stale artifacts.
  - `MESONPY_EDITABLE_VERBOSE` shows the build output.
- meson-python source `_editable.py` [fetch-summary F5]:
  - The rebuild is `subprocess.run(..., check=True)`.
  - On `CalledProcessError` it raises `ImportError('rebuilding the "<name>" editable package failed')`, with the log from the first `FAILED:` line attached when not in verbose mode.
  - So with meson-python editable installs a failed rebuild is meant to fail the import loudly rather than fall back to the old `.so`.
  - The fetch summary also says the file contains no code that deletes the old extension, so whether the old `.so` stays on disk depends on ninja, not shown there.
- scikit-build-core docs [fetch-summary F2]:
  - Rebuild-on-import is `editable.rebuild` and experimental.
  - The docs do not describe a failed rebuild.
  - The docs say the persistent install tree is wiped before rebuild so stale artifacts do not linger (from the S10 snippet; F2 summary did not repeat it, so treat as [snippet]).
  - A rebuild after import takes effect only in a new process.
- scikit-build-core source `_editable_redirect.py` [fetch-summary F6]:
  - `run_checked` raises on a nonzero exit, so the import fails.
  - If `rebuild` is not enabled, no build runs and stale files are used without warning.
- setuptools `build_ext --inplace` [snippet S8, our reading of the code, not stated by a source]: the copy into the source tree happens after the build, so a failed build leaves any existing in-tree `.so` untouched. Not verified by us against current setuptools.

Net: the two modern backends we checked (meson-python, scikit-build-core with rebuild enabled) raise on failed rebuild. The stale-binary-passes path exists for classic setuptools `build_ext --inplace` / develop-style workflows and for any setup with no rebuild step (our bottleneck replay used an incremental tree, which matches this path). We did not test this ourselves in N3.

### 3b. Literature on stale artifacts and false passes

- Licker and Rice, "Detecting Incorrect Build Rules" (ICSE 2019, build fuzzing) [snippet S11]: incorrect incremental builds, e.g. executables linked against stale objects; C/C++ with Make.
- Bezemer et al., EMSE 2017, unspecified dependencies in make-based builds (glib, openldap, Linux, Qt) [snippet S11]: C/Make.
- EChecker (arXiv 2404.13295) [fetch-summary F9]: missing and redundant dependencies in incremental builds, C/C++ with GNU Make and CMake; 12 projects, 240 commits. The abstract does not link build errors to false test passes. "Python" in that paper is CPython itself (a Make project), not a Python extension build.
- "Identifying Bugs in Make and JVM-Oriented Builds" (arXiv 2005.06881) [snippet S11]: stale artifacts can cause runtime errors or wrong build outputs. This is the closest to "stale artifacts harm reliability", with no link to test false passes seen.
- Zheng et al. (Bazel CI, arXiv 2405.00796) [snippet S20]: evaluates speed only; the authors say correctness is future work.
- Empirical study of bugs in build systems (Tamrawi et al.-type, SMU listing, 800 bug reports; Ant, Maven, CMake, QMake) [snippet S19]. Not Python-extension-specific.
- Python native-code bug studies (arXiv 2608.29851, Hu and Zhang) [snippet S19]: bugs in Python/C code, not build-staleness.
- Python ecosystem anecdotes (setuptools issue about `.pyx` edits skipping the Cython step, Cython timestamp issue where changing only C files leaves cythonize "up to date", `.so` shadowing `.pyx`) [snippet S12, S19]: mailing-list or issue-tracker reports, not studies.
- SWE-bench-style harness literature [snippet S18]: weak tests and environment effects on SWE-bench; nothing about stale compiled extensions.

### 3c. Closest works for H1/C8

| Work | Relevance | Gap |
|---|---|---|
| Licker and Rice; Bezemer 2017; EChecker | Incremental builds can be incorrect via missing dependencies | C/C++/Make; no Python extension, no test-pass outcome |
| meson-python and scikit-build-core docs and code | Define rebuild-on-import and failure behaviour | Design behaviour, not empirical; no replay study |
| setuptools/Cython issue threads | Anecdotal stale `.so` and skipped rebuilds | Not a study |

### 3d. Verdict C8

**Partial for the general topic; not found for the specific claim.** Studies of incremental-build correctness exist (Licker and Rice, Bezemer 2017, EChecker), but they target C/C++ Make/CMake. In our 6 stale-binary-focused searches (S7-S12) plus S19 and S20, we did not find an empirical study of incremental-rebuild correctness for Python extension modules, nor a study measuring that a non-compiling state passes tests against a stale `.so`. Documentation and source for meson-python and scikit-build-core indicate a failed rebuild-on-import raises, so the false pass is specific to workflows without such a rebuild gate (setuptools in-place, replay of commits into a kept tree).

Caveat: we did not search conference proceedings by hand, or the Python packaging discourse threads in depth; F5/F6 are summariser outputs.

Safe wording for C8 (use instead of "no empirical study"): "In our recorded searches we found studies of incremental-build correctness for C/C++ build systems (e.g. Licker and Rice; EChecker) but none for Python extension modules; documentation and source for meson-python and scikit-build-core show rebuild-on-import failing with an error, so the stale-binary false pass we saw needs an in-place setuptools-style or replayed tree."

### 3e. Verdict H1 (the single bottleneck event)

Consistent with our "replay artefact, not a natural-edit event" label: a prerequisite commit was missing, so the replayed state was not a state any developer committed, and the stale parent `.so` made 191/191 pass. Nothing found contradicts that label, and nothing found cites a natural occurrence. We still recommend that the harness verify a clean build (or at least check that the extension build succeeded) before trusting test passes on compiled-extension projects.

Safe wording: "On bottleneck, one replayed state did not compile yet passed 191/191 tests because the incremental tree retained the parent's compiled extensions; the clean build failed with 8 collection errors. We attribute this to a missing prerequisite commit in the replay, and we treat it as evidence that incremental tests need a build-success gate, not as a natural-edit rate."

## 4. Open items

- Read Laaber and Leitner MSR 2018, Daly ICPE 2021 and Ghaleb EMSE 2019 in full for any build/test/benchmark time table (not read here).
- Verify setuptools in-place behaviour by experiment if C8 wording will be defended in the paper.
- No PDFs were downloaded, so there is no N3-downloads.json.
