# EvalPerf (Differential Performance Evaluation, in EvalPlus)

Status: critic-checked 2026-11-21 (6 fixes; paper re-read only via arXiv-HTML summary) · Last checked: 2026-11-21
Artifact: https://github.com/evalplus/evalplus @ 26d6d00bb1fd0fa37f39c99d5290da67891d1c5e (local clone: `C:\Users\pc\study\bt-lab\survey\evalplus_evalplus`) · Paper: arXiv 2408.06450 (COLM 2024; PDF read via pdftotext)
Evidence labels: **[src]** read in source (file path + line or paper section quoted/paraphrased), **[inf]** inferred by us from sources, **[unk]** not found (say where you looked).

## 1. What it is
- Python benchmark of performance-exercising tasks (HumanEval+/MBPP+ derived; docs say 118 tasks, paper reports 121 in the COLM version). Each task has one heavy test input and reference solutions grouped in clusters. [src] docs/evalperf.md:17-22; paper §3, abstract-level text @26d6d00.
- Metric: Differential Performance Score (DPS), the cumulative share of reference clusters a correct solution matches or beats. [src] paper §2.4-2.5; evalplus/evalperf.py:257-280.

## 2. Build / environment
- No build step. A solution is Python source `exec`-ed in a forked process. [src] evalplus/perf/profile.py:85-100.
- Requires Linux `perf_event_open` (checked up-front with `simple_test_profiler`); `perf_event_paranoid` may need lowering. [src] evalplus/perf/profile.py:31-43; evalplus/evalperf.py:314.
- Worker parallelism defaults to `max(cpu_count, RAM/12 GB) // 4`; 12 GB RAM per process budget. [src] evalplus/perf/profile.py:27-28; evalplus/config.py:9.
- No cache across candidates except a per-task dict that reuses profiles of byte-identical solution strings. [src] evalplus/evalperf.py:234,246-255.
- Reference solutions are **re-profiled on the user's machine** (lazy, cached per task), not stored as counts. [src] evalplus/evalperf.py:172-219.

## 3. Correctness tests per candidate
- Stage 1 (all `n_samples`=100 samples per task): EvalPlus `untrusted_check` on `base_input + plus_input` against stored expected outputs, with `fast_check=True` so it stops at the first failure. Time limit per test `max(4 s, 4 x reference time)`. [src] evalplus/evalperf.py:76-92, 124-146; evalplus/eval/__init__.py:209,237; evalplus/config.py:2-3.
- Tests are the EvalPlus extended suites (`noextreme=True` variants): HumanEval+/MBPP+ base plus LLM+mutation-generated "plus" inputs. [src] evalplus/evalperf.py:95-108. [unk] number of tests per task (searched evalperf.py, docs/evalperf.md; counts are in the dataset files, not read).
- Pass = all tests pass. Failing samples are never profiled. [src] evalplus/evalperf.py:241-242.
- The efficiency input (`pe_input`) is separate from the correctness tests: one input per task, curated for high cost via the SaS (scale-and-sample) generator. [src] evalplus/evalperf.py:162-166; docs/evalperf.md:20; paper §2.2.
- Test selection per edit: [inf] none; fixed suite; correctness and performance are decoupled stages.

