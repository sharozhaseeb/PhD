# Predicted questions and answers (M1–M8, P01–P20)

**Status:** 2026-11-21, updated 2026-11-23. Questions are the advisor model's predictions ([persona](../pm/advisor/persona.md) section 8, AI-SIM/INFER; not the advisor's words). Answers are condensed from repository files; each lists its evidence. Status values: **answered** (evidence exists), **partial** (design or literature exists, part is open), **TODO (W3)** (needs a W3 result). Updated after W3's PRELIMINARY draft results: W3 numbers appear only with W3's labels and a link to the W3 file; see [03-results-summary.md](03-results-summary.md), sections "What may be shown" and "Superseded figures".

Section numbers (§) refer to the file linked on the same line.

| ID | Status | ID | Status |
|---|---|---|---|
| P01 | answered (PRELIMINARY; noisy single runs) | P11 | answered; PRELIMINARY (no benefit shown) |
| P02 | answered | P12 | partial |
| P03 | answered (PRELIMINARY) | P13 | partial (PRELIMINARY) |
| P04 | PRELIMINARY: functional 0/20 (simulated); regression safety not measurable | P14 | partial; B2 design gap (PRELIMINARY) |
| P05 | answered (PRELIMINARY, pure-Python edit) | P15 | partial; latent null stands (0/5) |
| P06 | answered, with a stated limit | P16 | partial (PRELIMINARY) |
| P07 | answered (design); B1 PRELIMINARY | P17 | answered |
| P08 | answered | P18 | answered |
| P09 | answered | P19 | answered |
| P10 | partial | P20 | partial; floor applied, 12/14 repeat, directory confound open |

## Most likely questions for the meeting (updated 2026-11-23)

IDs P23–P29 refer to the advisor-persona hit-list ([review-new-results](../pm/advisor/review-new-results.md), "Hit-list updates"). Sources: the advisor-persona reviews [review-paper-draft-1](../pm/advisor/review-paper-draft-1.md) §6, [review-new-results](../pm/advisor/review-new-results.md) (b) and [review-final-results](../pm/advisor/review-final-results.md) §4 (all AI-SIM, a model of the advisor, not the advisor). The earlier N1–N5 and Q1–Q5 rehearsal questions are merged here, with answers updated to the 2026-11-23 results. Every number is from [03-results-summary.md](03-results-summary.md) and the files it cites.

**M1. "Did you read the 14 diffs yourself? Would you put your name on each label?"** (P26)
No. The 14 optimization labels come from two blind agent raters plus an agent adjudicator against a frozen codebook (κ 0.948, likely inflated because the raters are the same model); no human read the diffs. Mining precision of the keyword rule by these labels is 50/70 = 71% [60–81%] pooled. The owner decided the labels stay agent-only (D26); the advisor-persona review will not accept that for E1 and asks for a blind human-labelled subset with a human-agent κ. This is an open disagreement for the meeting (ask A14).
Evidence: [findings.md](../knowledge-base/findings.md) B4; [precision_b1.json](../03-experiment/results/labelling/precision_b1.json); [review-paper-draft-1](../pm/advisor/review-paper-draft-1.md) §3 C6. Slot S2.

**M2. "Is B1 a networkx problem or a general one? How many projects have you checked?"** (P23)
One project. On networkx, 8 of 14 agent-labelled optimizations are executed by no benchmark (measured S0 profile; 57%, Wilson 33–79%; static reach 3/14). Outside networkx, B1 was **not validly tested** (not "did not replicate"): static reach from one old base is not a bound (geopandas), pvlib's base has no asv suite, and bottleneck's template code gives 4/8 or 0/8 depending on the reading. The replication (E1) comes first after the meeting; the advisor-persona bar is at least 4–5 projects and 50–60 true optimizations, with profiles at each edit's parent.
Evidence: [findings.md](../knowledge-base/findings.md) B4, B3; [results.md](../03-experiment/results/results.md) "Q3". Slot S2; ask A13.

**M3. "For the edits a benchmark does execute, what share of the case's time is the changed function? How many could the suite actually see?"**
Computed now (no timing): of the 14 edits, 8 are not executed and 1 (step 4) is executed but diluted (share 0.021). **At a 1.2× slowdown of the changed function at most 4 of 14 edits can even clear asv's 1.1 ratio; at 2×, 5 of 14.** The share effect is Amdahl's law applied to a benchmark case; what is new is measuring it per edit. Slowdown #3 shows it directly: share about 0.005, so a dilution miss.
Evidence: [findings.md](../knowledge-base/findings.md) V1, V2; [edit_share.json](../03-experiment/results/raw/networkx/edit_share.json). Slot S2.

