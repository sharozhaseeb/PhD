# Advisor-persona advice: turning Study 1 into a first paper

Written 2026-11-22, after the owner changed the goal to "a first-draft, near-publishable paper" (WORKLOG 15:12). Reviewer: advisor-persona subagent (**AI-SIM**: a model of the advisor, not the advisor). It follows [persona.md](persona.md), [review-final-results.md](review-final-results.md) and [review-new-results.md](review-new-results.md).

Read: `pm/CHARTER.md`; `knowledge-base/findings.md` (all rows); `03-experiment/results/results.md` (status, RQ1 headline, selection table, slowdown oracle, Q3, A/A, 1 + 3σ section); `01-literature/beyond-literature-claims.md`; `01-literature/closest-works.md`; `meeting-2026-11-advisor/01-agenda-and-asks.md`; the tail of `knowledge-base/WORKLOG.md`.

Nothing was run. **W1's targeted novelty search (B1, C11, A/A floor, R1, C8) has not reported yet.** Where its outcome would change this advice, the text says so and marks it **[NOVELTY-DEPENDENT]**.

Venue deadlines below are **not checked**. Confirm each one against the current call for papers before planning around it.

---

## 0. Bottom line

- **There is a paper here, but it is not yet the paper the charter planned.** The charter asked whether a new deterministic policy can reduce validation cost safely (old RQ3). The answer is no, and that is the least interesting result. The interesting result is about the **oracle**: for optimization edits, the expensive part (benchmarks) is also the part that often cannot see the edit.
- **As it stands, the evidence supports a short or emerging-results paper,** not a full research-track paper. The lead finding (B1) rests on **one project, 15 edits and a CI of 36–80 %**. No full-track reviewer will accept "benchmarks do not cover optimizations" from that.
- **One experiment turns it into a full empirical paper:** the pre-registered multi-project B1 replication with measured profiles. It is counts-only (no timing), so it suits one laptop. Everything else is secondary.
- **Do not write the paper around A4.** It is one paragraph in the discussion and an appendix.

---

## 1. The paper

### 1.1 Thesis (one sentence)

> **When a Python project is optimized edit by edit, the cost of validating each edit is dominated by its benchmarks, yet those benchmarks often do not execute the code an optimization changes and lack the power to see moderate slowdowns in the code they do execute; so reducing build and test work, which existing tools already do, leaves the real problem — a weak performance oracle — untouched.**

The short form, for the abstract and the talk: *"In iterative optimization, the benchmark oracle, not build or test cost, is the bottleneck: it is expensive, and it often cannot see the edit."*

**Condition.** The "often" in the thesis needs the B1 replication (§2, E1). Until then, every sentence must say "on networkx". If the replication fails (pooled unreached share low, e.g. < 25 %), the thesis becomes a per-suite one: "whether benchmarks see optimization edits depends on suite design (networkx vs bottleneck)". That is still a paper, but a weaker one, and it should then be framed around the two-leg decomposition (coverage and power) rather than around prevalence.

### 1.2 Contributions the evidence supports

Each entry gives what can be claimed **now**, and what it needs to become a full claim.

