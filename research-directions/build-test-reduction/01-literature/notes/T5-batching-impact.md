# T5 - Batching, checkpointing, culprit finding in CI; change-impact analysis as selection basis

Researcher notes, 2026-11-21. Study context: Python code optimized through many small performance-motivated edits; each edit validated with reduced build + reduced tests/benchmarks; periodic FULL checkpoints; mandatory final full validation; culprit finding when a checkpoint fails. No AI in the method.

Evidence labels: **[read-in-source]** = I read the text (PDF via pdftotext, or HTML/PDF fetched); location given. **[read-fetch-summary]** = page fetched with the WebFetch tool, whose small model summarised it; section numbers come from that summary and should be spot-checked. **[abstract-only]** = abstract / search snippet / landing page only. **[inferred]** = my reasoning, not in a source. **[unknown]** = could not establish.

PDFs saved: see `T5-downloads.json` (9 files). Bib: `T5.bib`.

---

## (a) Source cards

### S1. Najafi, Rigby, Shang, "Bisecting Commits and Modeling Commit Risk during Testing", ESEC/FSE 2019, pp. 279-289. PDF saved.
- Setting: batch testing at Ericsson, 3 projects, 9 months of data, simulation of batch sizes 1-20. [read-in-source, Abstract, Sec. 4]
- Bisection cost: binary search needs about 2*log2(n) executions per culprit (Eq. 1; Fig. 1 states 2*log2(n)+1; example: 4 commits -> 5 executions if the batch fails, 1 if it passes). [read-in-source, Sec. 2 / Fig. 1]
- Best batch size depends on CulpritRate (per-project culprit proportion: 6.8%, 8.6%, 2.8% for A,B,C): higher culprit rate -> smaller best batch. Savings versus testing every commit: 34%/34%/44% at batch size 2; max 50%/47%/74%; most savings by size 4; project C plateaus above size 9. [read-in-source, Sec. 5.1, Fig. 5]
- Flaky batch failures cost an extra bisection: #FlakyExecutions = #Batches x FlakeRate x 2 log2(n) (Eq. 7); Total = CulpritExecutions + FlakyExecutions (Eq. 8). FlakeRate (batch-level) 23.6%/23.1%/16.9%; with flakiness the best size for project C drops from 9 to 4 and savings from 72% to 41%. [read-in-source, Sec. 4.1, 5.2; abstract says 72% -> 42%]
- Risk-guided bisection "TestTopK": test top-K riskiest commits individually, rest as one batch. Risk models: BugModel (Kamei-style) and TestExecutionHistory (P(file fails test), Eq. 2-3, normalised by lines changed). TestExecutionHistory Top2 saves 9.0% / 7.6% executions vs Ericsson's plain bisection (projects B, C, batch size 4). [read-in-source, Sec. 3, 5.3, Table 1]
- Stated assumption: a flaky batch costs the same as finding one culprit (2 log2 n), conservative. [read-in-source, Sec. 6.3]. Multiple culprits per batch occur, so Top1 alone is often insufficient. [read-in-source, Table 1 note]

### S2. Beheshtian, Bavand, Rigby, "Software Batch Testing to Save Build Test Resources and to Reduce Feedback Time", IEEE TSE (online 2021; DOI 10.1109/TSE.2021.3070269); ICSE 2022 journal-first. PDF NOT obtained (no open full text found). [abstract-only]
- Six strategies on Travis CI projects: TestAll, BatchBisect, Batch4, BatchStop4 (Batch4 + bisection with a stopping condition), RiskTopN, RiskBatch. Execution reductions vs TestAll: 46%, 48%, 50%, 44%, 49% (BatchBisect, Batch4, BatchStop4, RiskTopN, RiskBatch). Feedback-time reductions 33%, 16% (Batch2), 32%, 37%. Failure rate correlates strongly with savings (Spearman r = -0.97); every project with build failure rate below 40% benefits; with Batch4, 85% of projects save. "No slip-throughs" because failing batches are re-tested. [abstract-only, ICSE 2022 journal-first page]
- Fallahzadeh et al. (S3) state that BatchStop4 "has been shown both mathematically and empirically" to be the top approach, citing this paper. [read-in-source, S3 Sec. 3.2] The mathematical model itself: [unknown] (paper not read).

