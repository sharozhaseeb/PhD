# Search log and gaps

**Status:** v3.2, 2026-11-21. Every search was run on 2026-11-21.

**Tools.** The WebSearch tool (general web, US results, standard or extended mode), the WebFetch tool (page fetches, which return a summary) and curl for open-access PDFs. No Scopus, Web of Science, Google Scholar API or citation-chasing tool was used.

**This is not a systematic review.**
- Result counts were not captured, so none are reconstructed here.
- Inclusion rule: primary sources (peer-reviewed papers, arXiv preprints marked as such, official documentation and source files) relevant to the topic brief.
- Exclusion rule: shadow libraries, and secondary summaries used as evidence.

## Researcher searches
Each topic researcher logged its queries in its own notes file, section (f) or (e):

| Topic | Searches logged | File |
|---|---|---|
| T1 Builds | 29 (queries, fetches, curl) | `notes/T1-builds.md` (f) |
| T2 RTS | 26 + curl attempts | `notes/T2-rts.md` (f) |
| T3 Performance | 36 | `notes/T3-perf.md` (f) |
| T4 Safety evaluation | 27 + 5 fetches | `notes/T4-safety-eval.md` (e) |
| T5 Batching / impact | 36 | `notes/T5-batching-impact.md` (e) |

## Architect gap searches (targeted, for `beyond-literature-claims.md`)

| ID | Query (exact) | Mode | Notable hits | Not found |
|---|---|---|---|---|
| G1 | `regression test selection trigger full test run after accumulated changes since last full run threshold` | extended | Vendor and practitioner blogs (accelq, smartbear, orangebeard, qable); a USPTO patent that narrows selection by run count; arXiv 2604.26689 (RTS for ML modules) | No research paper that triggers a full run from accumulated change |
| G2 | `benchmark selection profile call graph Python performance regression changed functions pyperf asv` | extended | NameRTS; PyCG; DyPyBench; a pyan3-based Python test-impact GitHub pull request; Grambow et al. PeerJ CS 2021 (call graphs vs microbenchmark relevance, PMC8176533) | No Python benchmark selection study |
| G3 | `cumulative performance drift many small commits benchmark baseline regression detection study` | extended | Daly et al. arXiv 2003.00584; Grambow 2212.09515; PRICE / RIT thesis; arXiv 2610.09023 (change-point method evaluation); corten issue #867 | No evaluation of drift against per-edit selection |
| G4 | `regression test selection Python C extension Cython coverage native code unsafe` | extended | arXiv 2603.06107 (C-extended Python fault detection); NameRTS; Cython Coverage.py; cython issue #6186; cython_coverage_demo | No RTS work on native extensions |
| G5 | `LLM code optimization agent selective validation test selection benchmark selection per iteration checkpoint full validation` | extended | PerfAgent; arXiv 2512.22256 (survey: LLM-based selection in agent scaffolds is unsound; analysis-based selection is not integrated — snippet only) | No other optimization system with selection and checkpoints |
| G5b | `regression test selection stale dependency information over multiple revisions without re-collection safety` | extended | Ekstazi §5; Legunsen 2016; STARTS; ISSRE 2018 "RTS opportunities" (Illinois); an unverified "freshness" snippet | No study of staleness across revisions |
| G6 | `incremental build correctness Python extension modules stale .so setuptools meson editable empirical study` | standard | Licker & Rice; EChecker; LaForge (arXiv 2108.12469, "same output as full build"); discuss.python.org setuptools thread; meson-python tests | No Python-extension rebuild study |
| G7 | `"test selection" "detection delay" OR "time to detect" missed failures batching periodic full run evaluation metric` | standard | Jin & Servant (ar5iv 2102.06666); Fallahzadeh et al. EMSE 2025 (queensu.ca, selection vs batching); DANTE (ICSE 2026, polimi) | No standard detection-delay metric for periodic full checks |

Sources from G1–G7 were seen only as search results [A]. The ones worth reading next are listed under "Still open" below.

