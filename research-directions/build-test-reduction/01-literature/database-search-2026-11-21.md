# ACM DL and IEEE Xplore searches (2026-11-21)

**Status:** run 2026-11-21 in the student's own Chrome (Claude in Chrome extension), with the student's authorisation. This closes the "ACM DL and IEEE Xplore" gap in `gap-and-search-log.md` (v3.1 section). That file is not edited here.

**How the searches were run**
- I typed each query into the site's own search box, as a user would, and read only result pages and abstract pages.
- I did not sign in or download anything, and I called no internal API.
- ACM DL showed a "Performing security verification" interstitial, which cleared by itself after about 6 s. No CAPTCHA was solved. I declined non-essential cookies ("Use necessary cookies only") and closed the open-access notice. IEEE Xplore showed no cookie banner that needed an answer.
- **ACM DL** searches the ACM Full-Text Collection (865,616 records), Basic edition. `AllField` matches full text, so broad queries also return whole proceedings volumes (front-matter records). The sort was the site default, which looks like relevance (results were not in date order).
- **IEEE Xplore** searches metadata (title, abstract, index terms), sorted by relevance. Its parser is strict: free words outside quotes are ANDed. So the exact strings from the log returned 0 hits. To give IEEE a fair test, I added adapted Boolean queries (marked "adapted").
- **Relevance calls:** irrelevant / adjacent / known (already in `references.bib` or the notes) / **threatens Cx**.

## Summary

| Site | Ran? | Queries | Hits returned (sum) | Titles screened |
|---|---|---|---|---|
| ACM DL | Ran. Interstitial cleared by itself; no CAPTCHA | 4 logged + 3 supplementary | 77 + 1 + 20 + 47 + 0 + 6 + 1 = 152 | 20 + 1 + 20 + 20 + 0 + 6 + 1 = 68 |
| IEEE Xplore | Ran. No block (the HTTP 418 seen earlier from the scripted fetch did not recur in a normal browser) | 5 exact (log string + 4 ACM strings) + 1 control + 7 adapted | exact: 0 each; adapted: 4 + 23 + 6 + 3 + 5 + 2 + 12 = 55 | 55 |

**Total screened: 123 records** (many ACM records are proceedings front matter, not papers).

**Result for the claims.** No record found here anticipates C1, C5, C8 or C11 as stated. One paper narrows **C7**: Chittimalli & Harrold, TSE 2009, which is not in the corpus (details below). Two more papers should be added to C5's "partial elsewhere" list: Elsner et al. ICSE-SEIP 2022 and Kauhanen et al. SANER 2021, whose venue is now confirmed.

---

## ACM Digital Library

### A1. `"regression test selection" accumulated changes full test run`
Date 2026-11-21. **77 results**; the first 20 screened.

