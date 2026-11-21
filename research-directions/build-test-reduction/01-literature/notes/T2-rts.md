# T2 - Functional regression test selection (RTS), prioritization, flaky tests

Researcher: T2 literature agent. Date: 2026-11-21. Scope: deterministic rules for reduced build and reduced test set per optimization edit in Python (possibly C/Cython) code. No AI in the method.

Label legend: [read-in-source] = I read the passage in a PDF I downloaded (section given; page numbers are not reliable in the text extraction, so sections are cited); [abstract-only] = only abstract, search snippet or web-page summary seen; [inferred] = my reasoning; [unknown] = could not verify.

Local PDFs are in `../papers/`. Text of each was extracted with pdftotext; section numbers come from that extraction.

---

## (a) Source cards

### A1. Rothermel and Harrold 1997 - safe RTS definition and "controlled regression testing"
- Citation: G. Rothermel, M. J. Harrold. "A Safe, Efficient Regression Test Selection Technique." ACM TOSEM 6(2), April 1997, article pages 173-210 (pages 173-210 confirmed from Ekstazi's reference list; journal header "Vol. 6, No. 2, April 1997" read in the PDF).
- File: `../papers/1997-Rothermel-Safe-Efficient-RTS-TOSEM.pdf`. This copy was NOT downloaded by me (another researcher's file, found in the folder, originally named "1996-..." and not the TSE 1996 paper). I read it but did not hash it for T2-downloads.json.
- [read-in-source] Sec. 3.1.2: "Controlled regression testing is the practice of testing P' under conditions equivalent to those that were used to test P" (holding all other factors that might affect behavior constant). An algorithm that selects every fault-revealing test is safe; under controlled regression testing, the modification-traversing tests are a superset of the fault-revealing tests, so selecting all modification-traversing tests is safe (Theorem 3.1.2.1, SelectTests safe for controlled regression testing).
- [read-in-source] Sec. 3.1.1/3.1.2: assumes P terminated and produced specified output for each test on the old version; the test-obsolescence assumption is "necessary in order to reuse tests at all". Technique selects tests whose execution trace (via CFG edges, branch traces) reaches changed code; no efficient algorithm precisely identifies modification-traversing tests in general (Sec. 3.1.2 discussion, "unless P = NP").
- NOT read: the TSE 1996 "Analyzing regression test selection techniques" paper (inclusiveness, precision, efficiency, generality) - I could not locate an open-access copy. Mentioned only through citations in RTSCheck (Sec. I: "framework for analytically evaluating RTS techniques [16]"), [read-in-source] for that citation; the four-metric list is [unknown] here beyond the task brief.

### A2. Gligoric, Eloussi, Marinov - Ekstazi (ISSTA 2015)
- Citation: M. Gligoric, L. Eloussi, D. Marinov. "Practical Regression Test Selection with Dynamic File Dependencies." ISSTA 2015. Pages not verified. File: `../papers/2015-Ekstazi-ISSTA.pdf` (author-hosted copy at users.ece.utexas.edu/~gligoric).
- [read-in-source] Sec. 1: end-to-end time (analysis A + execution E + collection C phases) must be below RetestAll time for adoption; most papers report only E.
- [read-in-source] Sec. 2: method-level selection by naive intersection of used methods with changed methods is unsafe (e.g., an added overriding method D.m; a changed final field value). Safe method granularity needs extra dependencies (fields, existence of methods), making collection and analysis expensive. Class granularity can use a fast check of the new revision only. "when tests depend not only on the code under test but also on external files, collecting only the classes is not safe, and hence Ekstazi uses files as dependencies."
- [read-in-source] Sec. 3: analysis phase checks whether the checksums of all files used by each test are unchanged; no old revision or VCS needed. Collection records all files read or written, including attempted accesses to non-existent files, instruments bytecode incl. "reflection invocations" (Sec. 3.3, instrumented code points list). Sec. 3.5 smart checksums ignore debug-info-only differences. The paper states "We leave it as a future work to formally prove that Ekstazi is safe" (Sec. 3 intro) and that safety "intuitively follows from the proven safety of RTS based on class dependencies".
- [read-in-source] Sec. 4.3: selection ratio of test entities 5%-38% of RetestAll; end-to-end time (AEC) 9%-138% of RetestAll, mean 68%; AE only mean 53%. All slowdowns were for projects with short-running test suites. For long-running suites: AEC mean 46%, AE mean 34% ("roughly halves their testing time" for suites over a minute). Sec. 4.7: Ekstazi compared with FaultTracer (method-level); FaultTracer's cost stems from fine-grained collection/analysis.
- [read-in-source] Discussion (Sec. 5, heading not extracted): "if a dependency changes for another run that was not observed, the test will not be selected. This is the common approach in RTS" - dependencies come from one observed run only.
- Relevance: file-level dynamic dependencies with checksums is the closest published analogue to rule F1 below.

### A3. Legunsen et al. - static RTS study (FSE 2016)
- Citation: O. Legunsen, F. Hariri, A. Shi, Y. Lu, L. Zhang, D. Marinov. "An Extensive Study of Static Regression Test Selection in Modern Software Evolution." FSE 2016, Seattle, pp. 583-594 (pages as cited in another paper's reference list). File: `../papers/2016-StaticRTS-Legunsen-FSE.pdf` (mir.cs.illinois.edu).
- [read-in-source] Abstract and Sec. 1: 985 revisions of 22 Java projects; class-level static RTS (ClassSRTS, class firewall) comparable to Ekstazi but sometimes unsafe; method-level static RTS (MethSRTS, call graph) performs poorly. Dynamic RTS may be unsafe with non-determinism (randomness, concurrency) because dependencies collected dynamically may not cover all traces (Sec. 1).
- [read-in-source] Sec. 4.2.1: mean fraction of tests selected: Ekstazi 20.6%, ClassSRTS 29.4%, MethSRTS 43.8%. Sec. 4.2.2: end-to-end time vs RetestAll about 62.5%-68.2% for ClassSRTS and Ekstazi (offline modes 62.5% vs 64.0%); "offline" mode excludes dependency collection time from end-to-end time (footnote 3), "online" includes it. Some projects worse than RetestAll (ClassSRTS 2, Ekstazi 5 projects); more benefit for long-running tests.
- [read-in-source] Sec. 4.2.3: ClassSRTS safety violations in 2 projects, 0.2% of revisions on average (safety measured relative to Ekstazi's selection, so it is "unsafe w.r.t. Ekstazi", not ground truth); MethSRTS 10.6% of revisions unsafe. Sec. 4.3: safety violations due to reflection (commons-math example: nine tests missed).

### A4. Gligoric et al. - manual vs automated selection (ISSTA 2014)
- Citation: M. Gligoric, S. Negara, O. Legunsen, D. Marinov. "An Empirical Evaluation and Comparison of Manual and Automated Test Selection." Venue/year not printed in the extracted text; I know it as ASE 2014 from memory only - [unknown], not used in bib as venue. File: `../papers/2014-ManualRTS-Gligoric.pdf`.
- [read-in-source] Abstract: 14 developers, three months; almost all do manual selection ad hoc; over 450 test sessions manual and automated selection differed in every session; manual picked more tests 73% of the time and fewer 27% of the time (potentially missing bugs).
- Relevance: a human "pick the relevant tests" policy is both wasteful and unsafe; motivates a deterministic rule.

### A5. Shi, Zhao, Marinov - RTS in CI (2019)
- Citation: A. Shi, P. Zhao, D. Marinov. "Understanding and Improving Regression Test Selection in Continuous Integration." IEEE, 2019 (copyright line 2019 IEEE; conference name not found in extracted text; the brief says ISSRE 2019 - [unknown] as read). File: `../papers/2019-Shi-RTS-in-CI-ISSRE.pdf` (NSF PAR copy).
- [read-in-source] Abstract/Sec. I: module-level (GIB) vs class-level (Ekstazi) vs hybrid GIBstazi on Travis CI; RTS saves time but total build time with RTS is 76.0% of RetestAll, "not as low as found in previous work, due to the extra overhead in a cloud-based CI environment".
- [read-in-source] Sec. I: class-level RTS "has two issues": it can miss changes in non-source files such as configuration files (module-level selects the whole module in that case), and needs extra analysis time. GIBstazi defaults to selecting all tests in the affected module when a change touches a non-source file not tracked by class-level RTS.
- [read-in-source] Sec. I: RTS missed 39 failures that RetestAll saw, 38 of 39 were flaky-test failures; 19 non-flaky failing pull-request jobs: no failure missed. (Flaky failures are avoided "by chance".)

### A6. Wang and Yu - RTS in CI (ISSRE 2018)
- Citation: T. Wang, T. Yu. "A Study of Regression Test Selection in Continuous Integration Environments." IEEE 29th International Symposium on Software Reliability Engineering (ISSRE) 2018; pages 135-143 as given in Shi et al.'s reference list (listed there as "T. Yu and T. Wang", author order differs from the PDF title page "Ting Wang, Tingting Yu" - [read-in-source]). File: `../papers/2018-WangYu-RTS-in-CI-ISSRE.pdf`.
- [read-in-source] Abstract/Sec. I: 918 GitHub CI projects, 7,018,512 commits. 60% of commits are separated by more than 10-minute intervals; 62.2% of Java projects have average test time not exceeding 25% of commit interval (RTS may not be needed); static method-level RTS worse than RetestAll in 97.3% of Java projects, static class-level RTS saves time in 56.8%.
- Relevance: RTS pays off only when analysis overhead is small relative to test time.

### A7. Zhu, Legunsen, Shi, Gligoric - RTSCheck (ICSE 2019)
- Citation: C. Zhu, O. Legunsen, A. Shi, M. Gligoric. "A Framework for Checking Regression Test Selection Tools." ICSE 2019, pp. 430-441 (pages and DOI from the BibTeX listing, [abstract-only]). File: `../papers/2019-RTSCheck-ICSE.pdf` (cs.cornell.edu/~legunsen). A second copy `2019-Zhu-RTSCheck-ICSE.pdf` exists from another researcher.
- [read-in-source] Abstract and Sec. I: RTSCheck feeds evolving programs to an RTS tool and checks seven hand-crafted rules covering safety, precision, generality violations; 27 bugs in Clover, Ekstazi, STARTS. "RTSCheck uses the common assumptions in RTS research that tests are not flaky and there is no test-order dependency." Efficiency report compares end-to-end time with RetestAll. "proofs and analyses may not carry over to the RTS tools that implement those techniques".
- [read-in-source] Sec. I: example safety rule: a newly failed test (passes old, fails new under RetestAll) must be selected; precision rule: second run on the same revision should select nothing. These are directly adaptable to validating a reduced-test policy.

### A8. Liu et al. - more precise RTS (ISSTA 2023)
- Citation: Y. Liu, J. Zhang, P. Nie, M. Gligoric, O. Legunsen. "More Precise Regression Test Selection via Reasoning about Semantics-Modifying Changes." ISSTA 2023, Seattle, July 17-21, 2023. File: `../papers/2023-Liu-PreciseRTS-SemanticsModifying-ISSTA.pdf`.
- [read-in-source] Abstract: analysis-based RTS has hit a "performance wall"; authors manually inspect changes and find 13 finding types, 11 of which are semantics-modifying; they extend Ekstazi and STARTS to ignore changes that cannot alter test behaviour. [abstract-only for the numeric details beyond 13/11.]
- Relevance: formalizes that some edits (e.g., refactoring, comment edits) need no re-testing; but performance-motivated edits are by definition semantics-visible only in time, not output - see (d).

### A9. Zhang et al. - analysis-based vs learning-based RTS (AST 2022)
- Citation: J. Zhang, Y. Liu, M. Gligoric, O. Legunsen, A. Shi. "Comparing and Combining Analysis-Based and Learning-Based Regression Test Selection." AST '22, May 17-18, 2022, Pittsburgh (read in first page). File: `../papers/2022-Zhang-AnalysisVsLearning-RTS-AST.pdf`.
- [read-in-source] Abstract: ML-based RTS combined with Ekstazi and STARTS selects 25.34% and 21.44% fewer tests respectively (as stated; the safety trade-off is discussed in the paper). ML-based RTS: later AI study only.

### A10. Wang, Pradel, Liu - NameRTS (arXiv 2026) - Python RTS research
- Citation: Y. Wang, M. Pradel, Z. Liu. "Names Are All You Need: Effective and Safe Regression Test Selection for Python." arXiv:2605.25356v1 [cs.SE], 25 May 2026, 22 pages. Preprint; peer-review status [unknown]. DOI placeholder in the PDF ("nnnnnnn") - not a real DOI. File: `../papers/2026-NamesAreAllYouNeed-PythonRTS-arXiv.pdf`.
- [read-in-source] Abstract: first Python RTS approach with fine-grained dependency analysis; bipartite graph of code elements and names; selection is reachability from the names used by a test; dataset of 500 commits of 10 Python projects; skips 69.90% of test files on average, cuts end-to-end time by 45.59%; selects all affected tests for 99.6% of commits. Baselines: BabelRTS (file-level; safe for 76.6% of commits) and EkstaP (their safe Ekstazi-style file-level baseline).
- [read-in-source] Sec. 1: Python's eager importing means importing a submodule executes parent `__init__.py` files so file-level dependency sets inflate; call-graph construction is weak (PyCG detects 49% of runtime call edges of DynaPyt on 39 projects, citing Bouzenia et al.). Coverage-based RTS selects most tests because import-time code is covered by every test.
- [read-in-source] Sec. 4.2: EkstaP (file-level, safe) reduces only 7.42% of tests and 3.10% of time; on average one test file imports 83.27% of source files and 80.92% of source files are imported by every test file. BabelRTS unsafe cases: ignoring implicit parent-package imports (matplotlib safe rate 14.00%, pylint 48.00% - pylint through runtime plugin loading via importlib). NameRTS precision 66.65%; ground-truth maximum reduction 80.69%.
- [read-in-source] Sec. 4.2 safety misses (2 commits): (1) shared global state in `astroid.MANAGER` left by an earlier test made a pruned path unreachable (test interference); (2) a callback protocol hard-coded in an external library (docutils calling sphinx `dispatch_visit`) is invisible because library code is not analyzed.
- [read-in-source] Sec. 3.4: introspection (getattr etc.) is handled by monkey-patching built-ins; names accessed during import are treated as shared by all tests; "Dynamic code execution through eval or similar mechanisms is not tracked". Sec. 5: "NameRTS does not model fully dynamic code execution mechanisms such as eval and exec". Granularity of evaluation is test files, not test functions.
- [read-in-source] Sec. 4.3 overhead: average 10.04% of full-suite time (init 2.38%, selection 3.22%, runtime instrumentation 4.45%); pays off after about five commits. Sec. 4.1: 50 consecutive commits per project; build-failing commits excluded; commits changing only non-Python files excluded ("We also require that each commit modifies at least one Python source file"). Network-dependent projects excluded because timing is unstable.
- Not covered: C extensions, Cython, non-Python data files are not discussed in the passages I read ([unknown] whether they are mentioned elsewhere in the 22 pages).

### A11. pytest-testmon (documentation)
- Sources: https://testmon.org/blog/determining-affected-tests/ ("Determining affected tests"); https://pypi.org/project/pytest-testmon/ ; https://github.com/tarpas/pytest-testmon . Fetched via WebFetch on 2026-11-21, so content is a summary produced by the fetch tool, not the raw page: label [read-in-source, via fetch summary].
- Mechanism: coverage.py supplies executed lines per test; source is split into blocks; each test depends on the blocks it executed; per block a checksum is stored ("testmon doesn't store the whole code of the block but just a checksum of it"); a test is re-run if any dependent block checksum changed; "no heuristics". The page says its "limits and reliability ... are pretty much the same as limits of coverage.py". It assumes an unexecuted line "doesn't influence the outcome of execution of the surrounding code". Executed code changes trigger re-execution ("we re-execute dependent tests even on smallest change"). Database `.testmondata`; tests that failed last time are always re-run (PyPI summary of version history, [abstract-only]).
- [read-in-source via fetch] PyPI page: beta status, Python >= 3.11, and an offer to CI users that "no tests are deselected initially".
- NOT found in testmon docs (as fetched): any statement on data files, config files, environment, C extensions, third-party package changes. [unknown]; do not claim testmon tracks or misses them from this source. https://testmon.org/docs/ returned 404.

### A12. coverage.py limitations
- Source: https://coverage.readthedocs.io/en/latest/trouble.html (fetched 2026-11-21).
- [read-in-source via fetch summary] "Things that don't work": exec/execv variants lose collected data; threads created with the low-level `thread` module are not traced; other tools using sys.settrace or sys.setprofile conflict.
- [unknown] The fetched page does not mention C extensions or compiled code at all. That coverage.py traces Python bytecode lines only and therefore cannot attribute execution inside C/Cython code to .c/.pyx lines is [inferred] (well-known in practice, but I did not read it in a source). Cython line tracing needs a separate Cython coverage plugin and compile-time `linetrace` directive - [unknown]/[inferred], verify in Cython docs before relying on it.

### A13. pytest cache and pytest-picked
- pytest cache docs https://docs.pytest.org/en/stable/how-to/cache.html [read-in-source via fetch summary]: `--lf` re-runs only last failures; `--ff` runs failures first then rest; `--nf` runs new tests first, ordered by file modification time; `--sw` stops at first failure; `--lfnf` controls what `--lf` does with no known failures (default all); `--cache-clear` is "recommended for invocations from Continuous Integration servers".
- pytest-picked https://github.com/anapaulagomes/pytest-picked [read-in-source via fetch summary]: selects test files modified but not committed via `git status` (`--mode=unstaged` default) or against a parent branch (`--mode=branch`); `--picked=first` runs modified-file tests first then the rest. It selects changed TEST files only, not tests affected by changed source [inferred from the described behaviour; the README does not state this explicitly]; no limitations section.
- These are heuristics (prioritization or cheap filters), not safe RTS.

### A14. Kauhanen et al. - pytest-rts (Helsinki)
- Citation: Kauhanen, Nurminen, Mikkonen, Pashkovskiy, "Regression Test Selection Tool for Python in Continuous Integration Process" (University of Helsinki / F-Secure). Venue and year [unknown] (CORE download returned HTTP 403 / HTML; not downloaded). [abstract-only via search snippet]: coverage-based RTS integrated with pytest, coverage.py and git. PyPI (pytest-rts) lists workflow: `pytest --cov=... --cov-context=test` builds a mapping database; `pytest --rts` selects after changes ([abstract-only], PyPI search snippet). NameRTS (A10, Sec. 6 related work) describes pytest-rts as selecting "based on previously observed coverage at the test-function level" [read-in-source, secondhand].

### A15. Elbaum, Rothermel, Penix - Google CI (FSE 2014)
- Citation: S. Elbaum, G. Rothermel, J. Penix. "Techniques for Improving Regression Testing in Continuous Integration Development Environments." FSE 2014, pp. 235-245, DOI 10.1145/2635868.2635910 (pages and DOI from search record, [abstract-only]). File: `../papers/2014-Elbaum-RTS-CI-Google-FSE.pdf` (copy from a University of Waterloo course page; not the publisher's version, unverified identity beyond title/authors read on page 1).
- [read-in-source] Abstract: pre-submit phase uses RTS with algorithms that are inexpensive and "do not rely on code coverage information"; post-submit phase uses prioritization. Sec. 4.1: SelectPRETests (Algorithm 1) selects test suites that (1) failed within a failure window Wf, (2) have not been executed within an execution window We, or (3) are new. Windows are counted in time/commit terms relative to prior pre-submit and post-submit results. Empirical study on a large Google data set.
- Relevance: a cheap, history-based rule that is deterministic, needs no coverage, and guards against stale baselines (execution window).

### A16. Flaky tests: Luo (FSE 2014), Lam iDFlakies (ICST 2019), Gruber (ICST 2021), Parry survey (TOSEM 2021)
- Luo et al. "An Empirical Analysis of Flaky Tests." FSE 2014, pp. 643-653 (pages and DOI from search [abstract-only]; PDF title page read). File: `../papers/2014-FlakyTests-Luo-FSE.pdf`. [read-in-source] Abstract: "An important assumption of regression testing is that test outcomes are deterministic". 201 commits fixing flaky tests in 51 projects. Findings F.1: top three causes Async Wait (74 of 161 classified commits = 45%), Concurrency, Test Order Dependency (these three = 77% of 161); F.7: 47% of order-dependency flaky tests due to external resources; F.10: 74% of order-dependency flaky tests fixed by cleaning shared state; other categories include Floating Point Operations, Randomness, Time, IO (Sec. 3.1).
- Lam et al. "iDFlakies." ICST 2019, pp. 312-322 [abstract-only for page range]. File: `../papers/2019-Lam-iDFlakies-ICST.pdf` (NSF PAR copy). [read-in-source] Abstract: detects flaky tests by reordering/rerunning; dataset of 422 flaky tests, 50.5% order-dependent. Maven/Java tool.
- Gruber, Lukasczyk, Kroiss, Fraser. "An Empirical Study of Flaky Tests in Python." ICST 2021 (arXiv:2101.09077). File: `../papers/2021-Gruber-FlakyTests-Python-ICST.pdf` (arXiv). [read-in-source] Sec. I/RQ summaries: 22 352 PyPI projects, 876 186 tests; 7 571 flaky tests (0.86% of tests) in 1 006 projects (4.5% of projects); 59% of flakiness from order dependencies, 28% from test-infrastructure problems, 13% mostly networking and randomness. Contribution (c): a rerun-count estimate; "170 reruns" for 95% confidence appears in the search abstract [abstract-only].
- Parry, Kapfhammer, Hilton, McMinn. "A Survey of Flaky Tests." ACM TOSEM 31(1), Article 17, 2021/2022. File: `../papers/2021-Parry-SurveyFlakyTests-TOSEM.pdf` (author copy, 74 pages). [read-in-source] Abstract: 76 papers surveyed; causes, costs, detection, mitigation. Sec. 3.2 defines victim and brittle order-dependent tests (victim passes alone and fails after a polluter; brittle needs a state-setter run before it). Sec. 1: common practice of rerunning failures. Not read in depth: the sections on RTS interplay; the survey does not appear to centre RTS.
- Effects on RTS: see (c).

### A17. Shi et al. - Reflection-aware static RTS (OOPSLA 2019)
- Citation: A. Shi, M. Hadzi-Tanovic, L. Zhang, D. Marinov, O. Legunsen. "Reflection-Aware Static Regression Test Selection." PACMPL 3(OOPSLA), 2019, DOI 10.1145/3360613 (from search record). 
- NOT downloaded: guessed URLs returned HTML; par.nsf.gov purl/10603280 returned HTML. [abstract-only via search snippet]: evaluates five reflection-aware static RTS techniques (three static, two hybrid); finding: making static RTS safe wrt reflection is challenging; thesis predecessor reports 805 revisions of 22 Java projects (Hadzi-Tanovic M.S. thesis, Illinois 2018 - from search snippet, [abstract-only]).

### A18. Zhang - HyRTS (ICSE 2018); STARTS tool; Harrold OOPSLA 2001; Yoo and Harman; Gligoric dissertation; Machalica
All NOT read in full; no PDF downloaded.
- L. Zhang. "Hybrid Regression Test Selection." ICSE 2018, pp. 199-209, DOI 10.1145/3180155.3180198 [abstract-only]: combines method- and file-level selection; 2,707 revisions of 32 projects; fewer tests than file-level and faster offline.
- O. Legunsen, A. Shi, D. Marinov. "STARTS: STAtic Regression Test Selection." ASE 2017 tool demo, pp. 949-954, DOI 10.1109/ASE.2017.8115710 [abstract-only]: compile-time dependency graph of types, Maven plugin; abstract reports about 35.2% of tests selected and end-to-end time about 81.0% of RetestAll (as relayed by search result).
- M. J. Harrold et al. "Regression Test Selection for Java Software." OOPSLA 2001, pp. 312-326 [abstract-only]: safe RTS technique for Java; the search snippet names the system "Retest", not DejaVOO. Legunsen FSE'16 Sec. 1 cites "DejaVOO [27]" and Sec. 2.1 cites "Orso et al. [27]" for the intertype relation graph, so DejaVOO = Orso et al. [27] [read-in-source]; RTSCheck's reference list contains "A. Orso, N. Shi, M. J. Harrold, Scaling regression testing to large software systems, FSE" [read-in-source] (that is probably [27], the FSE 2004 paper - [inferred]). Flag to the lead: the brief's "Harrold OOPSLA 2001 DejaVOO" pairing is probably wrong; OOPSLA 2001 is the Retest system, DejaVOO is the Orso FSE 2004 line. Neither PDF was obtained.
- S. Yoo, M. Harman. "Regression testing minimization, selection and prioritization: a survey." STVR 2012, DOI 10.1002/stvr.430 [abstract-only]: three branches; not downloaded (only a 2007 preprint copy was located; I did not use it).
- M. Machalica, A. Samylkin, M. Porth, S. Chandra. "Predictive Test Selection." ICSE-SEIP 2019 (arXiv:1810.05286) [abstract-only]: learned classifier on historical outcomes; reports over 95% of individual test failures and over 99.9% of faulty changes caught per search snippet. LATER AI STUDY ITEM ONLY (no AI in the method now).
- BabelRTS: G. Maurina, W. Cazzola, S. Ghosh, "BabelRTS: Polyglot Regression Test Selection," IEEE TSE 2025 - [read-in-source] only as a reference-list entry in A10 plus A10's description (file-level, regex-based rules, "not always safe"). The paper itself not found/read.
- Rothermel et al. TSE 2001 (APFD) and Graves et al. TOSEM 2001: only found as typeset.io, Scribd or similar; I did not download those (not legitimate-host OA that I could verify; the UNL digital commons guessed URL returned HTML). Content [unknown]. APFD is therefore not source-verified in this file.

---

## (b) Synthesis

### Static vs dynamic
- Dynamic RTS (Ekstazi, testmon, pytest-rts): run tests on the old revision, record what each test touches, and select tests whose recorded dependencies changed. Safe only for dependencies seen in the recorded run [read-in-source: Ekstazi Sec. 5 discussion; Legunsen Sec. 1 on non-determinism].
- Static RTS (STARTS/ClassSRTS, NameRTS static part): over-approximates dependencies without running tests; rarely misses at class level in Java (0.2% of revisions relative to Ekstazi, Legunsen Sec. 4.2.3) but is blind to reflection (Sec. 4.3). For Python, static call-graph approaches are weak [read-in-source: NameRTS Sec. 1], so Python tools lean on name matching (NameRTS) or runtime coverage (testmon, pytest-rts).
- Hybrid: NameRTS uses static name reachability pruned by dynamic observation; HyRTS combines file and method level [abstract-only].

### Granularity
- Class/file level: cheaper analysis, selects more tests, but safer and faster end to end (Ekstazi Sec. 2, 4.5-4.6; Legunsen Sec. 4.2). Module level: cheapest and coarsest, used in industry (Shi 2019 Sec. I).
- Method level: more precise but costs more in A and C phases and is unsafe if only used methods are intersected (Ekstazi Sec. 2).
- Python: file level is almost useless because of eager imports (EkstaP 7.42% test reduction; NameRTS Sec. 4.2); function/name level gives 69.90% test-file reduction (NameRTS). testmon works at block (function/method body) checksum level, coverage-based [read-in-source via fetch].

### Safety assumptions (all [read-in-source] unless marked)
1. Controlled regression testing: all factors other than code held constant (Rothermel 1997 Sec. 3.1.2).
2. Deterministic tests: no flaky tests, no test-order dependency (RTSCheck Sec. I; Luo abstract; Legunsen Sec. 1).
3. All dependencies observed: files, resources, reflection, and non-existent files attempted (Ekstazi Sec. 3.3); dynamic collection only sees one run.
4. Old revision's recorded dependencies describe the current baseline (Ekstazi: checksums from the previous run) - [inferred] consequence: stale dependency data makes the guarantee void.
5. Terminating tests with specified outputs and non-obsolete tests (Rothermel Sec. 3.1).

### Overhead and reported savings (numbers with locations)
- Ekstazi: AEC mean 68% of RetestAll across projects, 46% for long-running suites; slowdowns up to 138% on short suites (Sec. 4.3).
- ClassSRTS/Ekstazi: 62.5%-68.2% mean end-to-end (Legunsen Sec. 4.2.2); offline mode excludes collection time, online includes it.
- CI cloud: RTS full build time 76.0% of RetestAll (Shi 2019 abstract).
- NameRTS: -45.59% end-to-end time, 10.04% overhead, break-even about 5 commits (Sec. 4.3, abstract); EkstaP -3.10% time.
- STARTS: about 81.0% end-to-end (ASE 2017 abstract, [abstract-only]).
- Wang and Yu: static method-level RTS worse than RetestAll in 97.3% of Java projects (abstract).
- Take-away: RTS savings are roughly "halve long suites"; short suites can slow down. [inferred] For performance-edit loops, where benchmark time dominates test time, savings must be assessed against benchmark cost, not unit-test cost.

### Python support summary
| Tool/approach | Basis | Granularity | Safety evidence |
|---|---|---|---|
| pytest-testmon | coverage.py + block checksums | block/function, per test | reliability "same as coverage.py" (docs); no data-file/C-extension statement found |
| pytest-rts | coverage contexts + git diff | test function | NameRTS paper says not compared; no safety claim read |
| BabelRTS | regex file-level deps | file | safe on 76.6% of commits in NameRTS study |
| EkstaP (NameRTS baseline) | Ekstazi-style file deps | file | safe but reduces 3.10% time |
| NameRTS | name graph + pruning | function/element, test file | safe on 99.6% of 500 commits; misses via shared state, external callbacks |
| pytest --lf/--ff/--nf, pytest-picked | cache / git status | test | heuristics, not safe RTS |

---

## (c) Known unsafety causes and detection

| Cause | Source | Detection / mitigation in sources |
|---|---|---|
| Reflection | Legunsen Sec. 4.3 (commons-math, 9 missed tests); Shi OOPSLA 2019 [abstract-only] | dynamic tracking of reflective invocations (Ekstazi Sec. 3.3); NameRTS monkey-patches getattr (Sec. 3.4) |
| eval/exec, dynamic code | NameRTS Sec. 3.4, 5 (not tracked) | not handled; accept or force full run |
| Dynamic imports, plugin loading | NameRTS Sec. 4.2 (pylint via importlib; BabelRTS safe rate 48.00%) | initialization run to capture dynamic imports (EkstaP) |
| Implicit parent-package imports | NameRTS Sec. 4.2 (BabelRTS unsafe in matplotlib, safe rate 14.00%) | model `__init__.py` execution |
| Non-source files (config, data, resources) | Ekstazi Sec. 2 (files as dependencies); Shi 2019 Sec. I (class-level misses config changes; GIBstazi falls back to module level) | track files read; fall back to selecting everything affected when an untracked file changes |
| Native code / C extensions | [unknown] not found in any read source; coverage.py trouble page silent | [inferred] see (d) |
| External library callbacks | NameRTS Sec. 4.2 (docutils->sphinx) | library code not analyzed |
| Shared global state / test interference | NameRTS Sec. 4.2 (astroid.MANAGER); Luo F.10, Gruber (59% order dependency) | test isolation (NameRTS "isolator"), reorder tests (iDFlakies) |
| Non-determinism in collected dependencies | Legunsen Sec. 1 | repeat collection [inferred] |
| Flaky tests | Luo; Shi 2019 (38 of 39 missed failures flaky); RTSCheck assumes none | rerun failures; reordering (iDFlakies abstract); Gruber rerun estimate |
| Test-order dependence | Luo F.1/F.7/F.10; Parry Sec. 3.2 victim/brittle; Gruber 59% | reorder/rerun; RTS changes which tests run, so a brittle test can fail only because its state-setter was deselected [inferred] |
| Tool bugs | RTSCheck (27 bugs in 3 tools) | evolving-program rule checks |
| Changes in build/compile settings | Ekstazi Sec. 3.1 (executable can change when "compilation" changes) | checksum of executables |

Flakiness interplay: RTS reduces exposure to flaky failures by chance (Shi 2019) but flaky failures confound dependency collection and safety evaluation (RTSCheck excludes flaky tests by running each three times, Sec. on EvoEP subject setup).

---

## (d) Assumptions that may break under accumulated performance-motivated edits - all [inferred]

1. Behaviour-preserving intent vs observable change. Selection rules assume that a test not touching the changed code cannot change (controlled regression testing). A caching/memoization edit changes shared state and call counts; behaviour on inputs the covered tests never exercise (cache invalidation, thread safety, mutation of cached objects) is unobserved. Tests that import the module but do not cover the new code path are not selected, though a global cache object can alter their results.
2. C extension and Cython edits are invisible to coverage.py-based selection (source of "which Python lines ran") unless the .c/.pyx/.so file is itself a tracked dependency. testmon's block checksums are for Python source [read-in-source via fetch], so a .pyx edit selects nothing. File-level checksums of compiled artifacts (Ekstazi style) would catch it but select every test importing the extension, which for a core extension may be most tests.
3. Numerical tolerance changes. Replacing an algorithm (e.g., vectorizing, float32, reordering summation) alters floating-point results inside tolerance; tests with thresholds may flip only on rare inputs. Luo lists Floating Point Operations as a flaky-test cause (Sec. 3.1) and Gruber and Luo both show randomness as a cause; an RTS decision based on stale pass/fail results amplifies this.
4. Dependency-graph drift across many small edits. Each edit shifts which code each test touches (inlining, new helper modules, changed import structure). A dependency database recorded at revision k is only valid for k+1 if the previous edit's tests were rerun and re-recorded. With edits applied without recording (reduced runs record only selected tests), the database for unselected tests ages. testmon and Ekstazi re-record only for executed tests [read-in-source: Ekstazi collection phase "for the executed test entities", Sec. 3.3].
5. Stale baseline for selection. Selection against "last full run" vs "last accepted edit" differ; if an accepted edit's reduced test set skipped test T, and the next edit also does not touch T's recorded dependencies, T never reruns although the accumulated diff may have crossed its dependencies indirectly (non-transitive recording: recorded dependencies are from a run before several edits). NameRTS pruning relies on prior-execution observations remaining valid until a modified element is reached (Sec. 5) - a safe argument per edit that does not obviously compose across unrecorded edits.
6. Performance edits often touch import-time/global code (precomputed tables, lazy imports, module-level caches). In Python, such edits make every test importing the module "affected" (NameRTS Sec. 4.2: global-code changes select all tests, e.g., matplotlib `_get_executable_info`). Reduced test sets may collapse to the full set for exactly the edits we want to speed up.
7. Time-sensitive tests and benchmarks: tests with timeouts (Luo's Async Wait / Time) may become flaky or pass/fail differently after an edit changes timing, independent of code dependencies.
8. Order dependence amplified by selection: caching edits introduce new inter-test state (cache survives across tests); a deselected test may be the one that previously reset it.
9. Environment inputs (installed package versions, NumPy build, CPU flags, env vars, random seeds) are outside source-level checksum tracking - Ekstazi tracks files read via instrumentation only in Java; no equivalent evidence for Python tools was found.
10. Safety measured against ground truth that is itself instrumented-function-call-based (NameRTS ground truth, Sec. 4.1) captures calls but not implicit semantic effects (shared state changed by a function that the test never calls).

---

## (e) Candidate deterministic rules, each traced to sources

R-F1. File-level dynamic dependency selection with checksums. Record, per test, the set of files (Python modules, data files, extension binaries) accessed in one instrumented run; select a test iff any recorded file's checksum changed. Sources: Ekstazi Sec. 2-3. Python caveat: eager imports make file-level selection weak (NameRTS Sec. 4.2: 3.10% time reduction), so use at module-package level only as the safe fallback.

R-F2. Function-level dependency selection (testmon-style block checksums) as the default for Python-only edits; fall back to F1 when the changed file is global/import-time code. Sources: testmon docs (blocks, checksums, coverage.py); NameRTS Sec. 4.2 (import-time code selects all).

R-F3. Always-run set for non-Python/native inputs. If an edit touches any file that the selector does not track (.c, .pyx, .pxd, setup/build config, pyproject, data/fixture files, environment pins), run every test that imports the changed extension or, if the dependency map is not available for that file, the full suite. Sources: Ekstazi Sec. 2 (files as dependencies); Shi 2019 Sec. I (class-level misses config changes; hybrid defaults to module-level); testmon/coverage.py silence on C extensions ([unknown] -> must be assumed unsafe).

R-F4. Re-collect dependencies after every k accepted edits (and after any edit that touches import-time code or build files), by rerunning the full suite once under the recorder. k to be set from the measured safety loss on a ground-truth experiment; NameRTS reports break-even after about five commits (Sec. 4.3) and a per-commit unsafe rate of 0.4% (2/500). Sources: Ekstazi Sec. 5 discussion (dependencies from observed run only); NameRTS Sec. 4.2-4.3, Sec. 5.

R-F5. Execution-window rule (cheap history-based guard against staleness): also select any test that has not run within window We edits, any test that failed within the failure window Wf, and any new test. Source: Elbaum et al. Sec. 4.1 Algorithm 1 SelectPRETests.

R-F6. Always include tests that were failing or flaky-labelled on the baseline run when comparing outcomes; treat a failure as real only if it reproduces on rerun and is not in a known-flaky set. Sources: Luo (flaky cause breakdown); Shi 2019 (38/39 missed failures were flaky); Parry survey (rerun practice); Gruber (rerun estimate).

R-F7. Isolation check on reduced runs: run selected tests in randomized or reversed order at least once per k edits; any outcome change relative to the original order flags order dependence. Sources: iDFlakies (reordering), Parry Sec. 3.2, Gruber (59% order dependence in Python).

R-F8. Validate the selector itself, not just the code: replay an evolving sequence of revisions, flag (1) a newly failing test under RetestAll that the selector did not choose (safety), (2) any selection on a second run of an unchanged revision (precision), (3) end-to-end selector time vs RetestAll time (efficiency). Source: RTSCheck Sec. I rules (safety, precision, efficiency report).

R-F9. Compute the stop-condition on end-to-end time, including collection overhead: do not adopt RTS for a test set whose suite is short (< ~1 minute) since Ekstazi slowed projects with short suites (Sec. 4.3; Wang and Yu 2018 findings). Report offline vs online time explicitly (Legunsen Sec. 4.2.2).

R-F10. Prioritization (not reduction) as a safety net: when the full suite is too costly, run it after the reduced set in failure-first order (`pytest --ff`/`--lf`, pytest cache docs) and treat reduced pass as provisional. Sources: pytest cache docs; Elbaum et al. (prioritize post-submit). APFD-based comparison is [unknown] here (not source-verified).

Later AI study (not part of this method): learned predictive selection (Machalica et al.; Zhang et al. AST 2022 combining ML and analysis-based RTS, A9).

---

## (f) Search log (all on 2026-11-21)

Engine: WebSearch tool (general web search, US-only; no scholarly-database API). WebFetch for pages.

| # | Query / action | Engine | Notable hits | Looked for / not found |
|---|---|---|---|---|
| 1 | Ekstazi practical RTS dynamic file dependencies ISSTA 2015 pdf | WebSearch | users.ece.utexas.edu/~gligoric/papers (dissertation, abstracts), par.nsf.gov | Found author-hosted PDF later via direct URL guess GligoricETAL15Ekstazi.pdf; typeset.io copy rejected (not a legitimate host) |
| 2 | regression test selection Python empirical study arXiv | WebSearch | arXiv 2605.25356 NameRTS; core.ac.uk Kauhanen; Gyori ISSRE 2018 (Java) | Python RTS research: found NameRTS (2026) and pytest-rts (Helsinki). No other Python-specific empirical RTS paper found |
| 3 | pytest-testmon how it works fingerprints coverage.py | WebSearch | PyPI versions, testmon.org | "fingerprint" term: docs use "checksum of block" |
| 4 | Shi Reflection-aware static RTS OOPSLA 2019 pdf | WebSearch | par.nsf.gov biblio/10603280, ideals 107148, bibtex.github.io | PDF not retrievable (HTML responses); metadata only |
| 5 | Zhu Legunsen Shi Gligoric "A framework for checking RTS tools" ICSE 2019 | WebSearch | cs.cornell.edu/~legunsen PDF | downloaded |
| 6 | Luo Hariri Eloussi Marinov An empirical analysis of flaky tests FSE 2014 pdf | WebSearch | huang.isis.vanderbilt.edu course copy | downloaded (course host copy) |
| 7 | Zhang "Hybrid regression test selection" ICSE 2018 HyRTS pdf | WebSearch | experts.illinois.edu, par.nsf.gov 10175678 (turned out to be the Shi CI paper) | HyRTS PDF not found; abstract only |
| 8 | Parry Kapfhammer Hilton McMinn A survey of flaky tests TOSEM 2021 | WebSearch | o-parry.github.io/papers/2021a.pdf | downloaded |
| 9 | Elbaum Rothermel Penix techniques improving regression testing CI FSE 2014 | WebSearch | cs.uwaterloo.ca course copy, research.google | downloaded course copy |
| 10 | Rothermel Untch Chu Harrold Prioritizing test cases TSE 2001 APFD | WebSearch | typeset.io, Scribd, academia.edu, digitalcommons.unl.edu/csearticles/9 | guessed UNL download URL returned HTML; APFD paper NOT obtained |
| 11 | Lam et al. iDFlakies ICST 2019 | WebSearch | par.nsf.gov/biblio/10101224, cs.gmu.edu author page (blocked) | downloaded from PAR |
| 12 | Gruber Python flaky tests ICST 2021 | WebSearch | arXiv 2101.09077 | downloaded |
| 13 | Machalica Predictive test selection ICSE-SEIP 2019 | WebSearch | arXiv 1810.05286 | not downloaded (later AI item) |
| 14 | Yoo Harman regression testing survey STVR 2012 | WebSearch | KAIST DSpace record; 2007 preprints | published version OA not found |
| 15 | Harrold et al. RTS for Java software OOPSLA 2001 | WebSearch | utdallas course PDF, gatech paths | download returned HTML; DejaVOO identification unresolved |
| 16 | WebFetch testmon.org/blog/determining-affected-tests/ | WebFetch | blocks, checksums, "no heuristics" | data files/C extensions: not covered |
| 17 | WebFetch pypi.org/project/pytest-testmon/ | WebFetch | beta, Python >= 3.11, CI opt-in | limitations: none |
| 18 | WebFetch coverage.readthedocs.io/en/latest/trouble.html | WebFetch | exec, thread, settrace | C extensions: not in this page |
| 19 | WebFetch docs.pytest.org/en/stable/how-to/cache.html | WebFetch | --lf/--ff/--nf/--sw/--lfnf/--cache-clear | |
| 20 | WebFetch github.com/anapaulagomes/pytest-picked | WebFetch | git status based selection | no limitations section |
| 21 | WebFetch github.com/tarpas/pytest-testmon | WebFetch | README overview only | limitations absent |
| 22 | WebFetch testmon.org/docs/ | WebFetch | HTTP 404 | |
| 23 | BabelRTS polyglot RTS Maurina Cazzola Ghosh | WebSearch | only a reference-list mention; TUM multi-language RTS (Elsner ICSE-SEIP 2022 snippet) | BabelRTS paper not found |
| 24 | STARTS ASE 2017 tool demonstration | WebSearch | dblp, bibtex.github.io | metadata only; PDF not downloaded |
| 25 | pytest-rts coverage-based RTS Python tool paper | WebSearch | PyPI pytest-rts, core.ac.uk 479167931 | CORE PDF blocked (403/HTML); venue unknown |
| 26 | WebFetch core.ac.uk/download/479167931.pdf | WebFetch | HTTP 403 | |
| - | curl attempts: guessed OA URLs for Reflection-aware RTS (3), Harrold OOPSLA (2), Orso FSE04, Rothermel TSE 2001 (UNL) | curl | all returned HTML | not retrieved |

Not searched / not found (explicit gaps):
- "PyRTS", "regression test selection Cython/C extension", "pytest-testmon unsafe/missed data files" - not searched as separate queries; no Python RTS paper beyond NameRTS and pytest-rts was found.
- No source read on how any Python RTS tool treats C extensions, Cython modules, data files, environment changes.
- TSE 1996 Rothermel and Harrold framework paper and TSE 2001 Rothermel prioritization (APFD) not obtained.
- Gligoric et al. "Regression test selection for distributed software histories" and RTS surveys beyond Yoo and Harman not searched.
- Machalica/Meta: only abstract-level via search; later AI study.
