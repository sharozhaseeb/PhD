# T3 - Performance testing, benchmark selection, measurement rigor

Researcher run date: 2026-11-21. Scope: reduced benchmark/test sets per performance-motivated edit (Python, possibly C/Cython), deterministic rules only (no AI in the method).

Label legend: [read-in-source] = I read the text of the PDF/doc (section or page given); [abstract-only] = only abstract/landing page/search snippet seen; [inferred] = my reasoning; [unknown] = could not establish.

Page numbers: pdftotext output has no reliable page mapping, so I cite section/figure/abstract rather than page unless stated.

---------------------------------------------------------------------------

## (a) Source cards

### A. Performance regression test selection / prioritization

**A1. PerfScope** - Huang, Ma, Shen, Zhou, "Performance regression testing target prioritization via performance risk analysis", ICSE 2014.
- CORRECTION to brief: authors are Peng Huang, Xiao Ma, Dongcai Shen, Yuanyuan Zhou (not Holmes/Luo). Tool name is PerfScope.
- [abstract-only] (project page ryanphuang.github.io/perfscope + search snippets; no PDF obtained): static, white-box risk analysis of a commit built on LLVM, C/C++ only; ranks commits by likelihood of introducing a perf regression.
- [read-in-source] via PerfRanker intro (A3): PerfScope extracts features from original version and the commit and trains a classifier to predict whether a commit may significantly affect performance; PerfRanker's authors state a non-trivial share of commits still require perf testing after PerfScope. (Note: this makes PerfScope a learned model; not usable under the "no AI" constraint except as a design contrast.)
- No PDF downloaded (no OA copy found on the project page).

**A2. Perphecy** - de Oliveira, Fischmeister, Diwan, Hauswirth, Sweeney, "Perphecy: Performance Regression Test Selection Made Simple but Effective", ICST 2017, pp. 103-113, DOI 10.1109/ICST.2017.17.
- CORRECTION: "Petkovich" is not an author of this paper (that is a different paper by the same group). Authors verified from the Waterloo ESG page and USI SAPE page.
- [abstract-only]: predicts whether a commit is likely to affect performance and which tests to run; claims to be simple and general and to avoid prior approaches' static/dynamic analyses. Abstract contains no numbers.
- [abstract-only, secondary via PRICE abstract A6]: PRICE reports outperforming Perphecy; PRICE calls Perphecy "the state-of-the-art deterministic approach".
- No OA PDF found (sape.inf.usi.ch page links only to the DOI). Not downloaded. GAP: method details (what the "simple" heuristic is) are [unknown] to me; must be read via institutional access.

**A3. PerfRanker** - Mostafa, Wang, Xie, "PerfRanker: Prioritization of Performance Regression Tests for Collection-Intensive Software", ISSTA 2017, pp. 23-34, DOI 10.1145/3092703.3092725. PDF: 2017-Mostafa-PerfRanker-ISSTA.pdf.
- [read-in-source, abstract + Sec. 1]: prioritizes test cases (does not skip them) using performance impact analysis of the revision on each test's execution; top-3 most-affected tests are covered within the top 30%-37% of the prioritized tests vs top 65%-79% for three baselines (abstract). Subjects: Apache Commons Math, Xalan (Sec. 4).
- [read-in-source, Sec. 1]: states reasons to prioritize: cost; "various random factors" require many repeated executions, so ranked tests can be given more repetitions; a commit may speed up some tests and slow others.
- [read-in-source, Sec. 4.5.4]: reports analysis overhead (profiling and per-commit analysis time in seconds; base-version profiling overhead stated as low); I did not extract exact figures.
- Safety assumption: performance impact is estimated via dynamic call graph + collection-loop model; collection-intensive Java only. Python support: none.

**A4. Laaber, Gall, Leitner (EMSE 2021)** - "Applying test case prioritization to software microbenchmarks", Empirical Software Engineering 26(6), art. 133, DOI 10.1007/s10664-021-10037-x. PDF: 2021-Laaber-TCP-Microbenchmarks-EMSE.pdf.
- [read-in-source, abstract + Sec. 4.2]: 54 TCP technique instantiations (total/additional greedy; static/dynamic coverage; granularity) on 10 Java JMH projects, 1,829 distinct benchmarks, 161 versions (the 6,460 parameterizations figure is from the search snippet = [abstract-only]).
- [read-in-source, abstract]: mean APFD-P 0.54-0.71; the three largest performance changes are captured after executing 29%-66% of the suite; best technique costs 11% of total suite runtime in overhead; total strategy beats additional; dynamic coverage favoured over static unless prioritization time is limited.
- [read-in-source, Sec. 4.7 / 6.6]: threats and "what is an important performance change" discussion (threshold t).
- Note: this is prioritization (ordering), not selection; it never drops benchmarks, so it has no miss rate in the selection sense, only "time to detect".

**A5. Laaber, Yue, Ali - search-based microbenchmark prioritization** - "Evaluating Search-Based Software Microbenchmark Prioritization", arXiv:2211.13525 (v4 dated 18 Apr 2024). PDF: 2022-Laaber-Search-Based-MB-Prioritization.pdf.
- [read-in-source, abstract + Sec. 1]: search algorithms only match, do not beat, the best greedy coverage-based TCP; a greedy technique using only performance-change history (no coverage) is equal or better and has <1% runtime overhead; prior coverage-based TCP is described as having a 17% overhead in their earlier work (Sec. 1; this differs from the 11% best-case in A4 abstract: different configuration).
- Journal venue: search snippet says later IEEE TSE = [abstract-only, unverified]; cite as arXiv.
- Relevance: history-based (change-frequency of past benchmark results) selection is deterministic and cheap, but depends on a history of performance changes per benchmark.

**A6. PRICE** - Alshoaibi, Hannigan, Gupta, Mkaouer, "PRICE: Detection of Performance Regression Introducing Code Changes Using Static and Dynamic Metrics", SSBSE 2019, DOI 10.1007/978-3-030-27455-9_6 (journal extension 2022, Swarm and Evolutionary Computation, "Search-based detection of code changes introducing performance regression", different author list).
- [abstract-only]: multi-objective evolutionary rule generation from static (Lizard) and dynamic (benchmark-run) metrics; 8,000 commits of the Git project; average detection 77%, 22% above "the state-of-the-art deterministic approach" (Perphecy); rule performance "degrades over time".
- ML/search-based => outside "no AI"; kept as a contrast. Not downloaded.

