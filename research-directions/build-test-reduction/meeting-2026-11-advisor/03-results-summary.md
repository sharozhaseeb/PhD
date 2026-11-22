# W3 results summary (PRELIMINARY)

**Status:** updated 2026-11-22 13:29 PKT against W3's final results.md, with W3's completed queue (A/A noise floor, profile-completeness check 5/5, Q3, edit-set reconciliation; [findings.md](../knowledge-base/findings.md) N6, N7, P5, B3). Story order follows the advisor-persona review of the near-final results ([review-final-results.md](../pm/advisor/review-final-results.md), AI-SIM). Sources of truth: [results.md](../03-experiment/results/results.md), [build-hazard-iterators-h.md](../03-experiment/results/build-hazard-iterators-h.md) and [LABELS.md](../03-experiment/results/raw/networkx/bench/LABELS.md). Every number is copied from the W3 file cited next to it, with W3's labels kept: **PRELIMINARY**, **measured**, **estimate**, **noisy**, **concurrent**, **simulated**, **post-hoc**, **provisional**, **optimistic**. Nothing here is new analysis. Story and asks revised after the advisor-persona review of these new results ([review-new-results](../pm/advisor/review-new-results.md)).

**Evidence boundary.** A **pilot** on one machine: networkx with 18 replayed edits, of which **15 are optimizations** and 3 are not (steps 8, 13, 17, matched by the subject rule; [results.md](../03-experiment/results/results.md) "networkx edit sets"); bottleneck main window = states 1–8 of the amended window (base `f51ed86`), states 9–13 held out. Single runs; WSL2 Ubuntu 24.04, i5-12400F, 7 GB. A benchmark A/A noise floor now exists (0/46 false verdicts), but the noise sits close to the threshold, the oracle reliably catches only about 2× slowdowns on 2 of the 3 sampled `benchmark_algorithms` cases (3 of 49), and one module's per-process benchmark setup drifts about 1.7–3× within a protocol (about 10× only across protocols) for unknown reasons, so benchmark verdicts stay **provisional**.

**Superseded figures, do not use:** "at least 0.9–4.5 h" per benchmark pass, "40–180×", the bottleneck "about 22%" build share, and any "A4 beats batching" wording ([results.md](../03-experiment/results/results.md) "Correction" and "RQ3 — C5 batching comparators").

## What may be shown (TPM go/no-go and PM rulings)

The TPM rule: no W3 number without the A/A noise floor and the injection-based miss counts ([TPM log, go/no-go](../pm/tpm-log.md)). Both inputs now exist: the A/A run (0/46, with the limits in S7) and the miss counts. Rulings applied:
- **PM, 2026-11-21:** functional miss counts may be shown as k/N with the Wilson CI, labelled "frozen mutants filtered by FULL; not a safety guarantee", with the construction bias (M2).
- **PM, 2026-11-21:** no speed-up claim from benchmarks; benchmark seconds are **cost**.
- **PM, 2026-11-22:** the slowdown oracle is reported with W3's labels; its pre-registered result is "regression safety not measurable on networkx with the frozen set"; #2 and #8 only as labelled post-hoc analysis.

Also not to be claimed ([TPM log, "Must not be claimed"](../pm/tpm-log.md)): "safe" or "no misses" as a general property; generalisation beyond the 1–2 repos, the edit sample or this machine; perf-regression detection below the measured noise floor; confirmation of the historical commits' speed-ups unless re-measured; build-time savings for Python unless measured as non-negligible; novelty before W1's recorded search; an iterative-session effect from replay of non-adjacent commits; anything about AI-based selection.

## The story in four steps

