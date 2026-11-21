# Industrial CI test selection: Meta Predictive Test Selection, Google TAP, Bazel affected targets

Status: critic-checked 2026-11-21 (4 fixes) · Last checked: 2026-11-21
Artifact: none public · Papers: (a) Machalica, Samylkin, Porth, Chandra, "Predictive Test Selection", ICSE-SEIP 2019, arXiv:1810.05286; (b) Memon et al., "Taming Google-Scale Continuous Testing", ICSE-SEIP 2017 (research.google/pubs/pub45861); (c) Bazel docs (bazel.build/remote/caching, bazel.build/query/language)
Evidence labels: **[src]** paper section/page or docs, **[inf]** inferred, **[unk]** not found. (a) critic re-read the arXiv PDF text (ICSE-SEIP version, 10 pp); (b) read from a local pdftotext extraction of the PDF (no page numbers captured; section by quoted text); (c) fetch summaries.

## 1. What it is
Three ways large monorepos decide, per change, which tests to run: Meta uses a learned model on top of build-dependency selection; Google TAP uses reverse-dependency "affected targets" batched into milestones; Bazel provides the underlying build graph and action cache.

## 2. Build / environment
- Meta: build system selects tests that "transitively depend on modified code according to build dependencies" [src (a) Sec. I], about 10^4 tests per change [src (a) Sec. I].
- Google TAP: BUILD files define packages and test targets; TAP uses the file-to-target dependency rules to compute a reverse-dependency structure, outputting all test targets that directly or indirectly depend on modified files = AFFECTED targets [src (b) Sec. II, text near Fig. 2]. A test target is "essentially a buildable and executable code unit" [src (b) Sec. I].
- Bazel: actions with declared inputs; action cache keyed by action hash; local outputs reused first, then remote cache; only actions with no cached output execute [src (c) /remote/caching]. Requires hermetic/reproducible actions; tools outside the workspace and env vars not in the action definition are not tracked [src (c)]. Affected-test queries: `rdeps(universe, target)`, and `allrdeps(x)` (which is Sky Query only and needs `--universe_scope` or `--infer_universe_scope` with `--order_output=no`); `tests(...)` expands test rules. The exact expression `tests(allrdeps(//foo/bar:changed.cc))` is NOT on the docs page; the page's combined example is `tests(//a/... + b/...) intersect allrdeps(siblings(rbuildfiles(...)))` [src (c) /query/language].
- Build is thus incremental at target/action granularity in Bazel-style systems [inf from (c)]; (a) and (b) do not describe the compile step of a single change [unk].

## 3. Correctness tests per candidate
- **Meta PTS**: gradient-boosted decision trees on features: change history of files (3/14/56 days), file/target cardinality, extensions, number of distinct authors, target failure rates (7-56 days), project, number of tests, and cross features: minimal distance between modified files and the test target, shared tokens between file paths and test defines [src (a) Sec. IV-A, IV-B, VI-B]. Selection = union of tests above a score cutoff and top-N by score [src (a) Sec. IV-B]. Calibrated for test recall >0.95 and change recall >0.999 at land time (i.e. misses <5% of individual failures, <0.1% of faulty changes) [src (a) Sec. VI-A].
- **Google TAP**: runs all AFFECTED targets, but not per change: unexecuted affected targets are bundled until a "milestone" cut and each is run once, at its latest affecting CL (e.g. t14 affected by cl2..cl16 runs only at cl16) [src (b) Sec. II, text near Fig. 2]. Milestone typically every 45 minutes at peak; sizes up to 4.2 million tests selected by reverse dependencies [src (b) Sec. I]. The paper's contribution is a model, with "closeness" (MinDist in the dependency graph between changed files and test target) as the main predictor: failing tests are generally closer to the changed code [src (b) Abstract, Sec. IV].
- Granularity differs: both treat the test target (build unit) as atomic, not individual test cases [src (a) Sec. II-A; (b) Sec. I].
- Flakiness: Meta retries a failed target "up to ten times or until it reports a successful result" (in the runs that produce training and evaluation data; whether production gating uses the same retry is not stated in the passage read [unk]) and counts as failed only if all attempts fail; training on un-deflaked data gives about 3x as many missed failures at the same selection rate [src (a) Sec. V, VI-C]. Google: flaky tests prevent "rerun tests that failed before" style heuristics; only 2.07% of target histories both PASSED and FAILED, and after filtering flaky ones 1.23% of targets found a real breakage (Sec. III, Table II); the Introduction phrases the 1.23% as a fraction of test executions [src (b) Sec. I, III].
- Google data: of 5.5M affected tests in the study window only 63K ever failed [src (b) Sec. I].

## 4. Performance measurement per candidate
These systems are about correctness test selection, not performance. Neither paper describes performance confirmation [src (a),(b) read for this: absent]. Meta's flakiness handling is the nearest noise control (retry up to 10x) [src (a) Sec. V].

## 5. Cost per candidate
- Meta: ML selection cuts executions by about 3x and infrastructure cost about 2x versus build-dependency selection; fewer than a third of dependency-selected tests are chosen [src (a) Sec. I, VI-A].
- Google: running all affected targets per CL is infeasible ("may run into Millions" and take hours), hence batching [src (b) Sec. II]; milestone delays up to 9 hours observed in practice [src (b) Sec. I].

## 6. Iteration / cumulative re-validation
- Meta stages: optional manual pre-submit; diff-time subset on each diff version; land-time subset (the calibrated stage; diff rejected on any failure); **stabilization: all tests run on master every few hours**, catching missed faults [src (a) Sec. II-B1-B4]. Model retrained weekly, deployed only if criteria met [src (a) Sec. IV-D].
- Google: milestone runs batch many CLs, so failures are attributed to a range of CLs and a culprit has to be found afterwards [src (b) Sec. II, III: "we know for sure the culprit CL for a breakage and fix" for edge targets; detailed bisection procedure not read [unk]]. Targets not run at a milestone stay AFFECTED until run on demand [src (b) Sec. II].
- Therefore both industrial CI designs accept that per-change test selection is lossy and rely on periodic or batched full re-validation after merge [inf from both].

## 7. Limitations the authors state
- (a): the retry approach may miss some flakiness; flake estimate is a lower bound [src Sec. V]. Selection offers statistical, not absolute, recall guarantees [src Sec. VI-A].
- (b): TAP's one-size-fits-all milestone scheduling wastes resources on targets that almost never fail [src Sec. III]; granularity of AFFECTED depends on how developers write BUILD files [src Sec. II].

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- [src] Industry baseline for "reduced tests per change" is dependency-based affected-target selection (TAP, Meta, Bazel `rdeps`), which is conservative and deterministic, then optionally pruned by a learned (non-deterministic by training data) model with explicit recall targets (0.95/0.999).
- [src] Both pair reduced per-change testing with a later, broader run (Meta: all tests on master every few hours; Google: milestone batching + culprit finding). This is the precedent for per-edit reduced check + cumulative final check.
- [src] Bazel's reduced build rests on hermetic, hash-keyed actions; determinism of the cache depends on declared inputs [src (c)]. Python optimization edits without such declared inputs cannot reuse this directly [inf].
- [unk] Neither industrial paper treats performance acceptance; ECO (google-eco.md) defers that to post-rollout monitoring.

## Sources
- https://ar5iv.arxiv.org/html/1810.05286 (Sec. I, II-A, II-B1-B4, IV-A-D, V, VI-A-C)
- https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45861.pdf (local pdftotext; abstract, Sec. I, II, III, IV)
- https://bazel.build/remote/caching ; https://bazel.build/query/language
