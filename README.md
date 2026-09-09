# PhD Research Workspace

This repository stores candidate PhD research directions and a local audit harness for checking whether their documentation records evidence, comparisons, protocols, and unresolved risks before implementation.

## Research directions

- [Workload regressions in iterative Python optimization](research-directions/llm-optimization-validation/README.md) — current provisional direction; empirical study first, two-year plan, novelty unresolved.
- [Daily-feedback-assisted financial forecast calibration](research-directions/stock-feedback-calibration/README.md) — earlier finance candidate.
- [Reliable Agentic Stock Forecasting](research-directions/stock-selective-routing/README.md) — earlier broader finance proposal.
- [Cross-domain feasibility review](research-directions/2026-09-05-direction-review.md)

## Research audit harness

- [Harness documentation](research-audit-harness/README.md)
- [Harness schema and behavior reference](research-audit-harness/docs/reference.md)
- Run the Python optimization proposal audit:

  ```powershell
  python research-audit-harness/scripts/audit.py research-directions/llm-optimization-validation
  ```

- Run the refined forecast audit:

  ```powershell
  python research-audit-harness/scripts/audit.py research-directions/stock-feedback-calibration
  ```

- Run the stock audit:

  ```powershell
  python research-audit-harness/scripts/audit.py research-directions/stock-selective-routing
  ```

The harness is deliberately local and uses only the Python standard library. It does not install or execute third-party agent skills.

