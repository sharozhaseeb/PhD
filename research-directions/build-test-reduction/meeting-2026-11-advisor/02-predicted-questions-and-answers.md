# Predicted questions and answers (N1–N5, Q1–Q5, P01–P20)

**Status:** 2026-11-21, updated 2026-11-22. Questions are the advisor model's predictions ([persona](../pm/advisor/persona.md) section 8, AI-SIM/INFER; not the advisor's words). Answers are condensed from repository files; each lists its evidence. Status values: **answered** (evidence exists), **partial** (design or literature exists, part is open), **TODO (W3)** (needs a W3 result). Updated after W3's PRELIMINARY draft results: W3 numbers appear only with W3's labels and a link to the W3 file; see [03-results-summary.md](03-results-summary.md), sections "What may be shown" and "Superseded figures".

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
| P10 | partial | P20 | partial; A/A 0/46 measured, limits stated |

## Five likely questions on the new results (added 2026-11-22 afternoon)

Source: [review-new-results](../pm/advisor/review-new-results.md) section (b) (AI-SIM, a model of the advisor, not the advisor). Answers condensed from W3 files.

**N1. "You said you would pivot if B1 replicated. Did it?"**
It was **not validly tested**, which is different from failing to replicate. On networkx, B1 holds on true optimizations: 9 of 15 unreached by measured profile (about 60%, Wilson 36–80%). geopandas: 18/20 by static reach from a 2017 base, where functions added later are unreached by construction; a post-hoc name heuristic gives 7/20, and neither is a bound. pvlib: invalid (its 2014 base has no asv suite; about 4 of its 14 mined edits are optimizations). bottleneck: 4/8 as frozen, 0/8 under the template reading; its suite benchmarks functions by name, which suggests B1 depends on suite design. A valid test needs measured profiles at each parent and a mining rule fixed before mining (counts only, no timing); proposed as the first post-meeting step (A13).
Evidence: [W3 results.md](../03-experiment/results/results.md) "Q3", "networkx edit sets". Slot S2 in [results summary](03-results-summary.md).

**N2. "Your regex matched 'coefficient'. How do you know the remaining 15 are optimizations? Did anyone read the diffs?"**
By subject only, post hoc, by one reader; the diffs were not classified and there was no second rater. The 3 exclusions came by three routes: one through "coefficient" (step 13), one through `fast_`/`faster_` names (step 8, MAINT), one bug fix through `vectoriz` (step 17). The 2 edits dropped on apply conflicts were optimizations. The functional conclusions survive the exclusion (A3 misses 1/18, every other arm 0/18). The A4 point gets worse: 2 of A4's 5 full checks fired on non-optimization edits.
Evidence: [W3 results.md](../03-experiment/results/results.md) "networkx edit sets". Slots S2, S4.

**N3. "What is your noise floor, and can your oracle see the slowdowns that matter?"**
0 false verdicts in 46 A/A comparisons (Wilson upper bound 7.7%), optimistic because it is the same 23 cases twice. The noise sits close to the threshold: two cases had p < 0.002 and were stopped only by the ratio condition, and a ratio of 1.77 still read "same". Power from measured noise is 0.91 at 1.2× overall, but for 2 of the 3 sampled `benchmark_algorithms` cases (3 of 49) only about 2× is reliable. So #3 may be a power miss of a small effect; #4 is a coverage miss (reached only statically). On 1 + 3σ: the pre-registered ratio > 1 + 3·σ_noise condition has now been computed ([results.md](../03-experiment/results/results.md) "Pre-registered noise floor"), but σ exists only for the 23 A/A cases (2 repeats, not 5), and **none of the flagged "slower" verdicts is among them, so the rule cannot be applied to any reported verdict**; a deviation is recorded. A labelled post-hoc proxy (floors of same-class A/A cases) suggests #2's on-target verdict (about 1.85×) survives, while #1, #8 and #9 are ambiguous (ask A3).
Evidence: [W3 results.md](../03-experiment/results/results.md) A/A section. Slots S2, S7.

