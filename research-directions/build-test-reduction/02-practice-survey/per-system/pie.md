# PIE / pie-perf (Learning Performance-Improving Code Edits)

Status: critic-checked 2026-11-21 (10 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/LearningOpt/pie @ eb3d72bc4f3c9095d0f62506340bc8ca0ef27b09 (local clone: `C:\Users\pc\study\bt-lab\survey\LearningOpt_pie`) · Paper: arXiv 2302.07867 v5 (ICLR 2024), local PDF
Evidence labels: **[src]** read in source (file path + line or paper section quoted/paraphrased), **[inf]** inferred by us from sources, **[unk]** not found (say where you looked).

## 1. What it is
- C++ competitive-programming (CodeNet) slow->fast pairs; LLM proposes a faster program; scored by correctness on all tests plus gem5-simulated runtime. 978 test pairs from 41 problems. [src] paper §2 (dataset), §4 Metrics.
- Evaluation is a Docker-hosted Flask service (`alexshypula/gem5-skylake:api`) driven from `gem5/simulator.py`. [src] gem5/simulator.py:31 (`FROM alexshypula/gem5-skylake:api` in DOCKERFILE_TEMPLATE; class PieEnvironment starts ~l.411) @eb3d72b.

## 2. Build / environment
- "Build" = one `g++` compile of a single `code.cpp`, per candidate: flags `--std=c++17 -O3` (default; paper says GCC 9.3.0). Compile timeout = the per-binary timeout (10 s default). [src] gem5/gem5_api.py:98-99,104,129; gem5/benchmarking.py:53-77; paper §4 Metrics.
- Each candidate is written to a fresh `tempfile.TemporaryDirectory`, compiled from scratch; no incremental build, no compile cache. [src] gem5/gem5_api.py:112-132 (single_submission). [inf] trivially cheap since one file, no dependencies.
- Environment is one prebuilt Docker image pulled once, container reused across all candidates. CPU pinning (queue + `taskset`) is applied only when `timing_env` is `binary`/`both`; with the gem5-only path used by `gem5_eval.py` (`"gem5"`, l.387) `cpu_number` is None, so no pinning. [src] gem5/gem5_api.py:117; gem5/benchmarking.py:66,87,97; gem5/gem5_eval.py:384-387; gem5/README.md (Overview/Usage).
- Compile failure => accuracy 0 for all tests, skip simulation. [src] gem5/benchmarking.py:127-131 (compile error caught, every test gets acc 0).

## 3. Correctness tests per candidate
- Output equality (line by line; floats within 1e-3) vs stored ground-truth outputs, run on the **native g++ binary** for each test input. Per-test timeout 10 s (default); a non-zero exit or timeout scores 0 for that test; accuracy is the fraction of matching lines (zip over lines, divided by ground-truth line count), so a test can score partial credit. [src] gem5/benchmarking.py:33-51, 83-90, 107-147; gem5/gem5_api.py:104.
- Gate: mean accuracy over tests must be >= `gem5_acc_threshold` (default 0.95) or gem5 is skipped; final "correct" requires accuracy == `threshold_accuracy` 1.0. [src] gem5/gem5_api.py:93,135-143 (default 0.95 and gate); gem5/simulator.py:418; gem5/gem5_eval.py:171,461.
- Test set: CodeNet tests (~4 avg) plus AlphaCode LLM-generated tests; after dropping tests that time out in gem5, median 104 tests per test problem (82.5 train, 75 val). "Reject if a single test fails." [src] paper §2 "Test cases".
- Tests are a fixed per-problem list (the dataset row's `tests` column), passed as `testcases` to the service; not selected per edit. [src] gem5/gem5_eval.py:385 (`batch["tests"]`, sorted in reverse; the service API does accept a `testcases` subset, so per-edit selection would be mechanically possible). This is not test selection in our sense: [inf] all tests run for every candidate.
- Early exit: in the gem5 loop, after the first test whose gem5 run errors or times out, remaining tests are skipped (`exit_early_on_fail`, default True). Output correctness is not re-checked in gem5 (it was checked by the native pass). [src] gem5/benchmarking.py:212-246; gem5/simulator.py:429; gem5/gem5_eval.py:374.

## 4. Performance measurement per candidate
- Metric: gem5 `sim_ticks / sim_freq` (simulated seconds) per test, summed over tests as `agg_runtime`; Skylake "Verbatim" config; timeout 120 s per gem5 run in `gem5_eval.py`/`gem5_api.py` (PieEnvironment class default is 60 s). [src] gem5/benchmarking.py:168-169; gem5/simulator.py:235-271,425; gem5/gem5_api.py:105; gem5/gem5_eval.py:374; paper §2 "Performance measurement using gem5".
- No repeats, no statistic, no statistical test: single deterministic run per test (`agg_stdev` is hard-coded 0 for gem5). [src] gem5/simulator.py:271 (`agg_stdev = 0`). Authors note 2-min timeout may add slight variability. [src] paper footnote 2.
- Thresholds: "optimized" = correct and >=10% faster (speedup >= 1.10); speedup floored at 1.0 when slower/incorrect; the script also reports 1.25 ... 10.0. [src] paper §2, §4 Metrics; gem5/gem5_eval.py:176-177,192 (mean_speedup / percent >= each threshold).
- Motivation for simulation: hyperfine on 500 identical program pairs gave mean "speedup" 1.12x (sd 0.36; top 5% >= 1.91x). [src] paper §2 (p.3-4).
- Optional hyperfine path exists (10-500 runs, 5 warm-ups, CPU pinned) but README calls it a prototype. [src] gem5/gem5_api.py:159-173; gem5/README.md:59 (timing_env).
- Order of cost: [inf] compile (~1 s) + N native runs + N gem5 runs; gem5 dominates.

## 5. Cost per candidate (if reported)
- [unk] No per-candidate wall-clock reported. Only: "over 42.8 million simulations" to relabel the dataset; tests that exceeded 2 min in gem5 were excluded (paper §2). Searched paper §2, §4, appendices and gem5/README.md.

## 6. Iteration / cumulative re-validation
- Best@k: sample k candidates (temperature 0.7), take the fastest that passes all tests. No iterative refinement loop in the evaluation. [src] paper §4 "Decoding strategy"; gem5/gem5_eval.py:83-95.
- Self-play data generation exists (training only), not an evaluation of cumulative edits. [src] README.md:77-81. Each candidate is independent; no re-validation of composed edits. [inf]

## 7. Limitations the authors state
- Test cases may not cover all cases: 10 of 120 inspected speedups came from shrinking array-size constants. [src] paper App. A.1 (spurious-speedups paragraph).
- gem5 timeout may introduce slight variability. [src] paper footnote 2.
- Wall-clock CodeNet runtimes were inconsistent (duplicate code, different runtimes). [src] paper App. A.9.

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- Strongest precedent for deterministic measurement: simulated cycles remove repeats and statistics; but full test list still runs per candidate. [src] paper §2; gem5/benchmarking.py:212-246.
- A cheap two-stage pipeline already exists: native-binary correctness gate (0.95 mean, then 1.0) before expensive gem5; failing candidate short-circuits. [src] gem5/gem5_api.py:135-143.
- No build reduction: the build is already trivial (single file); a study of build reduction needs repo-scale systems. [inf]
- Test count is large (median 104) and was only reduced at dataset curation via a timeout filter, which is a form of fixed reduction. [src] paper §2.

## Sources
- gem5/benchmarking.py L25-147, 168-172, 195-250 @ eb3d72b
- gem5/gem5_api.py L98-105, 110-200 @ eb3d72b
- gem5/simulator.py L25-35, 235-271, 411-450 @ eb3d72b
- gem5/gem5_eval.py L83-95, 165-200, 372-395, 455-461 @ eb3d72b
- gem5/README.md, README.md, docs/PIE_experiments_readme.md
- Paper v5 (local PDF, read via pdftotext): §2, §4 Metrics/Decoding, App. A.1 (spurious speedups), A.5, A.9
