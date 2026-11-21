# R1 - PerfAgent full read (arXiv:2607.19653v1, 22 Jul 2026)
Source: PDF read in full via pdftotext (17 pages; body pp.1-11, refs, Appendix A-D pp.13-17). File: papers/2026-PerfAgent-arXiv.pdf. Labels: [read-in-source §x p.y] / [unknown]. Page numbers are PDF pages (approx. +-1).
Important: the "supplemental material" in the text = Appendices A-D at the end of the same PDF. "Section B of the supplemental" = APPENDIX B "Filtering and selecting tests" (p.15) + Tables X/XI (p.16). It is SHORT and contains NO testmon mechanics.

## a. §III-D selective validation
- Mechanism claim: [read-in-source §III-D p.5] "uses code-coverage information to precisely select only the tests affected" ; "without missing any correctness regressions" (asserted, not measured).
- Run after every iteration on a "curated test suite"; failures returned as feedback [§III-A p.3, §III-D p.5]. Build failure or any test failure exits outer phase early and returns error output [§III-A p.3].
- Savings: tests run reduced "66%-99% on GSO and 47%-98% on SWE-fficiency-Lite" vs full suite [§III-D p.5]; counts in Tables X, XI [App. B p.16].
- How testmon DB is created / which run seeds it / on which revision: [unknown] (not stated anywhere).
- When DB refreshed across iterations: [unknown].
- Fallback to full suite (when): [unknown]; none described.
- Native-extension files trigger anything: [read-in-source §VI p.10] testmon "tracks only Python coverage"; so native-extension regression "can slip between iterations". No mechanism (rebuild-triggered rerun etc.) described. Future work: "extending selective testing to native-extension coverage" [§VII p.10-11].
- Cost of seeding run: [unknown]. (Only implicit: Appendix B runs the suite 5x per task offline for flake filtering; not testmon seeding.)

## b. Supplemental Section B (Appendix B, p.15-16)
- Pre-filtering at base commit: failing tests and flaky tests removed. Flakes: "we run the test suite 5 times" with different random seeds and randomized order; exclude tests failing in any run; "produces a stable test suite for each of the tasks".
- Tables X (SWE-fficiency-Lite) / XI (GSO): per repo columns Base Test Count, Filtered Test Count, Patch Test Count (mean +- sd over tasks). "Patch Test Count" = tests selected by agent's changes (inferred = testmon selection; paper only says "selecting tests based on the specific changes made by the agent").
- Examples: GSO numpy 35,002 base -> 34,458 filtered -> 109 patch; pandas 130,994 -> 130,002 -> 4,691; tornado 330 -> 179 -> 1.75; SWE-ff pandas 170,837 -> 164,893 -> 31,666; scipy 36,842 -> 25,329 -> 1,312. Large SDs (e.g. numpy 109 +- 614) => selection highly skewed/variable.
- No wall-clock time, no seeding cost, no per-iteration refresh, no miss analysis.

## c. §VI Threats to validity (p.10), near-verbatim
Construct/internal: performance measured on the single given workload; SWE-ff times only provided script (easy to game; reward hacking). "Because our controller validates with pytest-testmon, which tracks only Python coverage, a native-extension regression can slip between iterations; this deflates rather than inflates our score, since each benchmark's own correctness suite runs at evaluation time." External: ~dozen Python-centric repos, 2 models, one harness (Mini-SWE-Agent); single-run results; Kimi GSO gap ~2 tasks.

## d. Full suite / misses / safety eval
- Does PerfAgent run the full suite at any point (final patch, best-patch selection)? [read-in-source §III-A,C p.3-4] No: only curated/selected tests per iteration; best patch = highest measured speedup among submitted (patches that failed build/tests exit before profiling, so effectively only passing ones). The benchmark's own correctness suite (GSO hidden tests; SWE-ff "curated subset of the repository's existing test suite" [§II p.3]) is run at evaluation, outside PerfAgent.
- Misses of selective validation (tests failing under full suite but not selected): [unknown] - not reported. No testmon safety/recall evaluation.
- Indirect evidence only, final correctness at benchmark eval [Table II p.6-7]: GSO: OpenHands 88.2, Codex 89.2, AL(loop only) 91.2, +Tests 96.1, +Profiler 95.1, PerfAgent 96.1. SWE-ff-Lite: 82, 80, 80, 93, 83, PerfAgent 90. So PerfAgent still fails 3.9% GSO (4 of 102) and 10% SWE-ff (10 of 100) correctness - residual includes both selection misses and other causes; paper does not decompose. App. D (p.17): PerfAgent failed correctness on pandas-2f4c93e (GSO) and numpy-12575, numpy-21832, pandas-39332 (SWE-ff) where OpenHands passed.
- Fig. 4 (p.5): GSO instances with validation failure before submit fall 53 -> 5 over turns 1->5; avg speedup 2.5x -> 6.4x.

## e. Acceptance rule
- Per iteration: apply patch, rebuild; fail on build error or any test failure -> feedback, no profiling [§III-A p.3]. Else profile, measure speedup on provided workload [§III-A p.3].
- Final output: "the patch with the highest speedup" over up to N=5 submissions [§III-A p.3; Fig.1 caption]. No minimum-speedup threshold in controller [unknown if any]. Budget: $5/task, 200 steps [§IV-A p.6].
- Evaluation thresholds (benchmark, not controller): Opt@1 = correct and speedup ratio SR>=0.95 vs human; Sp@1 uses 1.2x speedup threshold [§IV-A1 p.6].
- Timing repetitions / statistics / noise handling in controller: [unknown]. (Only: SWE-ff harness times workload many times in a loop, separate Python process per evaluation [§IV-A2 p.6-7]; reward-hack fix of timing only first run for the AL ablation.)

## f. Build
- Controller "rebuilds" after each patch [§III-A p.3]; agent prompt: "/build.sh rebuilds the repository", "Do not build the repository in other ways" [App. A p.13]. Whether incremental: [unknown]; build.sh contents: [unknown]. "Some rebuilds may take time" implies non-trivial builds (C/Cython/Rust repos).

## g. Code / artifacts
No PerfAgent repository/artifact link found in text. GitHub URLs present are only for Codex, py-spy, deep-swe (refs). Built on Mini-SWE-Agent; profiler py-spy [ref 12]. [unknown] whether code is released.

## Relevance note
PerfAgent validates iteratively with testmon selection but gives no soundness/recall data and no seeding/refresh/fallback details; the native-extension blind spot is acknowledged by the authors. Useful as the closest prior work that motivates (and leaves open) the question of validated reduced build/test checks.
