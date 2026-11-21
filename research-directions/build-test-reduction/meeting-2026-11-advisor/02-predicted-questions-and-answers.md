# Predicted questions and answers (P01–P20)

**Status:** 2026-11-21. Questions are the advisor model's predictions ([persona](../pm/advisor/persona.md) section 8, AI-SIM/INFER; not the advisor's words). Answers are condensed from repository files; each lists its evidence. Status values: **answered** (evidence exists), **partial** (design or literature exists, part is open), **TODO (W3)** (needs a W3 result). Updated after W3's PRELIMINARY draft results: W3 numbers appear only with W3's labels and a link to the W3 file; see [03-results-summary.md](03-results-summary.md) and its do-not-show table.

Section numbers (§) refer to the file linked on the same line.

| ID | Status | ID | Status |
|---|---|---|---|
| P01 | partial (PRELIMINARY; benchmark pass is a lower bound) | P11 | answered; benefit TODO (W3) |
| P02 | answered | P12 | partial |
| P03 | answered (PRELIMINARY) | P13 | partial (PRELIMINARY) |
| P04 | functional: PRELIMINARY result; slowdowns pending | P14 | partial; B2 design gap (PRELIMINARY) |
| P05 | answered (PRELIMINARY, pure-Python edit) | P15 | partial; latent null stands (0/5) |
| P06 | answered, with a stated limit | P16 | partial (PRELIMINARY) |
| P07 | answered (design); B1 PRELIMINARY | P17 | answered |
| P08 | answered | P18 | answered |
| P09 | answered | P19 | answered |
| P10 | partial | P20 | partial; repeatability not measured |

---

### P01. "How long do a full build, full test and full benchmark run take per edit, and how many edits per session?"

**Answer (PRELIMINARY, single runs).** On networkx (18 replayed edits): build 1.19 s median, serial tests 85.7 s median per edit (6771 tests), about 1700 s of tests over the session. A full benchmark pass is at least 0.89-4.45 h per edit (**lower bound**, import cost only, not a measured pass), so benchmarks are about 40-180x build plus tests (a **cost lower bound** only, import-only, concurrent; no benchmark verdict is claimed). On bottleneck a clean build is 9.9 s against 34.4 s of tests (**noisy**). W2 found no system that reports build seconds per candidate. The measured benchmark pass and idle re-timing run overnight.
**Evidence:** [W3 results.md](../03-experiment/results/results.md) "RQ1"; [rq1_networkx.csv](../03-experiment/results/rq1_networkx.csv); [rq1_bottleneck_build.md](../03-experiment/results/rq1_bottleneck_build.md); [OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md); [W2 at-a-glance table](../02-practice-survey/README.md).
**Status:** partial (PRELIMINARY). Slot: S1 in [results summary](03-results-summary.md).

### P02. "What is new compared with RTS (Ekstazi, STARTS, testmon) and incremental builds?"

**Answer.** We do not propose a better selector. PerfAgent already runs testmon on every optimization iteration, never runs the full suite and reports no misses. The contribution is evidence of when these techniques fail for performance-motivated, accumulating edits: native-extension boundary (C5), stale dependency data (C7), dropped benchmarks (C11), incremental-rebuild correctness (C8). The RQ3 policy follows from those. A manual ACM DL / IEEE Xplore pass found no record anticipating C1, C5, C8 or C11; one 2009 paper narrows C7.
**Evidence:** [W1 README, "What's new"](../01-literature/README.md); [closest-works.md](../01-literature/closest-works.md); [beyond-literature-claims.md](../01-literature/beyond-literature-claims.md); [database-search-2026-11-21.md](../01-literature/database-search-2026-11-21.md).
**Status:** answered (literature). Measurement of the mechanisms is TODO (W3).

### P03. "What does 'build' mean for Python, and why Python?"

