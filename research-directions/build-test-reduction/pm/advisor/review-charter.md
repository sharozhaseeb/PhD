# Advisor-persona review of the Study 1 charter

Reviewed: `research-directions/build-test-reduction/pm/CHARTER.md` (opened 2026-11-21). Reviewer: advisor-persona subagent, modelling the advisor from `persona.md`. This is a simulated review (AI-SIM), not the advisor's opinion. Literature named below is from reviewer knowledge and is **to be verified by W1-LIT** unless a repository file is cited.

## 1. Verdict

**Approve direction, revise before the meeting.** The charter matches the owner-relayed decision (step by step, deterministic, reduced build + reduced test selection, beyond literature). Three things would stop the meeting going well:

1. **No cost evidence yet.** Study 1 is motivated by "full validation is too slow". Without a measured per-edit cost on a real project, the first question has no answer (persona P01). AI-SIM reviews already named this as the redirect condition.
2. **"Build" is close to empty for pure-Python code.** RQ3 says "real Python codebases". Unless projects with compiled extensions (Cython/C/C++, meson or setuptools builds) are chosen, the "reduced build" half of the title has nothing to reduce. Decide this now.
3. **Novelty is asserted in RQ4 but not yet positioned.** Regression test selection (RTS), incremental/cached builds, performance-test prioritization and CI batching/bisection each exist. The combination plus "iterative optimization" is the claim, and the advisor said it must go beyond the literature. RQ4 needs a falsifiable, comparative form.

Secondary: four RQs, two of them literature questions, read as too broad for "step by step"; the oracle for "stays optimized" is undefined; the source of iterative edit sequences is a validity risk.

## 2. The 10 questions the advisor is most likely to ask (ranked)

| # | Likely question | Evidence in the repo that answers it | Exists now? |
|---|---|---|---|
| 1 | "How slow is full build + full test (+ benchmarks) per edit, really? Show me numbers." | W3-EXP: timed full build, full test, full benchmark on ≥2 pinned projects (command, raw log, SHA). Plus published numbers: SemOpt validated 8,082 C/C++ and 9,483 Python candidates by build/install + unit tests + 6 performance runs per version (TOSEM pp. 31–34, Table 16; local PDF `llm-optimization-validation/papers/2026-SemOpt-TOSEM-author-version.pdf`). | Paper evidence yes; own measurements no |
| 2 | "What is new compared with existing regression test selection and incremental builds?" | W1-LIT closest-work table: Rothermel & Harrold safe RTS (1997); Ekstazi (Gligoric et al., ISSTA 2015); STARTS (Legunsen et al., FSE 2016); HyRTS (Zhang, ICSE 2018); pytest-testmon (Python practice); Build Systems à la Carte (Mokhov et al., ICFP 2018); ccache/Bazel remote caching; CloudBuild (Microsoft, ICSE-SEIP 2016). One column: "what it does not handle in our setting". Plus the recorded search. | No |
| 3 | "Why Python? What gets *built* in a Python project?" | Project selection rationale in W3-EXP: projects with real compile steps (e.g. Cython/C extensions) and measured build share of per-edit time; or a stated decision to add a C/C++ arm. | No |
| 4 | "How do you know the reduced selection didn't miss a bug or a slowdown?" | Oracle definition: full build + full test + full benchmark on every edit as ground truth; safety = missed functional failures and missed performance regressions above a stated threshold; fault/regression injection protocol; periodic and final full checks. | Partly (RQ3 text); no protocol |
| 5 | "Walk me through one edit." | A worked example in W3-EXP: one real optimization edit → changed files → rebuilt targets → selected tests and benchmarks → time full vs reduced → result. One figure. | No |
| 6 | "Where do the iterative edits come from? Are historical commits a realistic session?" | Edit-source decision and justification: historical optimization commits (GSO / SWE-fficiency / SWE-Perf / FormulaCode-style task repos, or asv-tracked commits), possibly decomposed into hunks applied in sequence; stated limitation vs agent sessions. | No |
| 7 | "'Stays optimized' — how is performance checked, and do you also reduce benchmarks?" | Performance oracle: benchmark suite (e.g. asv), repetitions, threshold, baseline = original, not just parent (AI-SIM pivot review Objection 2). Change-aware benchmark selection literature: PerfRanker (Mostafa et al., ISSTA 2017); performance risk prioritization (Huang et al., ICSE 2014); Perphecy (de Oliveira et al., 2017); microbenchmark prioritization (Laaber et al., EMSE 2021, already cited in `llm-optimization-validation/2026-09-07-advisor-review.md`). | No |
| 8 | "How do SemOpt, SWE-Perf, GSO etc. validate each candidate, and what does it cost them?" | W2-PRACTICE table: per system — what is rebuilt, which tests, which benchmarks, repetitions, reported or estimated cost per candidate, source page/file+commit. SemOpt row can be filled from `2026-10-07-semopt-method-diagram.md`. | Partly (SemOpt only) |
| 9 | "Isn't the periodic full check just CI batching/bisection?" | Literature: Google TAP / continuous testing at scale (Memon et al., ICSE-SEIP 2017); commit batching and bisection (Najafi et al., FSE 2019). Our difference must be stated: optimization-session edits, dual functional + performance oracle, schedule tied to accumulated dependency footprint. | No |
| 10 | "What is Study 2, and what exactly does Study 1 hand to it?" | One slide/paragraph: Study 1 output = deterministic rules + benchmark harness + measured safety/cost frontier; Study 2 tests whether AI (learned selection, LLM optimizer in the loop) improves on that frontier. Note: learned selection already exists (Facebook predictive test selection, Machalica et al., ICSE-SEIP 2019) — Study 2 must also beat that. | No |

