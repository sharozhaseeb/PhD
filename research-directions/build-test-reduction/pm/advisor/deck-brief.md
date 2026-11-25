# Deck brief for the Study 1 advisor meeting (24 Nov 2026)

Written 2026-11-24 by the advisor-persona subagent (**AI-SIM**: a model of the advisor, not the advisor). Based on night-2 results as of 03:30 PKT.

Read: `persona.md`, `review-final-results.md`, `review-paper-draft-1.md` (E1 and label sections), the `meeting-2026-11-advisor/*.md` pack, `knowledge-base/findings.md`, `01-literature/beyond-literature-claims.md`, the paper sections (abstract, introduction, RQ1, RQ4, threats, plus a skim of oracle), `generated/numbers.tex`, and `results.md` (RQ1 headline, E3 tier 2, E5, Directory A/A, dir-swap tier 2).

**Warning before anything else: parts of the meeting pack are stale after night 2.** Do not copy slides from these passages:
- `00-one-page-study-statement.md` and `03-results-summary.md` S1 say E5 is "estimate, not measured… planned for the night of 23→24". **It is now measured (N15).**
- Both files, and S7, say "directory rotation starts tonight". **The rotation is now done and did not remove the flips (N14).**
- The one-pager still lists **3 RQs**, while the paper has **4** (cost, coverage, visibility, reduction). Pick the paper's four and say so. Two RQ lists in one meeting invites a "which is it?" question.
- `beyond-literature-claims.md`'s B1 safe wording still says **9/15**. The deck uses **8/14 (agent labels)**.

Path shorthand used below: `F:` = `knowledge-base/findings.md`, `R:` = `03-experiment/results/results.md`, `NUM:` = `04-paper/generated/numbers.tex`, `LIT:` = `01-literature/beyond-literature-claims.md`.

---

## 1. The hardest questions, ranked, with the answer the deck must give

**Q1. "Your brief was 'reduced build + reduced tests'. You found build is negligible and test selection is solved by testmon. So what is Study 1's contribution, and is it beyond the literature?"**
- **The deck must say:** the contribution is a measurement study with one lead finding. The benchmark oracle, not build or test cost, limits per-edit validation of optimization edits.
- Show three facts:
  - **Executed:** 8 of 14 agent-labelled optimizations are executed by no benchmark: 57%, Wilson 33–79% (F: B4; NUM `BOneAgentUnreached`).
  - **Visible:** at a 1.2× slowdown of the changed function, at most 4 of 14 edits could even clear asv's 1.1 ratio, and 5 of 14 at 2× (F: V2).
  - **Detectable:** above the pre-registered floor, FULL detects 1 of 10 injected slowdowns, Wilson 1.8–40.4% (F: N9).
- Novelty is narrowed to "the rate". See §2.
- **Honest gap:** "this is one project. The replication E1 is the gate for the full paper."

**Q2. "Is B1 a networkx problem or a Python/asv problem? How many projects?"**
- **Honest gap. Say:** "One project. B1 was *not validly tested* elsewhere: static reach from old bases, pvlib has no asv suite, bottleneck is template code (`03-results-summary.md` S2; paper Appendix Q3). E1 is pre-registered for after this meeting."
- Do **not** show the static pilot on other projects as support.

**Q3. "E5: with setup cached, benchmarks are only about 2× build+tests. Is your cost headline an artefact of a badly set-up suite?"**
- **The deck must say:** "Partly yes, and we measured it."
  - Under asv's standard protocol, a FULL pass is at least about 8× build+tests (659–2,984 s over 9 passes, median about 14×; NUM `NxBenchRatioTypical/Median/Hi`). Same night as E5: 7.8–8.1×.
  - Setup-cached, it is **2.2–2.3×** (median 195 s vs 691 s standard, 3.54×; F: N15).
  - So benchmarks are still the largest single part, but not by an order of magnitude when cached.
  - The STD−CACHED gap of 484–504 s is *inferred* to be per-process start-up and re-import.
- **Caveat to say aloud:** E5 ran on a fast night, so the ratio on slow nights is not measured. 3.54× is not a strict lower bound.

