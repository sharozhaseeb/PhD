# Layman Explanation

## The question

Imagine several specialists trying to forecast stocks:

- one studies recent prices and momentum;
- one studies company accounts and valuation;
- one studies news and company events; and
- one studies volatility and risk.

Each specialist may be useful in some situations and unreliable in others. The research question is:

> Can a small coordinator determine which specialist is currently trustworthy—and recognise when none is reliable enough to use?

The coordinator is the agent. It manages the forecasting process rather than directly guessing a stock price.

## What has already been done

Researchers have already developed:

- systems containing several forecasting models;
- uncertainty-aware expert routers;
- regime-based mixture-of-experts models;
- financial agents using multiple information sources;
- confidence-based refusal or abstention; and
- dynamic strategy weighting.

Therefore, “we combine several models using an agent” is not an adequate novelty claim.

Another problem is that an apparently profitable backtest may not demonstrate intelligence. The return may come from a rising market, momentum exposure, risky stocks, test-period selection, hidden future information, or repeated experimentation until one configuration wins.

## What we will do

Before acting, the proposed coordinator asks:

1. What market conditions are plausible now?
2. Which specialists have been reliable under comparable recent conditions?
3. Do their predictions agree?
4. Is the evidence complete, recent, and properly timestamped?
5. Is the expected opportunity large enough to exceed costs and a safety buffer?
6. Should the system select a specialist, combine approved specialists, request evidence, use a safe fallback, or abstain?

Abstention means: “There is not enough reliable evidence to justify a prediction or change in position.” The objective is not necessarily to issue more predictions. It is to reduce unjustified decisions while preserving useful coverage.

## What we will predict

The recommended starting task is not an exact future price. It is a five-trading-day cross-sectional ranking:

> Which stocks are more likely to outperform other stocks in the same universe after common market and style effects are considered?

## How we will know whether it works

The controller must be compared against the best individual specialist, equal-weight ensemble, fixed optimized ensemble, deterministic volatility and disagreement rules, ordinary mixture-of-experts, an AlphaMix-style router, and a contextual bandit receiving exactly the same information and compute.

We then ask whether any improvement remains after fees, spread, slippage, turnover, and market/style attribution. If the agent loses to a simpler gate, that is a valid and potentially publishable result.

## One-sentence summary

> We are not building an agent that claims to predict the stock market directly; we are testing whether a cautious controller can determine which forecasting model is trustworthy, when it should refuse to act, and whether any resulting performance reflects genuine stock-selection ability rather than luck or market exposure.

