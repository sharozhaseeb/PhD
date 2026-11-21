# Mercury

Status: critic-checked 2026-11-21 (6 fixes; paper sections only partly re-verified, see critic-log-C) · Last checked: 2026-11-21
Artifact: https://github.com/Elfsong/Mercury @ e88551021137c0a1591e198877471d09e5d4fb01 (local clone: `C:\Users\pc\study\bt-lab\survey\Elfsong_Mercury`) · Paper: arXiv 2402.07844 (NeurIPS 2024; critic could only re-read the arXiv HTML via a summarising fetch, the PDF fetch timed out, so paper section numbers below are as reported by that summary: dataset = §2, metric/Eq. 1 = §3, K=5 = §4.3, limitations = §6, timeout = App. A.3, tiers = App. A.10/Fig. 10)
Evidence labels: **[src]** read in source (file path + line or paper section quoted/paraphrased), **[inf]** inferred by us from sources, **[unk]** not found (say where you looked).

## 1. What it is
- LeetCode-based NL-to-code benchmark: 1,889 tasks; Mercury-eval = a difficulty-balanced random 256 tasks, avg 18.4 historical human solutions each, giving a runtime distribution per task. Python. [src] paper §2 (task filters), App. A.2 Table 6 (88 easy/81 medium/87 hard); confirmed 256 tasks in `data/openai/gpt-4-1106-preview_eval.json` (loaded locally).
- Metric **Beyond**: runtime percentile of the generated code within the distribution of human solutions; failing code scores 0. [src] paper §3 Eq. 1 (clip runtime to [min,max]; failed test => runtime +inf => p=0; averaged over N tasks x K samples).
- Note: README (Mar 2026) says a newer evaluator `Mercury_Eval` was released in a separate repo; this clone is the older in-repo `src/`. [src] readme.md:12-14 @e885512. [unk] the new repo was not cloned or read.

## 2. Build / environment
- No build: candidate is a Python class text `exec`-ed in a forked process. [src] src/sandbox.py:174-213 @e885512.
- Fresh `multiprocessing.Process` per candidate and per human reference solution (new namespace, temp dir, libs imported each time; `lctk`, `sortedcontainers` required). [src] src/sandbox.py:162-203, 252-264.
- No container in this repo; isolation is Python-level (`reliability_guard`, which the file itself says is not a security sandbox). Paper describes a "sandbox" with time (30 s) and memory (2048 MB) limits and isolated filesystem. [src] src/sandbox.py:91-97; paper App. A.3.
- No environment caching/rebuild concept; reduced build: not applicable. [inf]

## 3. Correctness tests per candidate
- All tests of the task, in-process, sequentially: `convert_offline` -> call `Solution.<entry_point>` -> `evaluate_offline(inputs, outputs, expected)` per test; pass iff every test passes (`total == passed`). [src] src/sandbox.py:217-235 (load errors do not stop the test loop, l.214-217; the first appended status wins, `result[0]`, l.264); paper App. A.3 (Fig. 5).
- Tests come from a per-task generator written by GPT-4 and validated by submitting 24 generated cases to LeetCode OJ; expected outputs from the human solutions, tasks with non-unique answers dropped. [src] paper §3.1 (Test Case Generator; consistency check across solutions).
- Number of tests per task at evaluation: [unk]; stored as `test_cases` JSON in the HF dataset (not in this repo); Fig. 1 of the paper mentions "100 test cases". [src] paper Fig. 1.
- Failure modes recorded: `failed@load`, `failed@eval`, `failed@cases`, `timeout`, `failed@error`; test failure is captured as status, not early-exit (the loop stops only on an exception); one 30 s alarm covers load + all tests. [src] src/sandbox.py:208-239.
- No test selection; the full list runs per candidate. [inf]

## 4. Performance measurement per candidate
- Runtime = `time.time()` difference around the loop over all test cases within one process (wall clock, one run). [src] src/sandbox.py:218-228. Paper says runtime spans solution instantiation to completion across all tests. [src] paper §3.3.
- Repeats: none in this code. [src] src/sandbox.py:218-228. No statistic, no statistical test, no speed-up threshold; relative scoring only against the human distribution. [src] src/evaluator.py:426-486; reference and candidate runs go through serial `run_sample` calls (l.438,459). The threaded `Sandbox.run_samples` (4 workers) is a separate stale path whose call at evaluator.py:185 passes an unsupported `timeout=` kwarg and sandbox.py:275 increments an undefined `n_samples`; not used for Beyond.
- Reference distribution is rebuilt on the evaluation machine each time: every human solution is re-executed (≈18.4 per task) before scoring candidates. [src] src/evaluator.py:426-441. [inf] the dominant cost per task; and `min(runtimes)` would raise if none passed.
- Beyond in code: `beyond = max_runtime - runtime`, clipped to [0,1] **in seconds**, then divided by (max - min); differs from paper Eq. 1, which clips runtime into [min, max] first. [src] src/evaluator.py:461-466 vs paper Eq. 1. Consequences [inf, arithmetic on the code]: the runtime is not clipped to [min,max], so a candidate faster than every human solution gets beyond_p = (max-runtime)/(max-min) > 1 whenever max-min < 1 s (paper: exactly 1); and max==min divides by zero. The practical gap is therefore not always small. Also the final score averages `cases[0]` only, i.e. one sample per task (Pass@1/Beyond@1, l.477-486), while the paper averages over K=5. Failing code gets runtime inf, so beyond is 0. [src] src/evaluator.py:462.
- Noise controls: hardware-tier test (0.25, 0.5, 1 CPU core) showing Beyond stays consistent across tiers; `OMP_NUM_THREADS=1`; timeout via `setitimer`. [src] paper §3 / App. A.10 Fig. 10 (tiers 0.25/0.5/1 CPU core); src/sandbox.py:113, 52. No CPU pinning in code. [unk] searched src/sandbox.py, src/evaluator.py.

## 5. Cost per candidate (if reported)
- [unk] Not reported (searched paper §4-§6, App.). Timeout 30 s per candidate. [src] paper App. A.3; src/evaluator.py:331,456.

## 6. Iteration / cumulative re-validation
- None; single-shot generation, `num_samples_per_task` random samples per task (script uses `--samples 5`, script/mercury_evaluate.sh:3; paper K=5, §4.3) but the printed score uses only the first. [src] src/evaluator.py:424,481. The "PairWise" evaluator and DPO/SFT training exist for model training, not edit chaining. [src] src/evaluator.py:244-345.

## 7. Limitations the authors state
- Assumes runtime is uniformly distributed over the human solutions; few solutions per task limit precision; data contamination can inflate scores. [src] paper §6 Limitations (uniform-runtime assumption, few solutions, contamination).

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- Gives a way to avoid absolute-time thresholds (percentile vs reference set), but costs re-running ~18 references per task on each machine; unlike a per-edit baseline-vs-edit comparison. [src] src/evaluator.py:426-441. [inf]
- Same run serves correctness and timing, fully serial in-process; timing is non-deterministic single wall-clock sample. [src] src/sandbox.py:217-228.
- Demonstrates evidence that Beyond ranks are stable across CPU quota tiers, a citable data point for "relative metrics tolerate noisier hardware". [src] paper Fig. 10 / App. A.10.

## Sources
- src/sandbox.py L1-283, src/evaluator.py L1-517, readme.md, script/mercury_evaluate.sh @ e885512
- data/openai/gpt-4-1106-preview_eval.json (structure only)
- Paper arXiv 2402.07844: §3.1, §3.3, §4 setup, §6, App. A.3 (Fig. 5), Fig. 10
