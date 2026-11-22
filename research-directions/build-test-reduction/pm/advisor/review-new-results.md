# Advisor-persona review of the new Study 1 results (A/A, profile completeness, Q3, edit sets, machine drift)

Reviewed 2026-11-22, after the 12:59 PKT update of `results.md` and `findings.md`. Reviewer: advisor-persona subagent (AI-SIM: a model of the advisor, not the advisor). Follows [persona.md](persona.md) and the hit-list after [review-final-results.md](review-final-results.md).

Read:
- `03-experiment/results/results.md`: the A/A section (L543–602), the profile-completeness check and the #9 re-check (L449–502), Q3 (L293–353), "networkx edit sets — reconciliation" (L258–291), the RQ1 headline and machine-state note (L21–69), idle re-timing (L138–162), the slowdown-oracle tie to B1 (L519–531);
- `knowledge-base/findings.md` rows B1, B3, N6, N7, P3, P4, P5;
- the pack: `meeting-2026-11-advisor/` (all five files; timestamps 07:54, README 09:58);
- spot checks against raw files: `q3/q3_b1_static.json`, `q3/q3_b1_static.first_count.json`, `frozen/networkx.aa_noise_sample_cut23.json`, `harness/bth/benchrun.py` (processes run one after another), `03-experiment/readiness.md` §4.2 (L166).

Nothing was run.

## Bottom line

- **The PM's summary is mostly right. Four points in it overstate the files:**
  - **"Machine speed drifts 10×."** The files show something narrower. Only the *per-process setup of `benchmark_algorithms`* drifts. The cheap cases ran at 0.74–1.14× of expected (L596), the timed samples did not move (≈ 0.96×, L49), and tests stayed at 71–89 s. The "≈ 10×" also compares runs with 2 processes against runs with 5 (L598–601). Within one protocol the changes are ≈ 3× and ≈ 1.7×.
  - **"B1 did not replicate."** Not so: B1 was **not validly tested**. That is not the same as failing to replicate, and the pack must not say either "replicated" or "did not replicate".
  - **"The regex matched 'coefficient': 3 of 18 are not optimizations."** Only one of the three (`bf130bfe`) matched through "coefficient". `519e819f` matched through `fast_`/`faster_` names, and `9f6079c0` is a bug fix (L314).
  - **"Only ≈ 2× is reliably detectable on the algorithm benchmarks."** This rests on 2 of 3 sampled cases out of 49, from an optimistic bootstrap (L590). L500 states it too broadly.
- **What changes in the story:** the networkx "oracle gap" now has **two legs**:
  - *coverage*: B1, 9 of 15 true optimizations unreached;
  - *power*: the A/A noise means moderate slowdowns in the heavy module may be invisible even when they are reached.

  That makes the networkx finding stronger and more honest. It still rests on **one project**.
- **A13's condition (B1 replicates) is unmet, and it is unmet because the test was weak, not because the evidence went against B1.**
  - Q3 did produce something useful: measuring B1 across projects is harder than it looked (mining precision, old-base bias, template code).
  - Bottleneck also gave a counter-signal: its suite benchmarks functions by name.
- **A gap nobody has named:** the pre-registered regression rule includes **ratio > 1 + 3·σ_noise(b)** (readiness §4.2, L166). Now that an A/A run exists, that condition is still applied nowhere in `results.md`, and σ exists for only 23 of 171 cases.
- **Can the pack go ahead? Yes, after a text-only refresh.** Every pack file is from 07:54 or 09:58. All of them still say "no A/A yet", "Q3 in progress", "completeness check 3 of 5" and "12 of 18". No new run is needed before the meeting.

## (a) What changes in the story and in the asks

