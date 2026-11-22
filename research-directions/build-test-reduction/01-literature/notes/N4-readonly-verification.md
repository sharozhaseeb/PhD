# N4 read-only verification (2026-11-22)

Labels: [read-in-source §/p] = read in a locally saved PDF text; [fetch-summary] = fetch-model summary of a web page, not read directly; [unknown].
Nothing downloaded was executed. PDFs saved: see N4-downloads.json (Shahedi, FormulaCode, Henning). Not obtained: Grambow PeerJ 2021 PDF (PeerJ/PMC/EuropePMC PDF endpoints returned HTML, 1.8-5.6 KB), Laaber & Leitner MSR 2018 PDF (Chalmers, ZORA, typeset/scispace returned HTML or errors).

## Part A

### A1. Shahedi et al. 2025 (arXiv 2508.07084, Java/JMH) - VERIFIED exclusion; rate NOT reported
- Exclusion: [read-in-source §4.6.3, p.18] "If no benchmarks targeted the changed methods, we excluded the commit from analysis". Same sentence says benchmarks "typically have lower coverage rather than unit tests" (cites Traini 2021, Stefan 2017, Laaber & Leitner 2018, Chen & Shang 2017).
- Limitation: [read-in-source §7 Threats, "Missing Data Points"] "a substantial number of commits were excluded due to being unbuildable or lacking microbenchmark coverage". Unbuildable and no-coverage are lumped together.
- Rate: [read-in-source Table 1] no count or percentage of "excluded for no covering benchmark". Table 1 gives per-project columns Commits, Commits with Method Changes, Commits with Benchmarks, Candidate Commits, Executed Commits, Collected Method Changes. Executed is far below Candidate (e.g. netty 2,472 candidate, 56 executed) but that gap mixes weighted sampling (§4.5, compute limit), build failures and no-coverage. Table text extraction is garbled for several rows. Conclusion: exclusion exists, rate is not separable or reported. Correct any note implying a rate.
- How coverage was determined: [read-in-source §4.6.3] each JMH benchmark run once (1 fork, 1 iteration, 1 s, no warm-up) with JIB bytecode agent to see which invoke the modified methods.

### A2. FormulaCode (arXiv 2603.16011) - "% Coverage 41.24%": DEFINITION NOT GIVEN
- PDF obtained in full (3,430,646 bytes, %PDF, 4,225 text lines); HTML also fetched.
- [read-in-source Table 1, p.5, caption "(Micro-averaged) statistics characterizing different attributes of a FORMULACODE task instance"]: group "Workloads", rows "# Eval. Fns 264.58 (max 1364)" and "% Coverage 41.24% (max 97.86%)". Note the PDF row label is "# Eval. Fns" while the text calls 264.58 the number of workloads per task (§3.2; Table of benchmarks).
- Searched the whole PDF for coverage, exercise, covered, coverage.py, line cover: no definition. Only prose: [read-in-source §6 Limitations] "a patch's measured gain reflects only the code paths that the workloads exercise"; [App. A.9 "Dependence on ASV workloads"] "If community-maintained workloads do not exercise the performance-critical paths modified by a pull request, the benchmark signal may be incomplete."
- So what is covered over what (diff lines? repo lines? functions?) is [unknown]. Do not state it as diff coverage. Safest wording: "Table 1 reports a mean '% Coverage' of 41.24% for workloads; the paper does not define the metric."
- Other facts: [read-in-source §3.1-3.2] 957 tasks, 70 repos, asv repos found by asv.conf.json (766 repos), perf-intent PRs, kept only if workloads show a significant speedup after the expert patch (so conditioned on at least one workload responding). Own-repo asv suites.

