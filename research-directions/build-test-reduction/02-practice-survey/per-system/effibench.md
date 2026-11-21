# EffiBench

Status: critic-checked 2026-11-21 (7 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/huangd1999/EffiBench @ d29e43bccdfa6a9ba9e76c10d79e4b57aaa4a154 (local clone: `C:\Users\pc\study\bt-lab\survey\huangd1999_EffiBench`) · Paper: arXiv 2402.02037 (PDF read via pdftotext)
Evidence labels: **[src]** read in source (file path + line or paper section quoted/paraphrased), **[inf]** inferred by us from sources, **[unk]** not found (say where you looked).

## 1. What it is
- 1,000 LeetCode problems (Python); an LLM writes a `class Solution`; the harness checks it with generated asserts and measures time and memory against the canonical solution. Generation-only (no edit/optimisation task). [src] paper §3, Table 1; src/code_efficiency_calculator.py:77-101 @d29e43b.
- Note: `dataset.jsonl`, `data/dataset.json` are Git-LFS pointers in the clone; `results/gpt-3.5-turbo.json` is real (1000 rows) and was inspected. [src] dataset.jsonl:1-3; results/gpt-3.5-turbo.json.

## 2. Build / environment
- No build. Each candidate is written to a single `.py` file: import prelude + ListNode/TreeNode stubs + completion + `solution=Solution()` + the test asserts. [src] src/code_efficiency_calculator.py:9-51, 94-97.
- Environment: `python:3.11.2` Docker image with `pip install -r requirements.txt`; no per-candidate environment, files run directly with `mprof`. [src] Dockerfile:1-11 (comments are in Chinese). A public HF server/leaderboard also exists. [src] paper §1.
- Host: Xeon Platinum 8336C, 128 cores, "timeout 10 s". [src] paper §5. The repo passes `max_execution_time=5`. [src] src/code_efficiency_calculator.py:53,66. [inf] paper and code disagree (10 s vs 5 s).

## 3. Correctness tests per candidate
- Tests are Python `assert` lines appended to the candidate file; one process runs all of them (about 100 per problem, 984/1000 rows contain `assert`; mean 100 lines). [src] results/gpt-3.5-turbo.json (`test_case` field, counted by us); paper §3.3 ("100 tests within EffiBench").
- Tests were produced by a GPT-3.5-turbo-written test-case generator per problem (`test_case_generator` field), varying input sizes and edge cases; users may regenerate 10 or 1,000 tests. [src] paper §3.3; results/gpt-3.5-turbo.json keys.
- `small_test_cases` (the LeetCode examples) are used only if `evaluation_code=True`; default False. [src] src/code_efficiency_calculator.py:77-81, 66.
- Pass/fail is implicit: a `.dat` memory profile is kept only if the script reports no stderr; otherwise the `.dat` is deleted and the problem drops out of aggregates. [src] scripts/run_code.sh:39,46-48 (rm .dat if exit_status!=0 or stderr file non-empty); src/report_overhead.py:75-83; "pass" = has a .dat for both candidate and canonical, `pass1 = len(list)/1000*100`, report_overhead.py:110-112,143.
- Quirk: `exit_status=$?` is read after two assignments, so it reflects the assignment (always 0), not `timeout`/`mprof`. Failure detection effectively relies on non-empty stderr. [src] scripts/run_code.sh:39-42 (`exit_status=$?` on l.42 follows the arithmetic assignment on l.41); check at l.46. [inf] a silent non-zero exit or timeout with empty stderr may be counted as passing with a truncated profile; not tested by us.
- Paper: efficiency is computed only on code that "can pass all test cases". [src] paper §5 ("can pass all test cases", l.428 of pdftotext).
- Test selection: [inf] none; one fixed set per problem, all asserts in one process.

## 4. Performance measurement per candidate
- Tool: `mprof run --interval 0.001` (memory_profiler) wrapped in `timeout`; wall time derived from first/last profile timestamps, memory from the .dat series. [src] scripts/run_code.sh:39 (`timeout $max mprof run --interval 0.001`); src/report_overhead.py:25-37.
- Runtime = max timestamp - min timestamp of the profile for the single run of the whole test file (all tests together). [src] src/report_overhead.py:25-37. [inf] includes interpreter startup/profiler overhead and the import prelude.
- Metrics: ET, NET (candidate / canonical), max memory (MU/NMU), total memory (area under memory-time, MB*s; TMU/NTMU). [src] paper §3.4; src/report_overhead.py:6-23, 121-141.
- Repeats: none (one run per candidate and per canonical). Statistic: the script reports NET as a ratio of sums (total candidate time / total canonical time), whereas the paper defines NET as the mean of per-problem ratios; per-problem ratios are computed (l.121-122) but not printed. No statistical test, no speedup threshold. [src] src/report_overhead.py:121-122,136-145; paper §3.4. [unk] repeat count in paper: searched §3.4, §5, App. for "repeat/runs"; only a cross-environment ranking test (p-value>>0.05, Kruskal-Wallis H, Table 26) is reported. [src] paper §5.
- Noise controls: same machine for all models; 128-core server with no stated pinning; [unk] CPU isolation/pinning (grep of repo scripts finds none). Threads run candidates in parallel via `ThreadPoolExecutor` (default workers), so concurrent runs share the machine. [src] src/code_efficiency_calculator.py:64-67. [inf] this adds timing noise.

## 5. Cost per candidate (if reported)
- [unk] Not reported. Searched paper §5 and App. for "time per"/"hours"; the 10 s (paper) or 5 s (code) per-candidate cap is the only bound. 

## 6. Iteration / cumulative re-validation
- None in the repo: single-shot generation, one evaluation. [src] src/closed_source_model_completion.py:16-72 (single completion call per problem). [inf]

## 7. Limitations the authors state
- Python-only; LeetCode algorithmic problems only; results depend on hardware/software environment and need standardised environments (leaderboard server). [src] paper Appendix A.1 "Limitations".
- Normalised metrics reported per task; different LLMs correct on different problem subsets, so a common-subset analysis (210 problems) is given. [src] paper §5.2.

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- Counter-example for reduction: all ~100 generated tests execute in one process and the same run is the performance measurement, so correctness and speed are coupled and not separable. [src] src/code_efficiency_calculator.py:94; src/report_overhead.py:25-37.
- Paper shows sensitivity to test count (10 vs 100 vs 1,000 tests in Table 24; NET rises with more tests) and environment; the stable-rankings claim is about environments (Table 26), so it only weakly supports using fewer tests. [src] paper §3.3, §5. Table 24 (GPT-3.5-turbo-0301; paper App. A.14): NET 2.36 / 3.18 / 3.95 and ET 0.27 / 0.39 / 0.56 s for 10 / 100 / 1,000 tests, so absolute scores are NOT stable in test count (only rankings are claimed stable). [src] paper A.14, Table 24.
- Timing is not deterministic (wall clock via sampling profiler, concurrent threads, single run). [inf]
- Heavy per-candidate overhead is avoided because no build exists; reduction target is the test list, not the build. [inf]

## Sources
- src/code_efficiency_calculator.py L1-123, src/report_overhead.py L1-145, scripts/run_code.sh L1-47, Dockerfile, README.md @ d29e43b
- src/closed_source_model_completion.py (grep only)
- results/gpt-3.5-turbo.json (fields and assert counts computed locally; read-only)
- Paper arXiv 2402.02037: §3.3, §3.4, §5, §5.2, App. A.1, A.14 (Table 24)
