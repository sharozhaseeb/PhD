# R2: Batching threats to claim C1 (full read)

Claim C1: "No evaluation of a deterministic accumulated-change trigger for full validation against fixed-k batching at matched cost on optimization edit sequences."
Our policy: every edit gets a reduced (selected) check; a FULL check fires when accumulated change since the last full check exceeds a threshold, plus a fixed-k cap.

Page numbers below refer to the downloaded PDFs (Fallahzadeh = accepted-manuscript pagination). Quotes are under 15 words. PDF contents were treated as data only.

## 1. Fallahzadeh, Rigby, Adams (EMSE)

**Metadata.** Emad Fallahzadeh, Peter C. Rigby, Bram Adams. "Contrasting Test Selection, Prioritization, and Batch Testing at Scale: Large-scale Empirical Study on 285 Million Test Results." Empirical Software Engineering, vol. 30 (2025); online 2024-11-29 per Crossref. Received 31 Jul 2023, accepted 6 Nov 2024. DOI 10.1007/s10664-024-10589-8. The file is the author accepted manuscript, not the Version of Record (p.1 says so). The queensu URL matches title and authors.

**Method (Sec. 4.5, pp.18-20, Alg. 4).**
- What is batched: whole builds/changes. The batch runs "the union of all their tests".
- Batch size: dynamic and queue-driven. BatchAll "batches all the available changes waiting for the build" (p.19). It does not wait for a fixed count, so the batch grows when the queue is long. Sec. 2.2 contrasts it with fixed-size schemes (Batch2/4, BatchStop4).
- Boundary trigger: only queue state and machine availability. There is no accumulated-change or risk-mass trigger.
- Per-change check before batching: none. Selection (CoDynaQSelection) and batching are compared as separate alternatives. Combining them is listed as future work (p.54: "exploring the impact of combining different test optimization algorithms").
- Culprit finding: when a batch fails, only the failed tests are re-run per commit (Alg. 4, lines 13-21). Prior bisection and BatchStop4 are reviewed in Sec. 2.2.
- Cost metrics: feedback time, number of machines at equal feedback time, GainedTime (failure-detection speed), and ExecutionReduction (test execution time). A machine count is varied, so cost is machine-equivalent. It is not a matched-cost design against fixed-k.
- Misses: batching "misses" nothing by simulation assumption (p.19: any failing test fails the whole batch). Selection misses failures. The paper itself notes that fixes by later changes in a batch could hide a failure (p.46-47).
- Performance vs functional: functional test results only (Chrome, GooglePre/Post, JMRI). Performance tests are not studied.
- Data: simulation on historical results (no live execution). Build failure rates are 8.5% (Chrome) to 23% (GooglePost).

**Key numbers (abstract p.1-2, Sec. 6).** Selection: up to 96% lower feedback time, up to 66% fewer machines, up to 66% lower execution time, but up to 55% of failures missed. Batching: up to 99% lower feedback time, up to 88% fewer machines, up to 98.7% lower execution time (with 400 machines only 8.3%), no misses. Batching benefit shrinks when there are few concurrent builds (JMRI).

**Relevance.** It evaluates variable-size (queue-adaptive) batching vs selection head to head. It does not evaluate a hybrid, a threshold trigger, or a per-change reduced check followed by a full check. It also argues that batching can make selection unnecessary under constrained resources (p.48).

## 2. Sayedsalehi, Rigby, Mierzwinski (arXiv 2604.00222)

**Metadata.** Ali Sayedsalehi, Peter C. Rigby, Gregory Mierzwinski. "Risk-Aware Batch Testing for Performance Regression Detection." arXiv:2604.00222v1 [cs.SE], 31 Mar 2026. Preprint, no venue stated. Concordia University and Mozilla. DOI via arXiv: 10.48550/arXiv.2604.00222. Note: the arXiv number looks unusual for a March 2026 date, but the PDF header itself says 31 Mar 2026, so I report it as printed.