**M4. "What is your noise floor, and can your oracle see the slowdowns that matter? Why believe #2 and #8?"** (P20, P29)
σ_noise is now measured for the 12 flagged verdicts (120 runs, 5 repeats, ABBA) and the pre-registered 1 + 3σ floor is applied: **FULL detects 1 of 10 slowdowns above the floor (Wilson 1.8–40.4%)**, 2 by asv's rule alone. Only #2 (1.81–1.90× on 8 on-target cases) survives; #8 (floor 2.18) does not, and its own A/A pooled also reads "slower". Repeated, 12 of 14 verdicts agree; the two off-target flags do not repeat. At the verdict design the heavy module reliably resolves only about 1.5× and above (power 0.84 at 1.5×). A second repeat found 2.2% off-target flips with edit and clone directory fully confounded; a directory A/A and directory rotation start tonight (D28). The pre-registered primary result stands: regression safety of reduced selection is not measurable on networkx with the frozen set.
Evidence: [findings.md](../knowledge-base/findings.md) N9, N10, N11, N14. Slots S2, S7.

**M5. "#9 flagged reach-based selection as unsafe. Is it?"**
The flag does **not** survive the pre-registered noise floor (1.130 against a floor of 1.140, read as "at the floor"), so it is no longer a finding. The completeness check also covered only the 5 slowdowns no benchmark reaches, so it was never a safety rate.
Evidence: [findings.md](../knowledge-base/findings.md) N9, P5. Slot S2.

**M6. "Your benchmark cost moves during the day. Which number is R1?"** (P28)
A range, never one pass. networkx: 659–2,984 s over 9 passes, median about 1,220 s, so at least about 8×, median about 14×, up to about 34× build plus tests; 8 of 9 passes are labelled noisy. The timing loops (132–171 s) and the tests are stable; the drift (2.45× within one evening) sits in one module's per-process setup, cause unknown. bottleneck is a second project: about 18.5–19×, two passes 0.5% apart.
Evidence: [findings.md](../knowledge-base/findings.md) R1, N12, N13, R5; [numbers.tex](../04-paper/generated/numbers.tex) `NxBenchPassMedian`. Slot S1.

**M7. "If the setup-cached pass comes back at 1.5× build plus tests, what is left of 'expensive', and what is the paper about?"** (P24, P25)
The estimate is already about 1.5–2× (not measured; E5 runs the night of 23→24). If it holds, benchmarks stay the largest single part but not by an order of magnitude, and the cost half becomes motivation; the visibility half (executed, visible, detectable) stands on its own. The draft title already avoids "expensive".
Evidence: [results.md](../03-experiment/results/results.md) "RQ1 headline"; [review-paper-draft-1](../pm/advisor/review-paper-draft-1.md) §4, §6. Slots S1, S8.

**M8. "Your mutants sit in the edited functions, so every selector catches them. And your policy adds nothing. So what is Study 1's contribution, and does it go beyond the literature?"** (P25)
Agreed on the fault model: it cannot rank selection rules (M2 bias), and A4 as implemented costs more than testmon and about 2× batching once benchmarks count. The contribution is a cost characterization (benchmarks dominate on two projects; build is a minor lever; testmon is a 3.5–4× end-to-end win) plus the measured oracle gap on networkx: coverage, share and power. Novelty is narrowed: Traini et al. (TOSEM 2021) already profile per commit which methods benchmarks execute, but report no uncovered-commit rate; Peass and Laaber & Leitner split misses into uncovered and below-noise. What is ours is the measured rate for optimization commits, and generalisation is untested until E1.
Evidence: [beyond-literature-claims.md](../01-literature/beyond-literature-claims.md) row B1; [results summary](03-results-summary.md) story; [review-paper-draft-1](../pm/advisor/review-paper-draft-1.md) §4. Asks A5, A13.

---

### P01. "How long do a full build, full test and full benchmark run take per edit, and how many edits per session?"