### S3. Fallahzadeh, Bavand, Rigby, "Accelerating Continuous Integration with Parallel Batch Testing", ESEC/FSE 2023 (arXiv 2308.13129v1). PDF saved.
- Compares TestAll, ConstantBatching (Batch2, Batch4), BatchAll (dynamic size = whole queue), TestCaseBatching, on Chrome (276M test cases, 9,524 changes) and Ericsson data. No closed-form formula tying batch size to failure rate (Eqs 1-4 are feedback time / execution reduction only). [read-fetch-summary of Sec. 2.1, 3, 4; spot-checked: text mentions 40% failure threshold and Dorfman]
- Names Dorfman as an example culprit-finding family alongside bisection ("approaches like Dorfman and bisection [18, 44]"); ref [18] is Dorfman 1943, Ann. Math. Stat. 14(4):436-440. The paper uses BatchStop4, not Dorfman. [read-in-source, Sec. 3.2 and reference list]
- Reported: Batch4 on Chrome 75% fewer executions, 61 vs 217 machines; BatchAll 99% down to 9% execution reduction as machines rise. [read-fetch-summary, Sec. 4.2-4.3, Table 1]; threat: only tests Ericsson guarantees independent are batched; no re-runs simulated. [read-fetch-summary, Sec. 6]
- Also in Related Work: bisection cost bounded by 2 log n up to 2n+1 executions. [read-fetch-summary, Sec. 7]

### S4. Memon et al., "Taming Google-Scale Continuous Testing", ICSE-SEIP 2017, pp. 233-242. PDF saved (IEEE copy via Vanderbilt course page).
- TAP cannot test each change individually: compute grew quadratically (submission rate x test-pool size, both linear). Remedy: "milestones": bundle consecutive commits, run once per milestone (typically every 45 min at peak; up to 4.2M tests selected via reverse dependencies on changed files since previous milestone; delays up to 9 h observed). Tests are run at their latest affecting change only. [read-in-source, Sec. I, Sec. II-III]
- 5.5M affected tests analysed; only 63K ever failed; 1.23% of executions found a breakage/fix; PASS:FAIL ratio per change 99:1. Tests >10 dependency edges from changed code hardly ever break; files edited by >3 developers break more. [read-in-source, Sec. I and III-IV]
- Culprit finding: when a milestone fails, "any of the N changelists between the P and F may have caused the breakage"; the culprit is known for sure only when there is no AFFECTED (unexecuted) outcome between PASSED and FAILED (77% of edge targets). [read-in-source, Sec. IV, Fig. 11 text]
- Idea of running low-risk tests less often than risky ones is the motivation, not a deployed result in this paper. [read-in-source, Sec. I, IV]

### S5. Ziftci & Reardon, "Who Broke the Build? ...", ICSE-SEIP 2017, pp. 113-122. PDF NOT obtained (research.google page has no PDF link). [abstract-only]
- Heuristic algorithm ranking changes; case studies on 140 Google projects; culprit in the top 5 among thousands of candidates 82% of the time. Related Google patent US9176731 (not read).

### S6. Henderson et al., "Flake Aware Culprit Finding" (FACF), ICST 2023 industry track. PDF saved (author preprint).
- Problem: tests run only at milestones, many tests skipped as unaffected, so a failure at milestone m has a search range of changes; flaky tests add noise. Traditional bisect (git-style) ignores flakiness; with k reruns to deflake, accuracy plateaus while cost grows linearly. [read-in-source, Sec. I-II]
- Algorithm: Bayesian noisy binary search over the suspects, input = prior distribution, estimated flake rate f_t, suspects; posterior updated by Bayes rule after each pass/fail (Eq. 2-8, Algorithms 2-3); can run k parallel runs; returns most likely culprit or NONE (flake). Best-case logarithmic builds. [read-in-source, Sec. III]
- Priors: static build-graph filtering plus minimum build distance between changed files and the test; historical probability of real breakage vs flake. Flaky tests get reruns at the failure-detecting version first. [read-in-source, Sec. III-C]
- Evaluation: 13,000+ test breakages at Google; accuracy via a verification system with reruns to a stated confidence; cost = number of test executions. [read-in-source, Abstract, Sec. IV-V]. I did not extract the headline accuracy/cost numbers: [unknown] (not captured; read Fig. 2-3 and Sec. V-F if needed).
- A search range with no true culprit (pure flake) is a first-class outcome. [read-in-source, Sec. IV-B]

### S7. Ananthanarayanan et al. (Uber), "Keeping Master Green at Scale", EuroSys 2019. PDF saved (third-party blog host).
- Describes batching with split-on-failure ("if a batch fails it is divided into smaller batches and retried"), notes it does not scale as failures rise with batch size; contrasts with SubmitQueue's speculative builds ordered by logistic-regression success probability and a conflict graph for independent changes. [read-in-source, Sec. 2.2]
- Conflict data: with two concurrent potentially-conflicting changes there is a 5% chance of a real conflict, rising to 40% with 16; 1000 changes/day x 30 min build serialised gives >20 days for the last change. [read-in-source, Sec. 2.1-2.2, Fig. 1]. "Real conflict" = each change passes alone but together break the mainline. [read-in-source, Sec. 2.1]
- Follow-up (abstract only): Juloori et al., ICSE 2025, arXiv 2501.03440: 53% less CI resource use, 44% less CPU, 37% lower P95 wait. [abstract-only]