| # | Title (venue, year) | Call |
|---|---|---|
| 1 | Hybrid Regression Test Selection by Integrating File and Method Dependences (ASE 2024) | adjacent (RTS granularity) |
| 2 | RTL Regression Test Selection Using Machine Learning (ASP-DAC 2022) | irrelevant (hardware) |
| 3 | A comparative study of coarse- and fine-grained safe RTS techniques (TOSEM 2001) | adjacent (classic RTS) |
| 4 | Neural-MCTS Test Prioritization for Smart Contract Mutation Testing (DLT 2026) | irrelevant |
| 5 | When Automated Program Repair Meets Regression Testing (TOSEM 2024) | adjacent (RTS inside a patch-generation loop) |
| 6 | Techniques for improving regression testing in CI (Elbaum, Rothermel, Penix, FSE 2014) | known; adjacent to C1 (time-window selection and prioritisation, no accumulated-change trigger) |
| 7 | Faster Feedback with AI? A Test Prioritization Study (Programming 2024) | irrelevant |
| 8 | Fuzz4DB: LLM-Agent-Guided Fuzzing for Database Feature-Level Delta Testing (ASE 2026) | adjacent (per-delta validation in a CI budget; fuzzing, not RTS) |
| 9 | The Importance of Accounting for Execution Failures when Predicting Test Flakiness (ASE 2024) | irrelevant |
| 10 | HybridCISave: A Combined Build and Test Selection Approach in CI (TOSEM 2023) | known; adjacent to C1 and C3 (ML-based build and test skipping) |
| 11 | Faster Explicit-Trace Monitoring-Oriented Programming for RV of Software Tests (OOPSLA 2025) | irrelevant |
| 12 | Prioritizing Regression Tests … Execution Frequency of Modified Code (PPPJ 2016) | irrelevant |
| 13 | Software Evolution Management with Differential Facts (ASE 2022, short) | irrelevant |
| 14 | A Systematic Literature Review on Design for Testability (CSUR 2026) | irrelevant |
| 15 | Practical selective regression testing with effective redundancy in interleaved tests (ICSE-SEIP 2018) | adjacent |
| 16 | APICIA: An API Change Impact Analyzer for Android Apps (ICSE-Companion 2024) | irrelevant |
| 17 | Fine-grained test minimization (ICSE 2018) | irrelevant |
| 18 | Don't Retest Everything: Auditable Regression Scoping for Safety-Critical Systems (ASE 2026) | adjacent (cross-boundary regression scoping; not accumulation-triggered) |
| 19 | EvoMe: software evolution management engine (ASE 2021) | irrelevant |
| 20 | SimRT: regression testing for data races (ICSE 2014) | irrelevant |

### A2. `"regression test selection" Python "C extension"`
Date 2026-11-21. **1 result**: the ESEC/FSE 2022 proceedings volume (front matter). Irrelevant; the terms match across separate papers in the volume. **No paper on RTS for Python C extensions.**

