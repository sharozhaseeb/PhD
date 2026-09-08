# PhD Research Workspace

This repository stores candidate PhD research directions and a local audit harness for testing their novelty, validity, feasibility, and reproducibility before implementation.

## Research directions

- [Daily-feedback-assisted financial forecast calibration](research-directions/stock-feedback-calibration/README.md) — current refined candidate; pre-pilot, novelty unresolved.
- [Reliable Agentic Stock Forecasting](research-directions/stock-selective-routing/README.md) — earlier broader proposal.
- [Cross-domain feasibility review](research-directions/2026-09-05-direction-review.md)

## Research audit harness

- [Harness documentation](research-audit-harness/README.md)
- Run the refined forecast audit:

  ```powershell
  python research-audit-harness/scripts/audit.py research-directions/stock-feedback-calibration
  ```

- Run the stock audit:

  ```powershell
  python research-audit-harness/scripts/audit.py research-directions/stock-selective-routing
  ```

The harness is deliberately local and uses only the Python standard library. It does not install or execute third-party agent skills.