### A3. Quansight 2021 blog (Rodriguez-Guerra, "Is GitHub Actions suitable for running benchmarks?", labs.quansight.org/blog/github-actions-benchmarks; dev.to mirror) - mostly VERIFIED, definitions partly absent
All [fetch-summary] (dev.to mirror fetched; labs.quansight.org returned HTTP 429). Blog not read directly.
- A/A design: two commits identical in tested code; ideal ratio 1.0; scikit-image asv suite, 75 benchmarks per run.
- Schedule: GitHub Actions workflow every 6 h (4/day) for 16 days; ~64 runs.
- Tool/factor: `asv continuous A B` (interleaved A-B-A-B passes, default processes=2); default threshold factor 1.2.
- Variants (runtime, FP, min, max): default interleaved 1h55, 3.7% (4/108), 0.51-1.36; no interleaving 1h39, 9.99% (6/66), 0.43-1.50; single pass 1h07, 12.5% (8/64), 0.51-2.76.
- Flags: 6/66 = 9.09%, so "9.99%" appears to be the blog's own typo (or rounding quirk); denominators 108/66/64 are not explained in the summary (108 does not match 64 runs). FP definition: an outlier where asv would report a regression that does not exist; no explicit cutoff stated in the summary, and it is [unknown] whether the cutoff is the 1.2 factor. Cite as "3.7%, 9.99% (sic), 12.5%" only with this caveat and re-check on the original page when reachable.
- Search snippet (labs page) also: observed ratios "between 0.6 and 1.5" in practice, sensitive to regressions of more than 50%.

### A4. Henning et al. 2025 - VERIFIED (title/venue corrected)
- Exact: S. Henning, A. Vogel, E. Perez-Wohlfeil, O. Ertl, R. Rabiser. "When Should I Run My Application Benchmark? Studying Cloud Performance Variability for the Case of Stream Processing Applications." FSE Companion '25 (33rd ACM Int. Conf. on the Foundations of Software Engineering, industry track), DOI 10.1145/3696630.3728563; arXiv 2504.11826. Full PDF saved and read.
- What was measured: [read-in-source Abstract, §4-5] a Dynatrace stream-processing application benchmark (ShuffleBench) run repeatedly on AWS: >3 months, ~591 h, 789 Kubernetes clusters, 2,366 benchmark executions. Measured throughput. RQ1 overall variability (50% of results within -2.4%/+2.3% of median, §5.1), RQ2 daily pattern (§5.2; runs every 6 h, every 3 h for ~3 weeks; US/Eastern; hours 0:00-6:00 significantly different), RQ3 weekly, RQ4 long-term, RQ5 infrastructure reuse, RQ6 machine type, RQ7 region.
- Abstract quote: "exhibit a daily and weekly pattern, although with only small variability" (<=2.5%). It is an application benchmark on cloud clusters, not microbenchmarks, not Python, not asv. Companion paper arXiv 2510.12397 ("Should I Run My Cloud Benchmark on Black Friday?") is separate.
- N2 note cited it as "591 h on AWS, CV<3.7%, daily/weekly <=2.5%" and [abstract-only]: upgrade to read-in-source for the 591 h / 2.5% facts; the "CV<3.7%" figure was not re-verified here.

### A5. Laaber & Leitner MSR 2018 - numbers confirmed from abstract only; full text NOT obtained
- DOI 10.1145/3196398.3196407, pp.119-130. Chalmers portal page (research.chalmers.se/publication/501018) fetched: no PDF link; no ZORA/typeset/scispace PDF retrievable.
- [fetch-summary of Chalmers abstract + search snippet] ten open-source Java and Go libraries; suites of 16 to 983 tests; runtimes "between 11 minutes and 8.75 hours"; injected slowdowns into public API methods; API benchmarking score (ABS) "varies between 10% and 100%"; some benchmarks have result variability of 50% or higher.
- Verified as stated in the abstract: "11 min to 8.75 h" and "ABS 10-100%". Which project has which value, section and table: [unknown] (not read). ABS measures the share of injected slowdowns in core API methods that the suite detects (abstract-level description).

