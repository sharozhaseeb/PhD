# Advisor persona — for Study 1 (reduced build and test validation)

Prepared 21 November 2026 by the advisor-persona subagent for the PM. Purpose: predict what the student's PhD advisor will ask at the ~23/24 November meeting. This is a model of the advisor, not the advisor.

## 0. Evidence labels used here

| Label | Meaning |
|---|---|
| **REAL** | The real advisor is recorded as saying or deciding it (file + short quote). |
| **OWNER** | The student/owner relays it as the advisor's decision; second-hand, not written by the advisor. |
| **AI-SIM** | Written by an AI acting as advisor or reviewer. Useful as a rehearsal, not as the advisor's view. |
| **INFER** | My inference from the pattern of material. Treat as a hypothesis. |
| **UNKNOWN** | No evidence in the repository. |

## 1. What the repository actually records about the real advisor

Short answer: almost nothing first-hand. Every "advisor review" in the repo is AI-written.

| Item | Label | Source and quote |
|---|---|---|
| No advisor feedback has been written down | REAL (absence) | `Spark Elevate/04-advisor/agenda-and-decisions.md`, "## Advisor feedback": "(NEEDED: feedback and resulting decisions after discussion)" |
| Decision register: nothing approved | REAL (absence) | `llm-optimization-validation/05-advisor-questions.md`: "Do not infer that a structural PASS means any of these decisions has been approved." Every row is "current position", not an advisor decision. |
| A paper discussion with the advisor on SemOpt was prepared (6 Oct 2026), with PIE and the TSE time-efficiency paper as references | REAL that it was prepared; UNKNOWN who chose the papers | `output/pdf/semopt-advisor-deck.pdf`, slide 1: "Advisor paper discussion 6 October 2026"; commit `d1f19ff` "Add SemOpt advisor presentation in PowerPoint and PDF". |
| Advisor was a candidate PI for SPARK grant | REAL as a plan only; outcome UNKNOWN | `agenda-and-decisions.md`: "Confirm the advisor's willingness and eligibility to serve as the university-nominated PI". Deadline shown was 26 Oct 2026; whether submitted is not recorded. |
| Advisor's expertise unknown | REAL (absence) | `2026-09-05-direction-review.md`: "advisor expertise ... remain unspecified." |
| Latest decision (Study 1) | OWNER | `build-test-reduction/pm/CHARTER.md` "Problem (owner's words, condensed)" plus PM brief: study step by step; Study 1 = keep an optimized codebase optimized and valid via builds and tests; **no AI first** to establish deterministic rules; full build + full test per small edit is too slow; study reduced builds and reduced test selection; **must go beyond existing literature**. |

AI-written "advisor" material (all labelled AI-SIM below):

- `llm-optimization-validation/2026-09-07-advisor-review.md` — self-describes as "an evidence-based advisory assessment, not an actual university examination."
- `llm-optimization-validation/2026-09-07-pivot-advisor-review.md` — "an advisor-style assessment of our own proposal, not an independent university review."
- `Spark Elevate/04-advisor/adversarial-review.md` and `review-history/` — GPT-6 Astra; "simulated external-review scrutiny, not ... human advisor approval."
- `masters-implementation-review.md` — AI source inspection; records a **user** (not advisor) statement: "efficient allocation of validation effort is the primary interest."

## 2. What this advisor values