1. **Where the cost is (R1).** On networkx, benchmarks, not build or tests, dominate per-edit validation cost. The stable parts: timing loops 132–171 s per pass and tests 71–89 s per edit. On top comes setup, which is large, volatile and cacheable: whole passes took 659–2444 s (the 659–751 s passes came from the fastest machine state seen), about 8–28× build plus tests. 87–96% of a pass is the 49 `benchmark_algorithms` cases, including their loops; 80–94% of a pass is outside the timing loops. Caching the setup would cut a pass to about 1.5–2× build plus tests (estimate, not measured).
2. **The oracle gap: coverage and power (B1, S2).** On networkx, the suite executes none of the changed functions for **9 of 15 true optimizations** (measured S0 profile; about 60%, Wilson 36–80%; 4 of 15 by static call graph). 6 of the 9 slowdowns in true-optimization functions are unreached, FULL detects at most 3, and where slowdowns are reached the A/A power suggests moderate ones in the heavy module can still be missed. Pre-registered result: regression safety of reduced selection is **not measurable** on networkx with the frozen set. **B1 is a networkx-only finding; it was not validly tested elsewhere** (W3 Q3: geopandas, pvlib, bottleneck).
3. **Functional selection is a solved, modest win (T1).** testmon is 3.5–4× cheaper than FULL end to end (tests plus build), about 6× on the worked edit, and misses 0/20 frozen mutants (95% Wilson 0–16.1%; frozen mutants filtered by FULL; not a safety guarantee; simulated; caught almost by construction, M2). PerfAgent already uses it per edit.
4. **A deterministic policy on top does not help on this data (A4).** Two separate statements: the fault model **cannot tell selection rules apart** (a design limitation), and **A4 as implemented costs more** than testmon and, once benchmarks count, about 2× batching, which depends on finding B2.

## S1. Where the cost is (RQ1)

**networkx, FULL** ([results.md](../03-experiment/results/results.md) "RQ1 headline", "RQ1", "idle re-timing"; [rq1_networkx.csv](../03-experiment/results/rq1_networkx.csv)):

| Component | Value | Label |
|---|---|---|
| Benchmarks (171 asv cases, 2 processes × 3 values) | **659–2444 s per pass, median about 730 s**, 6 passes; about **8–28×** build plus serial tests | measured; all noisy-labelled or concurrent; single passes |
| of which the `benchmark_algorithms` module | **87–96%** of a pass (80–94% of a pass is outside the timing loops): 49 cases that rebuild their graphs at import, once per process; this share includes their own timing loops and process start-up | measured |
| of which timing loops | 132–171 s per pass | measured |
| "Setup cached" pass | about 130–170 s, about **1.5–2×** build plus tests, instead of 8–28× | **estimate, not measured** (lower bound: excludes process start-up and warm-up); a measured setup-cached pass is not yet scheduled |
| Tests (6771, serial) | about 71–89 s per edit across first runs and re-runs, excluding the S16/S17 first runs (first-run median 85.7 s over clean states) | measured; re-runs all noisy-labelled |
| Build (`pip install -e`) | median 1.19 s: 1.19–2.11% of serial test time; **about 0.15%** of build plus tests plus a median benchmark pass | measured |

- **Cost noise is itself a finding (R4):** the 6 passes spread about 3.7× under one protocol on one machine in one night; **cause unknown** (host load is one unverified candidate).
- **Machine drift (N7):** one module's per-process setup (`benchmark_algorithms`) drifted about 1.7–3× within a protocol during the day (about 10× only across protocols), while timing loops, timed samples and tests stayed stable; cause unknown. The A/A run took 2483 s against 753 s expected, all of the excess in `benchmark_algorithms`. The 659–751 s passes are the fastest machine state seen. It inflates benchmark **cost**, not the timing samples the verdicts use ([results.md](../03-experiment/results/results.md) "Finding (machine state" and A/A section).
- **Reading (advisor-persona review, AI-SIM):** on this suite, most benchmark cost is setup, and setup is reducible by caching, not by selection. Benchmarks would still be the largest single part if cached, but not by an order of magnitude.

**bottleneck (C extension), amended base** ([results.md](../03-experiment/results/results.md) "Bottleneck"): clean build 4.7–5.4 s against about 24 s of tests (191), about **16–18% of clean build plus full tests, before benchmarks** (noisy). With benchmarks counted, build is a small share in both projects, so **reduced build is a minor lever** in the Python projects studied ([review-final-results.md](../pm/advisor/review-final-results.md), R2, AI-SIM).

**Open:** the scikit-learn cost-only measurement (heavy build) planned in readiness §1.2 was **not run or reported**, so the heavy-build question stays open.

