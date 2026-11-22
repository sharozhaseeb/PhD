# Advisor-persona review of the near-final Study 1 results

Reviewed 2026-11-22, about 08:00 PKT. Reviewer: advisor-persona subagent (AI-SIM: a model of the advisor, not the advisor).

Read:
- `knowledge-base/findings.md` (all rows);
- `03-experiment/results/results.md`: RQ1 headline, idle re-timing, slowdown oracle, the powered spot check and "RQ3 — C5 batching comparators";
- `03-experiment/results/build-hazard-iterators-h.md`, through `findings.md` and `results.md` only (H1–H4); the hazard file was not read separately;
- `meeting-2026-11-advisor/03-results-summary.md` and `01-agenda-and-asks.md`.

Still running and not reviewed: the A/A noise floor with an order arm, and the top-up of spot-check slowdowns #7 and #9.

## Bottom line

The pilot has produced **one strong, slightly unexpected result and a set of honest negatives**.

- **The strong result:** on networkx, *benchmarks* (not builds or tests) dominate per-edit cost (R1). The project's own benchmark suite does not even execute most optimized functions (B1, S2). So "stays optimized" cannot be checked for most edits, however cleverly anything is selected.
- **What it means for Study 1:** this is the most interesting thing it has found, and it fits the owner-relayed brief, "make sure a codebase, once optimized, stays optimized/valid".
- **Where the pack is weak:** generalisation (one project for B1), noise (no A/A floor yet), and a narrative that still reads around the A4 policy rather than leading with B1.

## (1) Claims: accept or push back

| Finding | Verdict | Why |
|---|---|---|
| **R1** Benchmarks dominate cost: 659–2444 s per pass, median about 730 s, against about 87 s for build plus tests | **Accept the direction** | Even the fastest pass is about 7.5× build plus tests, so the conclusion survives the 3.7× noise. **Push back on the wording.** 88–94% of a pass is import-time graph construction in one module (`benchmark_algorithms`), repeated for every process. The advisor will say: "That is a badly set-up suite under asv's process isolation, not a property of validation. Cache the setup and the cost falls." Say it outright: *on this suite, most benchmark cost is setup, and setup is reducible by caching, not by selection.* Otherwise the claim looks inflated. |
| **R4** 3.7× cost spread under one protocol | Accept as measured | The cause (Windows host load) is inferred and labelled so. Good. |
| **R2** Build negligible in networkx; 16–18% in bottleneck, before benchmarks | **Accept** | Add the obvious consequence: once benchmarks are counted, build is a small share in *both* projects. So **"reduced build" is a minor lever** in the Python projects studied. The planned scikit-learn cost-only measurement was never reported, so the heavy-build question (P03) is still open. Say so, or drop it from agenda item A1. |
| **R3** Tests 71–89 s serial per edit | Accept | All re-runs are noisy-labelled, but the direction holds. |
| **T1** testmon 3.5–4× cheaper end to end; **T2** worked edit about 6× | **Accept** | This is the corrected end-to-end view I asked for, with startup and overhead included. It shows functional test selection is a solved, modest win here, and PerfAgent already does it. |
| **B1** 12 of 18 edits executed by no benchmark | **Accept as counts. Strongest finding. Not yet general.** | One project with 171 cases (networkx is not a performance-focused library), and the profiles come from S0 only. The advisor's first reaction will be "Is that networkx or is that Python?" (see Q1). |
| **S1/S2** FULL detects 2 of 10 on target; 5 of the 7 misses are reached by no benchmark | Accept, labelled as one oracle run with no A/A floor | Consistent with B1. #1 judged an oracle false positive "by reading" is acceptable *only* as a label until the A/A result is in. |
| **S4** Regression safety of reduced selection is not measurable (pre-registered) | **Accept; well framed** | |
| **P4** Powered out-of-reach spot check: 0 slower in 30 | **Push back on what it is called** | It only covers slowdowns that *no* benchmark reaches, so it tests whether the S0 profiles are *complete*, not whether selection is *safe*. Call it a "profile-completeness check". The strong off-target "faster" verdict in #5 (0.628×, p = 3.4e-6, base run first, warm-up outliers) shows the oracle has a real false-verdict rate under fixed order. That is exactly why the A/A run with an order arm matters. |
| **N1–N4** A4 buys no extra functional detection; accumulation null; A4 behaves like k ≈ 4 | Accept as measured | Framing is discussed in (2). |
| **N5** "A4 beats batching at matched test cost" | **Push back. Remove "beats".** | Every arm that selects per edit gets delay 0 *by construction*, because each mutant sits in an edited function (M2). The comparison measures the fault model, not A4. Report: "with this fault model the per-edit tier, not the trigger, explains detection; plain testmon dominates A4; once benchmarks count, batching is 1.7–6× cheaper". |
| **B2** Profile selection collapses to all 171 cases | Accept as a design gap | It is the reason A4 loses on total cost. Present it as unfinished design, not as a result. |
| **C7** 2.4% of functions get nondeterministic dependency data | Accept | Small, real, and a nice connection to claim C7. |
| **H1** Incremental tree masks a failed compile; rule B0 | **Accept the mechanism; demote it** | It is a replay artefact. Also, "reject a failed build" is what every harness already does, so it is not a finding about reduced builds. Keep it as a harness lesson, one line. |
| **H2/H3** `iterators.h` hazard did not reproduce; B4 invalid | Accept | Honest. Minor. |

## (2) Are the honest negatives framed well?