**Answer.** Build is a C or Cython extension compile, editable install and bytecode; dependency resolution is excluded. networkx has no build step beyond the editable install, so its build share was expected to be negligible; the PRELIMINARY result below confirms it. bottleneck has four template-generated C extensions built with setuptools `build_ext`, where incremental builds are non-trivial. A cost-only scikit-learn measurement (meson-python plus Cython) is planned. The choice of Python is a charter choice, not an advisor decision.
**Evidence:** [readiness §1.2](../03-experiment/readiness.md); [tpm-log, R1](../pm/tpm-log.md); [persona §5](../pm/advisor/persona.md); [review-w3-readiness](../pm/advisor/review-w3-readiness.md) (P03 row).
**Result (PRELIMINARY):** networkx build is 1.19-2.11% of serial test time, so negligible and reported as such; bottleneck clean build is about 22% of build plus tests, before benchmarks (**noisy** single runs). Evidence: [W3 results.md](../03-experiment/results/results.md); [rq1_bottleneck_build.md](../03-experiment/results/rq1_bottleneck_build.md).
**Status:** answered (PRELIMINARY). Slot S1 in [results summary](03-results-summary.md). Ask: A1 in [01-agenda-and-asks.md](01-agenda-and-asks.md).

### P04. "How do you know the reduced selection did not miss a bug or a slowdown?"

**Answer.** FULL (full build, tests, benchmarks) is the oracle at every state. Faults and slowdowns are injected, frozen and hashed before any selection rule is configured. A mutant counts only if FULL kills it; survivors are reported separately. Results are "k of N missed" with a Wilson 95% interval, and each miss gets a one-line reason. Natural reverts are reported separately from synthetic slowdowns. We never claim "no misses means safe". Known bias (TPM M2): synthetic faults sit in edited functions and must be detected by FULL, so dependency/profile selection catches them almost by construction; RQ3 is therefore headlined as cost at equal detection, with misses on natural reverts reported separately.
**Evidence:** [readiness §4, §4.4](../03-experiment/readiness.md); [tpm-log, R2 and M2](../pm/tpm-log.md); [review-w3-readiness](../pm/advisor/review-w3-readiness.md) (P04 row).
**Result (PRELIMINARY, networkx, functional only; frozen mutants filtered by FULL, not a safety guarantee; simulated; selection catches these almost by construction (M2); N = 20 means a miss rate below 16.1% at 95%, not "safe"):** of 20 FULL-killed mutants, every arm missed 0/20 (95% Wilson CI 0-16.1%) except the changed-module rule, 2/20 (2.8-30.1%), both from test files whose names do not match the module. W3 states the M2 bias: on this fault class selection catches almost everything by construction. Slowdown detection is pending ([OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md)). Evidence: [W3 results.md](../03-experiment/results/results.md) "Fault detection"; [rq2_steps.csv.summary.csv](../03-experiment/results/sim/networkx/rq2_steps.csv.summary.csv).
**Status:** functional result PRELIMINARY; slowdowns pending; no performance verdict before the noise floor exists. Slot: S2 in [results summary](03-results-summary.md).

### P05. "Walk me through one edit: what is rebuilt, which tests run, what time is saved."

**Answer (PRELIMINARY).** networkx step 10, edit `c1c468d5` (one changed function, `_build_paths_from_predecessors`). FULL runs the build and 6768 tests (about 86 s end to end); testmon runs 20 tests, the changed-module rule 28, our rule 38, each about 13.6 s end to end, mostly pytest startup: about 6x, not the 3500x that test execution alone suggests. Benchmarks are pending. It is a pure-Python edit, so it shows no reduced build; the planned bottleneck example is not produced yet.
**Evidence:** [worked-edit.md](../03-experiment/results/worked-edit.md) (with diagram); [readiness §0](../03-experiment/readiness.md).
**Status:** answered (PRELIMINARY). Slot: S4 in [results summary](03-results-summary.md).

### P06. "Where do the edit sequences come from? Are historical commits a realistic session?"

**Answer.** Commits are mined by a deterministic subject-line regex, frozen before any run, and replayed in history order onto one base tree; all hits in the window are used and drops happen only by rule. bottleneck has 17 `PERF:` commits in one burst (2019-09 to 2020-11), the closest public history to a real step-by-step session. A replay of independent commits is not a recorded session (threat T1), and we claim no session effect.
**Evidence:** [readiness §1.3, §2, §6](../03-experiment/readiness.md); [tpm-log, charter observation 3](../pm/tpm-log.md).
**Status:** answered, with the limit stated. Ask: A2 and A8 in [01-agenda-and-asks.md](01-agenda-and-asks.md).