**A7. Risk-Aware Batch Testing** - Sayedsalehi, Rigby, Mierzwinski, arXiv:2604.00222 (31 Mar 2026).
- [abstract-only]: ML commit risk (CodeBERT, ROC-AUC up to 0.694) + batching on Mozilla Firefox data; 32.4% fewer test executions, 26.2% lower max time-to-culprit vs a production-inspired baseline. Learned => outside scope; included because it is the most recent (2026) CI performance-test-reduction paper found, and shows ROC-AUC well below deterministic-rule reliability.

**A8. Grambow et al. (IEEE TCC)** - Grambow, Kovalev, Laaber, Leitner, Bermbach, "Using Microbenchmark Suites to Detect Application Performance Changes", arXiv:2212.09515 (v1 cs.PF, 19 Dec 2022; published IEEE Trans. Cloud Computing per search snippet = [abstract-only] for venue details). PDF: 2022-Grambow-Microbenchmark-Suites-AppPerf-TCC.pdf.
- CORRECTION: Japke is not an author of this paper.
- [read-in-source, abstract + results section/Fig. 9]: compares complete and "optimized" (reduced) microbenchmark suites against an application benchmark on InfluxDB (70 commits) and VictoriaMetrics (110 commits). Abstract: detecting application-level changes with an optimized suite is possible "if frequent false-positive alarms can be tolerated". InfluxDB optimized suite (results section, Fig. 9 discussion): 4 true positives (commits 10, 59, 64, 65), false alarms for 17 commits, and it misses a negative group-by trend starting at commit 20 (false negative).
- [read-in-source, Sec. 7 conclusion/discussion]: suites "are unlikely to always have full code coverage of the SUT"; the optimized suite cannot replace the application benchmark; suited for fast local/CI feedback with a daily application benchmark as backstop (abstract, via search + text).
- Safety assumption tested and FOUND WEAK: that microbenchmark change at a function corresponds to application-level change.