### S8. Zeller, "Yesterday, my program worked. Today, it does not. Why?", ESEC/FSE 1999 (LNCS 1687, pp. 253-267). PDF saved.
- Given N changes where none applied works and all applied fails, finds a minimal failure-inducing change set. Claims: arbitrary interference in linear time; single failing change in logarithmic time; handles inconsistent (untestable) configurations (dd+). [read-in-source, Sec. 1]
- Interference = several changes each fine alone but failing together (frequent when merging parallel work). [read-in-source, Sec. 1]
- dd returns a minimal set only if the configuration is monotone, unambiguous and consistent; for non-monotone or ambiguous cases it still returns a failure-inducing set (possibly not minimal / one of several). Inconsistent configurations (change cannot be applied, build fails, run fails) produce UNRESOLVED outcomes and are the main practical problem. [read-in-source, Defs 6-8, Sec. 4-5]
- Case studies: GDB 178,000 changed lines isolated within hours; DDD with 116 logical changes. [read-in-source, abstract, Sec. 7]

### S9. Zeller & Hildebrandt, "Simplifying and Isolating Failure-Inducing Input", IEEE TSE 28(2):183-200, 2002. PDF saved.
- ddmin (minimizing) and dd (difference isolating) over a passing/failing pair. ddmin worst case |c|^2 + 3|c| tests; best case logarithmic when a single element is responsible. [read-in-source, Sec. III-C, Prop. 12-13; the PDF text layer is garbled so exact exponents should be checked against the page]
- Outcomes PASS/FAIL/UNRESOLVED; 1-minimality; Mozilla HTML case 896 lines -> 1 line (from search summary, [abstract-only]).

### S10. Jin & Servant, "What helped, and what did not? ...", ICSE 2021, pp. 213-225. PDF saved.
- 14 variants of 10 techniques on 100 Travis projects (13,464 failing builds out of 82,427 per fetch summary). Techniques include build skipping (SB_Abd19 = the Abdalkareem rule-based CI-skip), test selection (Gligoric15 = Ekstazi-style, Herzig15, Machalica19) and prioritization (Liang18 = continuous prioritization). [read-fetch-summary, Sec. III-IV]
- Savings and missed failures trade off: cost-saving ranking nearly the reverse of the missed-failure ranking. SB_Abd19 saved a median 21% build time, still missed failing builds; "skipping builds with no-code changes ... is not enough to guarantee" they will not fail. [read-fetch-summary, Sec. IV-C2, VI-B; the "missed failure observation" dimension D2 spot-checked in PDF text]
- Skipped builds' changes accumulate into the next executed build (implicit batching). Periodic full runs are not studied. [read-fetch-summary, Sec. III-B]

### S11. Jin & Servant, "HybridCISave", ACM TOSEM 32(4):93, 2023. [abstract-only] Combines build-level skipping and test-level selection with a Random-Forest predictor over the outputs of several techniques; more savings than previous build-selection techniques over 100 projects. PDF author-hosted at jxianhao.github.io (not downloaded).

### S12. Abdalkareem et al., "Which Commits Can Be CI Skipped?" (TSE). [abstract-only; author PDF URL returned 404]
- 1,813 explicitly skipped commits in 58 Java projects; rule-based technique (e.g. meta-files, release-prep changes), average 18.16% fewer CI-triggering commits; tool CI-SKIPPER. A later ML paper by the same group notes rules produce false negatives, and an independent study found even rule-skipped commits sometimes ended in failing builds (S10). Year uncertain (see bib).

### S13. Liang, Elbaum, Rothermel, "Redefining Prioritization: Continuous Prioritization for Continuous Integration", ICSE 2018, pp. 688-698. [abstract-only] Prioritizes commits (not tests) as an alternative to running every full CI cycle; evaluated on three CI datasets.

