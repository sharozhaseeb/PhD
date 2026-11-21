# Critic report: citation check of W1-LIT draft v1

**Date:** 2026-11-21. **Critic:** an independent agent that did not write the review.
**Method:**
- Ran `pdftotext -layout` on all 69 local PDFs and grepped each cited number or quote. Where a column split was ambiguous, checked again with `-raw`.
- Checked bib metadata against PDF first pages. For the 4 keys with no PDF, used WebSearch/WebFetch on abstract pages.
- Ran a script over every `.md` file to find citation keys missing from `references.bib`.
- Ran 7 novelty searches of my own (WebSearch, standard mode, 2026-11-21).
- Edited no existing file.

**Not done:**
- [F] claims for documentation (pyperf, asv, testmon, Bazel, ccache, setuptools/Cython source): only sampled, not re-fetched.
- `notes/T*.md`: not audited line by line. They were used only to locate passages.

## 1. Summary counts

| Verdict | Count |
|---|---|
| Claims checked (numbers, quotes, [R] locations, bib entries, key resolution) | **96** |
| OK (number or passage found at roughly the stated location) | **71** |
| WRONG (number, formula or fact contradicts the source) | **2** |
| UNSUPPORTED / overstated (source does not support the generalisation) | **4** |
| MISLABELLED (right fact, wrong section or label, or presented misleadingly) | **8** |
| METADATA (bib entry wrong, incomplete or duplicated) | **7** |
| UNVERIFIABLE locally (labelled [R], but no local PDF) | **4** |

Overall, the numeric claims are accurate. I found no invented paper and no fabricated number. The problems fall into four groups:
- (a) two over-strong "Python is under-served" statements;
- (b) one cost formula in a candidate rule;
- (c) Daly et al. cited for a design that Daly et al. abandoned;
- (d) bib hygiene, plus one closely related 2026 paper missing from the closest-works list.

## 2. Findings (non-OK)