Answers [P01](02-predicted-questions-and-answers.md), [P03](02-predicted-questions-and-answers.md), predicted first question 2.

## S2. The oracle gap: coverage and power (B1, slowdown oracle, A/A)

**B1** (counts; not a timing; [results.md](../03-experiment/results/results.md) "Finding B1", "networkx edit sets"). A post-hoc reading of the subjects (one reader; diffs not classified) found that 3 of the 18 replayed networkx edits are not optimizations, each by a different route: step 13 (`bf130bfe`) matched through "coefficient"; step 8 (`519e819f`, MAINT) through `fast_`/`faster_` names; step 17 (`9f6079c0`, a bug fix) through `vectoriz`. The 2 edits dropped on apply conflicts were optimizations.

| Reach measure (networkx, S0) | All 18 replayed edits | 15 true optimizations |
|---|---|---|
| Measured profile | 12/18 unreached, 67% [44–84%] | **9/15, 60% [36–80%]** |
| Static call graph | 7/18, 39% [20–61%] | **4/15, 27% [11–52%]** |

So for about 60% of the true optimizations the project's own suite cannot confirm the claimed speed-up. **Profile provenance:** part of the S0 profile (24 cases) was recorded in a shared work tree that had moved to S6; an isolated S0 re-profile gave identical executed-function sets, so no reach claim changes ([results.md](../03-experiment/results/results.md) provenance note). **One project only** (171 cases; networkx is not a performance-focused library, per the AI-SIM review).

**Q3: B1 was not validly tested outside networkx** (neither "replicated" nor "did not replicate") (static reach from one old base, as frozen; [results.md](../03-experiment/results/results.md) "Q3"; [findings.md](../knowledge-base/findings.md) B3):
- **geopandas:** 18/20 unreached as frozen, but the 2017 base biases the count; a post-hoc name heuristic gives 7/20; neither is a bound. Consistent with B1 under a heuristic, **not established**.
- **pvlib-python:** 14/14, **invalid** (the 2014 base has no asv suite; about 4 of 14 mined edits are optimizations).
- **bottleneck, states 1–8:** 4/8 as frozen [22–78%]; 0/8 under the post-hoc template interpretation.
- Replicating B1 would need measured profiles at each edit's parent and a mining rule with better precision, set before mining; counts only, no timing. Bottleneck's suite benchmarks functions by name, which suggests B1 depends on suite design.

**Slowdown oracle, FULL only** ([results.md](../03-experiment/results/results.md) "Slowdown oracle"). 10 frozen synthetic slowdowns, each in a function changed at its step; asv rule (ratio above 1.1, Mann-Whitney p below 0.002); one oracle run. #6 sits on step 8, a non-optimization edit; without it FULL still detects at most 3 of 9.

