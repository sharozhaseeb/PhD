# W3 results summary (PRELIMINARY)

**Status:** updated 2026-11-23 about 06:40 PKT for the advisor meeting. Sources of truth: [results.md](../03-experiment/results/results.md), [findings.md](../knowledge-base/findings.md) (rows N9–N14, V1, V2, R5, B4 are new since the last refresh), [build-hazard-iterators-h.md](../03-experiment/results/build-hazard-iterators-h.md), the paper draft [main.pdf](../04-paper/build/main.pdf) with its numbers file [numbers.tex](../04-paper/generated/numbers.tex), and the advisor-persona review [review-paper-draft-1.md](../pm/advisor/review-paper-draft-1.md) (AI-SIM). Every number is copied from the file cited next to it, with W3's labels kept: **PRELIMINARY**, **measured**, **computed**, **estimate**, **noisy**, **simulated**, **post-hoc**, **provisional**, **optimistic**. Nothing here is new analysis.

**Evidence boundary.** A **pilot** on one machine (WSL2 Ubuntu 24.04, i5-12400F, 7 GB): networkx with 18 replayed edits, of which **14 are optimizations by agent labels** (two agent raters plus an agent adjudicator; no human rater); bottleneck main window = states 1–8 of the amended window. Benchmark verdicts are now judged against the pre-registered 1 + 3σ noise floor where σ exists, but per-pass benchmark cost drifts for unknown reasons, 8 of the 9 networkx FULL passes are labelled noisy, and a directory confound in the A/B oracle is not yet resolved (S7).

**Superseded figures, do not use:** "at least 0.9–4.5 h" per pass; "40–180×"; the bottleneck "about 22%" build share; "8–28×" as the cost range (now 9 passes, see S1); B1 "9/15" as the primary figure (now 8/14 on agent labels); "FULL detects 2 or 3 of 10" (now 1/10 above the floor); "the 1 + 3σ floor could not be applied" (now applied to the 12 flagged verdicts); the #9 profile-completeness flag (does not survive the floor); "#3 may be a power miss" (now a dilution miss); any "A4 beats batching" wording ([findings.md](../knowledge-base/findings.md) N9, V1, B4, N12 and "Corrections").

## What may be shown (TPM go/no-go and PM rulings)

The TPM rule: no W3 number without the A/A noise floor and the injection-based miss counts ([TPM log, go/no-go](../pm/tpm-log.md)). **Both now exist:** σ_noise has been measured for the 12 flagged verdicts (120 runs, 5 repeats, ABBA) and the 1 + 3σ floor is applied to them ([findings.md](../knowledge-base/findings.md) N9). Rulings still applied:
- **PM, 2026-11-21:** functional miss counts as k/N with the Wilson CI, labelled "frozen mutants filtered by FULL; not a safety guarantee", with the construction bias (M2).
- **PM, 2026-11-21:** no speed-up claim from benchmarks; benchmark seconds are **cost**.
- **PM, 2026-11-22:** the slowdown oracle is reported with W3's labels; its pre-registered result is "regression safety not measurable on networkx with the frozen set".

Also not to be claimed ([TPM log, "Must not be claimed"](../pm/tpm-log.md)): "safe" or "no misses" as a general property; generalisation beyond the projects, the edit sample or this machine; perf-regression detection below the measured noise floor; confirmation of the historical commits' speed-ups unless re-measured; build-time savings for Python unless measured as non-negligible; novelty before W1's recorded search (B1 is now narrowed by Traini et al. 2021, S2); an iterative-session effect from replay of non-adjacent commits; anything about AI-based selection.

## The story in four steps