### S14. Change-impact analysis papers
- Arnold & Bohner, "Impact Analysis - Towards a Framework for Comparison", ICSM 1993 pp. 292-301: framework (how used / how it works internally / effectiveness) and definition "identifying the potential consequences of a change, or estimating what needs to be modified". [abstract-only] My brief named a 1996 book chapter; that book (Bohner & Arnold, eds.) I did not verify: [unknown].
- Lehnert, "A taxonomy for software change impact analysis", EVOL/IWPSE 2011, pp. 41-50, DOI 10.1145/2024445.2024454. Metadata only: [unknown] content.
- Law & Rothermel, "Whole Program Path-Based Dynamic Impact Analysis" (PathImpact), ICSE 2003, pp. 308-318. Original not read. Described in S15.
- Orso, Apiwattanapong, Harrold, "Leveraging Field Data for Impact Analysis and Regression Testing", ESEC/FSE 2003, pp. 128-137 (CoverageImpact with field data). [abstract-only]: field data can substantially change dynamic-analysis results (20 changes).
- Ren et al., Chianti, OOPSLA 2004, pp. 432-448. [abstract-only]: decomposes a version diff into atomic changes and reports affected tests; on a year of Daikon CVS history ~51% of unit tests were affected, each affected test by on average 3.88% of atomic changes. Mentions helping debug a test that fails after a long editing session, i.e. close to our culprit-among-edits problem.
- S15. Orso, Apiwattanapong, Law, Rothermel, Harrold, "An Empirical Comparison of Dynamic Impact Analysis Algorithms", ICSE 2004. Read in full text (fetched copy, not saved into papers/). CoverageImpact and PathImpact compute impact relative to execution data for a specific input set; "safe with respect to the dynamic information used", i.e. nothing excluded that could be affected given the observed executions; PathImpact more precise (uses traces, whole-path DAG), CoverageImpact cheaper (coverage bit vectors). [read-in-source, Sec. 1-2.3]

### S16. Python call graphs
- Salis et al., PyCG, ICSE 2021 (arXiv 2103.00587). PDF saved. Handles higher-order functions, closures, classes/MRO, modules, generators; ignores conditionals/loops (flow-insensitive), does not analyse eval/code generation, does not track built-in types (list.append unresolved), ignores getattr/setattr, skips modules without source. Micro-benchmark: 112 programs, complete in 111 and sound in 103; macro-benchmark 5 packages each under 3.5k LoC, average precision 99.2%, recall 69.9%. [read-fetch-summary, Sec. III-C, V-B, V-C; precision/recall also in the arXiv abstract]
- Huang et al., Jarvis (arXiv 2305.05949; the title "Scalable and precise application-centered call graph construction for Python" is confirmed as an earlier name of the Jarvis paper; publication venue not verified). Says PyCG does not scale to whole-program, application+library analysis, is flow-insensitive, misses context managers/built-in types, and Jarvis misses calls through dynamically linked libraries and functions held in lists/tuples/dicts. Macro: 6 apps, 108k-515k whole-program LOC. Application-centered whole-program precision 0.35 vs PyCG 0.19, recall 0.60 vs 0.48/0.52. [read-fetch-summary, Sec. IV-A/C, Table V]. The abstract's "at least 20% recall" is not matched by Table V for one configuration (fetch summary flagged this).

### S17. Tool documentation
- git bisect: binary search between a good and bad commit; ~10 steps for 675 revisions; `skip` for untestable commits (may leave result ambiguous if the skipped commit is adjacent to the culprit); `bisect run` automation with exit code 0 good, 1-127 (not 125) bad, 125 skip, otherwise abort. [read-fetch-summary, git-scm.com/docs/git-bisect]
- asv `find`: "Adaptively searches a range of commits for one that produces a large regression"; "only works well when the regression in the range is mostly monotonic"; `asv continuous` / `asv compare --factor` default 1.1; `--interleave-rounds` reduces ordering bias. The page says nothing about noise handling in `find` or about the search algorithm. [read-fetch-summary, asv.readthedocs.io/en/stable/commands.html]
- Performance bisection effectiveness (Empirical Software Engineering 2022, project page): performance regressions are "neither binary nor monotonic due to the noise inherent in performance measurements"; defines a probability-of-effective-bisection measure; 310 bug reports analysed. [abstract-only, project page; authors/volume unknown]
- Chromium perf bisect doc: page fetched but the relevant parts (repeat counts, statistics) were not readable: [unknown]; dropped.

### S18. Dorfman 1943, "The Detection of Defective Members of Large Populations", Ann. Math. Stat. 14(4):436-440. Not read. Cited by S3 (ref [18]). Search-result summary: two-stage pool-then-individual testing, optimal group size is a function of prevalence. [abstract-only] No source I read connects it to CI beyond S3's one-line mention.

---

## (b) Synthesis

