# Literature and novelty map

Screening boundary: 5 September 2026. Focused primary-source review seeded from the conversation; not a completed systematic review. Missing search counts remain blank.

## Closest work

| ID | Source | Existing contribution | Required distinction |
|---|---|---|---|
| W01 | [Adaptive Conformal Predictions for Time Series (2022)](https://proceedings.mlr.press/v162/zaffran22a.html) | Aggregated adaptive calibration | Must beat adaptive aggregation |
| W02 | [Sequential Predictive Conformal Inference for Time Series (2023)](https://proceedings.mlr.press/v202/xu23r.html) | Residual dependence and conditional efficiency | Must exceed existing residual forecasting |
| W03 | [Market Implied Conformal Volatility Intervals (2023)](https://proceedings.mlr.press/v204/canete23a.html) | Financial volatility scaling and calibration | Five-day return target alone is not novelty |
| W04 | [Conformal Inference for Online Prediction with Arbitrary Distribution Shifts (2024)](https://jmlr.org/papers/v25/22-1218.html) | Drift adaptation including financial volatility | Same-information transition benefit untested |
| W05 | [Adaptive Conformal Inference for Multi-Step Ahead Time-Series Forecasting Online (2024)](https://proceedings.mlr.press/v230/hallberg-szabadvary24a.html) | Maturity-aware multi-step ACI | Horizon delay alone is not new |
| W06 | [Online conformal inference for multi-step time series forecasting (2026)](https://arxiv.org/html/2410.13115v2) | AcMCP and multi-step PID | Daily auxiliary signal must add beyond these |
| W07 | [Testing Marginal and Conditional Coverage in Conformal Prediction for Non-Stationary Time Series via Value-at-Risk Backtesting (2025)](https://proceedings.mlr.press/v266/retzlaff25a.html) | Formal coverage and interval-score evaluation | Specific mechanism rather than generic audit |
| W08 | [Heterogeneous-Horizon Conformal Ensembles for Online Prediction Under Distribution Shift: An Empirical Comparison with Strongly Adaptive Methods (2026)](https://www.mdpi.com/2571-9394/8/5/77) | Multiscale extreme-regime coverage-width tradeoff | Auxiliary feedback only a candidate difference |
| W09 | [Conformal PID Control for Time Series Prediction (2023)](https://papers.nips.cc/paper_files/paper/2023/hash/47f2fad8c1111d07f83c91be7870f8db-Abstract-Conference.html) | Quantile control and error prediction | Rapid error correction already available |

W06 is a February 2026 revised preprint, not a verified accepted journal article. W08 publisher text was accessible in prior search results; direct retrieval was intermittent. Baseline reproduction remains pending.

## Explicit future work versus our inference

Hallberg Szabadvary's [2024 conclusion](https://arxiv.org/html/2409.14792v1) suggests multi-step PID. W06 now includes it: that older suggestion is not a current novelty opportunity.

W06 identifies unknown future covariates and interval efficiency as further research. These are explicit author suggestions. They do not state that our daily-surprise mechanism is missing. We reserve the future-covariate question for a separate review.

Canete's [2023 Section 5.1](https://proceedings.mlr.press/v204/canete23a/canete23a.pdf) suggests stronger adaptive comparisons and other uncertainty signals and data. This establishes a historical agenda, not that later literature left it open.

Our inference: daily auxiliary errors might improve calibration of **newly issued** five-day cumulative-return intervals before enough recent five-day labels mature. Conditional volatility, SPCI, PID, AcMCP, and same-feature scale models may already capture this. Novelty remains unresolved.

## Gap test

For each closest implementation record target, issue/maturity times, daily inputs, residual model, normalization, partial-path usage, update timing, interval objective, assumptions, and code availability.

A different ETF dataset or horizon alone is weak novelty. If a published method expresses the candidate by changing covariates or scores, frame the work as application/evaluation unless a distinct contribution is demonstrated.

Cumulative-return targets need care when adapting pointwise multistep methods. Use a compatible log-total-return price formulation or document the target adaptation and test it against original code. Do not transfer guarantees automatically.

## Remaining evidence

Targeted web searches returned irrelevant uses of conformal and do not establish absence. Complete database screening, backward/forward citation checks, and full-text comparison of delayed online learning, auxiliary short-horizon losses, partial-path forecasting, heteroskedastic uncertainty, volatility normalization, and sequential quantile regression.

Archive exact paper/code versions and exclusions. Recheck W06 and W08 before the continuation decision. Search-log entries identify which verification occurred and which searches remain pending.
