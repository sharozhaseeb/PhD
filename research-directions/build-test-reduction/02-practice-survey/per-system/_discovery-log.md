# Discovery log (2026-11-21)

All WebSearch calls used mode standard. Pages read via WebFetch (summarising model): details are second-hand; line numbers approximate.

## Queries run
1. EffiBench-X multi-language benchmark efficiency LLM generated code sandbox arxiv
2. KernelBench evaluation correctness timing CUDA kernels github
3. SysLLMatic LLM agent system-level software performance optimization profiling arxiv
4. OpenEvolve evaluator cascade evaluation github
5. repository-level performance optimization benchmark LLM agents 2025 regression tests per patch speedup
6. FormulaCode benchmark agentic optimization real-world codebases arxiv 2603.16011
7. COFFE benchmark time efficiency code generation CPU instruction count
8. PerfCodeGen execution feedback LLM code efficiency unit tests runtime
9. SBLLM search-based LLM code optimization evolutionary search github
10. ShinkaEvolve github evaluate.py novelty rejection sampling
11. LLM code optimization agent regression test selection coverage-based only run affected tests speedup validation 2025
12. RAPGen DeepPERF Microsoft performance improvement LLM C# artifact

Also fetched: GitHub API commit endpoints (SHA lookup) for KernelBench, OpenEvolve, Coffe, EffiBench-X, fc-eval, datasmith, sysllmatic; raw files listed in each note.

## Candidates and decisions
- FormulaCode: KEPT (repo-level, per-task Docker, ASV stats, public fc-eval/datasmith). Note: ASV core overlaps other researchers' asv coverage but harness is new. Appendix B.1 and the last 64k chars of the paper not read.
- KernelBench: KEPT (differential correctness + CUDA event timing, anti-cheat). Paper itself not fetched; only repo files.
- COFFE: KEPT (instruction-count measurement, offline stressful-test selection).
- OpenEvolve: KEPT (cascade evaluation = staged early-exit). Docs/config pages not fetched; only evaluator.py.
- SysLLMatic: KEPT (multi-file Java/C++, accumulated edits, RAPL/perf, coverage weakness evidence).
- EffiBench-X: KEPT (core-pinned Docker sandbox). Sandbox source not read.
- PerfCodeGen: DROPPED from notes. No public code link found in paper HTML (Python function level only). Facts seen: 12 runs trim min/max, slowest-test feedback, re-test every refinement (arXiv 2412.03578 Sec. 2-3, App. B.2); the paper has an internal inconsistency (10 vs 12 runs).
- SBLLM (2408.12159): DROPPED. No official repo found in search; function level.
- ShinkaEvolve: DROPPED. Search returned only paper/PyPI; evaluate.py is user-supplied like OpenEvolve; no validation novelty beyond OpenEvolve. Repo not opened.
- RAPGen / DeepPERF (Microsoft): DROPPED. No public artifact found in search; snippet-level only.
- PerfAgent (arXiv 2607.19653): already assigned to others. Search snippet only: it uses pytest-testmon to select tests affected by agent edits (coverage-based per-edit selection). NOT verified by me; flag for the PerfAgent researcher.
- TDAD (arXiv 2603.17973) and TestPrune (2510.18270): seen in search; coding/issue-resolution agents, not optimization; not read, dropped.
- SWE-Opt (NeurIPS 2026 submission, slides only): seen in search; 102 tasks pandas/sklearn/xarray; no paper/artifact read; dropped, mention as a lead.
- SWE-Perf, SWE-fficiency, GSO: already covered by others.
- PIE/Supersonic/EffiLearner/Performance-Aligned LLMs/KernelLLM/Mercury-like: not searched individually (time); unverified, not claimed.

## Per-edit test selection / cumulative re-validation found
- Per-edit selection: only the unverified PerfAgent/pytest-testmon snippet. None of the six kept systems does it.
- Cascade early-exit: OpenEvolve.
- Accumulated edits with final rebuild/measure: SysLLMatic.
- Final-state-only validation: FormulaCode (inferred).


## Late search (architect, 2026-11-21)
Queries run by the architect:
- (a) "LLM code optimization agent regression test selection per edit incremental build validation cost"
- (b) "performance benchmark selection for code changes LLM optimization agent which benchmarks to run per patch"
- (c) "iterative LLM code optimization cumulative validation accumulated edits periodic full test suite checkpoint"
- (d) "pytest-testmon OR test impact analysis software optimization agent SWE-bench performance arXiv 2026"

Hits and outcome:
- PerfAgent: already surveyed (perfagent.md).
- SysLLMatic: already surveyed (sysllmatic.md).
- TDAD 2603.17973 (test-impact graph for bug-fixing agents): belongs to W1 methods, not surveyed here.
- TestPrune 2510.18270: not surveyed here (issue-resolution agents, not optimization; see earlier entry).
- "Impact Is Not Invalidation" 2609.25130: arXiv ID resolves (Atul Anand, cs.CL). It concerns claim invalidation for coding-agent memory and compares against pytest-testmon (high recall, low precision). Not optimization; DROPPED from this survey.
- LLM4LLM 2608.21836: seen in search, not read; not surveyed.
- Phi-Bench 2609.10226: seen in search, not read; not surveyed.
- 2607.01211 "Are Performance-Optimization Benchmarks Reliably Measuring Coding Agents?": ID resolves to that title. KEPT (perf-bench-reliability.md): measured noise and cross-machine reference-patch validity for GSO, SWE-Perf, SWE-fficiency.
- 2607.07744 PERFOPT-Bench: ID resolves. KEPT (perfopt-bench.md): hidden tests, single-run speedup, shortcut audit; repo is an anonymous mirror, not opened.
- 2606.25530 SWE-Opt: ID resolves. KEPT (swe-opt.md): full paper and repo now exist; supersedes the earlier "slides only" lead.
- 2605.04677 CodeEvolve: ID resolves. KEPT (codeevolve.md) with caveat: staged build/test/perf/static/LLM filter confirmed, but test selection, repeats and build details are not given and no repo exists.
Note: the four papers were read through summarising WebFetch (not raw PDF); the critic should spot-check numbers.
Critic check (group E, 2026-11-21): all nine arXiv IDs resolve to the stated titles on arxiv.org/abs. Corrections/clarifications:
- The four KEPT papers were re-read in full (arXiv HTML). Dispositions stand, but note-level facts were fixed: PERFOPT-Bench has 12 tasks (7 is the number of agent stacks) and its anonymous mirror is now expired; SWE-Opt's "RCIW 0.1" is the sampling-stop rule, while acceptance uses a 20% noise ceiling, SNR>=2 and a 5% effect floor in code.
- TDAD 2603.17973 abstract: pre-change impact analysis giving the agent a code-to-test dependency map so it knows which tests to verify before committing a patch (SWE-bench Verified, regressions 6.08% to 1.82%). It is bug-fixing, not optimization, but it is directly a per-edit test-selection method; the "W1 methods" disposition is right and it should be read there, not dropped.
- TestPrune 2510.18270 ("Can Old Tests Do New Tricks for Resolving SWE Issues?"): reuses and minimizes the regression suite for reproduction and patch validation; issue resolution, not optimization. Disposition OK.
- "Impact Is Not Invalidation" 2609.25130: abstract confirms claim invalidation for agent memory and a pytest-testmon comparison (recall 0.868, precision 0.415). Disposition OK.
- LLM4LLM 2608.21836 and Phi-Bench 2609.10226: only titles checked (closed-loop kernel/deployment optimization; LLM-infrastructure engineering); neither was read, so the "not surveyed" status is unverified as to relevance.