## Critic and verification searches (2026-11-21)

**Critic counter-evidence searches** (standard mode; full queries in `critic-report.md` §3):
- C1 ×2: found Ekelund & Engström (ICSME 2015) and Rothermel et al. STVR 2004; no counter-example.
- C4: no counter-example.
- C5: found RTSLinux (FSE 2017) and BinaryRTS (Java/native).
- C6: found Sayedsalehi 2026 and a practitioner forum thread.
- C7: found Gligoric et al. distributed histories.
- C10: found Ocariza EMSE 2022 and BISCEPTER arXiv 2610.02995 (not read).

**Architect metadata checks** (standard mode). Each confirmed the metadata now in `references.bib`:
| Query | Confirms |
|---|---|
| Ocariza "On the Effectiveness of Bisection in Performance Regression Localization" | EMSE 27(4) 2022, DOI 10.1007/s10664-022-10152-3 (Crossref) |
| Gligoric Negara Legunsen Marinov manual vs automated test selection | ASE 2014, pp. 361–372, DOI 10.1145/2642937.2643019 |
| Celik et al. "Regression test selection across JVM boundaries" | ESEC/FSE 2017, pp. 809–820 |
| Ekelund Engström test history industrial evaluation | ICSME 2015, pp. 449–457 |
| Gligoric et al. "Regression test selection for distributed software histories" | CAV 2014 (not ISSTA) |
| Shi Zhao Marinov RTS in CI ISSRE 2019 | ISSRE 2019, pp. 228–238 |

## v3 reads and forward-citation screening (2026-11-21)

**Full reads**
- `notes/R1-perfagent-fullread.md`: PerfAgent PDF, including Appendices A–D.
- `notes/R2-batching-threats-fullread.md`: Fallahzadeh 2025 (accepted manuscript), Sayedsalehi 2026, and the agentic survey (targeted sections).

**Forward citations** (`notes/R3-forward-citations-namerts-artifact.md`, which holds the full query log)
- Tools: the Semantic Scholar Graph API citations endpoint, OpenAlex `cited_by_count`, and WebSearch.
- PerfAgent: 7 citers. NameRTS: 1 citer.
- Gap: the OpenAlex citer lists were not enumerated.
- NameRTS artifact found via the arXiv HTML; WebSearch did not surface it.

## ACM DL and IEEE Xplore (done 2026-11-21, v3.2)

