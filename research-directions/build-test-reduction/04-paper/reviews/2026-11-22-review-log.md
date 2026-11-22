# Review log: first full draft (2026-11-22)

Two passes were run on the full draft. Both were fresh subagents that saw only the paper (plus the standards text for pass 2).
- **Pass 1: hostile reviewer** (`.claude/agents/hostile-reviewer.md`, template 4.2, read-only). Recommendation: **weak reject**. "The measurement idea is sound and the reporting is unusually honest", but the headline rests on one project, one base-state profile, unfloored verdicts and three A/A cases.
- **Pass 2: Empirical Standards** (General, Benchmarking, Repository Mining, Engineering Research; text fetched 2026-11-22). No Essential attribute is blocking. Many are PARTLY met. One was NOT MET: the risks/ethics statement, now fixed.

## Dispositions

| # | Finding (source) | Severity | Disposition |
|---|---|---|---|
| 1 | General thesis on one project and 14 edits (P1) | critical | **Fixed in text.** The title is now "A Case Study on networkx". The abstract says "In this case study". Restating the thesis stays a TODO on E1. |
| 2 | Reach measured at S0: functions absent at S0, or benchmarks added later, could inflate the unreached count (P1) | critical | **Disclosed + TODO for W3.** §RQ2 has a new paragraph, "Reach at the base state", with a TODO: per-edit existence at S0, parent-suite reach, date span, recompute at parents. **Needs W3; no timing needed.** |
| 3 | #1 and #8 handled asymmetrically; no verdict passed 1 + 3σ (P1) | critical | **Fixed in text.** One explicit decision rule (on target = the flagged case executes the slowed function). #8 is called weak, inside the noise band. Abstract and F3 now say "flags … under asv's rule; no verdict has yet passed the floor". TODO E2/E3. |
| 4 | "Only about twofold" rests on 3 cases (P1) | major | **Softened** to "a bootstrap on three cases suggests high detection probability only for large slowdowns". TODO E2 for ≥ 10 cases plus intervals. |
| 5 | #3 is dilution, not power (P1) | major | **Fixed.** Reworded, plus a TODO for W3: time share of the slowed function per reaching case. |
| 6 | RQ1 is a suite-design property; E5 and E6 are unmeasured (P1) | major | Already TODOs (E5, E6). **Added:** the six passes are single passes at different states, not repeats. |
| 7 | Runner not validated against asv; n per side not stated; hardware TODO (P1, P2) | major | **Partly fixed.** The verdict protocol per side is now stated. Hardware is still a TODO. Runner-vs-asv validation is **open (W3)**. |
| 8 | Same-model LLM raters; adjudicator; recall (P1, P2) | major | Threat already stated. **Added** TODO: model/version, adjudicator identity, prompts in the artifact. The human second rater is still a TODO on E1. **Open: owner.** |
| 9 | testmon vs FULL measured under different load; "misses none" by construction (P1) | major | **Fixed in text.** "Under mixed load" and the by-construction caveat are in F4 and the abstract. The table caption says estimated and measured seconds are not comparable. Back-to-back re-timing is **open (W3, needs a timing window)**. |
| 10 | Uncited related work (P1) | major | **Fixed.** Now cites Leitner & Bezemer, Stefan et al., Laaber & Leitner, µOpTime, worded to W1's evidence level. TODO for W1: full read of Laaber & Leitner MSR'18, plus three [verify] candidates (Traini; Chen & Shang; Jangali). |
| 11 | Pre-registration not checkable (P1, P2) | major | **TODO added** in §3: cite the frozen-protocol commit hash and date (or an OSF/Zenodo snapshot). **Owner/PM decision.** |
| 12 | Headline macros "quoted", not computed (P1) | major | **Open.** 70 of 193 macros are still "quoted" (123 computed) (R1 shares, drift, testmon ratios, worked edit). W3 could add machine-readable summaries so `make_all.py` can compute them. |
| 13 | Build-share 1.2/820 vs 730 median (P1) | minor | No change: 820 s = median pass (730 s) + build + tests, so the text "of a full validation at the median pass" is correct. |
| 14 | E3 TODO said "reached" for #1/#4 (P1) | minor | **Fixed:** "at least one case in profile or static reach". |
| 15 | bottleneck "probably reached by name" (P1) | minor | **Fixed:** labelled as conjecture. |
| 16 | Changed-function extraction unspecified (P1, P2) | minor | **Fixed:** unit of analysis and extraction rule are in §3 (from `03-experiment/rules.md` §1). A TODO asks for a hand-checked sample. |
| 17 | κ is 3-category, but the text implied binary (P2) | minor | **Fixed.** |
| 18 | Internal codes (B1, Q3, E3) in body text; strength bands undefined (P2) | minor | **Fixed.** Bands are defined in §3 (macros `BandModLo/Hi`). Codes remain only inside TODOs. |
| 19 | No ethics/risk sentence (P2, NOT MET) | minor | **Fixed** (§3, Platform). |
| 20 | Methodology not named; why mining; why networkx; why 20 (P2) | minor | **Fixed** (§3 opening, Subjects, Mining). |
| 21 | Test assumptions not stated (P2) | minor | **Fixed** (§3 Oracles, "Test assumptions"). |
| 22 | A4 score formula and target fault class (P2) | minor | **Fixed** in App. A (threshold as a macro, penalties in words) and §3. |
| 23 | Table omits A1/A5 (P2) | minor | **Fixed** in the caption. |
| 24 | `OffTargetComparisons` provenance: 843 + 50 = 893, but results.md says "about 890" (P2) | minor | **Kept "about"**, as in results.md. Flag to W3 to state 893 or explain. |
| 25 | `fig_precision.pdf` not referenced (P2) | minor | **Open.** Unused. Either reference it in §Lessons or drop it. |
| 26 | Figure axis ranges unchecked (P2) | minor | Checked by rendering fig_cost and fig_coverage (linear axes from 0). fig_power and fig_slowdowns are not inspected yet. |

## Still open after this pass (for PM routing)
- **W3 (no timing):** #2 per-edit reach at parents; #5 time share per reaching case; #24 the 890/893 wording; #12 machine-readable summaries for the quoted macros.
- **W3 (timing window):** E2, E3, E5, E6, bottleneck R1, testmon vs FULL back to back; validate the runner against asv.
- **W1:** #10 reads and searches; the B1/C11 novelty-search wording for §2 "Positioning".
- **Owner:** human second rater; pre-registration snapshot; LaTeX toolchain; venue and AI-use disclosure.
