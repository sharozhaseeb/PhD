# KernelBench

Status: critic-checked 2026-11-21 (11 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/ScalingIntelligence/KernelBench @ 423217d9fda91e0c2d67e4a43bf62f96f6d104f1 (main, commit date 2026-03-05; local clone `C:/Users/pc/study/bt-lab/survey/ScalingIntelligence_KernelBench`, HEAD verified by critic) · Paper: https://arxiv.org/abs/2502.10517 (not fetched; every paper-level statement here is [unk]/unverified)
Evidence labels: **[src]**, **[inf]**, **[unk]**. Code lines re-opened by the critic in the clone (file:line @423217d).

## 1. What it is
Benchmark of PyTorch ops/models for which an LLM writes faster GPU kernels (CUDA, later Triton/CuTe/TileLang etc.); metric fast_p = correct AND speedup > p (fraction over all n tasks). [src] README.md:51-52; src/kernelbench/score.py:28-36 (`speed_up > p`, divided by n).

## 2. Build / environment
- "Build" = JIT compile of a torch C++/CUDA extension per candidate, in-process: the candidate source is prefixed with `os.environ['TORCH_EXTENSIONS_DIR']=<build_dir>` and `exec`-ed, so torch's extension loader builds during import. [src] src/kernelbench/eval.py:184-207 (`load_custom_model`), :522. For triton/tilelang/cute backends the source is written to a temp .py and imported instead. [src] eval.py:151-181, 513-519.
- Separate pre-compile path: `build_compile_cache` runs the same load on CPU "to do this massively in parallel" and stores the artifacts in the cache directory; the later GPU eval loads from the same `build_dir` (per run/problem/sample dir). Only `build_compile_cache_with_capturing` uses a subprocess (`python tmp.py`). [src] eval.py:289-327, 330-367; src/kernelbench/compile.py:30-52. So there is an explicit build-once-then-evaluate split (cached per candidate dir; no sharing across different candidates). [inf]
- Compile-lock / missing-file errors return None ("retry"). [src] eval.py:530-537.

## 3. Correctness tests per candidate
- Output equality vs reference Model on random inputs: `num_correct_trials` library default 1 but all scripts use 5; seed 42 with per-trial seeds drawn from it; `torch.allclose` with atol=rtol=1e-4 (fp32) or 1e-2 (fp16/bf16); all trials must pass. [src] eval.py:83-102, 397-398, 727-845; scripts/eval_from_generations.py:120,182; scripts/run_and_check.py:107; scripts/generate_and_eval_single_sample.py:266. (Comment at eval.py:800 says v0/v0.1 used 1e-2 for fp32.)
- Differential testing against the PyTorch reference on random inputs; no human test suite. [src] eval.py:750-806.
- Test selection: none; fixed generator-seeded inputs per task. [inf]

## 4. Performance measurement per candidate
- cuda_event timing: 3 warm-up calls (default), then `empty_cache`, then per trial: sync, L2-thrash (256 MB int64 tensor fill), event record around the call, sync; the first trial is discarded (`discard_first=1`); stats = mean/std/min/max/num_trials (std is population std). [src] src/kernelbench/timing.py:126-142, 201-281, 602-625.
- Library default `num_perf_trials=10`; the scripts use 100 (eval_from_generations.py:121,183; run_and_check.py:109; generate_and_eval_single_sample.py:267). Reference-baseline timing (`measure_ref_program_time`) defaults to 5 warm-ups and 100 trials. [src] eval.py:399; timing.py:9-15.
- Speed-up is ratio of mean times; no statistical test, no confidence interval. [src] eval.py:683; timing.py:613-619.
- Baselines: precomputed per GPU in `results/timing`, but README recommends generating your own (power, software versions affect timing). [src] README.md:153-154. In addition, `eval_kernel_against_ref` re-times the PyTorch reference in the same call (default `check_for_excessive_speedup=True`), i.e. one extra reference timing per candidate. [src] eval.py:654-680.
- Anti-cheat: flags (does not fail) speedup > 10x (`excessive_speedup_threshold=10`); regex `kernel_static_checker.py`; adversarial unit tests (reuse of cached reference output, input mutation, non-default CUDA stream). [src] eval.py:411-412, 691-695; EVAL.md (Checkers, Unit Tests with Adversarial Examples); src/kernelbench/unit_tests/test_eval_adversarial.py (file exists; contents not read).

## 5. Cost per candidate
- [unk] no per-candidate cost figure in the repo. [inf] compile plus 100 timed trials with L2 flush, plus a reference re-timing, is the per-candidate cost shape; "compile dominates" is not shown by any source we read.

## 6. Iteration / cumulative re-validation
- Core eval is single-shot per candidate. Multi-turn refinement is delegated to the separate Caesar engine (feeds correctness/runtime/profiling back each turn); EVAL.md does not discuss refinement. [src] README.md:164; eval.py:511 (comment on multi-turn hashes). Each refined kernel re-runs full compile + correctness + timing. [inf]

## 7. Limitations stated
- Reward-hacking exploits (no-op kernels, stream tricks, calling torch ops); EVAL.md marked work in progress, correctness section "More coming". [src] EVAL.md (Correctness: "More coming"; Methodology "More on that coming"; reward-hacking warning). [unk] v0.1 blog not read.

## 8. Relevance to Study 1
- [src] Textbook per-candidate loop: compile -> differential correctness vs reference -> event timing; correctness cost small relative to compile.
- [src] Hardening against cheating (static checker, excessive-speedup flag) shows validity risks when correctness is reduced to a few random inputs.
- [inf] Not repo-level; useful as contrast for what "reduced test per edit" does with a single-function oracle.

## Sources
- src/kernelbench/eval.py L83-102, 151-207, 289-367, 394-700, 727-845; timing.py L9-15, 126-142, 201-281, 602-625; score.py; compile.py L30-52; scripts/eval_from_generations.py, run_and_check.py, generate_and_eval_single_sample.py (grep); EVAL.md; README.md @ 423217d
- arXiv 2502.10517 not read (the earlier "paper says 5 trials" is confirmed only by the scripts)
