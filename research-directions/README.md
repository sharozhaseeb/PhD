# Research directions

**Status:** 2026-11-21. Study 1 is the current direction. The other entries are background.

**Evidence boundary.** This page indexes the folders and states how they relate. The relationship between the earlier package and Study 1 is partly inferred; each such statement is labelled. Labels follow the advisor model ([persona.md](build-test-reduction/pm/advisor/persona.md), section 0): OWNER = relayed by the student as the advisor's decision, second-hand; INFER = our inference; REAL = recorded in a file.

## Index

| Order | Direction | Dates | Status |
|---|---|---|---|
| 1 | [**Study 1: reduced build and test validation for iterative code optimization**](build-test-reduction/README.md) (`build-test-reduction/`) | Nov 2026 | **Current.** W1 final, W2 final draft, W3 PRELIMINARY draft results, overnight runs pending. [Advisor meeting pack](build-test-reduction/meeting-2026-11-advisor/README.md) |
| 2 | [Workload regressions in iterative Python optimization](llm-optimization-validation/README.md) (`llm-optimization-validation/`) | Sept–Oct 2026 | Provisional, pre-pilot, no benchmark executed. Background; superseded as the active direction by Study 1 |
| 3 | [Cross-domain feasibility review](2026-09-05-direction-review.md) | 5 Sept 2026 | Historical screening of candidate directions; not a systematic review |

Two earlier finance candidates (`stock-feedback-calibration/`, `stock-selective-routing/`) are not in the working tree. They were deleted without a commit and are recoverable from git history (commit `a9de702`). They are not linked.

## How Study 1 follows from the earlier package

1. **The earlier package asked** which workload-related failures persist when Python code is optimized repeatedly, and whether a small, adaptively selected workload suite can prevent them at acceptable cost ([its README](llm-optimization-validation/README.md)). Its first contribution was to be an empirical study; no benchmark was ever run for it.
2. **The SemOpt discussion.** A paper discussion on SemOpt (with PIE and the TSE time-efficiency paper as references) was prepared for 6 October 2026 ([persona.md](build-test-reduction/pm/advisor/persona.md), section 1; deck: [PDF](../output/pdf/semopt-advisor-deck.pdf)). SemOpt validates each candidate by build/install, unit tests and repeated performance runs ([method diagram](llm-optimization-validation/2026-10-07-semopt-method-diagram.md); persona section 2 cites TOSEM pp. 31–33).
3. **The November decision (OWNER).** The student relays that the next step is narrower: validate each optimization edit with a **reduced build and reduced test/benchmark selection**, chosen by **deterministic rules, no AI first**, one step at a time, and it must go beyond existing literature ([CHARTER](build-test-reduction/pm/CHARTER.md), "Problem"; [persona](build-test-reduction/pm/advisor/persona.md), sections 2 and 5). This is second-hand; no first-hand advisor record exists.
4. **The link between steps 2 and 3 is INFER.** The persona model infers that the Study 1 cost problem came out of the SemOpt discussion ([persona](build-test-reduction/pm/advisor/persona.md), section 2). Nothing in the repository records the advisor saying so.

**What carries over, as stated in the sources:**

| Carried over | Where it is stated |
|---|---|
| Python code optimization edits as the setting | Earlier package title and README; Study 1 charter RQ3 history ("real Python codebases") and [W3 targets](build-test-reduction/03-experiment/readiness.md) (section 1.2). The language itself is a charter choice, not an advisor decision (persona section 5) |
| Validation cost per candidate as the practical problem | SemOpt per-candidate validation (persona section 2); [W2 at-a-glance table](build-test-reduction/02-practice-survey/README.md) |
| Concern about the performance oracle: noise, thresholds, baseline = original not just parent | Earlier package pivot review, as cited in [persona](build-test-reduction/pm/advisor/persona.md) section 3, objection 3; Study 1 definitions in the [CHARTER](build-test-reduction/pm/CHARTER.md) and [readiness](build-test-reduction/03-experiment/readiness.md) section 4.2 and 5 |

**What does not carry over:** the earlier package's acceptance-statistics and adaptive workload-selection framing, and any AI-based selection. AI-based selection is explicitly a later study ([CHARTER](build-test-reduction/pm/CHARTER.md), "Problem"). The earlier package's open decisions ([05-advisor-questions.md](llm-optimization-validation/05-advisor-questions.md)) were never answered by the advisor on record.