**Answer (PRELIMINARY).** networkx (18 replayed edits): build 1.19 s median, serial tests 85.7 s median per edit (6771 tests), about 1700 s of tests over the session. A FULL benchmark pass (171 cases, 2 processes × 3 values) took 659–2,984 s over 9 passes, median about 1,220 s: at least about 8×, median about 14×, up to about 34× build plus serial tests (cost only; 8 of 9 passes noisy; drift in one module's setup, cause unknown). bottleneck: two FULL benchmark passes at 544 and 547 s, about 18.5–19× build plus tests; its clean build is about 16–18% of build plus tests but 0.8–0.9% once benchmarks count. W2 found no system that reports build seconds per candidate. [findings.md](../knowledge-base/findings.md) R1, N12, R5.
**Evidence:** [W3 results.md](../03-experiment/results/results.md) "RQ1 headline" and "RQ1"; [rq1_networkx.csv](../03-experiment/results/rq1_networkx.csv); [W2 at-a-glance table](../02-practice-survey/README.md).
**Status:** answered (PRELIMINARY). Slot: S1 in [results summary](03-results-summary.md).

### P02. "What is new compared with RTS (Ekstazi, STARTS, testmon) and incremental builds?"

**Answer.** We do not propose a better selector. PerfAgent already runs testmon on every optimization iteration, never runs the full suite and reports no misses. The contribution is evidence of when these techniques fail for performance-motivated, accumulating edits: native-extension boundary (C5), stale dependency data (C7), dropped benchmarks (C11), incremental-rebuild correctness (C8). The RQ3 policy follows from those. A manual ACM DL / IEEE Xplore pass found no record anticipating C1, C5, C8 or C11; one 2009 paper narrows C7.
**Evidence:** [W1 README, "What's new"](../01-literature/README.md); [closest-works.md](../01-literature/closest-works.md); [beyond-literature-claims.md](../01-literature/beyond-literature-claims.md); [database-search-2026-11-21.md](../01-literature/database-search-2026-11-21.md).
**Status:** answered (literature). PRELIMINARY measurements exist for C7, C8 and B1/C11 (slots S2, S4, S5 in the [results summary](03-results-summary.md)); C5 is not measured.

### P03. "What does 'build' mean for Python, and why Python?"

**Answer.** Build is a C or Cython extension compile, editable install and bytecode; dependency resolution is excluded. networkx has no build step beyond the editable install, so its build share was expected to be negligible; the PRELIMINARY result below confirms it. bottleneck has four template-generated C extensions built with setuptools `build_ext`, where incremental builds are non-trivial. A cost-only scikit-learn measurement (meson-python plus Cython) was planned and is not reported. The choice of Python is a charter choice, not an advisor decision.
**Evidence:** [readiness §1.2](../03-experiment/readiness.md); [tpm-log, R1](../pm/tpm-log.md); [persona §5](../pm/advisor/persona.md); [review-w3-readiness](../pm/advisor/review-w3-readiness.md) (P03 row).
**Result (PRELIMINARY):** networkx build is 1.19–2.11% of serial test time, so negligible; bottleneck clean build is about 16–18% of build plus tests on the amended base (**noisy**), but 0.8–0.9% of total per-edit validation once benchmarks count, so reduced build is a minor lever in both projects. A failed build is a reject (rule B0), a harness lesson from one replayed state. Evidence: [W3 results.md](../03-experiment/results/results.md) "Bottleneck", "(c) Two FULL asv benchmark passes for bottleneck"; [build-hazard-iterators-h.md](../03-experiment/results/build-hazard-iterators-h.md).
**Status:** answered (PRELIMINARY). Slot S1 in [results summary](03-results-summary.md). Ask: A1 in [01-agenda-and-asks.md](01-agenda-and-asks.md).

### P04. "How do you know the reduced selection did not miss a bug or a slowdown?"

**Answer.** FULL (full build, tests, benchmarks) is the oracle at every state. Faults and slowdowns are injected, frozen and hashed before any selection rule is configured. A mutant counts only if FULL kills it; survivors are reported separately. Results are "k of N missed" with a Wilson 95% interval, and each miss gets a one-line reason. (Planned: natural reverts reported separately from synthetic slowdowns; none were measured in the pilot.) We never claim "no misses means safe". Known bias (TPM M2): synthetic faults sit in edited functions and must be detected by FULL, so dependency/profile selection catches them almost by construction; RQ3 is therefore headlined as cost at equal detection, with misses on natural reverts reported separately.
**Evidence:** [readiness §4, §4.4](../03-experiment/readiness.md); [tpm-log, R2 and M2](../pm/tpm-log.md); [review-w3-readiness](../pm/advisor/review-w3-readiness.md) (P04 row).
**Result (PRELIMINARY, networkx, functional only; frozen mutants filtered by FULL, not a safety guarantee; simulated; selection catches these almost by construction (M2); N = 20 means a miss rate below 16.1% at 95%, not "safe"):** of 20 FULL-killed mutants, every arm missed 0/20 (95% Wilson CI 0-16.1%) except the changed-module rule, 2/20 (2.8-30.1%), both from test files whose names do not match the module. W3 states the M2 bias: on this fault class selection catches almost everything by construction. Slowdowns: above the pre-registered 1 + 3σ noise floor FULL detects **1 of 10** frozen slowdowns (Wilson 1.8–40.4%; 2 by asv's rule alone), so the pre-registered result is that **regression safety is not measurable** on networkx with the frozen set. 7 of the 10 slowed functions are run by no benchmark, and #3 is a dilution miss. The profile-completeness flag on #9 does not survive the floor. [findings.md](../knowledge-base/findings.md) N9, V1. Evidence: [W3 results.md](../03-experiment/results/results.md) "Fault detection", "Slowdown oracle"; [LABELS.md](../03-experiment/results/raw/networkx/bench/LABELS.md); [rq2_steps.csv.summary.csv](../03-experiment/results/sim/networkx/rq2_steps.csv.summary.csv).
**Status:** PRELIMINARY. Functional counts shown; regression safety not measurable; A/A noise floor measured with limits. Slots S2, S3 in [results summary](03-results-summary.md).

### P05. "Walk me through one edit: what is rebuilt, which tests run, what time is saved."

**Answer (PRELIMINARY).** networkx step 10, edit `c1c468d5` (one changed function, `_build_paths_from_predecessors`). FULL runs the build and 6768 tests (about 86 s end to end); testmon runs 20 tests, the changed-module rule 28, and the A4 single-edit view (no accumulation, S0 data) 38, each about 13.6 s end to end, mostly pytest startup: about 6x, not the 3500x that test execution alone suggests. Benchmark cost: FULL, testmon and static reach run all 171 cases (about 1668 s est., noisy S0 pass); the A4 single-edit view runs 1 case. In the session simulation A4 runs 71 tests and 171 cases at this step (B2). It is a pure-Python edit, so it shows no reduced build; the bottleneck build hazard is in S5.
**Evidence:** [worked-edit.md](../03-experiment/results/worked-edit.md) (with diagram); [readiness §0](../03-experiment/readiness.md).
**Status:** answered (PRELIMINARY). Slot: S6 in [results summary](03-results-summary.md).

### P06. "Where do the edit sequences come from? Are historical commits a realistic session?"

**Answer.** Commits are mined by a deterministic subject-line regex, frozen before any run, and replayed in history order onto one base tree; all hits in the window are used and drops happen only by rule. bottleneck has 17 `PERF:` commits in one burst (2019-09 to 2020-11), the closest public history to a real step-by-step session. A replay of independent commits is not a recorded session (threat T1), and we claim no session effect.
**Evidence:** [readiness §1.3, §2, §6](../03-experiment/readiness.md); [tpm-log, charter observation 3](../pm/tpm-log.md).
**Status:** answered, with the limit stated. Ask: A2 and A8 in [01-agenda-and-asks.md](01-agenda-and-asks.md).

### P07. "How is 'stays optimized' checked, and are benchmarks also reduced?"

**Answer.** Performance is checked with the asv rule (ratio above 1.1 and Mann-Whitney p below 0.002) against the original base and against the previous accepted state, and only above the measured noise floor. Benchmarks are reduced in the arms: all benchmarks (FULL, incremental), file-name rule (A3), static call-graph rule (A5), and profile/call-graph selection (A4, RQ3 part b). Dropping benchmarks is claim C11.
**Evidence:** [readiness §3, §4.2, §5](../03-experiment/readiness.md); [CHARTER definitions](../pm/CHARTER.md); [beyond-literature-claims.md](../01-literature/beyond-literature-claims.md).
**Result (PRELIMINARY, counts only; S0 profiles):** B1: 8 of the 14 agent-labelled optimizations (57%, Wilson 33–79%; earlier 9/15 by subject-only reading) change no function any benchmark executes, so for many of them the project's own suite cannot confirm the claimed speed-up. Of the rest, the changed function's share of case time limits visibility: at a 1.2× function slowdown at most 4 of 14 edits can clear asv's 1.1 ratio. Above the noise floor FULL detects 1 of 10 frozen slowdowns, so the pre-registered result is that regression safety is not measurable with the frozen set. Evidence: [findings.md](../knowledge-base/findings.md) B4, V2, N9. Ask: A13 in [01-agenda-and-asks.md](01-agenda-and-asks.md).
**Status:** answered (design); B1 PRELIMINARY. The asv source was read on 2026-11-22 ([results.md](../03-experiment/results/results.md) "Exact-test recompute").

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
**Status:** answered (positioning). PRELIMINARY: the trigger behaves like fixed k of about 4 and fires at the same steps as additive-budget batching. (a) Design limitation: with mutants in edited functions every per-edit arm catches everything at injection, so detection cannot separate trigger from batching. (b) A4 as implemented costs more: with benchmarks counted batching is 1.7–6× cheaper, A4 about 2× at matched cost (depends on B2). Regression detection per arm is not simulated (slot S4).

### P12. "What are the timeline and target venue for Study 1?"

**Answer.** Not known. The repository records no venue or timeline decision. The W3 schedule covers the experiment only (about 36 hours from sign-off).
**Evidence:** [persona §6, §7](../pm/advisor/persona.md); [readiness §8](../03-experiment/readiness.md).
**Status:** partial. Ask: A10 in [01-agenda-and-asks.md](01-agenda-and-asks.md).

### P13. "On networkx, testmon already does this for pure Python. What does your rule add?"

**Answer.** Per-edit test selection is not our contribution; PerfAgent already uses testmon per edit, and arm A2 runs it as shipped. On networkx any added value had to come from benchmark selection and the accumulation/checkpoint policy, not test selection; PRELIMINARY: none is shown on this data. networkx is a pilot, and its build share is measured as negligible (PRELIMINARY).
**Evidence:** [readiness §1.2, §3](../03-experiment/readiness.md); [review-w3-readiness](../pm/advisor/review-w3-readiness.md).
**Result (PRELIMINARY):** on networkx, testmon is 3.5-4x cheaper than FULL end to end (mixed load: 404 s measured **concurrent, pinned**, against 1634 s first runs incl. 1 noisy state or 1413 s re-runs, **noisy**) and detects 20/20 frozen mutants (filtered by FULL; not a safety guarantee; simulated; selection catches these almost by construction (M2); N = 20 means a miss rate below 16.1% at 95%, not "safe"); at equal detection it is cheaper than our policy (330 s against 655 s est.). W3: "our policy's extra cost buys no extra functional detection"; latent faults are 0/5 on networkx, and regression safety of benchmark selection is not measurable with the frozen set. Evidence: [W3 results.md](../03-experiment/results/results.md) "RQ2/RQ3".
**Status:** partial (PRELIMINARY). Slots S3, S4 in [results summary](03-results-summary.md).

### P14. "Profile-based benchmark selection is just coverage-based performance-test selection."

**Answer.** The design anticipates this. Arm A5 applies an existing static dependency rule (STARTS-style) to benchmarks for the current edit, and profile/call-graph selection (P1) must beat A5, not only the file-name rule. The literature mostly orders benchmarks rather than dropping them; coverage of the change is not sufficient (Ding, ICSE'20: 74–77% of covering tests show no known speed-up), and a per-edit miss rate for Python was not found. The STARTS reference is marked to-verify in readiness.
**Evidence:** [readiness §3](../03-experiment/readiness.md); [W1 one-pager](../01-literature/literature-in-one-page.md) (C11); [beyond-literature-claims.md](../01-literature/beyond-literature-claims.md).
**Status:** partial (PRELIMINARY, counts only). A5 static reach selects 61% of benchmark cases (1893/3078). B2: as specified, A4's profile rule collapses to all 171 cases from step 3 on, because only S0 profiles exist and checkpoint re-profiling is not done (a design gap, not a selection result). A labelled variant that reuses S0 profiles (violating P8) selects 889 cases in total. Regression safety of reduced selection is not measurable on networkx with the frozen set (pre-registered result); the per-arm regression simulation is not run. Evidence: [W3 results.md](../03-experiment/results/results.md) "Finding B2". Slot S4 in [results summary](03-results-summary.md).

### P15. "Why would accumulation matter if each fault is in the changed function?"

**Answer.** Accumulation can only help when a fault is invisible at the step that introduces it and becomes visible after a later edit, or when the dependency map is stale. W3 planned about five latent faults per repo; in the pilot the latent check used the 5 FULL-surviving mutants, and no further latent faults were added. It is pre-registered that if fewer than three latent faults exist per repo, the accumulation ablation is expected to show no effect and will be reported as such, not as evidence for or against accumulation.
**Evidence:** [readiness §4.1b](../03-experiment/readiness.md); [review-w3-readiness](../pm/advisor/review-w3-readiness.md); [assumptions-under-iterative-optimization.md](../01-literature/assumptions-under-iterative-optimization.md).
**Status:** partial. PRELIMINARY: accumulation adds 494 test runs (+3 est. test-s) and changes no detection on the in-function mutants; the latent-fault re-check found 0 of the 5 FULL survivors detectable at any later state, so the pre-registered null stands (no effect expected; not evidence for or against accumulation); caller faults were not generated. C7: 62 of 2589 functions (2.4%) get different test sets in repeat runs of the same code ([W3 results.md](../03-experiment/results/results.md) "C7 finding"). Slot S4 in [results summary](03-results-summary.md).

### P16. "Isn't the accumulated-change trigger just batching with a variable batch size?"

**Answer.** Conceded as a model-free variant of risk-mass batching. The only claim is C1 as narrowed. The test is ablation (c), accumulated-change trigger against a fixed period k = 5, at matched cost. Ablation (c) is among the items cut if the schedule slips.
**Evidence:** [W1 README](../01-literature/README.md); [beyond-literature-claims.md](../01-literature/beyond-literature-claims.md); [readiness §3, §8](../03-experiment/readiness.md); [review-w1-v2](../pm/advisor/review-w1-v2.md).
**Status:** partial. PRELIMINARY: the score trigger currently behaves like a periodic full check at k of about 4 (fired at steps 3, 5, 8, 13 plus final), costing 655 s est., between testmon + full every k=5 (594 s) and testmon + full every k=3 (735 s), with equal functional detection (0/20, simulated; regression detection per arm not simulated) ([W3 results.md](../03-experiment/results/results.md)). C5 batching comparators (done, simulated): the per-edit catch is by construction (M2), so the design cannot tell selection rules apart; separately, A4 as implemented costs more, and with benchmarks counted batching is 1.7–6× cheaper than every per-edit benchmark arm, A4 about 2× (depends on B2). No "A4 beats batching" claim ([W3 results.md](../03-experiment/results/results.md) "RQ3 — C5 batching comparators"). Slot S4 in [results summary](03-results-summary.md).

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

**Answer.** Done in part. The verdicts that matter were repeated: E3 tier 1 (14 verdict-relevant cases, 4 repeats) agrees on 12 of 14, and the two disagreements are the off-target flags turning "same"; E3 tier 2 (2 repeats) agrees on 488 of 499 but shows 2.2% off-target flips with edit and clone directory confounded, so a directory A/A runs tonight. σ is measured for the 12 flagged verdicts and the 1 + 3σ floor applied ([findings.md](../knowledge-base/findings.md) N9, N11, N14). The motivating literature is arXiv 2607.01211, summarised in W2 (headline 5 and finding F7).
**Evidence:** [readiness §5, "Oracle repeatability"](../03-experiment/readiness.md); [W2 README, headline 5](../02-practice-survey/README.md); [findings.md](../02-practice-survey/findings.md).
**Status:** partial, much advanced. A/A on 23 cases: 0/46 false verdicts (optimistic). σ measured for the 12 flagged verdicts and the 1 + 3σ floor applied: FULL detects 1 of 10. Repeat (E3 tier 1): 12 of 14 verdicts agree; the two off-target flags do not repeat. Tier 2: 2.2% off-target flips with edit and clone directory confounded; a directory A/A and directory rotation start tonight (D28). [findings.md](../knowledge-base/findings.md) N6, N9, N11, N14. Slot S7 in [results summary](03-results-summary.md).
