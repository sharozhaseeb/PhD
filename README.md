# PhD Research Workspace

This repository stores candidate PhD research directions and a local audit harness for testing their novelty, validity, feasibility, and reproducibility before implementation.

## Current direction

- [Reliable Agentic Stock Forecasting](research-directions/stock-selective-routing/README.md)

## Research audit harness

- [Harness documentation](research-audit-harness/README.md)
- Run the stock audit:

  ```powershell
  python research-audit-harness/scripts/audit.py research-directions/stock-selective-routing
  ```

The harness is deliberately local and uses only the Python standard library. It does not install or execute third-party agent skills.

