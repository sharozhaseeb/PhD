# Advisor Questions and Failure Criteria

## Questions requiring answers before proposal approval

### Scientific target

- What exactly is predicted: direction, residual return, rank, volatility, or action?
- What is the forecast horizon and decision frequency?
- Is the primary contribution predictive, methodological, theoretical, economic, or evaluative?
- What is the single falsifiable central hypothesis?
- What evidence would cause us to abandon or materially reframe the idea?

### Agent necessity

- What meaningful sequential action can the agent take that a gating network cannot?
- Why is memory necessary, and what is permitted to enter it?
- Is additional evidence acquisition useful after its latency and monetary cost?
- Will the agent and every baseline receive identical information and comparable tuning/compute?
- Does the thesis remain publishable if a deterministic gate or contextual bandit wins?

### Regime and uncertainty

- How is regime belief estimated using only contemporaneously available information?
- Are regimes states, continuous conditions, or merely analyst labels?
- How will regime uncertainty be represented?
- Does abstention simply avoid high-volatility periods?
- Does calibration remain meaningful under temporal dependence and shift?

### Data feasibility

- Can the chosen universe be reconstructed point-in-time?
- Are delisted firms and delisting returns available?
- Are corporate actions and historical constituent changes handled correctly?
- Are fundamentals stored by original publication and revision timestamp?
- Are macro vintages and reliable news timestamps available?
- Can the dataset be legally used, retained, and described in publications?
- Can the data source be afforded and maintained throughout the PhD?

### Economic validity

- What cost, spread, slippage, liquidity, and capacity assumptions are defensible?
- Will performance be decomposed into market, sector, size, value, momentum, volatility, and residual stock-selection components?
- What prevents an abstaining strategy from appearing safer simply because it holds more cash?
- Is prediction improvement economically material after costs?

### Evaluation and statistics

- What are the training, calibration, embargo, validation, and frozen test windows?
- How are overlapping five-day labels purged or handled statistically?
- How many model, universe, feature, cost, and window variants will be tried?
- How will selection and multiplicity be controlled?
- Which block-bootstrap, HAC, reality-check, SPA, PBO, or deflated-Sharpe procedures are appropriate?
- Is there an untouched prospective shadow-trading period?
- What second universe or market tests external validity?

## Thesis-killing loopholes

The direction must be stopped or reframed if:

- the “agent” has no meaningful sequential action;
- point-in-time, survivorship-aware data cannot be obtained;
- regime labels depend on future information;
- the agent receives more information, tuning, or compute than baselines;
- performance requires extremely low coverage;
- gains disappear against a simple matched-coverage volatility gate;
- gains disappear after realistic costs or factor attribution;
- calibration collapses in unseen periods;
- specialists have nearly identical residual errors;
- results depend on LLM recognition of tickers, dates, or historical events;
- the effect is confined to one favourable period or universe; or
- the final holdout has been repeatedly inspected or reused.

## Claims we must not make

- guaranteed prediction accuracy;
- guaranteed profit;
- investment suitability;
- universal market-regime detection;
- distribution-free validity without stating assumptions;
- “the first” without a completed, reproducible novelty search; or
- causal benefit from predictive association alone.

