# N5 - Laaber & Leitner (MSR 2018) and three candidate related-work papers

Date: 2026-11-22. Reading only; nothing executed. Labels: [read-in-source §/p], [abstract-only], [fetch-summary], [unknown].
Crossref checked for every item (plain GET https://api.crossref.org/works/<DOI>).

## Important correction to our current sentence
Laaber & Leitner's "covered" is DETECTION-based, not execution-based. A method k is "covered" iff at least one benchmark shows a
statistically and practically significant difference when a sleep-based slowdown is injected into k (Wilcoxon p<0.01 AND relative
mean difference >= half the injected slowdown, in both of 2 runs) [read-in-source §6.2, Eq. 2-3]. So ABS is detectability, a
stronger property than reach (being executed). Our B1 (reach = executed by some benchmark) is a necessary condition for their
ABS, not the same quantity. "Evaluate how well suites detect injected slowdowns" is accurate; "a related property, its reach" is
fair if we say reach is the weaker, execution-only property.

## 1. Laaber & Leitner, MSR 2018
- Crossref [verified]: DOI 10.1145/3196398.3196407; "An evaluation of open-source software microbenchmark suites for continuous
  performance assessment"; Christoph Laaber (Univ. Zurich), Philipp Leitner (Univ. Gothenburg); Proc. MSR '18, pp. 119-130;
  published 2018-05-28; ACM.
- Full text obtained: author version, saved at 01-literature/papers/2018-Laaber-Leitner-Microbenchmark-Suites-MSR.pdf (see
  N5-downloads.json). Source: http://www.ifi.uzh.ch/dam/jcr:ccf1399a-2d57-4ff9-a3b0-59d69616d5d3/msr18-author-version.pdf (link
  found on the MSR 2018 program page https://2018.msrconf.org/details/msr-2018-papers/29/...). %PDF verified, 1,538,492 bytes.
  Not obtainable: ZORA (www.zora.uzh.ch/handle/20.500.14742/148521, found via Unpaywall; connection refused), ACM DL and PeerJ
  preprints (HTTP 403 Cloudflare), typeset.io (403; third-party aggregator, not used), Chalmers record 501018 (no full text).
  NOTE: Chalmers file 536894 is a DIFFERENT paper (Laaber/Gall/Leitner, TCP for microbenchmarks, EMSE 2021); I deleted it.

### Subjects [read-in-source §3, Table 1-2]
10 OSS library/middleware projects, 5 Java (JMH): Caffeine, JCTools, Log4j2, protostuff, RxJava; 5 Go: bleve, etcd, fasthttp, gin, otto.
Chosen from Google BigQuery GitHub extracts (Java files committed in 2015; Go files), ordered by stars/watchers; kept if they compile,
have >10 benchmarks that mostly run, and have non-trivial usage by other OSS projects. Suite sizes 16 (gin) to 983 (RxJava).
Benchmarks: Caffeine 89, JCTools 169, Log4j2 437, protostuff 31, RxJava 983; bleve 70, etcd 41, fasthttp 99, gin 16, otto 49
(JMH parameterised benchmarks counted per parameter combination).

### Suite duration [read-in-source §4.2-4.3, Table 2]
Whole suite run 5 times in two environments: bare-metal (12-core Xeon X5670, 70 GiB) and a Google Compute Engine VM (text says
"n1-standard-26" but also "two virtual CPUs, 7.5 GB" - a typo in the source). Mar-May 2017. A uniform default JMH config was
imposed (10 warmup, 20 measurement iterations, 1 fork) because developer overrides are not visible in repos; Go: each benchmark
repeated 20 times. Mean single full-suite duration, hours, bare-metal / cloud:
Caffeine 0.79/1.81; JCTools 2.28/2.30; Log4j2 4.76/4.61; protostuff 0.25/0.26; RxJava 8.75/8.72;
bleve 1.16/0.92; etcd 0.63/0.72; fasthttp 1.30/1.20; gin 0.19/0.18; otto 0.55/0.50.
So "11 min" = gin bare-metal 0.19 h; "8.75 h" = RxJava bare-metal. These are wall-clock under THEIR imposed configuration, not the
projects' own configured durations. Run-to-run std dev <= 0.17 h. Duration tracks suite size (each benchmark runs ~fixed time).
Also [§5.3]: variability maxSpread >= 50% for some benchmarks; only slowdowns >50% (most Java) / >25% (Go) reliably detectable in cloud.

### Injected-slowdown method [read-in-source §6.2]
Mutation-testing inspired. Per project |K'| = 20 "often-used" public API methods. Chosen by tracing invocations of the subject's public API
from the unit tests of 4-6 other GitHub projects that depend on it (AspectJ load-time weaving for Java; AST rewriting for Go; Table 4
trace counts), top-used taken. Not chosen by change history. Slowdown size v per project: v = 2 x maxSpread at the 95th percentile
of the suite's benchmark stability. Implementation: AST transformation (javaparser / Go ast) measures the method body time t(k) and
appends Thread.sleep / time.Sleep of v x t(k). Table 5 v values: Caffeine 2.6, JCTools 1.0, Log4j2 1.0, protostuff 1.0, RxJava 0.6;
bleve 0.1, etcd 0.3, fasthttp 0.2, gin 0.2, otto 0.2. One injection at a time; each needs a full suite run; 2 repetitions
=> 2(|K'|+1) suite executions per project, 7.5 h (gin) to ~15.3 days (RxJava). Total injections 200 (derived: 20 x 10).

### Detection criterion and ABS [read-in-source §6.2, Eq. 2-3]
re(M_rbk, M_rb) true iff Wilcoxon rank-sum p<0.01 AND |mean_mut - mean_base|/mean_base >= v/2, in both runs. covered(k,B,v)=1 iff some
benchmark b has re true. ABS(K',B,v) = 100 x sum_k covered(k) / |K'|. Variants: total, relative (drop worst 5% by maxSpread),
absolute (drop maxSpread > 0.5). Results total/rel/abs (Table 5): Caffeine 65/60/60; JCTools 55/55/55; Log4j2 80/40/40; protostuff
40/35/35; RxJava 95/95/95; bleve 100/100/100; etcd 10/10/10; fasthttp 95/95/95; gin 65/65/65; otto 60/60/60 => the "10%-100%".
Redundancy: many benchmarks detect slowdowns in the same few methods (Fig. 3). They note there is no similar coverage-like metric for
microbenchmarks (§6.2) and put "covered" in quotes.

### Coverage of changed methods?
[read-in-source] Nothing about real commits or real optimizations; the only changed code is the 20 synthetic injection sites per project.
No execution-coverage tool is used; "covered" = detected, so ABS conflates reach with sensitivity/noise (e.g. Log4j2 80% -> 40% when
unstable benchmarks are removed; etcd 10% is attributed to the API not reflecting performance-critical code). They list as threats that
20 methods may be too few and that usage in others' unit tests is a proxy for importance [§7.2].

## 2. Traini et al., How Software Refactoring Impacts Execution Time
- Crossref [verified]: DOI 10.1145/3485136; ACM Trans. Softw. Eng. Methodol. 31(2), pp. 1-23 (Article 25), issued 2021-12-24 (issue
  dated 2022; also ASE 2022 journal-first). Authors (9): Luca Traini, Daniele Di Pompeo, Michele Tucci, Bin Lin, Simone Scalabrino,
  Gabriele Bavota, Michele Lanza, Rocco Oliveto, Vittorio Cortellessa. (The candidate list "Lin, Sun" was off: no Sun; Scalabrino,
  Bavota, Lanza, Oliveto are authors.)
- Read in full: https://rocoli.github.io/pubs/tosem2021refactoring.pdf (author-hosted, 1,373,966 bytes; not saved to papers/). The
  usi.ch copy returned 403. No arXiv copy found [unknown whether one exists].
- Study [read-in-source §2.1]: Java systems with JMH suites; RefactoringMiner found 494,826 refactoring operations (48 types) in 43,008
  commits of 31 projects (7 rename/package types ignored). Each benchmark run 1 s under Java Flight Recorder at the pre- and
  post-commit snapshots to get the methods it executes (221 machine-days, 4M+ benchmark executions, 7,901 snapshots). 39,665 commits
  discarded (22,938 = 58% had no benchmark suite yet; rest unbuildable), 3,343 retained. A benchmark is "suitable" for a refactoring iff
  it executes >=1 method touched by it: 3,533 data points over 201 commits, 521 refactorings, 26 projects. Final measured set: 82 commits,
  167 refactorings, 20 systems.
- What it says about benchmarks covering changed methods:
  (a) RQ1 [§2.2.2, §3.1, Fig. 2]: a method is "performance-relevant" if executed by >=1 benchmark. They compare refactoring DENSITY
  (share of methods refactored) in benchmark-executed vs other methods: below 1.5% in both; density higher in non-relevant methods in
  most projects (significant except jooby, vert.x; camel is the reverse). This is a per-method density, not a per-commit coverage rate.
  (b) Implicit commit-level filter: 201 of 3,343 retained commits (about 6.0%) touched >=1 benchmark-executed method. This is MY
  derivation; the paper does not state it, and the denominator may include commits whose refactorings are only of excluded types.
  Hedge if cited.
- Not about optimization commits or injected regressions; refactorings in Java.
- Side note [§ related work]: it describes Chen & Shang as studying Python; Chen & Shang actually study Java (Hadoop, RxJava).

## 3. Chen & Shang, ICSME 2017
- Crossref [verified]: DOI 10.1109/ICSME.2017.13; "An Exploratory Study of Performance Regression Introducing Code Changes"; Jinfu Chen,
  Weiyi Shang; 2017 IEEE ICSME, pp. 341-352; Sept 2017; IEEE. Local PDF read [read-in-source].
- Subjects: 1,126 commits from ten Hadoop releases and 135 commits from five RxJava releases evaluated [abstract, §II]. Hadoop: tests
  chosen per commit by naming heuristic (TestX.java for X.java); RxJava: all 76 microbenchmarks run on every commit. Each test run 30
  times; t-test plus effect size.
- Coverage of commits: NOT reported as a rate. Counts given are only: filter to commits changing .java files; 132 tests/106 commits use
  new tests, 21 tests/19 commits dropped, only six commits excluded because all their tests failed/did not compile [§II-2]. No count of
  commits whose changed code the tests/benchmarks execute or miss. Threats section ("The effectiveness of the tests"): heuristic and
  microbenchmarks "may not cover all the performance impacts from code changes" (qualitative only).

## 4. Jangali et al., ju2jmh, IEEE TSE
- Crossref [verified]: DOI 10.1109/TSE.2022.3188005; "Automated Generation and Evaluation of JMH Microbenchmark Suites From Unit Tests";
  Mostafa Jangali, Yiming Tang, Niclas Alexandersson, Philipp Leitner, Jinqiu Yang, Weiyi Shang; IEEE TSE 49(4), pp. 1704-1725; issued
  2023-04-01.
- Read: https://ece.uwaterloo.ca/~wshang/pubs/MOSTAFA_TSE_2022.pdf (author version on co-author's page, 4,163,219 bytes; not saved).
  No arXiv found.
- Study [read-in-source §1, §5]: ju2jmh turns JUnit tests into JMH benchmarks; evaluated on RxJava, eclipse-collections, zipkin (454K SLOC,
  2,417 JMH benchmarks = 2,262 manual + 155 AutoJMH, 35,084 JUnit tests evaluated of 171,366 ju2jmh built). Their PMT framework injects
  artificial performance bugs (5 mutation operators, 149K mutants generated, a subset selected, favouring mutants covered by more tests).
- Coverage: yes, execution-based, per test type. RQ2 summary: ju2jmh covers (executes) 100% of mutants vs 66% for manual JMH; but Table 7
  total shows 46 of 155 = 29.7% for manual JMH; the paper's two figures disagree - flag when quoting. Mutants were selected from code
  covered by tests, so not a rate over random locations or real changes.
- Real regressions [RQ3]: ONE real bug (Storio, fix commit 566d3e9, 21 covering JUnit tests) compared against a similar injected mutant.

## Closeness to B1 (one line each)
- Laaber & Leitner: same suite-level question, but measures DETECTION of sleep slowdowns at 20 usage-ranked API methods x 10 Java/Go
  libraries, not execution reach of functions changed by real optimization commits (Python).
- Traini et al.: closest in method (JFR profile of which methods each JMH benchmark executes, per commit); but Java refactorings, reported
  as per-method density; no stated "fraction of commits with no covering benchmark" (my derived ~6% of retained commits touch one).
- Chen & Shang: runs tests/microbenchmarks per commit but reports no covered/uncovered count, only a qualitative threat.
- Jangali et al.: execution coverage of injected mutants by test type (manual JMH 29.7-66%), synthetic mutants, Java, one real bug; no
  real optimization commits.

## Suggested wording
"Laaber and Leitner evaluate whether Java and Go microbenchmark suites detect slowdowns injected into 20 often-used API methods per
project; we instead measure the weaker, execution-based property (reach) for the functions that real optimization commits changed."
Consider also citing Traini et al. 2021 for method-level dynamic benchmark reach on real (refactoring) commits.
