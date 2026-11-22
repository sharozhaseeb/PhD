# Research content in brief

This page summarises and links. The sources are the W1 and W2 folders; read them for citations and labels ([R] read in source, [F] fetch summary, [A] abstract, [I] inferred, [U] unknown).

## The problem

Iterative optimization makes many small edits. Each edit is re-validated: build, tests, and a check that the speed-up is real and nothing regressed. Doing a full build, full tests and full benchmarks after every edit is slow. Study 1 asks how to validate each edit with a reduced build and a reduced test and benchmark set, chosen by deterministic rules, and how far that can be trusted. [CHARTER](../pm/CHARTER.md).

## Research questions (revised 2026-11-21)

- **RQ1 Cost.** What share of per-edit validation time goes to build, tests and benchmarks, and how does it accumulate over a sequence of edits?
- **RQ2 Existing techniques, unchanged.** How much end-to-end time do incremental builds and RTS (pytest-testmon, changed-module rule) save, including their overhead, and what failures and regressions do they miss, and why?
- **RQ3 New deterministic policy.** Does a policy using (a) changes accumulated since the last full check, (b) profile/call-graph benchmark selection and (c) a full check triggered by accumulated change miss fewer failures and regressions than the best existing combination at matched cost? Ablate each part.

Background chapters, not RQs: how optimizers validate (W2) and what reduction techniques exist (W1). The original RQ1–RQ4 are kept as history in the charter.

## Literature map

Full table: [taxonomy](../01-literature/taxonomy.md). Narrative: [review](../01-literature/review.md). One page: [literature-in-one-page](../01-literature/literature-in-one-page.md).

| Area | Main techniques | Safety assumption | Key keys |
|---|---|---|---|
| Reduced builds | Timestamp rebuild, hash traces, early cutoff, caches, traced builds, ccache | Complete declared dependencies, deterministic tasks | `mokhov2020buildsystems`, `licker2019incorrect`, `gallaba2020kotinos` |
| Regression test selection | Safe RTS, Ekstazi, STARTS, testmon, NameRTS, history windows | Controlled regression testing; fresh dependency data | `rothermel1997safe`, `gligoric2015ekstazi`, `legunsen2016static`, `WangPradelLiu2026`, `Elbaum2014`, `chittimalli2009recomputing` |
| Performance / benchmark selection | Coverage-based prioritization, PerfRanker, reduced suites, µOpTime, interleaved A/B | Effects stay where coverage is; noise known | `laaber2021tcp`, `mostafa2017perfranker`, `grambow2022microbenchmark`, `japke2025uoptime`, `ding2020readily` |
| Batching | Constant batch + bisection, risk-ordered, risk-mass flush, batching vs selection | Low culprit rate; monotone failures | `najafi2019bisecting`, `sayedsalehi2026riskaware`, `bavand2021mining`, `fallahzadeh2025contrasting` |
| Checkpointing / periodic full runs | Google TAP milestones, Meta periodic full runs, MongoDB change points | Full run as backstop | `memon2017taming`, `daly2020changepoint` |

Synthesis ([review](../01-literature/review.md) §6): every reduction is only conditionally safe; Python is under-served; coverage is necessary but not sufficient for performance; accumulation over many edits is studied only at its edges.

## Key prior works

From [closest-works](../01-literature/closest-works.md) (22 rows):

| Work | Key | Relation to Study 1 |
|---|---|---|
| PerfAgent (arXiv 2607.19653, 2026) | `deng2026perfagent` | Already runs testmon-selected tests per iteration in an LLM optimization loop; never runs the full suite; names the native-extension hole |
| NameRTS (arXiv 2605.25356, 2026) | `WangPradelLiu2026` | Strongest Python RTS found (−45.6% time, safe on 99.6% of commits); excludes non-Python-only commits |
| Sayedsalehi et al. 2026 (Mozilla) | `sayedsalehi2026riskaware` | Risk-mass batch flush; our trigger is a model-free variant of it (conceded) |
| Fallahzadeh, Rigby, Adams (EMSE 2025) | `fallahzadeh2025contrasting` | Selection misses up to 55% of failures; batching compared as an alternative |
| Ekstazi / pytest-testmon | `gligoric2015ekstazi`, `TestmonBlog` | Baseline selectors; one observed run; Python lines only (testmon) |
| Chittimalli & Harrold (TSE 2009) | `chittimalli2009recomputing` | Outdated coverage harms selection for one version step; narrows C7 |
| Grambow et al. | `grambow2022microbenchmark` | Reduced benchmark suite missed a trend; precedent for C11 |
| Ding et al. (ICSE 2020) | `ding2020readily` | 74–77% of covering tests show no known speed-up |
| RTSLinux, Elsner, Kauhanen | `celik2017rtslinux`, `elsner2022buildaware`, `KauhanenPytestRTS` | Native-boundary analogues for C5 |

## The literature's own stated future work

| Source | Stated future work | Where recorded |
|---|---|---|
| PerfAgent | "Extending selective testing to native-extension coverage" (§VII) | [R1 note](../01-literature/notes/R1-perfagent-fullread.md) |
| Fallahzadeh et al. 2025 | Combining test optimization algorithms (selection with batching) (p. 54) | [R2 note](../01-literature/notes/R2-batching-threats-fullread.md); [review](../01-literature/review.md) §5 |
| Ekstazi | A formal proof that Ekstazi is safe | [T2 note](../01-literature/notes/T2-rts.md) |
| Build tracing (A10 in T1) | Dynamic-analysis incompleteness: tracing sees only exercised paths | [T1 note](../01-literature/notes/T1-builds.md) |