### B1. Batching strategies and cost models
1. Constant batch of n, bisect on failure. Cost per failing batch about 2 log2(n)+1; passing batch costs 1 (S1 Fig. 1; Eq. 1). Savings logarithmic in batch size; most gain by n=4 in three Ericsson projects (S1 Sec. 5.1). On open-source Travis data Batch4 reaches nearly the savings of BatchStop4 without bisection (S2 abstract).
2. Optimal n depends on the per-change culprit rate and flake rate, measurable from history ("the CulpritRate can be trivially calculated from historical test results", S1 Sec. 4.2). Best n shrinks as culprit rate rises (S1 Sec. 5.1) and as flake rate rises (S1 Sec. 5.2, with Eq. 7-8 as the explicit analytic cost). That is the only explicit cost model for batch size I read; a closed form linking n to failure rate is absent from S3 (Sec. 2.1). Whether S2 contains the "mathematical" analysis is [unknown].
3. Group-testing analogy: Dorfman's two-stage scheme is the classical optimum-pool-size model; it is named in S3 only in passing. Mapping to our setting is [inferred]: a checkpoint = a pool test over the edits since the last green checkpoint; per-edit "defect probability" p gives expected pool size trade-off.
4. Dynamic/queue-driven batches (BatchAll) and test-level batching (S3); milestones (S4): run when resources allow, tests only at their latest affecting change. Frequency chosen by heuristics that trade delay against freshness of the latest change (S4 Sec. III: "heuristics based on the tradeoff between delay to execute work, and getting the data about the freshest CL possible"); the heuristics themselves are not given. [read-in-source]
5. Risk-aware batching: isolate risky commits, batch the rest (TestTopK in S1; RiskTopN/RiskBatch in S2). Gains reported: 9.0% / 7.6% fewer executions than plain bisection (S1); in S2 the risk-based variants (44%, 49%) were not better than BatchStop4 (50%) on average. [abstract-only for S2]
6. Merge-queue style (Uber): split-on-failure batching is judged not to scale when failures grow with batch size; speculation with conflict graph preferred (S7 Sec. 2.2). Conflict probability grows fast with concurrency: 5% (2 changes) to 40% (16 changes) (S7 Fig. 1 text). This is about concurrent human changes, not sequential edits; relevance [inferred].

### B2. Culprit-finding algorithms
- Bisection: log2(n) steps, assumes monotone good->bad transition and a single culprit; handles untestable commits by skip (S17 git).
- Batch splitting at failure (split in half recursively), multiple culprits require continuing on every failing half (S1 Sec. 2).
- Risk-ordered: test top-K riskiest first (S1), Bayesian prior from build-graph distance and past breakage (S6), heuristic ranking (S5, abstract only).
- Delta debugging: ddmin/dd over change subsets; tolerates interference (changes failing only together) but with non-minimal results; best case logarithmic, worst case about quadratic; unresolved outcomes (patch does not apply or build breaks) are a first-class case (S8, S9). Most relevant to us when edits are interdependent.
- Flake-aware: FACF treats each test run as a noisy observation, updates posterior, may conclude "no culprit"; plain bisect with k reruns plateaus in accuracy while cost grows linearly (S6 Sec. I). Direct analogue for noisy performance measurements, [inferred]: replace f_t by a false-alarm/miss rate of the benchmark comparison.
- Verification of culprit: Google verifies a conclusion by reruns until a stated confidence (S6 Sec. IV-C).

### B3. Periodic full runs and how frequency is chosen
- Google: selected tests on every change is not what TAP does at scale; it runs affected tests at milestones, with timing set by heuristics; tests that "almost never fail" proposed to be executed less often (S4). A literal "reduced on every change + full periodic" schedule as in our plan is [not stated in S4]; closest read statements are the milestone strategy and the proposal of lower frequency for low-risk tests.
- Frequency rules found in sources: fixed batch size n (S1, S2: 2-4 typical), machine-availability-driven (S3 BatchAll, S4 milestone), risk threshold (S1 TopK). I found no source choosing a checkpoint interval from a cumulative-change or cumulative-risk threshold; [unknown]. Memon et al. do report that files changed by many developers, or frequently, break more (S4), supporting a risk threshold from change history, but not a rule.
- Build/test skipping: rule-based CI skip (S12), ML build selection (S10, S11). The empirical warning: cost savings and missed failures trade off; rules like "no code changed" still miss failing builds (S10). Implication: a skipped or reduced validation needs a later catch-up run, which is what a checkpoint is.
- Continuous prioritization of commits (S13) reorders rather than skips.