## Part B: comparison with B1
B1 = for real performance-improving commits mined from a Python project's git history (networkx), the fraction whose changed functions are executed by NONE of the project's own asv cases: 9/15 by measured per-case profile, 4/15 by static reach.

### B-1. Shahedi et al. 2025 (read in full where relevant; PDF)
- Unit: commits containing method-level changes; changed methods. Java, 15 OSS projects (Table 1), project's own JMH microbenchmarks. Coverage = whether a benchmark invokes a modified method, measured by bytecode instrumentation (JIB) on a short run (§4.6.3).
- Commits are NOT selected as performance-improving: all non-merge commits with Java production changes after benchmarks exist (§4.2); outcomes afterward: 14.2% of 1,499 method changes improve, 18.5% regress, 67.3% unchanged (§5.2).
- Numbers: 739 commits executed, 1,499 method-level changes, 15 projects. No fraction without covering benchmark.
- Difference from B1: coverage was a filter to drop commits, not an outcome; no rate; mixed regress/improve/neutral commits; Java/JMH; no per-case static vs measured comparison.

### B-2. Grambow et al., "Using Microbenchmark Suites to Detect Application Performance Changes" (IEEE TCC 2022; arXiv 2212.09515; PDF read)
- Unit: commits in a series (VictoriaMetrics 70 commits, InfluxDB 110 commits, §3.1) and call-graph nodes (functions). Go, each project's own microbenchmarks (VictoriaMetrics 177 microbenchmarks; InfluxDB 426 falling to 109 across the period, §3.1). Reference is an application benchmark (YCSB-TS-based), not the changed code.
- "Coverage"/practical relevance = share of project functions called in the application-benchmark call graph that also appear in the microbenchmark call graphs (§2 Removing Redundancies; §4 Computing Optimized Suites). Numbers: VictoriaMetrics 314 of 634 project functions covered (about 50%); InfluxDB complete suite relevance about 40% at commit 15 (269 of 660 nodes), optimized 10-benchmark suite 36% (§4). Complete suites run for every 5th commit; optimized suite every commit.
- Performance-improving commits: no selection; whole commit series, detected changes include improvements and regressions (e.g. InfluxDB commit 37 speeds queries ~25%/15%). Question is whether the microbenchmark suite detects app-level changes; false alarms 17 and 27 commits for the optimized suite. One missed change (commit 48) is attributed to the runtime environment (profiling activation).
- Difference from B1: denominator is app-benchmark functions, not changed functions of perf commits; no per-commit "changed function reached by no benchmark" rate; Go, DB systems.

### B-3. Grambow et al., PeerJ CS 2021 (PMC8176533) [fetch-summary only; PDF not obtained]
- Unit: call-graph nodes (functions) at one fixed version per project. Coverage: functions called in the application benchmark that also appear in at least one microbenchmark graph, project-only and overall; structural node overlap only (no edge/line/path coverage).
- Projects: InfluxDB 1.7 (347 microbenchmarks, 288 call graphs) and VictoriaMetrics v1.29.4 (65 microbenchmarks, 62 call graphs); Go; own suites; app benchmark YCSB-TS in three scenarios (Table 2).
- Numbers (Table 3): InfluxDB overall 62.90-66.29%, project-only 40.43-41.25%; VictoriaMetrics overall 43.50-47.74%, project-only 35.62-40.43% (text says 46.74% max, table 47.74%: inconsistency in the source as summarized). Redundancy removal: 288 -> 19-27; 62 -> 13-14 benchmarks.
- No commits, no performance-improving changes studied.
- Difference from B1: no commits, no diffs; coverage of app-benchmark call graph, not of changes.

### Net position for B1
None of the three reports "fraction of real performance-improving commits whose changed functions no project benchmark executes", nor compares measured per-case profile with static reach. Closest premise-level evidence: Shahedi (drops uncovered commits, rate unreported), Grambow (functional overlap 36-66%), FormulaCode (mean "% Coverage" 41.24%, undefined). B1 appears distinct, with the caveat that the search was not exhaustive.
