# PERFOPT-Bench

Status: critic-checked 2026-11-21 (6 fixes) · Last checked: 2026-11-21
Artifact: https://anonymous.4open.science/r/Dataset-D3CC (anonymous mirror linked from abstract; expired, no SHA [unk]) · Paper: arXiv 2607.07744 (Cui, Xie, Wang, Ma, Liu, Cao), "PERFOPT-Bench: Evaluating Coding Agents on Software Performance Optimization". Critic re-read the full arXiv HTML text (v1). Critic also tried the anonymous mirror API: it returned {"error":"repository_expired"} on 2026-11-21, so no artifact is available [unk].
Evidence labels: **[src]**, **[inf]**, **[unk]**.

## 1. What it is
Benchmark of 12 long-horizon C tasks (selected by an expert from ~28 calibrated candidates), each a correct but deliberately slow codebase; evaluated with 7 agent stacks (the earlier "7 tasks" was wrong: 7 is the number of stacks). Scoring = hidden correctness tests + verified speedup + trajectory audits. [src abstract, Sec. 3.1, App. A.4 Stage 3-4, B.6]

## 2. Build / environment
- C compiled with GCC/MSVC; each task has build.ps1 and test.ps1 (Windows) / test.sh (Linux/macOS); all evaluation on a single Intel Core i7 / Windows 11 machine (early May 2026). No container use described for evaluation. [src App. A (client versions para), B.3, B.6]
- Hidden evaluator compiles baseline and submission, checks correctness, "measures repeated speedup". [src A.2.1]
- In the agent loop the prompt tells the agent to run test.ps1 during optimization and again at the end; B.5 says test.sh checks both correctness and a predefined speedup threshold. Whether test.ps1 invokes build.ps1 is not stated [unk]. [src A.3.1, B.5]
- Build reduction: [unk].

## 3. Correctness tests per candidate
- Hidden correctness tests and hidden validation inputs; the agent-visible test.ps1/test.sh (correctness + threshold) runs in the loop, but the final scoring uses the hidden evaluator. [src 3.1, A.3.1, B.5]
- Final eval may swap the hidden benchmark and run randomized API semantic-equivalence tests. [src A.3.2]
- Fixed per task; not per-edit selection. [inf]

## 4. Performance measurement per candidate
- Metric: baseline runtime / submitted runtime, after hidden correctness. [src 3.1]
- Repeats, warm-ups, statistic, significance test: not specified ("repeated speedup"). [src A.2.1; unk]
- Noise control for agent evaluation: none described beyond a single machine. The GPU/NUMA-serial and cgroup-cpuset isolation sentence is in A.4 Stage 3 (difficulty calibration with a pilot solver during task construction), NOT the evaluation of the 7 stacks (earlier wording misattributed it). [src A.4 Stage 3]
- Candidate speedup threshold set from a private reference solver's run, then possibly raised during calibration ("raising the performance threshold"); expert only selects the 12 tasks. [src A.4 Stages 2-4]
- Each model-framework-task cell measured once ("single run"); results are "descriptive snapshots rather than statistically stable rankings"; variance and significance left to future work. [src 3.1, Limitations]
- Raw speedup gameable via benchmark-specific shortcuts. [src abstract]

## 5. Cost per candidate
[unk] no token or dollar figures; compute cost named as a risk (App. C).

## 6. Iteration / cumulative re-validation
- Relay pilot (Tasks 5 and 8, two stacks codex-gpt and cc-opus, 8 two-round sequences): a fresh session continues from the R1-modified workspace plus an optimization summary; R2 beat R1 in all 8 (1.02-2.48x). Exploratory, budget-confounded. [src 3.5, Table 5]
- No re-validation of accumulated edits beyond the final hidden evaluation. [inf]

## 7. Limitations the authors state
Hardware/compiler dependence; single run per cell; one expert for audits; non-exhaustive shortcut audit; exploratory, budget-confounded relay study. [src Limitations]

## 8. Relevance to Study 1
- Weak measurement rigor (single run), but evidence that gains can be shortcuts, so per-edit acceptance needs hidden or semantic checks. [src+inf]
- Multi-session relay is a cumulative-edit setting without cumulative re-validation. [inf]
- C + Windows build.ps1: different ecosystem from Python. [src]
- Artifact unavailable (anonymous mirror expired), so nothing is checkable in code. [src API response]

## Sources
- arxiv.org/html/2607.07744 (Sec. 3.1, 3.5, App. A.2-A.4, B.3-B.6, C; full text read by critic). Repo expired.