### B4. Reported numbers (each with location)
| Figure | Value | Where |
|---|---|---|
| Batch testing saves executions vs per-commit | 72% (batch up to 9, project C, no flakes); 42% with flakiness (abstract; 41% in Sec. 5.2) | S1 abstract; Sec. 5.2 |
| Batch size 2 savings | 34%, 34%, 44% | S1 Sec. 5.1 |
| Risk-guided bisection | 9.0% / 7.6% fewer executions | S1 Sec. 5.3, Table 1 |
| Batch2/4/BatchStop4 execution cuts on Travis | 46/48/50% (BatchBisect/Batch4/BatchStop4) | S2 abstract |
| Failure-rate threshold for benefit | below 40% build failure rate | S2 abstract |
| Chrome Batch4 | 75% fewer executions; 61 machines vs 217 | S3 Sec. 4.2, Table 1 [fetch summary] |
| Google breakage frequency | 1.23% of executions find a breakage/fix; 63K of 5.5M affected tests ever failed; milestone every 45 min | S4 Sec. I, III |
| Ziftci culprit ranking | top 5 among thousands 82% | S5 abstract |
| Conflict probability | 5% at 2 concurrent changes; 40% at 16 | S7 Sec. 2.1 |
| Uber follow-up | 53% fewer CI resources | S7 follow-up abstract |
| CI skip by rules | 18.16% fewer CI-triggering commits | S12 abstract |
| Chianti | ~51% tests affected, 3.88% of atomic changes per affected test | S14 abstract |
| PyCG | precision 99.2%, recall 69.9% | S16 abstract/Sec. V-C |

### B5. Change-impact analysis as a selection basis
- Static: dependency/call-graph reachability (Google build-graph "affected" sets, S4/S6; Chianti atomic changes plus call graphs, S14). Memon et al. found tests more than 10 dependency edges away hardly ever break (S4, Sec. I) but a distance cut-off is not safe in general [inferred].
- Dynamic: CoverageImpact and PathImpact estimate impact from recorded executions; "safe" only relative to the observed executions (S15 Sec. 2.3). So a test/input set missing a path yields an unsound impact set. For our design: the impact set from profiling is a heuristic selection basis, hence the need for full checkpoints. [inferred, grounded in S15]
- Chianti reports that only a small fraction of atomic changes affects any given test (S14), which supports reduced test sets per edit; and its use case (which change broke which test after many edits) matches checkpoint culprit finding.
- Taxonomy-level sources (Arnold-Bohner 1993, Lehnert 2011) give vocabulary only; content not read.
- Python call graphs: PyCG (precision high, recall about 70% on small packages) is unsound by design for eval, getattr/setattr, built-in container flows and unavailable source (S16); Jarvis adds scalability and flow sensitivity but still misses dynamic-library calls and containers of callables and, in whole-program mode, has low precision (0.35) (S16). Consequence: a static Python impact set under-approximates; it should be a selection heuristic with a safety net (dynamic coverage union, or periodic full run). Dynamic tracing also misses unexercised paths (S15). For performance edits, an impact set of tests is not the same as an impact set of benchmarks: no source covered; [unknown].

---

## (c) Assumptions that may break for performance-motivated, accumulating edits  [all inferred]

1. Binary, deterministic oracle. Bisection and dd assume a stable pass/fail (S8 monotony/consistency; S6 flake awareness exists because this fails). Performance outcomes are noisy and not binary or monotone (S17 perf-bisect page, asv `find` "mostly monotonic" caveat). Needs repeated measurements and a threshold/ratio (asv uses a factor, default 1.1), or a Bayesian noisy search as in S6 with noise parameters estimated for benchmarks.
2. Single culprit. A checkpoint can fail because of an interaction: each edit passes alone with the reduced suite but the combination fails (S8 interference; S7 "real conflict"). Plain bisection can then return a wrong edit; dd/ddmin-style subset search is the documented tool (S8, S9) but each probe is a full-suite run.
3. Independent edits. Later edits may depend on earlier ones (same function refactored twice; an edit reads a helper introduced earlier). Removing a culprit mid-sequence yields an unbuildable or different program: dd's UNRESOLVED outcome (S8 Sec. 5). Search must then be over prefixes (bisect on order) rather than arbitrary subsets, and "revert the culprit" is really "revert the culprit plus its dependents" or "re-do later edits".
4. Flakiness only from tests. Here benchmarks add timing noise; also environment drift (CPU frequency, background load) can make a "regression" appear at a checkpoint without any culprit: FACF's NONE outcome (S6) matters.
5. Failure probability roughly constant per edit. In S1/S2 batching pays when failure rates are low (below 40%, S2). Performance edits are made precisely in risky areas (hot paths, algorithmic rewrites), and risk rises with files changed by multiple people or frequently (S4). If edits are sequential and cumulative the chance that a window of k edits contains a failure grows with k; the optimal k from group-testing logic shrinks as p grows [inferred from S1 Sec. 5.1].
6. Reduced test selection safe. Static/dynamic impact sets are unsound for Python dynamics (S16) and dynamic ones only cover observed executions (S15); CI-skip rules miss failures (S10). Therefore an edit can pass the reduced check and still break something the full suite would catch, which pushes breakage detection to the checkpoint.
7. Culprit cost is independent of position. With cumulative state, testing "edit i alone" is not meaningful; probes are "prefix up to i", which is bisection on the ordered list and works if breakage persists once introduced (monotone) but not if a later edit accidentally masks an earlier fault.
8. Performance regression across edits can be additive (each edit loses 1-2% under noise). Neither bisection nor dd localizes a diffuse drift; a cumulative-threshold checkpoint (compare against last green baseline) catches it, but attribution is statistical. No source read covers diffuse drift: [unknown].
9. Correctness vs performance targets: an edit "must not slow down" is a different oracle from "tests pass"; only asv/perf-bisect sources address it (S17).

