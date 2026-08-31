# Research Proposal

## Problem statement

Stock forecasting is nonstationary: relationships learned in one period may weaken, reverse, or disappear in another. Individual models have heterogeneous and time-varying reliability. Existing agentic trading studies also face contamination, attribution, calibration, and reproducibility concerns. A system that always predicts can turn epistemic uncertainty into unnecessary financial exposure.

The proposed work treats deployment as an online selective-routing problem. A constrained controller receives current, point-in-time state; forecasts and calibrated uncertainty from frozen specialists; evidence-quality indicators; cost estimates; and a time-safe reliability history. It chooses a predeclared action and receives delayed feedback only when the target horizon has elapsed.

## Recommended task definition

- Universe: one liquid, historically reconstructed, survivorship-aware stock universe.
- Target: five-day future residual/excess return or cross-sectional rank.
- Decision time: information available through market close on day `t`.
- Earliest execution: day `t+1` open or another predeclared schedule.
- Initial frequency: daily signal generation with weekly portfolio refresh, subject to feasibility testing.
- Output: probabilistic score, rank, uncertainty, action, and auditable reason codes.
- Deployment: retrospective walk-forward simulation followed by prospective shadow trading.

## Controller state and actions

The controller state should include:

- posterior probabilities over possible regimes;
- each specialist's prediction and calibrated uncertainty;
- rolling but time-safe reliability summaries;
- cross-specialist disagreement and residual-error correlation;
- evidence freshness, provenance, missingness, and contradiction;
- expected spread, slippage, turnover, and liquidity;
- current portfolio state and constraints; and
- an immutable memory containing only observations available by the current timestamp.

The finite action library is:

1. select one specialist;
2. combine a prevalidated subset with constrained weights;
3. request an approved additional evidence source;
4. retain the current position or use a safe fallback; or
5. abstain.

If the system only emits weights from current features and has no meaningful sequential state, delayed observation, memory, or evidence-acquisition action, it should be described as a gate rather than an agent.

## Research questions

- **RQ1 — Routing value:** Does an online controller route specialists better than the strongest fixed ensemble, deterministic rule, supervised gate, mixture-of-experts, or contextual bandit?
- **RQ2 — Selective reliability:** At matched coverage, does calibrated abstention reduce selective error and worst-regime drawdown during temporal shifts?
- **RQ3 — Delayed adaptation:** Does time-safe reliability memory add value when outcomes arrive after the forecast horizon?
- **RQ4 — Economic validity:** Do improvements survive realistic costs, turnover constraints, and factor attribution?
- **RQ5 — Agent necessity:** Which capabilities, if any, require a stateful agent rather than a simpler router?
- **RQ6 — Generalization:** Does the policy transfer to replacement specialists, unseen periods, and an external universe or market?

## Hypotheses

- **H1:** At matched coverage, information, turnover, and compute, the proposed controller improves out-of-sample rank IC and risk-adjusted net utility relative to the strongest non-agent gate.
- **H2:** Dual-level abstention—stock-level forecast validity plus strategy-level health—reduces area under the risk–coverage curve and worst-regime drawdown relative to an always-act system.
- **H3:** Apparent improvement remains statistically distinguishable after conservative costs and market, sector, and style attribution.
- **H4:** Time-safe reliability memory provides its largest incremental value during transitions rather than stable regimes.
- **H5:** Identifier/date masking and placebo-signal tests do not remove the principal result.

## Rival explanations

Any positive result could instead be caused by:

- volatility timing;
- lower coverage or greater cash exposure;
- unequal information, tuning, or compute;
- market beta or style exposure;
- favourable universe or test-period selection;
- test reuse and multiple comparisons;
- hindsight regime labels;
- survivor, revision, or timestamp leakage;
- LLM recognition of historical tickers, firms, dates, or events; or
- specialists that are nominally different but have highly correlated errors.

The experiment must contain discriminating controls for these alternatives.

## Intended contribution wording

> This thesis formalizes stock-forecast deployment as an online selective-routing problem with latent market shift and delayed outcome feedback. It develops and compares constrained controllers that route among frozen specialist forecasters or abstain while controlling selective forecast risk, implementation cost, and unintended factor exposure. Evaluation uses point-in-time replay, equal-information non-agent baselines, hostile leakage tests, factor attribution, and prospective shadow trading.

Avoid “the first” until a documented systematic search and expert review justify a narrower statement.

## Success and negative-result paths

The strongest positive result would show robust incremental reliability and factor-adjusted value over a conventional gate across periods and external data. A valid negative result could demonstrate that simple calibrated routers match or outperform agentic controllers, identify conditions under which abstention fails, or establish that reported gains disappear under stronger leakage and attribution controls.