| Result | Count | Label |
|---|---|---|
| Detected by FULL, as classified | 3 of 10 (#1, #2, #8), Wilson 10.8–60.3% | measured, single run, provisional |
| Detected on target | 2 of 10 (#2, #8), Wilson 5.7–51.0% | measured, single run, provisional |
| Detected within the pre-set bands (≥ 2×, or 1.2–1.5×) | 0 | pre-registered: the regression set is empty |
| #1 | judged an oracle false positive by reading (off target, p = 0.0018) | label only; the A/A floor (0/46) cannot separate a 0.3% false rate from zero |
| Missed by FULL | 7: five (#0, 5, 6, 7, 9) reached by no benchmark (profile or static); #4 reached only statically, so a **coverage** miss; #3 reached by 3 profiled cases (ratios 0.95–1.01), so possibly a **power** miss of a small effect (< ≈1.1×) | measured |
| Slowed functions executed by no benchmark (S0 profile) | 7 of 10 | counts |

- **Pre-registered primary result:** regression safety of reduced selection is **not measurable** on networkx with the frozen set. What limits regression detection is **coverage and oracle power**, not the selection rule. On true-optimization functions: 6 of 9 slowdowns unreached.
- **Post-hoc, not pre-registered** ([LABELS.md](../03-experiment/results/raw/networkx/bench/LABELS.md)): #2 (1.90×, 8/8 profiled cases) and #8 (1.12×, 1/1) are on-target FULL detections outside the bands; both lie inside profile and static reach; the changed-module benchmark rule (0 cases) would miss both.

**Profile-completeness check** (the powered out-of-reach spot check, relabelled; **complete, 5 of 5 slowdowns**; [results.md](../03-experiment/results/results.md); [findings.md](../knowledge-base/findings.md) P5):
- **What it tests:** whether anything outside the measured reach slows down, i.e. whether the S0 profiles are **complete**. **It is not safety evidence.**
- **Result: 1 "slower" in 50 out-of-reach comparisons** (15 vs 15 samples). #9 (`DiGMState.__init__`) on `time_louvain_communities('Erdos Renyi (100, 0.9)')`: 1.13×, p = 0.0019. By the pre-registered C11 rule this **flags reach-based selection as unsafe for #9, and the flag stands.**
- **Re-check not confirmed:** a post-hoc partial re-check with a base-vs-base control (5 of 6 runs; no comparison was order-balanced) gave 0.97–1.01×. The function is in neither the static nor the profile reach of louvain, and the result sits just past both thresholds. With 50 null comparisons, the chance of at least one false "slower" is about 5%: noise is plausible, but neither direction is proven.
- Labels: #0 concurrent, #7 noisy (peak load 1.62).
- **#5 "faster" verdict** (0.628×, p = 3.4e-6, first case of its block, base first): the A/A order arm found no order effect but has low power, so its cause is **unresolved**.

**Benchmark A/A noise floor** (S0 against S0 in two clones, 23 frozen cases, 5 processes × 3 values, fixed and reversed order; measured 11:05–11:53 PKT, peak load 1.06; [results.md](../03-experiment/results/results.md) "Benchmark A/A noise floor"; [findings.md](../knowledge-base/findings.md) N6):
- **0 false verdicts in 46 per-repeat comparisons** (95% Wilson upper bound 7.7%; optimistic, because it is the same 23 cases twice).
- **The noise sits close to the threshold:** two A/A cases passed p < 0.002 and stayed "same" only on the ratio condition, and ratios up to 1.77 were "same" under the fixed order.
- **Order effect:** none detected (median 0.99, 10 of 23 first-slower, sign test p = 0.68), but power is low, so the #5 "faster" verdict stays **unresolved**.
- **Power from measured noise** (bootstrap, optimistic): 0.91 at 1.2× over all 23 cases, but for **2 of the 3** sampled `benchmark_algorithms` cases (3 of the module's 49) only about **2× slowdowns are reliably caught**. So FULL missing a small slowdown there can be a power failure of the oracle: #3 may be one; #4 is a coverage miss (W3). This does not change the B1 counts, which are about reach.
- **1 + 3σ noise floor:** the pre-registered ratio > 1 + 3·σ_noise condition has now been computed ([results.md](../03-experiment/results/results.md) "Pre-registered noise floor"), but σ exists only for the 23 A/A cases (2 repeats, not 5), and **none of the flagged "slower" verdicts is among them, so the rule cannot be applied to any reported verdict**; a deviation is recorded. A labelled post-hoc proxy (floors of same-class A/A cases) suggests #2's on-target verdict (about 1.85×) survives, while #1, #8 and #9 are ambiguous (#1 1.245×, #8 1.116×, #9 1.13×). The C11 flag for #9 stands.
- **State caveat** (from the AI-SIM review, not in results.md): the A/A ran 11:05–11:53, in the slow late-morning machine state, while #1, #2 and #8 were measured overnight.

Answers [P04](02-predicted-questions-and-answers.md), [P07](02-predicted-questions-and-answers.md), predicted first questions 1 and 4.

## S3. Functional selection is a solved, modest win (T1)

**Tests and build, networkx, 18 edits** (benchmarks not in these totals; est. end-to-end = est. test-s + build + 13.6 s pytest startup per step; [results.md](../03-experiment/results/results.md); `rq2_networkx.csv`):

| Arm | Tests run (Σ) | Est. end-to-end s | Measured end-to-end s | Missed (k/N) | 95% Wilson CI |
|---|---|---|---|---|---|
| A0 FULL | 121 824 | 1548 | 1634 (first runs, incl. 1 noisy state); 1413 (re-runs, **noisy**: none M5-clean) | 0/20 | 0–16.1% |
| A1 incremental build | 121 824 | 1524 | — | 0/20 | 0–16.1% |
| A2 testmon (PerfAgent-style) | 3 583 | 330 | 404 (**concurrent, pinned**) | 0/20 | 0–16.1% |
| A3 changed-module | 461 | 221 | — | **2/20** | 2.8–30.1% |

*Frozen mutants filtered by FULL; not a safety guarantee; simulated; caught almost by construction (M2); N = 20* ([rq2_steps.csv.faults.csv](../03-experiment/results/sim/networkx/rq2_steps.csv.faults.csv); [summary](../03-experiment/results/sim/networkx/rq2_steps.csv.summary.csv)).
- **testmon is 3.5–4× cheaper** than FULL end to end (mixed load), not the 15× that test-seconds suggest; startup and testmon's own analysis dominate its cost (first DB build 279.7 s against 88.0 s plain).
- **A3's two misses:** test-file names do not match the module (`isomorph.py`, `katz.py`); any periodic full check catches both. On the 15 true-optimization steps N = 18 and A3 misses 1/18 (`katz`); every other arm misses 0/18; conclusions unchanged ([results.md](../03-experiment/results/results.md) "networkx edit sets").

Answers [P13](02-predicted-questions-and-answers.md).

## S4. A deterministic policy on top does not help on this data (A4, RQ3)

Two separate statements ([results.md](../03-experiment/results/results.md) "RQ3 — C5 batching comparators", summary points 1 and 2):

**(a) Design limitation: the functional fault model cannot tell selection rules apart.** The mutants sit in the edited functions (M2), so every arm with a per-edit tier catches every mutant at its injection step **by construction**. Differences in caught-at-injection between per-edit arms and batching reflect the mutant model, not rule quality. A fault model that could separate rules (faults in callers or callees, interaction faults) was planned and not built ([review-final-results.md](../pm/advisor/review-final-results.md) (2), AI-SIM).

**(b) Real negative, for A4 as implemented:**
- On tests plus build, A4 (655 s est.) is **dominated by plain testmon** (330 s) and testmon + full every k=8 (541 s), all with 20/20 caught at injection.
- **With benchmarks counted, batching is 1.7–6× cheaper** than every arm with a per-edit benchmark tier; at A4's matched primary cost A4 costs **about 2×** batching (about 27 338 s against about 13 350 s interpolated). Benchmark weights come from one noisy pass; batching's bisection cost is not modelled, so its cost is a lower bound.
- This depends on **B2:** A4's profile selection collapses to all 171 cases after its first full check because checkpoint re-profiling was not built. B2 is unfinished design, not a result.

| Arm (C5 comparison, simulation) | Full checks | Est. s, no benchmarks | + benchmarks (noisy weights) | Missed | Caught at injection | Mean delay (steps) |
|---|---|---|---|---|---|---|
| BATCH cap = 2 / 3 / 5 / 8 | 9 / 6 / 4 / 3 | 774 / 516 / 344 / 258 | 15 783 / 10 522 / 7 015 / 5 261 | 0/20 | 9 / 6 / 5 / 2 | 0.55 / 1.05 / 1.70 / 3.65 |
| BATCH budget = 5 / 10 / 20 | 8 / 5 / 3 | 688 / 430 / 258 | 14 030 / 8 769 / 5 261 | 0/20 | 10 / 6 / 3 | 0.65 / 1.30 / 3.75 |
| A4 ours (T = 10) | 5 | 655 | 27 338 | 0/20 | 20 | 0 |
| testmon + k = 8 | 3 | 541 | about 30 560–30 950 (family) | 0/20 | 20 | 0 |
| testmon (no full check) / FULL | 0 / 18 | 330 / 1548 | 30 349 / 31 567 | 0/20 | 20 / 20 | 0 |

Other negatives, as measured:
- **A4 behaves like periodic full checks at k ≈ 4** (trigger at steps 3, 5, 8, 13 plus final, each from a module-level edit); the additive-budget trigger fires at exactly the same steps. Two of the five full checks (steps 8 and 13) come from non-optimization edits.
- **Accumulation:** 0 of 5 FULL-surviving mutants become detectable later, so the pre-registered null stands; caller faults were not generated.
- **C7:** 62 of 2589 functions (2.4%) get different test sets in repeat runs of the same code.

Answers [P11](02-predicted-questions-and-answers.md), [P14](02-predicted-questions-and-answers.md), [P15](02-predicted-questions-and-answers.md), [P16](02-predicted-questions-and-answers.md), predicted first questions 3 and 5.

## S5. Build reduction on bottleneck (harness lessons)

From [build-hazard-iterators-h.md](../03-experiment/results/build-hazard-iterators-h.md):
- **Harness lesson (H1), not a natural-edit hazard:** replayed state `98b59df2` does not compile because a prerequisite commit is missing from the replay (a **replay artefact**). The incremental tree kept the old `.so` files and passed 191/191; the clean build failed. Rule **B0** (a failed build is a reject) is kept; every harness already does this, so it is not a finding about reduced builds.
- **`iterators.h` stale-header hazard:** did **not** reproduce at the natural edits; the counterfactual probe leaves stale artefacts that are byte-identical to the correct rebuild.
- **B4 (`.so` hash comparison):** invalid as specified (the build path is embedded in every `.so`); fix after the meeting.

## S6. Worked edit (networkx step 10)

Source: [worked-edit.md](../03-experiment/results/worked-edit.md) (PRELIMINARY, with a diagram). Edit `c1c468d5`, "Optimize _build_paths_from_predecessors stack logic for 30-40% speedup (#8460)" (upstream commit subject; the speed-up is not re-measured). Selections use S0 data only.

| Arm | Tests run | Est. end-to-end tests s | Benchmarks run | Est. bench s (cost) |
|---|---|---|---|---|
| A0 FULL | 6768 | 85.99 | 171 | 1667.73 |
| A2 testmon | 20 | 13.61 | 171 | 1667.73 |
| A3 changed-module | 28 | 13.61 | 0 | 0.00 |
| A5 static-bench (testmon tests) | 20 | 13.61 | 171 | 1667.73 |
| **A4 single-edit view** (no accumulation; S0 depmap and profile) | 38 | 13.62 | 1 | 2.49 |

- End to end the test cost drops from about 86 s to about 14 s (about 6×), because pytest startup remains.
- Benchmark seconds are cost estimates from the **noisy** S0 pass; no benchmark verdict is shown.
- In the session simulation A4's last full check was step 8, so at step 10 it runs 71 tests and 171/171 cases (B2).

Answers [P05](02-predicted-questions-and-answers.md).

## S7. Noise floor and oracle repeatability (measured, with limits)

- **Benchmark A/A noise floor:** 0 false verdicts in 46 per-repeat comparisons (Wilson upper bound 7.7%, optimistic); noise close to the threshold; no order effect detected at low power; only about 2× slowdowns reliably caught on 2 of the 3 sampled `benchmark_algorithms` cases (3 of the module's 49; optimistic bootstrap); the 1 + 3σ condition cannot be applied to any reported verdict (no σ for those cases; deviation recorded). Details in S2. It cannot separate a 0.3% false rate from zero, so #1, #2, #8, the #5 "faster" verdict, the #9 flag and the `a638b282` outlier stay provisional.
- **Machine drift:** one module's per-process setup (`benchmark_algorithms`) drifted about 1.7–3× within a protocol during the day (about 10× only across protocols), while timing loops, timed samples and tests stayed stable; cause unknown (S1).
- **Also:** the 3.7× cost spread across 6 passes; M5 load labels (410 of 5330 slowdown-oracle runs above load 1.5); the post-hoc test `timing_label` rule (S16 noisy, S17 borderline; both normal on re-run); C7.
- Context (not a W3 result): full-benchmark verdicts do not repeat across machines in the literature (W2 headline 5; arXiv 2607.01211; [W2 README](../02-practice-survey/README.md)).

Answers [P20](02-predicted-questions-and-answers.md), predicted first question 4.
