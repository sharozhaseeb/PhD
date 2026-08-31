# Reliable Agentic Stock Forecasting

## Working title

**Attribution-Constrained Online Selective Routing under Latent Regime Shift and Delayed Feedback**

## Status

- Stage: pre-proposal / advisor discussion
- Literature boundary last checked: 31 August 2026
- Novelty status: candidate, not established
- Intended use: academic research and paper trading only
- Primary artifact owner: PhD researcher

## One-paragraph summary

This research studies whether a small, auditable controller can decide which of several replaceable stock-forecasting specialists should be trusted at a particular time, request additional evidence when useful, or abstain when evidence is unreliable. The controller does not directly invent price predictions. It operates under uncertain market regimes and delayed outcome feedback. Its success must survive point-in-time evaluation, equal-information non-agent baselines, transaction costs, calibration tests, and attribution that separates genuine stock-selection value from market, sector, and style exposure.

## Documents

1. [Advisor briefing](00-advisor-briefing.md)
2. [Layman explanation](01-layman-explanation.md)
3. [Research proposal](02-research-proposal.md)
4. [Literature and novelty map](03-literature-novelty-map.md)
5. [Architecture and methodology](04-architecture-methodology.md)
6. [Advisor questions and failure criteria](05-advisor-questions.md)
7. [Evaluation protocol](06-evaluation-protocol.md)
8. [Three-year plan](07-three-year-plan.md)
9. [Figures](figures/README.md)
10. [Audit data](audit/README.md)

## Central research question

> Can an online controller choose among frozen heterogeneous stock forecasters—or abstain—while maintaining verifiable selective-risk constraints and producing net stock-selection value after transaction costs and factor attribution, when market regimes are latent and outcomes arrive only after the forecast horizon?

## Candidate novelty

The candidate contribution is not the use of multiple models, agents, regime routing, or abstention individually. Those elements already have close precedents. The defensible problem combines:

- latent rather than retrospective regime information;
- delayed outcome feedback;
- constrained actions: select, combine, acquire evidence, safe fallback, or abstain;
- selective-risk control under temporal shift;
- rewards and evaluation based on net residual stock-selection value;
- hostile leakage, masking, attribution, and prospective tests; and
- equal-information comparison with deterministic and learned non-agent controllers.

A theory-bearing extension would attempt to establish a time-uniform selective-error or routing-regret result under explicit assumptions about regime drift and feedback delay. This remains a research objective, not a current claim.

## Scope boundary

The feasible initial study uses one point-in-time stock universe, one five-trading-day horizon, daily or weekly decisions, three or four genuinely different specialists, and paper execution. Exact-price prediction, high-frequency trading, real-money deployment, global markets, and unrestricted multi-agent debate are outside the initial scope.