| # | Contribution | Supported now | Needed for a full claim |
|---|---|---|---|
| K1 | **Per-edit validation cost breakdown for optimization edits** (R1, R2, R3). Benchmarks are 8–28× build + tests on networkx; most of that is outside the timing loops (one module's per-process setup); build is ≈ 0.15 % with benchmarks counted on networkx and 16–18 % of build + tests on a C-extension project (bottleneck). | Yes, as a direction, on one project for benchmarks. Magnitude is a range (machine drift, N7). | A second project with benchmarks (E4), repeated passes, and a **measured** setup-cached pass (E5) instead of the 1.5–2× estimate. |
| K2 | **Coverage leg of the oracle gap** (B1, S2). On networkx, 9 of 15 true optimizations change no function any benchmark executes (60 %, Wilson 36–80 %); 6 of the 9 slowdowns injected into true-optimization functions are unreached. | networkx only. | E1 (multi-project, measured profiles). This is the paper's main contribution once replicated. **[NOVELTY-DEPENDENT]** |
| K3 | **Power leg of the oracle gap** (N6, S1). The full suite detects 2 of 10 frozen slowdowns on target. A/A: 0/46 false verdicts, but power at 1.2× is 0.91 overall and ≈ 0.35 for the sampled heavy-module cases (3 of 49). | Indicative only; σ missing for every flagged case (N8). | E2 (σ for flagged and heavy cases, apply 1 + 3σ) and E3 (oracle repeatability). |
| K4 | **Overhead-honest measurement of per-edit RTS in an optimization loop** (T1, T2). testmon is 3.5–4× cheaper end to end, against the 15× that test-seconds suggest; pytest start-up and testmon's own analysis dominate. | Yes, one project, one run. | Not novel as a technique (PerfAgent uses it). Its value is as a correction to "% fewer tests" reporting (PerfAgent §III-D). Keep it as a supporting result, not a headline. |
| K5 | **Negative result: a deterministic accumulated-change policy adds nothing measurable** (N1–N5, B2). A4 behaves like periodic full checks at k ≈ 4; testmon dominates it on cost; the fault model cannot separate selection rules. | Yes, as "A4 as implemented, under this fault model". | Nothing more. One paragraph plus an appendix. Do not spend compute here. |
| K6 | **Methodological lessons for measuring this problem.** (a) Subject-regex mining of "performance" commits has poor precision (networkx 17/20, pvlib ≈ 4/14; "coefficient" matches `efficien`). (b) Static reach from one old base is not a bound in either direction. (c) 6 vs 6 samples cannot reach p < 0.002 with Mann-Whitney, so a common asv-style spot check has no power by construction. (d) Function-level dependency data is 2.4 % nondeterministic (C7). (e) Incremental trees can pass tests on stale binaries after a failed compile (H1, a replay artefact; rule B0). | Yes; these are measured. | Short. A "lessons for replication" subsection. They protect the paper against reviewer doubts more than they add novelty. |

**Not contributions (do not claim):**
- a better selector;
- per-edit test selection in optimization loops (PerfAgent did it);
- a two-sided performance gate (SemOpt, PerfAgent);
- the A/A method itself (standard practice: Georges et al. 2007, Kalibera and Jones 2013, Laaber et al.). Only its *result here* counts, as part of K3;
- C8 (incremental-rebuild correctness for Python extensions): the only event is a replay artefact (H1), and H2 did not reproduce. **Drop C8 from the paper's claims whatever W1 finds.**
- C7 (staleness over a growing refresh interval) and C5 (native-boundary misses): not measured. Name them as future work.

### 1.3 Type of paper

**Empirical study with an embedded negative result.** It is not a technique paper. The paper type depends on E1:

| If | Then |
|---|---|
| E1 is **not** done before the first deadline | Short or emerging-results paper (4–5 pages): K1 + K2 + K3 on networkx, framed as a problem statement with a clear replication protocol. |
| E1 is done (≥ 5 projects, ≥ 60 true optimization edits pooled) | Full empirical paper (10–12 pages): K1–K3 as the main results, K4–K6 as supporting results. |
| E1 is done **and** W1 finds a prior benchmark-coverage study of performance commits **[NOVELTY-DEPENDENT]** | Still a full paper, but reframed: "replication and extension in Python, with the power leg and the per-edit cost context added". Lead with the coverage-times-power decomposition (§5), not with prevalence. |

### 1.4 Venues (2–3 realistic; deadlines to be confirmed)

1. **ESEM (research track; it also has a registered-reports track).** First choice for the full paper.
   - Why: it values empirical rigour, pre-registration, honest negative results and threats sections. The pre-registered replication protocol (§2, E1) is exactly what this community rewards.
   - Timing: ESEM's main deadline has usually been in spring (around May), which fits "replicate in December, write in January–March". **Not checked.**
2. **ICPE (research track; the work-in-progress or vision track for a short version).** Second choice, or the first if the deadline fits better.
   - Why: the audience knows benchmarking, asv-style suites, noise and performance-test selection. K3 and the oracle-gap framing will land well.
   - Risk: these reviewers are the strictest on measurement. One laptop under WSL2, unexplained machine drift (N7) and a 23-case A/A will be attacked first. Do not go here without E2, E3 and a pinned or lab machine.
3. **A short version now: an ICSE-co-located workshop** (for example AST, or one on LLMs for code and agents, where the optimizer-validation motivation fits) **or MSR's registered-reports track** for the replication protocol alone.
   - Why: it gets the problem statement and the networkx evidence out early and fixes priority, at low risk. A registered report also forces the mining rule and analysis to be fixed before the data, which answers P26 ("did you read the diffs?") by design.
   - Check the deadlines; some ICSE-workshop deadlines fall in December–January.

**Later: EMSE journal**, as the extended version (more projects, the measured power map of §5, and possibly the Study 2 baseline).

**Not recommended:** the ICSE or FSE research tracks for this paper. The contribution is a characterization from a few projects with no new technique, and the competition there is for broader studies.

---

## 2. Minimum extra evidence before submission (ranked)

Effort assumes one laptop (WSL2, 6 cores, 7 GB) with timing runs only at night and nothing else running. "Compute" means unattended machine time; "human" means the student's hands-on time.

| Rank | ID | Experiment | Status | Effort | What it fixes |
|---|---|---|---|---|---|
| 1 | **E1** | **Pre-registered B1 replication.** 5–8 projects with an asv suite present at each edit's parent. Mining rule fixed and frozen **before** mining (exclude `coefficient`, `efficiency`, `scipy.optimize`, `fast_`-names; require a source-file change). **Every mined edit classified from its diff** by the student and a second rater (blind to reach), with Cohen's κ reported. **Measured profiles** (`sys.monitoring`, one quick run per case, no timing) at each edit's parent. Target ≥ 60 true optimizations pooled, so the pooled CI is about ±10–12 points; report per project and pooled (random-effects or a simple per-project forest plot). Candidates: xarray, scikit-image, astropy, geopandas (later bases), shapely, pandas (big but valuable), dask or sympy (separate benchmark repos: check the rule handles that). | **MUST** | Human 3–4 days (rule, diff reading, second rater, script hardening). Compute 2–5 days, profiling only, **not timing-sensitive**, so it can run in the day alongside writing. Heavy-build projects (pandas, astropy) cost most; skip them if their build exceeds an hour. | P23; K2 becomes a finding; decides the paper type. |
| 2 | **E2** | **σ for the flagged and heavy cases; apply the pre-registered 1 + 3σ.** A/A, S0 vs S0, 5 repeats, ABBA, for every case with a "slower" verdict (#1, #2's 9 cases, #8, #9) plus a seeded sample of ≥ 10 of the 49 `benchmark_algorithms` cases. | **MUST** | Compute 1–2 nights (≈ 25 cases × 5 repeats; the algorithm cases are 2–4 min each under today's drift). Human ½ day. | N8 deviation; K3; makes S1 a clean pre-registered result instead of "ambiguous by proxy". |
| 3 | **E3** | **Oracle repeatability.** Re-run the slowdown oracle for the reached slowdowns (#1, #2, #3, #4, #8) with ABBA, 5 processes, at least 2 repeats; report verdict agreement. | **MUST** | Compute 1–2 nights. Can share nights with E2 if the two are interleaved into one plan. | P20; whether #1 is noise; whether #3 is a power miss. |
| 4 | **E5** | **Measured setup-cached pass on networkx.** Move `benchmark_algorithms`' import-time graph construction into asv `setup_cache` (or an equivalent cached fixture) in a patched copy of the suite, then run 3 full passes. Report loops, setup and total. | **SHOULD** (close to must for K1) | Human ½–1 day; compute 1 night. | Replaces the 1.5–2× **estimate** in R1 with a measurement. Answers "your suite is just badly set up". |
| 5 | **E4** | **R1 on a second project with benchmarks.** One E1 project with a cheap build: build, full tests and full benchmarks at 3–5 states, 3 repeated passes each. | **SHOULD** | Compute 2–3 nights; human 1 day. | K1 generality; "is it only networkx's setup?" |
| 6 | **E6** | **Repeated FULL passes for R1 on networkx** (≥ 3 passes at 2–3 states, same night). | **SHOULD** (cheap if folded into E5) | 1 night, shared. | R1's range is from 6 single passes across states and machine states. |
| 7 | **E7** | **Lab or pinned machine** for E2, E3, E5. Native Linux, fixed CPU frequency if possible. | **SHOULD** (ask at the meeting, agenda A12) | Depends on access. | N7 drift; ICPE reviewers. If refused, keep the laptop, run timing only at night, and report N7 as a threat. |
| 8 | E8 | NameRTS as a second Python RTS baseline. | NICE | 2–3 days (no documented command for arbitrary repos). | P17. Not needed: the paper does not claim a selector. |
| 9 | E9 | A fault model that separates selection rules (faults in callers or callees; interaction faults). | NICE, **cut** | 1 week+. | Only matters if the paper were about A4. It is not. |
| 10 | E10 | Heavy-build project (scikit-learn, cost only). | NICE, **cut** | 1–2 days. | P03. State "Python projects with small builds" in the scope instead. |

**Cut entirely for this paper:** C7 refresh-interval experiment; C5 native-boundary misses; rule B4 and `.so` hashing; trigger tuning for A4; culprit finding; the video.

**Minimum viable set:** E1 + E2 + E3 (+ E5 if at all possible). About **2 weeks** of calendar time, because profiling (E1) runs in the day and timing (E2, E3, E5) runs at night. Without E1, submit only the short version.

---

## 3. Threats to validity a reviewer will raise

| Threat | What the reviewer will say | Honest mitigation |
|---|---|---|
| **External: one project for B1** | "networkx is not a performance library; its suite is small." | E1. Until then, every B1 sentence says "on networkx". Report bottleneck as the counter-example (its suite names functions directly), and present suite design as a moderator. |
| **External: historical commits as an "iterative session"** | "Real optimizer sessions are many small edits minutes apart." | State it as a limitation (readiness threat T1). The coverage finding (B1) is per edit, so it does not depend on the session model. The cost and policy results do. |
| **External: Python, asv, small builds** | "Build cost is negligible only because these are pure-Python packages." | Scope the claim to "Python projects with small or moderate builds". bottleneck (C extension) shows build can reach 16–18 % of build + tests, still small once benchmarks count. No heavy-build project: say so. |
| **Construct: "executed" is not "able to detect"** | "A benchmark may execute the function on a trivial path." | That is exactly why K3 (power) exists next to K2. The two-leg decomposition answers it. Executed is a necessary condition; report it as an upper bound on detectability. |
| **Construct: what counts as an optimization edit** | "Did you read the diffs?" (P26) | E1: diff-based classification, two raters, κ. Report networkx's own precision audit (17/20) and the pvlib failure honestly. |
| **Construct: synthetic slowdowns** | "`double_call` is not a realistic regression." | Agree: it is a controlled probe of detectability, not a model of real regressions. Report it as such; graded slowdowns (§5) make it a dose-response probe. |
| **Construct: profiles from S0, not each parent** | "Reach changes as the code changes." | E1 profiles at each parent. For networkx, report that reach was taken at S0 (state it; a re-profile at S0 confirmed 24/24 cases). |
| **Internal: measurement noise and machine drift** | "One laptop, WSL2, unexplained 1.7–3× drift." | Verdicts use interleaved A/B samples, which the drift does not inflate (N7: timed samples stable). Cost is reported as a range. E2, E3; E7 if possible. |
| **Internal: post-hoc analyses and deviations** | "Many rules changed after seeing the data." | Keep the deviation log in the paper (pre-registered vs post hoc, per result). The primary pre-registered result (S4: regression safety not measurable) is reported unchanged. This is a strength if it is shown openly. |
| **Conclusion: small N and multiplicity** | "Wilson CIs of 36–80 %; ≈ 890 off-target comparisons." | Report CIs everywhere; state the expected false-verdict count under α = 0.002; never say "most" without a CI above 50 %. |
| **Conclusion: A4 negative depends on the fault model** | "Your mutants sit in edited functions, so every per-edit arm catches them." | Agree, and say it first (M2). Present the cost dominance (testmon < A4) as the real negative, and "the design cannot discriminate" as a limitation. |
| **Reliability: artefacts and replay** | "Can I reproduce this?" | Frozen inputs with sha256, raw JSON with state SHA and harness hash in `meta`; package the harness. Fix the missing `meta` in `aa/sigma_noise.json`. |
| **Research process: AI assistance** | Venue policies now ask authors to disclose generative-AI use. | Large parts of the harness, analysis and text were produced with AI agents. Disclose per the venue's policy, and have the student personally re-derive every headline number from the raw files before submission. This is about integrity, not a reviewer trick. |

---

## 4. Outline

Working title: **"Expensive and Blind: Benchmarks as the Bottleneck of Per-Edit Validation in Iterative Code Optimization"** (or a plainer one: "Where Does Per-Edit Validation Cost Go When Optimizing Python Code, and Can Benchmarks See the Edits?").

Reframed RQs for the paper (the charter's RQ2/RQ3 fold into RQ4):
- **RQ1 (cost):** Where does per-edit validation cost go: build, tests or benchmarks?
- **RQ2 (coverage):** Do a project's own benchmarks execute the code that optimization edits change?
- **RQ3 (power):** When they do, can the full suite detect a slowdown in that code above its noise floor?
- **RQ4 (reduction):** How much do existing deterministic reductions (incremental build, testmon) save end to end, and does a deterministic accumulated-change policy add anything?

| § | Section | Content | Results and figures |
|---|---|---|---|
| 1 | Introduction (1 p) | LLM and agent optimizers validate every candidate with build, tests and benchmarks (SemOpt, PerfAgent, SWE-Perf). Reducing that work is the obvious goal. We find the cost sits in benchmarks, and benchmarks often cannot see the edit. Contributions K1–K3, plus K4–K6 briefly. | Teaser: one networkx edit (the worked edit, T2) where FULL takes ≈ 12+ min, tests 86 s, and no benchmark executes the changed function. |
| 2 | Background and related work (1–1.5 p) | RTS (Ekstazi, STARTS, testmon, NameRTS); performance-test selection and prioritization (PerfRanker, Laaber, Grambow, Ding et al.: unit tests as performance tests); benchmarking noise (Georges, Kalibera, Laaber); benchmark coverage and generation (WEDGE, PerfForge, the 2026 "rethinking performance benchmarks" preprint); how optimizers validate (W2 survey). | Table 1: how ~10 optimization systems validate a candidate (from W2), one line each. **[NOVELTY-DEPENDENT]**: the closest coverage study, if W1 finds one, goes here with a precise difference. |
| 3 | Study design (1.5–2 p) | Subjects (networkx; bottleneck for build; E1 projects for RQ2). Edit mining and replay; precision audit. Arms (FULL, INC, testmon, changed-module, static/profile benchmark selection). Oracles: functional (frozen mutants), performance (asv rule + 1 + 3σ, interleaved A/B). Pre-registration and deviation log. Platform. | Fig. 1: pipeline (mine → classify → replay → profile → measure). Table 2: subjects and edit counts. |
| 4 | RQ1: cost | Benchmarks 8–28× build + tests; loops 132–171 s; setup outside loops 80–94 %; measured setup-cached pass (E5); build 0.15 % (networkx) and 16–18 % of build + tests (bottleneck); drift as a range. | Fig. 2: stacked bar per edit (build / tests / benchmark loops / benchmark setup), with range whiskers. |
| 5 | RQ2: coverage | B1 per project and pooled, measured profiles, CIs; static vs profile reach; suite design as a moderator (networkx vs bottleneck). | Fig. 3: forest plot of unreached share per project with Wilson CIs. Table 3: example unreached edits. |
| 6 | RQ3: power | Slowdown oracle (2/10 on target; coverage miss vs power miss); A/A floor with E2 σ; 1 + 3σ applied; repeatability (E3); profile-completeness check (1 flag in 50, C11). | Fig. 4: decomposition of the 10 slowdowns (unreached / reached-undetected / detected). Fig. 5: power curve (detection probability vs slowdown factor), overall vs heavy module. |
| 7 | RQ4: reductions | testmon 3.5–4× end to end vs 15× by test-seconds; incremental build negligible; A4 summarized in one paragraph: behaves like k ≈ 4, testmon dominates, fault model cannot separate rules. | Table 4: arms × (tests run, end-to-end s, functional misses). A4 rows go to the appendix. |
| 8 | Discussion (1 p) | Implications: an optimizer that accepts an edit on "tests pass and benchmarks are not slower" is accepting on an oracle that, for many edits, does not execute the edit. Recommendations: report reach of changed code per accepted edit; time the unit tests that reach the function (SWE-Perf style) as a deterministic fallback; cache benchmark setup before selecting. Bridge to Study 2 (generate targeted workloads for unreached edits). | — |
| 9 | Threats | §3 of this file, condensed. | — |
| 10 | Conclusion | One paragraph. | — |
| A | Appendix / artefact | A4 policy and C5 batching comparators (N1–N5, B2); build hazards (H1–H4, rule B0); C7 nondeterministic dependency data; the 6 vs 6 power trap; deviation log; Q3 pilot lessons (geopandas, pvlib, bottleneck). | — |

**Drop from the main text:** A4 details and its ablation rows; the C5 batching interpolation; the `iterators.h` hazard study; B4 and `.so` hashing; the pvlib and geopandas static counts (they move to the appendix as "why we needed measured profiles"); "88–94 % import-time setup" (it was withdrawn; use "80–94 % outside the timing loops"); the "≈ 10×" drift.

**One paragraph each, main text:** H1 (stale-binary false pass, as a harness lesson); C7 (2.4 % nondeterminism, as a caution for dependency-based RTS); N4 (accumulation null).

---

## 5. Going one step further than the literature (1–2 weeks, one laptop)

The literature has RTS for functional tests, ordering of performance tests, and benchmark generation. What it does not seem to have (pending W1's search) is a **per-edit account of whether an existing suite can see an optimization at all, split into why not**. Three steps, in order of value per hour:

1. **"Effective oracle coverage" of optimization edits (the headline step).**
   - For each true optimization edit, combine (a) reach: does any benchmark execute a changed function (E1) with (b) power: the smallest slowdown that a reaching benchmark detects with probability ≥ 0.8 at the measured noise (from E2, per case).
   - Report, per project, the share of edits for which the suite could detect a 1.2× and a 2× regression in the changed code.
   - This turns "coverage" and "power" into one number a practitioner or an optimizer can use. It is the Peass-style three-way split (not covered / below noise / detected) made per edit and quantitative.
   - Cost: E1 + E2 already give most of it. Power on other projects needs a small A/A per project for the reaching cases only (1 night each; do it for 2 projects, not all).
   - **[NOVELTY-DEPENDENT]** If W1 finds a coverage study of performance commits, this decomposition is still the difference; if W1 finds a per-benchmark minimum-detectable-effect study, cite it and keep the per-edit combination as ours.
2. **A deterministic fallback, measured: do unit tests reach what benchmarks miss?**
   - networkx's function-to-test dependency map already exists (`raw/networkx/depmap`). Count how many of the 9 unreached optimizations are executed by at least one unit test: no new run needed for the count.
   - Then time those tests as micro-workloads for the 6 unreached slowdowns (#0, #5, #6, #7, #9 and #4), ABBA, 5 processes: about 1–2 nights.
   - Result: "the existing tests close X of Y coverage gaps, at power Z". This is the SWE-Perf idea, but measured as an oracle with a noise floor. It is the deterministic baseline Study 2 (AI-generated workloads) must beat, so it serves both papers.
3. **Graded slowdowns for a dose-response curve.** Inject 1.1×, 1.2×, 1.5× and 2× slowdowns (a calibrated busy-loop or repeat factor, not only `double_call`) into 3–4 reached functions; measure detection with FULL. This replaces the bootstrap power estimate with a measured one. 2 nights.

**Not worth it in this window:** a new selector; a learned or AI method; C7 or C5 experiments; more A4 variants.

**Realistic two-week plan:**

| Days | Day (human, profiling) | Night (timing, machine idle) |
|---|---|---|
| 1–2 | Freeze E1 mining rule and project list; write the registered protocol; start mining | E5 setup-cached passes + E6 repeated passes |
| 3–6 | Diff classification (two raters); profiling at parents, project by project | E2 σ (flagged + heavy cases), then E3 repeatability |
| 7–9 | Finish E1; count step 2's unit-test reach; start writing §3–§5 | Step 2 timing (unit tests as workloads); graded slowdowns (step 3) |
| 10–14 | Analysis, figures, writing | E4 (second-project cost) if E1 picked a cheap-build project |

At the end of two weeks there should be a complete first draft of §3–§7, with §1, §2 and §8 drafted. If the replication slips, submit the short version (networkx, K1–K3 + protocol) to a workshop or registered-report track and keep the full paper for the next deadline.

---

## 6. Where W1's novelty search would change this advice

| If W1 finds… | Change |
|---|---|
| A study measuring how often benchmarks cover performance-improving commits (B1) | K2 becomes a replication and extension in Python; lead with §5 step 1 (coverage × power). Venue choice unchanged; the short version loses most of its value, so go straight for the full paper. |
| A per-edit miss rate for dropped benchmarks in Python (C11) | Not a big change: C11 is not a headline here. Cite it in RQ3. |
| An A/A noise-floor and power study on asv-style suites | Expected. N6 is method, not contribution; K3 keeps only its result for these suites. |
| A per-edit cost breakdown (build / tests / benchmarks) for optimization loops (R1) | K1 becomes motivation, confirmed on our projects. The paper rests on K2 + K3. |
| An incremental-rebuild correctness study for Python extensions (C8) | No change: C8 is already dropped. |
| Nothing for B1 | K2 + §5 step 1 is the paper's novelty claim, stated as "not found in our recorded searches". Record the queries in `gap-and-search-log.md`. |