**Q4. "You claim no AI in the method. Who labelled the 14 optimizations?"**
- **The deck must say exactly this:** "The selection and validation rules contain no learned or LLM component. The edit labels that define the B1 denominator come from two blind LLM agent raters plus an LLM adjudicator, all the same model family. κ = 0.948 is inflated for that reason. No human rater." (F: B4; paper `threats.tex`.)
- Robustness to show: on the earlier subject-only reading, B1 was 9/15. It moves by one edit (F: B1, B4).
- Mining precision is 50/70 = 71% [60–81%] pooled, and pvlib is only 3/14 (F: B4).
- Then raise A14 yourself (see §5). **Do not wait to be asked.**

**Q5. "Why should I believe any benchmark verdict? What is your false-verdict rate?"**
- **The deck must say:**
  - In the 12v12 A/B design, about 2% of off-target comparisons give a non-"same" verdict:
    - 2.2% with fixed directories (11/499);
    - **2.4% with identical code** (directory A/A, 4/168, Wilson 0.9–6.0%);
    - 1.8% with the directories swapped (6/340) (F: N14).
  - So **single verdicts of ≤ about 1.4× in either direction are not evidence** (largest identical-code deviation: 1.308× slower, 0.725× faster).
  - #2's 1.76–1.90× stands: it is above that band, cleared its own floors (1.08–1.33), and repeated in tier 1 (F: N9, N14; R: §Directory A/A).
  - This works out to about 4 false "changes" per 171-case comparison (range 1.6–10), **for the 12v12 design only**.
- **Honest gap:** "The 18v18 oracle design itself was not A/A-tested at this scale."

**Q6. "Did the directory swap fix the confound?"**
- **Honest gap. Say:** "No. The swap gives the same rate, and no flip reverses sign, so a directory effect alone does not produce them. The cause is unresolved. Candidates: per-night variation, an anti-conservative test on correlated samples (12 samples from 4 processes per side), or a case-specific effect (`connected_components ER(100,0.9)` recurs)."
- Sign consistency is not evidence: the identical-code flips also kept their sign 4/4, and 3 of 4 #8 cases vary between nights (R: §dir swap).
- Next test: a process-level analysis or more processes per side.
- **Also say:** #8's on-target 1.12–1.20× was *not* re-tested in the swap, so #8 stays uncounted (WORKLOG 03:30).

**Q7. "Executed is not detected. Isn't 'no benchmark executes it' just a lower bound on the problem? And which reach is right, profile 8/14 or static 3/14?"**
- **The deck must say:**
  - Static reach over-approximates. The motivating `bidirectional_dijkstra` edit is statically connected to all 171 cases, yet no profile executes it.
  - The profile under-approximates: one call per case, S0 only.
  - 0 of 14 edits are unreached by construction (F: V1).
  - The share argument is in F: V2. #3 is a dilution miss: share 0.005, so expected about 1.005× (F: V1).
- **Honest gap:** "Profiles at each edit's parent are planned for E1. A benchmark added between S0 and an edit would bias the unreached count upward."

**Q8. "Your mutants sit in the edited functions, so every selector catches them. What does RQ4 actually show?"**
- **The deck must say:**
  - **Design limitation:** this fault model cannot rank selection rules; it only shows the cheap arm is not obviously unsafe.
  - **Real negative, as implemented:** A4 (655 s est.) is dominated by plain testmon (330 s). With benchmarks counted, batching is 1.7–6× cheaper. A4 costs about 2× batching at matched cost, and that is conditional on B2 (profile selection collapses to 171/171) (`03-results-summary.md` S4; F: B2).
- testmon is 3.5–4× cheaper end to end, not the 15× that test-seconds suggest. That is a single run under mixed load (F: T1).
- Functional misses: 0/20 frozen mutants, Wilson 0–16.1%, simulated, caught almost by construction.

**Q9. "88% of cost was setup and 8 of 9 passes are noisy. Are your cost numbers even reproducible?"**
- **The deck must say:**
  - 8 of 9 networkx passes are noisy by one uniform rule (F: N13).
  - Three passes in one evening drifted 2,984 → 1,217 s (2.45×), with the timing loops stable at 144–155 s. The cause is unknown (F: N12).
  - That is why the headline is reported as a range with a lower bound of about 8×.
  - bottleneck: two passes 0.5% apart, 544 and 547 s, about 18.5–19×. That is one state, labelled noisy (F: R5).
- **Honest gap:** "One WSL2 machine; the governor cannot be pinned."

