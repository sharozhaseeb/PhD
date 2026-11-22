# Advisor-persona review: Study 1 paper, first full draft

Reviewed 2026-11-22, ahead of the ~23/24 November meeting. Reviewer: advisor-persona subagent (**AI-SIM**: a model of the advisor, not the advisor). It follows [persona.md](persona.md) and checks the draft against my own plan, [paper-plan-advice.md](paper-plan-advice.md) ("the plan" below).

Read: `04-paper/main.tex` and every `\input` (`sections/abstract, introduction, background, design, rq1-cost, rq2-coverage, rq3-power, rq4-reductions, discussion, threats, conclusion, appendix`); `04-paper/generated/numbers.tex` (all macros); `refs.bib` (grep only); `04-paper/reviews/2026-11-22-review-log.md`. Spot checks: `knowledge-base/findings.md` rows B1, V1, S1, S2, R1, T1, N6, N8; `03-experiment/results/results.md` §W6 hostile-review checks (L728–743) and the R1 headline (L32); `01-literature/beyond-literature-claims.md` rows B1 and C11.

Nothing was run or compiled. Line numbers refer to the `.tex` files as of this review. Venue deadlines are **not checked**.

---

## 1. Verdict

**This is the right paper and the right story.** The draft follows the plan's thesis: the cost sits in benchmarks, and the benchmarks often cannot see the edit. It scopes every claim to networkx and reports the negative results plainly. The honesty is its strongest asset, and the hostile reviewer saw that too ("unusually honest").

**It is not yet the right *size* of paper.** It is a 12-page full empirical paper built on one project, 14 labelled edits, 10 synthetic slowdowns and 3 heavy-module A/A cases, with about 20 `\TODO`s. Read cold, it is a careful lab notebook. Every second sentence is a hedge, and four results sections each end on a pending experiment. The hostile reviewer's weak reject is correct for this evidence. Better prose will not move it.

**The single most important change:** treat the replication (E1) as the gate for the full paper, and **run it to the plan's specification, not the reduced one in the draft**. That means ≥ 5 projects and ≥ 60 true optimizations pooled, profiles at each edit's parent, and **at least a human-labelled subset**. The draft has slid to "3–4 projects" with labelling that "stays agent-only, by the authors' decision" (`design.tex` L54). Pooled at 3–4 projects, the CI will still be about ±14 points. And a headline proportion whose denominator only same-model LLM raters ever defined is the first thing an ESEM reviewer will reject. Until E1 lands, the honest form of this draft is a 5–6 page short paper (see §5).

The most important change to the **text** is to merge RQ2 and RQ3 into one oracle section with a per-edit table (§2, RQ2/RQ3). After E1, that change matters most.

---

## 2. Section-by-section comments

### Title (`main.tex` L45–46)
- "Expensive and Blind" overstates both halves. On *expensive*: the draft's own estimate says a setup-cached pass costs only 1.5–2× build + tests (`rq1-cost.tex` L27). On *blind*: 6 of 14 optimization edits are reached, and #2 was detected on all 8 cases. "Blind" is the case only for some edits.
- Keep "A Case Study on networkx" until E1. See §4 for the title I would use.