**A9. Japke, Witzko, Grambow, Bermbach, UCC 2023** - "The Early Microbenchmark Catches the Bug - Studying Performance Issues Using Micro- and Application Benchmarks", 2023 IEEE/ACM 16th Intl. Conf. on Utility and Cloud Computing (UCC '23), arXiv:2311.04108. PDF: 2023-Japke-Early-Microbenchmark-Catches-Bug.pdf.
- [read-in-source, Sec. 1]: testbed microservice (flight booking) with three configurable-severity injected performance issues; microbenchmarks detected all three earlier, some at the lowest severity; application benchmarks raised false positives, wrongly flagged improvements, and detected the issues later.
- Relevance: supports microbenchmarks as the sensitive instrument for localized changes; contradicts A8 on proxy-ness only in direction (here micro is MORE sensitive; A8: micro is less specific). Single synthetic testbed (three injected issues), so generality is [unknown].

**A10. µOpTime** - Japke, Grambow, Laaber, Bermbach, "µOpTime: Statically Reducing the Execution Time of Microbenchmark Suites Using Stability Metrics", ACM TOSEM 34(8), Article 231, Oct 2025, DOI 10.1145/3715322. arXiv:2501.12878v2. PDF: 2025-Laaber-uOpTime.pdf.
- CORRECTION to brief: this is TOSEM 2025, not ICPE 2023; Japke is first author. No ICPE 2023 µOpTime exists in what I found (log).
- [read-in-source, abstract + Sec. 1 RQ1-RQ4]: from a previous full run, picks per-benchmark minimal measurement repetitions with stability metrics (5 metrics incl. RMAD, RCIW). 14 projects (3 Go, 11 Java), 4,304 benchmarks. Reduction up to 95.83% (Go; median 76.8%), up to 35.96% (Java dataset 2; median 13.08%), up to 71.74% (Java dataset 3; median 26.78%) with >=80% of benchmarks within 3% of the full-run result. RMAD on Java: up to 64.1% of benchmarks deviate >10% (rxjava); RCIW(median) keeps >=75.37% within 1%. RQ4 (CI simulation over successive versions): for 348 Go + 1,844 Java benchmarks, 3 and 29 false positives, 2 and 7 false negatives vs full configuration; Go total time 38.75/43.75/26.25 min -> 2.75/1.75/1.1 min; the four Java projects 40/78/94/104 min -> 36.43/66.93/81.23/92.6 min (Sec. 1, RQ4).
- Assumption: the previous full run is representative (static configuration from old run) - exactly the staleness risk in section (d).

**A11. Laaber & Leitner MSR 2018** - "An Evaluation of Open-Source Software Microbenchmark Suites for Continuous Performance Assessment", MSR 2018, pp. 119-130, DOI 10.1145/3196398.3196407.
- [abstract-only] (Chalmers landing page + search): 10 Java/Go projects, 16-983 benchmarks, suite runtimes 11 min - 8.75 h; some benchmarks vary 50%+; injected artificial slowdowns in public API methods, benchmark-suite detection score (ABS) 10%-100% across subjects. No OA PDF fetched. GAP.

### B. Microbenchmark stability, dynamic reconfiguration

**B1. Laaber, Würsten, Gall, Leitner (ESEC/FSE 2020)** - "Dynamically Reconfiguring Software Microbenchmarks: Reducing Execution Time without Sacrificing Result Quality", pp. 989-1001, DOI 10.1145/3368089.3409683.
- [abstract-only] (FSE 2020 program page fetched): first technique to dynamically stop a microbenchmark once results are sufficiently stable; three statistical stopping criteria; on JMH suites execution time reduced 48.4%-86.0%; same result quality as default run for 78.8%-87.6% of benchmarks.
- [read-in-source, secondary: Traini et al. EMSE 2023 text, Sec. 2/3 "dynamic reconfiguration"]: the three criteria are coefficient of variation (CV; stable when max-min CV over a sliding window is within a threshold), relative confidence interval width (RCIW; hierarchical bootstrap after Kalibera & Jones), Kullback-Leibler divergence (KLD).
- No PDF: ZORA host refused connections (ECONNREFUSED on fetch; curl returned no PDF link), ACM returned 403; Unpaywall lists only a ZORA "submittedVersion" landing page. Not downloaded. GAP: the actual paper text is unread.

**B2. Laaber, Scheuner, Leitner, EMSE 2019** - "Software microbenchmarking in the cloud. How bad is it really?", Empirical Software Engineering 24(4):2469-2508, DOI 10.1007/s10664-019-09681-1. PDF: 2019-Laaber-Microbenchmarking-Cloud-EMSE.pdf.
- [read-in-source, abstract]: >4.5 million data points, Java and Go microbenchmarks, AWS/GCE/Azure (3 instance types each) plus IBM Bluemix bare metal; CV of results ranges from 0.03% to >100% depending on benchmark and instance type; running test and control on the same instances in randomized order detects slowdowns of 10% or less "with high confidence" using Wilcoxon rank-sum and overlapping bootstrapped CIs; Wilcoxon detects smaller slowdowns.
- [read-in-source, Sec. 5.3 and intro]: A/A testing used to measure false positives; A/A + detection experiments total roughly 130 h + 500 h.
- Note: earlier preprint title "Performance testing in the cloud. How bad is it really?" (PeerJ Preprints) [abstract-only].

**B3. Traini, Cortellessa, Di Pompeo, Tucci, EMSE 2023** - "Towards effective assessment of steady state performance in Java software: Are we there yet?", EMSE (DOI 10.1007/s10664-022-10247-x; accepted 30 Sep 2022; downloaded arXiv:2209.15369v2 author version). PDF: 2023-Traini-SteadyState-Java-EMSE.pdf.
- [read-in-source, abstract]: Java microbenchmarks do not always reach steady state; developer warmup estimates are often inaccurate; dynamic reconfiguration improves warmup estimation but is still suboptimal. [read-in-source, results]: developer config stops warmup... developers overestimate warmup end in 48% of forks and underestimate in 32% of forks (text near Sec. 5 results); RCIW overestimates in 72% of forks.
- Python relevance: [inferred] the warmup problem is mostly JIT-related; CPython w/o JIT has pyperf default of 1 warmup (see D1), but PyPy/JIT-enabled builds (e.g. CPython 3.13+ experimental JIT) may revive it.

**B4. Costa, Bezemer, Leitner, Andrzejak, TSE 2021** - "What's Wrong With My Benchmark Results? Studying Bad Practices in JMH Benchmarks", IEEE TSE 47(7):1452-1467, DOI 10.1109/TSE.2019.2925345. [abstract-only] (Chalmers listing): static-analysis tool flags 5 bad JMH practices, all found prevalent across 123 Java systems; they often significantly change results. (The brief said "Costa et al. TSE 2019": the DOI year is 2019 early access, issue year 2021.) No PDF.

### C. Rigorous benchmarking and measurement bias

**C1. Georges, Buytaert, Eeckhout, OOPSLA 2007** - "Statistically Rigorous Java Performance Evaluation", DOI 10.1145/1297027.1297033. PDF: 2007-Georges-Statistically-Rigorous-Java-OOPSLA.pdf.
- [read-in-source, Sec. 2, 3, 4]: "best of 30" vs mean with 95% CI; confidence intervals for means (Sec. 3.2; z for n>=30, Student t otherwise, Sec. 3.6); comparing two alternatives via CI of the difference (Sec. 3.3); ANOVA + Tukey HSD for >2 alternatives (Sec. 3.4); steady-state definition via CoV of k iterations falling below a threshold, multiple VM invocations, CI over invocation means (Sec. 4).

**C2. Kalibera & Jones, ISMM 2013** - "Rigorous Benchmarking in Reasonable Time", pp. 63-74, DOI 10.1145/2464157.2464160 (as printed in the Kent repository cover page; Crossref also surfaced 10.1145/2491894.2464160). Downloaded Author's Accepted Manuscript. PDF: 2013-Kalibera-Rigorous-Benchmarking-ISMM.pdf.
- [read-in-source, abstract + Sec. 1]: statistically rigorous method for repetition and summarising, modelling experiment cost to choose how many repetitions at each level (VM executions, iterations, etc.) to get a given precision for a fixed budget; error bounds for a single system and for ratio of baseline vs new version; critiques common methods; surveys papers and finds most do not repeat or summarise soundly.
- Companion: Kalibera & Jones, "Quantifying Performance Changes with Effect Size Confidence Intervals", arXiv:2007.10899 (posted 21 Jul 2020, dated Nov 2013, Kent TR 4-12) [abstract-only]: CI on the ratio of mean execution times; review of 122 papers found most ignore uncertainty.

**C3. Mytkowicz, Diwan, Hauswirth, Sweeney, ASPLOS 2009** - "Producing Wrong Data Without Doing Anything Obviously Wrong!", pp. 265-276, DOI 10.1145/1508244.1508275. PDF: 2009-Mytkowicz-Producing-Wrong-Data-ASPLOS.pdf.
- [read-in-source, abstract + Sec. 1-2]: UNIX environment size and link order alter results; environment-size changes shift performance "frequently by about 33% and once by almost 300%" on a Core 2 (Sec. 1/Fig. 1b); survey of 133 papers (ASPLOS, PACT, PLDI, CGO) found none adequately considered measurement bias; proposes causal analysis and setup randomization.

**C4. Curtsinger & Berger, ASPLOS 2013** - "STABILIZER: Statistically Sound Performance Evaluation", DOI 10.1145/2451116.2451141. PDF: 2013-Curtsinger-STABILIZER-ASPLOS.pdf.
- [read-in-source, abstract + Sec. 1-2.2]: re-randomizes code, stack, heap layout at runtime; makes execution time approximately normal so ANOVA/t-tests apply; median overhead <7%; -O3 vs -O2 on SPEC CPU2006 indistinguishable from noise; link-order changes can decrease performance by up to 57% (Sec. 1). LLVM 3.1-era tool, C/C++ only. Python: none; relevant to C/Cython extension layout bias only.

**C5. Barrett, Bolz-Tereick, Killick, Mount, Tratt, OOPSLA 2017** - "Virtual Machine Warmup Blows Hot and Cold", Proc. ACM Program. Lang. 1(OOPSLA), 52:1-52:27; arXiv:1602.00602 (v6, 6 Oct 2017). PDF: 2017-Barrett-VM-Warmup-OOPSLA.pdf.
- [read-in-source, abstract]: changepoint analysis; "at most 43.5% of <VM, benchmark> pairs consistently reach a steady state of peak performance" across 3 machines. Includes PyPy among VMs [inferred from memory of the paper; not verified in text I read].

**C6. Bulej, Horky, Tuma, Farquet, Prokopec, ICPE 2020** - "Duet Benchmarking: Improving Measurement Accuracy in the Cloud", pp. 100-107, DOI 10.1145/3358960.3379132, arXiv:2001.05811. PDF: 2020-Bulej-Duet-Benchmarking-ICPE.pdf.
- [read-in-source, abstract + Sec. 1, 4.2, conclusion]: run the two artifacts concurrently on the same machine and evaluate their relative performance; accuracy improvement 2.3x-12.5x (avg 5.03x) for ScalaBench/DaCapo workloads and 23.8x-82.4x (avg 37.4x) for SPEC CPU 2017; premise: interference is "synchronized" (affects both artifacts similarly); Sec. 4.2 (RQ2) tests that; the procedure does not always utilize resources evenly (benchmarks that contend with each other affect results; Sec. 4).
- Related earlier work: MASCOTS 2019 initial experiments [abstract-only via search].

### D. Unit tests as performance tests

**D1. Ding, Chen, Shang, ICSE 2020** - "Towards the Use of the Readily Available Tests from the Release Pipeline as Performance Tests. Are We There Yet?", DOI 10.1145/3377811.3380351. PDF: 2020-Ding-ReadilyAvailableTests-ICSE.pdf.
- [read-in-source, abstract + Sec. 3-5]: 127 performance issues from Hadoop and Cassandra; tests run before/after fix commits; Mann-Whitney + Cliff's delta, only LARGE effect counted (Sec. 3 "Filtering false-positive results"); on average only 9.2% (Cassandra) and 20.6% (Hadoop) of tests can demonstrate improvements for all associated metrics; 76.9% (Cassandra) and 74.3% (Hadoop) of tests cannot demonstrate any improvement even though they execute the changed code (Sec. 4 results); eight reasons (e.g. insufficient input size, not enough repetition - 9 tests, limited line coverage of the perf-relevant code); random operations and I/O produce the largest false-positive changes in unimpacted tests.
- Key relevance: "covers the changed code" is NOT sufficient for a test to expose a speed-up.

**D2. Stefan, Horky, Bulej, Tuma, ICPE 2017** - "Unit Testing Performance in Java Projects: Are We There Yet?", DOI 10.1145/3030207.3030226. PDF: 2017-Stefan-Unit-Testing-Performance-Java-ICPE.pdf.
- Brief called the first author "Stefan"; the real author is Petr Stefan (surname Stefan; Czech diacritic Štefan).
- [read-in-source, abstract]: mines GitHub Java projects for performance-test framework usage (JMH etc.); the "<3% of projects / unsuitable for build-time testing" statement comes from the authors' slides snippet = [abstract-only].

**D3. Leitner & Bezemer, ICPE 2017** - "An Exploratory Study of the State of Practice of Performance Testing in Java-Based Open Source Projects", pp. 373-384, DOI 10.1145/3030207.3030213. PDF: 2017-Leitner-Performance-Testing-State-of-Practice-ICPE.pdf.
- [abstract-only via search; PDF downloaded, not read in depth]: 111 Java OSS projects with performance tests; perf tests are a small part of suites, rarely updated; only 16% of projects use a dedicated framework (JMH/Caliper).

**D4. Chen & Shang, ICSME 2017** - "An Exploratory Study of Performance Regression Introducing Code Changes", pp. 341-352. PDF: 2017-Chen-Exploratory-Perf-Regression-Changes-ICSME.pdf.
- [read-in-source, abstract + Sec. 1]: 1,126 commits from ten Hadoop releases and 135 commits from five RxJava releases, each test/micro-benchmark repeated 30 times independently; regression-introducing changes are prevalent, are often accompanied by improvement in other metrics ("developers may not be aware of the existence of performance regressions, even when they are trying to improve performance"), mostly introduced while fixing OTHER functional bugs; six code-level root causes; 12.5% of examined regressions avoidable.

### E. Performance change detection in CI

**E1. Daly, Brown, Ingo, O'Leary, Bradford, ICPE 2020** - "The Use of Change Point Detection to Identify Software Performance Regressions in a Continuous Integration System", DOI 10.1145/3358960.3375791; arXiv:2003.00584 "Change Point Detection in Software Performance Testing". PDF: 2020-Daly-ChangePoint-MongoDB-ICPE.pdf.
- [read-in-source, Sec. 1]: previous system was threshold-based with three comparisons: (1) vs the immediately preceding run, (2) vs a run a week ago, (3) vs the last stable release; it produced "a large number of false positives (up to 99% depending on how you count)", missed smaller regressions and flagged commits unrelated to the regression; list of failure modes includes "multiple small changes over time causing a drift down in performance". [read-in-source, Sec. 2]: noise decomposed into platform (Np), software (Ns) and workload generator (Nw) components; E-Divisive means used; "we have to learn to live with noise". CI runs thousands of benchmarks, typically every 2 h or 24 h.

**E2. Fleming, Kolaczkowski, Kumar, Das, McCarthy, Pattabhiraman, Ingo - Hunter** - "Hunter: Using Change Point Detection to Hunt for Performance Regressions", ICPE 2023, arXiv:2301.03034. PDF: 2023-Fleming-Hunter-ChangePoint.pdf.
- Brief said "Fleming et al. 2023": confirmed first author Matt Fleming; seven authors.
- [read-in-source, abstract]: modified E-divisive means; replaces the randomized-permutation significance test with Student's t-test because the randomized approach "did not produce deterministic results"; open source; designed for normally-distributed metrics. Direct relevance: deterministic decision rule.

### F. Python tooling (docs; no peer-reviewed Python benchmark-stability study found)

**F1. pyperf** (docs.readthedocs.io/pyperf).
- [read-in-source, Runner page "Loop iterations"]: default CPython: 20 processes x 3 values = 60 values, 1 warmup; with JIT: 6 x 10, 10 warmups; each value >= 100 ms (min-time default) by loop calibration; `--rigorous` doubles processes (40x3=120 values), `--fast` halves to 10 processes, 2 values (20 values).
- [read-in-source, Analyze page]: `pyperf compare_to` uses Student's two-sample two-tailed t-test, non-significant benchmarks hidden; on outliers, advice is to re-run with more runs/values/loops or `pyperf system tune`; median/MAD recommended when unstable.
- [read-in-source, System page]: `system tune` sets CPU governor to performance, raises min frequency, stops irqbalance, sets perf_event_max_sample_rate=1; checks (does not change) CPU isolation, nohz_full, ASLR=2, power cable.

**F2. asv (airspeed velocity)** (asv.readthedocs.io).
- [read-in-source, Using page]: `asv run RANGE` with `--steps`; `asv compare` flags ratio beyond `--factor` (default 1.1), "~" marks statistically insignificant; `asv find` binary-searches a range for the commit with the largest regression, "works best on a small range with roughly monotonic runtimes"; `asv publish` regressions tab "detects statistically significant decreases".
- [read-in-source, Commands page]: `asv continuous` = "side-by-side comparison of two commits for continuous integration", `--factor`, `--only-changed`, `--interleave-rounds` ("interleave benchmarks with multiple rounds across commits" to reduce ordering bias), `--bench REGEX` selects benchmarks.
- [unknown]: step-detection algorithm details (step_detection page returned 404 via fetch).

**F3. CodSpeed** (codspeed.io/docs/instruments/cpu).
- [read-in-source]: CPU Simulation instrument runs each benchmark once and simulates the CPU; instructions weighted by measured cost; L1/LL cache-miss penalties; cycles converted to time at constant frequency; I/O and system calls excluded; Python, Rust, C++, Node supported (Go/Java walltime only); Walltime instrument for syscall-heavy code. The page did not name Valgrind/cachegrind (brief's assumption NOT confirmed) [unknown]. I did not read pytest-codspeed docs.

**F4. pytest-benchmark** (comparing page).
- [read-in-source]: `--benchmark-autosave/save`, `--benchmark-compare`, `--benchmark-compare-fail=<stat>:<N>%` fails the run when a statistic (min/mean) is more than N% slower; no statistical test on this page.

**F5. CPython community noise reports** - python-dev/speed mailing-list threads and discuss.python.org posts surfaced by search; [abstract-only/snippet]: Stinner ignores <5% changes as noise; locale/command-line length/cache effects changed timings; CPU isolation, ASLR off, Turbo off helped; Pitrou: timings right-skewed, prefer median; a discuss.python.org post (2026, about an AI-agent denoising skill) [read-in-source, forum text]: unrelated code change can cross a layout boundary and cause a large regression in one benchmark; `.pyc` state before PGO changes results; recommends fixed summary statistic, build-identity checks, treating cold/steady/JIT states as separate experiments. Forum-quality evidence; flagged as weak.

---------------------------------------------------------------------------

## (b) Synthesis

### b1. What is reduced

| Approach | What is reduced | Granularity | Deterministic? | Reported saving / quality | Source |
|---|---|---|---|---|---|
| TCP on microbenchmarks (coverage greedy) | order only (can stop early) | benchmark / parameterization | yes (static or dynamic coverage) | top-3 largest changes found after 29%-66% of suite; overhead 11% of suite time (best) | A4 abstract |
| History-based greedy | order | benchmark | yes | equal or better than coverage TCP, overhead <1% | A5 abstract |
| PerfRanker | order, plus more repetitions on top-ranked | test case | yes (dynamic call graph model) | top-3 in top 30-37% vs 65-79% baselines | A3 abstract |
| PerfScope / Perphecy / PRICE | whole commit skipped or run (selection at commit level) | commit | PerfScope learned; Perphecy [unknown details]; PRICE evolved rules | PRICE avg detection 77% (+22% over Perphecy) | A1, A2, A6 [abstract-only] |
| Dynamic reconfiguration (CV/RCIW/KLD) | iterations/forks stopped early | per benchmark, runtime | deterministic given data, but depends on measured noise | 48.4%-86.0% time saved; same quality for 78.8%-87.6% of benchmarks | B1 [abstract-only] |
| µOpTime | measurement repetitions, fixed statically from an old run | per benchmark | yes | up to 95.83% (Go), 94.17% (Java, abstract); median 76.8% Go / 13.08% / 26.78% Java; RQ4 3/29 FP, 2/7 FN | A10 |
| Optimized (reduced) microbenchmark suite | subset of benchmarks | benchmark | selection method: application-coverage-based [inferred from Grambow footnote 7 mentioning call graphs] | misses a trend; 17 false alarm commits in InfluxDB | A8 |
| Duet/RMIT | not reduction; reduces variance so fewer repetitions needed | pair/benchmark | yes | 2.3x-37.4x accuracy gain | C6, B2 |
| Change point detection | analysis only (no reduction of runs) | metric time series | Hunter yes (t-test); E-Divisive permutation test not deterministic | n/a | E1, E2 |

### b2. Safety assumptions (explicit or implicit)
1. Localization: a performance change shows up in benchmarks whose execution covers the changed code (coverage-based TCP, PerfRanker, A8 optimized suite). [read-in-source: A3 Sec. 3 model; A4 Sec. 3] Counter-evidence: Ding et al. found 74.3%-76.9% of covering tests could not show the known improvement (D1), and Grambow found micro-detections not visible at application level and application regressions missed (A8).
2. Steady state reachable and warmup estimable (dynamic reconfiguration; Georges CoV rule). Counter-evidence: Barrett (<=43.5% of VM/benchmark pairs consistently reach steady state, C5), Traini (B3).
3. A prior full run is representative (µOpTime static configs, history-based TCP). Staleness risk is acknowledged by the approach (A10 RQ4 re-evaluates over successive versions) but see (d).
4. Noise model: approximately normal/iid at the right level of the hierarchy (Georges CI; Kalibera & Jones hierarchical; Stabilizer makes normality plausible via re-randomization); Daly explicitly says noise "is not clear a priori iid" and may be time-correlated (E1 Sec. 2).
5. Interference is shared between compared artifacts (duet; C6 Sec. 4.2).

### b3. Overhead
- Coverage TCP 11% of suite runtime (best) up to >55% for badly parameterized static coverage (A4 abstract/search snippet); history-based <1% (A5). PerfRanker overhead stated in Sec. 4.5.4 (profiling base version once; per-commit analysis seconds) [numbers not extracted].
- Stabilizer <7% median (C4).
- Python-specific costs of coverage collection (coverage.py / sys.monitoring) are [unknown] in this literature; none of the above papers measured them.

### b4. Python support
- None of the selection/prioritization papers (A1-A6) targets Python; all Java/JMH, C/C++ (PerfScope), or Go. The only Python-native pieces are tooling: pyperf, asv, pytest-benchmark, CodSpeed (F1-F4). No peer-reviewed study of Python benchmark stability or Python benchmark selection was found (see search log).
- µOpTime and dynamic reconfiguration are implemented for JMH/Go test harnesses [read-in-source A10 abstract]; nothing equivalent exists for pyperf/asv in what I found [unknown whether pyperf's calibration plays the same role: pyperf fixes values per process; it does not stop early on a stability criterion per the docs I read].

---------------------------------------------------------------------------

## (c) Measurement threats for per-edit acceptance and recommended procedures

Threats (all [read-in-source] unless noted):
1. Layout/environment bias: unrelated environment size or link order shifts results by ~33% typically and ~300% once (C3 Sec. 1); link order up to 57% (C4 Sec. 1). CPython discussion reports the same class of effects from code layout (F5, weak). For C/Cython extensions, a one-line edit that moves code across a boundary can change another benchmark.
2. Run-to-run and cross-process noise: Laaber cloud CV from 0.03% to >100% across benchmark x instance type (B2 abstract). MongoDB: "worst case run-to-run variation ... as much as 20% or more" over small numbers of runs (E1 Sec. 1; I read the passage but wording is garbled by ligature extraction, treat as approximate).
3. Warmup and non-steady state (B3, C5). In CPython without JIT pyperf warmup default = 1 (F1).
4. Cloud/shared-machine variance (B2, C6); mitigated by running A and B on the same instance in randomized order (B2) or concurrently (C6).
5. Static thresholds are a poor decision rule across tests with different noise (E1 Sec. 1).
6. Statistical significance without effect size: large samples make trivial differences significant (D1 Sec. 3, citing effect size practice).
7. Random operations and I/O in tests produce large spurious changes in unimpacted tests (D1).

Recommended procedures (sources in brackets):
- Repetition hierarchy: multiple independent process executions (forks), each with several values; allocate repetitions by variance at each level for a fixed budget [C2; pyperf defaults F1: 20 x 3 on CPython].
- Interleave/pair A and B in the same session on the same machine: randomized interleaving (asv `--interleave-rounds` F2; RMIT per B2 and arXiv 2510.18640 snippet [abstract-only]) or concurrent duet [C6] when two cores are free and the assumption of shared interference holds.
- Report the ratio of means with a confidence interval (not best-of-N, not a bare mean) [C1 Sec. 2-3; C2 companion arXiv:2007.10899 [abstract-only]].
- Test + effect size: Student t or Wilcoxon/Mann-Whitney with a CI on the ratio, plus Cliff's delta or an explicit minimum-effect threshold [B2 (Wilcoxon, bootstrap CI); D1 (Mann-Whitney + Cliff's delta); F1 (t-test)].
- Always run A/A control (same code twice) to estimate false-positive rate for each benchmark on the actual machine [B2 Sec. 5.3].
- System hygiene for wall time: `pyperf system tune`, CPU isolation, ASLR check, plug in power [F1 System page]; pin build identity (same compiler, flags, PGO state) [F5, weak].
- Layout randomization where possible (C4 for C/C++; for Cython/C extensions this is [inferred] and not packaged for Python).
- Instruction-count (simulation) metrics as a deterministic secondary signal [F3]; [inferred] they exclude I/O and cannot see cache/branch effects not modelled, and may disagree with wall time.

---------------------------------------------------------------------------

## (d) Assumptions that may break when edits are performance-motivated and accumulate  [inferred] unless a source is cited

1. Compounding sub-noise changes. Each edit may be below the per-run detection threshold (e.g. asv default factor 1.1 = 10% [F2 read]); N edits each slowing a different path 1-2% compound invisibly. Support: MongoDB lists "multiple small changes over time causing a drift down" as an unsolved failure mode of per-run comparison and compared to the last stable release as a partial counter (E1 Sec. 1). [inferred] Need a cumulative check against the ORIGINAL baseline, not just the previous commit.
2. Edits to improve X regress Y. Chen & Shang show regression-introducing changes often also improve other metrics, and developers may not notice even when intentionally improving performance (D4 Sec. 1). Performance-motivated edits (caching, inlining, memory layout, algorithm swaps) have exactly this trade-off shape [inferred], so selecting only benchmarks that cover the edited function is risky.
3. Non-local effects through shared state: shared caches (CPU), allocator behaviour, GC pressure, import-time/start-up cost, global interpreter state, module-level caches, specialization caches in CPython [inferred]. Coverage-based selection (A3, A4) sees none of these. Layout bias (C3, C4) is one proven non-local mechanism; F5 reports unrelated code changes causing regressions in single benchmarks (weak source).
4. Selection from stale coverage/history. µOpTime and history-greedy TCP use an older run/history (A5, A10); after a series of edits that moves hot paths, the old coverage/profile no longer predicts which benchmarks touch the changed code [inferred]. Perphecy-like or PRICE-like rules are reported to "degrade over time" (A6 abstract).
5. Overfitting to the targeted workload. Performance-motivated edits are typically validated on the benchmark that motivated them; speed-ups may not generalize (D1: many covering tests do not reflect the change; A8: microbenchmark change may be invisible at application level; asv `find` assumes monotonic runtimes F2). [inferred] A benchmark's "improvement" may stem from the benchmark's input size or repetition structure.
6. Test-as-benchmark flakiness. Tests with random operations or I/O create noise (D1); test suites mix correctness and perf concerns, and reduced test sets for correctness (T1/T2 topics) may drop tests that matter for perf [inferred].
7. Warmup/steady-state assumptions shift as edits introduce lazy initialization/caches [inferred; B3, C5 show steady state is not guaranteed even for fixed code].
8. Early stopping by stability criteria (B1, A10) can stop at a "stable" plateau that is not the final steady state; or the criterion's quality is metric- and language-dependent (A10 RQ2: RMAD fine for Go, poor for Java; RCIW preferable for Java).
9. Dependence of consecutive measurements: successive edits tested on the same machine state (thermal, page cache, .pyc state F5) are not independent samples [inferred]; MongoDB notes noise may be time-correlated (E1 Sec. 2).
10. Application-level vs micro-level proxy gap (A8) grows when many micro-edits are accepted by micro-level evidence only.

---------------------------------------------------------------------------

## (e) Candidate deterministic rules (each traced; [inferred] = my synthesis)

R1. Changed-function benchmark selection. Select benchmarks whose recorded call-profile (from a profile or coverage run at the pre-edit commit) includes any changed function or any caller within depth d. Source: A3 (call-graph impact), A4 (dynamic coverage best; total strategy), A8 fn.7 (call graphs). Caveat: Ding D1 and Grambow A8 show coverage is necessary-not-sufficient; use R3-R5 to compensate. [rule inferred]

R2. Pinned inputs and fixed budget. For each selected benchmark, fixed plan of P processes x V values x warmups with loop calibration (e.g. start from pyperf 20x3, 1 warmup [F1]); the plan is part of the acceptance record. Increase to `--rigorous`-like (2x) if the pilot CI is wider than the minimum effect threshold. Sources: F1, C2 (repetition by level). Determinism: fixed counts, fixed seeds, fixed env vars.

R3. Paired/interleaved A/B in one session. Execute baseline and edited builds alternating (ABBA / randomized fixed seed order), same machine, same Python build flags. Source: B2 (randomized order on same instance), C6 (duet), F2 (`--interleave-rounds`). [fixed pseudo-random order is deterministic given seed]

R4. Acceptance rule: accept edit's claimed speed-up only if the CI (95%, bootstrap or t on log-ratio) of the time ratio on the TARGET benchmarks excludes 1 AND the point estimate exceeds a pre-registered minimum effect (e.g. >= max(2 x A/A noise half-width, x%)). Reject if ANY selected non-target benchmark shows a CI entirely above 1 + epsilon (slower) with effect-size above negligible. Sources: C1 (CI comparison), C2 companion (ratio CI), B2 (Wilcoxon/bootstrap), D1 (effect size), F1 (t-test). Epsilon from A/A (R6).

R5. Always include a fixed "sentinel" set irrespective of coverage: a small set of benchmarks chosen once (e.g. highest historical sensitivity per A5 history rule, or broad macro workload per A8's daily application-benchmark recommendation) run on every edit. Sources: A5 (history greedy, <1% overhead), A8 (application benchmark as backstop), D4 (regressions arrive via unrelated changes). [composition inferred]

R6. A/A calibration per benchmark per machine: run original-vs-original with the same plan, derive per-benchmark noise (CV/RCIW) and the minimum detectable effect; benchmarks whose A/A false-positive rate exceeds a threshold are demoted to informational. Sources: B2 Sec. 5.3, E1 (per-test noise; static threshold fails), A10 (stability metrics, RCIW for Java).

R7. Periodic full-suite checkpoint: after every K accepted edits (or when the cumulative touched-function count crosses a bound), run the entire benchmark set against the previous checkpoint AND the original baseline; if any benchmark regresses beyond its MDE, bisect over the K edits (`asv find`-style on the sequence, valid only if roughly monotonic [F2]). Sources: E1 (compare to last stable release; drift), F2 (find), A8 (cheap suite plus periodic comprehensive run). K chosen from the miss-rate budget [inferred].

R8. Cumulative drift check against the ORIGINAL baseline for the selected set at every edit: ratio vs baseline commit must not fall below a threshold even if each step passes. Source: E1 Sec. 1 comparison (3) and "multiple small changes over time" failure mode. [applies to R2-R4 outputs; threshold inferred]

R9. Refresh coverage/profile map after each accepted edit (incremental) or at least at each checkpoint (R7), never reuse a map older than the last checkpoint. Source: A6 (rule decay), A10/A5 (dependence on old run). [inferred]

R10. Deterministic change-point test on the series of per-edit results (optional): apply Hunter-style E-divisive with Student's t-test (deterministic) on the time series of each sentinel benchmark to detect gradual shifts after the fact. Source: E2 (deterministic significance test), E1.

R11. Environment pinning and layout-bias control: fixed `PYTHONHASHSEED`, env size, `pyperf system tune`, ASLR check, same compiler flags/PGO state; for C/Cython changes rebuild both A and B with identical flags and, if feasible, repeat with a second layout (e.g. altered link/object order or extra padding) to see whether the effect survives. Sources: C3, C4 (layout bias), F1 (system), F5 (weak, PGO/.pyc). The second-layout re-run is [inferred].

R12. Dual metric for C-level edits: record instruction counts (CodSpeed-style simulation, F3) in addition to wall time; accept only if both directions agree or the discrepancy is explained. [inferred; F3 limits: excludes I/O and syscalls]

R13. Early stopping only with a fixed deterministic criterion per benchmark: use RCIW (or CV) over a sliding window with fixed threshold and a hard maximum, with the rule frozen per benchmark from the A/A run. Sources: B1 [abstract-only], A10 (RCIW preferable on Java), B3 (reconfiguration still suboptimal). Python applicability [unknown]: no studied Python implementation.

---------------------------------------------------------------------------

## Gaps and cautions
- Full texts NOT read: Perphecy (A2), PerfScope (A1), Laaber FSE 2020 (B1), Laaber/Leitner MSR 2018 (A11), Costa TSE (B4), PRICE (A6) - no OA copy retrievable or hosts unreachable. Numbers for these are abstract-level only.
- No Python-specific peer-reviewed study on benchmark selection or benchmark stability found.
- No study of cumulative drift under many successive small optimizations was found (closest: Daly E1 qualitative; Chen & Shang D4). This is a research gap relevant to the PhD claim.
- No source gives a miss rate for coverage-based benchmark SELECTION (as opposed to prioritization); closest are A8 (false negatives) and D1 (coverage not sufficient).
- Page numbers are not given; section references are from text structure of the downloaded PDFs.

---------------------------------------------------------------------------

## (f) Search log (date: 2026-11-21)

Engine for all: WebSearch (standard mode) unless "WebFetch"/"curl".

| # | Query / action | Notable hits | Not found / notes |
|---|---|---|---|
| 1 | Laaber Würsten Gall Leitner Dynamically reconfiguring software microbenchmarks... | FSE 2020 program page, ZORA record, figshare replication package, sealuzh/jmh | no PDF link in results |
| 2 | Perphecy performance regression test selection made simple but effective ICST 2017 | Waterloo ESG page, SAPE USI page, RIT thesis (Hannigan) | author list in brief wrong (Petkovich); no PDF |
| 3 | PerfRanker ... ISSTA 2017 | taoxiease.github.io PDF, Illinois experts | - |
| 4 | Laaber Applying test case prioritization to software microbenchmarks EMSE 2021 | Chalmers fulltext PDF, PMC, Springer | - |
| 5 | Japke Grambow Leitner Bermbach Using microbenchmark suites... | arXiv 2212.09515, Chalmers, Simula | Japke is not an author of that paper; Japke appears on 2311.04108, 2501.12878, 2510.18640 |
| 6 | Laaber dynamic reconfiguration FSE 2020 pdf zora OR arxiv | Crossref API, uOpTime arXiv | still no PDF |
| 7 | Daly ... change point detection MongoDB ICPE 2020 arxiv | arXiv 2003.00584, SPEC proceedings, Hunter arXiv 2301.03034, arXiv 2505.06758, arXiv 2610.09023 "Evaluating Change Point Detection Methods..." | the last two were not opened (not verified) |
| 8 | Ding Chen Shang ... ICSE 2020 | Waterloo PDF, core.ac.uk | - |
| 9 | Laaber Scheuner Leitner "Software microbenchmarking in the cloud" | Chalmers fulltext, PeerJ preprint, Springer | - |
| 10 | Kalibera Jones Rigorous benchmarking in reasonable time | Kent KAR PDF; arXiv 2007.10899 | - |
| 11 | WebFetch zora.uzh.ch FSE record | ECONNREFUSED | host unreachable |
| 12 | Bulej Duet benchmarking ICPE 2020 | arXiv 2001.05811, SPEC proceedings | - |
| 13 | Unpaywall API for FSE DOI | only ZORA landing, url_for_pdf null | - |
| 14 | Georges Buytaert Eeckhout OOPSLA 2007 | dri.es PDF, core.ac.uk | brief had "Georges, Buytaert" fine; no author named "Georges Buytaert" |
| 15 | Mytkowicz et al. ASPLOS 2009 | Vanderbilt-hosted PDF, USI SAPE | I downloaded from a course-hosting copy (huang.isis.vanderbilt.edu); original authors' page not used |
| 16 | Curtsinger Berger STABILIZER | UMass author page PDF | - |
| 17 | Laaber Leitner MSR 2018 | Chalmers, dblp | no PDF fetched |
| 18 | Costa Bezemer Kalibera "What's wrong with my benchmark results" | Chalmers, Alberta | authors are Costa, Bezemer, Leitner, Andrzejak; Kalibera is NOT an author |
| 19 | Huang Holmes Luo ... ICSE 2014 | PerfScope project page + slides | authors are Huang, Ma, Shen, Zhou |
| 20 | WebFetch arXiv 2604.00222 | Risk-Aware Batch Testing (2026) | - |
| 21 | pdftotext/curl downloads (arXiv, Chalmers, Kent, UMass, Waterloo, SPEC, dri.es, Vanderbilt) | see downloads JSON | Perphecy URL guessed at sape.inf.usi.ch returned 196-byte HTML; deleted. arXiv truncations required retry via export.arxiv.org |
| 22 | WebFetch pyperf Runner/Analyze/System pages | defaults, t-test, tune items | CPU isolation not set by tune |
| 23 | WebFetch asv using.html, commands.html, dev.html, step_detection (404) | continuous, find, compare, interleave-rounds | step detection details not found; dev.html page irrelevant |
| 24 | WebFetch codspeed docs (docs.codspeed.io redirect to codspeed.io/docs/instruments/cpu) | CPU simulation description | Valgrind/cachegrind not named on the page |
| 25 | WebFetch pytest-benchmark comparing page | compare-fail syntax | - |
| 26 | Alshoaibi ... PRICE | researchr, RIT thesis, Springer chapter DOI | brief author names wrong (Hasan/Rahman/Ouni mix); two versions |
| 27 | Python microbenchmark stability pyperformance noise study | python-dev threads, discuss.python.org, arXiv 2510.18640 | no peer-reviewed Python benchmark stability study found |
| 28 | Chen Shang exploratory study performance regression introducing code changes ICSME 2017 | Waterloo PDF | - |
| 29 | WebFetch Waterloo Perphecy page | abstract, no numbers | - |
| 30 | WebFetch discuss.python.org noise-skill thread | noise sources | forum, weak evidence |
| 31 | Stefan et al. unit testing performance in Java projects ICPE 2017 | SPEC proceedings p401 PDF | brief's "Stefan" is first name Petr (Stefan surname) |
| 32 | Leitner Bezemer exploratory study ... ICPE 2017 | SPEC proceedings p373 PDF, PeerJ preprint | - |
| 33 | WebFetch arXiv abs 1602.00602 (Barrett), 2007.10899 (Kalibera & Jones) | abstracts | - |
| 34 | Verification of "µOpTime ICPE 2023" | none: µOpTime is ACM TOSEM 2025 (read in PDF) | the claimed ICPE 2023 paper not found; also no "Japke et al. ICPE 2023 µOpTime" |
| 35 | Verification of "Chen & Shang analysing performance-aware code changes" | found instead ICSME 2017 exploratory study (D4) | other title not verified; dropped |
| 36 | Not searched / not found | Georges follow-ups, Hunter real-world numbers, TSE 2022 version of A5, PRICE full text, pytest-codspeed docs, pyperformance docs | listed as gaps |