**Q10. "What does 'build' mean for Python? Did you study a heavy build?"**
- **The deck must say:**
  - networkx editable install: median 1.19 s, 0.04–0.16% of a full validation once benchmarks count.
  - bottleneck clean build: 4.7–5.4 s, 16–18% of build+tests, but 0.8–0.9% once benchmarks count (F: R2, R5).
- **Honest gap:** "The scikit-learn heavy-build measurement was planned and not run. We make no claim for heavy builds."
- Mention H1 (stale `.so` false pass) as a harness lesson only.

**Q11. "Historical commits are weeks apart and large. That is not an optimizer session."**
- **Honest gap. Say:** "Replay of non-adjacent commits; no session effect is claimed. Per-edit coverage and visibility do not depend on the session model. Cost totals and the accumulation policy do." (paper `threats.tex`, External.)

**Q12. "Why is 50–60 optimizations / 4–5 projects the right E1 size? And what if the pooled rate is low?"**
- **The deck must say:**
  - At n = 14, the Wilson interval is 33–79%, which is ±23 points.
  - At n ≈ 50–60, a 50% rate has a half-width of about ±12–14 points (my arithmetic; put it in the slide notes as "computed").
  - At 71% mining precision, 50–60 true optimizations needs about 70–85 mined candidates.
  - The pre-registered decision rule decides the thesis. If the pooled unreached share is low, the paper reframes around suite design (abstract TODO).

**Q13. "What is Study 2, and does Study 1 hand it anything?"**
- **The deck must say:** "Undecided (A9). The evidence-driven proposal: close the coverage gap B1 exposes, with per-edit targeted workloads judged by the B1 coverage metric, detection at a measured floor, and cost."
- Deterministic baselines come first: time the existing unit tests that reach the function (as SWE-Perf does), parameter sweeps, and performance fuzzing.
- **Say the novelty risk:** WEDGE, PerfForge and the 2026 benchmark-rethinking preprint.

**Q14. "Venue and timeline?"**
- **The deck must say:**
  - Proposed: ESEM 2027 full paper after E1. E1 by mid-to-late December, draft 2 mid-January, submission-ready about February.
  - Optional: a 5–6-page short paper now.
  - **Deadlines not verified** (agenda A10).
- The draft is 14 pp; the paper is currently 14 IEEE pages and ESEM uses ACM format.

**Q15 (likely, short). "Why testmon and not NameRTS? Is this just CI batching?"**
- NameRTS was not run (A7), and that is the honest answer.
- The trigger is conceded to be a deterministic variant of risk-mass batching (Sayedsalehi 2026; LIT C1).

---

## 2. Novelty: what to claim, what not to claim, and the close work to name

**Claim (exact safe wording, adapted from LIT row B1 with current numbers):**
> "Per-commit profiling of benchmark reach exists (Traini et al., TOSEM 2021, for Java refactorings). Prior work excludes or notes benchmark-uncovered commits. In our recorded searches we found no study reporting what fraction of real performance-improving commits have their changed functions executed by the project's own benchmark suite. We measure it for one project: networkx, 8 of 14 agent-labelled optimizations, Wilson 33–79%."

**Secondary claims, each with "in our recorded searches":**
- A per-candidate build/test/benchmark cost split for optimization loops (R1, *partial*).
- Per-edit miss rates when dropping benchmarks by reach or profile, for Python/asv (C11 reach-dropping part, *not found*).
- Incremental-rebuild correctness for Python extension modules (C8, *partial*; our evidence is one replay artefact).

**Must NOT claim:**
- That per-commit benchmark-reach profiling is new. Traini 2021 did it.
- That the uncovered / below-noise / not-selected split is new. Peass (Reichelt 2023) and Laaber & Leitner MSR 2018 already split misses this way. Our "share" is Amdahl's law operationalised.
- That per-edit test selection in an optimization loop is new. PerfAgent uses testmon per iteration.
- That the accumulated-change trigger is a new mechanism. It is a deterministic variant of risk-mass batching (Sayedsalehi 2026; Bavand & Rigby 2021).
- That a two-sided performance oracle is new. SemOpt's gate and PerfAgent's "fastest passing patch" already do this.
- That "nobody has done this", or that the review is systematic. There was no Scopus or Web of Science search, and ACM/IEEE were not re-run for the measured findings.
- That B1 is general.