### Abstract (`abstract.tex`)
- **Too long and too dense.** Eleven sentences carry about 25 numbers. Cut to six sentences: problem, method, cost result, coverage result, visibility/power result, implication. The A/A sentence (L9) and the testmon sentence (L10) can each drop to half their length.
- L5: lead the cost claim with the median (about 8×), not "8–28×". See §3, claim C1.
- L8: "Most misses" breaks the project's own rule (no "most" without a CI above 50 %; 6 of 7 has a Wilson lower bound of ≈ 49 %). Write "six of the seven misses".
- L8: "executed by a benchmark is not visible to it" is the best sentence in the abstract. Keep it. It currently rests on one slowdown (#3), so frame it as an observation, not a measured rate (see §4).
- L12: the TODO is right. Add the condition from the plan: restate the thesis only if the pooled unreached share supports it, and otherwise reframe around suite design.

### Introduction (`introduction.tex`)
- L4–8: good opening. But L5 says every system validates "in the same three steps: rebuild the code, run tests, and run performance workloads", and the draft's own Table 1 says FormulaCode does no build per edit (`background.tex` L25). Write "most of them".
- L10–14: the "the measurements moved the question" narrative is honest, and it is the true story. Keep it, but in three sentences, not five. Reviewers dislike "this paper started as…" at length.
- L16–20 (motivating edit): **strong. This is the teaser the plan asked for.** Add one clause that the edit is reached by *static* reach (all 171 cases). That makes the point that static reach is not the evidence.
- L31–39 (F1–F4): F3 has an arithmetic gap. "Of the 7 it misses, 5 are in functions no benchmark reaches, and one is in a function … only 0.004–0.005 of their time" accounts for 6, so #4 is missing. Write "five … are reached by no benchmark at all, one more (#4) by no measured profile, and one (#3) …", or give the 7 = 6 coverage + 1 share split directly.
- L41–48 (contributions): **five is too many.** Collapse to three:
  1. the cost breakdown (RQ1);
  2. the oracle-visibility measurement: coverage, plus share and power as the reasons a reached edit can still be missed (RQ2 + RQ3), with the Traini-narrowed novelty sentence;
  3. overhead-honest RTS plus the negative result (RQ4).

  "Lessons" (item 5) is a subsection, not a contribution. The plan (K6) said that it "protect[s] the paper against reviewer doubts more than [it] add[s] novelty".
- L44: the novelty sentence is correctly narrowed after Traini. One problem: it cites Shahedi, Grambow and FormulaCode as support for an *absence* ("what we did not find … \cite{…}"). Cite them where they are described (§2), and support the absence by the search log instead (`background.tex` L61).

### Background (`background.tex`)
- L4–28 (Table 1): good, and it answers P08. Resolve the TODO at L5 by citing the survey in the artifact.
- L38–50: **the best related-work paragraph in the draft.** L46–47 ("Per-commit profiling of benchmark reach is therefore not new") is exactly the right honesty after Traini. Keep it verbatim.
- L45 (Peass) and L42 (Laaber & Leitner 2018): these two are why the three-factor split is not new as a *concept* (see §4). Say so in one sentence: "Peass and Laaber & Leitner split misses into uncovered and below-noise; we add the share of case time as a separate cause and measure all three per edit."
- **Missing:** the share effect is Amdahl's law applied to a benchmark case, $1+s(f-1)$ (`discussion.tex` L19). Cite Amdahl (read the paper first; it is not in `refs.bib`) or a profiling text that states it. Otherwise a reviewer will write "this is Amdahl's law" as if we had missed it.
- L58–62 (positioning): good. The search counts are useful. Keep "targeted, not systematic".

### Study design (`design.tex`)
- L4–9: L5 says "no generator's biases enter the edit set". The mining regex is a generator of bias: it selects commits whose authors *say* "faster". Rephrase: "no optimizer's biases enter; the mining rule's biases are discussed in §Lessons."
- L7: "written and frozen before the measurements" sits uneasily with deviation (4) (`threats.tex` L32): the labels that define RQ2's primary edit set were added after mining and after B1 was first seen. The hostile reviewer also asked for a checkable commit hash (L8 TODO). Until that hash is in, say "a written protocol, committed before the measurements (commit X)" and list the post-hoc parts here, not only in Threats.
- L47–54 (labelling): honestly written, but it is the weakest construct in the paper (see §3, C6). I do not accept "agent-only, by the authors' decision" (L54) for E1. Minimum: the student labels, blind, all 20 networkx rows and a random 30 E1 rows, and we report human-vs-agent κ.
- L41–45: the changed-function rule is clear. The hand-check TODO (L45) is cheap; do it this week.
- L61–70 (arms): fine. A4 gets one sentence here, which is correct.
- L80–91 (oracles): L84–88 are dense but complete. L89 ("Test assumptions") is good practice; keep it.
- L93–99 (platform): fill in the hardware macros. Move the ethics sentence (L97) to the end of the section; it interrupts the timing protocol.
- **Table 2 (subjects) is missing** (L34 TODO). For a mining study it is compulsory. Generate it now from the networkx data, with the date span and diff size from L39, and leave the E1 rows empty.

### RQ1 (`rq1-cost.tex`)
- L9–14: say which passes are clean. Five of the six passes are 659–751 s; the 1668 s pass is noisy and the 2444 s pass is the #1 oracle side. "8–28×" is therefore a median of about 8× plus two outliers under drift, not a spread. Report it that way (see §3, C1).
- L23–29: this is where RQ1 is honestly weakest. 80–94 % of a pass is setup outside the timing loops in **one module** that builds its graphs at import time. A reviewer will call RQ1 a networkx suite-design artefact (hostile reviewer #6). **E5 (measured setup-cached pass) is close to MUST for the "expensive" half of the title.** If E5 gives about 1.5×, the cost claim becomes "benchmarks are still the largest part, but not by an order of magnitude", which also makes "Expensive" in the title wrong.
- L31–34 (drift): move to the appendix, leaving one sentence here. It is a threat, not a result.
- L36–40 (bottleneck): fine as a contrast. Without the overnight benchmark pass it shows only the build share; say that in the sentence, not only in the TODO.

### RQ2 and RQ3: merge into one section (`rq2-coverage.tex`, `rq3-power.tex`)
**Structural change, the most important one in the text.** The two sections are one argument: can the benchmark oracle see this edit? Today the reader meets coverage in RQ2, then has to rebuild it for the slowdowns in RQ3 L27–31, and meets the share factor only halfway through RQ3. Proposed structure:
1. **Coverage** (current RQ2 L4–33): optimization edits, measured versus static reach.
2. **Share** (current RQ3 L22–38): **extended to the 6 reached optimization edits**, not only to the slowdown functions. The share of each changed function in each reaching case's time is a cProfile run with no timing (the same `slow_share.py`). It turns V1 from one case (#3) into a per-edit distribution on 14 edits, and it is cheap. Do it before the next draft.
3. **Power** (current RQ3 L42–60).
4. **Injected slowdowns as the check** (current RQ3 L4–13 plus Fig. 3): the slowdowns are where the three factors are *tested*, not where they are introduced.
5. **One per-edit table** for all 14 optimization edits, with columns *executed? / max share in a reaching case / detectable at 1.2× and 2× (by bootstrap)*. That is the plan's "effective oracle coverage" (§5 step 1), now partly in the discussion as a TODO (`discussion.tex` L17–22). It belongs in the results.

Specific lines:
- RQ2 L8: "the reading does not depend on the labels". The two label sets come from the same agents plus a subject reading. Write "does not depend on which of our two label sets is used".
- RQ2 L18–25 (reach at the base state): good work, and it answers the hostile reviewer's critical #2. It can shrink to three sentences.
- RQ2 L27: remove "(the advisor's threshold: below a quarter)" from the TODO before anyone else reads it. A paper does not cite its advisor's threshold. Cite the pre-registered E1 decision rule instead.
- RQ2 L39–42 (suite design as a moderator): no evidence yet. The bottleneck claim is labelled a conjecture, and the one fact (a `nanmax` benchmark that calls `nanmin`) is a source reading. Move it to the Discussion as a hypothesis for E1.
- RQ3 L11: the multiplicity paragraph is good. Keep it.
- RQ3 L34 and L39: two claims I will not sign (§3, C3 and C4).
- RQ3 L40: the pre-registered primary result ("not measurable") is buried mid-section. State it first in the safety discussion. It is the pre-registered answer, and leading with it is the honest order.
- RQ3 L65–69 (statistics) belongs in Design or Lessons. RQ3 L71–76 (profile completeness) can go to the appendix with one sentence left here.
- RQ3 L79: "moderate slowdowns there are likely to go unseen" is stronger than the abstract's "suggests" (abstract L9) and F3's "suggests" (intro L37), and it rests on 3 of 49 cases. Use the same hedge in every place.

### RQ4 (`rq4-reductions.tex`)
- Table 1 and L28–34: good. The 15× versus 3.5–4× contrast is a useful correction to how test selection is reported.
- L34: overgeneralizes (§3, C5).
- L39: "Any periodic full check catches both one or two steps later" holds only for k ≤ 2 at those steps. Give k.
- L42–47 (A4): **still too long for the plan.** The plan said "one paragraph plus an appendix", and this is a full paragraph of six sentences with three numbers. Cut it to three sentences: what A4 is, that it behaved like k ≈ 4 periodic checks, and that testmon dominates it. Everything else goes to Appendix A.
- RQ4 could become a short §7 of about half a page. Space is better spent on the per-edit oracle table.

### Discussion (`discussion.tex`)
- L5–8: the strongest implication paragraph. Fix L6 and L7 (§3, C7 and C8).
- L10–15 (recommendations): good and concrete. **The TODO at L15 needs no new run.** Counting how many unreached optimizations at least one unit test executes uses the existing depmap. Do it before the next draft. It is the deterministic baseline Study 2 must beat, so it bridges the two studies, and it answers P10 in the meeting.
- L17–22 (effective oracle coverage): either compute it (see the RQ2/RQ3 restructure) or cut it to two sentences of future work. A discussion paragraph that promises a number we have the ingredients for invites "why didn't you?".
- L28–47 (lessons): keep mining precision and the 6-versus-6 trap in the main text. The 2.4 % nondeterminism and the stale-binary pass can be two sentences each, as the plan said.

### Threats (`threats.tex`)
- Well organized (Wohlin order, specific threats). It is the best-written section.
- L8: the labelling threat is stated honestly, but stating a threat does not mitigate it. See §3, C6.
- L33: "The method contains no learned or LLM component" is false as written (§3, C9).
- L25: "We judged the one off-target flag (#1) noise by a reach argument, not by re-measurement" is good. E3 tonight replaces it.

### Conclusion (`conclusion.tex`)
Fine and short. L7 should carry the scope in its verb, for example "On this project, the limiting part … was the performance oracle". It already says "On this project", so this is minor.

### Appendix (`appendix.tex`)
Right content in the right place. Appendix B (static pilot) is good for showing why measured profiles were needed. `fig_precision.pdf` is unused (review log #25): put it in §Lessons or delete it.

---

## 3. Claims I would not sign off on

| # | Where | Exact sentence | Why |
|---|---|---|---|
| C1 | `abstract.tex` L5; `introduction.tex` L35; `rq1-cost.tex` L12, L43 | "a full benchmark pass costs … about \NxBenchRatioLo–\NxBenchRatioHi× the build plus the serial test suite" (8–28×) | The upper end comes from the #1 oracle side (2444 s) under drift, and the 1668 s S0 pass is labelled noisy. Five of six passes give about 8×. A range that is mostly two outliers misleads. Say "about 8× at the median pass (up to 28× under unexplained drift)". Add the setup-cached estimate to the abstract, because it decides how robust "expensive" is. |
| C2 | `abstract.tex` L8 | "Most misses are in functions no benchmark executes" | 6 of 7, Wilson lower bound ≈ 49 %: our own rule forbids "most". Give the count. |
| C3 | `rq3-power.tex` L34; `discussion.tex` L19–20 | "no number of repetitions would make it visible to these cases" / "cannot see even a doubling, however many repetitions it runs" | Under **asv's rule** this is true, because the ratio condition (> 1.1) cannot be met at ≈ 1.005×. Under the statistical test alone it is false: with enough samples, Mann-Whitney can detect a 0.5 % shift if noise allows. Write "asv's ratio condition can never flag it, and no practical repetition count resolves a 0.5 % effect against this noise". The share is also an approximate cProfile estimate, so call it "about 0.5 %". |
| C4 | `rq3-power.tex` L39 | "No selection rule can detect more than the full suite" | Not true in general. With the same time budget, a selected subset can be run with more repetitions and gain power. It is also contradicted by the oracle's own design, where verdicts used more processes than the cost passes. Restrict it to "no selection *of these cases at this protocol* can detect more than running all of them". |
| C5 | `rq4-reductions.tex` L34 | "Reported reductions in tests run … are therefore not reductions in validation time." | One project, one testmon run, under mixed load. The finding supports "are not proportional reductions in validation time; on networkx, a 15× cut in test-seconds became 3.5–4× end to end". |
| C6 | `design.tex` L47–54; RQ2 throughout | The primary RQ2 edit set: "the commits both raters or the adjudicator labelled as optimizations" | The labels define the denominator of the paper's headline result. They come from two same-family LLM agents and an LLM adjudicator, with κ = 0.948 that the text itself says is inflated. No human ever read the diffs. That is an unvalidated construct, not just a threat. I will sign once a human (the student) has labelled at least the networkx rows blind and the human-agent κ is reported. P26 ("did you read the diffs?") will be asked, and the answer must be yes. |
| C7 | `discussion.tex` L6 | "For such edits the benchmark verdict 'not slower' carries no information about the edited function" | It holds only for function-body changes. Module-level changes were excluded from coverage counts (`design.tex` L43), and profiles are one-call samples (`rq2-coverage.tex` L46). Write "carries no information about the changed functions, as far as one profile shows". |
| C8 | `discussion.tex` L7 | "Reducing build and test work, which existing tools already do well" | We measured one existing tool on one project. "do well" is an evaluation we did not make. Write "which existing tools already do". |
| C9 | `threats.tex` L33 | "The method contains no learned or LLM component." | The edit labels, which define RQ2's edit set, come from LLM agents (the next clause says so). The *selection rules* contain no LLM component. Say exactly that, or the "no AI first" framing reads as contradicted by our own threats section. |
| C10 | `rq3-power.tex` L79 (and the matching F3 wording) | "#1's only flag is an off-target noise verdict" | We *judged* it noise by a reach argument, and E3 has not run. Write "which we classify as an off-target flag; repetition is pending". |
| C11 | `introduction.tex` L5 | "validate each candidate in the same three steps: rebuild the code, run tests, and run performance workloads" | Contradicted by Table 1 (FormulaCode: "none per edit"). Write "most validate…". |
| C12 | `design.tex` L7 | "The protocol … was written and frozen before the measurements" | Not checkable without the commit hash, and not true for the RQ2 edit set (labels added post hoc). Qualify it in place, not only in the deviations list. |

---

## 4. Should "executed / visible / detectable" become the central contribution and title?

**No, not now. Make it the organizing frame of the merged oracle section and a named contribution, but keep it out of the title and do not let it become the headline claim until it is measured per edit across projects.**

Reasons:
1. **The concept is not new, and reviewers will see that at once.** "Visible" is Amdahl's law applied to a benchmark case: the case changes by $1+s(f-1)$. "Executed versus detectable" is the Peass split (uncovered versus below noise) and Laaber & Leitner's detection-based coverage, both cited in §2. A title built on the decomposition invites "a known identity with a new name", the same "composition of known parts" objection as in the persona (objection 4). What is new is the **measurement**: how often each factor bites for real optimization edits.
2. **The middle factor rests on n = 1.** V1 is one slowdown (#3) in one function, with a cProfile share the text itself calls approximate, on a synthetic double-call probe. #2 confirms the prediction, and #8 does not fit the formula. That is a sound observation and a good sentence ("executed is not visible"). It is not a result that can carry a title.
3. **The share has been measured only for slowdown functions, not for the optimization edits.** RQ2's 6 reached edits have no share yet. Until they do, we cannot say how often "visible" bites, which is the only quantitative claim the frame could make.

**What would change my answer.** Suppose (a) the share is computed for every reached optimization edit (cheap: cProfile, no timing), on networkx now and on the E1 projects later, and (b) E2 gives per-case noise for the reaching cases. Then the paper can report, per project, the share of optimization edits that the suite could see at 1.2× and 2×. That is the "effective oracle coverage" of the plan (§5 step 1). If that number is low and varies with suite design, it becomes the central contribution and earns the title, for example *"Executed Is Not Visible: Can Project Benchmarks See Optimization Edits?"*

**Title for now:** something plain that does not overclaim either half. For example: *"Can the Benchmarks See the Edit? Cost and Visibility of Per-Edit Validation for Python Optimization Commits — A Case Study on networkx"*. Keep "expensive" out of the title until E5 has measured the setup-cached cost.

---

## 5. Venue and timeline check against my plan

**Where the draft stands against the plan's minimum set (plan §2):**

| Plan item | Plan status | Draft status | Gap |
|---|---|---|---|
| E1 replication | MUST, ≥ 5 projects, ≥ 60 edits, two raters incl. diff reading, κ | "3–4 projects, after the meeting", agent-only labels | **Fewer projects than planned, and no human rater.** I would accept 4 projects if they give ≥ 50 true optimizations pooled; I will not accept agent-only labels. |
| E2 σ + 1 + 3σ | MUST | tonight | on track |
| E3 oracle repeatability | MUST | tonight | on track |
| E5 setup-cached pass | SHOULD (close to must) | TODO, not scheduled tonight | **Schedule it**: the "expensive" claim depends on it. |
| E6 repeated passes | SHOULD | tonight (drift passes) | on track |
| E4 second-project cost | SHOULD | TODO | fold into E1 if one project has a cheap build |
| §5 step 2 (unit-test fallback count) | high value, no run | TODO | do it this week |
| Share for reached edits (new, from V1) | — | not planned | add it: cProfile only, cheap |

**Venues (deadlines not verified; confirm against current calls):**
- **ESEM 2027, full paper**: still the first choice. Its main deadline is usually in spring, which leaves room for E1 in December and January, writing in February and March, and an internal review cycle. ESEM uses the ACM format with its own page limit: confirm the limit and plan the switch to `acmart` (the preamble comment at `main.tex` L2 already anticipates it). Twelve IEEE pages will not fit as they stand.
- **Short version now (optional)**: 5–6 pages on networkx (cost, coverage, the "executed is not visible" observation, and the E1 protocol). Candidates are an ICSE-co-located workshop or a registered-report track. Several such deadlines fall in December and January; check them this week. Do it only if it costs at most a week of the student's time and the venue permits a later extended version.
- **ICPE**: not yet. It needs a pinned native-Linux machine for E2, E3 and E5 (agenda A12). Without one, the WSL2 drift (1.7–3× setup drift) is the first thing those reviewers will attack.
- **Not** the ICSE or FSE research tracks (unchanged from the plan).

**Timeline.** The plan expected E1 + E2 + E3 + E5 in about two weeks from 22 Nov. With E1 now after the meeting, a realistic schedule is E1 complete by mid-to-late December, the second full draft by mid-January, and submission-ready by about February for a spring ESEM deadline.

**Before I would let it be submitted (gates):**
1. E1 done and analysed per project and pooled, with profiles at each edit's parent, and the thesis restated or reframed by the pre-registered rule.
2. A human rater (the student) has labelled at least the networkx rows and a random sample of E1 rows blind, with human-agent κ reported.
3. E2 and E3 run; every verdict reported against the 1 + 3σ floor; #1 and #8 resolved.
4. E5 measured; the cost claim and the title follow from the measured setup-cached cost, not from the estimate.
5. The share is computed for the reached optimization edits, and the per-edit oracle table is in the results.
6. Every claim in §3 of this file is fixed.
7. The frozen-protocol commit hash and date are cited, and the post-hoc parts are listed in Design.
8. The student has personally re-derived every headline number (abstract and F1–F4) from the raw files. The 70 "quoted" macros (review log #12) are computed by `make_all.py`, not typed.
9. Zero `\TODO` or `\citeneeded`; `check.py` clean; the artifact has a DOI or an anonymized link.
10. The AI-assistance disclosure is written to the chosen venue's policy, covering both the tooling and writing assistance and the LLM labels. This is an integrity requirement, not a formality.

---

## 6. Three questions I would ask in the meeting

1. **"Did you read the 14 diffs yourself? Would you put your name on each label?"** If not, why should the E1 labels stay agent-only, when the denominator of the headline result depends on them? (P26; it pairs with C6.)
2. **"For the six optimization edits that a benchmark *does* execute, what share of the reaching case's time is the changed function? How many of the six could the suite actually see?"** This is the number that decides whether "executed is not visible" is the paper's contribution or a footnote (§4). It needs no timing run.
3. **"If the setup-cached pass comes back at 1.5× build plus tests, what is left of 'expensive', and what is the paper then about?"** I want to hear that the student already knows the answer: the visibility half survives on its own, and the cost half becomes motivation (P24, P25).
