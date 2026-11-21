# OpenEvolve

Status: critic-checked 2026-11-21 (8 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/algorithmicsuperintelligence/openevolve @ 4167db4325727138215c55470fdd5cd302f74b66 (main, 2026-11-20; cloned at bt-lab/survey/algorithmicsuperintelligence_openevolve, HEAD verified = 4167db4, package version 0.4.1) · Paper: none (open-source AlphaEvolve reimplementation; HF blog https://huggingface.co/blog/codelion/openevolve, not read)
Evidence labels: **[src]**, **[inf]**, **[unk]**. Critic re-read evaluator.py and config.py in the local clone; line numbers below are exact at 4167db4.

## 1. What it is
Evolutionary program-search framework (LLM mutations, MAP-Elites DB). The user supplies `evaluate()`; the framework only orchestrates scoring. AlphaEvolve itself is covered elsewhere. [src openevolve/evaluator.py; search results]

## 2. Build / environment
- No build concept: each candidate is written to a fresh `tempfile.NamedTemporaryFile` (suffix = program_suffix, deleted in `finally`) and the user's evaluate function is called with its path [src evaluator.py:258-271, 391-393]. The call runs in-process in a `ThreadPoolExecutor` thread (not a subprocess/sandbox) with `asyncio.wait_for` timeout; a timed-out thread is orphaned, not killed [src evaluator.py:64-72, 452-461].
- No result cache in evaluator.py (no "cache" string in the file) [src evaluator.py grep]. Any compile/install is the user's evaluator's job. [inf]

## 3. Correctness tests per candidate
- Entirely user-defined (inside evaluate / evaluate_stage1..3). Framework supports cascade: stage1 (cheap) gated by `cascade_thresholds[0]`, stage2 by `[1]`, stage3. Failed thresholds return partial results. [src evaluator.py:467-660; thresholds applied at 531-535 and 596-598 via `_passes_threshold` (:797-830: uses `combined_score` if present, else mean of numeric metrics except `error`)]. Config defaults: `cascade_evaluation=True`, `cascade_thresholds=[0.5,0.75,0.9]`, `timeout=300`, `max_retries=3`, `parallel_evaluations=1` [src config.py:411-430]. If a later stage function is absent the cascade returns the earlier partial result.
- That stages are ordered smoke test -> quality gate -> benchmark so timing only runs on correct candidates is a convention in an example README (examples/background_blur/README.md:172 "stage 1 cheap smoke test"), not enforced by the framework [src example]; release notes not checked [unk].
- This is staged early-exit validation per candidate (a form of cost-ordered test selection), but which tests go in which stage is decided by the user. [inf]

## 4. Performance measurement per candidate
- Entirely user-defined; framework only receives metrics dict (or EvaluationResult with artifacts), optional `combined_score`, optional LLM-judge feedback when `use_llm_feedback`: LLM metrics are scaled by `llm_feedback_weight` (default 0.1, config.py:430), and if `combined_score` exists it is overwritten by 0.7*accuracy + 0.3*LLM average, constants hard-coded [src evaluator.py:292-317]. `_process_evaluation_result` not re-read [unk].
- Noise control: none in framework. [unk]

## 5. Cost per candidate
- Per-eval timeout via asyncio.wait_for; timeout returns {"error": 0.0, "timeout": True}, no retry [src evaluator.py:356-368]; non-timeout exceptions retried up to max_retries+1 attempts with 1 s sleep [src :258, 373-388], then {"error": 0.0} [:399]; concurrency limited by `parallel_evaluations` (TaskPool and executor size) [src :64-69]. Defaults: timeout 300 s, retries 3 [src config.py:411-412].

## 6. Iteration / cumulative re-validation
- Iterates by design; each child is scored independently from its parent; no cumulative re-validation of an accumulated lineage. [inf]
- Claimed past bug (timeout averaged to 0.5, fixed v0.3.2) comes from search snippets only; not confirmed in the clone (no changelog file) [unk]. Current code returns error 0.0 on timeout (evaluator.py:368) [src].

## 7. Limitations stated
- [unk] in files read.

## 8. Relevance to Study 1
- [src] Concrete public implementation of cascade (cheap-gate-first) evaluation; a reference design for "reduced per-edit validation" ordering.
- [src] Shows failure-handling pitfalls (timeout scoring) that affect acceptance decisions.
- [inf] Provides no build/test reduction itself; Study 1 would be an evaluator plugged into it.

## Sources
- openevolve/evaluator.py @ 4167db4
- openevolve/config.py:405-430; examples/background_blur/README.md:172; GitHub releases page not fetched [unk]