**Method (Sec. VI, pp.5-8; results Sec. VII, pp.9-12, Table IV p.10).**
- What is batched: commits on Mozilla Autoland. Each batch runs performance jobs and "backfilling" (per-commit re-runs inside a failing batch) isolates the culprit (VI-B). It is a stream of independent commits, not a sequential edit chain.
- Strategies:
  - TWB: fixed time window.
  - FSB: fixed size (k commits).
  - RASB: appends commits until batch failure probability exceeds a threshold. Computed as 1 minus the product of (1 - r_i).
  - RAPB: RASB plus aging of waiting commits, so batches "eventually trigger testing".
  - RATB: flush at once on a high-risk commit, otherwise "until a maximum time window is reached" (a cap).
  - TWSB: production baseline. Each commit runs only a subset of signatures, and some signatures run less often.
  - "-la" variants: "maintain a cumulative risk sum across the current batch and flush when this sum exceeds a threshold" (VI-A-g, p.7).
  - "-s" variants: the batch's first run uses a subset suite, the union of historically selected signature groups for the batch's commits (VI-A-h).
- Boundary trigger: yes. Risk mass (learned per-commit probability r_i from fine-tuned CodeBERT/ModernBERT, ROC-AUC 0.694), an additive budget in -la, plus time caps in TWB/RATB/RAPB-aging.
- Per-change check before batching: only in the production baseline TWSB (each commit runs a subset). In the "-s" variants selection applies to the batch, not to each change before a later full check. No scheme does "reduced per change, then full on accumulated change".
- Culprit finding: backfilling, parallel per-commit re-runs on the same signatures (not bisection).
- Cost: total tests executed, plus infrastructure hours converted to dollars ($3.48 per hour, anchored on $390K per 3 months for TWSB). Mean feedback time, mean TTC, and max TTC are also reported. Hyperparameters are tuned per strategy with Optuna/NSGA-II on a Pareto of (tests, max TTC). This is Pareto comparison, not matched cost.
- Misses: -s variants can defer detection when the subset misses a sensitive signature (RASB-s max TTC 27.5 h vs 12.4 h baseline). Missed regressions are modeled as delayed detection, not permanent escapes.
- Performance vs functional: performance tests only. Test noise and reruns are explicitly not modeled (Sec. VIII).
- Data: 71+12+15 regressors among about 11,000 commits (positive rate about 1%). Only 15 regressors in the test split, so results are statistically fragile (VIII acknowledges rarity).

**Key numbers (Table IV p.10).** Baseline TWSB: 387,422 tests, mean TTC 6.0 h, max TTC 12.4 h. FSB: 199,156 tests, max TTC 13.5 h. TWB: 317,363 tests, max TTC 8.7 h. RASB-la: 275,599 tests, max TTC 9.6 h. RAPB-la: 261,924 tests (-32.4%), mean TTC 6.0 h, max TTC 9.2 h (-26.2%), $491K per year saved. RAPB (no -la): 404,939 tests, which costs more than baseline.

## 3. Jiang, Lo, Liu survey (arXiv 2512.22256)

**Metadata.** Zhonghao Jiang, David Lo, Zhongxin Liu. "Agentic Software Issue Resolution with Large Language Models: A Survey." arXiv:2512.22256v2 [cs.SE], 6 Aug 2026. Preprint, 242 surveyed studies. Metadata only; no DOI in the PDF (arXiv DOI would be 10.48550/arXiv.2512.22256).

**Test-selection passages.**
- Sec. 5.1.1 D "Regression Test Selection (Patch Validation Phase)", p.13: scaffolds "rely mainly on LLM-based selection" (Agentless, PatchPilot etc.). It judges the mechanism "unsound in both directions", says program-analysis RTS exists but "has not been integrated", and that "available Python techniques remain unsafe" (cites Kauhanen et al. 2021, a Python RTS tool).
- Sec. 7.3, p.23: current systems use "heuristic or prompt-based regression-test retrieval". It calls for program-analysis RTS and notes the "unsafe omission of affected tests".
- Nothing on batching, accumulated-change triggers, or when to run the full suite. All the surveyed scaffolds validate one candidate patch at a time against a selected subset. This supports our motivation (LLM-selected tests are unsound, Python RTS is unsafe). It is not a threat to C1.