**Close work to name on one slide, with how we differ:**

| Work | What it does | How ours differs |
|---|---|---|
| Traini et al. TOSEM 2021 | Per-commit JMH reach, refactoring commits, 31 Java projects | Ours: performance-improving commits, Python/asv, and we report the **uncovered rate**, which they do not |
| Laaber & Leitner MSR 2018 | Injected slowdowns in 20 sampled API methods; "covered" means detected | Ours: reach of real changes, not sampled methods |
| Peass (Reichelt 2023) | Uncovered vs noise split of missed regressions, Java | We reuse the split; we do not claim it |
| Shahedi et al. 2025 | Exclude commits with no targeting benchmark, report no rate | Their coverage is a filter; ours is the outcome |
| Grambow et al. (TCC, PeerJ CS 2021) | Microbenchmark coverage of app-benchmark functions, fixed versions, Go | Ours: per-commit, optimization commits |
| FormulaCode / SWE-fficiency / SWE-Perf / GSO | Harnesses that require a workload speed-up or a covering test | They cannot measure the uncovered fraction by design |
| Ding et al. ICSE 2020 | Tests that cover a change rarely show its speed-up | Applies only to already-covering tests |
| PerfAgent, SemOpt | Optimizers that validate every candidate (testmon per iteration; full build + tests + 6× perf runs) | Ours measures what that validation costs and can see |
| Quansight 2021 (asv A/A, blog) | 3.7–12.5% false positives in asv CI | Context for N14; not peer-reviewed |

---

## 3. Recommended storyline (14 slides, about 22 min)

1. **Study 1 in one line.** Can per-edit validation of optimization edits be cut with deterministic reduction (build, tests, benchmarks), and what can the cheapest trustworthy check see? No AI in the rules.
2. **Why it matters.** Optimizers (SemOpt, PerfAgent; harnesses SWE-Perf, GSO, FormulaCode) build, test and benchmark every candidate, so the cost multiplies per edit. Use the motivating edit: `bidirectional_dijkstra` "1.1x to 25x faster", with no benchmark executing it.
3. **Setup.** networkx (pure Python, 171 asv cases, 6,771 tests) and bottleneck (C extension). 18 replayed historical commits, 14 optimizations by agent labels. One WSL2 machine. Pre-registered rules.
   - Four RQs: cost, coverage, visibility, reduction.
4. **RQ1: where the cost is.** Benchmarks are at least about 8× build+tests (median about 14×, up to 34× under drift). bottleneck is about 18.5–19×. Build is ≤ 0.9% once benchmarks count.
5. **RQ1 caveat, measured (E5, new).** Setup-cached, the factor is 2.2–2.3×, so much of the cost is suite design. Benchmarks are still the largest part. Fast-night caveat.
6. **RQ2: executed?** 8/14 unreached by profile (33–79%), 3/14 by static reach. Explain why the two differ, using the worked example.
7. **RQ3: visible and detectable?** Share bound: at most 4/14 edits can clear 1.1 at a 1.2× slowdown. FULL detects 1/10 slowdowns above the floor. The heavy module resolves only ≥ about 1.5×. Pre-registered: regression safety of reduced selection is not measurable.
8. **How far to trust a verdict (night 2).** About 2% non-"same" with identical code, fixed or swapped directories. Verdicts ≤ about 1.4× are not evidence. #2 at 1.8× stands. Cause unresolved.
9. **RQ4: reductions.** testmon is 3.5–4× end to end (not 15×). Changed-module misses 2/20. Incremental build saves nothing here. One table.
10. **RQ4: our policy, a negative result.** The fault model cannot rank rules (a limitation). A4 as implemented loses to testmon and to batching (B2). One slide only.
11. **What is new, and the close work.** The safe wording from §2 and the Traini/Peass/Laaber table. Name the non-claims explicitly.
12. **Limits.** One project for B1; agent-only labels; S0 profiles; replay is not a session; one noisy machine; no heavy build; the 18v18 design is not A/A-tested.
13. **Next: E1 replication.** Pre-registered, 4–5 projects, ≥ 50–60 optimizations, profiles at each parent, decision rule. Then per-case σ and a process-level test. Paper: ESEM 2027 after E1, plus an optional short paper.
14. **Decisions I need from you.**
    - A13: lead with the oracle gap?
    - A14: who labels E1?
    - E1 size.
    - A10: venue.
    - A9: Study 2 direction.
    - A1: is a heavy-build project needed?