## 4. Performance measurement per candidate
- Metric: CPU instruction count via Linux perf counters (Cirron `Collector`) around calls with the single `pe_input`. [src] evalplus/perf/profile.py:57-61.
- Repeats: `PERF_PROFILE_ROUNDS = 1` (one profile per solution). [src] evalplus/config.py:8; evalplus/perf/profile.py:138,183. Paper §2.5 says each reference is profiled "multiple times" with no number given (App. A.1 uses 5 runs only for the runtime-variation study); [inf] code default is one round, which is acceptable for counters.
- Each round runs in a fresh process; timeout 45 s per evaluation; reference retried twice with +10 s. [src] evalplus/config.py:12; evalplus/evalperf.py:186-203; evalplus/perf/profile.py:145-167.
- Warm-up: the profile function supports warm-up calls but evalperf passes none. [src] evalplus/perf/profile.py:103-106 vs evalplus/evalperf.py:189-194, 249-254.
- Score: iterate references fast to slow; the first reference with count >= the candidate's gives DPS = its cumulative ratio; slower than all references -> cluster -1, score 0. DPS_norm = 100*(j+1)/m. Failure/timeout in profiling gives 0. [src] evalplus/evalperf.py:257-278.
- No statistical test; no speedup threshold; relative-to-reference only. A physical-time profiler exists but is not the default. [src] evalplus/perf/profile.py:50-54.
- Noise: instruction counts "negligible variation" vs runtime; cross-platform study over 4 test beds (desktop, workstation, server, heterogeneous i9-12900K) gave max coefficient of variation 0.4%. [src] paper §4.2 Table 2 (4 test beds: i7-10700K, i9-12900K, TR Pro 5975WX, Xeon 6442Y; max CV 0.4%).
- Curation criteria: tasks need >10k instructions (about "hello world" scale) and >= 4 clusters (adaptive 1-D clustering, base threshold 20%). [src] evalplus/config.py:15-16; evalplus/perf/select_pe_tasks.py:44-46,102-110, 131; paper §3.

## 5. Cost per candidate (if reported)
- Whole evaluation of a model takes "approximately no more than 15 minutes for most" models. [src] paper §4.2. [inf] the "up to 10 profiled solutions on 121 tasks" and per-solution amortised cost were our assumptions, not in the verified sentence; no per-candidate figure is reported.
- Default now: at least `min_correct`=10 passing samples to evaluate a task, up to `max_profile`=min(2*min_correct, n_samples)=20 solutions profiled. [src] evalplus/evalperf.py:301-313, 438-440 (task skipped if n_pass < min_correct), 418-428; the paper version said up to 10 correct. [src] evalplus/evalperf.py:5-9. Note: the module docstring says all correct solutions are evaluated, but `perf_worker` stops at `max_profile` (l.238).

## 6. Iteration / cumulative re-validation
- None: independent samples per task; no edit chaining or refinement loop. [src] evalplus/evalperf.py:124-146. [inf]

## 7. Limitations the authors state
- Paper positions DPE as a meta technique; discusses that only samples that pass are scored and recommends comparing models on commonly passing tasks. [src] paper §5 (Related work, last paragraphs).
- Linux with hardware counters required. [src] evalplus/perf/profile.py:33.
- [unk] No dedicated Limitations section (confirmed on re-read). Closest: DPS needs reference solutions of diverse efficiency (§2.5); counters cannot always replace simulators and counts may vary across platforms (App. A.2).

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- Best precedent for a **deterministic-ish, cheap per-candidate performance signal**: one heavy input and instruction counts instead of repeated wall-time; cross-platform CV <= 0.4%. [src] paper §4; evalplus/perf/profile.py:57-61.
- Strong example of staged reduction: correctness gate with `fast_check` early exit before any profiling, then profile only passing candidates, capped at `max_profile`. [src] evalplus/evalperf.py:241-247; evalplus/eval/__init__.py:209.
- Separation of test suite (many inputs, correctness) from one performance input is a reusable reduced-benchmark design. [src] evalplus/evalperf.py:162-166.
- Caveat: reference counts are recomputed per machine and only valid for one performance input, so cross-edit comparison needs the same baseline program profiled on the same input. [src] evalplus/evalperf.py:172-219. [inf]

## Sources
- evalplus/evalperf.py L1-558 (read L1-520), evalplus/perf/profile.py L1-183, evalplus/config.py, evalplus/perf/select_pe_tasks.py (grep L15-226), evalplus/eval/__init__.py (grep L122-313), docs/evalperf.md @ 26d6d00
- Paper arXiv 2408.06450: §2.2-2.5, §3 (setup), §4.2 (cross-platform variation, Table 2), §5 related work, App. A.2