| Value | Label | Basis |
|---|---|---|
| **Step-by-step research**: one bounded study at a time, deterministic baseline before AI | OWNER | Latest decision. Strongest real signal we have. |
| **Novelty beyond existing literature** is a hard bar, not a nice-to-have | OWNER | "must go beyond existing literature". |
| **Practical engineering cost** framing (time per iteration, many iterations) | OWNER | "full build + full test per small edit is too slow across many iterations". |
| **Validity of the optimized result over time** ("stays optimized/valid"), i.e. both functional correctness *and* retained speed-up | OWNER | Study 1 framing. Note: two oracles, not one. |
| Grounding in real systems the advisor has read (SemOpt-style build/install → unit tests → perf tests per candidate) | INFER | SemOpt discussion on 6 Oct preceded the Study 1 decision; SemOpt's real-project evaluation builds/installs and runs unit + performance tests for every candidate (SemOpt TOSEM pp. 31–33). 8,082 C/C++ and 9,483 Python candidates (Table 16, p. 34). The Study 1 cost problem looks like it came out of that discussion. |
| Moving away from LLM-centric and statistical-acceptance framing toward a classical SE problem (build/test reduction) | INFER | Contrast between Sept–Oct AI-proposed directions (acceptance statistics, workload selection) and the owner-relayed decision (deterministic build/test reduction, no AI). |
| Empirical rigor, strong baselines, ablations, counting overhead | AI-SIM (consistent, but not shown to be the real advisor's) | Both 7 Sept reviews; Spark Astra review. Keep these as hygiene; do not present them as "what the advisor wants". |

## 3. Recurring objections (likely to resurface)

From AI-SIM reviews, still applicable to Study 1, ranked by how directly they hit the new charter:

1. **"Is full validation actually expensive?"** Pivot review: "redirect if full testing is already cheap enough that selection has little practical value." Study 1 lives or dies on measured cost.
2. **"This is already done."** Reuse of validation effort was candidate C in the 7 Sept AI-SIM review: "Reuse is an established concept... The possible contribution is a well-defined validity model and measurable benefit across optimization sequences, not caching itself." It was *deferred* there; Study 1 revives it, so the overlap critique transfers in full.
3. **"Accumulation is trivial; check against the original baseline."** Pivot review Objection 2. A periodic full checkpoint (charter RQ4) is the obvious safeguard and is close to existing batch/bisect CI practice.
4. **"Composition of known parts is not a contribution."** "A novel name for combining familiar selectors is insufficient." Applies to incremental build + RTS + benchmark selection + checkpoints.
5. **Overhead must be counted** (analysis, coverage collection, dependency tracking, profiling) — AI-SIM, consistent across reviews.
6. **Units of generalization are projects/sessions**, not repetitions — AI-SIM.

New objections specific to Study 1 (INFER):

7. **"What build, in Python?"** Pure-Python packages have almost no build step; reduced build only matters for compiled extensions (Cython/C/C++/Rust, meson/setuptools builds) or C/C++ projects. SemOpt's own Python arm "install[s] the package"; its C/C++ arm compiles.
8. **"Are historical commits a realistic iterative session?"** Real optimization commits are weeks apart and large; an LLM/agent session is many small edits minutes apart.
9. **"Selected tests are only as good as the suite."** SemOpt reports all 9,483 Python candidates passed the unit tests (Table 16, p. 34). If the suite cannot detect optimization bugs, "safe" selection is meaningless; the oracle must be strengthened (mutation/fault injection, differential checks).
10. **"Why no AI if the motivation is AI optimizers?"** Owner answer: deterministic baseline first, AI in a later study. Have the one-line answer ready.

## 4. What convinced them before

UNKNOWN for the real advisor — no recorded approval of any earlier direction. The only observable outcome is that the student moved from "acceptance statistics / workload selection for LLM optimizers" (Sept–Oct, AI-proposed) to "deterministic reduced build + test validation" (Nov, owner-relayed). INFER: the advisor responded to a concrete, practical engineering bottleneck grounded in a paper they discussed (SemOpt) more than to statistical decision framings.

## 5. Decisions already made (as far as we know)

| Decision | Label |
|---|---|
| Research proceeds as a series of studies, step by step | OWNER |
| Study 1 = reduced build + reduced test/benchmark selection for iterative optimization, deterministic, no AI | OWNER |
| Study 1 must exceed existing literature | OWNER |
| AI-based selection is a later study | OWNER (charter) |
| Python as the target language | **Not an advisor decision** — charter choice (RQ3 "real Python codebases"); earlier AI-SIM docs also chose Python. Open. |
| Thesis contribution, venues, timeline, sample sizes | UNKNOWN / open (`05-advisor-questions.md`) |

## 6. Open questions to settle at the meeting

1. Language and project type: Python-only, Python with compiled extensions, or include C/C++ (where builds are genuinely expensive)?
2. Source of edit sequences: historical human optimization commits, decomposed commits, or recorded optimizer trajectories (used as data, not as method)?
3. Definition of "stays optimized": performance oracle, threshold, baseline (parent vs original).
4. Acceptable safety: zero missed failures (safe RTS) vs a bounded miss rate caught by checkpoints.
5. What counts as Study 1's contribution (empirical characterization vs new deterministic technique vs both).
6. Status of SPARK grant and whether Study 1 must fit it.
7. Target venue/timeline for Study 1.

## 7. Unknowns (do not guess in the meeting pack)

Advisor's name/field strength in build systems or testing; whether the advisor chose SemOpt; whether the advisor has seen the Sept–Oct AI-written proposal package; publication and thesis requirements; SPARK outcome; compute available.

## 8. Running hit-list of predictions

Update after each deliverable review and after the meeting (status: pending / hit / miss / partial).

| ID | Prediction for the meeting | Conf. | Status |
|---|---|---|---|
| P01 | Asks for a number: how long full build + full test (+ benchmark) takes per edit on a real project, and how many edits per session | High | pending |
| P02 | Asks "what is new compared to regression test selection (Ekstazi/STARTS/testmon-style) and incremental builds?" | High | pending |
| P03 | Asks what "build" means for Python projects / why Python | High | pending |
| P04 | Asks how we know a reduced selection did not miss a bug or a slowdown (oracle + safety metric) | High | pending |
| P05 | Asks for a concrete worked example: one edit, what gets rebuilt, which tests run, time saved | High | pending |
| P06 | Asks where the edit sequences come from and whether they are realistic | Medium | pending |
| P07 | Asks how "stays optimized" is checked (performance, not just tests) and whether benchmarks are also reduced | Medium | pending |
| P08 | Asks how SemOpt / SWE-Perf / GSO validate each candidate and what that costs | Medium | pending |
| P09 | Pushes back on four RQs as too many for "step by step"; wants Study 1 smaller | Medium | pending |
| P10 | Asks what Study 2 (AI) will be and how Study 1's rules feed it | Medium | pending |
| P11 | Asks about periodic full checks: how often, and is this not just CI batching | Low–Med | pending |
| P12 | Asks about timeline and a target venue for Study 1 | Low–Med | pending |
| P13 | On networkx: "testmon already does this for pure Python — what does your rule add?" | Medium | pending |
| P14 | "Your profile-based benchmark selection is just coverage-based performance-test selection" (if no existing perf-selection arm) | Medium | pending |
| P15 | "Why would accumulation ever matter if each fault is in the changed function?" | Low–Med | pending |
| P16 | "Isn't the accumulated-change trigger just batching with a variable batch size?" | Medium | pending |
| P17 | "Why testmon and not NameRTS as the Python baseline?" | Low–Med | pending |
| P18 | "How does PerfAgent validate each edit, and does it report misses?" (closest work) | Medium | pending |
| P19 | "Benchmark harnesses rebuild per patch for isolation — that's not a gap" | Medium | pending |
| P20 | "If the full benchmark verdict itself isn't repeatable (2607.01211), how can you count misses?" | Medium | pending |
| P21 | "Estimated seconds aren't real time. What is the measured wall time, including pytest startup and testmon overhead?" | High | pending |
| P22 | "Your trigger fires on every module-level edit, so isn't A4 just periodic full checks?" | Medium | pending |

### Deliverable review log

| Date | Deliverable | Coverage of predictions | File |
|---|---|---|---|
| 2026-11-21 | Charter | — | `review-charter.md` |
| 2026-11-21 | W3 readiness v1 | P04 answered; P01 and P05 planned; P03 partial (bottleneck only, small build) | `review-w3-readiness.md` |
| 2026-11-21 | W3 draft results | P01 partly answered (tests and build, no benchmarks yet). Biggest risk: estimated test-seconds leave out startup and testmon overhead, so real wall savings are about 4×, not 15× | reply only |
| 2026-11-21 | W5 video shot list v1 | Order OK. Too heavy on literature, thin on results. On-disk C7 status is stale. Missing: an RQ1 per-edit cost chart (P01) | reply only |
| 2026-11-21 | W2 practice survey | P08 answered (28 systems), but cost per candidate is [unk] (P01 still open); needs a 2-minute table for optimizers only | `review-w2.md` |
| 2026-11-21 | W1 literature v2 | P02 answered explicitly (19 works); P11 (CI batching) answered; "combination" framing is the weak spot | `review-w1-v2.md` |