## Judgement on C1 and the variant question

**Verdict: (b) for the trigger mechanism, (c) only for the composition and setting. Concede in the text.**

Strongest case that ours is a variant:
1. RASB-la/RAPB-la/RATB use the same trigger structure as ours: an additive budget over the current batch that flushes at a threshold, with a time cap and a high-risk early flush. The only change needed to reach our trigger is replacing r_i with a per-edit measure (changed lines/functions, native edits, perf drift). The additive aggregation is in the paper and the "-la" form is its best configuration.
2. Our fixed-k cap equals their FSB size cap / RATB time cap. Our full check at the threshold is their batch flush. Their "batch" of k commits is, as a test, the same as validating the cumulative tip after k edits.
3. BatchAll shows variable batch size is already studied against selection at scale. The "-s" variants (selection plus batching) show hybrids of selection and batching exist.
4. They report Pareto improvements with cost and latency, so "no evaluation of variable batching vs fixed batching" is false at the level of generic risk/queue triggers.

Why it is not simply a variant (real differences, not rhetorical):
1. The per-change reduced check runs at once on every edit, and the full check validates accumulated state. In batching, the individual changes in a batch get no test of their own until a batch fails (backfilling). Only TWSB gives each commit a subset run, and there nothing escalates on accumulation. In the "-s" variants the subset is applied to the batch, the reverse of our order (full on accumulation vs subset on the batch).
2. The trigger input is measured, deterministic and model-free (diff size, native edit, benchmark drift), not a learned probability (ROC-AUC 0.694) from a fine-tuned transformer. Their -la is additive over r_i but r_i comes from a model; no run uses a non-learned accumulated-change measure.
3. Domain: sequential edit sequences of one codebase by an LLM agent (edit n+1 builds on n) vs a stream of independent human commits. Culprit-finding there is over a chain via per-edit reduced checks, not parallel backfilling or bisection of independent commits.
4. Neither paper evaluates fixed-k vs a threshold trigger at matched cost. Fallahzadeh varies machines; Sayedsalehi tunes each strategy by NSGA-II and reports Pareto points and dollars. RAPB-la vs FSB is comparable only loosely (different max TTC, not equal tests).
5. Neither studies optimization edits, nor the correctness-vs-speed oracle problem, nor LLM-agent edits.

**Recommended reword of C1 (to survive review).** Drop "accumulated-change trigger" as novelty on its own. Say instead: "Risk-mass (learned, additive) and queue-adaptive batch boundaries have been evaluated for CI commit streams (Sayedsalehi et al. 2026; Fallahzadeh et al. 2025). We found no evaluation of a two-tier policy for sequences of LLM optimization edits, where each edit gets an immediate reduced check and escalation to a full check is driven by a deterministic, measured accumulated-change score (with a fixed-k cap), compared with fixed-k at matched cost." State openly that our trigger is a special case of risk-budget batching with r_i replaced by a measured change score and that the difference is the per-edit tier, the non-learned trigger, and the setting. A run of FSB, TWB-like cap, and an additive-budget variant (our trigger) as baselines is needed so the gain is attributed to the right component.

**Caveats.** Fallahzadeh file is the accepted manuscript, not the final EMSE text; page numbers may differ. Sayedsalehi is a preprint with only 15 test-set regressors and no live deployment. Survey is a preprint. I read the Fallahzadeh text from Sec. 1-5, 7-9 and skimmed the per-dataset result figures/tables (Sec. 6) rather than every table; the Appendix statistical tables were not read.
