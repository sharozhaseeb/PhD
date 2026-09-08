# Advisor briefing: a smaller forecasting research question

## Proposed question

Can today's one-day forecasting errors help calibrate a newly issued five-day return interval before recent five-day outcomes mature, beyond what existing same-information methods already achieve?

## What the audit changed

- Replaced the broad agent-routing architecture with a small uncertainty-calibration experiment.
- Distinguished new five-day predictions from revisions to an older partially completed forecast.
- Made ordinary volatility scaling and a same-feature conditional scale model mandatory rivals.
- Made interval score primary so simply widening intervals cannot establish improvement.
- Specified immutable issue-time scales, label maturity, chronological splits, and overlap-aware inference.
- Kept novelty, data vintages, and statistical adequacy unresolved rather than treating completed forms as evidence.

## Decision

**Proceed to reproduction and an exploratory pilot; do not claim a novel method or commit the thesis yet.**

The most important experiment is whether the daily-signal policy beats a standard model given the same daily information. If it does not, retire the special-mechanism claim. An observed failure of weak baselines is insufficient.

## Current audit

32 PASS, 5 WARN, 0 FAIL. This is structural completeness only. The five warning categories are unresolved novelty, close prior-work overlap, incomplete search counts, pending searches, and open critical risks. Six critical risks cover novelty, data vintages, statistical dependence, leakage, unsupported guarantees, and holdout reuse.

Nine closest works, four falsifiable hypotheses, nine planned experiments, and ten risks are recorded. No experiment has run and no holdout has been sealed.

The first study is a small equity-ETF pilot. Extending claims to individual stocks requires separate historical-universe and delisting controls. A provisional four-to-six-week schedule tests feasibility; it is not a publication estimate.

Start with [the plain-language explanation](01-layman-explanation.md), then [the proposal](02-research-proposal.md) and [evaluation protocol](06-evaluation-protocol.md).