**Result: done.** Searches were run in the student's own Chrome with the student's authorisation; there was no sign-in and no internal API was called. Full record: [database-search-2026-11-21.md](database-search-2026-11-21.md).
- 7 ACM DL queries and 13 IEEE Xplore queries (5 exact, 1 control, 7 adapted to IEEE's Boolean parser).
- **123 records screened.**

**Effect on the claims**
- **C7:** not found → partial (Chittimalli & Harrold, TSE 2009).
- **C1, C5, C8, C11:** stand. Added references: Bavand & Rigby (ICSME 2021) for C1; Elsner et al. (ICSE-SEIP 2022) and Kauhanen et al. (SANER 2021, venue now confirmed) for C5.
- The four DOIs were resolved through the Crossref API on 2026-11-21: 10.1109/TSE.2009.4, 10.1109/ICSME52107.2021.00026, 10.1145/3510457.3513078, 10.1109/SANER50967.2021.00077. Title and authors match.

**Earlier attempt (v3.1).** The same ACM DL URLs returned HTTP 403 to the fetch tool, and IEEE Xplore returned a connection reset and then HTTP 418. A scripted call to IEEE's internal API was denied by the tool-permission policy and was not retried.

## Metadata re-checks (v3.1)

| Item | Source | Confirmed |
|---|---|---|
| pytest-testmon | PyPI JSON | 2.3.1, `requires_python >=3.11`, Beta |
| Peass (Reichelt et al.) | WebSearch `Reichelt Kühne Hasselbring "Automated Identification of Performance Changes at Code Level" QRS 2022` | IEEE QRS 2022, pp. 916–925, DOI 10.1109/QRS57517.2022.00096 |

## Novelty searches on measured findings (2026-11-22)

Targeted searches on W3 findings B1, C11, N6, N7, R1 and H1/C8.
- Query logs: `notes/N1-benchmark-coverage-search.md` (37 queries), `notes/N2-aa-noise-search.md` and `notes/N3-cost-and-stale-binary-search.md` (20 searches, 9 fetches).
- Tools: WebSearch, WebFetch, arXiv, and GitHub source for asv and pyperf. ACM DL and IEEE Xplore were not re-run.
- Results are in `beyond-literature-claims.md`, section "Measured findings vs literature (2026-11-22)".

**Open from these searches**
- Read Laaber & Leitner MSR 2018 and FormulaCode in full.
- Search the asv and pandas GitHub issue trackers directly.
- Confirm the installed asv version's default factor, and that `mann_whitney_u` is two-sided.

## Known gaps in coverage (not read or not obtained)

**Full text not obtained**
- Rothermel & Harrold TSE 1996 (the four-category framework is known only through TOSEM 1997 §4.1).
- Rothermel et al. TSE 2001 (APFD).
- Perphecy, PerfScope and PRICE.
- Laaber et al. FSE 2020 (dynamic reconfiguration) and Laaber & Leitner MSR 2018.
- Costa et al. TSE (JMH bad practices).
- HyRTS, STARTS tool paper, reflection-aware RTS (OOPSLA 2019), Harrold et al. OOPSLA 2001.
- Yoo & Harman survey.
- Beheshtian et al. TSE, Ziftci & Reardon, Abdalkareem et al. CI skip.
- Andrews et al. ICSE 2005, Delgado-Pérez et al. performance mutation.
- Commit-aware mutation (ICSME 2020).
- Chianti, Law & Rothermel, Orso et al. FSE 2003.
- Arnold & Bohner, Lehnert.

**Not searched**
- Buck2, Pants and BuildXL docs; pip wheel cache; importlib caches; `-X` flags.
- Microsoft and Facebook culprit finding.
- pyperformance docs; pytest-codspeed docs.
- Python-specific impact-analysis tools beyond PyCG and Jarvis.

**Corrections made to the brief** (titles or authors that were wrong or not found)
- "Escaping dependency hell" — not found.
- "Lessons from Eleven Years of CI build failures" — not found.
- DejaVOO is Orso et al. (FSE 2004 line), not Harrold et al. OOPSLA 2001.
- PerfScope authors are Huang, Ma, Shen, Zhou.
- Petkovich is not a Perphecy author.
- µOpTime is TOSEM 2025, not ICPE 2023.
- Japke is not an author of the Grambow et al. TCC paper.
- Kalibera is not a Costa et al. author.
- Shi et al. ISSTA 2018 authors are Shi, Gyori, Mahmood, Zhao, Marinov.
- RegMiner and commit-aware mutation authors corrected.
- "Mining Bug Databases" — not found (real: Bavand & Rigby ICSME 2021).
- "Probabilistic Flakiness" — a Facebook blog, not a Google paper.

**Still open before any novelty claim** (the prior package's rule)
- Forward citations of PerfAgent and NameRTS: done in v3 (see "v3 reads and forward-citation screening" above). Still open: backward citation screening of both, and forward and backward screening around Najafi 2019, Grambow 2022 and Daly 2020.
- Done in v3: Fallahzadeh 2025, Sayedsalehi 2026, arXiv 2512.22256 (targeted), PerfAgent. Still unread: BISCEPTER (C10 struck, so not needed for Study 1) and the RTSLinux full text.
- Done in v3.1: Peass venue (QRS 2022) and testmon PyPI metadata.
- Done in v3.2: ACM DL and IEEE Xplore searches (`database-search-2026-11-21.md`).
- Still open: the full text of Chittimalli & Harrold 2009 (needs institutional access).
