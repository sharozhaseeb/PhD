# Benchmark and publication assessment

**Working title:** Reliable Acceptance Decisions During Iterative Python Code Optimization  
**Date:** 7 September 2026  
**Stage:** Literature-grounded proposal. No benchmark experiments or performance improvements have been demonstrated.

**Further review:** The [pivot advisor review](./2026-09-07-pivot-advisor-review.md) adds closer iterative-optimization and traditional performance-analysis work. Use it alongside this protocol when assessing novelty; the current proposal remains provisional.

## 1. Advisor's decision

Proceed with a six-week pilot. Confidence is moderate that this can support a useful empirical paper, and low-to-moderate that the proposed controller will supply a sufficiently novel methods contribution. The two-year PhD plan remains conditional on the pilot and the department's requirements. These are qualitative judgments, not calibrated probabilities of acceptance.

A pipeline alone is insufficient. The research needs to establish how acceptance policies behave over optimization histories, why particular failures occur, and whether an identifiable intervention improves the reliability/cost trade-off beyond strong existing methods.

This plan extends the earlier [advisor review](./2026-09-07-advisor-review.md) and [methods map](./2026-09-07-methods-map.md). An additional novelty threat is algorithm racing: allocating evaluations among competing candidates and dropping poor candidates early is established in automatic configuration. The irace authors provide an implementation and references to the 2016 method and 2017 adaptive-capping extension. [Author repository](https://github.com/MLopez-Ibanez/irace)

## 2. Distinguish the benchmark from the baseline

- **Benchmark:** tasks, candidate patches, workloads, measurement environments, and the evaluation protocol.
- **Baseline:** an existing decision method applied to that benchmark.
- **Our proposed improvement:** a decision policy that uses measurements more effectively while retaining useful optimizations and avoiding mistaken approvals.

There is no defensible single published percentage for us to beat. Different papers measure agent speedup, benchmark duration, regression discovery, or statistical stability. We must evaluate relevant policies under a common acceptance objective.

## 3. Data to reuse

| Resource | Verified existing contribution | Role in this project | Limitation to handle |
|---|---|---|---|
| FormulaCode / FormulaCode-V | The March 2026 paper reports 957 tasks across 70 scientific Python repositories and a manually validated 108-task subset used for evaluation. It includes numerous performance workloads and expert patches. | Primary source; start with reproducible tasks from FormulaCode-V. | V was selected from stronger-performing tasks. Do not treat it as representative of all Python services or all optimization attempts. |
| SWE-Pro | June 2026 preprint: 102 validated tasks from pandas, scikit-learn, and xarray; parameterized inputs and runtime/memory measurement. | Secondary evaluation for input-dependent behavior and measurement-policy comparison. | Only three repositories, with pandas dominant. Deduplicate overlapping PRs/tasks across datasets. |
| Existing small algorithm tasks | The master's tasks and small public code tasks can expose harness bugs cheaply. | Development and smoke checks. | They cannot alone substantiate claims about repository-scale Python optimization. |
| Recorded optimization histories | We will record candidates, parent revisions, available feedback, measurement actions, and decisions. | The study's session-level experimental data. | A benchmark's final patches do not automatically provide all intermediate states and timing observations. Audit released trajectories before deciding what must be collected. |

Sources: [FormulaCode paper, including Appendix B](https://arxiv.org/html/2603.16011v1), [SWE-Pro paper](https://arxiv.org/html/2606.25530v1), [SWE-Pro implementation](https://github.com/probench-swe/SWE-Pro).

Pin dataset revisions. FormulaCode's live website shows evolving counts; use a documented release rather than mixing live counts with the paper's evaluated subset. This review checked papers and public artifacts, but did not verify that their environments reproduce locally.

Both principal datasets originate in successful human optimizations. Add no-change controls and real unsuccessful LLM candidates so the evaluation is not dominated by easy positive examples. Controlled slowdowns and behavioral mutants are useful diagnostic additions; report them separately from naturally occurring failures.

## 4. Existing methods we must compare against

| Method family | What already exists | Fair comparison or adaptation |
|---|---|---|
| Generate, test, benchmark, select | PerfCodeGen uses execution feedback for iterative refinement. Codeflash implements an industrial optimization workflow. | Reuse a fixed generator for the validator experiment. An accessible, pinned complete tool can be an additional end-to-end comparator. A locally reimplemented documented policy must be labeled an adaptation. |
| Fixed measurement allocation | A straightforward repeated comparative benchmark over a declared workload suite. | Same paired measurement runner and total budget as other policies, with uniform or round-robin allocation. |
| Workload prioritization | Coverage-based and change-aware microbenchmark ordering have been studied. | Rank affected workloads first; collect coverage separately from timing and charge its cost. |
| Adaptive measurement | SWE-Pro uses calibration, warmup, confidence-interval-width stopping, and noise-aware validation across fresh containers. | Reproduce the relevant runtime procedure, including its noise handling, rather than comparing only against a fixed-repeat caricature. |
| Stability/detectability methods | μOpTime selects repetition configurations from historical stability. TT-MDE has a public detectability-oriented implementation and evaluation scripts. | Use applicable policies or documented Python adaptations. Check TT-MDE's full method before making a novelty claim; its inspected artifact evaluates Java/JMH projects. |
| Racing | irace and related methods allocate evaluation effort across competing configurations. | Treat patch candidates as alternatives and workloads as instances where appropriate; compare the racing component with the same candidate pool. Do not describe a fixed-pool adaptation as reproducing all of irace's search. |
| Sequential inference and fresh confirmation | Sequential regression testing already exists. Independently confirming the chosen patch is a strong conventional alternative. | Use a predeclared confirmation test; where approvals recur, account for the sequence of approval opportunities. |

Sources: [PerfCodeGen](https://arxiv.org/abs/2412.03578), [Codeflash workflow](https://docs.codeflash.ai/codeflash-concepts/how-codeflash-works), [Codeflash timing objective](https://docs.codeflash.ai/codeflash-concepts/benchmarking), [prioritization study](https://link.springer.com/article/10.1007/s10664-021-10037-x), [μOpTime](https://arxiv.org/abs/2501.12878), [TT-MDE artifact](https://github.com/chenzongxiong/ASE-2026), [sequential regression detection](https://arxiv.org/abs/2205.14762).

The most important comparator is a **constructed strong baseline**: sensible workload prioritization + an established adaptive timing policy + candidate elimination + fresh confirmation with an appropriate error policy. It is our composition of existing techniques, not a claim that one paper implements this exact combination.

For an initial experiment, implement fixed allocation, prioritization, one well-reproduced adaptive policy, racing, the strong composition, and the proposed policy. Expand the stopping-method comparison before a full methods submission. Choose parameters on development tasks, never retrospectively on the final evaluation tasks.

## 5. The research question and proposed intervention

**Question:** Under a fixed validation budget, can a controller make better accept/reject/defer decisions across an optimization session than strong existing policies?

Two workflows must be distinguished:

1. **One final approval:** search over many provisional candidates, then independently confirm one frozen selection. With suitable fresh evidence, selection among many candidates need not invalidate that single final test. This simple approach might solve most of the practical problem.
2. **Repeated approvals:** successive patches become accepted incumbents and influence later optimization. Repeated approval opportunities and accumulated regressions need explicit treatment. Preserve the parent graph and compare the final result with the original session baseline as well as relevant parent versions.

Evaluate these separately. Internal exploration is not an integration approval. Do not manufacture a session-level problem by counting every provisional candidate as a deployed patch.

The first proposed controller will:

1. Apply the same behavioral test gate as competitors.
2. Gather an initial, small but diverse set of paired runtime measurements.
3. Track which workload constraints remain unresolved for each eligible candidate.
4. Choose between measuring another workload, repeating a noisy comparison, discarding a weak candidate, or moving a frozen candidate to fresh confirmation. A transparent first heuristic can prioritize measurements likely to change a decision relative to their execution cost.
5. Reserve confirmation resources and return **defer** if evidence is insufficient.

The allocator is the component whose added value we must establish. Each individual action has prior art. Removing the allocator while retaining the same confirmation procedure is an essential ablation.

Start with deterministic CPU-oriented Python operations and runtime as the performance objective. Hold correctness testing constant initially; record behavioral violations separately. This keeps the first research question manageable. Memory optimization, distributed service behavior, and new LLM test generation can substantially broaden the work and are not needed for this first claim.

## 6. Define acceptance before measuring improvements

One illustrative policy is:

- Preserve the observable behavior covered by the specified tests.
- Reduce a declared weighted mean of normalized workload runtimes by at least 5%.
- Do not slow any designated protected workload by more than 5%.
- Return defer when the available evidence does not support a decision.

The 5% values are examples, not published standards or achieved results. Choose practical thresholds, workload weights, and the confidence target before the main evaluation. The weighted normalized metric is a declared benchmark objective; it is not automatically the latency of a deployed service.

Claim only what the evidence supports. Passing finite tests does not prove universal semantic equivalence. A timing confidence procedure does not establish behavior on untested input families. Fresh timing observations on known workloads address different uncertainty from previously unseen workloads.

For statistical approval claims, specify the estimand, sampling assumptions, stopping rule, and scope of error control. Valid repeated monitoring within one comparison does not automatically control selection across many approvals. Fresh confirmation also needs a policy if failed confirmations are repeatedly retried or new candidates are repeatedly certified. Treat such retries as additional opportunities, not a reset.

## 7. Experimental protocol

### A. Isolate acceptance-policy effects

Record candidate histories using a fixed optimizer configuration and freeze them for a paired comparison. Each policy sees only information its own measurement actions reveal. Store independent measurement streams for screening, confirmation, and retrospective assessment.

Replay is appropriate only when it does not invent counterfactual trajectories. Candidates generated from particular feedback or parent versions cannot be silently treated as if every policy would generate the same next patch. Use common-base candidate pools or replay compatible portions of a recorded history, and state this limitation.

### B. Test end-to-end consequences

Run a smaller live experiment in which each policy supplies feedback to the same optimizer. Match generation budgets and record actual costs. Different trajectories are expected here; this experiment measures the effect on the complete optimization process.

### C. Establish a stronger independent reference

Use higher-budget measurements over a broader, predeclared workload suite, with independent final audit data and behavioral checks. Label candidates beneficial, harmful, or unresolved relative to the stated policy. Do not force uncertain cases into binary ground truth or call this reference an equivalence oracle.

Randomize or alternate baseline/candidate execution order, repeat across fresh processes and measurement sessions, and validate warmup and input-reset behavior. Time critical code without coverage instrumentation. Include A/A comparisons of unchanged code. Assess robustness in a second environment if feasible; a Docker image alone does not eliminate hardware variability.

Split development and evaluation by repository where possible. Report project-level variation and clustered uncertainty. Hundreds of timing repetitions of one task are not hundreds of independent software tasks. Audit source-task overlap and keep expert answers away from the optimizer during generation.

## 8. What counts as improvement

| Measure | Definition and reason |
|---|---|
| Mistaken approvals | Report both performance-policy violations and observed behavioral failures; keep these categories separate. |
| Session error rate | Fraction of sessions containing at least one mistaken integration approval; also report the final delivered patch separately. |
| Harm among approvals | Harmful approvals divided by all approvals, with uncertainty. If nothing is approved, this rate is undefined, not proof of useful reliability. |
| Useful optimizations retained | Beneficial candidates accepted; for session-level delivery, whether a beneficial available candidate was delivered. Report rejection and deferral separately. |
| Validation cost | Wall time, CPU time, and any model cost, including calibration, prioritization, and final confirmation. |
| Delivered benefit | Independent runtime improvement of the delivered patch and its protected-workload regressions, relative to the original baseline. |

The desired result is lower validation cost at comparable reliability and useful-acceptance rate, or fewer mistaken approvals at comparable cost and useful-acceptance rate. Plot these trade-offs across budgets. Rejecting every candidate cannot win by reporting zero harmful approvals.

Predeclare a practically meaningful improvement and a tolerable loss in useful acceptance after feasibility work, before the main test. There is no universal percentage improvement that guarantees publication.

## 9. Six-week decision gate

| Period | Deliverable |
|---|---|
| Weeks 1–2 | Reproduce environments for an initial 20–30 tasks across several repositories; audit the closest methods; establish controlled timing and A/A checks. Reduce scope transparently if build costs are excessive. |
| Weeks 3–4 | Collect short optimization histories, implement the simple and strongest conventional policies, and inspect decision disagreements against independent measurements. |
| Weeks 5–6 | Test the proposed allocator, include a component-removal comparison, and assess whether any advantage survives on held-out tasks. |

Twenty to thirty tasks are a feasibility target, not a statistical power calculation. For perspective, even zero errors in 30 independent identically distributed sessions gives an exact one-sided 95% binomial upper bound of about 9.5%. Roughly 300 such error-free independent sessions are needed to get that bound below 1%. Real project clustering complicates this further. A small pilot cannot empirically certify a rare-error guarantee.

Continue if there is a reproducible, practically important decision problem and a plausible improvement beyond the strongest composition. Redirect the methods work if fresh confirmation and established racing/stopping policies resolve it at similar cost. A rigorous negative result can be scientifically useful, but publication still depends on novelty, scale, explanation, and venue fit.

## 10. Publication assessment and two-year scope

| Proposed output | Current judgment | Evidence needed |
|---|---|---|
| Another testing/optimization pipeline | Weak publication case | An engineering integration alone is unlikely to establish the proposed contribution. |
| Empirical study of decisions across realistic optimization histories | Moderate confidence | Meaningful new findings beyond known statistical pitfalls, strong baselines, varied projects, and a reproducible artifact. |
| New allocation/acceptance method | Low-to-moderate confidence before pilot | A distinctive mechanism and practical advantage over racing, adaptive timing, prioritization, and fresh confirmation together. |
| Completed PhD within two years | Plausible but conditional | Positive feasibility results, statistical guidance, affordable measurement infrastructure, and a contribution plan accepted by the supervisor/department. |

An additional July 2026 preprint already re-examines performance benchmarks and develops a performance-test generation workflow. Therefore, merely showing that weak performance tests miss differences is insufficient differentiation. [Rethinking Code Performance Benchmarks for LLMs](https://arxiv.org/html/2607.07619v1)

A feasible schedule is months 1–2 for the pilot, 3–7 for the empirical study, 8–14 for a justified method and evaluation, and 15–24 for replication, revisions, and thesis integration. This is a planning allocation, not a promise of publication turnaround. The method stage must be revised if the initial evidence does not justify it.

The main risks are novelty overlap, simple confirmation outperforming a complex policy, insufficient independent tasks for reliability claims, and costly environment reproduction. Python experience reduces implementation risk; the central research difficulty is experimental and statistical design. A precise numerical publication probability would be invented without a completed study, target venue, and review evidence.
