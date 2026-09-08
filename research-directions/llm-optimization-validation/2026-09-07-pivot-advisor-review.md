# Advisor-style review of the proposed empirical pivot

**Date:** 7 September 2026  
**Proposal reviewed:** Understanding and Detecting Workload Regressions in Iterative Python Code Optimization  
**Decision:** Approve a bounded feasibility study. Keep the thesis contribution provisional.

## 1. Assessment

The proposed pivot fits the student's Python and software engineering background and retains useful infrastructure from the master's project. However, moving from a new acceptance controller to studying regression mechanisms does not by itself resolve the novelty problem. The revised topic describes a worthwhile area; it does not yet establish a distinctive PhD contribution.

The strongest route is a focused empirical study that distinguishes measurement artifacts, workload-specific trade-offs, and interactions between successive edits, followed by an intervention justified by those findings. A generic failure taxonomy or another generate-test-profile loop would be weak.

This is an advisor-style assessment of our own proposal, not an independent university review. It extends the earlier [review](./2026-09-07-advisor-review.md), [methods map](./2026-09-07-methods-map.md), and [benchmark plan](./2026-09-07-benchmark-plan.md). The search used primary papers, author/conference pages, and public repository documentation. It covered direct LLM optimization work and adjacent performance evolution, fuzzing, diagnosis, and iterative coding research. It is targeted literature scoping, not an exhaustive systematic review. No reported results were experimentally reproduced.

## 2. What the additional literature changes