### A3. `"benchmark selection" "performance regression" Python`
Date 2026-11-21. **20 results**, all screened.
- Papers: (1) Tracing Optimization for Performance Modeling and Regression Detection (TOSEM 2026), adjacent to C11 (tracing, not benchmark dropping); (2) Evaluating Compiler Optimization Impacts on zkVM Performance (ASPLOS 2026), irrelevant.
- The other 18 are proceedings volumes (EASE '23, ESEC/FSE 2023, ASE '26, ICSE '26/'24/'23, SIGOPS ATC '26, ICPE '25, SC-W '25/'24, ICS '26, ISSTA 2024, ASPLOS '24/'23, UIST '25, CIKM '26, FAccT '26, FSE 2016). All irrelevant as records.
- **No Python benchmark-selection miss-rate study.**

### A4. `"test selection" stale dependencies multiple revisions`
Date 2026-11-21. **47 results**; the first 20 screened.
- Papers: (1) Comparing and combining test-suite reduction and RTS (Shi et al., ESEC/FSE 2015), adjacent; (2) ML for hardware design verification survey (TODAES 2024), irrelevant; (3) Neural-MCTS smart-contract prioritisation (DLT 2026), irrelevant.
- The other 17 are proceedings volumes (ASPLOS '25, SOSP '26, ASE '26, ICPE '25 Companion, ICSE-Companion '26, MODELS Companion '26, ICSE-SEIP '26, CIKM '26, ICSE '26, ICSE-NIER '23, MSR '24, JCDL '26, Internetware '25, SC-W '25, ICSE '23, ISSTA 2023, FSE 2024 Companion). All irrelevant as records.
- **No study of RTS safety against dependency-data staleness.**

### A5 (supplementary, C1). `"test selection" "batch testing" threshold "full test suite"`
Date 2026-11-21. **0 results.**

### A6 (supplementary, C1). `"batch testing" "test selection" "continuous integration"`
Date 2026-11-21. **6 results**, all screened.

| Title | Call |
|---|---|
| Accelerating Continuous Integration with Parallel Batch Testing (Fallahzadeh, Bavand, Rigby, ESEC/FSE 2023, 10.1145/3611643.3616255) | known (in `references.bib`); adjacent to C1 (batching, no per-edit reduced tier) |
| Predictive test selection (Machalica et al., ICSE-SEIP 2019) | known; adjacent (learned selection) |
| Bisecting commits and modeling commit risk during testing (Najafi, Rigby, Shang, ESEC/FSE 2019) | known; adjacent to C1 (risk-based batching and bisection) |
| A Survey of Flaky Tests (TOSEM 2021) | irrelevant |
| ESEC/FSE 2023 proceedings; ICSE '23 proceedings | irrelevant (volumes) |

### A7 (supplementary, C8). `"incremental build" Python "extension modules" Cython`
Date 2026-11-21. **1 result**: the ICSE '26 proceedings volume. Irrelevant. **No Python-extension incremental-rebuild study.**

---

## IEEE Xplore

### Exact strings (all run 2026-11-21, 0 results each)
| Query | Hits |
|---|---|
| `"regression test selection" accumulated changes` (the IEEE string from the log) | 0 |
| `"regression test selection" accumulated changes full test run` | 0 |
| `"regression test selection" Python "C extension"` | 0 |
| `"benchmark selection" "performance regression" Python` | 0 |
| `"test selection" stale dependencies multiple revisions` | 0 |
| Control: `regression test selection` (unquoted) | 6,704 (the search works; zeros come from the strict AND over metadata) |

### I1 (adapted, C1). `"test selection" AND batch*`
**4 results**, all screened:
- Modified code entity-based RTS for manual E2E testing (ISSREW 2019): adjacent.
- Accelerating Search-Based Program Repair (ICST 2018): adjacent.
- Neural networks for novelty-based test selection (AITest 2023): irrelevant.
- Automated maintenance of avionics software (NAECON 1993): irrelevant.

### I2 (adapted, C1/C5). `"regression test selection" AND "continuous integration"`
**23 results**, all screened.

| Title (venue, year) | Call |
|---|---|
| Regression Test Selection Tool for Python in CI Process (Kauhanen et al., SANER 2021) | known; adjacent to C5 (see notes below) |
| A RTS technique based on incremental dynamic analysis (CEE-SECR 2009) | adjacent |
| Understanding and Improving RTS in CI (Shi, Zhao, Marinov, ISSRE 2019) | known |
| Build System Aware Multi-language RTS in CI (Elsner et al., ICSE-SEIP 2022) | **adjacent to C5/C8: not in references.bib** (see notes) |
| A Study of RTS in CI Environments (Yu & Wang, ISSRE 2018) | known (ISSRE 2018 line) |
| Improving Data Quality for RTS by Reducing Annotation Noise (SEAA 2020) | irrelevant |
| Requirement-based RTS in BDD (COMPSAC 2021) | irrelevant |
| BinaryRTS: Cross-language RTS for C++ Binaries in CI (ICST 2023) | known; adjacent to C5 |
| Resurgence of RTS for C++ (Fu, Misailovic, Gligoric, ICST 2019) | adjacent to C5 (native-language RTS) |
| Regression Test Selection at Scale (Mehnaz et al., ICSME 2026, 10.1109/ICSME67971.2026.00114) | adjacent (call graph + ML ranking, fixed per-commit test budget; no full-check trigger) |
| Practical Pipeline-Aware Regression Test Optimization for CI (Schwendner et al., ICST 2025, 10.1109/ICST62969.2025.10989002) | adjacent to C1 (pre-/post-submit split, RL-based; tiers are fixed pipelines, not an accumulated-change trigger) |
| Perphecy: Performance Regression Test Selection (ICST 2017) | known; adjacent to C11 |
| Efficient Incremental Code Coverage Analysis for Regression Test Suites (ASE 2024) | adjacent to C7 (incremental coverage update) |
| Empirical Study of Regression Testing for Android Apps in CI (ESEM 2023) | irrelevant |
| Multi-Agent Change Impact Analysis and Test Optimization for AI-Enabled Systems (AITest 2026) | adjacent |
| Adaptive and Explainable TCP in CI: systematic review (IEEE Access 2026) | irrelevant |
| Shaping QA Coverage with Production Telemetry: Risk-Based Test Selection Under CI Budget (ICAISET 2026) | adjacent |
| Hybrid Software Testing Recommendation System (CSCWD 2025) | irrelevant |
| Assessing Transition-Based Test Selection Algorithms at Google (ICSE-SEIP 2019) | adjacent |
| Instrumentation-Driven Evolution-Aware Runtime Verification (ICSE 2025) | irrelevant |
| Practical Selective Regression Testing … Interleaved Tests (ICSE-SEIP 2018) | adjacent |
| Business Value Driven Regression Testing for Agile (AIxSE 2025) | irrelevant |
| Change-Based Test Selection in the Presence of Developer Tests (CSMR 2013) | adjacent |

### I3 (adapted, C5). `"regression test selection" AND (Python OR Cython OR native OR "cross-language")`
**6 results**, all screened:
- Kauhanen SANER 2021; BinaryRTS ICST 2023; Elsner ICSE-SEIP 2022 (all as above).
- DIRTS: Dependency Injection Aware RTS (ICST 2023): adjacent.
- ReTestDroid (COMPSAC 2018): irrelevant.
- Shaping QA Coverage (ICAISET 2026): adjacent.

### I4 (adapted, C7). `"test selection" AND (stale OR outdated OR obsolete) AND (dependenc* OR coverage)`
**3 results**, all screened:
- **Recomputing Coverage Information to Assist Regression Testing** (Chittimalli & Harrold, TSE 2009): **threatens C7 (partially)**; details below.
- Re-computing Coverage Information to Assist Regression Testing (same authors, ICSM 2007): the conference version of the TSE paper.
- Efficient Process Shift Detection and Test Realignment (TCAD 2013): irrelevant (hardware).

### I5 (adapted, C11). `"performance regression" AND benchmark* AND (selection OR "test selection")`
**5 results**, all screened:
- Perphecy (ICST 2017): known.
- On the Detection of Performance Regression Introducing Code Changes: Experience from the Git Project (STC 2022): adjacent to C11 (C project; no Python or benchmark-dropping miss rate).
- Ranking commercial machines through data transposition (IISWC 2011): irrelevant.
- GNN network localization (ICASSP 2021): irrelevant.
- Robust cross-view hashing (SPL 2016): irrelevant.

### I6 (adapted, C8). `"incremental build" AND (correctness OR stale OR Python OR extension)`
**2 results**, both irrelevant: a game-space exploration paper (CoG 2021) and a static-analysis scheduling paper (ASE 2006).

### I7 (adapted, C1). `("batch testing" OR "test batching" OR "batch size") AND ("regression test*" OR "continuous integration")`
**12 results**, all screened:
- **Software Batch Testing to Save Build Test Resources and to Reduce Feedback Time** (Beheshtian, Bavand, Rigby, TSE 2022): known (full text not obtained); adjacent to C1.
- **Mining Historical Test Failures to Dynamically Batch Tests to Save CI Resources** (Bavand & Rigby, ICSME 2021, 10.1109/ICSME52107.2021.00026): known; adjacent to C1 (see notes).
- TCP-Net (ICSTW 2022) and the TCP replication study (IEEE Access 2025): irrelevant.
- The other 8 (fake news, stock forecasting, SageMaker and DevOps books, DeepHealth, a crypto forecasting paper): irrelevant.

---

## Papers that bear on the claims

### Threatens C7 (partial): Chittimalli & Harrold 2009
- **Authors:** Pavan Kumar Chittimalli, Mary Jean Harrold.
- **Title:** "Recomputing Coverage Information to Assist Regression Testing".
- **Venue:** IEEE Transactions on Software Engineering 35(4), pp. 452–469, 2009. DOI **10.1109/TSE.2009.4**.
- **Conference version:** ICSM 2007, "Re-computing Coverage Information to Assist Regression Testing".
- **What the abstract says (paraphrase):**
  - The paper presents RECOVER. It reuses an RTS algorithm to produce accurate, updated coverage for version P(i+1) without rerunning tests that do not reach the changes.
  - It argues against two alternatives: estimating coverage, and reusing outdated coverage from P(i).
  - Its empirical studies on industrial subjects show the inaccuracies that arise when RTS uses estimated or outdated coverage data.
- **Effect on C7:** C7 currently says no study measures RTS safety as a function of dependency-data staleness. This paper shows empirically that stale coverage makes RTS inaccurate, and it offers a recompute technique. As far as the abstract shows, it covers one version step (P(i) to P(i+1)). It does not measure misses as staleness grows over a chain of k edits.
- **Recommended C7 wording:** "Chittimalli & Harrold (TSE 2009) show that outdated coverage makes RTS inaccurate and propose recomputation. We found no measurement of missed faults as a function of refresh interval over chains of dependent edits."
- **Next step:** C7 should move from "not found" to "partial". Read the full text, which needs institutional access.

### Adjacent, worth adding to C5's "partial elsewhere" list
- **Elsner, Wuersching, Schnappinger, Pretschner, Graber, Dammer, Reimer.** "Build System Aware Multi-language Regression Test Selection in Continuous Integration". ICSE-SEIP 2022. DOI 10.1145/3510457.3513078.
  - Industrial Java and C/C++ code base with non-code artifacts. RTS works at module level through the build system and compiles only affected modules.
  - Reports up to 75% of tests safely excluded, with no real failures escaping on 397 PRs.
  - Another native and cross-language analogue, like BinaryRTS. It is not Python and does not measure misses on extension edits. **C5 stands.**
  - It also bears on C8, since it selectively compiles modules, but it does not study whether incremental builds are correct.
- **Kauhanen, Nurminen, Mikkonen, Pashkovskiy.** "Regression Test Selection Tool for Python in Continuous Integration Process". SANER 2021. DOI 10.1109/SANER50967.2021.00077.
  - This fills the venue and year that `notes/T2-rts.md` A14 marks [unknown].
  - Coverage-based Python RTS (pytest-rts), evaluated by mutation against full-suite runs: missed-fault rate 0–2% at file level and 16–24% at line level.
  - It is a precedent for measuring misses of Python RTS, but on pure-Python mutants. It says nothing about C/Cython edits. **C5 stands**, and this is a method precedent for W3.

### Adjacent to C1 (no change to the narrowed claim)
- **Bavand & Rigby, ICSME 2021** (10.1109/ICSME52107.2021.00026). Batch size adapts dynamically to the project's weighted historical failure rate. It says all prior batching used a constant batch size.
  - This is a model-free adaptive batching rule, but it is driven by failure history, not accumulated change size.
  - It has no per-edit reduced check underneath. Batching replaces per-change testing rather than sitting on top of selection.
  - Cite it next to Sayedsalehi 2026 as the other non-fixed-k batching precedent.
- **Schwendner et al., ICST 2025.** A two-tier pre-/post-submit split with RL prioritisation. The tiers are fixed pipelines, and there is no trigger from accumulated change.
- **Mehnaz et al., ICSME 2026.** A fixed per-commit budget of selected tests with an ML ranker, and no periodic full check.

## Claims after this search
- **C1 (narrowed):** unchanged. Add Bavand & Rigby 2021 as a second adaptive-batching precedent alongside Sayedsalehi 2026. No record evaluates a deterministic accumulated-change trigger on top of per-edit reduced checks against fixed-k at matched cost.
- **C5:** unchanged ("not found" for Python). Add Elsner ICSE-SEIP 2022 (and Fu et al. ICST 2019) as native analogues, and Kauhanen SANER 2021 as a Python method precedent.
- **C7:** **downgrade to partial.** Cite Chittimalli & Harrold TSE 2009 and narrow the wording to the chain-of-edits refresh-interval measurement.
- **C8:** unchanged ("not found"). Both databases returned nothing on Python extension incremental-rebuild correctness.
- **C11:** unchanged ("partial"). Nothing new beyond Perphecy and an adjacent Git-project study.
- **C6, C3, C2:** not specifically searched here; no counter-evidence seen in the screened titles.

**Limits**
- Abstracts only, with no full texts. ACM was Basic edition (no filters). ACM full-text matching inflates counts with proceedings records.
- IEEE's strict parser meant the exact strings returned zero, so the adapted queries carry the IEEE evidence.
- This is still not a systematic review.
