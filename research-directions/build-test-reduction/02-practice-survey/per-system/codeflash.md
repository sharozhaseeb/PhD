# Codeflash

Status: critic-checked 2026-11-21 (9 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/codeflash-ai/codeflash @ a3a38efc9ec3d0a52a23056fd0a069863398a7ce (local clone: `C:\Users\pc\study\bt-lab\survey\codeflash-ai_codeflash`) · Paper: none (source-available tool, BSL-1.1 per README line 84; LICENSE says it "is not an Open Source license" until the change date to MIT)
Evidence labels: **[src]** read in source (file path + line or paper section quoted/paraphrased), **[inf]** inferred by us from sources, **[unk]** not found (say where you looked).
Paths below are relative to `codeflash/` in the clone, all @ a3a38ef (bare `optimizer.py` = `optimization/optimizer.py`; `function_optimizer.py` = `languages/function_optimizer.py`; architect spot-checked `result/critic.py` 94 and `models/models.py` 989-999). Source was only read, never run.

## 1. What it is (2–3 lines)
LLM-based optimizer for Python (also JS/TS, Java, Go paths exist) that works one function at a time. For each target function it asks a hosted AI service for candidate rewrites, runs the project's existing tests plus LLM-generated tests on the original and on each candidate, and keeps the fastest candidate that behaves the same. [src] `languages/function_optimizer.py` 771–881 (`optimize_function`), 1318–1433 (`determine_best_candidate`).
Candidate generation, test generation, refinement and repair are remote API calls. [src] `function_optimizer.py` 792–799, 1349–1365, 1281–1302, 2918–2966. The server side is not in the repo. [unk]

## 2. Build / environment
- No build step per candidate. A candidate is a source-text swap of the function (and its helpers) in the working tree, followed by a pytest subprocess. [src] `function_optimizer.py` 1187–1191 (`replace_function_and_helpers_with_optimized_code`), 3002–3009, 3043–3051; `languages/python/support.py` 1155–1160, 1202–1207.
- grep over the package for `pip install`, `build_ext`, `maturin`, `cythonize`, `setup.py` found no rebuild of the target project. [src] absence in `codeflash/**/*.py`. So C extensions of the target are not rebuilt; edits are Python-source only. [inf]
- The environment is the user's own existing venv/project. Nothing is imaged or cached per candidate. [inf]
- The tree is NOT reset to the original between candidates. Each candidate is applied in place by `replace_function_definitions_in_module` over whatever is currently in the file (the previous candidate's function body), and the file is rewritten with the un-instrumented candidate after each test run. The original source is restored once, in a `finally` after the whole candidate loop. [src] `function_optimizer.py` 1187–1191, 3010–3013, 3052–3057, 1409–1412; `languages/python/function_optimizer.py` 198–219. (Researcher claimed per-candidate restore; wrong. Whether leftover helper edits from one candidate can leak into the next is not shown. [unk])
- Optional git worktree mode (`--worktree`) copies the repo so edits happen outside the main checkout. [src] `optimization/optimizer.py` 19–24, 522–523; `code_utils/git_worktree_utils.py` 50–60.
- Test files are instrumented once per function (a `__perfinstrumented` behaviour copy and a `__perfonlyinstrumented` perf copy), not per candidate. [src] `function_optimizer.py` 1691–1739.

## 3. Correctness tests per candidate
- **Existing tests, found per target function.** Test files are scanned with `ast` for imports of the target, then Jedi resolves which test functions call it. This builds a map `function -> tests that call it`. [src] `discovery/discover_unit_tests.py` 532–590 (import filter), 859–1118 (`process_test_files`, Jedi), 610–676 (`discover_tests_for_language`); `optimization/optimizer.py` 287–301.
  - Test collection itself is a `pytest --collect-only`-style pass pickled to a file before the import filter and Jedi resolution. [src] `discover_unit_tests.py` 711–765 (`discover_tests_pytest`).
  - Discovery runs once per run. It is keyed on the function, not on the candidate edit. [src] `optimizer.py` 601, 669–671.
- **Replay tests.** A tracer records real calls (args and return values) and generates `__replay_test` files. They are treated as test type REPLAY_TEST. [src] `tracing/replay_test.py` 46–162; `discover_unit_tests.py` 774, 818, 659.
- **Generated regression tests.** `N_GENERATED_TESTS` is 2 at every effort level. Concolic coverage tests exist as another type. [src] `code_utils/config_consts.py` 78; `verification/equivalence.py` 86–90.
- **What runs per candidate.** The same fixed set every time, for that one function: all instrumented existing + replay + generated test files. The behaviour run is one loop. [src] `languages/python/support.py` 1086–1107; `function_optimizer.py` 3002–3009. Replay tests are run as individual `file::function` ids, other files as whole files. [src] `support.py` 1088–1097.
- **Equivalence check.** Baseline and candidate behaviour results are compared test by test. For Python: [src] `languages/python/function_optimizer.py` 188–196, `verification/equivalence.py` 30–149.
  - invocations present in only one side are skipped, not failed: candidate-only (48–49), original-only or missing (57–58) and a missing `INIT_STATE_HELPER` record (51–56). Empty results on either side count as not equal (34–35). [src]
  - pass/fail of each test must match (86–103);
  - return value via `comparator` (105–119);
  - captured stdout via `comparator` (132–144);
  - timed-out originals are skipped, and if all timed out the result is "not equal" (59–61, 147–148).
  - The base-class hook compares pass/fail only (`pass_fail_only=True`); Go and JS also use that. The Python override (above) is the only path that compares return values and stdout. [src] `function_optimizer.py` 580–588; `golang/function_optimizer.py` 57; `javascript/function_optimizer.py` 158.
  - The comparison covers return values and stdout, plus object state via `INIT_STATE_*` verification types. [src] `equivalence.py` 63–67, 51–56. Arbitrary side effects (files, global state) are not compared. [inf]
- **Test-count and coverage gates (baseline and candidate).** `MIN_TESTCASE_PASSED_THRESHOLD = 6` passing tests are needed, or at least 1 passing replay test. Original-code coverage must be `>= COVERAGE_THRESHOLD = 60.0`. [src] `config_consts.py` 22–23; `result/critic.py` 192–210; `function_optimizer.py` 2794–2820, 1229–1237 (candidate gate in `process_single_candidate`: `speedup_critic` and `quantity_of_tests_critic`, the latter applied to the candidate's behaviour results), 1968–1969 (baseline: `quantity_of_tests_critic` and, if `should_check_coverage()`, `coverage_critic`).
- **Determinism controls.** `PYTHONHASHSEED=0`; `random.seed(42)` and numpy seed 42; `time` and `perf_counter` mocked inside the pytest plugin. [src] `function_optimizer.py` 3256–3270; `verification/pytest_plugin.py` 115–133, 164, 169, 187.
- **Is this test selection?** Selection is per function, fixed at discovery. It is not per edit. Every candidate for a function re-runs the same files. [src] `function_optimizer.py` 1925–1935, 3002–3009. There is no diff-aware or coverage-aware narrowing between candidates. [inf] Within a function, `quantity_of_tests_critic` only counts tests; it does not choose them.

## 4. Performance measurement per candidate
- **Workload** = the same instrumented tests, in the "performance" copy. Existing, replay and generated tests all count. [src] `support.py` 1184 (`benchmarking_file_path`).
- **Loops and time budget.** Perf run is a pytest session with `--codeflash_min_loops=min_loops`, `--codeflash_max_loops=max_loops`, `--codeflash_seconds=10`, `--codeflash_stability_check=true`. Defaults are `pytest_min_loops=5`, `pytest_max_loops=250`. `TOTAL_LOOPING_TIME` = 10 s (env `CODEFLASH_LOOPING_TIME`). [src] `support.py` 1185–1193; `function_optimizer.py` 3115–3116 (Python defaults; 3159 is the JS call); `config_consts.py` 21. In subagent mode the loop bounds are 3 and 100. [src] `function_optimizer.py` 2847, 3050.
- **Early stop (stability).** Stop once the last 35% window of per-loop runtimes is within +-0.25% of the median and its spread is <= 0.25%. [src] `pytest_plugin.py` 312–345; `config_consts.py` 30–32.
- **Statistic.** For each test case: min over loops of its runtime. Then the sum over test cases. Called "summed runtime". Only passed tests count. [src] `models/models.py` 970–999 (`total_passed_runtime`, `min(...)` at 998).
- **Speed-up definition.** `(orig - opt) / opt`. A value of 0.05 is about 1.05x. [src] `result/critic.py` 27–34.
- **Threshold.** `MIN_IMPROVEMENT_THRESHOLD = 0.05`. Noise floor = 0.05, or 0.15 when original summed runtime < 10,000 ns. Doubled when `env_utils.is_ci()` (GitHub Actions). Accept needs gain > floor and runtime < best so far. [src] `config_consts.py` 15; `critic.py` 94–101, 104. The docstring says "2x" but code uses `3 *`. [src] `critic.py` 81 vs 94.
- **Extra criteria for async code.** Throughput gain > 10% or concurrency-ratio gain > 20% can also accept. [src] `config_consts.py` 16–17; `critic.py` 109–136.
- **Noise controls found.** `gc.disable()` around the timed call (async wrapper at line 84; sync wrappers at 150 and 187); fixed hash seed; the stability window; the higher floor in CI. [src] `code_utils/codeflash_wrap_decorator.py` 84; `critic.py` 95–96. No CPU pinning, affinity or cgroups. [src] grep for `taskset`, `sched_setaffinity`, `isolcpus` over `codeflash/**/*.py` returned nothing. Baseline and candidates are run back to back on the same machine, not interleaved. [inf]
- **Per-candidate order.** Behaviour tests first. If they do not match, the candidate is dropped (maybe sent to repair) and perf is not run. [src] `function_optimizer.py` 3022–3033.

## 5. Cost per candidate (if reported)
- Wall-clock: each candidate runs a behaviour pass plus a perf pass of up to 10 s of looping, plus a line-profiler pass if it was accepted. [src] `function_optimizer.py` 3002–3051, 980–983. The perf budget is per candidate, not split among tests. [inf]
- Number of candidates per function: 3 / 5 / 6 optimizer candidates plus 4 / 6 / 7 line-profiler candidates (low / medium / high). Medium is escalated to high for the top 15 ranked functions. Refinement, repair and adaptive rounds add more. [src] `config_consts.py` 75–76, 54, 91, 80; `optimizer.py` 654–656.
- No dollar or token cost reported in the repo. [unk] (searched `codeflash/**/*.py`; the LLM calls are server-side).

## 6. Iteration / cumulative re-validation
- Within one function: first-pass candidates, then refinement of the top valid ones, repair of failing ones (up to 2/3/5 per function), and adaptive rounds (high effort only). Each new candidate gets the full behaviour + perf cycle against the original baseline. [src] `config_consts.py` 69, 80, 89–97; `function_optimizer.py` 1384–1405, 1262–1303, 2918–2966.
- Best selection is across the valid candidates by runtime, refinement and diff rank. [src] `function_optimizer.py` 1022–1101; `config_consts.py` 35.
- **Across functions: no cumulative re-validation found.** Each function is optimized and checked on its own. The accepted edit is reverted right after the PR is raised only when `raise_pr` and (`--all`, a PR number in env, `--replay-test`, or `--file` without `--function`), or when staging review is on; `--worktree` returns before any revert; in the remaining case (e.g. a single named function) no revert branch is taken here and the accepted edit presumably stays in the tree. [src] `function_optimizer.py` 2709–2725; `optimizer.py` 634–684. [inf] for the last case.
- In `--worktree` mode the accepted edit is kept and a snapshot commit is made before the next function. A diff patch is saved per function. [src] `function_optimizer.py` 2709–2711; `optimizer.py` 692–706. The next function then gets its own baseline on the already-modified tree. [src] `establish_original_code_baseline` 2740–2751 [inf: baseline therefore includes earlier accepted edits]. No full-suite or combined run of all accepted edits at the end was found. [src] absence; `optimizer.py` 716–720 only logs the patch list.
- Whole-project suite is not run before a PR is opened. The only tests run are the discovered function-level tests plus generated ones. [inf] from `function_optimizer.py` 1925–1935, 3002–3009.

## 7. Limitations the authors state
- No paper. Code comments state two known weaknesses: `total_passed_runtime` "doesn't look at the intersection of tests of baseline and original" (TODO) and it "doesn't handle the loop index". [src] `models/models.py` 996; `function_optimizer.py` 2863.
- Stability thresholds are labelled "experimental" and "strict". [src] `config_consts.py` 28–29.
- Docs / marketing claims on correctness are not read. [unk]

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- Closest existing thing to per-target test selection: tests are chosen per function via an import filter and Jedi call resolution. [src] `discover_unit_tests.py` 532–590, 859–1118. It is static and computed once. It is not re-selected per edit and does not use coverage of the edit. [inf]
- Test selection per candidate is therefore fixed. Every candidate re-runs the full function-level set and a 10 s timing loop, so cost per candidate is high and constant. [src] `function_optimizer.py` 3002–3051. A deterministic reduced benchmark (fewer loops, a cheaper metric) would target this. [inf]
- Speed-up uses sum of per-test minimums with a 5% floor and a stability stop. It is noisy-by-design, with no instruction counting or CPU isolation. [src] `models.py` 998; `critic.py` 94; `pytest_plugin.py` 312–345. [inf]
- Build reduction is not applicable: nothing is rebuilt, because edits are in pure-Python source. Compiled-language targets are out of scope for the Python path. [inf]
- Cumulative re-validation of several accepted edits is absent. Only worktree mode stacks them, with no combined check. [src] `optimizer.py` 692–706. This is a gap Study 1 could fill.

## Sources
- Files read (path @ a3a38ef):
  - `code_utils/config_consts.py` 1–116
  - `result/critic.py` 1–211
  - `verification/equivalence.py` 1–150
  - `verification/pytest_plugin.py` 225–254, 312–345 (grep for 92–187, 421–524)
  - `models/models.py` 970–1015
  - `languages/function_optimizer.py` 565–605, 771–1020, 1129–1433, 1652–1741, 1925–1960, 2349–2463, 2695–2911, 2918–3079, 3106–3290
  - `languages/python/function_optimizer.py` 185–210
  - `languages/python/support.py` 1070–1251
  - `optimization/optimizer.py` 625–748 (grep for 19–301, 522–601)
  - `discovery/discover_unit_tests.py` 532–590 (grep for the rest)
  - `code_utils/codeflash_wrap_decorator.py` 75–119
  - `code_utils/git_worktree_utils.py` 1–60
  - `tracing/replay_test.py` (grep)
- Not read: `verification/comparator.py` internals, `codeflash_capture.py`, the server-side service, docs site.
- README license line (BSL-1.1) via https://github.com/codeflash-ai/codeflash.
