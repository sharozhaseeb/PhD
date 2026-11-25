# Deck fact sheet: Study 1 advisor meeting (2026-11-24)

Author: TPM subagent, written 2026-11-24 for the slide deck. Nothing was run; this is a reading of the files.

**Rule for the deck:** use only the values in §1. Where sources disagree, `04-paper/generated/numbers.tex` wins (generated from raw files). I checked that numbers.tex is current: its header hashes (results.md `3c06ea6b303a`, findings.md `fbc55eab779e`) match the files on disk now, and it was regenerated at 03:28 on 24 Nov, after the last night-2 write-up.

Abbreviations: RM = `03-experiment/results/results.md`; KB = `knowledge-base/findings.md`; NT = `04-paper/generated/numbers.tex` (macro name in brackets).

---

## 1. Headline numbers the deck may use

### Scope: what was studied

| Claim | Value | n | Source | Say aloud |
|---|---|---|---|---|
| Projects with experiments | **2**: networkx (pure Python, all RQs) and bottleneck (C extension, cost and build only) | 2 | RM "Status of each piece"; KB header | A pilot. B1 (coverage) is **networkx only**. |
| Projects mined and labelled for mining precision | **4** (networkx, bottleneck, geopandas, pvlib) | 70 qualified commits (81 sheet rows) | NT `PrecPooledN`, `LabelRows`; RM §Mining precision | geopandas and pvlib were **not** replayed or benchmarked. |
| networkx edits | 20 mined → **18 replayed** (19 states incl. base) → **14 optimizations by agent labels** (15 by the earlier subject-only reading) | 18 | NT `NxMined`, `NxReplayed`, `NxStates`, `NxAgentOpt`, `NxManualOpt` | Labels are from AI agents (see risk 1). |
| bottleneck edits | 16 qualifying → 13 applied → **8 in the main window** (states 1–8, base `f51ed86`) | 8 | NT `BnEdits`; decisions D06, D19 | States 9–13 held out (replay artefact `98b59df2` does not compile). |
| Test and benchmark suites | networkx **6,771 tests, 171 benchmark cases**; bottleneck **191 tests, 840 benchmark cases** | — | NT `NxNumTests`, `NxBenchCases`, `BnNumTests`, `BnBenchCases` | |
| Injected faults (networkx) | **25 frozen mutants** (20 killed by FULL); **10 frozen slowdowns** | 25 / 10 | NT `MutantsFrozen`, `MutantsKilled`, `NumSlowdowns` | Frozen with sha256 before any arm ran (D04). |
| Hardware | One laptop: WSL2 Ubuntu 24.04, i5-12400F, 6 cores, 7 GB | 1 | RM "Platform" | Every timing claim is "on this machine". |

### RQ1: cost

