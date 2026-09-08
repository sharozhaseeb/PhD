# Choosing a manageable PhD direction

Date: 5 September 2026. Status: focused literature screening and three-agent discussion; not a completed systematic review, established novelty claim, or advisor-approved proposal.

## Recommendation

Provisionally prioritize **reliable forecasting with delayed observations**, starting with an empirical electricity-demand study. Preserve finance as an application option and cybersecurity as an advisor-dependent alternative. Do not commit the thesis before a bounded pilot.

Concrete starter question: **How should prediction intervals update when delayed observations arrive in batches?**

Example: a forecast service temporarily cannot obtain validation outcomes. When reporting resumes, it receives many old errors at once. If conditions have changed, do ordinary adaptive calibration updates react to stale errors and produce unnecessarily wide or unreliable intervals? How long does recovery take?

This is a hypothesis to investigate, not a verified literature gap. Delay, drift, conformal prediction, and missingness already have extensive prior work. Combining their names is insufficient novelty.

## Basis for the comparison

Three agents independently screened finance, general forecasting, and applied cybersecurity. The main review challenged their recommendations against overlapping work and checked primary proceedings, publisher pages, author repositories, and dataset documentation. Paper existence and descriptions were screened; code was not run, datasets were not downloaded, and not every paper was read in full. Some OpenReview pages were verification-blocked; indexed primary PDF text was available. This is a starting bibliography, not an exhaustive search.

The provisional ranking assumes a normal workstation, public data, and an advisor receptive to empirical ML methodology. The user's skills, advisor expertise, GPU access, and degree publication requirements remain unspecified.

| Direction | Pilot feasibility judgment | Principal obstacle | Recommendation |
|---|---|---|---|
| Forecast calibration with delayed outcome reporting | Relatively manageable with cached forecasts and simple update loops | Crowded methods literature; real reporting-time data needed eventually | First pilot |
| Financial forecast uncertainty | Manageable models; harder interpretation and data validation | Existing volatility/stock calibration studies; market nonstationarity | Alternative application |
| Intrusion detection with selective, delayed feedback | CPU-based tabular pilot feasible | Strong prior overlap; dataset artifacts and lack of real analyst timelines | Prefer if advisor/data support exists |
| Original agentic stock routing proposal | Highest scope and evaluation burden of these options | Many coupled mechanisms, financial attribution, unclear incremental agent value | Defer as the thesis starting point |

These are comparative judgments, not measured acceptance probabilities. Accepted papers establish publication precedent, but omit the denominator of rejected and abandoned projects. They cannot establish the probability that our proposed paper will be accepted.

## Forecasting literature