### P07. "How is 'stays optimized' checked, and are benchmarks also reduced?"

**Answer.** Performance is checked with the asv rule (ratio above 1.1 and Mann-Whitney p below 0.002) against the original base and against the previous accepted state, and only above the measured noise floor. Benchmarks are reduced in the arms: all benchmarks (FULL, incremental), file-name rule (A3), static call-graph rule (A5), and profile/call-graph selection (A4, RQ3 part b). Dropping benchmarks is claim C11.
**Evidence:** [readiness §3, §4.2, §5](../03-experiment/readiness.md); [CHARTER definitions](../pm/CHARTER.md); [beyond-literature-claims.md](../01-literature/beyond-literature-claims.md).
**Result (PRELIMINARY, counts only; S0 profiles):** B1: for 12 of the 18 networkx edits, no benchmark case executes any changed function, so W3 notes that "even FULL benchmarking cannot confirm the claimed speed-up of most of these commits with the project's own suite". No benchmark verdict is shown (no A/A noise floor yet). Evidence: [W3 results.md](../03-experiment/results/results.md) "Finding B1". Ask: A13 in [01-agenda-and-asks.md](01-agenda-and-asks.md).
**Status:** answered (design); B1 PRELIMINARY. The asv defaults are still to be verified against the asv source (readiness §4.2).

### P08. "How do SemOpt, SWE-Perf, GSO and others validate each candidate, and what does it cost?"

**Answer.** W2 covers 28 systems. Among iterative optimizers, SemOpt does one compile/install, the whole unit suite (inferred; selection not described) and six runs of the project performance tests per candidate; PerfAgent runs testmon-selected tests per edit; Codeflash does no build. Benchmark harnesses (GSO, SWE-fficiency) re-install and time far more per patch for isolation. No surveyed system reports build seconds per candidate (W2); the framing of this as a finding is from the AI-written W2 review.
**Evidence:** [W2 README table](../02-practice-survey/README.md); [findings.md](../02-practice-survey/findings.md); [survey-table.md](../02-practice-survey/survey-table.md); [review-w2](../pm/advisor/review-w2.md).
**Status:** answered.

### P09. "Four RQs is too many for 'step by step'."

**Answer.** The charter was revised on 2026-11-21 to three RQs. The two literature questions (how optimizers validate, what techniques exist) became background chapters W1 and W2. If time runs short, a cut order is fixed in advance (sqlglot first, wall-time repeats, some ablations).
**Evidence:** [CHARTER](../pm/CHARTER.md) (revised RQs); [review-charter §3](../pm/advisor/review-charter.md); [readiness §8](../03-experiment/readiness.md).
**Status:** answered.

### P10. "What is Study 2 (AI), and how do Study 1's rules feed it?"

**Answer.** The charter says AI-based selection is explicitly a later study and Study 1 sets the deterministic baseline and its limits. The concrete hand-off is not decided. An AI-written proposal suggests: rules, benchmark harness and a measured cost/safety frontier, with a note that learned selection already exists (predictive test selection, Machalica et al., ICSE-SEIP 2019, listed as known in the database search).
**Evidence:** [CHARTER, "Problem"](../pm/CHARTER.md); [review-charter §2, Q10](../pm/advisor/review-charter.md); [database-search-2026-11-21.md](../01-literature/database-search-2026-11-21.md).
**Status:** partial. Ask: A9 in [01-agenda-and-asks.md](01-agenda-and-asks.md).

### P11. "Periodic full checks: how often, and is this not just CI batching?"

**Answer.** Largely yes, and we say so. Periodic full runs (Meta, Google) and batching, bisection and risk-based batch size (Najafi, Fallahzadeh, Sayedsalehi) are not claimed. Our trigger is a model-free variant of Sayedsalehi's risk-mass batching. Claim C1 is narrowed to a model-free accumulated-change trigger on top of a per-edit reduced check, against fixed-k batching at matched cost. The frequency is a fixed parameter (k in {3,5} for the draft; trigger T = 10 with sensitivity {5,10,20}), reported as curves, never tuned on the frozen faults.
**Evidence:** [W1 README](../01-literature/README.md); [literature-in-one-page.md](../01-literature/literature-in-one-page.md); [readiness §3](../03-experiment/readiness.md).
**Status:** answered (positioning). Whether the trigger beats fixed-k is TODO (W3, RQ3).