They are stated plainly and labelled, which the advisor will respect. Two framing problems:

1. **The pack mixes up "the design cannot discriminate" and "A4 is worse".**
   - "A4 buys no extra functional detection" and "A4 beats batching" both come from the same construction bias (M2). With mutants placed in edited functions, *no* per-edit arm can differ in detection.
   - Split these into two statements:
     - **(a) Limitation:** the functional fault model cannot distinguish selection rules. A fault model that could (faults in callers or callees, or interaction faults) was planned and not built.
     - **(b) Real negative:** on cost, testmon dominates A4, and with benchmarks counted, batching dominates both. **(b) is conditional on B2:** A4's benchmark selection never worked because checkpoint re-profiling was not built. Say "A4 as implemented", not "A4".
2. **Order of the story.** If the meeting opens with A4's negatives, it sounds like a failed method study. Open with:
   - R1: where the cost is;
   - B1 and S2: the suite cannot see most optimizations, so regression safety cannot be measured;
   - T1: functional selection is a solved, modest win (testmon, PerfAgent);
   - then the A4 negatives, in one slide, as "a deterministic policy layered on top does not help on this data".

   The negatives then *support* the pivot instead of ending the story.

## (3) The pivot (agenda ask A13) and Study 2

**My view: pivot partly, and say it is evidence-driven.** Keep the three RQs, but change what Study 1 claims:
- **RQ1 answer:** benchmarks dominate cost; build is minor in Python projects; test selection is a solved 4–6× win.
- **RQ2 answer (new lead):** *the oracle is missing*. Most optimization edits are not executed by the project's benchmarks (B1), and most injected slowdowns are invisible even to FULL (S2). So reduced *selection* has little to select from.
- **RQ3:** a deterministic policy adds nothing measurable on this data (honest negative, with the stated limitations).

This is a better answer to the owner-relayed brief than a cleverer selector, and it is a finding rather than a tool. **Two conditions before it is a contribution:**
1. **Show B1 on more projects.** Profile or static reach counts for perf commits are cheap: no timing is needed. Start with bottleneck (the infrastructure exists), then 2–3 projects with asv suites and perf-commit histories, such as pandas, scipy, scikit-image or astropy.
2. **Search the literature specifically for benchmark coverage of performance-improving commits.** Related work exists: unit tests as performance tests (Ding et al.), performance-test generation and benchmark re-evaluation (the July 2026 "Rethinking Code Performance Benchmarks" preprint, WEDGE/PERFFORGE), and SWE-Perf using unit tests as workloads. W1 must record that search before anyone says "not found".

**Study 2 (AI), as I would set it:** *close the coverage gap B1 exposes.*
- Generate a targeted workload or benchmark for each optimization edit, so the changed functions are actually executed and timed.
- Evaluate it with Study 1's harness: the coverage of changed functions (the B1 metric), detection of frozen slowdowns at a measured noise floor, confirmation of the claimed speed-up, and cost.
- Baselines must include deterministic options first: timing the existing unit tests that reach the function, as SWE-Perf does; a parameter sweep of existing benchmarks; and performance fuzzing.
- This keeps the step-by-step logic: Study 1 finds the deterministic limit; Study 2 tests whether AI moves it.
- **Novelty risk is high** (WEDGE, PerfForge, the July 2026 benchmark-generation preprint). The angle that is ours is *per edit, inside an iterative session, judged by a coverage-and-detection metric*.
- AI-based *test selection* is the weaker Study 2: functional selection is already solved here.

## (4) The five questions I would ask first

1. "Is B1 a networkx problem or a general one? How many projects have you checked?"
2. "88–94% of your benchmark cost is import-time setup. If you cache it, do benchmarks still dominate, and does selection still matter?"
3. "Your mutants sit in the functions you edited, so every selector catches them. What fault model would actually separate the rules, and why wasn't it built?"
4. "You have no A/A noise floor yet, and one off-target verdict at p = 3.4e-6. Why should I believe #2 and #8, or any benchmark verdict?"
5. "So what is Study 1's contribution now, given that build reduction is minor, test selection is solved by testmon, and your policy adds nothing? Does it go beyond the literature?" The answer should be: a cost characterization plus B1/S2 as the oracle gap, pending generalisation.

## (5) Cheap fixes before the meeting

1. **Compute B1 on bottleneck**, and if possible on one or two asv repositories by static reach. These are counts only: hours, not days. This alone answers Q1.
2. **Reorder `03-results-summary.md`** to lead with R1, then B1/S2, then T1, then the negatives. Remove "A4 beats batching". Split each negative into "design limitation" and "real negative (as implemented)".
3. **Relabel P4** as a profile-completeness check, and note the #5 order effect as motivation for the A/A order arm.
4. **Add one sentence to R1** about setup: most of the cost is import-time graph construction, reducible by caching. Add the networkx build share *with* benchmarks (about 1.2 s of about 820 s, ≈ 0.15%).
5. **Sync stale statuses:**
   - `findings.md` P2 says the A/A run is "pending (not queued)", but it is running now.
   - P3 lists the C5 comparators as pending, but they are done (N5).
   - `03-results-summary.md` S3 also lists cap-only and additive-budget as pending, and its S5 says "not queued".
   - Agenda A1 still cites a scikit-learn measurement that was never reported.
6. **If the A/A run finishes before the meeting:** report the false-verdict rate per comparison and re-read #1, #2, #8 and the #5 "faster" against it. If it does not finish, state that every benchmark verdict is provisional until it does.