Backup slides: the worked edit (step 10), the batching table, the E5 phase split, power at 18v18, mining precision per project.

---

## 4. Overclaims to avoid

Night 2 (new):
- "The directory confound is resolved" or "the swap removed the flips". **False:** 1.8% with the swap, cause unresolved.
- "Bias SUPPORTED" read as a stable, case-specific directory bias. The frozen label only means the rate is above 0.5%. Recurrence was 1/6.
- "Sign-consistent flips are real edit effects." No: the A/A flips were 4/4 sign-consistent too.
- "#8 is detected" or "#8 confirmed by the swap". Its on-target cases were not re-tested, so it stays uncounted.
- "About 4 false changes per FULL comparison" applied to the 18v18 oracle. That figure is for the 12v12 design only.
- "Benchmarks dominate by an order of magnitude" without the cached 2.2–2.3×. Also "3.54× is a lower bound on caching savings": it is not strict, measured on a fast night.
- "The suite is badly designed." Say instead: "most of the standard-protocol cost is, by inference, per-process start-up and re-import, which module-level setup reuse removes". The phase split for STD is inferred, not timed.
- "E3 tier 2 confirms the oracle." It is complete for all 5 reached slowdowns, but the off-target rate is the finding.

Carried over:
- "Most optimizations are unreached." The CI includes 33%, so say "many".
- "FULL detects 2/10." Above the floor it is 1/10.
- "testmon is 15× cheaper." It is 3.5–4× end to end, single run, mixed load.
- "testmon is safe" or "0 misses". It is 0/20 frozen mutants, Wilson ≤ 16.1%, by construction.
- "A4 beats batching", or any A4 claim without "as implemented" and B2.
- "#9 shows reach-based selection is unsafe." The pre-registered flag stands but did not survive the floor (N9), is inside the ≤1.4× band (N14), and the ABBA re-check failed (P5).
- Speed-ups of the historical commits as confirmed. They were not re-measured.
- Any build-saving claim for Python, or any heavy-build statement.
- An iterative-session effect, or accumulation mattering (the null is 0/5).
- Anything about AI-based selection. Also "no AI anywhere": the labels are LLM-produced.
- Superseded numbers: 0.9–4.5 h, 40–180×, 8–28×, 1.5–2× estimate, 9/15 as primary, 22% build share.

---

## 5. My stance on the open disagreements, and how the deck should frame them

**A14: a human-labelled subset (declined by the student, D26).**
- **My stance is unchanged: I will not accept agent-only labels for the E1 denominator of a full paper.** The headline rate *is* a ratio over those labels. Same-model raters share errors, and κ = 0.948 says nothing about validity.
- The ask is small. The student labels blind:
  - the 14 networkx OPT rows plus the 6 non-OPT rows;
  - a random 30 E1 rows.
- Report human–agent κ and B1 under both label sets. That is roughly half a day.
- If the student still declines, an acceptable fallback is weaker but honest:
  - a second-model-family rater;
  - a pre-registered sensitivity analysis showing B1 under subject-only, agent and union labels (today: 9/15 vs 8/14).
- **Deck framing:** present it as a decision with options and costs on slide 14 (A14), and state the owner's current decision openly. Do not bury it in the limits slide. The real advisor decides. This persona is a simulation.

**E1 scale bar: ≥ 4–5 projects and ≥ 50–60 true optimizations.**
- **My stance:** this is the gate for a full paper. I would accept 4 projects if they give ≥ 50 pooled true optimizations, with per-project rates reported and no project above about 40% of the pool.
- Below that, it is a short paper on networkx plus the E1 protocol.
- Justify the bar by CI width, not taste: ±23 points now, about ±12–14 at n = 50–60.
- **Deck framing:** slide 13 shows the bar, the arithmetic (about 70–85 mined candidates at 71% precision, with pvlib-style low precision as a risk), the projects-with-asv shortlist, and the fallback. Then ask the advisor to confirm or cut it. Do not present the reduced "3–4 projects" from the paper's TODO as the plan; that is the slide I would push back on hardest.