## 3. Objections to the RQs and proposed rewrites

**General.** RQ1 and RQ2 are literature/practice surveys; the advisor will likely accept them as *background chapters*, not as research questions. Four RQs is heavy for "step by step". None of the RQs states the safety/cost metrics or the comparator. "Go beyond literature" is only in RQ4 and is phrased as a list of possibilities ("e.g.").

| RQ | Objection |
|---|---|
| RQ1 | Descriptive; useful only if it produces numbers (cost per candidate, candidates per task). Otherwise it is related work. |
| RQ2 | A literature review question. "Which assumptions break" is the interesting part and needs evidence, not just reading. |
| RQ3 | Good core, but conflates functional failures and performance regressions; injected faults may not resemble optimization bugs; "real Python codebases" leaves "build" empty; no comparator beyond full validation. |
| RQ4 | Not falsifiable as written; "allows" is not a result. Each listed idea has neighbours (dependency-based RTS, PerfRanker-style selection, CI batching). Needs a matched-cost comparison against the best existing composition, plus an ablation. |

**Proposed rewrite (three RQs, with RQ1/RQ2 of the charter moved to background chapters W1/W2):**

- **RQ1 — Cost.** In iterative optimization of real projects, what share of per-edit validation time goes to build, functional tests and performance benchmarks, and how does it scale with the number of edits? *(Answers "is the problem real?"; redirect if full validation is cheap.)*
- **RQ2 — Existing techniques in the new setting.** When existing deterministic techniques (incremental/cached builds; dynamic and static regression test selection; change-aware benchmark selection) are applied unchanged to sequences of optimization edits, how much end-to-end time do they save (including their own analysis overhead), and how many functional failures and performance regressions above a stated threshold do they miss? Which properties of optimization edits cause the misses? *(Characterization; the "what breaks" analysis is a contribution if backed by concrete cases.)*
- **RQ3 — A better deterministic policy.** Can a deterministic policy that uses the iterative setting — e.g. dependency footprint accumulated since the last full check, performance-aware benchmark selection from profiles, and a footprint-triggered full checkpoint with bisection — reach a better savings-vs-misses trade-off than the best RQ2 combination at matched cost, and which component matters (ablation)?

Fix before the meeting: one threshold example for "performance regression" (illustrative, e.g. >5% vs original on any benchmark, frozen before evaluation), and whether safety means "zero misses at final validation" or "bounded misses between checkpoints".

## 4. What would count as "more than what has already been done"

Each item must survive a recorded targeted search (charter rule 3). Ranked by strength:

1. **A dual-oracle result.** RTS literature mostly targets functional failures; performance-test selection mostly targets single changes. Showing, with numbers, how techniques behave when *both* correctness and retained speed-up must be guaranteed across an edit sequence would be new evidence, if the search confirms the gap.
2. **A characterization of why existing safe techniques miss optimization regressions** (e.g. performance effects outside changed code through shared data structures, caches, memory/GC, native extension rebuild boundaries, input-size dependence), with reproducible cases. New knowledge, not a new tool.
3. **A deterministic policy that beats the strongest existing composition** at equal total cost, with ablation showing the iteration-specific component (accumulated footprint / checkpoint schedule) adds value. Combining known parts without this comparison does not count.
4. **A reusable benchmark**: pinned projects + edit sequences + full-validation ground truth (build/test/benchmark logs) that later studies, including Study 2, can reuse.
5. **Cost evidence for optimization pipelines**: first published accounting of validation cost per candidate across systems (from W2), if no one has reported it.

Does **not** count: applying testmon/Ekstazi/ccache to new repos and reporting savings; renaming batching as "checkpoints"; only showing that cumulative small slowdowns add up (AI-SIM pivot review Objection 2: trivial, fixed by original-baseline checks); a survey alone.

## 5. Meeting checklist — what the repo must contain

Must-have (meeting fails without these):

- [ ] **One-page Study 1 statement**: problem, the three RQs, scope (language/project type decision), what "valid" and "optimized" mean, explicitly no AI.
- [ ] **Measured cost on ≥2 real projects**: full build, full test, full benchmark time per edit; command, raw log, commit SHA, machine.
- [ ] **One worked edit end-to-end** (full vs reduced) with a diagram.
- [ ] **Closest-work table (≥10 works)** across build reduction, RTS, performance-test selection, CI batching/bisection, with "what it lacks for our setting" and the search log.
- [ ] **Practice table**: how SemOpt, SWE-Perf, GSO, SWE-fficiency, PIE, Codeflash, asv-based CI validate each candidate, with cost where reported (source page/file + commit).
- [ ] **Experiment design**: projects and why, edit-sequence source, baselines (full; incremental build only; RTS only; benchmark selection only; best combination; proposed policy; ablation), oracle, safety and savings metrics, overhead accounting, injected-fault protocol.
- [ ] **"Beyond literature" claim list**, each tagged *searched – not found* / *found – differs by X* / *unknown*.

Should-have:

- [ ] Threats to validity (edit realism, test-suite weakness — cite SemOpt: all 9,483 Python candidates passed tests, Table 16 — timing noise, Python-vs-compiled scope).
- [ ] Study series slide: Study 1 → Study 2 (AI) → later; what each hands on.
- [ ] Timeline to first Study 1 result and candidate venue (proposal only).
- [ ] A short list of decisions needed from the advisor (persona §6).
- [ ] Clear labels separating measured, read-in-source, inferred and unknown; no reliance on the AI-written "advisor reviews" as advisor opinion.
