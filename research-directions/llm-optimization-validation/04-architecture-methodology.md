# Architecture and methodology

## Implementation boundary

The working software today is the local proposal audit CLI in `research-audit-harness`. The runtime study described here is planned and has not been implemented. Reuse suitable parsing, profiling, and execution infrastructure from the master's project only after checking its behavior and assumptions.

## Proposed components

| Component | Responsibility | Required output |
|---|---|---|
| Task registry | Pin repository revisions, environments, workload contracts, and inclusion criteria | Reproducible task manifest and exclusions |
| Candidate recorder | Save every attempt and the feedback that produced it | Immutable snapshots and parent relationships |
| Behavioral gate | Apply the same specified checks to all compared policies | Pass/fail details for returns, exceptions, mutations, and other specified behavior |
| Measurement runner | Execute valid workloads with controlled timing | Raw comparative observations and environment/session metadata |
| Workload policy | Choose which workloads to measure within its budget | Selected workload IDs, rationale/features, and overhead |
| Acceptance policy | Apply fixed improvement and regression requirements | Accept/reject/defer plus the evidence used |
| Independent assessor | Evaluate frozen outputs using protected audit data | Beneficial/harmful/unresolved labels and uncertainty |
| Analysis | Compare policies and verify failure mechanisms | Reproducible tables, plots, and case explanations |

## Proposed record contracts

These are design requirements, not existing file APIs.

- **Task:** task ID, source benchmark/revision, original code revision, environment manifest, valid input domain, workload weights, protected families, and exclusions.
- **Candidate:** candidate ID, session ID, parent candidate/revision, complete patch or snapshot, generator configuration, visible feedback, and generation cost. Record failed attempts too.
- **Workload:** workload ID, input family and parameters, contract-validation result, construction seed, setup/reset procedure, and timing boundary.
- **Measurement:** candidate and workload IDs, environment/run/process IDs, baseline identity, execution order, warmup settings, raw times, and failure/timeout status.
- **Decision:** policy version, available budget, consumed evidence, requirement thresholds, decision, confirmation attempt, and timestamp.

Store source inputs separately from derived summaries so analysis can be reproduced. Record provenance for generated tests. Treat source code and generated programs as experimental inputs and execute them in isolated task environments with explicit resource limits.

## Two experimental modes

**Paired policy comparison:** use frozen, compatible candidate pools to isolate the effects of validation policies. Reveal only evidence selected by each policy. Avoid reusing future observations as if they had been available earlier.

**Live optimization:** let each policy affect future feedback and candidate generation, using matched generation budgets. This is necessary when different decisions produce different parent versions or future patches. Offline replay cannot establish those counterfactual trajectories.

## Evidence separation

Maintain development data, optimization feedback, fresh confirmation observations, and a final protected audit set. A workload used to tune the selector becomes development evidence. A fresh timing sample on that workload does not turn it into an unseen input family.

See the [workflow diagram](figures/study-workflow.mmd), [evidence diagram](figures/evidence-separation.mmd), and [evaluation protocol](06-evaluation-protocol.md).
