# GSO (Global Software Optimization benchmark)

Status: critic-checked 2026-11-21 (8 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/gso-bench/gso @ 32d78b331d59ed689b1238789dc20d36576951c0 (local clone: `C:\Users\pc\study\bt-lab\survey\gso-bench_gso`) · Paper: https://arxiv.org/abs/2505.23671 (CRITIC re-read the PDF text of v3)
Evidence labels: **[src]** read in source (file path + line or paper section quoted/paraphrased), **[inf]** inferred by us from sources, **[unk]** not found (say where you looked).
Path abbreviation: `G/` = `src/gso/` in the clone. Line numbers are from the clone at the commit above.

## 1. What it is (2–3 lines)
- Benchmark of 102 optimization tasks from 10 codebases, 5 languages (Python, C, C++, Cython, Rust); ~59% of tasks need non-Python changes (Table 1 shows 58.8% non-Python; Sec. 2.4 text says "60%"). [src] paper Table 1, Sec. 2.4 (PDF text).
- Agent gets a codebase plus a performance test and must produce a patch that matches the expert commit's speedup; reported as Opt@K. [src] paper Sec. 2.1, 2.3 (PDF text).

## 2. Build / environment
- "Build" = Docker image build (once per instance) plus, at evaluation, a full run of the instance's `install_commands` after the patch is applied. [src] `G/harness/grading/evalscript.py:168-182` (order: base perf runs, `apply_patch`, `install_repo`, patch perf runs).
- Image: one Docker image per instance, built from `ubuntu:22.04` + miniconda + uv; runs `setup_repo.sh` (repo setup + install) and pre-caches test data by running each perf test once. [src] `G/harness/environment/dockerfile.py:3-82`. Evaluation expects images already built/pulled ("expects the image to already be built"). [src] `G/harness/environment/docker_build.py:310-311`.
- Default install command is `uv pip install -e .` in a `uv venv`; instances override it (e.g. onnxruntime gets `./build.sh --config RelWithDebInfo ... --allow_running_as_root`). [src] `G/data/problem.py:84-93`; `G/collect/utils.py:12-18`. The actual per-instance commands live in the HF dataset (`install_commands` field, README `load_dataset('gso-bench/gso')`), not the repo; they are produced at collection time by an LLM-driven setup stage (`G/collect/execute/execute.py:259` reads `install_commands` from experiment data) and cleaned by `prepare_install_commands`. [src] `G/collect/build_dataset.py:28,41`. Per-instance contents [unk] (HF dataset not downloaded; repo contains no per-instance install list, grepped `install_commands`/`RelWithDebInfo`).
- A candidate patch to C/Cython/Rust code therefore triggers a full re-install inside the container: `install_repo` runs `{install_commands}` after `apply_patch`. [src] `G/harness/grading/evalscript.py:111-124, 177-179`. Whether the install is incremental depends on the repo's build system (build dirs persist in the container); GSO does nothing explicit. [inf]
- The install step is run again after `git checkout <opt_commit>` (reference commit) in the same container, so each candidate evaluation does at least 2 full installs. [src] `evalscript.py:204-207`. A third (main-branch) install is disabled (`SKIP_MAIN = True`). [src] `evalscript.py:126, 191-203`.
- Before the reference install, `reset_repo_commands` runs `git clean -xfd` (clean tree); `git clean -xfd` is deliberately removed from the install commands to preserve result files. [src] `evalscript.py:156-158, 189`; `G/data/dataset.py:89-102`.
- Reduced/incremental/skipped build: no mechanism found. Docker layers cache the base install, but nothing selects which build steps to rerun per patch. [src] `evalscript.py` read in full; [unk] for dataset-side install lists.
- During agent generation the paper allows long steps "to allow C/C++ rebuilds" (3 h/task, 20 min per-step timeout). [src] paper Sec. 3 / App. G.1 (PDF text).

## 3. Correctness tests per candidate
- No repo unit tests run. The only check is the benchmark's own LLM-written performance test script run with `--eqcheck`, comparing the candidate's output to a reference result file stored from the base commit (`--reference`). [src] `evalscript.py:127-133` (RUN_BASE uses `--reference`, RUN_PATCH uses `--eqcheck`); prompt rules for `check_equivalence` in `G/collect/generate/prompt.py` (assertions only against the reference result, float tolerance).
- A non-zero exit (assertion failure) gives `>>>>> Tests Errored` and the patch is not scored; exit 124 is a timeout. [src] `evalscript.py:86-102`; `G/harness/grading/metrics.py:298-301`.
- Tests are generated per task at curation time by an LLM with execution-based rejection sampling, then manually curated; mean 12.45 tests per task, max 20. [src] paper Sec. 2.2, App. C.1-C.2 (PDF text); `G/constants.py:34` (MAX_TEST_COUNT = 20).
- Selection: the full fixed set of that task's tests runs for every candidate. No per-edit selection. [src] `G/harness/grading/grade.py:131-139` (all `instance.tests` copied) and `evalscript.py:181` (loop over `range(test_count)`). The repo's own test suite is never run. [inf] (no pytest/unit-test invocation in the harness files read).
- Correctness evidence is narrow (workload output equality only). Paper notes agents overfit tests (input-specific fast paths); tests were oversampled across input distributions to reduce this. [src] paper Sec. 5.2, 7, App. C.2 (PDF text).

## 4. Performance measurement per candidate
- Workloads: the same LLM-generated perf test scripts, using `timeit` with `number=1`; each run appends `Execution time: Xs`. [src] `G/collect/generate/prompt.py` (harness block, "number=1 ONLY"); `metrics.py:125`.
- Repeats: each test script is executed `MAX_ITERS` times: 5 by default, 1 for llama-cpp-python, onnxruntime, tokenizers. [src] `evalscript.py:141-146`. Each repeat is a fresh `python` process. [src] `evalscript.py:84`. Timeout per run 300 s (0 for llama-cpp-python/tokenizers). [src] `evalscript.py:138-140`.
- No explicit warm-up in the eval script; image build pre-runs each test once to fill caches (data downloads). [src] `dockerfile.py:81-82`; [inf] that is a cache warm, not a timing warm-up.
- Statistic: per-test mean over repeats, then per-test speedup = base/patch; gm, hm, am, gsd all computed; success uses the harmonic mean across tests. [src] `metrics.py:46-102, 105-114, 212-226`.
- Thresholds: `opt_base` = `base_mean > patch_mean` and `round(gm speedup patch-vs-base, 1) >= 1.1`; `opt_commit` (the flag Opt@K is computed from, `opt_at_k.py:173-177,225`) = harmonic-mean speedup of patch vs reference commit `> 0.95` AND it is evaluated only INSIDE the `opt_base` branch, i.e. a patch must first show >= ~1.1x geometric-mean speedup over base. [src] `metrics.py:34-43, 256-260`; `G/constants.py:33, 39`. Paper Sec. 2.3 defines OPT_p@K only with S >= p and correctness; the 1.1x gate and strict `>` are code-only. [src] paper Sec. 2.3 (PDF text). (Draft omitted the nesting.)
- Baseline is re-measured per candidate evaluation inside the same container (base runs, then patch, then reference commit). [src] `evalscript.py:174-175, 181, 208-209`. No statistical test (t-test etc.) in the grader. [src] `metrics.py` read in full.
- Noise control: none found in the harness. Container is created without cpuset, memory or CPU limits (only image, name, user, platform, cap_add, env). [src] `G/harness/environment/docker_build.py:326-341`. Parallelism: low-resource instances run `max_workers` at a time on the same host; the two HIGH_RESOURCE repos (llama-cpp-python, tokenizers) are run sequentially (`num_workers=1`) with a doubled timeout. [src] `G/harness/run_evaluation.py:127-175`, `G/constants.py:40`. (README.md:36 only says `--max_workers` scales parallel builds.) Each instance is re-run (up to 3 retries, 330 s sleep) if the base run failed or an HTTP error appears in the log. [src] `G/harness/run_evaluation.py:34-80`. Paper: all tasks on one n2-standard-64 VM (64 vCPUs, 256 GB) (Sec. 3); App. D compares speedups on 16/32/64-core machines and finds raw speedups differ but OPT@K does not. [src] paper Sec. 3, App. D (PDF text).

## 5. Cost per candidate (if reported)
- Wall time per candidate evaluation: not reported in the paper text read. [unk] searched paper HTML (both fetch ranges); code only logs `Test runtime` (`grade.py:146`).
- Structural work per candidate: N tests x 5 base runs + install + N x 5 patch runs + checkout + install + N x 5 reference runs (N up to 20). [inf] from `evalscript.py:168-213`.
- Agent API cost cited as limiting scaling experiments; no figure extracted. [unk]

## 6. Iteration / cumulative re-validation
- Opt@K = fraction of tasks with at least one success in K independent attempts (OR-merge over runs). Each attempt is one patch evaluated from a fresh container; no sequential accumulation of accepted edits. [src] paper Sec. 2.3; `G/harness/opt_at_k.py:60-62` ("OR logic for pass status").
- Within an agent trajectory the agent may edit/rebuild/test many times, but the harness does not re-validate intermediate states. [inf]
- No cumulative or final-state re-check beyond the single patch evaluation. [src] `grade.py` read in full.

## 7. Limitations the authors state
- Small benchmark (102 tasks), so higher variance; speedup is the only runtime metric (no memory/maintainability); hacky or non-idiomatic optimisations remain a concern; contamination judged unlikely. [src] paper Sec. 7 (PDF text).
- Reward hacking observed (memoisation such as `lru_cache`, `__init__.py` overrides) and mitigated by curation, `number=1`, and oversampled inputs. [src] paper Sec. 5.2, 7, App. C.2 (PDF text).

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- Baseline practice is the opposite of reduction: full reinstall after every patch, full fixed test set, three timed phases. Gives a clear control arm for a reduced-build experiment. [src] `evalscript.py:168-213`.
- Correctness oracle is only output equivalence of the perf workloads (no unit tests), so test selection is vacuous; tests are fixed per task, not per edit. Only workload count/repeats could be reduced. [src] `grade.py:131-139`; [inf]
- Timing is noisy by design (fresh process, `number=1`, 5 repeats, no pinning, no statistical test) with a 0.95 ratio threshold; a deterministic substitute would address a gap the harness leaves open. [src] `evalscript.py:141-146`, `docker_build.py:326-341`, `constants.py:39`; [inf] for the gap.
- Per-instance install commands (including full C++ builds such as onnxruntime) are dataset-side, so the build-cost distribution per task is [unk] until the HF dataset is inspected.

## Sources
- Files read (all @ 32d78b331d59ed689b1238789dc20d36576951c0):
  - `src/gso/harness/grading/evalscript.py` 1-250 (full)
  - `src/gso/harness/grading/grade.py` 1-186 (full)
  - `src/gso/harness/grading/metrics.py` 1-371 (full)
  - `src/gso/harness/environment/dockerfile.py` 1-107; `docker_build.py` 303-349
  - `src/gso/data/problem.py` 55-130; `src/gso/data/dataset.py` 60-120
  - `src/gso/collect/utils.py` 1-80; `src/gso/collect/generate/prompt.py` 28-110 (file-level cite for prompt rules; line numbers not individually recorded)
  - `src/gso/constants.py` 1-40; `src/gso/harness/opt_at_k.py` 1-80 (partial); `src/gso/harness/README.md` (grep only)
- Paper: https://arxiv.org/pdf/2505.23671 (Sec. 1, 2.2-2.4, 3, 7, App. D, G.1 re-read from PDF text by critic; Sec. 5.2, App. C only skimmed). Critic also read `G/harness/run_evaluation.py` 28-175, `G/harness/opt_at_k.py` 56-62,173-225, `G/constants.py` 33-40.
