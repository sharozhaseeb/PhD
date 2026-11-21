# EffiBench-X

Status: critic-checked 2026-11-21 (12 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/EffiBench/EffiBench-X @ 21b6668a49a342c843e679cc5ed16081064a5768 (main, commit date 2025-10-24; local clone `C:/Users/pc/study/bt-lab/survey/EffiBench_EffiBench-X`, HEAD verified by critic); data https://huggingface.co/datasets/EffiBench/effibench-x · Paper: https://arxiv.org/abs/2505.13004 (HTML; critic re-read the first ~100k chars via a summarising fetch; App. A and C.2 text not seen)
Evidence labels: **[src]**, **[inf]**, **[unk]**. Critic re-opened the code the first pass did not read: evaluate_solution.py, effibench/run_tests.py, effibench/utils.py, effibench/backends/docker.py, third_party/llm-sandbox/llm_sandbox/{utils.py,docker.py,profiler.cpp,statistics.cpp} (file:line @21b6668).

## 1. What it is
Multi-language (Python, C++, Java, JS, Ruby, Go) competitive-programming efficiency benchmark; scores LLM code against human expert solutions on time, memory peak, memory integral. [src abstract via search; README Features]

## 2. Build / environment
- Language images (gcc:14.2.0, openjdk:21, node:22.14.0, ruby:3.2.7, golang:1.23.7, python:3.11.11); the registry also lists `flags` (C++ `-O2 -fsanitize=address`, Node `--harmony`). [src] effibench/utils.py:301-364. The `flags` field has no consumer in the repo: the commands actually executed are `g++ -std=c++20 -O2 -o a.out` (no ASan), `javac --enable-preview --release 21`, `node --harmony`, `go run`. [src] third_party/llm-sandbox/llm_sandbox/utils.py:116-127; grep for `flags` finds only the registry. [inf] ASan is not applied at measurement time in this snapshot (paper Table 13 not re-read).
- Per-candidate compile happens inside the container, outside the profiler: only the last command (binary / `java` / `go run` / interpreter) is wrapped by the profiler. [src] llm_sandbox/utils.py:133,141. For Go, `go run` puts the Go build inside the measured window. [inf]
- Build reuse: within a worker session the code file is rewritten only if the source string changed, and then only the final run command is re-executed (compile skipped), so the first test of a candidate pays the compile and the other tests reuse the binary. [src] third_party/llm-sandbox/llm_sandbox/docker.py:327-331,358-359.

## 3. Correctness tests per candidate
- 100 generated tests per problem (fixed seed: boundary/typical/stress/edge); canonical solutions supply expected outputs. [src] paper §3.3 (via summary); evaluate_solution.py:58 (`generated_tests`).
- Every test is a separate execution (separate submission, fresh profiled process), submitted as one batch per candidate; a worker runs a batch sequentially. Evaluation calls `run_tests(early_stop=False, raise_on_error=False, as_batch=True, polling_interval=30)`, so all tests always run even after a failure. [src] evaluate_solution.py:63-73; effibench/run_tests.py:43-57,65-72; effibench/backends/backend_utils.py:353-369. (run_tests defaults are early_stop=True, raise_on_error=True; not used here.)
- Pass = every test passed: `is_passed` counts a test as passed if `passed` is true, OR (status done, empty output, exit 0), OR output equals input+output text; any non-pass leaves runtime/memory stats None and the problem scores 0. [src] evaluate_solution.py:232-246,272-280,311-336. [inf] the empty-output branch is a lenient oracle; not checked per problem.
- Fixed per problem; no selection. [inf]

## 4. Performance measurement per candidate
- Profiler: C++ `profiler` forks the command and samples `/proc/<pid>/statm` RSS every `sampling_interval` (default 0.0001 s) with `sleep_until`; runtime = last sample timestamp minus first (ns); max RSS; memory-time integral by trapezoid. [src] third_party/llm-sandbox/llm_sandbox/profiler.cpp:39-40,100-158; statistics.cpp:10-32,73-91; llm_sandbox/utils.py:92,133. [inf] runtime is quantised to about one sampling interval and includes interpreter/JVM start-up.
- Limits: `timeout 10` and 1024 MB per test run (profiler kills when RSS exceeds the limit). [src] effibench/run_tests.py:49-50,65; llm_sandbox/utils.py:132-137; profiler.cpp:127-146. Paper §5 gives the same limits.
- Scores: expert/LLM ratios clipped to [0,1] per problem (memory, runtime max and sum over tests, integral max/sum), averaged over problems; failed problems contribute 0. [src] evaluate_solution.py:271-279,311-340.
- No statistical test; no threshold other than the clipping. [src] evaluate_solution.py:311-340.
- Noise control: each backend worker's container gets `cpuset_cpus` = all logical CPUs of one physical core (worker_id mod #physical cores); server default workers = physical cores - 1. [src] effibench/backends/docker.py:47-57; start_sandbox.py:40-44; paper §3.4. Different candidates run concurrently on different pinned cores (evaluation uses `n_processes` default = cpu_count). [src] evaluate_solution.py:99-121,130-131. [inf] concurrency across cores still shares caches and memory bandwidth.
- Repeats: none in the evaluation code path (one profiled run per test). [src] evaluate_solution.py:63-73. The paper's repeat/noise study (App. C.2: 3 runs etc.) was NOT re-verified by the critic; treat as [unk] until read.

## 5. Cost per candidate
- Authors note high computational cost of evaluation (no figure; App. A text not re-read). [unk] Code-level floor: results are polled every 30 s per batch. [src] evaluate_solution.py:72; run_tests.py:96-97.

## 6. Iteration / cumulative re-validation
- None; single-shot generation scoring. [inf]

## 7. Limitations stated
- Competitive programming may not generalise; sandbox has "proprietary enhancements" hard to reproduce; fixed-seed tests may miss worst cases; clipped ratios. [unk] first-pass paper citations (§A, §3.4, §3.3) not re-verified: App. A was beyond the text the critic could read.

## 8. Relevance to Study 1
- [src] Strongest published noise control by core pinning in a benchmark (but one run per test, no statistical test); a reference for the non-instruction-count approach. effibench/backends/docker.py:47-57.
- [src] Evaluates all 100 tests every time (early_stop=False), with compile reuse across the tests of a candidate: baseline cost against which reduced tests would be compared. evaluate_solution.py:69; llm_sandbox/docker.py:358-359.
- [inf] Low priority for repo-level work; function/program level only.

## Sources
- README.md; evaluate_solution.py L28-135, 225-345; effibench/run_tests.py L43-166; effibench/utils.py L301-364; effibench/backends/docker.py L27-71; start_sandbox.py L30-60; third_party/llm-sandbox/llm_sandbox/{utils.py L87-142, docker.py L296-380, profiler.cpp, statistics.cpp} @ 21b6668
- arXiv 2505.13004 §3.3-3.5, §5 (verified via summary); §A, §C.2, Table 13 not re-read
