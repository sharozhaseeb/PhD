# Literature and Novelty Map

## Search boundary

- Last checked: 31 August 2026
- Current status: targeted recent-literature review, not yet a completed systematic review
- Source types used: primary conference papers, proceedings pages, arXiv manuscripts, and selected methodological papers
- Important limitation: absence within this search boundary does not prove universal novelty

## Closest work

| Work | What it already covers | Remaining distinction to test |
|---|---|---|
| [Sun, Wang & An, *AlphaMix* (2022)](https://arxiv.org/abs/2207.07578) | Uncertainty-aware trading experts and dynamic neural routing | Latent shift, delayed-feedback selective-risk control, attribution-constrained objective, and equal-information agent necessity tests |
| [Chalkidis & Savani, *Trading via Selective Classification* (2021)](https://arxiv.org/abs/2110.14914) | Refusal of low-confidence trades | Dual-timescale validity, expert routing, attribution constraints, and prospective audit |
| [Yu et al., *MIGA* (2024)](https://arxiv.org/abs/2410.02241) | Dynamic expert switching for different stock styles | Explicit abstention, delayed controller state, hostile leakage controls, and agent-versus-gate tests |
| [Kou et al., *Automate Strategy Finding with LLM in Quant Investment* (2025)](https://aclanthology.org/2025.findings-emnlp.1005/) | Multi-agent factor discovery, market-state filtering, and dynamic weighting | Formal selective deployment and attribution-constrained delayed feedback |
| [Xiong et al., *FLAG-Trader* (2025)](https://aclanthology.org/2025.findings-acl.716/) | LLM plus gradient-based reinforcement learning for trading | Constrained controller role and equal-information comparison rather than end-to-end trading claims |
| [Dong et al., *Large Language Model Agents in Finance: A Survey* (2025)](https://aclanthology.org/2025.findings-emnlp.972/) | Maps finance-agent architectures and deployment challenges | Supports need for transparent, reproducible, adaptive evaluation; not a direct method baseline |
| [Chen et al., *StockBench* (2025/2026)](https://arxiv.org/abs/2510.02209) | Contamination-conscious multi-period evaluation; many agents struggle against buy-and-hold | Use its negative findings to motivate strong basic baselines and forward evaluation |
| [Torres, Cheng & Huang, *FinAbstain* (2026)](https://arxiv.org/abs/2607.24875) | Point-in-time multimodal retrieval, specialist agents, calibration, conformal prediction, and abstention | Its numerical results are explicitly simulated; empirical delayed-feedback and attribution-constrained validation remain possible, but its architecture cannot be claimed as ours |
| [Ye & Borde, *RG-ResMoE* (2026)](https://arxiv.org/abs/2608.12251) | Regime information used specifically for routing residual experts; rolling cross-market volatility evaluation | Rules out “regime-gated expert routing” as novelty; motivates comparison with matched soft gates |
| [Zhu et al., *KTD-Fin* (2026)](https://arxiv.org/abs/2605.28359) | Identifier/date masking and Barra-style performance attribution | Provides required evaluation controls and evidence that raw return can mask limited stock-selection alpha |
| [Deng et al., *AlphaQuanter* (2026)](https://aclanthology.org/2026.findings-acl.456/) | Tool-augmented single agent that acquires information using reinforcement learning | Rules out generic active evidence acquisition as novelty; ours must focus on constrained reliability and attribution |

## Methodological foundations

- [Zaffran et al., Adaptive Conformal Predictions for Time Series (ICML 2022)](https://proceedings.mlr.press/v162/zaffran22a.html)
- [Xu & Xie, Sequential Predictive Conformal Inference for Time Series (ICML 2023)](https://proceedings.mlr.press/v202/xu23r.html)
- [Angelopoulos et al., Conformal Risk Control (2022)](https://arxiv.org/abs/2208.02814)
- [Retzlaff et al., Testing Marginal and Conditional Coverage in Conformal Prediction for Non-Stationary Time Series via Value-at-Risk Backtesting (COPA 2025)](https://proceedings.mlr.press/v266/retzlaff25a.html)

These papers provide foundations but do not automatically give valid guarantees for dependent, drifting stock returns. Every claimed guarantee must state its assumptions and be stress-tested under temporal dependence.

## What is not novel by itself

- multiple forecasting specialists;
- financial agents discussing evidence;
- mixture-of-experts;
- regime-aware routing;
- uncertainty estimation;
- confidence thresholds;
- abstaining from trades;
- multimodal financial retrieval;
- dynamic factor weighting;
- point-in-time data hygiene; or
- reporting transaction costs.

## Candidate defensible gap

The candidate gap is a formally specified online deployment problem joining delayed labels, uncertain regimes, selective-risk control, implementation costs, factor-exposure constraints, and causal tests of the controller's incremental contribution over simpler equal-information policies.

This wording remains provisional. A systematic search must include at least arXiv, OpenAlex/Crossref, Semantic Scholar, SSRN, NBER, RePEc, ACM, IEEE, ACL Anthology, PMLR, and publisher databases accessible through the university.

## Novelty maintenance

Every six months:

1. repeat stored searches;
2. screen citations and references of the closest papers;
3. add newly found work to `audit/nearest_work.csv`;
4. reassess whether each claimed difference is methodological, theoretical, empirical, or merely presentational;
5. narrow or reframe the claim when overlap appears; and
6. record the date, databases, search strings, result counts, and exclusions.