| Primary source | Existing contribution | Consequence for our proposal |
|---|---|---|
| [Gibbs & Candès, Adaptive Conformal Inference Under Distribution Shift, NeurIPS 2021](https://papers.nips.cc/paper_files/paper/2021/hash/0d441de75945e5acbc865406fc9a2559-Abstract.html) | Adaptive uncertainty under changing distributions | Drift adaptation alone is established |
| [Zaffran et al., Adaptive Conformal Predictions for Time Series, ICML 2022](https://proceedings.mlr.press/v162/zaffran22a.html) | Aggregates adaptive calibration settings | Include an adaptive aggregation baseline |
| [Xu & Xie, Sequential Predictive Conformal Inference for Time Series, ICML 2023](https://proceedings.mlr.press/v202/xu23r.html) | Exploits temporal dependence in residuals | Include a residual-dynamics baseline where feasible |
| [Angelopoulos et al., Conformal PID Control for Time Series Prediction, NeurIPS 2023](https://papers.nips.cc/paper_files/paper/2023/hash/47f2fad8c1111d07f83c91be7870f8db-Abstract-Conference.html) | Online quantile tracking with error forecasting and correction | Ordinary feedback correction and forecast horizons are not new |
| [Gibbs & Candès, Conformal Inference for Online Prediction with Arbitrary Distribution Shifts, JMLR 2024](https://jmlr.org/papers/v25/22-1218.html) | Online adaptation, including financial volatility experiments | Generic stock-volatility calibration is already studied |
| [Hallberg Szabadváry, Adaptive Conformal Inference for Multi-Step Ahead Time-Series Forecasting Online, COPA 2024](https://proceedings.mlr.press/v230/hallberg-szabadvary24a.html) | Multi-step adaptive conformal inference | Horizon-induced delay alone cannot be our novelty |
| [Retzlaff et al., Testing Marginal and Conditional Coverage in Conformal Prediction for Non-Stationary Time Series via Value-at-Risk Backtesting, COPA 2025](https://proceedings.mlr.press/v266/retzlaff25a.html) | Formal coverage assessment reveals problems hidden by average metrics | Use existing diagnostics; generic coverage auditing is established |
| [Chen et al., Post-Training Adaptive Conformal Prediction for Incomplete Time Series, TMLR May 2026](https://openreview.net/pdf/bc5b1f3cf33331fca072ddb0497af15a920e10ba.pdf) | Missingness-aware post-training calibration | Do not initially combine predictor missingness with reporting delay |
| [Sabashvili, Conformal Prediction Algorithms for Time Series Forecasting: Methods and Benchmarking, January 2026 preprint](https://arxiv.org/abs/2601.18509) | Compares conformal approaches on sales data | Another generic benchmark is insufficient; preprint is not acceptance evidence |

The existing workspace incorrectly labeled Retzlaff et al. as AISTATS; the literature map has been corrected to COPA 2025 and the full paper title.

## Finance and security literature checks

| Primary source | Relevance |
|---|---|
| [Pidan & El-Yaniv, Selective Prediction of Financial Trends with Hidden Markov Models, NeurIPS 2011](https://proceedings.neurips.cc/paper/2011/hash/dd458505749b2941217ddd59394240e8-Abstract.html) | Financial abstention has long-standing precedent |
| [Kaya & Nguyen, Conformal Prediction for Reliable Stock Selections, COPA 2025](https://proceedings.mlr.press/v266/kaya25a.html) | Direct applied precedent, but a three-page contribution does not establish thesis sufficiency |
| [Torres et al., FinAbstain, July 2026 preprint](https://arxiv.org/abs/2607.24875) | Close architecture overlap with specialist agents and abstention; explicitly simulated results are not empirical validation |
| [Pendlebury et al., TESSERACT, USENIX Security 2019](https://www.usenix.org/conference/usenixsecurity19/presentation/pendlebury) | Temporal/spatial evaluation bias already studied in malware detection |
| [Troubleshooting an Intrusion Detection Dataset, IEEE S&P Workshops 2021](https://intrusion-detection.distrinet-research.be/WTMC2021/) | CICIDS2017 problems and corrections already investigated |
| [Error Prevalence in NIDS Datasets, IEEE CNS 2022](https://intrusion-detection.distrinet-research.be/CNS2022/) | Broader dataset-error analysis and corrected resources |
| [Arp et al., Dos and Don'ts of Machine Learning in Computer Security, USENIX Security 2022](https://www.usenix.org/conference/usenixsecurity22/presentation/arp) | Strong precedent for methodological research; generic pitfalls are established |
| [Model update for intrusion detection: Analyzing the performance of delayed labeling and active learning strategies, Computers & Security 2023](https://doi.org/10.1016/j.cose.2023.103451) | Direct overlap with delayed labels and limited labeling budgets |
| [NOCTOWL, IEEE Access 2025, author PDF](https://iris.unimore.it/retrieve/79a63b13-7619-4d6b-81b9-3625afa8344c/NOCTOWL_Adaptive_Tree-Based_Model_for_Network_Anomaly_Detection_Under_Delayed_and_Sampled_Label_Availability.pdf) | Adaptive trees under delayed and sampled labels; mandatory close baseline |

Security is not demonstrated to be easier than forecasting. A narrower security question about score-dependent analyst delays may be worth testing, but requires further overlap checks and realistic timing data.

## A four-to-six-week feasibility pilot

This is a planning estimate for testing a candidate, not a publication schedule.

1. **Literature and reproduction:** build a closest-work matrix covering feedback timing, batch returns, out-of-order feedback, shift assumptions, datasets, metrics, code, and guarantees. Reproduce ACI and PID/quantile tracking with [author code](https://github.com/aangelopoulos/conformal-time-series). Chase references on delayed online learning before developing any new policy.
2. **Small controlled setup:** use synthetic variance changes and a fixed subset of [UCI electricity demand](https://archive.ics.uci.edu/dataset/321/electricityl), with seasonal-naive and ridge forecasts. Freeze predictions to isolate calibration behavior.
3. **Availability controls:** keep forecast inputs unchanged across policies and manipulate only the revelation of calibration outcomes. Separate forecast-horizon maturity from additional reporting delay. If lagged values reveal the same target, do not pretend that target is unavailable: use an independently delayed verification channel or revise the experiment to delay those inputs consistently. Every operational policy must receive identical available information.
4. **Stress scenarios:** immediate reporting, ordinary fixed delay, and a reporting blackout followed by batch release; test both stable conditions and independently specified variance shifts. These are synthetic stress tests, not evidence of actual utility reporting behavior.
5. **Baselines and candidates:** rolling residual calibration, ACI, a horizon-aware variant, PID/quantile tracking, and stronger adaptive or residual-based baselines as feasible. Compare ordinary arrival updates against bounded batch updates and age weighting. Treat the latter as candidate policies, not invented contributions. An immediate-feedback oracle is diagnostic and must be labeled as having extra information.
6. **Evaluation:** chronological validation, locked test configurations, interval score, coverage, width, and prespecified recovery measures. Report infinite intervals explicitly. Use uncertainty estimates that respect time dependence; avoid treating adjacent observations as independent replicates. Check a second held-out dataset/domain before claiming transfer.

UCI documents 370 client series, 15-minute measurements, a CC BY 4.0 license, and no missing values. It also documents zeros for clients not yet active and daylight-saving peculiarities. Consequently, do not interpret zeros as outages. Simulated reporting delays must be disclosed. [Monash Forecasting Archive](https://forecastingdata.org/) is a source for additional domains.

## Go/no-go decision and possible thesis

Continue only if a repeatable, meaningful failure survives strong existing baselines, untouched settings, and a specific closest-work check. Stop or reframe if the effect disappears, is only an implementation bug, or is already adequately addressed. Finding no effect does not automatically produce a publishable negative-result paper.

If justified, a coherent thesis could contain three distinct contributions:

- A reproducible characterization of calibration failures and recovery under a clearly motivated observation-availability process.
- A correction with strong empirical evidence and, if feasible with supervisor support, a limited result under explicit assumptions.
- Validation with genuine observation/release timestamps and a downstream decision task or independent domain.

These are contingent contributions, not three promised publications. COPA offers direct specialist publication precedent; TMLR, ICML, NeurIPS, and JMLR establish broader interest but are demanding precedents, not easy targets. Check the university's accepted venue and thesis requirements before setting submission plans.

Next review step: complete documented search strings and screening counts, perform backward/forward citation checks for the closest delay-aware papers, inspect full texts and code, and agree on a one-page pilot protocol with the advisor. The current screening cannot certify novelty or replace that review.