---

## (d) Candidate deterministic rules, each traced

R1. Checkpoint every k accepted edits, with k from historical failure rate: choose k by minimising expected executions per edit using the Najafi cost form (cost = 1 per window + 2 log2(k) x P(window fails), with extra for flaky/noise false alarms as in Eq. 7-8) estimated from the project's own history; initial k = 4 (S1 Sec. 5.1: most savings by 4; S2: Batch4 nearly as good as BatchStop4). Source basis: S1, S2 abstract, S3 for Batch4. The numeric default is transferred from CI commit batching to edit batching: [inferred].
R2. Early checkpoint if a risk score crosses a threshold: cumulative changed lines, number of distinct files/functions touched, or touching a hot module (edit-history-based risk). Source support: risk models guiding testing (S1 Sec. 3, S4 Sec. IV). A concrete cumulative-lines threshold is not in any source: [unknown]; design choice to calibrate.
R3. Immediate (k=1) validation of high-risk edits and batching of the rest (TestTopK-style): S1 Sec. 3 / Fig. 2; RiskTopN/RiskBatch in S2.
R4. On checkpoint failure, search the ordered edits since the last green checkpoint: bisect over prefixes (log2 k probes, S1 Fig. 1; git bisect run semantics, S17); if the culprit probe is untestable (build breaks) mark SKIP and continue (git bisect skip; dd UNRESOLVED, S8). Estimated worst-case probes 2 log2 k + 1 when only a single window; with multiple culprits continue in every failing half (S1 Sec. 2).
R5. If bisection result is inconsistent (the "culprit" passes when tested alone against the previous green state, or the failure disappears on rerun), fall back to subset search (dd) or declare interaction and revert the whole window; rerun to verify the conclusion (S6 Sec. IV-C verification; S8 interference).
R6. Noise handling for performance oracles: repeat each probe r times and require a ratio threshold (asv `--factor`, S17) before calling it a regression; use sequential/Bayesian stopping if the noise rate is estimated (S6). Number r and threshold: [unknown], to be set from benchmark variance.
R7. A failed checkpoint blocks further accepted edits until the culprit is isolated and reverted or fixed (Uber "always green" principle, S7 abstract); after revert, re-run a full validation before resuming. The revert-then-full-run rule is [inferred].
R8. Final full validation is mandatory regardless of schedule, since reduced validation is not safe (S10 missed failures; S15 safety only relative to observed data). Also periodically calibrate the reduced selection by comparing its verdict with the full run at each checkpoint (record missed failures per checkpoint as a measured quantity).
R9. Reduced per-edit selection: union of static impact (call graph, flagged as under-approximating, S16) and dynamic coverage from the last full run (S15), plus tests near changed code by dependency distance (S4); never rely on one source. [inferred composition]

---

## (e) Search log (engine: the WebSearch tool, mode standard; WebFetch for pages; date 2026-11-21)