PerfAgent is a particularly close July 2026 preprint. It describes profiler feedback, iterative validation, and retaining the fastest test-passing patch. Its threats-to-validity discussion explicitly identifies workload generalization and Python-only coverage of native-extension changes as limitations. We inspected the method and limitations; this search did not locate a verified author release of the complete implementation. [Paper, Sections III and VI](https://arxiv.org/html/2607.19653v1)

The earlier recommendation placed too much weight on iteration as a differentiator. The contribution must come from a specific unanswered question and convincing evidence. Adding more rounds, tracking each version, or keeping the best patch is insufficient.

The older literature is also essential. Perun links performance profiles to code versions, detects degradation, models performance, and generates stressing inputs. APOLLO combines regression-oriented SQL generation, input reduction, and diagnosis. These are strong precedents for the infrastructure and diagnosis ideas, even though they do not directly implement our proposed Python-agent study. [Perun](https://github.com/Perfexionists/perun), [APOLLO](https://github.com/sslab-gatech/apollo)

## 3. Implemented methods and their implications

Availability categories below distinguish an inspected public artifact from an implementation described in a paper. Neither category means reproduction has succeeded on the student's machine.

| Work | Method already implemented or reported | Evidence inspected | Consequence for novelty |
|---|---|---|---|
| Codeflash | Candidate generation, behavioral checks, and benchmarking | Product documentation; selected source inspected in the preceding review | A complete optimization/testing pipeline has close industrial precedent. |
| PerfCodeGen | Iterative refinement from correctness and runtime execution feedback | Research paper | Execution feedback is established. |
| FormulaCode | Repository optimization benchmark with many workloads, correctness checks, and performance trade-off analysis | Paper and project page; project identifies ICML 2026 acceptance | Multiple-workload evaluation is already a benchmark feature. |
| SWE-Pro | Parameter sweeps, runtime/memory metrics, adaptive timing, and noise-aware measurement | June 2026 preprint and public repository | Input-dependent evaluation plus reliable profiling is already implemented. |
| WEDGE / PERFFORGE | Synthesized performance conditions guide fuzzing toward expensive execution regions | NeurIPS 2025 paper; public release inspected | Performance-directed input generation is established. The inspected release contains test data and sampled synthesis artifacts; do not assume a complete runnable generator. |
| Rethinking Code Performance Benchmarks for LLMs | Re-evaluation of performance tests and a generate/diagnose/repair workflow | July 2026 preprint | Merely exposing weak performance tests is an existing research direction. |
| Perun | Version-linked profiling, degradation detection, modeling, and performance fuzzing | 2022 paper and public tool repository | A history-aware performance analysis pipeline is insufficient as a novel contribution. |
| APOLLO | Feedback-driven SQL fuzzing, regression-triggering query reduction, and diagnosis | PVLDB paper and public repository | Generating and shrinking performance regression examples already has substantial precedent. |
| Performance evolution of configurable systems | Performance-influence models and analysis across software releases and configurations | Empirical Software Engineering 2023 paper | Studying performance evolution and configuration-specific effects predates coding agents. |
| Workload impact on performance models | Studies how workload variation changes configuration effects; releases measurements and analysis artifacts | ICSE 2023 paper and artifact page | Workload sensitivity itself is not an unstudied phenomenon. |
| SlopCodeBench | Tracks code-quality changes as agents repeatedly extend their solutions | March 2026 preprint | Iterative degradation is already studied; its main outcomes concern structural quality and functionality, not our runtime-policy question. |
| Beyond Reproduction | Uses issue information and structured input mutations to explore latent performance regressions | ICPE Companion 2026 work-in-progress paper | LLM-guided, issue-aware regression input generation is also occupied territory. |

Sources for the rows not linked above: [Codeflash](https://docs.codeflash.ai/codeflash-concepts/how-codeflash-works), [PerfCodeGen](https://arxiv.org/abs/2412.03578), [FormulaCode](https://arxiv.org/html/2603.16011v1), [SWE-Pro](https://arxiv.org/html/2606.25530v1), [WEDGE](https://proceedings.neurips.cc/paper_files/paper/2025/hash/6a4d5d85f7a52f062d23d98d544a5578-Abstract-Conference.html), [PERFFORGE release](https://github.com/cirrus-uchicago/perfforge), [benchmark re-evaluation](https://arxiv.org/html/2607.07619v1), [performance evolution](https://link.springer.com/article/10.1007/s10664-023-10338-3), [workload study and artifact](https://conf.researchr.org/details/icse-2023/icse-2023-artifact-evaluation/24/Analyzing-the-Impact-of-Workloads-on-Modeling-the-Performance-of-Configurable-Softwar), [SlopCodeBench](https://arxiv.org/abs/2603.24755), [Beyond Reproduction](https://socs.uoguelph.ca/~lliao01/web-home/publications/Renmin_ICPE_2026.pdf).

If acceptance statistics remain part of the method, the earlier comparators still apply: [microbenchmark prioritization](https://link.springer.com/article/10.1007/s10664-021-10037-x), [irace](https://github.com/MLopez-Ibanez/irace), [μOpTime](https://arxiv.org/abs/2501.12878), [TT-MDE artifact](https://github.com/chenzongxiong/ASE-2026), and [sequential regression detection](https://arxiv.org/abs/2205.14762). Obtain the complete TT-MDE method before committing to a competing statistical claim.

## 4. The objections an examiner would raise

### Objection 1: A slowdown is not automatically a defective optimization

A patch may deliberately exchange a small slowdown on a rare input for a larger improvement on common inputs. Define the allowed input domain, workload weights, practical slowdown tolerance, and protected workload families before declaring a regression unacceptable. Distinguish a measured slowdown from an acceptance-policy violation.

### Objection 2: Repeated small losses can accumulate trivially

If every step permits a small slowdown relative to its immediate parent, cumulative slowdown relative to the starting version is expected. A checkpoint against the original baseline is an obvious safeguard. Demonstrating accumulation alone is not a substantial finding. The study must establish what remains after this safeguard.

### Objection 3: More rounds do not establish causation

Later rounds can involve different patch sizes, different code regions, or only the hardest surviving tasks. A correlation between round number and slowdown does not identify a mechanism. Record all attempted patches, their parent revisions, failures, and decisions. Confirm representative explanations through input sweeps and valid edit reversions or controlled alternatives.

### Objection 4: Single-target specialization is an expected outcome

If an optimizer is explicitly instructed to optimize only one input, poor performance elsewhere may simply reflect its objective. Give the optimizer the declared performance requirements. Separate legitimate specialization, inadequate validation, incorrect behavior, and deliberate benchmark-specific shortcuts. Do not rely on an LLM judge as the sole source of these labels.

### Objection 5: The LLM connection may be incidental

Include human performance patches and, where feasible, matched one-shot candidate generation. Determine whether the mechanism is specific to iterative agent feedback or is a broader optimization issue. A broader finding can still matter; avoid claiming LLM causation solely because an LLM produced the patches.

### Objection 6: Extra complexity may contribute nothing

A diverse fixed workload set plus fresh measurement and original-baseline checks may perform as well as a sophisticated method. This combination is a required comparator. Simpler conventional approaches succeeding should change the method proposal.

## 5. Candidate gaps, ranked for this student

These are hypotheses inferred from the inspected work. We have not established that they are absent from all research, or demonstrated them experimentally.

### A. Explain which validation failures persist during iterative optimization

**Question:** After controlling timing noise and applying sensible validation, which mechanisms cause target-workload improvements to violate requirements on other valid input families over successive edits?

**What we would contribute:** A reproducible corpus of optimization histories, independently assessed workload outcomes, and a mechanistic analysis that distinguishes timing artifacts, input specialization, cumulative tolerance effects, and edit interactions. Controlled experiments would determine which safeguards address each mechanism.

**Closest competition:** The workload benchmarks, the recent benchmark re-evaluation, performance-evolution studies, and iterative optimization systems in the methods table.

**Required differentiation:** Explain something beyond final-patch scores, generic poor coverage, or the arithmetic of accumulated tolerances. Show actionable findings across multiple projects and optimizer configurations.

**Assessment:** Best initial study; moderate fit and conditional publication potential. Merely listing failure categories is weak. An empirical study can be a substantive contribution without a new algorithm, but its findings must change what practitioners or researchers know.

### B. Select a small workload set that remains useful as optimizations change

**Question:** Under a fixed testing budget, can input characteristics and earlier regression evidence help select workloads that detect policy violations on future edits better than strong conventional selectors?

**Possible method:** Begin with contract-valid input families. Track which regions, such as size/cardinality combinations, expose different performance behavior. Select a small set using both diversity and relevance to the current change; retain some exploration capacity for regions not previously problematic. Measure all selected cases afresh rather than assuming cached timings remain valid.

**Closest competition:** Change-aware prioritization, structured parameter sweeps, historical-failure replay, and performance-directed fuzzing. Retaining failed tests is already standard practice.

**Required differentiation:** Beat both a static stratified suite and a strong combination of changed-code coverage plus failure replay at equal total cost, while retaining beneficial optimizations. Show that the history-dependent component adds value through an ablation. A novel name for combining familiar selectors is insufficient.

**Assessment:** Most suitable candidate method if study A reveals recurring input-dependent failures and excessive full-suite cost. This could use ordinary Python analysis and selection heuristics; foundation-model training is not required.

### C. Diagnose regressions involving interacting edits

**Question:** Can we efficiently produce a small valid reproducer and identify the relevant combination of edits when performance changes are non-monotonic across a history?

**Possible method:** Jointly simplify a triggering input and reduce a valid edit history, confirming that the measured slowdown persists. Preserve patch dependencies and recheck behavior after reduction.

**Closest competition:** Delta debugging, APOLLO's input reduction and diagnosis, and trajectory minimization. The July 2026 TRIM preprint minimizes coding-agent trajectories to remove unnecessary edits; it targets a different outcome but is relevant if our method reduces histories. [TRIM](https://arxiv.org/abs/2607.18161)

**Required differentiation:** Demonstrate useful interactions where ordinary first-bad-version localization or input reduction is insufficient, and show a measurable improvement over appropriate adaptations. A first regression is not necessarily the sole causal edit, especially under non-monotonic behavior.

**Assessment:** Higher implementation and novelty risk. Reserve for later if real interaction cases justify the work.

## 6. Recommended scope and research questions

Retain the existing provisional title rather than repeatedly renaming the project. Use the following questions to make its scope concrete:

- **RQ1:** How often do accepted optimizations violate a declared performance policy on independently assessed workloads, and how do those outcomes evolve across a session?
- **RQ2:** Which mechanisms explain the violations after controlling noise, workload requirements, and cumulative-baseline effects?
- **RQ3:** Which existing safeguards prevent them at acceptable cost, and does a focused new selector improve the trade-off?

Focus initially on Python-source changes to deterministic CPU-oriented operations in several repositories. Choose one or two common transformation families only after checking their frequency in the available data. Hold behavioral validation constant in the first method comparison. Python code can invoke native libraries; explicitly state whether native source edits are excluded and report the resulting coverage limits.

Do not promise universal correctness, robustness on arbitrary input distributions, or a formal error guarantee without the necessary assumptions and evidence.

## 7. Practical evaluation

Use FormulaCode-V as the primary starting point and suitable SWE-Pro tasks as a second source, with pinned releases and duplicate-task removal. The former has a 108-task validated subset; the latter has 102 instances across three repositories. Their curated human improvements do not by themselves provide an unbiased population of agent attempts. Keep rejected and invalid generated candidates too.

Record original revision, parent revision, code snapshot, optimizer configuration, visible feedback, selected workloads, raw timing measurements, behavioral results, and every accept/reject/defer decision. Distinguish provisional candidates from integration approvals and the final delivered patch.

Separate three kinds of evaluation data: measurements used during optimization, fresh confirmation measurements, and a final audit set that never drives method tuning. New repetitions on the same input do not test new input families. Use plausible documented input characteristics rather than constructing only adversarial extremes.

Compare at least:

1. The target-workload selection rule used by the chosen optimizer.
2. Fresh independent confirmation on that workload.
3. A static, stratified set spanning declared input families.
4. Change-aware test/workload selection.
5. Replay of previous regression-triggering inputs.
6. A strong combination of 3–5 with fresh measurements and original-baseline checks.
7. The proposed selector and an ablation that removes its use of history.

If new input generation is the claimed method, include an appropriate performance-fuzzing baseline, not just random examples. Some published methods operate on C/C++ or databases; label adaptations and report reproduction limits rather than claiming direct execution on Python.

Use frozen compatible candidate pools for paired policy comparisons. If a policy changes feedback, accepted parent versions, or future generated edits, replay alone cannot determine its end-to-end effects; perform a separate live comparison with matched generation budgets.

Report independently assessed policy violations, beneficial candidates retained, final improvement, deferrals, and full validation cost. Include selection overhead. Analyze variation by project and session; repeated timings within one task do not substitute for independent tasks. Explain representative mechanisms with verified examples and blinded/manual coding checks rather than model-generated explanations alone.

## 8. Six-week feasibility decision

The initial target is 20–30 tasks across several repositories and short histories of roughly 3–5 rounds. These are planning quantities, not a power calculation or a claim that all environments will reproduce easily. Start with one reproducible optimizer and add a second configuration before generalizing about agent behavior.

Weeks 1–2 should establish runnable tasks, workload contracts, reliable timing, and a small set of real examples. Weeks 3–4 should compare conventional safeguards and independently classify failures. Weeks 5–6 should test a minimal history-aware selector only if the observed mechanisms support it.

Continue if the pilot finds recurring, consequential failures beyond the obvious safeguards and enough diverse tasks to study them. The proposed method additionally needs a plausible reliability/cost advantage over the strong combined baseline. Predeclare the main-study effect threshold after feasibility work and before examining final evaluation outcomes.

Redirect if failures are predominantly invalid inputs, ordinary timing noise, explicitly permitted trade-offs, benchmark-specific hacks, or cumulative losses removed by an original-baseline check. Also redirect if full testing is already cheap enough that selection has little practical value. A negative result may inform a publication, but the existence of a negative result does not guarantee a publishable paper.

## 9. Publication and PhD judgment

The problem is relevant and the narrowed empirical study is feasible for this student with statistical guidance and reliable measurement infrastructure. Novelty remains unproven. Confidence is moderate for the potential of a rigorous empirical contribution and lower for a new-method claim until evidence exists. No numerical publication probability is justified.

The proposed thesis becomes credible when it offers a coherent chain: a consequential failure mechanism, evidence explaining it, and an effective response evaluated against strong alternatives. A collection of pipelines, benchmark scores, and renamed variants would remain vulnerable to the same criticism as the master's work.

Recommend study A now, method B conditionally, and C only if interaction cases emerge. This is one research program with evidence-based decision points, not three promised papers. Confirm departmental thesis expectations with the supervisor before treating the resulting paper plan as sufficient for graduation.
