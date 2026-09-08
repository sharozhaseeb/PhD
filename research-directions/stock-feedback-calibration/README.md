# Financial forecast reliability before five-day outcomes mature

Working title: **Daily-feedback-assisted calibration of five-day return prediction intervals**.

Status: pre-pilot; novelty unestablished; no experiments executed. Literature screening date: 5 September 2026.

## Research question

Can a lightweight calibration policy use newly observed daily forecast errors to improve **newly issued** five-day return intervals during volatility transitions, beyond strong methods receiving the same information, without worsening the overall coverage-width tradeoff?

The first task is to find out whether an incremental problem remains after existing methods are implemented correctly. The proposal does not assume that a new algorithm is necessary.

Start with a small fixed set of equity-market ETFs as development instruments, subject to data and licensing checks. Generalization to individual stocks is a later study, not a current claim. Keep the five-day point forecaster fixed within each evaluation fold. Daily information changes the uncertainty layer. Do not revise previously issued intervals.

## Package

- [Advisor briefing and audit decision](00-advisor-briefing.md)
- [Plain-language explanation](01-layman-explanation.md)
- [Proposal and hypotheses](02-research-proposal.md)
- [Literature and novelty map](03-literature-novelty-map.md)
- [Method and information timing](04-architecture-methodology.md)
- [Decisions and stop criteria](05-advisor-questions.md)
- [Evaluation protocol](06-evaluation-protocol.md)
- [Conditional PhD plan](07-three-year-plan.md)
- [Audit interpretation](audit/README.md)
- [Generated audit](audit/generated-audit-report.md)

Run: `python research-audit-harness/scripts/audit.py research-directions/stock-feedback-calibration`

The older [agent-routing proposal](../stock-selective-routing/README.md) remains a separate, broader direction. The September [cross-domain review](../2026-09-05-direction-review.md) explored electricity reporting blackouts; that is not this financial pilot's mechanism.