| # | Query / fetch | Notable hits | Not found / notes |
|---|---|---|---|
| 1 | Beheshtian Bavand Rigby Software batch testing ... | TSE 2021/2022 (ICSE 2022 journal-first page); arXiv 2308.13129 | No open PDF of the TSE paper |
| 2 | Najafi Rigby Shang Bisecting commits ... FSE 2019 | Author PDF at ece.uwaterloo.ca | - |
| 3 | Henderson Flake Aware Culprit Finding ICST 2023 | research.google; hackthology.com PDF | DOI not available |
| 4 | Ananthanarayanan Keeping Master Green EuroSys 2019 | lethain.com PDF; Uber page; arXiv 2501.03440 follow-up | No official ACM OA PDF seen |
| 5 | Memon Taming Google-Scale Continuous Testing | research.google/pubs/pub45861; Vanderbilt course PDF | No research.google PDF |
| 6 | Ziftci Reardon Who Broke the Build | research.google page; patent US9176731 | No PDF |
| 7 | Abdalkareem Which commits can be CI skipped | rabeabdalkareem.github.io PDF (later 404); ML follow-up | Year ambiguous |
| 8 | Jin Servant What helped, and what did not | arXiv 2102.06666 | - |
| 9 | Zeller Hildebrandt Simplifying and Isolating TSE 2002 | Saarland PDF | - |
| 10 | PyCG Salis ICSE 2021 | arXiv 2103.00587, PyPI | - |
| 11 | Scalable and precise application-centered call graph construction for Python | arXiv 2305.05949 (Jarvis, Huang et al.) | Venue not verified |
| 12 | Law Rothermel Whole program path-based dynamic impact analysis | Orso ICSE 2004 PDF describes it; ICSE 2003 pp. 308-318 | Original PDF not found |
| 13 | Zeller "Yesterday, my program worked" | Saarland PDF | - |
| 14 | Liang Elbaum Rothermel continuous prioritization ICSE 2018 | IEEE/researchr/crossref pages | No open PDF located |
| 15 | Ren Chianti OOPSLA 2004 | UW and Purdue PDFs listed; IBM report RC22983 | Not downloaded/read |
| 16 | Jin Servant HybridCISave TOSEM | jxianhao.github.io/files/TOSEM23.pdf; DOI 10.1145/3576038 | Not downloaded |
| 17 | Lehnert taxonomy change impact analysis 2011 | dblp, DOI | No full text |
| 18 | Orso Apiwattanapong Harrold field data FSE 2003 | gatech.edu PDF listed | Not downloaded; DOI conflicts |
| 19 | airspeed velocity asv find bisect | asv docs; perf-bisect page; python-dev post; scipy docs | - |
| 20 | Arnold Bohner Impact analysis framework | ICSM 1993 pp. 292-301 | The 1996 book chapter not located |
| 21 | Dorfman 1943 group testing ... CI | Dorfman PDF copies | No CI linkage in results |
| 22 | Beheshtian Bavand Rigby batch testing pdf (second attempt) | ICSE 2022 page, metadata | No open PDF |
| 23 | Bavand Rigby "Mining bug databases" OR "batch testing" Ericsson | "Mining Historical Test Failures to Dynamically Batch Tests to Save CI Resources" (ICSME 2021) | **"Mining Bug Databases..." does not appear to exist**; title in the brief corrected |
| 24 | WebFetch git-scm.com/docs/git-bisect | skip/run exit codes | - |
| 25 | WebFetch asv commands page | `asv find` description, monotonic caveat | no search algorithm detail, no noise discussion |
| 26 | WebFetch UBC perf-bisect-effectiveness | non-binary non-monotone claim, 310 bug reports | no numeric findings on page |
| 27 | WebFetch Chromium bisects.md | purpose only | repeat counts/statistics not readable; dropped |
| 28 | WebFetch arXiv 2501.03440 | CI at Scale abstract | - |
| 29 | WebFetch ar5iv 2308.13129 | batching algorithms, Dorfman mention | cross-checked with PDF text |
| 30 | WebFetch ar5iv 2102.06666 | technique list, D2 dimension | Periodic full runs not studied |
| 31 | WebFetch ar5iv 2103.00587 | PyCG limits | - |
| 32 | WebFetch rabeabdalkareem.github.io/files/11-abdalkareem_tse2019.pdf | HTTP 404 | Rule list and evaluation not read |
| 33 | WebFetch Zeller 1999 PDF; Orso ICSE04 PDF | binary returned, then read with pdftotext from saved tool-results copy | - |
| 34 | WebFetch arXiv HTML 2305.05949v5 | Jarvis limits and Table V | inconsistent benchmark counts in paper |
| 35 | WebFetch ICSE 2022 journal-first page (Beheshtian) | full abstract with numbers | - |
| 36 | WebFetch research.google Ziftci page | abstract | no PDF link |

Not searched / gaps: "Probabilistic Flakiness" (Facebook engineering blog, cited as [17] in S6; not a Google paper), Fowler-style CI writing, Chromium bisect practice beyond the above, Microsoft/Facebook culprit finding, monorepo "Test Impact Analysis" tooling, performance-specific culprit finding in CI (e.g., change-point detection; another researcher saved Daly et al. ICPE 2020 in the papers folder), Python-specific impact analysis tools, and Pytest-level dynamic impact tools. Titles from the brief confirmed: Beheshtian TSE, Najafi FSE 2019, Henderson ICST 2023, Ziftci ICSE-SEIP 2017, Memon ICSE-SEIP 2017, Ananthanarayanan EuroSys 2019, Zeller 1999/2002, Jin & Servant ICSE 2021 and TOSEM 2023, Liang ICSE 2018, Law & Rothermel ICSE 2003, Orso FSE 2003, Ren OOPSLA 2004, PyCG ICSE 2021, Jarvis. Corrected/dropped: "Mining Bug Databases" (not found), "Probabilistic Flakiness" (blog by Machalica et al., Facebook), "Arnold & Bohner 1996 chapter" (only the 1993 ICSM paper confirmed), CI-skip year (unsettled).
