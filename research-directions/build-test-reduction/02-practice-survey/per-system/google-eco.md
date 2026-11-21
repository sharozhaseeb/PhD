# Google ECO

Status: critic-checked 2026-11-21 (5 fixes) · Last checked: 2026-11-21
Artifact: none public · Paper: "ECO: An LLM-Driven Efficient Code Optimizer for Warehouse Scale Computers", Lin, Maas et al., arXiv:2503.15669 v1 (19 Mar 2025, 23 pp; section numbers below match this version) and v2 (17 Sep 2026, retitled "AI-Driven", renumbered: verification = Sec 6, evaluation = Sec 7, 7.3 production edits, 7.4 impact; headline numbers differ, e.g. "several hundred thousand normalized cores" over a year)
Evidence labels: **[src]** paper section (critic re-read the v1 PDF text; v2 PDF cross-checked for the test-selection sentence), **[inf]** inferred, **[unk]** not found.

## 1. What it is
A production system at Google that mines historical performance commits into an anti-pattern database, finds similar code across the monorepo, has a fine-tuned LLM generate C++ edits, and submits them to code owners as ordinary commits [src Sec. 2-5].

## 2. Build / environment
- Edits go through the teams' existing CI; build failures get automated fixes for trivial errors (e.g. missing includes), harder ones an LLM fix attempt, else "the edit is abandoned" [src Sec. 5].
- No description of incremental, affected-target or sandboxed per-edit builds beyond "existing CI" [unk; Sec. 5 as summarized].

## 3. Correctness tests per candidate
- Automated unit and integration tests run by the owning teams' CI, i.e. whatever tests the repo's presubmit selects; ECO does not choose tests [src v1 Sec. 5]. v2 adds that "all tests in our entire monorepo that are affected by a change" are identified and run automatically [src v2 Sec. 6]; the selection mechanism itself is not described [unk].
- LLM self-review before human review: "Code edits are not passed to a human reviewer unless the edits pass self-review" [src Sec. 5]. Code owners make the final submit decision [src Sec. 5].
- Stated weakness: "most tests provide no indication on code performance" and test coverage is imperfect [src Sec. 5 limitations].

## 4. Performance measurement per candidate
- **No per-edit performance test.** Quote: "we cannot perform isolated performance tests on each generated edit" [src Sec. 6.3]. Candidates are ranked and pruned by profile cost (functions with cost between C_min 0.1% and C_max 25% of fleet profile) before generation [src Sec. 3.1].
- Offline microbenchmark study of prompts: cycles per operation over 10 runs, 5 samples per prompt at temperature 0.3; no noise treatment or speed-up threshold [src Sec. 6.1].
- Real confirmation is post-rollout through Google-Wide Profiling (GWP), before/after metrics per commit [src Sec. 3.1.1, 5.1, 6.4].

## 5. Cost per candidate
Not reported per candidate. Scale: >10M localization candidates narrowed by retrieval to top-500 (ScaNN) per anti-pattern query [src Sec. 3.1-3.2]; 55k-commit fine-tuning set [src Sec. 2.2]; >25k lines in 6.4k production commits [src Sec. 1, 6.4].

## 6. Iteration / cumulative re-validation
- Post-submit monitoring: GWP tracks before/after, performance-regression alerts on sensitive functions, team can revert; reverts "<0.5% of commits" [src Sec. 5.1]. Production success >99.5% [src Abstract]. Savings about 500k normalized CPU cores per quarter, >2M over the past year [src Sec. 6.4].
- So cumulative performance validation is fleet-level, after merge, not per edit [inf].

## 7. Limitations the authors state
Imperfect tests; CodeBLEU only a weak signal for performance; edits mostly single-file; C++ and CPU/memory metrics only; reactive (similarity-driven) rather than proactive [src Sec. 5, 6.3, 8].

## 8. Relevance to Study 1
- [src] Strong industrial evidence that per-edit performance confirmation is skipped: correctness via normal presubmit CI, performance via post-rollout fleet profiling (production-scale, high-noise-tolerant).
- [src] Test selection is not ECO's job; it reuses the monorepo's CI test selection (see industrial-ci-test-selection.md) [inf link].
- [inf] A research prototype that confirms speed-up per edit with a deterministic reduced benchmark would address exactly the gap ECO admits.

## Sources
- arXiv:2503.15669 via https://ar5iv.labs.arxiv.org/html/2503.15669 (Sec. 1-8 as cited); Critic verified section numbers and quotes against the v1 PDF (arxiv.org/pdf/2503.15669v1): Sec. 5 / 5.1 (verification, monitoring), 6.1 (10 runs, five samples, temperature 0.3), 6.3 (quote on isolated tests), 6.4 (25k lines / 6.4k commits, "over 2 M" cores, 500k per quarter), 3.1.3 (Cmin 0.1% / Cmax 25%, >10M candidates), 3.2 (top-K=500), 2.2 (~55k commits), Sec. 8 (extensions/limitations). All OK. Note v1 Sec. 3.1.1 is the continuous profiler (GWP); the >99.5% figure is in the abstract/Sec. 1.
- https://www.usenix.org/conference/osdi26/presentation/lin-hannah (listing only)
