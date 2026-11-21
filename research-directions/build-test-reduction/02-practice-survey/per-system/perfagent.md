# PerfAgent

Status: critic-checked 2026-11-21 (10 fixes) · Last checked: 2026-11-21
Artifact: none found (see Sources) · Paper: https://arxiv.org/html/2607.19653v1 (arXiv:2607.19653v1, cs.SE, 22 Jul 2026; Deng, Liu, Lipka, Ma, Chen, Kaler, Ganhotra; MIT / RPI / IBM / MSU)
Evidence labels: **[src]** read in source (file path + line or paper section quoted/paraphrased), **[inf]** inferred by us from sources, **[unk]** not found (say where you looked).
Reading limit (researcher): the fetch tool returned only the first ~100k of 115.7k characters of the HTML, so appendices were not read. Critic re-read the full PDF text (arxiv.org/pdf/2607.19653v1, ~1190 lines incl. Appendices A–D, Tables X–XI). Section references below use the paper's own numbering; the 'supplemental material' Sections A–D are the PDF's Appendix A–D.

## 1. What it is (2–3 lines)
A workflow wrapped around an off-the-shelf coding agent (Mini-SWE-Agent with GPT-5.1 or Kimi-K2) for repository-level Python optimization. Three parts: curated py-spy profile feedback, a loop controller that intercepts the agent's STOP and keeps iterating, and selective validation with pytest-testmon. [src] Sec. III-A to III-D, IV-A.
Evaluated on GSO (102 tasks, 10 repos) and SWE-fficiency-Lite (100 tasks, 9 repos). [src] Sec. II, Table I, IV-A.

## 2. Build / environment
- After each submitted patch the controller "applies the patch ... builds the repository, runs tests and profiles". If the build fails or any test fails, the outer phase exits early and the error goes back to the agent (no profiling run on that patch). [src] Sec. III-A.
- The build is a script `/build.sh`: the agent prompt says to rebuild only through it. It also warns that "Some rebuilds may take time". [src] Appendix A (agent prompt).
- Whether the rebuild is incremental or full is not stated anywhere in the paper (checked Appendix A prompt and III-C). [unk]
- Rebuilding matters because the repos contain native extensions (the paper says py-spy was chosen since it also sees native code, and the testmon limitation names native extensions). [src] Sec. III-B, VI.
- Per-instance container images come from the benchmarks (GSO / SWE-fficiency). Whether builds are cached across iterations is not stated. [unk] Hardware: agents run on AWS c6i.8xlarge (32 CPUs, 64 GB); final evaluation on m8i.16xlarge (64 CPUs, 256 GB). [src] Sec. IV-A.