### P12. "What are the timeline and target venue for Study 1?"

**Answer.** Not known. The repository records no venue or timeline decision. The W3 schedule covers the experiment only (about 36 hours from sign-off).
**Evidence:** [persona §6, §7](../pm/advisor/persona.md); [readiness §8](../03-experiment/readiness.md).
**Status:** partial. Ask: A10 in [01-agenda-and-asks.md](01-agenda-and-asks.md).

### P13. "On networkx, testmon already does this for pure Python. What does your rule add?"

**Answer.** Per-edit test selection is not our contribution; PerfAgent already uses testmon per edit, and arm A2 runs it as shipped. On networkx the added value has to come from benchmark selection and the accumulation/checkpoint policy, not test selection. networkx is a pilot, and its build share is measured as negligible (PRELIMINARY).
**Evidence:** [readiness §1.2, §3](../03-experiment/readiness.md); [review-w3-readiness](../pm/advisor/review-w3-readiness.md).
**Result (PRELIMINARY):** on networkx, testmon is about 4x cheaper than FULL end to end (404 s measured, **concurrent, pinned**, against 1634 s serial with 1 noisy state) and detects 20/20 frozen mutants (filtered by FULL; not a safety guarantee; simulated; selection catches these almost by construction (M2); N = 20 means a miss rate below 16.1% at 95%, not "safe"); at equal detection it is cheaper than our policy (330 s against 655 s est.). W3: "our policy's extra cost buys no extra functional detection"; any value lies in latent faults, benchmark selection and as a backstop for weaker rules, all pending. Evidence: [W3 results.md](../03-experiment/results/results.md) "RQ2/RQ3".
**Status:** partial (PRELIMINARY). Slots S2, S3 in [results summary](03-results-summary.md).

### P14. "Profile-based benchmark selection is just coverage-based performance-test selection."

