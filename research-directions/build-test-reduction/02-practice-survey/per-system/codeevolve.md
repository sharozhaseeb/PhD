# CodeEvolve (multi-language, runtime-enriched target selection)

Status: critic-checked 2026-11-21 (4 fixes) · Last checked: 2026-11-21
Artifact: none public found; neither the abstract page nor the paper links a repo (only OpenEvolve is cited as base) [unk] · Paper: arXiv 2605.04677, "CodeEvolve: LLM-Driven Evolutionary Optimization with Runtime-Enriched Target Selection for Multi-Language Code Enhancement" (Borra et al.; enterprise Java/Apex). Critic re-read the full arXiv HTML text (v1, 6 May 2026).
Evidence labels: **[src]**, **[inf]**, **[unk]**.

## 1. What it is
OpenEvolve extension: JFR profiles pick hotspots, an LLM proposes edits, MCTS and islands (K=5, ring, migration every 50 generations), automated refinement. Reports 15.22 average speedup over 7 Java hotspot functions in the Salesforce Monolith, where each function's figure is averaged over 4 LLMs (GPT-4.1, Llama 4, Mistral, internal model) and compared to single-pass RPBD (7.12; CodeEvolve wins 5/7). [src 1.2, 5.1, 5.2, Table 2; Sec. 3, App. C]

## 2. Build / environment
- Java cascade: build validation, unit tests, performance tests, static checks, LLM review; Apex: syntax validation, sandbox tests, governor-limit checks, Apex review. "Candidates must pass early correctness checks before later quality and performance stages." [src 3.3]
- Build tool, incremental or cached builds: [unk] (Maven/Gradle not named).

## 3. Correctness tests per candidate
- Stage thresholds tau1=0.5, tau2=0.75, tau3=0.9, LLM-evaluator weight alpha=0.1 (which stage each tau gates is not stated in the text). [src 3.3]
- Java perf stage is part of the per-candidate cascade ("performance tests"), but the paper only describes the final speedup measurement as production traffic replayed in a sandbox; per-candidate use of that replay is [unk]. [src 3.3, 5.1]
- Which tests, how selected, full suite or subset: [unk] (not stated).
- Failed candidates go to a refinement agent that re-runs validation. [src 3.2]
- Authors call static analysis and LLM review "useful but incomplete proxies" for semantic equivalence. [src 6.2]

## 4. Performance measurement per candidate
- Speedup = ratio of baseline to optimized mean execution time, "measured by performance tests" using real production traffic replayed in a sandbox; no repeat count, CI or test stated. [src 5.1]
- Repeats, CI, variance, warm-up for Java: [unk]. Ablations report mean +/- std over "multiple runs", count not given. [src 4]
- JFR selects targets; it is not explicitly a per-candidate check. [src 3.1.2]

## 5. Cost per candidate
[unk] no tokens, spend or time; only iteration counts (20 for the Apex ablation).

## 6. Iteration / cumulative re-validation
- Only candidates passing evaluation enter the population ("validation-first"); periodic checkpoints. [src 1.2, Alg. 3]
- No cumulative re-test of several accepted edits is described. [inf]

## 7. Limitations the authors state
Evaluator-quality dependence (static and LLM review are incomplete proxies for semantic equivalence; stronger semantic checks and workload-aware dynamic profiling needed); scaling to very large codebases / dependency context. [src 6.2] Observation (not a stated limitation): simple pattern substitutions match single-pass generation, so evolution overhead is not always justified [src 5.3]; 7-function scope is [inf] from the setup, not stated as a limitation.

## 8. Relevance to Study 1
- The claimed "per-candidate build + unit tests + perf" is confirmed only as a staged filter; the details Study 1 cares about (test selection, incremental build, repeats) are absent. [src]
- Cascade early-exit resembles OpenEvolve (see openevolve.md). [inf]
- Closed enterprise codebase; not reproducible. [src]

## Sources
- arxiv.org/html/2605.04677 (Sec. 1.2, 3.1-3.4, 4, 5.1, 5.3, 6.2, App. C, Alg. 3-4; via summarising fetch)
