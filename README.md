# PhD Research Workspace

This repository stores candidate PhD research directions and a local audit harness for checking whether their documentation records evidence, comparisons, protocols, and unresolved risks before implementation.

## Course support guides

- [Applied Information Security — Lectures 1–3](courses/first%20sem/Applied%20information%20security/support.md)
- [Deep Learning — Lectures 1–5](courses/first%20sem/Deep%20Learning/support.md) — concise explanations, worked numerical videos, and optional longer lessons; [numerical practice with checked answers](courses/first%20sem/Deep%20Learning/numerical-practice.md).
- [Generative AI — Introduction, AE/VAE and GANs Parts 1–2](courses/first%20sem/genai/support.md) — short explanations, numerical video routes, optional depth, and assignment support; [numerical practice with checked answers](courses/first%20sem/genai/numerical-practice.md).

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