**Answer.** The design anticipates this. Arm A5 applies an existing static dependency rule (STARTS-style) to benchmarks for the current edit, and profile/call-graph selection (P1) must beat A5, not only the file-name rule. The literature mostly orders benchmarks rather than dropping them; coverage of the change is not sufficient (Ding, ICSE'20: 74–77% of covering tests show no known speed-up), and a per-edit miss rate for Python was not found. The STARTS reference is marked to-verify in readiness.
**Evidence:** [readiness §3](../03-experiment/readiness.md); [W1 one-pager](../01-literature/literature-in-one-page.md) (C11); [beyond-literature-claims.md](../01-literature/beyond-literature-claims.md).
**Status:** partial (PRELIMINARY, counts only). A5 static reach selects 61% of benchmark cases (1893/3078). B2: as specified, A4's profile rule collapses to all 171 cases from step 3 on, because only S0 profiles exist and checkpoint re-profiling is not done (a design gap, not a selection result). A labelled variant that reuses S0 profiles (violating P8) selects 889 cases in total. Whether any selection misses a regression is pending ([OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md)). Evidence: [W3 results.md](../03-experiment/results/results.md) "Finding B2". Slot S3 in [results summary](03-results-summary.md).

### P15. "Why would accumulation matter if each fault is in the changed function?"

**Answer.** Accumulation can only help when a fault is invisible at the step that introduces it and becomes visible after a later edit, or when the dependency map is stale. W3 therefore adds about five latent faults per repo. It is pre-registered that if fewer than three latent faults exist per repo, the accumulation ablation is expected to show no effect and will be reported as such, not as evidence for or against accumulation.
**Evidence:** [readiness §4.1b](../03-experiment/readiness.md); [review-w3-readiness](../pm/advisor/review-w3-readiness.md); [assumptions-under-iterative-optimization.md](../01-literature/assumptions-under-iterative-optimization.md).
**Status:** partial. PRELIMINARY: accumulation adds 494 test runs (+3 est. test-s) and changes no detection on the in-function mutants; the latent-fault re-check found 0 of the 5 FULL survivors detectable at any later state, so the pre-registered null stands (no effect expected; not evidence for or against accumulation); caller faults were not generated. C7: 62 of 2589 functions (2.4%) get different test sets in repeat runs of the same code ([W3 results.md](../03-experiment/results/results.md) "C7 finding"). Slot S3 in [results summary](03-results-summary.md).

### P16. "Isn't the accumulated-change trigger just batching with a variable batch size?"

**Answer.** Conceded as a model-free variant of risk-mass batching. The only claim is C1 as narrowed. The test is ablation (c), accumulated-change trigger against a fixed period k = 5, at matched cost. Ablation (c) is among the items cut if the schedule slips.
**Evidence:** [W1 README](../01-literature/README.md); [beyond-literature-claims.md](../01-literature/beyond-literature-claims.md); [readiness §3, §8](../03-experiment/readiness.md); [review-w1-v2](../pm/advisor/review-w1-v2.md).
**Status:** partial. PRELIMINARY: the score trigger currently behaves like a periodic full check at k of about 4 (fired at steps 3, 5, 8, 13 plus final), costing 655 s est., between testmon + full every k=5 (594 s) and testmon + full every k=3 (735 s), with equal detection ([W3 results.md](../03-experiment/results/results.md)). Cap-only and additive-budget comparators are not run. Slot S3 in [results summary](03-results-summary.md).

### P17. "Why testmon and not NameRTS as the Python baseline?"

**Answer.** NameRTS (arXiv 2605.25356) is the strongest Python selector found (reported -45.6% time, safe on 99.6% of commits). Its code is a replication package: each project needs a hand-built environment and no documented command runs it on a pytest repository. Nobody here has run it. It is a planned post-meeting comparator, not run before the meeting.
**Evidence:** [W1 README, "NameRTS as a comparator"](../01-literature/README.md); [literature-in-one-page.md](../01-literature/literature-in-one-page.md); [readiness §3](../03-experiment/readiness.md).
**Status:** answered. Ask: A7 in [01-agenda-and-asks.md](01-agenda-and-asks.md).

### P18. "How does PerfAgent validate each edit, and does it report misses?" (closest work)

**Answer.** One `/build.sh` per edit (incremental or not is unknown), testmon-selected tests per edit, one timed run and a profile. It never runs the full suite inside the loop and reports no misses. Its authors say native-extension regressions can slip between iterations (section VI). No public code was found.
**Evidence:** [W2 PerfAgent note](../02-practice-survey/per-system/perfagent.md); [W2 README table](../02-practice-survey/README.md); [W1 one-pager](../01-literature/literature-in-one-page.md).
**Status:** answered.

### P19. "Benchmark harnesses rebuild per patch for isolation, so that is not a gap."

**Answer.** Agreed. Repository-level harnesses score one final patch per task in a fresh container, on purpose. The relevant population is the iterative optimizers. Among them, W2 found none that decides by rule what to rebuild; that repeated install equals full build cost is inferred, not measured, and W3 measures it. Per-edit benchmark selection does happen ad hoc (human or agent chosen); what was not found is a deterministic rule derived from the diff.
**Evidence:** [review-w2](../pm/advisor/review-w2.md) (challenges 1–3); [W2 README headline 1–3](../02-practice-survey/README.md); [findings.md](../02-practice-survey/findings.md).
**Status:** answered.

### P20. "If the full benchmark verdict is not repeatable, how can you count misses?"

**Answer.** We do not count a miss where FULL's own verdict is unstable. The full asv-rule decision is re-run at least three times, interleaved, on a fixed subset of states; reduced-arm misses on oracle-unstable (state, benchmark) pairs are labelled "oracle-unstable" and reported separately. The motivating literature is arXiv 2607.01211, summarised in W2 (headline 5 and finding F7).
**Evidence:** [readiness §5, "Oracle repeatability"](../03-experiment/readiness.md); [W2 README, headline 5](../02-practice-survey/README.md); [findings.md](../02-practice-survey/findings.md).
**Status:** partial. No benchmark repeatability result yet; the oracle-repeatability rule is not in the overnight queue ([OVERNIGHT.md](../03-experiment/results/OVERNIGHT.md)). Slot S5 in [results summary](03-results-summary.md).
