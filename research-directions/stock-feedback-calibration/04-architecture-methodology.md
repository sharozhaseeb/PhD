# Architecture and time-safe methodology

## Information available at issue time

Define F(t) as evidence actually available after session t closes and before the declared issue timestamp. All methods share F(t). Daily prices, eligible lagged features, and the one-day prediction error made at t-1 may be used. Five-day labels are available only for origins s with s+5 <= t.

At t, score the five-day forecast from t-5, not t-4. Trading sessions, holidays, and publication times must be represented explicitly. Prices must be available before the declared issue time; do not assume an official close arrives instantaneously.

Five-day forecasts issued on successive dates overlap in four daily returns. They are neither independent experiments nor five independent pieces of evidence.

## Daily-surprise-assisted scale probe

Let mu(s,5) be the archived five-day point forecast issued at s. Let r(t) be today's log total return and mu(t-1,1) yesterday's one-day forecast. Set:
- e(t,1) = r(t) - mu(t-1,1).
- v(t-1) = a strictly positive daily scale calculated before observing r(t).
- z(t) = a bounded transform of abs(e(t,1))/v(t-1), with centering and bounds chosen on development data.
- g0(t) = sqrt(5) times an EWMA daily scale available at t.
- g(t) = max(epsilon, g0(t) * exp(beta * z(t))).

The sqrt(5) factor is a baseline scaling convention, not an independence assumption or validity theorem. Beta = 0 is the ordinary volatility-scaling ablation. Beta and clipping bounds are fixed by chronological validation.

For each matured origin s, compute a(s) = abs(Y(s,5)-mu(s,5))/g(s), using **the stored g(s)**. Never recompute g(s) using information available only now. Maintain a rolling calibration buffer of these matured scores. Issue I(t,5) = [mu(t,5)-q(t)*g(t), mu(t,5)+q(t)*g(t)], where q(t) is its prescribed 90% empirical conformal quantile.

This simple probe has no claimed drift-robust guarantee. Keep it separate from named published algorithms; do not label a modified implementation as the original baseline.

## Daily event ordering

1. Ingest and timestamp newly available observations.
2. Score yesterday's one-day prediction and five-day predictions whose targets have now matured.
3. Update eligible calibration buffers; do not retrain a frozen point forecaster.
4. Compute current features and issue both a one-day auxiliary prediction and a new five-day point forecast and interval.
5. Archive features, model version, mu, scale, quantile, endpoints, issue time, and maturity time.

Past intervals remain immutable. Updating their endpoints before scoring is leakage.

## Mandatory competing explanations

- A rolling empirical interval around the identical five-day point predictions.
- Volatility-normalized rolling calibration with beta = 0.
- Adaptive conformal inference and fully/strongly adaptive variants.
- Multi-step PID and AcMCP, reproduced from author implementations where possible.
- A conditional scale regressor using the same z(t), lagged volatility, and daily features; train only on matured five-day errors.
- A validation-tuned constant-width inflation control.
- No-daily-signal and stale-daily-signal ablations.

Compare native published implementations and controlled variants separately. Some baselines may require their own forecaster or score representation; disclose this, reproduce their native behavior, and avoid pretending they are exact swaps.

## Implementation acceptance checks before real-data inference

A future experiment runner must assert no label enters before maturity, changing future data cannot alter past outputs, issue-time scales remain immutable, and all methods see identical eligible inputs. Hand-calculated synthetic session sequences should exercise holidays and off-by-one errors. This proposal contains no experimental implementation yet.
