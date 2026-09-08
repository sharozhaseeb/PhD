# Evaluation protocol

## Dataset gate

Use a fixed three-instrument equity-ETF panel for the pilot. Instrument selection must precede performance inspection. Record inception/availability, trading calendars, distributions, splits, missing sessions, vendor, license, timezone, download time, and file hashes. Do not silently fill a suspended session or remove a failed instrument.

Historical adjusted prices are often revised. A frozen downloaded vintage supports reproducible retrospective analysis but is not automatically point-in-time data. Validate adjustment conventions, prefer contemporaneously reconstructible return data, and disclose unresolved revision risk. Do not make point-in-time validity claims until this gate is resolved.

## Chronological stages

- Development: provisional 2010-2018, contingent on data availability.
- Exploratory challenge: provisional 2019-2023. COVID and other previously discussed shocks are explicitly not untouched confirmation.
- Reserved retrospective candidate: 2024 through a fixed pre-registration cutoff in 2026, only if access/history checks establish that results have not been used for tuning. Otherwise relabel exploratory and reserve later observations.
- Prospective: begin after models, hashes, code, and protocol are locked. A provisional 120-session run is an operational check; it does not establish rare-transition performance or independent 120-sample evidence.

No data has been downloaded or sealed by this package. Dates and sample sufficiency remain open.

Use expanding or rolling chronological folds with separate fitting, validation, and evaluation periods. Remove fitting/validation origins whose five-day targets cross the next split boundary. Apply a minimum five-session embargo when reusing observations across selection folds; verify actual target overlap rather than assuming a generic gap solves leakage. Freeze point predictors within each evaluation fold. Online calibration may use only labels that mature during the fold.

## Primary endpoint

At alpha = 0.10, interval score:
IS = (U-L) + (2/alpha)*(L-Y)*1[Y<L] + (2/alpha)*(Y-U)*1[Y>U].

Normalize each instrument's score by a positive training-only scale of five-day returns and average with equal instrument weights. Fix the scaling rule and epsilon before validation. Primary contrast is candidate minus a single strong baseline selected on validation alone. Lower is better.

Provisional practical gate: at least 2% relative score improvement and observed pooled coverage >= 88%. Confirmatory inference additionally requires a 95% paired dependence-aware confidence interval below zero. Coverage has its own uncertainty interval; the guardrail is not a guarantee. Do not call conservative overcoverage a success if interval score worsens.

## Secondary outcomes and transition definition

Report width, overall and per-instrument coverage, 20-session rolling coverage descriptively, lower/upper misses separately, and empty/infinite interval frequency. Never cap infinite endpoints to obtain a finite score; report infinite mean score when applicable and separately summarize finite intervals with the selection caveat.

Define operational transition alerts from a trailing 5-session versus 60-session realized-volatility ratio, with threshold fixed using training/validation only. Alerts at t use evidence through t and affect new forecasts only. Group adjacent alerts into episodes using a fixed 20-session cooldown. Assess origins in the next 10 sessions after onset and after a predeclared return-to-normal rule.

Small windows produce noisy coverage estimates. Pool across independently defined episodes and show episode counts and uncertainty; do not claim a reliable daily estimate of 90% coverage. Synthetic shifts supply known onset and controlled duration. Real-data alerts are imperfect observable proxies, not true regimes. Recovery time is descriptive and censored if the target is not recovered within a fixed 60-session follow-up.

## Statistical controls

Resample paired method scores jointly across instruments using temporal blocks, preserving common market shocks. A pilot can examine block lengths 10, 20, and 60 sessions on development data; the final rule and resampling count must be locked before confirmation. Five-session overlap is only the minimum dependence concern: volatility clustering can last longer.

Keep one primary contrast. Use Holm correction for a prespecified finite family of secondary method contrasts, and label additional slices exploratory. The required block bootstrap assumptions and adequacy of event counts remain statistical-review items. No confirmatory p-values exist.

Equalize feature availability, hyperparameter search budget, validation access, and documented runtime budget. Record every tried candidate. Do not select the winning seed or drop a poor instrument.

## Finance policy applicability

The harness was designed for trading and unconditionally requires finance flags. Here they express obligations, not completed validations:
- Point-in-time availability, survivorship awareness, purge/embargo, frozen evaluation, same-information baselines, and forward logging apply directly.
- Transaction costs and factor attribution are mandatory **if a later stage claims trading or stock-selection value**. They are not computed for the current prediction-interval endpoint.
- Identifier/date masking is mandatory **if an LLM is introduced**. The current pilot uses no LLM.
- A negative-result path is documented but publication of a negative result is not assumed.

Return intervals are not trading signals or validated VaR forecasts. A two-sided 90% interval does not automatically calibrate either tail to 5% or 10%; a one-sided risk claim requires a separately designed target and test.