| ID | File:line | Claim | Citation | Verdict | Evidence (what the source says) | Suggested fix |
|---|---|---|---|---|---|---|
| F1 | review.md:83, review.md:220 (also README "Python under-served" framing) | "NameRTS … is the only peer-level Python RTS study found"; "Python RTS research is a single 2026 preprint" | WangPradelLiu2026 | **UNSUPPORTED** | NameRTS itself calls BabelRTS "the state-of-the-art Python RTS approach" (PDF l.143) and BabelRTS's TSE 2025 paper (`MaurinaCazzolaGhosh2025`) is in our own bib and cited at review.md:92. NameRTS also compares against coverage-based RTS [31] and speaks of "existing Python RTS approaches" (conclusion). `KauhanenPytestRTS` (pytest-rts paper) is also in the bib. | Say "NameRTS is the only *Python-specific, fine-grained* RTS study found. Python is otherwise covered only by the polyglot BabelRTS (TSE 2025, file level) and tool papers (pytest-rts)." |
| F2 | candidate-rules.md:64 (C1) | Najafi cost "about 1 + P(window fails)·(2·log2 k + 1) runs per window" | najafi2019bisecting Eq. 1 | **WRONG** | Eq. 1 (p.2, Fig. 1 caption): 2·log2(n)+1 *already includes* the initial batch execution ("Since we must determine if the starting batch passes, we need an additional execution"). The formula therefore counts the batch run twice. | Use 1 + P·2·log2 k (equivalently (1−P)·1 + P·(2·log2 k + 1)), plus the Eq. 7 flake term. |
| F3 | candidate-rules.md:55 (P5); closest-works.md:104 (#13); assumptions…md:27 (B3) | Daly cited as basis for comparing with the original or stable baseline; #13 "Compares results with the previous run, a run a week earlier and the last stable release; uses change-point detection" | daly2020changepoint §1 | **MISLABELLED** (misleading) | §1–2: the three-way comparison was MongoDB's *earlier* threshold system. It produced "a large number of false positives … up to 99%" and was *replaced* by E-Divisive change-point detection. The "drift down" failure mode (Fig. 1 caption) is listed as a weakness of that earlier system. | State that Daly abandoned the stable-release comparison because of false positives. P5 then needs a noise-aware threshold, which strengthens the case for P6. |
| F4 | assumptions…md:17 (A5); candidate-rules.md:43 (F6) | "NameRTS: global-code changes select all tests [R §4.2]" | WangPradelLiu2026 | **UNSUPPORTED** (overgeneralised) | §3.1 models global variables as SharedVariable nodes, "preventing unnecessary test selection caused by modifications to global variable definitions". The select-all case (§4.2, PDF l.993–999) covers only *side-effecting functions executed at import*: in matplotlib, 5 of 50 commits. The broad "global code forces re-execution of most tests" sentence (§1, l.102) is about *coverage-based* RTS, not NameRTS. | "Changes to functions run at import time (side-effecting global code) make NameRTS select all tests (5/50 matplotlib commits)." |
| F5 | closest-works.md (whole table); beyond-literature-claims.md:133, :138 (C1, C6) | Closest works to the RQ3 policy | — | **UNSUPPORTED** (omission) | `sayedsalehi2026riskaware` (Sayedsalehi, Rigby, Mierzwinski, arXiv 2604.00222, Mar 2026) is in the bib and in T3 notes A7. It does **risk-aware batch testing for performance-regression detection** at Mozilla (32.4% fewer executions, 26.2% lower time-to-culprit; abstract per T3). It is the closest batching-for-*performance* work, but it appears in neither closest-works nor C1/C6/C10. Its learned risk model makes it out of scope as a *method*, not as *prior art*. | Add it as row 17 (batching of performance tests; fixed or risk-driven batches; learned risk). Mention it in C1/C6 "partial". |
| F6 | review.md:220–222 (§6.2), README.md:122 | "Python benchmark selection has no peer-reviewed study" | G2, T3 #27/#36 | OK as worded, but see §3 | No contradiction found. The 2021 PeerJ CS call-graph relevance study (Grambow et al.) is Go, not Python. | Keep it as "not found in recorded searches". |
| F7 | review.md:43 | BuildFS "247 issues confirmed in 47 projects" | sotiropoulos2020buildfs Abstract | **MISLABELLED** (source-internal inconsistency not flagged) | The abstract says 247. The body says **237** twice: §1 (l.142) and §5 Table 2 text (l.1351, l.1710). | Write "237 issues (247 in the abstract)" or cite the Table 2 figure. |
| F8 | review.md:52 | "About 30% of projects adopt caching … [R] Obs. 2.1, 4.3" | ghaleb2026cicaching | **MISLABELLED** (location) | 30% adoption is **Observation 1.1** (l.238–241). Obs. 2.1 is "Only 24% of caching adopters maintain their configuration". Obs. 4.3 (27% unused dependencies) is correct. | Change to "Obs. 1.1, 4.3". |
| F9 | review.md:51 | Kotinos preconditions in the "future-work section" | gallaba2020kotinos | **MISLABELLED** (location) | Pinned locks, isolated tests and minimal conditional behaviour are listed in **§9 Threats to Validity** (PDF l.826–862), not future work. | Change to "§9". |
| F10 | review.md:42; candidate-rules.md:30 | "ptrace costs about 2× on clean builds" cited to §III | licker2019incorrect | **MISLABELLED** (location) | In **§V-E Performance**: "slows down builds by a factor of two … measured on clean builds running on 4 threads" (l.668–670). | Change to "§V-E". |
| F11 | review.md:101 | Luo: "77% of the classified flaky-test fixes" cited to "Abstract, F.1" | Luo2014 | **MISLABELLED** | 77% is in §3 body: "the top three categories … represent 77% of the 161 studied commits" (l.340–341). It is not in the abstract, and it counts *commits*, not fixes. | "77% of the 161 studied commits [R §3; F.1 names the categories]". |
| F12 | review.md:102 | Gruber: 0.86% flaky cited to §I | Gruber2021 | **MISLABELLED** (location, minor) | 59% is in the abstract. 0.86% is in the results section (l.442, l.471), not §I. | "Abstract; §IV". |
| F13 | references.bib:587, :854 | `kalibera2020effectsize` and `kalibera2012quantifying` | — | **METADATA** (duplicate) | Same title and authors, conflicting dates: one says TR 4-12 "Nov 2013", the other year 2012. The arXiv 2007.10899 listing (fetched) dates the abstract Nov 2013. review.md and candidate-rules use only `kalibera2020effectsize`. | Merge into one entry: arXiv 2007.10899 (2020), with a note on the Kent TR 4-12 and the year verified from the TR cover. |
| F14 | references.bib:1199 | `perfbisect2022`: title "Effectiveness of Performance Bisection", no author | — | **METADATA** (wrong title, missing author) | The actual paper is Frolin S. Ocariza Jr., "On the Effectiveness of Bisection in Performance Regression Localization", *Empirical Software Engineering* 2022, DOI 10.1007/s10664-022-10152-3. The bib title is the project page's title. (Source: author page and Crossref, found by WebSearch 2026-11-21.) | Fix the title and author. Rename the key to `ocariza2022bisection` and update assumptions…md:30. |
| F15 | references.bib:231 | `ShiZhaoMarinov2019` has no venue | — | **METADATA** | "Understanding and Improving Regression Test Selection in Continuous Integration", Shi, Zhao, Marinov: ISSRE 2019. The PDF lacks the venue string, but ISSRE 2019 is the published venue. | Add `booktitle = {ISSRE}`. |
| F16 | references.bib (GligoricNegaraLegunsenMarinov2014) | Venue and year blank | — | **METADATA** | This is ASE 2014 (the paper's file name already says 2014). | Add `booktitle={ASE}, year={2014}` after checking DOI 10.1145/2642937.2643019. |
| F17 | references.bib:847 | `reichelt2023peass` given as arXiv only | — | **METADATA** (probable) | arXiv 2303.14256 v1 (24 Mar 2023) matches the PDF. I believe a conference version appeared at IEEE QRS 2022, but I did not confirm this from a primary source. | Check DBLP; add the venue if confirmed. |
| F18 | references.bib (`ghaleb2026cicaching`, `lyu2024echecker`) | No booktitle | — | **METADATA** (minor) | The Ghaleb PDF header shows **EASE 2026, 9–12 June 2026, Glasgow**, so the venue is confirmed in source and not just "per arXiv listing". The Lyu PDF shows 6 authors including Rigger, which matches the bib. Its venue is still unknown. | Add the EASE booktitle. Keep Lyu as a preprint. |
| F19 | taxonomy.md (passim), assumptions…md:28,30,31, candidate-rules.md:68 | Short forms `mokhov2020`, `najafi2019`, `zeller1999`, `legunsen2016`, … | — | **METADATA** (keys do not resolve) | 16 short forms are not bib keys (list in §4). README says "follow its citation key", so these break that rule. | Replace them with the full keys. |
| F20 | papers/ | `2019-RTSCheck-ICSE.pdf` and `2019-Zhu-RTSCheck-ICSE.pdf` | — | **METADATA** (minor) | Identical sha256 prefix 1b98f1cf…, so this is a duplicate file. The README count of "69 PDFs" includes both. | Delete one copy and update the count. |
| F21 | review.md:201; candidate-rules.md:67 | Uber "real conflict" 5% / 40% [R] §2.1–2.2 | ananthanarayanan2019keeping | **UNVERIFIABLE** locally | The PDF was removed (non-author host), so the [R] cannot be re-checked. | Keep [R] only if the T5 card quotes the passage. Otherwise re-obtain the paper from ACM or the author. |
| F22 | review.md:205 | Orso: dynamic impact safe only for observed executions [R] §2.3 | orso2004empirical | **UNVERIFIABLE** locally | No local PDF (the note says a Purdue-hosted copy was fetched). | Add the PDF, or downgrade to [F]. |
| F23 | review.md:207 | PyCG 69.9% recall, labelled [F] | salis2021pycg | Label is *too weak* (not an error) | The local PDF contains "precision 99.2%, and adequate recall 69.9%" (abstract, l.37). | Upgrade to [R] Abstract. |
| F24 | review.md:59, taxonomy.md:73 | testmon "Python ≥ 3.11 per PyPI"; scikit-build-core rebuild-on-import | TestmonBlog etc. | **UNVERIFIABLE** (not re-fetched) | Not checked. | Re-fetch the PyPI metadata before W3 relies on it. |

### Claims verified OK (sample of the 71)

- **Builds**
  - Mokhov JFP 30 e11 (2020): §2.1 minimality, fn. on timestamps (l.212), §3.6 correctness, §5.2, §8.3, §8.4 exist as cited.
  - Spall et al. 2022: "same result as running the commands in order".
  - Pluto: "a missing dependency makes the build script unsound".
  - Bezemer: >1.2 M unspecified dependencies, 6 causes.
  - Licker: 30 projects; the Python-import generator example.
  - Kotinos: 87.9%, 74% two-fold, <1% median CPU, graph-structure bypass for added or renamed files.
  - Ghaleb: Obs. 4.3, 27%.
- **RTS**
  - Ekstazi: AEC 68%, 46% for long suites.
  - Legunsen: 0.2% / 10.6% safety violations, 62.5–68.2% end-to-end, reflection as the cause.
  - Shi 2019: 76.0%, 39 missed / 38 flaky, non-source-file fallback.
  - Wang & Yu: 97.3%, 62.2%.
  - Gligoric 2014: 450 sessions, 27%.
  - RTSCheck: 27 bugs, 7 rules, no-flaky / no-order assumptions, DefectsEP reversal.
  - NameRTS: 69.90%, 45.59%, 99.6% of 500 commits, EkstaP 3.10%, 83.27% imports, 10.04% overhead, pays off after five commits, misses via global astroid cache and a docutils callback, eval/exec not modelled, non-Python-only commits filtered, BabelRTS 76.6%.
  - Rothermel 1997: controlled regression testing §3.1.2, four categories §4.1.
  - Elbaum: failure and execution windows.
- **Flaky tests**
  - Gruber: 59%.
  - iDFlakies: 50.5% of 422.
  - Parry: §3.2 victim/brittle.
  - Luo: floating point among root causes (§3.1.4).
- **Performance**
  - PerfRanker: 30–37% vs 65–79%.
  - Laaber 2021: 54 variants, APFD-P 0.54–0.71, 29–66%, 11%, dynamic > static.
  - Laaber 2022: <1%.
  - Grambow: 4 TPs (commits 10, 59, 64, 65), 17 false alarms, missed group-by trend from commit 20, daily application benchmark as backup.
  - Japke 2023: three issues detected earlier.
  - µOpTime: 76.8% Go, 13.08% / 26.78% Java, 3/29 FP, 2/7 FN, RCIW preferable for Java.
  - Laaber 2020 [A]: 48.4–86.0%, 78.8–87.6% (confirmed via search snippet).
  - Barrett: ≤43.5%.
  - Georges: CI of the difference, CoV.
  - Mytkowicz: ~33%, ~300%, 133 papers.
  - Stabilizer: <7%, 57%, ANOVA.
  - Laaber 2019: CV 0.03% to >100%, ≤10% slowdowns detectable with same-instance randomised runs.
  - Duet: 2.3–12.5×, 23.8–82.4×.
  - Ding: 76.9% / 74.3%.
  - Chen & Shang §1.
  - Daly: up to 99% false positives, "drift down" quote, E-Divisive.
  - Hunter: permutation test replaced by t-test.
- **Safety evaluation**
  - Just: 73 / 17 / 10%.
  - Papadakis: undecidable, redundant mutants.
  - Petrović: ≤1 mutant per line, Python 14.7%.
  - Reichelt: 1,000 Jetty commits, busy waiting, 58.7 / 26.7 / 14.6%.
  - Jin 2012: simple, functionality-preserving fixes.
  - Zhao: 15%, 13% in Python.
  - BugsInPy: 493.
  - Shi 2018: FBDL on future builds.
- **Batching and culprit finding**
  - Najafi: Eq. 1, Eq. 7–8, savings mostly by batch size 4, 9.0% / 7.6%.
  - Memon: 45 min milestones, 1.23%, "know for sure the culprit".
  - Henderson: Bayesian noisy search, NONE outcome, plateau with linearly growing cost.
  - Zeller 1999: interference, inconsistency, UNRESOLVED.
  - Zeller 2002: ddmin worst case quadratic.
  - Fallahzadeh: 75% with Batch4.
  - Jin & Servant: median 21%, skipped builds accumulate.
- **W2 claims** (PerfAgent 66–99% on GSO, §VI testmon Python-only; SysLLMatic final rebuild; Meta master runs every few hours): these match the per-system files `../02-practice-survey/per-system/perfagent.md` l.20–25, `sysllmatic.md`, and `industrial-ci-test-selection.md` l.31.

### [I] presented as a source claim

No sentence presents an inference as a finding of a named paper, apart from F3 (Daly) and F4 (NameRTS global code) above. The [R]/[I] mixed tags in review.md §6 are honest.

## 3. Counter-evidence to novelty claims

All searches used WebSearch (standard mode) on 2026-11-21.

| Claim | Query | Result | Effect on the claim |
|---|---|---|---|
| C1 (full-check interval from accumulated change) | `adaptive full regression test run triggered by accumulated code change since last full run regression test selection safety` | Nothing that triggers a full run from accumulated change. Related hits: US patent 8276123 (adaptive RTS to a chosen safety level); a UMD minimisation study finding selection effectiveness varies with the *number of changes* (Rothermel et al., STVR 2004). | **Stands** as "not found". Cite the UMD finding as motivation: selection quality depends on change volume. |
| C1 (second query) | `"regression test selection" periodically run full test suite every N commits to catch missed failures evaluation` | Ekelund & Engström: periodic (daily, weekly, monthly) or *rule-based* full execution is treated as a policy choice. Shi et al. 2019 RetestAll comparison. Wang & Yu. | **Stands**, but Ekelund & Engström should be added to closest-works as a "periodic / rule-based full run" precedent (industrial, not change-triggered). |
| C4 (Python benchmark selection) | `Python benchmark selection per commit performance regression microbenchmarks asv study` | Only Grambow (Go), Laaber (Java), µOpTime, and asv/scikit-image practice notes. | **Stands.** |
| C5 (RTS for native and C extensions) | `regression test selection Python C extensions native code safety study` | No Python study. Cross-language RTS exists for **Java+native**: RTSLinux (Celik et al., FSE 2017, "RTS across JVM boundaries": 74.17% tests skipped, 52.83% time saved in 21 projects) and BinaryRTS (Java tests calling C++ via JNI). arXiv 2603.06107 (C-extended Python, test generation). | **Stands for Python**, but the related-work gap is real: RTSLinux/BinaryRTS show that native-boundary RTS has been studied for the JVM. Add them, and narrow C5 to "for Python C/Cython extensions". |
| C6 (cumulative drift) | `cumulative performance regression many small commits below threshold "death by a thousand cuts" benchmark CI study` | Daly 2020; **Sayedsalehi et al. 2026 (Mozilla risk-aware batch testing of performance tests)**; a Swift forums thread on gradual regressions becoming the new baseline (practitioner); cbdr README. | **Partial** stands. Add Sayedsalehi 2026 (see F5) and the practitioner evidence. |
| C7 (stale dependency data across revisions) | `regression test selection outdated dependency information multiple revisions safety evaluation Ekstazi stale dependencies` | Gligoric's PhD thesis and ISSTA 2014 "RTS for distributed software histories": Ekstazi reasons over **multiple old revisions** (merges). Legunsen 2016 notes old-revision dependencies may be unavailable. No study measures safety vs dependency-data age. | **Stands**, but cite Gligoric et al. ISSTA 2014 as the nearest multi-revision RTS work. It handles multiple *revisions*, not *stale data*. |
| C10 (bisection under noise) | `"performance bisection" effectiveness Empirical Software Engineering 2022` | Ocariza 2022 (EMSE): bisection effectiveness for performance regressions depends on baseline choice and per-commit distributions. 310 bug reports, 17 apps. arXiv 2610.02995 BISCEPTER (probability-driven bisection, 2026). | **Partial** stands. Fix the bib (F14) and add BISCEPTER as a 2026 candidate to read. |

The search log itself (gap-and-search-log.md) records one query per gap with no result counts. "Not found" therefore rests on 1–3 general web queries per claim. The file says so honestly, and the "still open" list (citation screening, ACM DL/IEEE Xplore) is the right next step.

## 4. Missing bib keys (mechanical check)

The script extracted backticked identifiers and `nameYYYY` tokens from every `.md` in 01-literature and compared them against the 130 keys in references.bib. It found no duplicate keys, but one duplicate *work* (F13).

| File | Short forms that are not bib keys | Full key |
|---|---|---|
| taxonomy.md | `mokhov2020` | mokhov2020buildsystems |
| taxonomy.md | `spall2022` | spall2022forward |
| taxonomy.md | `gallaba2020` | gallaba2020kotinos |
| taxonomy.md | `licker2019` | licker2019incorrect |
| taxonomy.md | `legunsen2016` | legunsen2016static |
| taxonomy.md | `salis2021` | salis2021pycg |
| taxonomy.md | `laaber2020` | laaber2020dynamic |
| taxonomy.md | `laaber2022` | laaber2022searchbased |
| taxonomy.md | `traini2023` | traini2023steady |
| taxonomy.md | `bulej2020` | bulej2020duet |
| taxonomy.md | `memon2017` | memon2017taming |
| taxonomy.md | `henderson2023` | henderson2023flake |
| taxonomy.md | `jin2021` | jin2021helped |
| taxonomy.md | `zeller2002` | zeller2002simplifying |
| taxonomy.md, assumptions…md, candidate-rules.md | `najafi2019` | najafi2019bisecting |
| taxonomy.md, assumptions…md | `zeller1999` | zeller1999yesterday |

**Cited works with no bib entry:**
- LaForge (arXiv 2108.12469);
- PerfAgent (arXiv 2607.19653);
- SysLLMatic;
- the Meta paper;
- PeerJ CS 2021 Grambow call-graph study (PMC8176533);
- arXiv 2603.06107;
- Fallahzadeh et al. EMSE 2025;
- arXiv 2512.22256.

The W2 and [A] items are cited by arXiv ID or name, which is acceptable for a draft. PerfAgent is central to closest-works and should get a bib entry.

## 5. Consistency checks

- EkstaP: "3.10%" (review) and "3.1%" (taxonomy, candidate-rules) agree; the source says 3.10%.
- PerfAgent test reduction is "66–99% on GSO" everywhere, which matches W2.
- README counts are correct: 130 bib entries, 16 assumptions (A1–A7 + B1–B9), 69 PDFs (but one is a duplicate, F20).
- The µOpTime ranges in taxonomy.md ("13–77%") and review.md (13.1–26.8% Java, 76.8% Go) agree with the source (13.08 / 26.78 / 76.8).
- CI-skip savings: review.md gives "median 21% of build time" [F Jin & Servant] and taxonomy.md gives "18% fewer CI commits" [A Abdalkareem]. These are different metrics from different sources and are not contradictory, but taxonomy.md should name the source of the 18%.
