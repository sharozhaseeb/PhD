# T4 - Evaluating the safety of test/benchmark selection and reduced validation

Researcher: T4. Date: 2026-11-21. Study context: Python code optimized by many small performance-motivated edits; each edit validated with a deterministic REDUCED build + REDUCED test/benchmark set; periodic full checks. No AI in the method.

Evidence labels: [read-in-source] = I read the text of the PDF/page (section/page given); [abstract-only] = only abstract/search snippet/landing page seen; [inferred] = my reasoning; [unknown] = not found.

Corrections to the brief (verified against sources):
- "Analyzing regression test selection techniques" (Rothermel & Harrold, TSE 1996): the PDF I could obtain from a legitimate host (cs.purdue.edu course page, `p173-rothermel.pdf`) is actually **"A Safe, Efficient Regression Test Selection Technique" (ACM TOSEM 6(2), Apr 1997)**, not the TSE 1996 paper. Its Sec. 4.1 summarizes the four-category framework and cites the TSE paper as "Rothermel and Harrold [1996]". The TSE 1996 text itself was NOT read. Existing file renamed accordingly.
- Shi et al. ISSTA 2018 authors are Shi, Gyori, Mahmood, Zhao, Marinov (not Gligoric/Groce). Title: "Evaluating Test-Suite Reduction in Real Software Evolution", pp. 84-94.
- RTSCheck (ICSE 2019) authors: Zhu, Legunsen, Shi, Gligoric - correct. [abstract-only + read]
- "Commit-aware mutation testing" (ICSME 2020): authors are Ma, Laurent, Ojdanic, Titcheu Chekam, Ventresque, Papadakis (not "Ma, Kim, Lee"). [abstract-only]
- "Performance mutation testing" (STVR 2021): authors Delgado-Perez, Sanchez, Segura, Medina-Bulo (not Dominguez-Jimenez). [abstract-only]
- RegMiner is by Song, Lin, Ng, Wu, Peng, Dong, Mei (ISSTA 2022), Java only; not Zhu/Legunsen/Shi/Gligoric.
- "Lima? Performance mutation operators", "PyPerf bugs", and "An empirical study of performance issues in Python" as titled: NOT found as such. The closest real items are Zhao et al. TSE 2022 (570 issues, Java/C++/Python) and PerfCurator (arXiv 2406.11731, mined perf-bug commits; abstract-only). Dropped the unverified titles.
- Mostafa et al. "PerfRanker" is ISSTA 2017 (verified), cited by Laaber et al. for APFD-P.

---------------------------------------------------------------------
## (a) Source cards

Format: Citation | Access | Claims [label] (section/page)

### A1. RTS evaluation frameworks and metrics

**Rothermel & Harrold, "A Safe, Efficient Regression Test Selection Technique", ACM TOSEM 6(2), 1997.** File: `papers/1997-Rothermel-Safe-Efficient-RTS-TOSEM.pdf` (downloaded). 
- Four evaluation categories: inclusiveness (extent to which a technique selects tests that reveal faults in the modified program; "a 100% inclusive technique is safe"), precision (extent it omits tests that cannot reveal faults), efficiency (space and time requirements, "focusing on critical-phase costs"), generality (ability to work in a practical, wide range of situations). [read-in-source] Sec. 4.1, pp. 194-195 (text near "analysis framework that consists of four categories").
- Safe selection holds only for "controlled regression testing" (same environment/inputs/determinism assumptions); "safe test selection is possible only for controlled regression testing". [read-in-source] Sec. 4.1, p. 195.
- Safe and 100% precise is impossible: identifying exactly the fault-revealing tests is undecidable. [read-in-source] Sec. 4.1, p. 195.
- The original framework paper (TSE 1996) is only cited here. [read-in-source that it is cited; its text unread]

**Gligoric, Eloussi, Marinov, "Practical Regression Test Selection with Dynamic File Dependencies" (Ekstazi), ISSTA 2015, pp. 211-222.** Read from existing file `papers/2015-Ekstazi-ISSTA.pdf` (saved by another researcher; not re-downloaded). DOI 10.1145/2771783.2771784 [abstract-only via search].
- RTS has three phases: Analysis (A), Execution (E), Collection (C). "Most research has evaluated RTS techniques based on the number of selected tests, i.e., implicitly based on the time only for the E phase; a few papers ... measure only A and E phases, ignoring the C phase." The authors argue for **end-to-end time** "from initiating the test-suite execution for a new code revision until all test outcomes become available". [read-in-source] Sec. 1 (Introduction), the paragraph on end-to-end time.
- Requirement for adoption: average end-to-end time shorter than running all tests (RetestAll). [read-in-source] Sec. 1.
- Evaluation protocol: for each revision run three scenarios - RetestAll, AEC (with collection), AE (without collection); time measured as the developers' own build command (e.g., `mvn test`), so fixed build overhead is included; revisions that do not build are skipped. [read-in-source] Sec. 5 (Evaluation setup, Fig. 5 legend: e%, m%, tAEC, tAE).
- Abstract result (32% average end-to-end saving, 54% for longer suites; 615 revisions of 32 projects). [read-in-source in abstract text]
- Safety argued by reduction to proven safety of class-dependency RTS; method-granularity dependencies "unsafe" in the simplified description. [read-in-source] Sec. 2-3.