**N4. "#9 flags reach-based selection as unsafe. Is it unsafe or not?"**
The pre-registered flag stands, and we cannot say which way it falls. `DiGMState.__init__` is in neither the profile nor the static reach of the louvain case; the verdict sat just past both thresholds (1.13×, p = 0.0019). The post-hoc re-check read "same" (0.97–1.01×), but it was cut at 5 of 6 runs and no comparison was order-balanced. Under 50 null comparisons the chance of at least one false "slower" is about 5%. The check covers only the 5 slowdowns no benchmark reaches: it is a profile-completeness check, not a safety rate.
Evidence: [W3 results.md](../03-experiment/results/results.md) "Profile-completeness check" and #9 re-check. Slot S2.

**N5. "Your benchmark cost moves during the day. Why should I believe R1?"**
The direction yes, the magnitude no. The drift is confined to one module's per-process setup; timing loops (132–171 s per pass), timed samples and tests (71–89 s) are stable. Even the fastest pass (659 s) is about 7.5× build plus tests, and the cached-setup estimate is about 1.5–2×. Within one protocol the setup changes are about 1.7× and about 3×; the "about 10×" figure crosses protocols (2 against 5 processes) and assumes cost is linear in processes. The cause is unknown and no setting was changed; this is the case for a lab machine (A12).
Evidence: [W3 results.md](../03-experiment/results/results.md) RQ1 headline, machine-state and A/A sections. Slot S1.

## The advisor's predicted first five questions (added 2026-11-22)

Source: the advisor-persona review of the near-final results, section 4 ([review-final-results](../pm/advisor/review-final-results.md); AI-SIM, a model of the advisor, not the advisor). Answers are condensed from W3 files and keep W3's labels.

**Q1. "Is B1 a networkx problem or a general one? How many projects have you checked?"**
**It was not validly tested** (not "did not replicate"). On networkx, 9 of 15 true optimizations (about 60%, Wilson 36–80%) are executed by no benchmark by measured S0 profile, 4 of 15 by static call graph; 3 of the 18 replayed edits turned out not to be optimizations (one through "coefficient", one through `fast_`/`faster_` names, one bug fix through `vectoriz`). 7 of 10 frozen slowdowns sit in functions no benchmark executes. The replication on geopandas, pvlib and bottleneck (W3 Q3) is **inconclusive**: static reach from one old base is not a bound, pvlib's base has no asv suite, and bottleneck is 4/8 as frozen or 0/8 under a template interpretation. A valid test needs measured profiles at each parent and a mining rule fixed before mining; counts only, no timing. Proposed as the first post-meeting step (A13).
Evidence: [W3 results.md](../03-experiment/results/results.md) "Finding B1", "Slowdown oracle". Slot S2 in [results summary](03-results-summary.md).

**Q2. "87–96% of your benchmark cost is one module's setup-heavy cases. If you cache it, do benchmarks still dominate, and does selection still matter?"**
Not by an order of magnitude. Timing loops are 132–171 s of a 659–2444 s pass; 80–94% of a pass is outside them. W3 **estimates** (not measured) a setup-cached pass at about 130–170 s, about 1.5–2× build plus tests instead of 8–28×; a measured setup-cached pass is not yet scheduled. (Precisely, 87–96% is the share of the 49 `benchmark_algorithms` cases, mostly import-time setup.) On this suite, most benchmark cost is setup, which caching, not selection, reduces. Benchmarks would remain the largest single part, and selection would still matter at a much smaller scale.
Evidence: [W3 results.md](../03-experiment/results/results.md) "RQ1 headline". Slot S1.

