# Evaluation Protocol

## Data firewall

- Maintain event time, public-release time, ingestion time, and revision time separately.
- Reconstruct universe membership for every date; include delisted securities and delisting outcomes where available.
- Use original filing publication times and macro release vintages.
- Delay ambiguous or after-market news to the next eligible decision session.
- Fit every imputer, scaler, feature selector, calibrator, regime model, and hyperparameter search only on permitted past data.
- Mask company identifiers and calendar dates in LLM-dependent tests.

## Walk-forward structure

The precise dates will be selected after data-coverage assessment. The protocol must include:

1. historical training window;
2. separate validation window for model/hyperparameter selection;
3. separate calibration window for probability or interval calibration;
4. purge and embargo at least as long as the forecast horizon;
5. frozen test window with a predeclared online-update policy; and
6. final untouched prospective shadow period.

The outcome of a five-day forecast cannot update reliability memory until those five days have elapsed. Online updates inside a test window must be specified before the window is opened and replayed exactly.

## Minimum baselines

1. Buy-and-hold benchmark.
2. Equal-weight stock portfolio.
3. Simple momentum/factor strategy.
4. Each specialist independently.
5. Equal-weight forecast ensemble.
6. Fixed optimized stacking ensemble.
7. Deterministic volatility gate.
8. Deterministic disagreement/data-quality gate.
9. Conventional supervised mixture-of-experts.
10. AlphaMix-style uncertainty-aware router.
11. Contextual bandit with identical state/actions.
12. Proposed controller without abstention.
13. Proposed controller without reliability memory.
14. Random routing and random abstention at matched coverage.
15. Hindsight oracle router, clearly labelled as unattainable.

## Required ablations

- remove regime belief;
- replace learned regime belief with volatility buckets;
- remove delayed reliability memory;
- remove disagreement;
- remove evidence provenance/quality;
- remove abstention;
- replace calibrated abstention with a raw confidence threshold;
- remove expected costs from controller state;
- remove factor-exposure constraints;
- remove or replace any LLM;
- mask ticker/company/date/event identity;
- shuffle controller actions while preserving their frequency; and
- replace specialist families without changing the controller interface.

## Metrics

### Forecast and ranking

- daily cross-sectional Spearman rank IC;
- IC information ratio;
- balanced accuracy and MCC for direction;
- Brier score or negative log-likelihood;
- MAE or quantile loss if magnitude is modelled.

### Calibration and selection

- empirical interval or set coverage;
- interval width or set size;
- expected calibration error;
- selective risk at fixed coverage;
- risk–coverage curve and area under the curve;
- abstention by regime, transition status, sector, liquidity, and volatility;
- instance-level and strategy-level false-deployment rates.

### Economic outcomes

- gross and net return under multiple cost assumptions;
- Sharpe, Sortino, Calmar, maximum drawdown, and turnover;
- cash exposure and effective market exposure;
- liquidity/capacity stress;
- market, sector, size, value, momentum, quality, and volatility attribution;
- residual stock-selection alpha with time-dependence-aware intervals.

### Controller behaviour

- regret relative to the best hindsight expert;
- routing stability and switch frequency;
- specialist utilization and concentration;
- evidence-acquisition frequency, latency, and cost;
- fallback and failure rates;
- sensitivity to model/provider changes.

## Statistical safeguards

- Use time-series-aware resampling or HAC inference rather than treating stock-days as independent.
- Report effect sizes and uncertainty, not only p-values.
- Control repeated strategy selection and disclose the complete experiment registry.
- Investigate White's Reality Check, Hansen's SPA, Probability of Backtest Overfitting, and Deflated Sharpe Ratio as finance-specific supplements.
- Report all prespecified primary outcomes, including null and negative findings.
- Separate exploratory analyses from confirmatory tests.

## Forward evaluation

Before prospective shadow trading begins:

- freeze the architecture, primary metrics, allowed updates, costs, and decision schedule;
- timestamp and archive the protocol;
- log every prediction and abstention before outcomes occur;
- prohibit retroactive deletion or replacement of predictions; and
- define operational failure and stopping rules.

