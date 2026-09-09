# Advisor decisions and open questions

This is a decision register for discussion. It does not require approval to inspect literature, document the proposal, or run the local structural audit. Main-study claims require these choices to be resolved and recorded before the corresponding evidence is examined.

| Decision | Current position | Evidence or agreement needed |
|---|---|---|
| Thesis contribution | Empirical study first; new selector conditional | Departmental expectations for a two-year thesis and acceptable contribution scope |
| Performance objective | Runtime under a declared workload policy | Workload weights, minimum useful improvement, protected-family slowdown tolerance |
| Initial tasks | FormulaCode-V plus suitable SWE-Pro instances | Runnable environments, valid inputs, overlap/exclusion audit, and manageable cost |
| Optimization families | One or two frequent families, not yet chosen | Counts from the feasible task pool; avoid choosing only easy positive examples |
| Generator | One configuration for the first pilot | Reproducibility, API/local access, budget, and second configuration for generalization |
| Statistical design | Independent sessions and clustered analysis | Advisor/statistical review of estimand, uncertainty, stopping, and sample size |
| Input coverage | Defined families and documented contracts | Evidence that chosen inputs are plausible and cover the claimed application domain |
| Novelty | Unresolved | Complete closest-method review, citation screening, and an explicit contribution comparison |
| Continue/redirect rule | Important failures must survive strong safeguards | Practical effect threshold chosen after feasibility work and before final evaluation |

The main objections to resolve are whether observed slowdowns are permitted trade-offs, whether an original-baseline check solves accumulation, whether fixed diverse testing is already cheap, and whether any effect is specific to iterative feedback.

Prioritize exact method comparisons over title changes. Do not infer that a structural PASS means any of these decisions has been approved. Publication acceptance cannot be estimated credibly from the current documentation alone.