**Q3. "Your mutants sit in the functions you edited, so every selector catches them. What fault model would separate the rules, and why wasn't it built?"**
Agreed: this is a design limitation (M2). Every arm with a per-edit tier catches every mutant at its injection step by construction, so the functional results cannot rank selection rules. Faults in callers or callees, or interaction faults, would separate them; the latent and caller fault classes were planned (readiness §4.1b), latent faults turned out empty on networkx (0/5), and caller faults were not generated in the time available. Separately, A4 as implemented costs more than plain testmon, and about 2× batching once benchmarks count (finding B2).
Evidence: [W3 results.md](../03-experiment/results/results.md) "RQ3 — C5 batching comparators", "Fault detection"; [readiness §4.1b](../03-experiment/readiness.md). Slot S4.

**Q4 (predicted before the A/A run). "You have no A/A noise floor yet, and one off-target verdict at p = 3.4e-6. Why should I believe #2 and #8, or any benchmark verdict?"**
Treat every benchmark verdict as provisional. The A/A run is now measured: 0 false verdicts in 46 A/A comparisons (Wilson upper bound 7.7%, optimistic), noise close to the threshold, only about 2× slowdowns reliably caught on 2 of the 3 sampled `benchmark_algorithms` cases (3 of the module's 49; optimistic bootstrap), and one module's per-process setup (`benchmark_algorithms`) drifted about 1.7–3× within a protocol during the day (about 10× only across protocols), while timing loops, timed samples and tests stayed stable; cause unknown. It cannot separate a 0.3% false rate from zero. The order arm found no order effect, but at low power, so the #5 verdict stays unresolved. #2 (1.90× on 8/8 profiled cases) and #8 (1.12×) are labelled post-hoc and are on-target with p of about 1e-7; the #5 "faster" verdict (0.628×, p = 3.4e-6) came on the first case of a block run base-first, whose cause is unresolved (the A/A order arm found no order effect, but at low power). The profile-completeness check flagged #9 (1 of 50, 1.13×, p = 0.0019); a post-hoc partial re-check (5 of 6 runs) did not confirm it, and the flag stands. The pre-registered result does not depend on any of these: regression safety is not measurable on networkx with the frozen set.
Evidence: [W3 results.md](../03-experiment/results/results.md) "Slowdown oracle", "Profile-completeness check"; [LABELS.md](../03-experiment/results/raw/networkx/bench/LABELS.md). Slots S2, S7.

**Q5. "So what is Study 1's contribution now, given that build reduction is minor, test selection is solved by testmon, and your policy adds nothing? Does it go beyond the literature?"**
A cost characterization (benchmarks, not build or tests, dominate; most of that is setup; build is a minor lever; testmon is 3.5–4× cheaper end to end over the session and about 6× on one edit) plus the oracle gap (B1, S2): on networkx the project's own benchmarks execute none of the changed functions for about 60% of true optimizations (9 of 15), and moderate slowdowns may be missed even where reached (coverage and power), so "stays optimized" cannot be checked for many edits. **Generalisation is untested:** B1 was not validly tested outside networkx (W3 Q3), and a targeted literature search on benchmark coverage of performance-improving commits is still to be recorded by W1. Related work that could already cover it includes Ding et al. (unit tests as performance tests), SWE-Perf (unit tests as workloads) and WEDGE/PerfForge-style benchmark generation. The A4 negatives support this reading rather than end it. See ask A13.
Evidence: [results summary](03-results-summary.md) (the story in four steps); [review-final-results](../pm/advisor/review-final-results.md) (3); [01-agenda-and-asks.md](01-agenda-and-asks.md) A13.

---

### P01. "How long do a full build, full test and full benchmark run take per edit, and how many edits per session?"

**Answer (PRELIMINARY, single runs).** On networkx (18 replayed edits): build 1.19 s median, serial tests 85.7 s median per edit (6771 tests), about 1700 s of tests over the session. A FULL benchmark pass (171 cases, 2 processes x 3 values) took 659-2444 s across 6 measured passes, median about 730 s, so benchmarks are about 8-28x build plus serial tests (cost only; all passes noisy-labelled or concurrent; the 3.7x spread is itself a noise finding). On bottleneck's amended base a clean build takes 4.7-5.4 s against about 24 s of tests (191), about 16-18% (**noisy**). W2 found no system that reports build seconds per candidate.
**Evidence:** [W3 results.md](../03-experiment/results/results.md) "RQ1 headline" and "RQ1"; [rq1_networkx.csv](../03-experiment/results/rq1_networkx.csv); [W2 at-a-glance table](../02-practice-survey/README.md).
**Status:** answered (PRELIMINARY). Slot: S1 in [results summary](03-results-summary.md).

### P02. "What is new compared with RTS (Ekstazi, STARTS, testmon) and incremental builds?"

**Answer.** We do not propose a better selector. PerfAgent already runs testmon on every optimization iteration, never runs the full suite and reports no misses. The contribution is evidence of when these techniques fail for performance-motivated, accumulating edits: native-extension boundary (C5), stale dependency data (C7), dropped benchmarks (C11), incremental-rebuild correctness (C8). The RQ3 policy follows from those. A manual ACM DL / IEEE Xplore pass found no record anticipating C1, C5, C8 or C11; one 2009 paper narrows C7.
**Evidence:** [W1 README, "What's new"](../01-literature/README.md); [closest-works.md](../01-literature/closest-works.md); [beyond-literature-claims.md](../01-literature/beyond-literature-claims.md); [database-search-2026-11-21.md](../01-literature/database-search-2026-11-21.md).
**Status:** answered (literature). PRELIMINARY measurements exist for C7, C8 and B1/C11 (slots S2, S4, S5 in the [results summary](03-results-summary.md)); C5 is not measured.

### P03. "What does 'build' mean for Python, and why Python?"

**Answer.** Build is a C or Cython extension compile, editable install and bytecode; dependency resolution is excluded. networkx has no build step beyond the editable install, so its build share was expected to be negligible; the PRELIMINARY result below confirms it. bottleneck has four template-generated C extensions built with setuptools `build_ext`, where incremental builds are non-trivial. A cost-only scikit-learn measurement (meson-python plus Cython) was planned and is not reported. The choice of Python is a charter choice, not an advisor decision.
**Evidence:** [readiness §1.2](../03-experiment/readiness.md); [tpm-log, R1](../pm/tpm-log.md); [persona §5](../pm/advisor/persona.md); [review-w3-readiness](../pm/advisor/review-w3-readiness.md) (P03 row).
**Result (PRELIMINARY):** networkx build is 1.19-2.11% of serial test time, so negligible and reported as such; bottleneck clean build is about 16-18% of build plus tests on the amended base, before benchmarks (**noisy**). A failed build is a reject (rule B0), because an incremental tree hid a failed compile on one replayed state. Evidence: [W3 results.md](../03-experiment/results/results.md) "Bottleneck"; [build-hazard-iterators-h.md](../03-experiment/results/build-hazard-iterators-h.md).
**Status:** answered (PRELIMINARY). Slot S1 in [results summary](03-results-summary.md). Ask: A1 in [01-agenda-and-asks.md](01-agenda-and-asks.md).

### P04. "How do you know the reduced selection did not miss a bug or a slowdown?"

**Answer.** FULL (full build, tests, benchmarks) is the oracle at every state. Faults and slowdowns are injected, frozen and hashed before any selection rule is configured. A mutant counts only if FULL kills it; survivors are reported separately. Results are "k of N missed" with a Wilson 95% interval, and each miss gets a one-line reason. (Planned: natural reverts reported separately from synthetic slowdowns; none were measured in the pilot.) We never claim "no misses means safe". Known bias (TPM M2): synthetic faults sit in edited functions and must be detected by FULL, so dependency/profile selection catches them almost by construction; RQ3 is therefore headlined as cost at equal detection, with misses on natural reverts reported separately.
**Evidence:** [readiness §4, §4.4](../03-experiment/readiness.md); [tpm-log, R2 and M2](../pm/tpm-log.md); [review-w3-readiness](../pm/advisor/review-w3-readiness.md) (P04 row).
**Result (PRELIMINARY, networkx, functional only; frozen mutants filtered by FULL, not a safety guarantee; simulated; selection catches these almost by construction (M2); N = 20 means a miss rate below 16.1% at 95%, not "safe"):** of 20 FULL-killed mutants, every arm missed 0/20 (95% Wilson CI 0-16.1%) except the changed-module rule, 2/20 (2.8-30.1%), both from test files whose names do not match the module. W3 states the M2 bias: on this fault class selection catches almost everything by construction. Slowdowns: FULL itself detects at most 3 of 10 frozen slowdowns (2 on target, 0 in the pre-set bands), so the pre-registered result is that **regression safety is not measurable** on networkx with the frozen set; 7 of the 10 slowed functions are run by no benchmark. #2 and #8 are a labelled post-hoc analysis. The first out-of-reach spot check had no power and is withdrawn; the powered re-run is relabelled a profile-completeness check, not safety evidence: complete, 1 slower in 50 out-of-reach comparisons (#9, 1.13×, p = 0.0019); a post-hoc re-check did not confirm it, and the flag stands. Evidence: [W3 results.md](../03-experiment/results/results.md) "Fault detection", "Slowdown oracle"; [LABELS.md](../03-experiment/results/raw/networkx/bench/LABELS.md); [rq2_steps.csv.summary.csv](../03-experiment/results/sim/networkx/rq2_steps.csv.summary.csv).
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
**Result (PRELIMINARY, counts only; S0 profiles):** B1: for 9 of the 15 true optimizations (12 of 18 replayed edits), no benchmark case executes any changed function, so for about 60% of true optimizations (Wilson 36–80%) the project's own suite cannot confirm the claimed speed-up. The slowdown oracle agrees: 6 of the 9 slowdowns in true-optimization functions (7 of all 10) sit in functions no benchmark executes (S0 profiles), and where slowdowns are reached the oracle's power is limited (coverage and power), and FULL detects at most 3 of 10 (2 on target, 0 in the pre-set bands), so the pre-registered result is that regression safety is not measurable with the frozen set. Evidence: [W3 results.md](../03-experiment/results/results.md) "Finding B1", "Slowdown oracle". Ask: A13 in [01-agenda-and-asks.md](01-agenda-and-asks.md).
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

**Answer.** Planned (readiness §5), not done: we do not count a miss where FULL's own verdict is unstable; the full asv-rule decision is to be re-run at least three times, interleaved, on a fixed subset of states; reduced-arm misses on oracle-unstable (state, benchmark) pairs to be labelled "oracle-unstable" and reported separately. Done so far: the A/A floor on 23 cases and a partial re-check of #9 only. The motivating literature is arXiv 2607.01211, summarised in W2 (headline 5 and finding F7).
**Evidence:** [readiness §5, "Oracle repeatability"](../03-experiment/readiness.md); [W2 README, headline 5](../02-practice-survey/README.md); [findings.md](../02-practice-survey/findings.md).
**Status:** partial. A/A measured: 0 false verdicts in 46 A/A comparisons (Wilson upper bound 7.7%, optimistic), noise close to the threshold, only about 2× slowdowns reliably caught on 2 of the 3 sampled `benchmark_algorithms` cases (3 of the module's 49; optimistic bootstrap), and one module's per-process setup (`benchmark_algorithms`) drifted about 1.7–3× within a protocol during the day (about 10× only across protocols), while timing loops, timed samples and tests stayed stable; cause unknown; it cannot separate a 0.3% false rate from zero ([W3 results.md](../03-experiment/results/results.md) A/A section; [findings.md](../knowledge-base/findings.md) N6, N7). Also: a 3.7x spread across 6 same-protocol benchmark passes, M5 load labels on 410 of 5330 oracle runs, and #1 judged an oracle false positive by reading, not re-measurement ([W3 results.md](../03-experiment/results/results.md) "Slowdown oracle"). Slot S7 in [results summary](03-results-summary.md).