**Legunsen, Hariri, Shi, Lu, Zhang, Marinov, "An Extensive Study of Static Regression Test Selection in Modern Software Evolution", FSE 2016, pp. 583-594.** Read from existing file `papers/2016-StaticRTS-Legunsen-FSE.pdf` (another researcher's; not re-downloaded). DOI 10.1145/2950290.2950361 [abstract-only via search].
- Defines **safety violation** and **precision violation** against a safe baseline (Ekstazi): with E = tests selected by Ekstazi, T = tests selected by technique X on a revision, safety violation = |E \ T| / |E union T|, precision violation = |T \ E| / |E union T|; reported per project as % of revisions with a violation plus min/max/avg. [read-in-source] Sec. 4.2.3 (RQ3), Table 3.
- Results: ClassSRTS unsafe in 0.2% of revisions on average (2 of 22 projects); method-level static RTS unsafe in 10.6% of revisions (14 projects). [read-in-source] Sec. 4.2.3.
- Offline vs online modes: offline mode excludes the closure-computation and graph-update cost from end-to-end time; online counts them. [read-in-source] Sec. 3 (Implementation).
- Causes of safety violations: reflection; excluding third-party libraries from call-graph analysis. [read-in-source] Sec. 4.3.
- "Any RTS technique can be simply made faster by not selecting to run some tests, but then it risks missing regressions" and RTS is not worthwhile for projects whose tests run under about 5 s. [read-in-source] Sec. 4.2.2/4.2.3.
- Note: the oracle for "safe" here is another tool (Ekstazi), not ground-truth fault detection. [read-in-source, Sec. 4.2.3 says Ekstazi is "a fairly safe and precise" baseline]

**Zhu, Legunsen, Shi, Gligoric, "A Framework for Checking Regression Test Selection Tools" (RTSCheck), ICSE 2019, pp. 430-441.** File `papers/2019-Zhu-RTSCheck-ICSE.pdf` (downloaded). DOI 10.1109/ICSE.2019.00056 [abstract-only via search].
- Motivation: analytical safety proofs "may not carry over to the RTS tools that implement those techniques"; tools can have bugs. [read-in-source] Sec. I.
- Seven rules (Table I): R1 (safety) "number of newly failed tests with the tool is lower than with RetestAll"; R2 (safety) tool selects zero tests while all other tools select all; R3-R5 precision; R6-R7 generality. R1 assumes no flaky tests and no test-order dependence. [read-in-source] Sec. III-A, Table I.
- Three sources of evolving programs: AutoEP (generated programs + Randoop tests + evolution operators akin to mutation operators), DefectsEP (Defects4J buggy/fixed revisions **reversed** so the fix-to-bug transition is a "regression" that a failing test must be selected for), EvoEP (real revision sequences). [read-in-source] Sec. III-B..D.
- Found 27 bugs in Clover, Ekstazi, STARTS. [read-in-source, Sec. I contribution list / abstract]

**Shi, Gyori, Mahmood, Zhao, Marinov, "Evaluating Test-Suite Reduction in Real Software Evolution", ISSTA 2018, pp. 84-94.** File `papers/2018-Shi-Test-Suite-Reduction-Real-Evolution-ISSTA.pdf` (downloaded). DOI 10.1145/3213846.3213875 [abstract-only via search].
- Defines **Failed-Build Detection Loss (FBDL)**: if F is the set of future failed builds and F_r those in which the reduced suite detects all the faults the original suite detects, FBDL = (|F| - |F_r|) / |F| x 100. [read-in-source] Sec. 3.
- Because a CI failed build may contain multiple faults, they propose a Failure-to-Fault Map (FFMap) and classify builds (DefMiss, LikelyMiss, SamePack, ...). [read-in-source] Sec. 1, 3.2.
- Data: 1478 failed builds from 32 GitHub/Travis projects. FBDL "up to 52.2%" (as stated in the text); traditional TSR metrics (suite-size reduction, mutation/fault loss) "are not good predictors of FBDL"; proposed predictor "historical FBDL" is better but "still not highly reliable". An "oracular" reduced suite of only future failing tests is on average ~20% of original size. [read-in-source] Sec. 1 and the results sections.
- Reduced suite is computed at a "reduction point" and evaluated on FUTURE failed builds; new tests added later are all kept. [read-in-source] Sec. 3.
- Lesson for us: evaluate reduction by replaying future history from a checkpoint, not by synthetic mutants only. [inferred from the above]

**Shi et al., "Balancing Trade-Offs in Test-Suite Reduction", FSE 2014.** (Author list not verified against the PDF header: [unknown].) File `papers/2014-Shi-Balancing-Tradeoffs-Test-Suite-Reduction-FSE.pdf` (downloaded; re-downloaded after a truncated first copy).
- Standard metrics: SizRed = (|O| - |R|)/|O| x 100 and MutLoss = (|mut(O)| - |mut(R)|)/|mut(O)| x 100 (loss in fault-detection capability measured with killed mutants). [read-in-source] Sec. 3 (metric definitions).
- Proposes evolution-aware metrics that evaluate the reduced suite on later versions; 18 projects, 261,235 tests. Statement/branch-coverage reduction loses up to 20.5% killed mutants; reduction on killed mutants has no loss but 11.9 percentage points larger suites. [read-in-source] Sec. 1 (as printed in the text).
- "Fault detection loss" thus = fraction of faults (mutants) detected by full suite but missed by reduced suite. [read-in-source]

### A2. Mutation analysis as a proxy for real faults

**Just, Jalali, Inozemtseva, Ernst, Holmes, Fraser, "Are Mutants a Valid Substitute for Real Faults in Software Testing?", FSE 2014, pp. 654-665.** File `papers/2014-Just-Mutants-Valid-Substitute-FSE.pdf` (downloaded). DOI 10.1145/2635868.2635929 [read-in-source in file].
- 357 real faults, 5 Java programs (321,000 LOC), ~230,000 mutants; developer-written and generated tests. [read-in-source] Sec. 1, abstract.
- RQ1/RQ2/RQ3: coupling of real faults to mutants, which faults are not coupled, correlation of mutant detection with real-fault detection. [read-in-source] Sec. 1.
- "Coupling effect for 73% of real faults"; "10% of real faults require a new or stronger mutation operator"; "17% of real faults are not coupled to mutants"; correlation between mutant detection and real-fault detection is statistically significant and stronger than statement coverage's. [read-in-source] Sec. 1 contributions list.
- Threat for us: Java, non-performance faults, one-bug-at-a-time version pairs. [inferred]

**Andrews, Briand, Labiche, Namin, "Using Mutation Analysis for Assessing and Comparing Testing Coverage Criteria", IEEE TSE 32(8), 2006, pp. 608-624** (journal extension of the ICSE 2005 paper). File `papers/2006-Andrews-Mutation-Coverage-Criteria-TSE.pdf` (downloaded). The ICSE 2005 PDF ("Is mutation an appropriate tool for testing experiments?", pp. 402-411, DOI 10.1145/1062455.1062530 [abstract-only via DBLP snippet]) could not be downloaded (host returned HTML).
- Finding: on one industrial-size program (space.c) with real faults, "use of mutation operators is yielding trustworthy results: Generated mutants can be used to predict the detection effectiveness of real faults". [read-in-source] Abstract.
- Threat: "only one program with real faults was used" - external validity. [read-in-source] Sec. 4 threats paragraph (~p. 620).
- Hand-seeded faults in earlier studies were harder to detect than real ones (discussion of Hutchins et al.). [read-in-source] Sec. 4.
- Conclusion about the ICSE'05 paper itself: [abstract-only] (search snippet: mutants appear to be different from hand-seeded faults, which seem harder to detect than real faults).

**Papadakis, Kintis, Zhang, Jia, Le Traon, Harman, "Mutation Testing Advances: An Analysis and Survey", Advances in Computers vol. 112, 2019.** File `papers/2019-Papadakis-Mutation-Testing-Advances-AdvComp.pdf` (authors' preprint; downloaded). (Year 2018 vs 2019 differs between repository entries.)
- Equivalent-mutant detection is undecidable; heuristics only. [read-in-source] Sec. 5.3.1.
- Redundant/subsumed mutants "inflate the mutation score ... skewing the measurement"; mutation-score overestimation "as high as 10%" in a cited study. [read-in-source] Sec. 5.3.2.
- Mutant sampling / selective mutation evaluated with plain mutation scores are vulnerable to the "subsumed mutant threat"; reduction techniques perform poorly when judged against subsuming mutants (Kurtz et al.). [read-in-source] Sec. 5.1 (mutant reduction).
- Mutation score as an indicator of fault revelation depends on equivalent/redundant mutants; "we know very little" about confidence from mutation score. [read-in-source] Sec. 9 area ("mutation score vs fault revelation").
- Test-suite reduction / prioritisation with mutation, strong vs weak mutation. [read-in-source] sections on test reduction/prioritisation.
- Python is mentioned in the tool table only; no Python-specific operator study found. [inferred from the greps; not exhaustively read]

**Petrovic & Ivankovic, "State of Mutation Testing at Google", ICSE-SEIP 2018, pp. 163-171.** File `papers/2018-Petrovic-State-Mutation-Testing-Google-ICSESEIP.pdf` (downloaded). DOI 10.1145/3183519.3183521 [abstract-only via search].
- Diff-based, probabilistic: for each changed line at most one mutant; operator chosen at random from applicable ones; incremental coverage used to restrict mutated lines. [read-in-source] Sec. 3.
- Operators AOR, LCR, ROR, SBR, UOI; supports Python among 7 languages. [read-in-source] Sec. 3.
- "Arid node" heuristic suppresses mutation in uninteresting statements (logging etc.). [read-in-source] Sec. 4.
- Dataset: 1,159,723 mutants; 72,425 diffs; >87% of mutant runs killed; **Python mutants have the highest survival rate (14.7%)**; SBR (statement deletion) is ~72% of mutants; 75% of findings with feedback marked useful. [read-in-source] Sec. 5.
- Developer-feedback usefulness is the main efficacy measure at Google, not mutation score. [read-in-source] Sec. 5.4.

**Ma, Laurent, Ojdanic, Titcheu Chekam, Ventresque, Papadakis, "Commit-Aware Mutation Testing", ICSME 2020, DOI 10.1109/ICSME46990.2020.00045.** [abstract-only via search snippet; not downloaded (core.ac.uk returned HTML)].
- Defines commit-relevant mutants (interaction between modified and unmodified code); standard mutation scores correlate weakly (0.15-0.4) with a commit-relevant score. [abstract-only, unverified numbers from a search summary]

**Ojdanic, Soremekun, Degiovanni, Papadakis, Le Traon, "Mutation Testing in Evolving Systems: Studying the relevance of mutants to code evolution", arXiv 2112.14566 (Dec 2021).** [abstract-only via WebFetch of the arXiv abstract page].
- >10 million mutants, 288 commits, 5 projects; commit-relevant mutants are "located mainly outside of program commit change (81%)". [abstract-only]
- IMPORTANT for our design: mutants restricted to changed lines under-represent mutants that matter for a change. (The "69%" I saw in one search snippet is unverified and conflicts; use 81% only with the abstract-only label.)

**Python mutation tools (documentation).**
- mutmut (github.com/boxed/mutmut, README fetched). [read-in-source: README]. Mutates only functions that are called; incremental runs re-test only mutants in functions whose source changed; `mutate_only_covered_lines`; runs only relevant tests per mutant using stats from a coverage-like collection run; `max_stack_depth` trades locality vs missed mutants; `only_mutate`/`do_not_mutate`, `# pragma: no mutate`; mutmut 3+ requires `fork` (POSIX; Windows only via WSL); mutmut 2 can mutate code outside functions.
- Cosmic Ray (cosmic-ray.readthedocs.io concepts page fetched). [read-in-source: docs page]. Session DB (resumable), operators as plugin classes, `timeout` -> "incompetent" mutants, `excluded-modules`; page does NOT describe a git-diff-based filter or baseline run.
- Mutatest (mutatest.readthedocs.io) [abstract-only via search]: mutates cached bytecode/AST, random sampling mode, "diagnostic tool, not something you would run in your CICD pipeline", docs list Python 3.7/3.8 (dated).
- Implication: none of the three documents a performance-aware operator set or a change-restricted mode out of the box except mutmut's function-level incremental behaviour. [inferred]

### A3. Performance regression / fault injection and real performance-bug data

**Delgado-Perez, Sanchez, Segura, Medina-Bulo, "Performance mutation testing", Softw. Test. Verif. Reliab. 31(5), e1728, 2021 (online 2020), DOI 10.1002/stvr.1728.** [abstract-only via search snippets of the IDUS record; PDF not retrievable (CORE returned HTML, IDUS 403)].
- Applies mutation testing to PERFORMANCE tests; proposes seven performance mutation operators from classical performance-bug patterns; proof of concept on C++ programs, mixing traditional and performance operators. [abstract-only]
- [unknown]: whether any operators transfer to Python; operator list not read.

**Reichelt, Kuehne, Hasselbring, "Automated Identification of Performance Changes at Code Level" (Peass), arXiv 2303.14256 (2023).** File `papers/2023-Reichelt-Peass-Injected-Regressions-Jetty-arXiv.pdf` (downloaded). [read-in-source]
- Injection method: 1,000 Jetty commits, each with one artificial regression made by "randomly inserting busy waiting" of 5 ns (about two `System.nanoTime` calls) into a method called by a randomly selected benchmark. [read-in-source] Sec. IV (Evaluation), (a) Implementation.
- Result: 58.7% of injected changes detected by transformed unit tests; 26.7% missed because unit-test standard deviation too high relative to the injected regression; 14.6% not covered by unit tests; vs 3.2% for Jetty's own JMH benchmarks (per search summary; the main text compares). [read-in-source] Sec. IV.
- Threats: results on artificial regressions may not generalize (e.g., regressions only under parallel use); false alarms cannot be studied because there is no ground truth for relevant regressions. [read-in-source] Sec. IV-C Threats to Validity.
- Detection config analysis uses F1-score, target Type I and Type II below 1% (one false positive/negative in 100 measurements) and controllable-effect-size artificial workloads. [read-in-source] Sec. III.

**Laaber, Gall, Leitner, "Applying test case prioritization to software microbenchmarks", Empirical Software Engineering 26(6):133, 2021.** File `papers/2021-Laaber-TCP-Microbenchmarks-EMSE.pdf` (**this filename already existed from another researcher; my curl overwrote it with the Chalmers open-access copy of the same paper - see report note**). DOI 10.1007/s10664-021-10037-x [abstract-only via search].
- Ground truth is REAL performance changes between adjacent versions measured by running all benchmarks in all versions (JMH, 10 warmup/20 measurement iterations as configured; bootstrap confidence intervals on the ratio of means; regression if lower CI bound > 1). [read-in-source] Sec. 4.4-4.5, Fig. 6.
- Metrics: APFD-P (adapted from APFD; values 0-1; accounts for size of performance change, via Mostafa et al. 2017) and Top-N (number of benchmarks that must run to capture the N largest changes). Best techniques APFD-P 0.54-0.71, top-3 captured after 29-66% of suite; most effective technique's overhead ~11% of suite time. [read-in-source] Sec. 1, 4.4.
- RQ2: effectiveness depends on the change-size threshold (APFD-P differs by a median of 0.11-0.28). [read-in-source] Sec. 1.
- No injection: real changes only. [inferred from reading; grep for "inject" found none]

**Mostafa, Wang, Xie, "PerfRanker: Prioritization of Performance Regression Tests for Collection-Intensive Software", ISSTA 2017, pp. 23-34, DOI 10.1145/3092703.3092725.** File `papers/2017-Mostafa-PerfRanker-ISSTA.pdf` (already existed from another researcher; my curl overwrote with the author-page copy). [abstract-only via search; APFD-P definition attributed to it by Laaber et al. - read-in-source in Laaber Sec. 4.4]

**Kalibera & Jones, "Quantifying Performance Changes with Effect Size Confidence Intervals", Univ. of Kent TR 4-12 (2012; arXiv 2007.10899 posted 2020).** File `papers/2013-Kalibera-Quantifying-Performance-Changes-TR-arXiv.pdf` (downloaded). Also "Rigorous Benchmarking in Reasonable Time", ISMM 2013 (pp. 63-74; file from another researcher).
- Review of 122 papers; 65 quantified a change as a ratio of execution times; proposes a statistical model and an effect-size confidence interval for the ratio of means. [abstract-only + read of abstract text in file] (T3 covers this in depth.)

**Jin, Song, Shi, Scherpelz, Lu, "Understanding and Detecting Real-World Performance Bugs", PLDI 2012, pp. 77-88, DOI 10.1145/2254064.2254075.** File `papers/2012-Jin-Real-World-Performance-Bugs-PLDI.pdf` (downloaded).
- 109 randomly sampled fixed performance bugs from Apache, Chrome, GCC, Mozilla, MySQL (ACM abstract says 110; the PDF says 109). [read-in-source] Abstract/Sec. 2.
- Performance bugs defined as defects where "relatively simple source-code changes can significantly speed up software, while preserving functionality". [read-in-source] Sec. 1.
- "Two thirds" of bugs introduced by wrong understanding of workload or API performance; "more than one quarter" arise from previously correct code due to workload or API changes. [read-in-source] Sec. 1.2 findings (guidance for bug avoidance).
- Not Python; C/C++/JS. [read-in-source]

**Zhao, Xiao, Bondi, Chen, Liu, "A Large-Scale Empirical Study of Real-Life Performance Issues in Open Source Projects", IEEE TSE 2022, DOI 10.1109/TSE.2022.3167628.** File `papers/2022-Zhao-Real-Life-Performance-Issues-TSE.pdf` (NSF PAR manuscript; downloaded).
- 570 issues from 13 projects: the paper text says Java 192, **Python 162**, C/C++ 216 (search summaries disagreed on the Python/C++ counts; the paper text governs). [read-in-source] Sec. 1 (extension paragraph).
- RQ3.1: "only a small portion (15%) involve test code revisions" (Java 27%, Python 13%, C++ 6%); design-level optimizations more likely to revise tests. [read-in-source] Sec. 5 (RQ-3.1 results).
- Implication: most real performance-optimization commits come with NO new tests, so selection must rely on existing tests. [inferred]
- A dataset on Zenodo (record 6383167) [abstract-only via search]. PerfCurator (arXiv 2406.11731) mined ~114K Python performance-fix commits [abstract-only via search].

### A4. Datasets for replay evaluation

**Defects4J: Just, Jalali, Ernst, ISSTA 2014 tool demo, pp. 437-440, DOI 10.1145/2610384.2628055.** [abstract-only via search snippets]. 357 bugs from 5 Java programs initially (395 in later release per search snippet). Java only. Used by RTSCheck's DefectsEP via reversal of buggy/fixed (read-in-source in Zhu Sec. III-C).

**BugsInPy: Widyasari et al., ESEC/FSE 2020 tool demo, DOI 10.1145/3368089.3417943.** File `papers/2024-Widyasari-BugsInPy-arXiv.pdf` (arXiv v1). [read-in-source] 
- 493 real bugs from 17 Python projects; each bug requires: bug in source code (not config/docs/tests), reproducible (a test from the FIXED version fails on the faulty version), and isolated (faulty and fixed differ only by the fix). [read-in-source] Sec. 2 (criteria 1-3).
- Not performance bugs; functional faults. [inferred from criteria]
- (Later counts, e.g. 501 bugs, appear in other papers; [abstract-only].)

**RegMiner: Song et al., ISSTA 2022.** File `papers/2022-Song-RegMiner-ISSTA.pdf` (arXiv v2). [read-in-source]
- Regression defined as a test passing at the regression-fixing commit (rfc) and at the working commit (ric-1) and failing at the regression-inducing commit (ric). Closed-world: precision 100%, recall 56% (50 regressions + 50 non-regressions); open world: 147 repos, 1,035 regressions (Java, Maven/Gradle). [read-in-source] Sec. 3, 5.1. Java only.

**TravisTorrent: Beller, Gousios, Zaidman, MSR 2017, pp. 447-450.** [abstract-only via search]. 2,640,825 Travis builds linked to GitHub commits. CI history for replay; Java/Ruby-heavy.

**RTPTorrent: Mattis, Rein, Duersch, Hirschfeld, MSR 2020, DOI 10.1145/3379597.3387458.** File `papers/2020-Mattis-RTPTorrent-MSR.pdf` (downloaded). [read-in-source]
- 20 open-source Java projects, >100,000 real Travis build logs; per job and test: counts of failures/errors/skipped and the test's execution index; links to TravisTorrent/GHTorrent via job/commit IDs. Created because most RTP evaluations use controlled environments or synthetic test runs (threat to ecological validity). [read-in-source] Sec. 1, 3.
- Java only; designed for prioritization, but usable for selection replay since failure per test per build is present. [inferred]

---------------------------------------------------------------------
## (b) Synthesis

### b1. Metrics: definitions and where defined

| Metric | Definition | Source | Label |
|---|---|---|---|
| Inclusiveness / safety | Extent to which selection includes tests that reveal faults; 100% inclusive = safe. Safe selection requires "controlled regression testing". | Rothermel & Harrold 1997 Sec. 4.1 (cites TSE 1996) | [read-in-source] |
| Precision | Extent to which tests that cannot reveal faults are omitted; safe and 100% precise is undecidable | same | [read-in-source] |
| Efficiency | Space/time of the technique, focusing on critical-phase costs | same | [read-in-source] |
| Generality | Works in practical, wide range of situations | same | [read-in-source] |
| Safety violation rate (vs reference tool) | |E \ T| / |E union T| per revision; also % of revisions with any violation | Legunsen 2016 Sec. 4.2.3 | [read-in-source] |
| Precision violation | |T \ E| / |E union T| | same | [read-in-source] |
| Missed newly failed tests | # newly failed tests with tool < # with RetestAll (R1) | Zhu 2019 Table I | [read-in-source] |
| Selection ratio | % of tests selected relative to RetestAll (e%, c%) | Gligoric 2015 Fig. 5; Legunsen Fig. 3 (avg 20.6%/29.4%/43.8% for Ekstazi/ClassSRTS/MethSRTS) | [read-in-source] |
| End-to-end time | Time from starting test execution for a revision to all outcomes available: A + E + C (+ build). Report AEC and AE separately; normalise by RetestAll | Gligoric 2015 Sec. 1, 5; Legunsen Sec. 3 offline/online | [read-in-source] |
| Suite-size reduction / fault-detection (mutant) loss | SizRed = (|O|-|R|)/|O|; MutLoss = (|mut(O)|-|mut(R)|)/|mut(O)| | Shi FSE 2014 Sec. 3 | [read-in-source] |
| FBDL | % of future failed builds in which reduced suite fails to detect all faults the original detects; (|F|-|F_r|)/|F| x 100 | Shi ISSTA 2018 Sec. 3 | [read-in-source] |
| APFD / APFD-P | Rate of fault detection of an ordering; APFD-P weights faults by performance-change size | Laaber 2021 Sec. 4.4 (APFD-P attributed to Mostafa 2017) | [read-in-source] (Laaber text); formula for plain APFD not re-derived by me |
| Top-N | # benchmarks to run (by ranking) to capture N largest performance changes | Laaber 2021 | [read-in-source] |
| Performance-change significance | Bootstrap CI of ratio of means; regression if lower bound > 1 | Laaber Fig. 6; Kalibera & Jones | [read-in-source] / [abstract-only] |
| F1 / Type I / Type II for change detection | Precision/recall of detection of known-size changes; false-positive and false-negative rates | Reichelt 2023 Sec. III | [read-in-source] |
| Detection delay (iterations) | Not defined in any source I read for selection; closest: "reduction point" evaluation of FBDL on FUTURE builds and Top-N/APFD-P (earlier detection). | Shi 2018 Sec. 3; Laaber 2021 | [inferred] - needs our own definition |
| False-alarm rate for performance (with noise) | A/A comparisons give measured false positive rate; Reichelt targets <1% | Reichelt Sec. III; Laaber | [read-in-source] for the A/A idea in Reichelt; not found as a standard named metric [unknown] |

Observation: RTS literature's "safety" is defined relative to a deterministic dependency analysis and controlled testing (Rothermel 1997; Gligoric 2015 relies on proven class-dependency safety). In practice every "safe" claim is evaluated empirically against RetestAll or a reference tool (Legunsen 2016; Zhu 2019), and violations are reported as rates over revisions. [read-in-source]

### b2. Mutation / fault-injection validity evidence

- Mutants vs real faults: 73% of real Java faults coupled to generated mutants; 17% not coupled and 10% need stronger operators; mutant-detection correlation with real-fault detection beats statement coverage (Just 2014). One industrial program with real faults agreed (Andrews 2006) but with explicit external-validity limits. [read-in-source]
- Mutation-score distortions: equivalent mutants undecidable, redundant/subsumed mutants inflate scores (Papadakis 2019 Sec. 5.3). Therefore report "missed-by-reduced / detected-by-full" counts on a deduplicated or at least clearly characterized mutant set, not just a mutation score. [read-in-source + inferred recommendation]
- Change-focused mutation: Google generates at most one mutant per changed line (Petrovic 2018) and dev usefulness is the ground truth there. But commit-relevant mutants mostly lie OUTSIDE the changed lines (81% in Ojdanic et al., abstract). Therefore, a mutant set restricted to changed lines cannot test the central safety risk of a reduced test set - tests that exercise UNchanged code affected by the change. [abstract-only + inferred]
- Python-specific: Google's data show Python mutants survive most often (14.7%) among 7 languages (Petrovic Sec. 5); no source I found validates Python mutants against real Python faults. [read-in-source for 14.7%; [unknown] for validity]
- RTS-tool testing uses a mix: generated programs with mutation-like operators (AutoEP), reversed real bug fixes (DefectsEP), real histories (EvoEP) (Zhu 2019). A combination of synthetic and real evidence is thus established practice. [read-in-source]

### b3. Performance regression injection approaches

- Peass evaluation: inject a tiny busy-wait into a randomly chosen method on a benchmark's call tree, one regression per commit/branch; measure detection by candidate method; report share detected, share lost to noise, and share not covered (Reichelt 2023 Sec. IV). Known size effect is controllable. [read-in-source]
- Performance mutation operators from performance-bug patterns (Delgado-Perez 2021). [abstract-only]
- Real regressions for ground truth: run ALL benchmarks across adjacent versions, bootstrap CI, compare technique rankings with APFD-P/Top-N (Laaber 2021). [read-in-source] No injection there.
- Real performance bug characteristics: simple source changes that preserve functionality (Jin 2012), root causes spread across call sites/function boundaries (Jin 2012 Sec. 3 findings), design-level fixes ~27% (search summary) and only 15% of performance fixes touch tests (Zhao 2022). [read-in-source for Jin/Zhao 15%; abstract-only for the 27%]
- Search for dedicated "performance bug injection benchmark for Python": [unknown]; none found.
- Statistical underpinnings of "is it a regression": Kalibera & Jones effect-size CI (T3 topic).

### b4. Datasets for replay

| Dataset | Language | Content | Usable for our replay |
|---|---|---|---|
| Defects4J (ISSTA 2014 demo) | Java | 357 bugs, per-bug tests | Pattern only (reverse fix to get a regression, as in RTSCheck) [read-in-source Zhu] |
| BugsInPy (FSE 2020 demo) | Python | 493 bugs / 17 projects; reproducible, isolated | Functional-fault injection from REAL bug diffs onto Python code; validate "reduced test set fails on bug commit" [read-in-source] |
| RegMiner (ISSTA 2022) | Java | regressions mined (rfc/ric/wc triples) | Method template (pass-fail-pass) transferable to Python [inferred]; data Java only |
| TravisTorrent (MSR 2017) | Ruby/Java | 2.6M builds | CI-history replay; not Python-specific [abstract-only] |
| RTPTorrent (MSR 2020) | Java | 20 projects, >100k builds, per-test failures | Replay of selection/prioritization; Java [read-in-source] |
| Zhao et al. issues (Zenodo) / PerfCurator | Java/Py/C++; Python commits | performance issues / perf-fix commits | Source of realistic perf-fix diffs to learn typical optimization shapes [abstract-only] |
| Jin 2012 | C/C++/JS | 109 perf bugs | Patterns only [read-in-source] |

---------------------------------------------------------------------
## (c) Recommended evaluation protocol elements (each traced)

P1. **Per-edit oracle = full build + full suite (+ full benchmark set), run in a separate shadow job.** For each edit, record: reduced-validation verdict (accept/reject, selected tests, selected benchmarks, time) and full-validation verdict. Safety is then measured directly as missed failures. Traces: Rothermel & Harrold 1997 (inclusiveness definition), Zhu 2019 rule R1 (fewer newly failed tests than RetestAll = safety violation, assuming no flaky tests/order dependence), Legunsen 2016 (violation rates per revision). [read-in-source]

P2. **Primary safety metrics:** (i) missed-failure rate = edits where full suite fails but reduced passes / edits where full suite fails; (ii) missed-test fraction per edit, |E\T|/|E union T| style (Legunsen Sec. 4.2.3) where E = full-oracle failing/affected set (for a dynamic-dependency reference use an "affected tests" reference such as tests that fail on mutants); (iii) % of edits with any violation (Legunsen's `revs`). Also report the confidence interval, since failures are rare. [read-in-source for formulas; the CI is inferred]

P3. **Efficiency metrics:** selection ratio; end-to-end time = analysis + build + execution + collection (+ any dependency re-collection) normalised by the full pipeline, with offline vs online accounting declared; report AE and AEC separately; keep fixed build overhead in the denominator by timing the developer's build command. Traces: Gligoric 2015 Sec. 1/5; Legunsen Sec. 3. [read-in-source] Also report break-even: in Legunsen, RTS can be slower than RetestAll for projects whose tests run under about 5 s (Sec. 4.2.2) - so include a "no-benefit" subset analysis. [read-in-source]

P4. **Functional fault injection - two tiers.**
  - Tier A (synthetic): Python mutants (mutmut / Cosmic Ray style operators, Google-style AOR/LCR/ROR/SBR/UOI, at most one per line to avoid clutter). Report detection by reduced vs full and the "loss" = MutLoss-style fraction of mutants killed by full but not reduced (Shi FSE 2014). Trace: Petrovic Sec. 3; Shi FSE 2014 Sec. 3; Papadakis Sec. 5.3 (equivalent/redundant caveats). [read-in-source]
  - Tier B (real): replay real Python bug-introducing diffs (BugsInPy fixed->buggy reversal, as RTSCheck's DefectsEP does with Defects4J) applied as edits on top of the evolving optimized code or as stand-alone edit sequences, and check that the reduced set contains a failing test. Traces: Zhu 2019 Sec. III-C; Widyasari 2020 criteria. [read-in-source]
  - Mutant placement: do not restrict to changed lines only. Include (a) mutants on changed lines and (b) mutants in UNCHANGED code reachable from changed code (callers/callees), since most commit-relevant mutants are outside the diff (Ojdanic et al. abstract: 81%). Compare both. [abstract-only + inferred]
  - Justification for using mutants at all: Just 2014 (73% coupling, 17% not coupled), Andrews 2006 (single program), with the stated validity limits. [read-in-source]

P5. **Performance regression injection, calibrated.**
  - Inject controlled slowdowns (e.g., deterministic busy-wait or extra loop iterations sized as a % of the target function's measured time) into (i) changed functions, (ii) unchanged-but-covered functions called by the changed code, (iii) unrelated functions covered by selected benchmarks, (iv) functions not covered by any selected benchmark. Vary size across a ladder (e.g., 1%, 2%, 5%, 10%, 20% of benchmark time; sizes are [inferred]-choices, not from sources). Trace: Reichelt 2023 Sec. IV (busy-wait injection on benchmark call tree; categories: detected / lost to noise / not covered). [read-in-source]
  - Report detection probability vs injected size, and split misses into "benchmark not selected / not covering" vs "selected but below noise" - the same 3-way split Peass reports (detected 58.7%, noise 26.7%, uncovered 14.6%). [read-in-source]
  - Use A/A runs (same code, no injection) to measure the false-alarm rate under the machine's noise, targeting a declared Type I/II (Reichelt aims for <1%). [read-in-source for the target; A/A as practice is inferred]
  - Also use REAL performance changes as ground truth when possible: run the full benchmark set on adjacent versions and use bootstrap CI of ratio (Laaber Sec. 4.4-4.5), then compute APFD-P/Top-N for any ordering the reduced policy implies. [read-in-source]
  - Statistics: effect-size CI for ratio of means (Kalibera & Jones; T3 for depth). [abstract-only]

P6. **Periodic full checkpoints and detection delay.** Run the full suite/benchmarks every K accepted edits (checkpoint); when a full check fails, bisect back to the first offending edit and record delay = (checkpoint index - index of edit that introduced the failure) in edits and in wall time. Evaluate K by replaying histories at "reduction points" and measuring losses on FUTURE failures, as Shi 2018 does for FBDL (reduced suite fixed at an earlier point, tested on later failed builds). [read-in-source for the evaluation style; delay metric definition [inferred]; no source defines "detection delay" for selection]
  - Note Shi 2018's finding: traditional reduction metrics do NOT predict loss on real failures and historical loss is only a moderately better predictor. So do not extrapolate from mutant-only results to real safety. [read-in-source]

P7. **Check the checker (RTSCheck-style).** Before trusting the rule set, run it on (a) a no-change edit (should select nothing; rule R5), (b) a known fault-introducing edit (reverse bug fix; must select a failing test), (c) comparison to RetestAll on a synthetic evolution. Include reflection/dynamic-import cases since reflection and excluded libraries caused real safety violations in static RTS (Legunsen Sec. 4.3). Python analogs: `importlib`, `getattr`, `eval`, decorators, monkeypatching, plugin entry points, dynamic dispatch, conftest/fixtures. [read-in-source for Java causes; Python analogs [inferred]]

P8. **Selection ratio vs loss trade-off curve** per rule family (e.g., file-level vs function-level dependency; benchmark subset by coverage) plotted with both axes (time saved incl. overhead; missed failures/regressions), following Shi FSE 2014's size-vs-loss trade-off presentation and Legunsen's cost/safety discussion. [read-in-source]

P9. **Threat reporting** - use these as checklists: single-language scope; mutants vs real faults (Just; Andrews); artificial regressions unrepresentative, e.g., concurrency (Reichelt Sec. IV-C); flaky/order-dependent tests invalidate R1 (Zhu Sec. III-A); real-history vs synthetic ecological validity (Mattis 2020 Sec. 1). [read-in-source]

P10. **Sample size and stratification.** Because true failures are rare, stratify by edit type (loop restructure, caching, data-structure swap, vectorization, algorithm change), by change size, and by whether the edit touches public API; report per-stratum miss rate with exact binomial intervals. [inferred; no source]

---------------------------------------------------------------------
## (d) Assumptions that may break in iterative performance-motivated editing [inferred]

1. Mutants are small syntactic, mostly behavior-changing faults; performance-motivated edits introduce faults that are semantic equivalences broken in rare inputs: wrong caching (stale or key-collision), memoization across mutable arguments, precision loss from algebraic reordering/floating-point reassociation, dtype/overflow changes, aliasing introduced by in-place ops or views, generator vs list laziness, evaluation-order changes, concurrency (threading/multiprocessing/async) changes, mutable default args, identity vs equality. Just 2014 reports 17% of real faults not coupled to mutants; for optimization-specific bugs the uncoupled share is [unknown] and likely higher. The Tier B real-bug replay therefore cannot substitute for optimization-bug seeds; we need a hand-built "optimization bug" mutant class (e.g., drop a cache invalidation, swap `copy` for view, change `float64`->`float32`, reorder reductions, remove a lock). Jin 2012 notes performance fixes are "relatively simple source-code changes ... preserving functionality" [read-in-source], which is exactly the situation where a wrong simplification passes weak tests.
2. Selected tests/benchmarks come from dependency information gathered on the PREVIOUS revision (Ekstazi/mutmut-style stats). Repeated small edits compound drift: stale dependency data after a chain of accepted edits. Periodic full checks must also refresh the dependency data (the "C" phase), and the experiment should measure staleness effects. [inferred; Gligoric 2015 C-phase described in source]
3. Only 15% of performance fixes touch tests (Zhao 2022): the reduced test set rarely changes with the edit, so tests do not encode the new semantics of optimized code (e.g., new fast path not covered). New code paths created by an optimization (specialized branches) may be uncovered by any existing test; coverage-based reduction "selects" no test that reaches them. [read-in-source for 15%; remainder inferred]
4. Performance noise: small optimizations (e.g., 1-5%) are comparable to noise (Reichelt: 26.7% of injected regressions missed due to noise; Laaber: results depend on change-size threshold). A reduced benchmark set with few repetitions may accept slower code (false accepts) or reject neutral edits (false alarms); in an optimization workflow the failure direction is inverted - the goal is a speed-up, so a "no effect" or negative result is a quality failure, not only a regression. [read-in-source for noise stats; inversion inferred]
5. Python dynamism breaks static dependency soundness: dynamic imports, `getattr`, monkeypatching, C extensions, native libraries (NumPy/Cython), JIT/bytecode caches, `.pyc` and `__pycache__`, environment/CWD-dependent behavior; mutmut documents fork-only execution and a call-stack depth cutoff (`max_stack_depth`) that "can miss more mutants". Legunsen found reflection and library exclusion as the main static-RTS safety holes. [read-in-source for those tool docs/findings; Python mapping inferred]
6. Build reduction (e.g., skipping rebuild of C extensions or docs, partial installs) introduces a separate failure class (stale artifacts) not covered by test-selection literature, which assumes a build exists. Build-system incremental correctness is T-other; here we must still inject "stale build" faults. [inferred; Gligoric 2015 is the only source linking file dependencies to partial builds, per its text]
7. Flakiness and test-order dependence: R1 in RTSCheck assumes none; Python suites with global state, random seeds, and time/IO dependence violate this. The oracle (full run) must itself be repeated or flake-filtered before computing "missed failure". [read-in-source for R1 assumption; Python implication inferred]
8. Mutation-score pitfalls on optimized code: tight numerical code produces many equivalent or near-equivalent mutants (e.g., tolerance-bounded changes); Python survival rate is highest among Google's languages (14.7%) so a nontrivial share are equivalent or untested. Must triage or report both killed-by-full and survived-by-full. [read-in-source for 14.7%; implication inferred]
9. Edit sequences are dependent: a fault introduced by edit i may only be exposed after edit j. Per-edit independent fault injection (as in all cited mutation studies) misses interaction faults; the periodic-full-check design partly measures this. [inferred]
10. Selection oracles from CI-history datasets (RTPTorrent, TravisTorrent) are Java/Ruby-centric and their failures are human mistakes, not optimization-induced; for a Python optimization study we likely need our own replay corpus. [read-in-source that RTPTorrent is Java-only; remainder inferred]

---------------------------------------------------------------------
## (e) Search log (engine: WebSearch standard mode unless noted; date 2026-11-21 for all)

| # | Query (abridged) | Notable hits | Not found / notes |
|---|---|---|---|
| 1 | Rothermel Harrold "Analyzing regression test selection techniques" inclusiveness precision ... | core.ac.uk/download/17237569.pdf; Purdue p173-rothermel.pdf | Hit set mixes TSE 1996 and TOSEM 1997; the Purdue p173 PDF turned out to be TOSEM 1997. TSE 1996 PDF not read. |
| 2 | Gligoric Eloussi Marinov Ekstazi ISSTA 2015 pdf | Gligoric15PhD.pdf (dissertation), abstract txt, bibtex page | No clean author PDF of the ISSTA paper; used existing `2015-Ekstazi-ISSTA.pdf` from another researcher. Dissertation download attempted then cancelled. |
| 3 | RTSCheck ICSE 2019 | cs.cornell.edu/~legunsen PDF; ICSE page | Downloaded. |
| 4 | Shi ... Evaluating test-suite reduction ISSTA 2018 | mir.cs.illinois.edu/gyori/pubs/issta18.pdf | Author list in my brief was wrong; corrected. |
| 5 | Just et al. mutants valid substitute | UW author PDF | Downloaded. |
| 6 | Legunsen ... static RTS FSE 2016 | mir.cs.illinois.edu Marinov pubs PDF | Already in folder from another researcher. |
| 7 | Andrews Briand Labiche ICSE 2005 | utdallas course PDF, simula.no, DBLP, ttu TSE06 PDF | utdallas link returned HTML on download; TSE 2006 extension obtained instead. |
| 8 | Papadakis ... Mutation testing advances | mutationtesting.uni.lu/survey.pdf | Downloaded. |
| 9 | Petrovic Ivankovic State of mutation testing at Google | research.google, course PDFs | Downloaded umich copy. |
| 10 | commit-aware mutation testing ICSME 2020 | lero.ie, arXiv 2112.14566, core.ac.uk 335377161, orbilu 53860 | core returned HTML; orbilu PDF downloaded twice but damaged (xref). Abstract fetched via WebFetch from arxiv.org/abs/2112.14566. Authors in brief were wrong. |
| 11 | Delgado-Perez performance mutation testing STVR | idus.us.es 134751, core.ac.uk 427725256 | Both inaccessible for full text (HTML / 403). Abstract-only. |
| 12 | Laaber Gall Leitner TCP microbenchmarks | Chalmers fulltext PDF, PMC8550681 | Downloaded (overwrote another researcher's copy). |
| 13 | Jin et al. PLDI 2012 | uwaterloo course PDF | Downloaded. |
| 14 | empirical study performance bugs Python projects dataset | Zhao TSE (par.nsf.gov 10332839, Zenodo 6383167), PerfCurator arXiv 2406.11731, Belias arXiv 2504.20224 | No paper titled "PyPerf bugs" or similar. Zhao TSE obtained. |
| 15 | mutmut documentation incremental | mutmut.readthedocs.io, GitHub README | README fetched. |
| 16 | cosmic-ray documentation | cosmic-ray.readthedocs.io concepts | Concepts page fetched; no diff-based filter documented. |
| 17 | BugsInPy FSE 2020 | arXiv 2401.15481, GitHub soarsmu/BugsInPy | Downloaded arXiv copy. |
| 18 | RTPTorrent MSR 2020 | HPI PDF, Zenodo 3610999 | Downloaded. |
| 19 | Zhao ... 570 issues Java C++ Python | par.nsf.gov | Counts differed between search summary and paper text (162 Python per paper). |
| 20 | Defects4J ISSTA 2014 | UW/UMass abstract pages | Only abstract pages; no PDF downloaded. |
| 21 | injected performance regressions evaluate microbenchmark detection | arXiv 2303.14256 (Peass), 2411.17548, 2605.18397, 2212.09515 | Only Peass read (downloaded). Others abstract-only/snippet and not used. |
| 22 | PerfRanker Mostafa ISSTA 2017 | taoxiease PDF | File already in folder from another researcher (overwritten by my download of the same paper). |
| 23 | Kalibera Jones Quantifying performance changes | arXiv 2007.10899, Kent TR page | Downloaded. |
| 24 | RegMiner dataset | arXiv 2109.12389, ISSTA 2022 page | Authors in brief wrong; first two downloads damaged; third (export.arxiv.org) OK. |
| 25 | Kalibera Jones Rigorous benchmarking reasonable time | ISMM 2013 | File already in folder (other researcher). |
| 26 | mutatest documentation | mutatest.readthedocs.io, PyPI | Abstract-level only. |
| 27 | TravisTorrent MSR 2017 | TU Delft repository, testroots.github.io | Not downloaded; abstract-level. |
| W1 | WebFetch arxiv.org/abs/2112.14566 | abstract: 288 commits, 81% outside change | Verified. |
| W2 | WebFetch core.ac.uk search for Delgado | HTTP 403 | - |
| W3 | WebFetch idus.us.es/handle/11441/134751 | HTTP 403 | - |
| W4 | WebFetch mutmut README (raw.githubusercontent) | see card | - |
| W5 | WebFetch cosmic-ray concepts | see card | - |

Not searched / not found overall: dedicated "detection delay" metric in selection literature; Python-specific mutant validity studies; a benchmark of injected Python performance regressions; a Python CI-history replay dataset (RTPTorrent/TravisTorrent are not Python-centric) - [unknown].

Process notes: other researchers share the `papers/` folder. I overwrote two existing files (`2021-Laaber-TCP-Microbenchmarks-EMSE.pdf`, `2017-Mostafa-PerfRanker-ISSTA.pdf`) with copies of the same papers because I did not check for them before a parallel download; both are valid PDFs of the same papers, but their sha256/byte counts may differ from what the other researcher recorded. They are NOT listed in my T4-downloads.json for that reason.