| Claim | Value | n | Source | Say aloud |
|---|---|---|---|---|
| A full networkx benchmark pass costs | **659–2,984 s per pass; median ≈ 1,220 s** | 9 passes | NT `NxBenchPassMin/Max/Median`; RM §(d) "R1 update" | A range, never one number. **8 of 9 passes are labelled noisy** (NT `PassesNoisy`). |
| Benchmarks vs build + serial tests (≈ 87 s) | **≈ 8× on the fastest passes, ≈ 14× at the median, up to ≈ 34× under drift** | 9 passes | NT `NxBenchRatioTypical`, `NxBenchRatioMedian`, `NxBenchRatioHi`; abstract | The strict minimum is **7.6×** (659/87). Say "about 8×", not "at least 8×" (see §2, D7). |
| Timed loops inside a pass | **132–171 s**, stable over all 9 passes | 9 | NT `NxLoopsLo/Hi` | The cost is outside the loops. |
| Share outside the timing loops | **79.9–94.8 %** of a pass; one module (`benchmark_algorithms`, 49 cases) is **86.9–96.8 %** | 9 | NT `NxOutsideLoopsLo/Hi`, `NxAlgoShareLo/Hi` | Per-process start-up and re-import, **by inference** (STD has no phase timers). |
| **E5 (measured, night 2):** standard vs setup-cached pass | **STD median 691 s, CACHED median 195 s, a factor of 3.54×** | 3 STD/CACHED pairs, 1 night | NT `EStdMedian`, `ECachedMedian`, `EStdOverCached`; RM §E5; KB N15 | That night's STD passes were at the **fast end** (679–705 s). The ratio on slow nights is not measured. |
| Setup-cached pass vs build + tests | **≈ 2.2–2.3×** (STD ≈ 7.8–8.1× on the same night) | 3 pairs | NT `ECachedRatioLo/Hi`, `EStdRatioLo/Hi` | Benchmarks stay the largest part, but **not by an order of magnitude**. CACHED is a cost lower bound, not an asv replacement. 1 of 171 cases is sample-shifted. |
| Overhead that caching removes | ≈ 484–504 s of each STD pass, i.e. **≈ 72 %** of a standard pass | 3 pairs | RM §E5 (STD minus paired CACHED); 72 % is my arithmetic (496/691) | Do **not** say "3.54× of a pass is overhead" (see §2, D8). |
| bottleneck benchmarks vs build + tests | **544 and 547 s per pass, ≈ 18.5–19× build + tests** | 2 passes, 1 state | NT `BnBenchPassLo/Hi`, `BnBenchRatioLo/Hi`; RM §(c) | One state; both passes noisy; build + tests are themselves noisy. |
| Build share | networkx build median **1.19 s**, ≈ 0.09 % of build + tests + the median pass; bottleneck build **16–18 % of build + tests**, but **0.8–0.9 %** once benchmarks count | 19 states / 3 repeats | NT `NxBuildMedian`, `BnBuildShareLo/Hi`, `BnBuildShareBenchLo/Hi`; pack 03 S1 | Reduced build is a minor lever in both projects. No heavy-build project was measured. |
| Test selection (testmon) | **3.5–4× cheaper than FULL end to end**, not the 15× that test-seconds suggest | 1 run, 18 edits | NT `TestmonRatioLo/Hi`, `TestSecRatio` | Mixed load, single run. Pytest start-up (13.6 s) stays. |

### RQ2: the oracle gap (networkx only)

