# Research proposal

## Target and scope

At the close of trading session t, issue an immutable interval for Y(t,5), the sum of log total returns over sessions t+1 through t+5. Equivalently, with a consistently constructed total-return index P, Y(t,5) = log(P[t+5]/P[t]). Simple percentage-return endpoints are exp(L)-1 and exp(U)-1.

Start with three equity ETFs selected before inspecting performance; SPY, QQQ, and IWM are provisional candidates, not a downloaded or licensed dataset. A fixed ETF study avoids a daily cross-sectional selection task but does not eliminate historical availability or survivorship limitations. Individual-stock transfer requires a separately approved point-in-time universe including delistings.

Primary horizon: five trading days. One-day forecasts are an auxiliary information source. Twenty-day outcomes are a later sensitivity study, not a second primary endpoint.

## Main hypothesis

H1: a daily-surprise-assisted calibration policy improves pooled normalized 90% interval score over a validation-selected strong existing baseline receiving the same information, while satisfying a prespecified overall empirical coverage guardrail.

Rivals: additional covariates rather than a new mechanism; ordinary volatility scaling; generic interval inflation; hyperparameter search advantage; temporal leakage.

## Secondary questions

H2: benefits are concentrated around observable volatility transitions rather than exclusively in calm periods.
H3: improvements survive comparison against a flexible scale model that receives the same daily-surprise features.
H4: method rankings remain qualitatively stable across instruments and an untouched forward period.

These are hypotheses, not findings. H3 is particularly important: if a standard model using the same features matches the proposal, withdraw the special-controller contribution.

## Candidate method, deliberately modest

Use a fixed within-fold ridge five-day point forecaster. Train a separate one-day ridge forecaster. A daily normalized absolute one-day error supplies a fast signal. A simple positive scale correction changes the next five-day interval's width; an outer conformal quantile is updated only from matured five-day errors normalized by their archived issue-time scales.

This rule is an experimental probe, not a novelty claim. Its components resemble heteroskedastic calibration, residual prediction, and online adaptation. The literature gate must establish what, if anything, is distinct.

## Contribution boundary

Possible contribution: an operationally precise comparison and a supported improvement in the response/width tradeoff for naturally delayed five-day outcomes. Neither daily information, delayed feedback, nor financial conformal prediction is individually new.

Not claimed: profitable trading, guaranteed acceptance, exact finite-sample conditional coverage under arbitrary market shifts, crash prediction, or agent superiority. An asymptotic coverage result for an existing baseline does not transfer automatically to our correction.

## Provisional success and stop rules

A pilot screens for at least 2% relative improvement in the primary pooled interval score, with overall empirical coverage at least 88% for a 90% target. These are planning thresholds, not universal statistical standards. Freeze or revise them using development data only before any confirmatory test.

For a confirmatory claim require the practical improvement threshold plus a dependence-aware 95% interval for the paired score difference entirely below zero. Report coverage uncertainty; passing the 88% observed threshold is not a coverage guarantee. The same-feature flexible baseline must also be beaten to support H3.

Stop the new-method claim if effects vanish under same-information comparisons, are purchased solely through wider intervals, depend on one instrument or hand-picked event, or duplicate a close method. A benchmark paper remains possible only if its independent scientific value is substantiated.
