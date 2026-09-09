# Evaluation protocol

**Status:** planned; no results. Pilot quantities are provisional. Main-study thresholds, sample size, and final analysis choices must be frozen before final evaluation results become visible.

## Units and requirements

A task identifies a pinned repository state and valid workload domain. A session contains candidate attempts with explicit parent relationships. Distinguish an attempted candidate, a provisional incumbent, an integration approval, and the final delivered patch.

For workload `w`, the normalized runtime is the candidate runtime divided by the original baseline runtime under the same measurement design. Define the aggregation weights and protected workload families before judging a patch. A parent comparison can help diagnosis, but approval must also check the original baseline to detect accumulated losses.

An illustrative requirement is a 5% reduction in a weighted normalized runtime metric while no protected workload slows by more than 5%. These values are examples only; they are not configured experimental thresholds. Insufficient evidence produces defer. A larger independent evaluation can also return unresolved rather than forcing a binary ground-truth label.

## Data and sampling

Start with 20–30 feasible tasks across several repositories and roughly 3–5 rounds per pilot session. These are workload estimates, not power calculations. Pin datasets and source revisions, deduplicate overlapping pull requests, record exclusions, and retain rejected/invalid attempts. Include unchanged-code A/A controls and genuine human optimizations. Report synthetic faults separately from natural agent failures.

Use documented input families such as size, cardinality, shape, or ordering where valid for the target API. Separate contract-valid data from invalid cases. Native source edits are initially excluded; native library calls from Python remain possible and must be recorded.

## Comparators

| ID | Policy | Purpose |
|---|---|---|
| B01 | Target-workload selection | Characterize the starting optimizer's decision rule |
| B02 | Target workload plus fresh independent confirmation | Test whether ordinary confirmation resolves measurement artifacts |
| B03 | Fixed stratified workload suite | Strong simple input-diversity baseline |
| B04 | Change-aware selection | Established relevance-based selection baseline |
| B05 | Replay earlier regression inputs | Established history baseline |
| B06 | Combined B03–B05 with fresh measurements and original-baseline checks | Main conventional comparator |
| P01 | Candidate selector using input regions and regression history | Conditional method; implement only if pilot evidence supports it |
| A01 | P01 with history removed | Isolate history's contribution |

Keep the correctness gate, declared requirements, measurement runner, and budget accounting shared in the paired experiment. Include an appropriate performance-fuzzing adaptation if new input generation becomes the claimed contribution. Document which published methods were run directly, adapted, or unavailable.

## Measurement controls

- Separate setup/reset and coverage collection from the timed operation; verify repeatable input state.
- Warm up as appropriate, alternate/randomize baseline and candidate order, and repeat across fresh processes and independent measurement sessions.
- Record raw measurements, environment versions, failures, and timeouts. Containerization alone does not eliminate hardware noise.
- Account for calibration, selection, profiling, input generation, and confirmation overhead. Report both wall time and compute/model costs where relevant.
- Freeze a candidate for confirmation. Retrying confirmation is another decision opportunity; do not reset statistical accounting silently.
- Use appropriate inference for the sampling/stopping design. An ordinary interval repeatedly inspected during selection does not automatically provide a session-wide guarantee.

## Splits and leakage controls

Keep method-development repositories/tasks separate from final evaluation where feasible. Record all method changes and experiment families. The final audit workload set and measurements must not drive the optimizer or selector tuning. Expert patches are evaluation references, not inputs to the optimizer.

Fresh repetitions on known workloads address timing uncertainty. Independent input families address workload generalization. These are different tests. The `forward_test` experiment family in this package means a protocol-frozen evaluation on untouched tasks/workloads; it does not claim a finance-style future calendar test or completed deployment.

In the offline comparison, use compatible frozen candidates and reveal measurements according to each policy. In a live comparison, preserve the actual policy-dependent history and match generation budgets. Do not substitute a single recorded trajectory for every possible policy's future edits.

## Outcomes

| Outcome | Interpretation |
|---|---|
| Session policy violations | Sessions with at least one mistaken integration approval; report final delivery separately |
| Harm among approvals | Violating approvals divided by approvals; undefined if nothing is approved |
| Useful improvements retained | Beneficial available candidates accepted or beneficial final patches delivered |
| Final runtime benefit | Independent measurement relative to the original version and by workload family |
| Deferrals | Evidence-insufficient cases, reported separately from rejections |
| Validation cost | Full cost including selection and confirmation overhead |

A useful result reduces cost at comparable violation and useful-acceptance rates, or reduces violations at comparable cost and useful acceptance. Report trade-offs across budgets. Rejecting everything cannot win.

Analyze uncertainty at session/task/project levels and report heterogeneity. Timing repetitions from one task are correlated observations, not independent software tasks. Choose main-study sample size using pilot variability and costs; a small pilot cannot certify rare-error guarantees.

## Mechanism checks and negative results

Use independent timing, parameter sweeps, valid edit reversions, and controlled alternatives to verify explanations. Separate permitted specialization, noise, behavioral faults, cumulative tolerance effects, and edit interactions. Use explicit annotation rules and a second reviewer for representative classifications where feasible; an LLM explanation is not causal evidence.

Redirect the method if B06 removes the practical problem or if P01's apparent benefit disappears after charging overhead and preserving useful acceptance. Report negative evidence honestly. A negative result does not automatically establish novelty or publication value.

## Audit profile mapping

All eight `software_performance` flags in [project.json](audit/project.json) declare required controls: valid inputs, original-baseline checks, behavioral validation, noise control, protected final evaluation, fair comparisons, full cost accounting, and a negative-result path. Their value `true` is a protocol commitment. It does not assert implementation, successful testing, or advisor approval.