| Item | Before (pack, 07:54) | After (files, 12:59) | Consequence |
|---|---|---|---|
| **R1** cost | 659–2444 s per pass, 8–28× build + tests | Direction holds. The dominant component, `benchmark_algorithms` per-process setup, varies with machine state (≈ 4.4 → ≈ 40 s per process). The 659–751 s passes came from the fastest state seen. Tests and timing loops are stable. | Lead R1 with the **stable parts**: timing loops 132–171 s and tests 71–89 s. Then add "+ setup: large, volatile, cacheable". The 730 s median is a best case, not a typical case. |
| **R4** cost noise | "Windows host load is the likely cause" | N7: the A/A overrun happened at WSL load ≤ 1.06 with the Windows gate at 9%, so load does not explain it. Cause unknown. Candidates (not checked): memory pressure (Windows had 2.5 of 15.8 GB free), boost state, page cache. | Drop "host load is the likely cause". Say "cause unknown; it affects one module's setup". |
| **B1** | 12/18, "most", replication in progress | **9/15 true optimizations, 60% [36–80%]** by measured profile; 4/15 by static reach. Single project. | "Most" is a point estimate, because the CI includes 36%. Say "about 60% (9 of 15)". |
| **S1/S2** slowdowns | 7 of 10 unreached; the suite is "the binding limit" | 6 of the 9 slowdowns in true-optimization functions are unreached (#6 sits in step 8). #3 and #4 are reached but missed, and the A/A says that miss may be **power**, not coverage (L592). | The limit is "coverage **and** oracle power", not coverage alone. |
| **P5** completeness | 0 slower in 30 (partial) | **1 slower in 50.** The pre-registered C11 flag for #9 stands. The post-hoc re-check (partial, 5 of 6 runs) did not confirm it. | Report the flag as the primary result and the re-check as context. Neither direction is proven. |
| **N6** noise floor | "none yet; every verdict provisional" | 0/46 false verdicts (Wilson upper bound 7.7%, optimistic), but close to the threshold. Power is 0.91 at 1.2× overall, and low on 2 of the 3 sampled `benchmark_algorithms` cases. | The TPM go/no-go ("no W3 number without the A/A floor") is now formally met **for the 23 sampled cases**. The 1 + 3σ condition is still unapplied. |

**Ask A13 (`01-agenda-and-asks.md` L30): rewrite it. Do not drop it.** Proposed text:

> **A13.** Should Study 1 pivot toward the benchmark oracle gap for optimization edits? On networkx, 9 of 15 true optimizations are executed by no benchmark (measured profile; 60%, CI 36–80%). FULL detects at most 3 of 9 relevant slowdowns. Where slowdowns are reached, the A/A power suggests moderate ones in the heavy module can still be missed. **The replication condition is not met.** Q3 was inconclusive by design: static reach from one old base is biased (geopandas), pvlib's base has no asv suite and its mined edits are mostly not optimizations, and bottleneck gives 4/8 as frozen or 0/8 under the template reading, because its suite benchmarks functions by name. **Proposed:** (i) keep the original RQs for the Study 1 write-up, with B1 as a single-project finding; (ii) make a pre-registered B1 replication the first post-meeting step, with measured profiles at each edit's parent, a stricter mining rule fixed before mining and a diff-based check of each edit; (iii) decide on the pivot after (ii). Options: as proposed; pivot now on networkx evidence; drop the pivot.

Also:
- **A3 (definition of "stays optimized"):** add one line. The pre-registered 1 + 3σ_noise condition has not been applied, and σ exists for 23 of 171 cases. Either apply it to the cases that have σ and log a deviation for the rest, or ask the advisor whether the asv rule alone is acceptable.
- **A12 (compute):** N7 is now a concrete reason to ask for a lab machine. A one-module setup cost that moves 5–10× with unknown machine state makes every per-pass cost a range.
- **A5 / P25 (contribution):** the answer moves from "cost characterization + B1, pending generalisation" to the following. The cost characterization holds in direction. The networkx oracle gap now has coverage and power legs. **Generalisation is untested.** The Q3 attempt is the reason the replication protocol needs measured profiles.

## (b) The five most likely meeting questions on these results

1. **"You said you would pivot if B1 replicated. Did it?"**
   - Honest answer: **it was not validly tested.** On networkx, B1 holds on true optimizations: 9/15 by measured profile, CI 36–80%.
   - geopandas: 18/20 by static reach, but from a 2017 base. Functions added later are unreached by construction. The post-hoc name heuristic gives 7/20, and it is not a bound in either direction.
   - pvlib: invalid. Its 2014 base has no asv suite, and only about 4 of its 14 mined edits are optimizations.
   - bottleneck: 4/8 as frozen, or 0/8 if the template edits count as reaching the named nan-functions. Its suite enumerates functions by name, which suggests B1 depends on how a suite is designed.
   - What a valid test needs: measured profiles at each parent and a mining rule fixed before mining. It needs counts only, no timing (L347–349).
2. **"Your regex matched 'coefficient'. How do you know the remaining 15 are optimizations? Did anyone read the diffs?"**
   - Honest answer: by **subject only**, post hoc, by one reader. The diffs were not classified, and there was no second rater.
   - The 3 exclusions came in by three different routes: one by "coefficient", one by `fast_`/`faster_` names (MAINT) and one bug fix.
   - The 2 edits dropped on apply conflicts were optimizations.
   - The functional conclusions survive the exclusion: A3 misses 1/18, every other arm 0/18.
   - The A4 point gets worse: 2 of A4's 5 full checks fired on non-optimization edits.
3. **"What is your noise floor, and can your oracle see the slowdowns that matter?"**
   - Honest answer: 0 false verdicts in 46 A/A comparisons (upper bound 7.7%). This is optimistic, because it is the same 23 cases twice.
   - The noise sits close to the threshold: two cases had p < 0.002 and were stopped only by the ratio condition, and a ratio of 1.77 still read "same".
   - Power from measured noise is 0.91 at 1.2× overall. For 2 of the 3 sampled `benchmark_algorithms` cases, only about 2× is reliable, and that comes from 3 of the module's 49 cases.
   - So #3 and #4 may be power misses.
   - The pre-registered 1 + 3σ condition is not applied yet. #8 (1.116×) and #9 (1.13×) are the verdicts it could affect.
4. **"#9 flags reach-based selection as unsafe. Is it unsafe or not?"**
   - Honest answer: **the pre-registered flag stands, and we cannot say which way it falls.**
   - `DiGMState.__init__` is in neither the profile reach nor the static reach of the louvain case. The original verdict sat just past both thresholds (1.13×, p = 0.0019).
   - The post-hoc re-check read "same" on every comparison, with the slowed clone level with both bases. But it was cut at 5 of 6 runs, and only slow-vs-base2 is order-balanced.
   - Under 50 null comparisons the chance of at least one false "slower" is about 5%. So noise is plausible, but this is a 1-in-20 event, not a certainty.
   - The check covers only the 5 slowdowns that no benchmark reaches. It is a profile-completeness check, not a safety rate.
5. **"Your benchmark cost moves 5–10× during the day. Why should I believe R1?"**
   - Honest answer: **the direction yes, the magnitude no.**
   - The drift is confined to one module's per-process setup. Timing loops (132–171 s per pass), the timed samples and the tests (71–89 s) are stable.
   - Even the fastest pass (659 s) is about 7.5× build plus tests, and the cached-setup estimate is about 1.5–2×.
   - The "≈ 10×" crosses protocols (2 against 5 processes) and assumes cost is linear in processes. Within one protocol the changes are about 3× and about 1.7×.
   - The cause is unknown, and no setting was changed. This is the case for a lab machine (A12).

(P25, "so what is the contribution", stays likely; see (a).)

## (c) What to drop, soften or add in the meeting pack

| Action | Where | Change |
|---|---|---|
| **Drop** | `03-results-summary.md` L5, L11, S7 (L140–146); `00-one-page…` L44; Q&A Q4 (L36–38); P20 status (L166) | "No benchmark A/A noise floor exists yet" and "A/A running". Replace them with the N6 numbers. |
| **Drop** | `03` L21, L49; `00` L40; Q&A Q1 (L24–26); A13 L30; README L7 | "B1 replication in progress (W3 Q3)". Replace it with the Q3 outcome (one short table: as frozen, and why it is not established). |
| **Drop** | `03` S2 L65–67 | "PARTIAL: 3 of 5 … 0 slower in 30 … #9 not started". Replace it with "5 of 5: 1 slower in 50; C11 flags #9; post-hoc re-check (partial) did not confirm it". |
| **Drop** | `00` L39, story step 1 (`03` L20) | "88–94% … mostly import-time setup" as a setup share. 88–94% is the `benchmark_algorithms` share including its loops; README L9 already notes this. |
| **Soften** | `03` S2 heading, story step 2, `00` L40 | "The suite cannot see most optimizations" becomes "On networkx, the suite executes none of the changed functions for 9 of 15 true optimizations (60%, CI 36–80%)". Use "12/18" only as the replayed-sequence figure. |
| **Soften** | `03` L62, `00` L40 | "The suite, not the selection rule, limits regression detection" becomes "coverage and oracle power, not the selection rule". |
| **Soften** | `03` L38 (R4) | Remove "Windows host load is the likely cause"; use "cause unknown" (N7). |
| **Soften** | `03` S1 table; `00` L39 | Give R1 as stable loops plus tests, with setup as volatile. Present 659–751 s as the fastest machine state observed. |
| **Add** | `03` S7 | A/A: 0/46, upper bound 7.7% (optimistic); close to the threshold; the power table; 3 of 49 heavy cases sampled; the 1 + 3σ condition not yet applied. |
| **Add** | `03` S1 or S7 | N7 drift, stated narrowly: one module's per-process setup, about 1.7× and about 3× within protocols, about 10× across protocols; samples and tests stable; cause unknown. |
| **Add** | `03` S2 | Mining precision: 15 of 18 replayed edits are optimizations by subject (post hoc, one reader, not diff-checked). Name the three routes correctly. |
| **Add** | Q&A | Update Q1 (P23) to "not validly tested". New entries for questions 2 and 4 above. Update Q4/P20 with N6. |
| **Add** | `01` A3, A12 | The lines given in (a). |
| **Sync** | `knowledge-base/findings.md` (owner: PM) | Row B1 (L9) still says "Most … 12 of 18". P3 still lists the C5 comparators as pending, as flagged at 08:00. P5 says "most likely reflects noise", which is stronger than results.md L498 ("does not prove it"). N7 says "at low load", but item 4 and #1 ran above 1.5. |

## (d) Claims in `results.md` that are wrong or overstated

| Line | Claim | Problem | Fix |
|---|---|---|---|
| **L26** | "88–94 % of a pass is import-time setup" | **Wrong as stated.** 88–94% is the `benchmark_algorithms` share including its loops (L41, L79). Non-loop time is ≈ 90% of the 1668 s pass ((1668 − 171)/1668) and ≈ 80% of the 708 s pass (taking ≈ 140 s of loops). | "88–94% is the `benchmark_algorithms` share; ≈ 80–90% of a pass is outside the timing loops." |
| **L43** | "per-process setup slowed ≈ 1.6× after a PC restart" | Misleading as a headline. L597–601 show the larger change, ≈ 4.4 → ≈ 23 s per process, came **before** the restart (overnight → morning). The restart adds ≈ 1.7× more. | Restate it as day-long drift; the restart is one step in it. |
| **L602** | "the cost varies about 10×" | It mixes 2-process and 5-process runs and assumes cost is linear in processes. Within one protocol the changes are ≈ 3× (load 1.63) and ≈ 1.7×. L70/L74 blame the 65–71 s import at 19:18 on concurrent load, which N7 now makes doubtful. | Give within-protocol figures first; label the 10× as cross-protocol. |
| **L209, L211, L213** | "most replayed optimizations…", "B1 holds", "most of these commits" | 9/15 with CI 36–80% does not establish a majority. Static reach gives 4/15. | "About 60% (9/15, CI 36–80%) by measured profile." |
| **L520–522** | "7 of 10 … matches B1, where 12 of 18" | Stale after the reconciliation. On true optimizations it is 6 of 9 slowdowns and 9 of 15 edits. | Update both figures. |
| **L522, L531** | the suite is "what limits regression detection", "the binding limit … (B1)" | L592 now says #3/#4 may be power misses. | "coverage and power". |
| **L500** | "for the `benchmark_algorithms` cases, only ≈ 2× slowdowns are reliably detectable" | Generalises from 2 of 3 sampled cases (of 49), using an optimistic bootstrap. L590 is the careful version. | Use the L590 wording. |
| **L19, L476** | "post-hoc ABBA re-check"; "flag stands until the ABBA re-measurement is run" | It is not ABBA: base is missing in repeat 1, so only slow vs base2 is balanced (L485). The "until" sentence is stale, since the re-check ran and the flag stands anyway. | "Post-hoc partial re-check (5 of 6 runs)"; delete "until…". |
| **L299** | "`q3/q3_b1_static.json` (as-frozen counts…)" | **Wrong file label, checked.** That file holds bottleneck **0/8** (the post-hoc template rule). The as-frozen **4/8** is in `q3_b1_static.first_count.json`. | Swap the labels, or name the file that holds the as-frozen bottleneck count. |
| **Not stated (readiness L166)** | Regression verdicts use the asv rule only | The pre-registered **1 + 3·σ_noise(b)** condition is not applied or reported anywhere, and σ exists for only 23 cases. It could matter for #8 (1.116×), #9 (1.13×) and #1 (1.245×). | Apply it where σ exists, or log a deviation. |
| **L550 vs L67** | A/A run in the slow morning state, read against overnight verdicts | Not wrong, but unstated: the floor was measured in a different machine state from #1, #2 and #8, and L67 says variance is not shielded. | One caveat line. |
| L3, L7 | Status "PRELIMINARY, 2026-11-21 20:00" | Stale header. | Bump it. |

## Hit-list updates (proposed; `persona.md` not edited)

| ID | Status after these results |
|---|---|
| P20 (repeatability) | partial: A/A on 23 cases; verdict repeatability on #9 only, and partial |
| P23 (is B1 networkx-specific?) | still open: Q3 inconclusive; answer "not validly tested" |
| P25 (contribution) | open; the answer changes as in (a) |
| **P26 (new)** | "Did you read the diffs? How many mined edits are really optimizations?" (High) |
| **P27 (new)** | "Is reach-based selection unsafe or not, given #9?" (Medium) |
| **P28 (new)** | "Your cost moves 10× in a day: which number is R1?" (Medium–High) |
| **P29 (new)** | "You pre-registered 1 + 3σ_noise. Where is it applied?" (Medium; only if the advisor reads readiness §4.2) |