| Claim | Value | n | Source | Say aloud |
|---|---|---|---|---|
| **B1: optimizations executed by no benchmark (measured profile)** | **8 of 14 = 57 %, Wilson 95 % CI 33–79 %** | 14 agent-labelled optimizations | NT `BOneAgentUnreached`, `BOneAgentPct/Lo/Hi`; KB B4 | **"Many", not "most"**: the CI includes 33 %. One project, profiles from S0 only, labels by same-model agents. |
| B1 by static call graph | 3 of 14 = 21 %, CI 8–48 % | 14 | NT `BOneAgentStatic*` | Static reach over-approximates. |
| B1 on the earlier subject-only labels | 9 of 15 = 60 %, CI 36–80 % | 15 | NT `BOneManual*` | Superseded as the primary figure. Show only as a sensitivity check. |
| Construct check | **0 of 14** edits unreached by construction | 14 | NT `ConstructUnreached`; KB V1 | Every changed function exists at S0 and at the parent. |
| Mining precision of the keyword rule | **50 of 70 = 71 %, CI 60–81 %** pooled; networkx 15/20, bottleneck 15/16, geopandas 17/20, pvlib 3/14 | 70 | NT `PrecPooled*`, `PrecNx` … `PrecPv` | Agent labels; κ **0.948** (79/81 agree), inflated because both raters are the same model. |
| Visibility (share of case time) | At a **1.2× function slowdown at most 4 of 14** edits can move a benchmark past asv's 1.1 ratio; **at 2×, 5 of 14** | 14 | NT `EditsClearMid/High`; KB V2 | Computed from cProfile shares, no timing. |
| **Detection above the pre-registered noise floor** | FULL detects **1 of 10** slowdowns on target above 1 + 3σ (**Wilson 1.8–40.4 %**); **2 of 10** by asv's rule alone; 3 of 10 as classified | 10 slowdowns | NT `FloorDetect*`, `SlowDetOnTarget`, `SlowDetClassified`; KB N9 | σ measured only for the 12 flagged verdicts (120 runs, 5 repeats, ABBA). |
| The one detection (#2, `_dijkstra_multisource`) | **1.81–1.90×** on 8/8 profiled cases; repeat (tier 1) **1.76–1.90×**; floors 1.08–1.33; share 0.84–0.86 | 8 cases | NT `SlowTwoRatioLo/Hi`, `RepTwoLo/Hi`, `ShareTwoLo/Hi`; RM §(b), §E3 tier 1 | Robust: well above the largest identical-code deviation (≤ 1.38×). |
| Misses by type (10 slowdowns) | **Coverage: 7** (#0, 1, 4, 5, 6, 7, 9: no profiled benchmark executes the slowed code; #4 reached by static reach only). **Dilution: 1** (#3, share 0.004–0.005, so ≈ 1.005× expected). **Below the noise floor: 1** (#8, 1.116× vs floor 2.18; its own A/A also said "slower", 1.129×). **Detected: 1** (#2). | 10 | NT `SlowUnreachedProfile`, `ShareThreeLo/Hi`, `FloorEight`, `EightAAPooled`; abstract; KB S2, V1, N9 | The 7 + 1 adds up to the abstract's "8 not detected on target by asv's rule". The pre-registered primary result is still **"regression safety not measurable on networkx with the frozen set"** (D13). |

### Noise, power, drift, repeatability

| Claim | Value | n | Source | Say aloud |
|---|---|---|---|---|
| A/A noise floor (S0) | **0 false verdicts in 46** comparisons, Wilson upper bound **7.7 %** | 23 cases × 2 repeats | NT `AAFalse`, `AAComparisons`, `AAUpper` | Optimistic: the same 23 cases twice. Ratios up to 1.77 still read "same". |
| Power at the paper's verdict design (18 v 18, exact test + floor) | All cases: **0.96 at 1.2×**. Heavy module (3 sampled cases): **0.035–0.13 at 1.2×, 0.84 at 1.5×, 0.985 at 2×** | 23 cases (3 heavy) | NT `PowDesignAllMid`, `PowDesignAlgoMid`, `PowDesignAlgoMidBoot`, `PowDesignAlgoOneFive`, `PowDesignAlgoTwo`; KB N10 | The heavy module reliably resolves only **≈ 1.5× and above**. σ from 2 repeats, optimistic bootstrap. |
| Drift within one evening | 3 repeated passes at S0: **2,984 → 1,694 → 1,217 s (2.45×)**; timed loops stayed **144–155 s** | 3 passes | NT `DriftEveningHi/Lo/Ratio`, `DriftLoopsLo/Hi`; KB N12 | 1,763 of the 1,767 s drop is in `benchmark_algorithms`. **Cause unknown**; no telemetry covariate tracks it. Earlier within-protocol drift ≈ 1.7–3× (NT `DriftWithinLo/Hi`). The old "10×" is **withdrawn**. |
| Pass-to-pass spread | **4.5×** (max/min over 9 passes) | 9 | NT `NxPassSpread` | |
| Repeatability, tier 1 (verdict-relevant cases) | **12 of 14 verdicts repeat** (ABAB, 112 runs, 24 v 24) | 14 | NT `RepAgree`, `RepTotal`, `RepRuns`; KB N11 | The 2 that do not repeat are the off-target flags (#1, NonNeighbors), which turn into "same": they were noise. #8 repeats "slower" pooled (1.202×) but is fragile and below its floor. |
| Repeatability, tier 2 (all other reached cases) | Fixed directories: **488 of 499 agree**. Directory-swapped: #8 **165/170**, #1 **168/170** | 499 + 340 | NT `TwoAgree`, `TwoTotal`, `SwapTotal`, `SwapFlips`; RM §E3 tier 2, §swap | E3 tier 2 is now complete for all 5 reached slowdowns. |
| **Off-target false-verdict rate (A/B oracle, 12 v 12)** | **Fixed directories 2.2 % (11/499, Wilson 1.2–3.9 %); identical code 2.4 % (4/168, Wilson 0.9–6.0 %); directories swapped 1.8 % (6/340)** | 499 / 168 / 340 | NT `TwoFlipPct/Lo/Hi`, `DirAAPct/Lo/Hi`, `SwapPct`; KB N14 | **≈ 2 % per comparison, i.e. ≈ 4 false "changes" per 171-case FULL comparison (1.6–10)** (NT `DirAAFalsePerComp`). Identical code gives the same rate, so the flips need no edit. The swap reverses no flip, so it is **not a directory effect alone. Cause unresolved.** Wilson intervals are too narrow (cases share runs). The swap Wilson CI is not in NT; my computation gives ≈ 0.8–3.8 %, so do not put it on a slide unless W3 adds a macro. |
| Size of a single verdict that is not evidence | **≤ ≈ 1.4× in either direction** (largest identical-code deviation 1.308× slower, 0.725× faster) | 168 | NT `DirAAMaxDev`; RM §Directory A/A | This covers #8, #1, #9, NonNeighbors and all tier-2 flips. #2's 1.76–1.90× stands. |

### Functional side and policy (short)

| Claim | Value | n | Source | Say aloud |
|---|---|---|---|---|
| Missed frozen mutants | FULL, testmon and A4: **0/20** (Wilson 0–16.1 %); changed-module rule A3: **2/20** (2.8–30.1 %) | 20 | NT `MutantsNone`, `ZeroMissHi`, `AThreeMissed/Lo/Hi` | Simulated; mutants sit in edited functions, so they are caught almost by construction (M2). **Not a safety guarantee.** |
| Our policy A4 | Adds nothing measurable; costs **655 s est.** vs testmon **330 s** at equal detection; behaves like a full check every **k ≈ 4** | 18 edits | NT `EstAFour`, `EstTestmon`, `AFourK` | Honest negative. No "A4 beats batching" claim (D23). |

### Compute spent (inferred)

| Claim | Value | Source | Say aloud |
|---|---|---|---|
| Machine time for measurement | **≈ 32–37 h wall-clock** over 21–24 Nov: night 1 ≈ 10.3 h (19:38–05:58), 22 Nov day ≈ 4.6 h (including a lost 1.4 h A/A), night of 22→23 ≈ 12.2 h, night 2 ≈ 4.7 h, plus ≈ 3–5 h of 21 Nov set-up runs (tests, profiles, depmaps) | My sum of the run windows logged in RM and `knowledge-base/WORKLOG.md` | **Inferred, not summed from raw run records**, and it includes several hours of per-run gate waits. Say "about 35 hours of machine time over three nights", not a precise figure. The verdicts rest on 1,026 recomputed verdicts (NT `RecomputeVerdicts`, 0 changed under the exact test). |

---

## 2. Numbers that differ between sources

numbers.tex and the paper abstract agree with each other on every number I checked. The disagreements are in the older prose files.

| # | Item | results.md | findings.md (KB) | Meeting pack | numbers.tex / raw (wins) | Deck should say |
|---|---|---|---|---|---|---|
| D1 | Cost of a networkx pass | RQ1 headline still says **659–2,444 s over 6 passes, median ≈ 730 s, 8–28×** (§(d) has the 9-pass update) | R1 row still says the same (superseded by N12, but R1 was not edited) | 9 passes, median ≈ 1,220 s, 8–34× (correct) | **659–2,984 s, 9 passes, median 1,220 s, ≈ 8× / 14× / 34×** | numbers.tex values |
| D2 | Setup-cached pass | Headline keeps the old 1.5–2× estimate, but marks it superseded by E5 | R1 still says **1.5–2× (estimate)**; N15 has the measurement | **Stale:** 03 S1 table, one-pager and Q&A M7 still say **1.5–2×, not measured, "E5 runs the night of 23→24"** | **Measured 2.2–2.3×; STD/CACHED 3.54×** | E5 values. Drop every "1.5–2×". |
| D3 | Build share with benchmarks (networkx) | **≈ 0.15 %** (from the old 730 s median) | same | **≈ 0.09 %** (0.04–0.16 % over 9 passes) | Macro `NxBuildShareBench` = 0.15 is quoted from the old median and is **stale**. It is not used in the paper text. 1.19 / (1,220 + 87) = 0.09 % | "≈ 0.1 %" or the pack's 0.09 %. W6 should regenerate or delete the macro. |
| D4 | `benchmark_algorithms` share | 86.9–95.5 % (6 passes) in the headline | R1: 87–96 % / 88–94 % | 86.9–96.8 % | **86.9–96.8 %** (9 passes) | 86.9–96.8 % |
| D5 | B1 primary figure | 9/15 in older sections | B1 row: **9/15**; B4 row: 8/14 supersedes | 8/14 (correct) | **8/14 = 57 % [33–79 %]** | 8/14 |
| D6 | p-values and power | — | S1: #1 p = **0.0018**; P5: #9 p = **0.0019**; N6: power **0.91** at 1.2× (old normal-approximation test) | — | Exact test: #1 **1.27e-3**, #9 **1.19e-3**; A/A power **0.93** at 1.2× (`SlowOneExactP`, `SlowNineExactP`, `PowAllOneTwo`) | Exact values if shown at all (they are below-floor verdicts anyway). |
| D7 | "At least ≈ 8×" | — | — | "at least about 8×" | `NxBenchRatioLo` = 8 is 659/87 = **7.6** rounded up; the four fastest passes give 7.6–8.6× | "about 8×" (or "≥ 7.6×"). Also affects the abstract and conclusion wording. |
| D8 | Caching overhead | "≈ 484–504 s of each pass" | — | — | Paper `rq1-cost.tex` L46: "about \EStdOverCached× of a standard pass is overhead" reads as **"3.54× of a pass"**, which is wrong | "≈ 72 % of a standard pass", or "a standard pass costs 3.54× a cached one". W6 to fix. |
| D9 | Off-target flips explanation | Tier-2 text: the "faster flips favour a clone or layout bias" reading is **withdrawn** | N14 current (cause unresolved) | **Stale:** 03 S7 says the faster flips "point to a clone or layout bias" and the directory A/A "starts tonight"; one-pager same | Not a directory effect alone; cause unresolved | N14 wording |
| D10 | Paper threats, directory | — | — | — | `threats.tex` L17 says **"Every A/B comparison"** ran in fixed directories, which is no longer true: night 2's swap runs balanced the directories | Not a deck number, but W6 should fix it before the PDF is shown. |
| D11 | Open work list | — | `open-questions-and-next.md` was last updated 22 Nov 06:12 and lists the A/A, the repeat and the spot check as "not run" | — | All of these have been run since | Do not show that file. |

---

## 3. Schedule and next steps

**Where E1 stands today (24 Nov).** Nothing for E1 has been built or frozen:
- The grouped profile runner is a design only (`03-experiment/docs/grouped-profile-runner.md`, "not built, not run"). `bth.benchrun` has `measure-cached` (one process per module) but no grouped `profile` mode.
- There is no frozen E1 pre-registration and no mining rule v2. The adjudicator proposed v2 codebook rules (WORKLOG 15:52).
- Labels so far are agent-only. The advisor persona will not accept that for E1 (ask A14).

**What E1 costs (inferred from the TPM plan and the advisor-persona review):**

| Part | Engineering / human | Machine | Notes |
|---|---|---|---|
| Rule v2 + pre-registration frozen | 2–3 h, plus the owner's 1 h review | — | Must come before any new mining. |
| Grouped profile runner, built and validated on networkx S0 (must reproduce 171/171 reach sets) | 4–5 h | 10–30 min | Without it, per-case profiling costs ≈ 15–50 h of machine time, which is not feasible. |
| Project set-up (clone, old Python via uv, build at old parents), per project | 2–4 h each, capped at 4 h | 0.5–1 h each | **Environment rot at old parents** is the main attrition risk. |
| Profiling at each edit's parent | — | ≈ 3–10 min per state, so ≈ 4–13 h for 4–5 projects × 15–20 edits | Not timing-sensitive, so it can run in the daytime, but never during a timing window. |
| Labels: agents on all rows; **human blind subset** (all 20 networkx rows + a random 30 E1 rows) if the advisor insists | Agent: ≈ 1 h. Human: ≈ 3–5 h for 50 diffs | — | The advisor persona puts the human effort at 3–4 days including rule work and diff reading. |
| Analysis (per project and pooled Wilson CIs, forest plot), critic pass, paper update | 6–10 h | — | |
| **Total** | **≈ 25–40 h of engineering and owner time** | **≈ 8–20 h machine** | |

**Size needed.** The advisor bar is ≥ 4 projects giving ≥ 50 true optimizations, or ≥ 5 projects and ≥ 60. At 71 % mining precision and ≈ 10 % replay loss, that means **≈ 80–95 mined commits**, i.e. 5–6 candidate projects attempted to keep 4–5 after attrition.

**Realistic before the next meeting** (date unknown; I assume about 2 weeks away):
- **Week 1:** freeze rule v2 and the pre-registration; build and validate the grouped runner; set up the first 2 projects. Owner labels the 20 networkx rows blind, which gives a human-agent κ early.
- **Week 2:** profile 2–3 projects; report per-project B1 with CIs.
- **Not realistic by then:** the full 4–5 project pooled result. The advisor persona's own estimate is **E1 complete mid-to-late December**, draft 2 of the full paper mid-January, submission-ready around February.
- **The TPM plan's 15 Dec full-draft date is no longer realistic with E1 in it.** E1 was planned to start on 25 Nov with (e) done first; (e) is done (agent labels), but the runner and the pre-registration are not started. **Recommend telling the advisor "E1 results by about 20 December, full draft mid-January"** rather than 15 Dec, and offering an earlier short paper on networkx if a workshop deadline fits. No CFP has been checked.
- **No new timing work is needed for E1** (it is profiling only). Optional timing items (E4 second-project cost, per-case σ) compete for the same nights and should wait unless the advisor asks.

---

## 4. Top 5 presentation risks

1. **"No AI in the method" next to AI-made labels.** The method (selection, oracle, analysis) is deterministic, but the **denominator of B1 (the 14 optimizations) and the 71 % mining precision come from LLM agent raters** (same model, κ 0.948). If the deck says "no AI" without this, the advisor will catch it. Say: "No AI in the validation method; edit labels were made by two blind agent raters plus an adjudicator, which is a disclosed threat, and a human-labelled subset is ask A14." The abstract also opens with LLM-driven optimizers as motivation, which is fine as motivation only.
2. **Stale meeting-pack items superseded by night 2** (pack last refreshed 23 Nov 08:00, before night 2). Do not copy from:
   - 03 S1 table, the one-pager and Q&A M7: "setup-cached ≈ 1.5–2×, not measured; E5 runs tonight". **E5 is measured: 3.54×, cached ≈ 2.2–2.3×.**
   - 03 S7 and the one-pager: "directory A/A and rotation start tonight"; "the faster flips point to a clone or layout bias". **Done: identical code gives 2.4 %, the swap gives 1.8 % with no sign reversal, cause unresolved.**
   - 03 S8: "still open: E5, the directory A/A". Both are closed.
   - Agenda slot 14–18 "the open directory confound": reword to "an ≈ 2 % off-target false-verdict rate, cause unresolved".
3. **Overclaiming B1 and detection.** Say "many" (8/14, CI 33–79 %), **never "most"**, and always "on networkx, one project, S0 profiles". "FULL detects 1 of 10" is a detection count, **not** a miss rate for reduced selection and **not** a safety result: the pre-registered primary result is "regression safety not measurable". Do not say any reduced selection is "safe". Do not say "first" or "novel": Traini et al. 2021 already profile benchmark reach per commit; what is ours is the measured uncovered-edit rate for optimization commits.
4. **Cost as point values or as an order of magnitude.** R1 is a range over 9 mostly noisy passes (8/9 noisy) with an unexplained 2.45× drift within one evening. With setup cached, benchmarks are only ≈ 2.2–2.3× build + tests, measured on a fast night. So "benchmarks dominate by an order of magnitude" is **true only for the suite as written**. Say "≈ 8–14× as written, ≈ 2.2–2.3× with setup reused; still the largest part". Also do not show testmon's 15× (test-seconds); it is 3.5–4× end to end.
5. **Off-target verdicts and #8 shown as findings.** The ≈ 2 % false-verdict rate means a single A/B verdict of ≤ ≈ 1.4× is not evidence. #8 (1.12–1.20×), #1, NonNeighbors and the #9 completeness flag must not appear as detections or as safety violations. Only #2 (1.76–1.90×) is a detection. Do not present the 2.2 % as "11× the nominal rate" without the caveat that the test's nominal α assumes independent samples, which these are not.

Also check before presenting: the PDF's `threats.tex` "Every A/B comparison…" sentence and the "3.54× of a standard pass" phrase (§2, D8 and D10) if the PDF is shown on screen.