1. **Where the cost is (R1), now on two projects.** Benchmarks, not build or tests, dominate per-edit validation cost. networkx: at least about 8× build plus tests, median about 14× over 9 passes, up to 34× under unexplained drift; bottleneck: about 18.5–19×. On networkx 80–95% of a pass is outside the timing loops in one module's setup, which caching, not selection, would reduce; the setup-cached pass (E5) is not yet measured.
2. **The benchmark oracle often cannot see the edit: executed, visible, detectable.** On networkx, **8 of 14 agent-labelled optimizations are executed by no benchmark** (57%, Wilson 33–79%). Of the edits that are executed, the changed function's share of case time limits what a slowdown can show: at a 1.2× function slowdown **at most 4 of 14 edits can even clear asv's 1.1 ratio** (5 of 14 at 2×). Above the pre-registered noise floor, **FULL detects 1 of 10** frozen slowdowns (2 by asv's rule alone). B1 is a networkx-only finding; Traini et al. 2021 is the closest method precedent, so novelty is narrowed to the uncovered-edit rate.
3. **Functional selection is a solved, modest win (T1).** testmon is 3.5–4× cheaper than FULL end to end and misses 0/20 frozen mutants (simulated; caught almost by construction). PerfAgent already uses it per edit.
4. **A deterministic policy on top does not help on this data (A4).** The fault model cannot tell selection rules apart (a design limitation), and A4 as implemented costs more than testmon and, once benchmarks count, about 2× batching (finding B2).

## S1. Where the cost is (RQ1), two projects

**networkx, FULL** ([results.md](../03-experiment/results/results.md) "RQ1 headline", "(d) Three repeated FULL networkx passes", "Pass labels"; [findings.md](../knowledge-base/findings.md) R1, N12, N13; [numbers.tex](../04-paper/generated/numbers.tex) `NxBenchPassMedian`):

| Component | Value | Label |
|---|---|---|
| Benchmarks (171 asv cases, 2 processes × 3 values) | **659–2,984 s per pass over 9 passes; median about 1,220 s**, i.e. at least about 8×, median about 14×, up to about 34× build plus serial tests (about 87 s) | measured; **8 of 9 passes noisy** by the uniform rule (any run above load 1.5 or gate not ok) |
| of which timing loops | 132–171 s per pass, stable across all 9 passes | measured |
| of which outside the timing loops | 79.9–94.8% of a pass, mostly per-process setup in one module (`benchmark_algorithms`, 49 cases, 86.9–96.8% of a pass) | measured |
| "Setup cached" pass (E5) | about 130–170 s, about 1.5–2× build plus tests | **estimate, not measured**; E5 is planned for the night of 23→24 |
| Tests (6771, serial) | about 71–89 s per edit, excluding the S16/S17 first runs | measured; re-runs noisy |
| Build (`pip install -e`) | median 1.19 s; about 0.09% of build plus tests plus the median pass of about 1,220 s (0.04–0.16% over the 9 passes) | measured |

- **Drift (N12):** three repeated passes at S0 in one evening took 2,984, 1,694 and 1,217 s (a 2.45× drop); 1,763 of the 1,767 s drop was in `benchmark_algorithms`, while the timed loops stayed at 144–155 s. No telemetry covariate tracks it; **cause unknown**. Earlier within-protocol drift was about 1.7× and 3× (N7).
- **Reading:** the direction holds on every pass; the magnitude is a range, not one number.

**bottleneck (C extension)** ([results.md](../03-experiment/results/results.md) "(c) Two FULL asv benchmark passes for bottleneck"; [findings.md](../knowledge-base/findings.md) R5, R2):
- Two FULL benchmark passes at **544 and 547 s** (0.5% apart), about **18.5–19× build plus tests**; one state, both passes labelled noisy.
- Build is about 16–18% of build plus tests, but only **0.8–0.9% of total per-edit validation** once benchmarks count. So **reduced build is a minor lever** in both projects.
- About 27% of bottleneck's benchmark wall is in timed loops; the non-loop time was not decomposed.

**Open:** the scikit-learn heavy-build measurement was not run; E5 (setup-cached pass) decides how robust "expensive" is ([review-paper-draft-1.md](../pm/advisor/review-paper-draft-1.md) §2 RQ1, AI-SIM).

Answers [P01](02-predicted-questions-and-answers.md), [P03](02-predicted-questions-and-answers.md), M6, M7.

## S2. The oracle gap: executed, visible, detectable (networkx)

**Executed (B1, coverage).** Edit labels now come from two blind agent raters plus an agent adjudicator against a frozen codebook (decision D26; κ 0.948, likely inflated because the raters are the same model) ([findings.md](../knowledge-base/findings.md) B4; [precision_b1.json](../03-experiment/results/labelling/precision_b1.json)).

| Reach measure (networkx, S0) | 14 agent-labelled optimizations | Earlier figures (superseded as primary) |
|---|---|---|
| Measured profile | **8/14 unreached, 57% [33–79%]** | 9/15 by subject-only reading; 12/18 over all replayed edits |
| Static call graph | 3/14, 21% [8–48%] | 4/15 |

- **Mining precision** of the keyword rule: networkx 15/20, bottleneck 15/16, geopandas 17/20, pvlib 3/14; **pooled 50/70 = 71% [60–81%]**, labelled by agents only.
- **Construct check:** 0 of 14 edits are unreached by construction (every changed function exists at S0 and at the parent); profiles from S0 only remain a limitation (V1).
- **Elsewhere:** B1 was **not validly tested** outside networkx (Q3: static reach from old bases, pvlib without an asv suite, bottleneck template code). A pre-registered replication (E1) is planned after the meeting.
- **Novelty, narrowed:** Traini et al. (TOSEM 2021) already profile per commit which methods JMH benchmarks execute (refactoring commits, 31 Java projects) but report no uncovered-commit rate. Per-commit profiling of benchmark reach is therefore not new; the measured uncovered-edit rate for optimization commits is the open part ([beyond-literature-claims.md](../01-literature/beyond-literature-claims.md) row B1).
- **Open disagreement on labels:** the advisor-persona review will not accept agent-only labels for E1 and asks for at least a blind human-labelled subset with human-agent κ; the owner decided labels stay agent-only (D26; [WORKLOG](../knowledge-base/WORKLOG.md) 16:38). See ask A14.

**Visible (share).** A slowed function's share of a benchmark case's time bounds the ratio the case can show (about 1 + share × (f − 1)) ([findings.md](../knowledge-base/findings.md) V1, V2; [edit_share.json](../03-experiment/results/raw/networkx/edit_share.json)):
- Per edit (14 agent-labelled optimizations, S0 profile share): 8 not executed; step 4 executed but diluted (share 0.021: ×1.004 at a 1.2× function slowdown, ×1.021 at 2×); steps 3, 9, 10, 14, 16 have shares 0.86, 1.00, 0.50, 0.57, 1.00.
- **At a 1.2× function slowdown at most 4 of 14 edits can clear asv's 1.1 ratio; at 2×, 5 of 14** (computed, no timing).
- Slowdowns: #2 share about 0.85 → expected about 1.85×, observed 1.81–1.90×; **#3 share about 0.005 → a dilution miss**, not a power miss (earlier wording superseded). #4 is a coverage miss (static reach only).

**Detectable (power and noise floor).**
- **Noise floor applied (N9):** with σ measured for the 12 flagged verdicts (120 runs, 5 repeats, ABBA), **FULL detects 1 of 10 slowdowns above the floor (Wilson 1.8–40.4%)**, down from 2 by asv's rule alone. Only #2's 8 on-target cases survive (floors 1.08–1.33 against ratios 1.81–1.90). #8 (floor 2.18), #1, NonNeighbors and #9 do not survive. **The #9 profile-completeness flag does not survive the floor.**
- **Power at the verdict design (N10, computed):** 18 v 18 with the exact test and the floor, all cases: 0.96 at 1.2×; the heavy module (3 cases): 0.035–0.13 at 1.2×, **0.84 at 1.5×**, 0.985 at 2×. So the heavy module reliably resolves only about 1.5× and above (σ from 2 repeats, 3 algorithm cases, optimistic bootstrap).
- **Pre-registered primary result (unchanged):** regression safety of reduced selection is **not measurable** on networkx with the frozen set.

Answers [P04](02-predicted-questions-and-answers.md), [P07](02-predicted-questions-and-answers.md), M1–M5.

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
- **A3's two misses:** test-file names do not match the module (`isomorph.py`, `katz.py`); any periodic full check catches both. On the 15 true-optimization steps by the earlier subject-only reading (not the 14 agent labels), N = 18 and A3 misses 1/18 (`katz`); every other arm misses 0/18; conclusions unchanged ([results.md](../03-experiment/results/results.md) "networkx edit sets").

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

Answers [P11](02-predicted-questions-and-answers.md), [P14](02-predicted-questions-and-answers.md), [P15](02-predicted-questions-and-answers.md), [P16](02-predicted-questions-and-answers.md), M8.

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

## S7. Noise floor and oracle repeatability

- **A/A noise floor (N6):** 0 false verdicts in 46 per-repeat comparisons on 23 cases (Wilson upper bound 7.7%, optimistic); noise close to the threshold.
- **σ and the 1 + 3σ floor for the 12 flagged verdicts (N9):** measured (120 runs, 5 repeats, ABBA); applied in S2.
- **Oracle repeatability, E3 tier 1 (N11):** **12 of 14 verdict-relevant cases repeat.** #2's 8 on-target cases are slower again (1.76–1.90×). The two off-target flags (#1, NonNeighbors) do not repeat, which supports reading them as noise. #8 is slower pooled (1.20×) but "same" in both order-balanced pairs and far below its 2.18 floor: fragile. #3 is "same" 3/3, consistent with dilution.
- **E3 tier 2 and a directory confound (N14):** 488 of 499 verdicts agree; **11 new off-target non-"same" verdicts (2.2%, about 11× the nominal rate)**, 7 slower and 4 faster. In every run the base side used one clone directory and the slowed side the other, so **edit and directory are fully confounded**; a slowdown patch cannot make code faster, so the 4 "faster" flips point to a clone or layout bias. #2's 1.8× is far beyond that bias; #8's 1.12–1.20× and the off-target flags are not. **Fix:** a directory A/A and directory rotation between sides, starting tonight (decision D28). Load could not be tested (5 of 1,356 runs above 1.5).
- **Pass labels (N13):** one uniform rule; 8 of 9 networkx FULL passes are noisy.
- Context (not a W3 result): full-benchmark verdicts do not repeat across machines in the literature (W2 headline 5; arXiv 2607.01211; [W2 README](../02-practice-survey/README.md)).

Answers [P20](02-predicted-questions-and-answers.md), M4.

## S8. The paper draft

- **[main.pdf](../04-paper/build/main.pdf)**, 14 pages, title "Can the Benchmarks See the Edit? Cost and Visibility of Per-Edit Validation for Python Optimization Commits — A Case Study on networkx". Every number comes from [numbers.tex](../04-paper/generated/numbers.tex), computed from the raw files ([04-paper README](../04-paper/README.md)).
- **Advisor-persona verdict on draft 1** ([review-paper-draft-1.md](../pm/advisor/review-paper-draft-1.md), AI-SIM): right story, wrong size (PM's summary, [WORKLOG](../knowledge-base/WORKLOG.md) 16:52). Until the replication (E1) lands it is a short paper; E1 should reach **at least 4–5 projects and 50–60 true optimizations**, with profiles at each edit's parent and a human-labelled subset. Draft 2 applied the text changes (merged oracle section framed executed/visible/detectable, per-edit table, claims C1–C12) ([WORKLOG](../knowledge-base/WORKLOG.md) 16:58).
- **Still open before submission:** E1 (after the meeting), E5 setup-cached pass (night of 23→24), the directory A/A (tonight), the human-label question (A14), venue and timeline (A10).
