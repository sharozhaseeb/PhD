# R3: Forward citations of PerfAgent and NameRTS; NameRTS artifact

Date of search: 2026-11-21. Fetched content treated as untrusted data. All abstracts read from arXiv `citation_abstract` metadata only, so every relevance label is [abstract-only].

## Query log

| # | Tool | Query | Date | Hits |
|---|------|-------|------|------|
| 1 | Semantic Scholar API | `/paper/arXiv:2607.19653/citations?fields=title,authors,year,venue,externalIds&limit=100` | 2026-11-21 | 7 citers |
| 2 | Semantic Scholar API | `/paper/arXiv:2605.25356/citations?...&limit=100` | 2026-11-21 | 1 citer |
| 3 | OpenAlex | `works?filter=title.search:PerfAgent` | 2026-11-21 | 2 (noisy, unrelated) |
| 4 | OpenAlex | `works?filter=title.search:Names Are All You Need` | 2026-11-21 | 17 (noisy, unrelated) |
| 5 | OpenAlex | `works/https://doi.org/10.48550/arXiv.2607.19653` | 2026-11-21 | W7170166335, cited_by_count 7 (matches S2) |
| 6 | OpenAlex | `works/https://doi.org/10.48550/arXiv.2605.25356` | 2026-11-21 | W7215057160, cited_by_count 1 (matches S2) |
| 7 | arXiv | abs/2605.25356, abs/2607.19653 | 2026-11-21 | both show only [v1] |
| 8 | arXiv | abs/2605.25356v2, abs/2607.19653v2 | 2026-11-21 | HTTP 404 both (no v2) |
| 9 | arXiv | html/2605.25356 (grep github/zenodo/figshare) | 2026-11-21 | github.com/ZJU-CTAG/NameRTS |
| 10 | arXiv | abs/<id> for 8 citers (abstract metadata) | 2026-11-21 | 8 abstracts |
| 11 | WebSearch | `"2607.19653" OR "PerfAgent: Profiler-Guided Iterative Refinement"` | 2026-11-21 | arXiv PDF + a third-party Codex CLI blog; no citers |
| 12 | WebSearch | `"Names Are All You Need" "Regression Test Selection for Python" NameRTS github` | 2026-11-21 | paper + aggregators; search did NOT surface the repo |
| 13 | WebSearch | `"2605.25356" NameRTS regression test selection Python Pradel Liu` | 2026-11-21 | paper + aggregators |
| 14 | GitHub REST API | repos/ZJU-CTAG/NameRTS, /commits, /contents; raw readme.md | 2026-11-21 | repo metadata, README |

Not done: authors' pages (software-lab.org, Zhongxin Liu) were not fetched separately; the paper's own HTML links the repo, which settles the artifact question. OpenAlex `cites:` filter was replaced by the per-work `cited_by_count` check (matches S2 counts) because title search was noisy; OpenAlex citer lists were not enumerated.

## Version check

- NameRTS 2605.25356: submitted 25 May 2026, v1 only (v2 URL 404). No changes to note.
- PerfAgent 2607.19653: submitted 22 Jul 2026, v1 only (v2 URL 404). No changes to note.

## Citing works: PerfAgent (2607.19653): 7 citers (S2 and OpenAlex counts agree)

| arXiv | Title | Authors (first 3) | Year | Relevance [abstract-only] |
|---|---|---|---|---|
| 2611.23203 | Identifying and Repairing Energy Smells with Agent Skills (Dr. Greens) | Mehditabar, Rajput, Sharma | 2026 | VALIDATION of optimization edits: Python energy-smell repair skill with "an independent verifier to confirm behavior preservation". No test selection/build reduction. Relevant. |
| 2610.25834 | FrontierRefactor: Benchmarking Multi-Scale Performance-Oriented Codebase Refactoring | S.-J. Wang, Meng, Chen | 2026 | Benchmark/validation: 60 tasks, behavior preservation via observable contract plus runtime regression. Relevant (benchmark of optimization edits). |
| 2610.17184 | DuoDiscover: Scaling Autonomous Discovery Beyond the Evaluation Bottleneck | Agarwal, Gupta, Heddes | 2026 | Evaluation-cost reduction: cheap proxy "yardstick" evaluators with fidelity tests vs true evaluation. Conceptually adjacent (cheap validation of candidate edits); not test selection. |
| 2604.05137 | EffiPair: Improving Efficiency of LLM-generated Code with Differential Execution Feedback | Hajizadeh, Jana | 2026 | Code-efficiency refinement via execution feedback; no test selection or acceptance gate beyond execution. Marginal. |
| 2606.12563 | Arbor: How Search Policy Shapes Agent Behavior in System Optimization | Prakriya, Hou, Gong | 2026 | Agent optimization of ML systems (kernels, etc.); not relevant to test/build reduction. |
| 2608.17007 | SkillEffect: Checked Lowering for Memory-Bounded Agent Tools | Y.-N. Wang, Shi | 2026 | Checker/postcondition validation of LLM-generated programs; different domain. Low. |
| 2608.22331 | Noise Floor Audit for Agent Benchmarks | Y.-H. Chen, Qian, Wang | 2026 | Benchmark measurement variability (BFCL); not about code optimization. Low. |

None of the 7 does regression test selection or build reduction.

## Citing works: NameRTS (2605.25356): 1 citer

| arXiv | Title | Authors (first 3) | Year | Relevance [abstract-only] |
|---|---|---|---|---|
| 2610.01967 | FastCI: Efficient GPU-Intensive CI for LLM Training Frameworks | Qiao, Zheng, Liu | 2026 | TEST SELECTION: uses runtime evidence to select affected tests, prune equivalent-context tests, prioritize risky tests, optimize test workloads. Directly relevant (but GPU/LLM-training frameworks, not Python-general RTS). |

None found validating LLM optimization edits with RTS.

## Task B: NameRTS artifact

**Found: https://github.com/ZJU-CTAG/NameRTS** (linked from the paper's arXiv HTML, https://arxiv.org/html/2605.25356; WebSearch alone did not surface it).

- Described in the README as the replication package for the paper. Description: "Fine-grained and safe regression test selection for Python via name-based dependency propagation."
- License: Apache-2.0.
- Created 2026-05-20; only two commits ("Initial commit", "init commit"), latest 2026-05-20T02:56:46Z, i.e. before the arXiv submission (25 May). No later updates visible. 2 stars at check time.
- Contents: `src/` (namebdp.py core, instrumentor, bytecode.py, checksum.py, import_collector.py, parser.py, evaluate.py, runall.py, a modified pytest-xdist-isolation, framework.py = EkstaP file-level baseline), `dataset/` (commit hashes), `ground truth/` (affected tests per commit), `results/` (rq1 to rq4), `build_env.md`, `environment_313.yml`, `environment_312.yml`, LICENSE.
- Python version: 3.13 for all projects except seaborn (3.12), via conda envs.
- Runnable on arbitrary pytest projects? NOT established. The README documents it as an evaluation/replication package: `evaluate.py` is the entry point for RQ1 to RQ4, and each evaluated project needs a dedicated, manually built test environment per `build_env.md`. It uses instrumentation plus a modified pytest-xdist. There is no documented CLI or pip package for applying it to a new repo. Treat reuse on other projects as requiring adaptation (not verified by running the code).
- No Zenodo or figshare DOI was found in the arXiv HTML. Authors' personal pages were not checked.