## 3. Correctness tests per candidate
- **Selective validation (Sec. III-D).** "PerfAgent's controller runs a curated test suite against the agent's patch after each iteration"; it uses pytest-testmon, which selects "only the tests affected by the agent's changes". Reported reduction vs the full suite: 66%–99% on GSO, 47%–98% on SWE-fficiency-Lite (the paper's own wording; the per-repo averages are in Tables X/XI). [src] Sec. III-D, Appendix B. Selection is therefore per submitted patch (per iteration), not fixed per task. [src] Sec. III-D ("after each iteration"), Appendix B ("selecting tests based on the specific changes made by the agent").
- Appendix B ("Filtering and selecting tests"): before the run, tests that fail at the base commit and flaky tests are removed; flaky = run the suite 5 times with different random seeds and randomised order, drop any test failing in any run. Tables X/XI list per-repo "Base / Filtered / Patch Test Count" (e.g. GSO numpy 35,002 / 34,458 / 109; pandas 130,994 / 130,002 / 4,691). [src] Appendix B, Tables X, XI. The "Patch Test Count" column is presumably the testmon-selected count per patch. [inf]
- Still not described anywhere in the paper: how the testmon database is built or refreshed after each patch, whether it falls back to the full suite, and the time cost of the baseline/seed run. [unk] (Appendix B read in full.)
- Selection is coverage-based (testmon) on Python-level dependencies. [inf] from III-D and VI.
- III-D also claims the selection works "without missing any correctness regressions"; Sec. VI contradicts that for native code (below). [src]
- Test failures are returned to the agent as feedback. [src] Sec. III-A.
- Final grading uses each benchmark's own correctness suite at evaluation time. That is part of the benchmark harness, not of PerfAgent's loop. [src] Sec. VI.
- Stated hole: testmon "tracks only Python coverage", so native-extension regressions can slip through between iterations. [src] Sec. VI.

## 4. Performance measurement per candidate
- Workload: one script provided by the benchmark instance. The agent loop times it; py-spy profiles it over a fixed 10 s window with setup frames dropped. [src] Sec. III-B, III-A.
- Timing uses only the first run, not an average over profiling iterations ("only times the execution time of the first run"). Authors report this adds variance "< 3% of overall runtime on average". Averaged timing was avoided because an agent can cache on the first run and replay it. [src] Sec. IV-E4. In the loop-only ablation AL on SWE-fficiency-Lite, switching to a first-run-only script cut flagged hacks from 18 to 3. [src] Sec. IV-E4. The <3% figure is the authors' own claim; how it was measured is not shown. [unk]
- Number of timing repeats and the statistic for the final reported speed-up are not given (the controller records "the speedup of each submitted patch on the provided workload"). [src] Sec. III-A; repeats/statistic [unk]. Final scores use each benchmark's own harness (GSO hidden perf tests; SWE-fficiency timing of the provided script). [src] Sec. II, IV-A.
- Success thresholds are from GSO: Opt@1 = correct and speed-up >= 0.95x of the human expert; Sp@1 = speed-up >= 1.2x. The 1.2x is meant to filter out timing-variance gains. [src] Sec. IV-A1.
- No CPU pinning, isolation or instruction counting mentioned anywhere in the paper (only the instance types above). [unk]

## 5. Cost per candidate (if reported)
- Cap: $5 per task, 200 steps, up to 5 submissions (theta = 5). [src] Sec. IV-A.
- Average cost per task: $2.88 (GSO), $4.25 (SWE-fficiency-Lite); OpenHands best@5 with oracle: $11.01 and $9.91. [src] Table VI.
- A $10 budget lifted SWE-fficiency-Lite Opt@1 from 75% to 79%. [src] Sec. IV-E5.
- Wall-clock per candidate and build time are not reported in the part read. [unk]

## 6. Iteration / cumulative re-validation
- Up to 5 outer iterations; each rebuilds, runs the selected tests and re-profiles (Sec. III-A: "every iteration re-validates the patch against the test suite"). [src] Sec. III-A, III-C, IV-A.
- Best-patch selection: the controller returns the submitted patch with the highest measured speed-up, not the last one. Fig. 3: Turn 4 (5.87x) kept over Turn 5 (5.85x). [src] Sec. III-A, III-C.
- Patches are refinements of one working tree across turns (the agent continues), not independent per-function edits. [inf]
- No separate full-suite re-run of the final selected patch inside PerfAgent is described. Each patch is validated once, in its own iteration, with the selected tests. [inf] Sec. VI confirms the benchmark's own correctness suite runs only at evaluation time. [src]
- Risk this creates: the selected patch may have been checked only against testmon-selected tests; the full correctness suite is run only by the benchmark afterwards. [inf]

## 7. Limitations the authors state
[src] Sec. VI unless noted:
- One provided workload per task, which may not generalize.
- testmon covers Python only; native-extension regressions can slip through.
- The LLM judge for reward hacking can miss or over-flag.
- Single run; small gaps (about two tasks for Kimi-K2 on GSO) are within noise.
- Two benchmarks, two models, one harness; not tried with OpenHands or Codex.
- 18 hack instances (SWE-fficiency-Lite, loop-only ablation) before the first-run timing fix, 3 after (Sec. IV-E4); SWE-fficiency times only the provided script and is "easier to game" (Sec. VI). [src]

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- Direct precedent for per-edit test selection in an LLM optimizer: coverage-based selection (pytest-testmon) in the loop, with 47%–99% of tests skipped (authors' figures). [src] Sec. III-D, Tables X/XI. No guarantee of safety is stated; native code is a known blind spot. [src] Sec. VI. This is the baseline to compare a build-aware selection with. [inf]
- The build is run after every patch through one script, with no reduction described. [src] Sec. III-C, App. A. A reduced or incremental build per edit is an open gap in this system. [inf]
- Timing is a single first-run measurement, with <3% variance claimed. [src] Sec. IV-E4. This is not a deterministic metric. [inf]
- Best-of-iterations selection with no final re-validation of the chosen patch against the full suite is a concrete case for cumulative / final re-validation. [inf]

## Sources
- Paper: researcher read HTML text (first ~100k chars). Critic re-read the full PDF text https://arxiv.org/pdf/2607.19653v1: Sec. II, III-A to III-D, IV-A, IV-E4, IV-E5, VI, Tables I, VI, IX–XI, Appendix A (prompt), Appendix B (filtering/selecting tests).
- Not read by critic: Appendix C/D beyond skim (reward-hack cases, win/loss analysis).
- Public code search: arXiv abs page https://arxiv.org/abs/2607.19653 lists no code link (only generic third-party panels). The HTML text lists only links to py-spy, Codex CLI and Kimi-K2. A web search for "PerfAgent ... github pytest-testmon" returned only the arXiv, alphaXiv, HF papers and Pith pages. GitHub repository search for "PerfAgent py-spy testmon" returned 0 results. Conclusion: no public code found (not proof that none exists). [unk]