The critic corrected one location: Kotinos' preconditions are in §9 Threats, not a future-work section ([critic-report](../01-literature/critic-report.md) F9).

## Practice survey (W2)

28 systems, critic-checked. [W2 README](../02-practice-survey/README.md); [findings](../02-practice-survey/findings.md); [survey-table](../02-practice-survey/survey-table.md).

| ID | Finding (short) |
|---|---|
| F1 | No iterative optimizer decides by rule what to rebuild per edit; benchmark harnesses re-install per patch |
| F2 | Test subsets are common but fixed per task by dataset authors, not chosen per edit |
| F3 | Benchmark subsets are picked by people or agents; no deterministic rule from the diff found |
| F4 | Speed-up confirmation: three schools, no agreement on statistics |
| F5 | Cumulative re-validation of accepted edits is rare in optimization; common in functional CI |
| F6 | Cheap-first staging is common and is itself a deterministic reduction |
| F7 | Oracle warning: full benchmark verdicts do not repeat across machines (GSO 39/102, SWE-Perf 11/140, SWE-fficiency 411/498 pass all 12 replays); tests let wrong edits through (all 9,483 SemOpt Python candidates pass) |

**Conflict noted.** The brief, the [W2 review](../pm/advisor/review-w2.md) and the PM summary speak of F1–F8. The current [findings.md](../02-practice-survey/findings.md) has F1–F7. The review asked to "promote F8 and F7 to one oracle warning", so F8 was most likely merged into F7 (inferred). Older files ([readiness](../03-experiment/readiness.md) §5) still cite "W2 F8" for oracle repeatability; that content is now F7.

"What nobody in this sample does": per-edit build reduction by rule; per-edit benchmark selection by a deterministic rule from the diff; measured miss rate of per-edit test selection on optimization edits; scheduled checkpoints across accepted optimization edits; build/tests/benchmarks cost split. [findings](../02-practice-survey/findings.md).

## The gap

Study 1 measures where existing deterministic build and test reduction becomes unsafe when edits are performance-motivated and accumulate. Four mechanisms are the main claims; the RQ3 policy follows from them. [beyond-literature-claims](../01-literature/beyond-literature-claims.md); [W1 README](../01-literature/README.md).

## Claims: stand vs struck

| ID | Claim | Status after searches |
|---|---|---|
| C5 | Coverage-based Python RTS cannot see C/Cython edits; no Python measurement of the misses | Stands: not found for Python |
| C7 | No measurement of missed faults as the dependency-refresh interval grows over a chain of edits | Stands, narrowed: partial (Chittimalli & Harrold 2009 covers one step) |
| C11 | No per-edit miss rate for dropping benchmarks by profile/coverage for Python with native code | Stands: partial (ordering studied; Grambow, Ding) |
| C8 | No study of incremental-rebuild correctness for Python extension modules | Stands: not found |
| C1 | No evaluation of a model-free accumulated-change trigger over per-edit reduced checks vs fixed-k at matched cost | Narrowed: conceded as a variant of risk-mass batching |
| C6 | Cumulative drift named, not evaluated against per-edit selection | Supporting, partial; do not promote |
| C3 | No surveyed optimizer reduces the build per candidate | Found by survey (W2), not a literature gap |
| C2 | Per-edit test selection in an LLM loop | Found (PerfAgent); not claimed |
| C4 | No Python benchmark-selection study | **Struck**, folded into C11 |
| C9 | Detection-delay metric | **Struck** (a method choice) |
| C10 | Culprit finding over noisy, dependent edits | **Struck**, deferred (BISCEPTER unread) |
| — | Two-sided "faster and no regression" oracle | **Struck** (SemOpt, PerfAgent have it) |

Novelty means only "not found in our recorded searches": 138 references, ACM DL and IEEE Xplore (123 records screened). Not a systematic review. [gap-and-search-log](../01-literature/gap-and-search-log.md); [database-search](../01-literature/database-search-2026-11-21.md).

## Candidate rules (W1 → W3)

[candidate-rules](../01-literature/candidate-rules.md) v1.1; as implemented in [rules](../03-experiment/rules.md).

| Family | Rules |
|---|---|
| B — build | B1 pure-Python edit → no compile; B2 native edit → rebuild dependents; B3 build-config edit → clean build; B4 clean-vs-incremental differential (invalid as specified, D16); B5 environment pinning; B6 fresh-build guard. W3 adds B0: failed build = reject (D14). |
| F — functional tests | F1 file-level dynamic selection; F2 fallback for non-Python inputs; F3 dependency refresh; F4 always-run set; F5 flaky handling; F6 block/name-level selection; F7 order and isolation check; F8 selector self-check. W3 adds F6-order (D08). |
| P — benchmarks | P1 profile-coverage selection; P2 interleaved A/B; P3 statistical acceptance; P4 dynamic stopping; P5 cumulative drift guard; P6 noise calibration; P7 sentinel set; P8 profile refresh. |
| C — checkpoints | C1 periodic full checkpoint; C2 culprit finding; C3 final full validation; C4 revert semantics; C5 change-triggered checkpoint (RQ3 part c); C6 window record. |

## What is not claimed

A better test selector; per-edit selection in optimization loops; a two-sided gate; periodic full runs; batching or bisection; culprit finding; general safety; generalisation beyond these repos and this laptop; anything about AI selection. [literature-in-one-page](../01-literature/literature-in-one-page.md); [tpm-log](../pm/tpm-log.md) "Must not be claimed".
