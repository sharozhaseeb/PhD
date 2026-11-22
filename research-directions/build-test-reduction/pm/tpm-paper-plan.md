# TPM paper plan: Study 1 → first-draft paper

Author: TPM subagent. Written 2026-11-22 ~15:30 PKT. Status: **recommendation**. Scope, thesis and venue are the PM's and owner's calls; the thesis and outline come from the advisor persona (`pm/advisor/paper-plan-advice.md`, in progress in parallel). This plan only covers feasibility, cost, schedule, risk and validity.

Inputs read: `pm/tpm-log.md`, `pm/CHARTER.md`, `knowledge-base/{findings,WORKLOG,decisions}.md`, `03-experiment/results/{RESUME,OVERNIGHT}.md`, `results.md` (RQ1 headline, Q3, A/A and 1 + 3σ sections). Nothing was run.

Labels: **measured** (from a project raw file), **inferred** (my estimate from measured rates), **unknown**.

---

## 0. Bottom line

- The paper that the current evidence supports is an **empirical study of validating performance-optimization edits** on Python projects. Its claims are: benchmarks dominate per-edit validation cost (R1); a large share of optimization edits is executed by no benchmark (B1, networkx only so far); unchanged RTS is cheap and functionally sufficient (T1, N1); the new policy brings no gain (N1, N4, N5). It is **not** a "new technique wins" paper. Its weakest link is that B1 holds on one project (9/15, CI 36–80 %). Experiment (a) is therefore the critical path; the others close validity gaps.
- **Go/no-go:**

| Exp | Verdict | When |
|---|---|---|
| (a) B1 replication, 3–5 projects, measured profiles | **GO, conditional**: (e) done first, pre-registration frozen, a grouped profile runner built; minimum 3 valid projects, maximum 4 | After the meeting; nights of 25 Nov to 5 Dec |
| (b) σ (A/A) for the flagged cases | **GO** | Tonight, first in the queue |
| (c) R1 cost breakdown, second project | **GO-limited**: a bottleneck FULL benchmark pass tonight (cheap); one new pure-Python project after the meeting, picked from (a) | Tonight (bottleneck); week of 30 Nov (new project) |
| (d) Repeated FULL passes / drift | **GO-limited**: 3 passes with telemetry tonight. **NO-GO** on open-ended diagnosis of the cause | Tonight, after (b) |
| (e) Mining precision by manual labelling | **GO**: human work, no machine time; it must come before (a) | Start tonight; done by 26 Nov |

- **Full first draft: Tue 2026-12-15** (slack to 2026-12-20). **Submission: the first verified deadline at least 6 weeks after the draft, realistically March–May 2027**, with an earlier short or workshop version as an option (§2.4).

---

## 1. Feasibility and machine-hours

Rates used (measured unless marked):
- FULL networkx pass (171 cases, 2 × 3): 659–2444 s, median ≈ 730 s.
- `benchmark_algorithms` setup per process: ≈ 4–47 s, varying over the day (N7).
- A/A runs at 5 × 3: `benchmark_algorithms` runs 132–235 s each; cheap cases 1–2 s.
- Build + serial tests ≈ 87 s per state (networkx); bottleneck clean build ≈ 5 s plus tests ≈ 24 s.

| Exp | Machine time | Idle-exclusive? | Engineering | Human (owner) | Main feasibility risk |
|---|---|---|---|---|---|
| (a) B1 replication, 4 projects × ≈ 15–20 edits | Clones and environments 2–4 h. Profiling: with a **grouped runner** (each benchmark module imported once per state, each case called once under `sys.monitoring`), ≈ 3–10 min per state, so **≈ 4–13 h**. With asv-style one-process-per-case profiling, ≈ 3–5× that (≈ 15–50 h), which is **not feasible** on one laptop in 2 weeks (inferred). | **No timing**, so not idle-exclusive for validity. It is CPU-heavy, though, so it must **never overlap a timing window**. It can run in parallel with writing. | 10–16 h: grouped profile runner 3–4 h; generalising replay and environment set-up per project 4–8 h; pre-registration 2 h; count script reuse 1 h | Pre-registration review 1 h | **Environment rot at old parents** (dependency drift, old Pythons via uv; inferred to be the main attrition source). Pre-register an attrition rule. |
| (b) σ (A/A) for the flagged cases | 12 cases: #1 (1), #2 (8 on target + `NonNeighbors`), #8 (1), #9 (1). 5 repeats × 2 sides, **each in its verdict's protocol** (#1/#2/#8 at 2 × 3; #9 at 5 × 3). ≈ 1.0–1.7 h (inferred from A/A per-run times); **cap 2 h**. | **Yes** | 1–1.5 h: plan, case list, reuse `aa_noise_nx.py` with checkpoints | — | Machine drift inflates wall time (N7). The cap and checkpoints contain it. |
| (c) R1 on a second project | Bottleneck: one FULL asv pass at `f51ed86` × 2, ≈ 0.2–0.5 h (inferred from the hazard run). New project: build + serial tests + FULL pass at 3 states × 2 passes ≈ **2–6 h** (unknown suite size; cap per night). | **Yes** | 3–4 h (new project's asv config and timing labels) | — | An asv suite that takes hours. Mitigation: pick by a pre-declared suite-size bound. |
| (d) Repeated FULL passes / drift | 3 passes at S0 (2 × 3) + a 1-minute canary (2 cheap cases + one `benchmark_algorithms` case) between passes: **≈ 0.7–2.2 h; cap 2.5 h** | **Yes** | 1–1.5 h: a telemetry logger (WSL load, Windows CPU %, Windows `% Processor Performance` counter, free memory, every 10 s, to JSONL). Read-only counters; **no settings changed**. | — | The cause may stay unknown. That is acceptable: the paper reports a range and a threat, not a cause. |
| (e) Mining rule v2 | ≈ 0 | No | 1 h: a labelling sheet and a precision script | **4–6 h**: label ≈ 150–200 commit subjects from the (a) candidates plus the 4 already-mined projects. A **second rater** labels a 20 % subset (Cohen's κ). | **Overfitting**: a v2 rule tuned on the 70 already-audited subjects. Mitigation: tune on those, and report v2 precision on a **held-out** labelled sample only. |

**Parallelism rule.** A timing window is exclusive. While (b), (c) or (d) runs, nothing else uses CPU on the host: no profiling, no builds or tests, no video render, no harness unit tests. Other Claude sessions are paused or doing text-only work. Profiling for (a), cloning, (e), writing and figure scripts can run together outside timing windows. **Effective capacity is one timing night (≈ 5–6 h) per night**, plus daytime non-timing work.

**Total for the paper (inferred):**
- Timing (idle-exclusive): ≈ 5–11 h, over 2–3 nights.
- Non-timing machine: ≈ 6–17 h.
- Engineering: ≈ 17–25 h.
- Owner labelling: 4–6 h.
- Writing: ≈ 40–60 h.

---

## 2. Schedule

### 2.1 Tonight, 22 Nov (15:30 → ~22:00): preparation only, no timing

| Window | Who | What |
|---|---|---|
| Now–19:00 | W3 | Write and freeze, **before measuring**: `aa_sigma_flagged.plan.md` for (b) (case list, the verdict protocol per case, 5 repeats, ABBA, the 1 + 3σ rule as pre-registered, the deviation note that σ comes from S0 while the verdicts were at S1–S11); `drift.plan.md` for (d); the bottleneck pass plan for (c). Build the telemetry logger. Add a **per-run gate** (postpone, not just label) to every driver. Unit tests. |
| Now–19:00 | W3 + owner | (e) Labelling sheet: a seeded random sample of mined subjects per project, with columns `is_optimization` (yes / no / unclear) and a reason. Owner starts labelling; the second rater is named. |
| Now–21:00 | W6-PAPER (new) | Paper skeleton (§5): folder, template, and figure scripts for **existing** results only. Text-only and light CPU. |
| By 21:00 | W5, W1 | The v11 video render and the novelty searches finish or stop. The render is the largest host-load risk to tonight's gate. |
| 21:00–21:45 | PM | **Data safety first** (R-2 below): commit the current results (owner approval) and back up raw data off the WSL disk. Pause all architect sessions except W3. Arm the detached watcher. Update `RESUME.md` with the queue and the resume commands. |

### 2.2 Overnight 22 → 23 Nov: one gated, checkpointed, detached queue

Gate: WSL load ≤ 1.0 and Windows CPU ≤ 20 % for 3 × 60 s, **re-checked before every run**. If the gate fails it postpones (up to 10 min, then labels the run noisy). Telemetry runs throughout. Per-run checkpoints. A detached watcher with a stall guard writes markers. Hard stop **06:30**.

| # | Item | Cap | Feeds |
|---|---|---|---|
| 1 | (b) σ A/A, 12 flagged cases, 5 repeats, ABBA | 2 h | Applies the pre-registered 1 + 3σ floor to #1, #2, #8 and #9 (closes deviation N8 for the flagged verdicts) |
| 2 | (d) 3 FULL passes at S0 + canary between passes, with telemetry | 2.5 h | R1 as a median of n ≥ 9 passes (6 old + 3 new); R4/N7 drift, with machine-state covariates |
| 3 | (c) Bottleneck FULL benchmark pass at `f51ed86` × 2 | 40 min | R1 second-project row (C extension) |

Expected total ≈ 2–4.5 h after the gate opens; the caps sum to 5.2 h.
- **Morning of 23 Nov:** W3 writes up and runs a critic pass.
- **The meeting pack is frozen** (W4 13:31, critic-clean). Overnight results go into `results.md` as new, dated sections for the paper. At most a one-line addendum goes to the pack, and only if critic-checked before the meeting.

### 2.3 After the meeting

| Dates (2026) | Experiments | Paper |
|---|---|---|
| 23–24 Nov | Meeting. No new timing on meeting day. | Fold the advisor's feedback into the thesis and outline |
| 25–27 Nov | (e) finished, κ computed, rule v2 frozen. (a) pre-registration frozen: candidate projects in order, selection criteria including an asv suite present **at the window base**, a suite-size bound, the mining rule v2, the measure (measured profile at each edit's parent, or at window base plus checkpoints, decided in the pre-registration), the attrition rule, and the analysis (per project and pooled Wilson CIs). Grouped profile runner built and **validated on networkx S0 against the existing profiles** (it must reproduce 171/171 reach sets). | §1–3 (intro, background, design) drafted from W1/W2/readiness |
| 28 Nov – 6 Dec | (a) runs: project setup by day, profiling at night or by day outside timing windows. (c) new-project timing on 1–2 nights. | Figures generated from raw data as each result lands |
| 7–12 Dec | Analysis, critic passes, advisor-persona review of all results | §4–7 (results, threats, related work, discussion) |
| **15 Dec** | — | **Full first draft to the advisor** |
| 16 Dec – ~15 Jan 2027 | Only gaps the advisor asks for | Revision. Buffer for exams and holidays (owner's course load: unknown, likely) |

### 2.4 Venue and submission (not verified: no CFP was checked; every date below must be confirmed by W1 or the PM)

- **Fit:** an empirical software-engineering or performance-engineering venue. The typical cycles below are from general knowledge and are **unknown for 2027**:
  - ICSME and ESEM research tracks: deadlines usually around March–May;
  - ASE: usually around May;
  - ICPE: research deadline usually in the autumn, so likely missed for 2027; a short or work-in-progress track may be later;
  - ICSE 2027 co-located workshops: deadlines usually around January (a short version for early feedback);
  - Journal with rolling submission: EMSE, JSS or IST (fallback with no deadline).
- **Recommendation:** submit to the **first verified research-track deadline on or after ~1 Feb 2027** (≥ 6 weeks after the draft), realistically **March–May 2027**. Optionally, submit a 4-page workshop version in January if a CFP fits. An arXiv preprint is the owner's and advisor's decision.

---

## 3. Top risks and mitigations

| # | Risk | Likelihood / impact | Mitigation | Residual |
|---|---|---|---|---|
| R-1 | **Machine drift** (≈ 1.7–3× within a protocol; cause unknown) | High / medium | Headline **deterministic** metrics (counts, reach, tests and benchmarks selected, per-case cost weights from one pass). Report wall time only as a **range over n passes**, never a single pass. ABBA interleaving for every verdict. Telemetry covariates. Do not chase the cause beyond (d). | Cost figures stay ranges. Say so in the threats section. |
| R-2 | **Lost data** (the first A/A lost everything; commit `326b399` is not pushed; 407 MB of depmaps exist only on disk; the raw data sit on one WSL ext4 disk) | Medium / **high** | Per-run checkpoints and detached watchers (in place). **New:** a nightly backup of `~/bt-lab/exp/**/raw` and the repo's raw folder to a second location (an external drive or the owner's cloud folder; owner's choice), checked by sha256. Push the branch to a private remote (owner decision). Commit after every critic-clean write-up. | Low once the backups run |
| R-3 | **Contamination from concurrent sessions** (the gate checks only at the start; W5 renders; W1 fetches) | High / high | The PM pauses sessions during timing windows (a written rule; **WIP ≤ 3**, §5). Per-run gate that postpones. Telemetry over the whole run. Label noisy if peak load > 1.5 or Windows CPU > 20 %. Re-run noisy runs only if budget allows, never silently drop them. | Medium: host load is still only sampled |
| R-4 | **Mining precision** (3/18 networkx replayed edits are not optimizations; pvlib ≈ 4/14) | Certain on v1 / high for (a) | (e): manual labels, a second rater on 20 % with κ, rule v2 frozen **before** mining any new project. Report v1 and v2 precision on held-out labels. Every count in the paper is computed on **manually confirmed optimizations**, with the regex only as the candidate filter. | Low |
| R-5 | **Single-laptop generality** | Certain / medium | Make the main claims machine-independent (B1 counts, reach, selection counts, mutant detection). Give the hardware spec, OS, WSL and Python versions. State timing as "on this machine". Optional: repeat (d) on a second machine, if the owner can get one (a cost and access decision, not assumed). | Stated as threat T-ext |
| R-6 | **Overclaiming novelty** | High / **high** (desk-reject risk) | W1's targeted novelty search must be recorded **before** any "first" or "gap" sentence. Likely related work on benchmark coverage and selection (to be verified by W1; titles from memory): Laaber & Leitner (MSR 2018) on microbenchmark suites; Leitner & Bezemer (ICPE 2017) on performance testing practice; Huang et al. (ICSE 2014) performance-risk test prioritisation; PerfRanker (ISSTA 2017); de Oliveira et al. on predicting performance regressions. Frame B1 as **"measured for optimization edits in Python"**, not "first". | Medium until W1 reports |
| R-7 | **Environment rot / attrition in (a)** | High / medium | Pre-registered attrition rule. Minimum 3 valid projects; report all attempted. Window bases where the asv suite exists (the pvlib lesson). Cap set-up at 4 h per project, then move to the next candidate in the frozen order. | Medium |
| R-8 | **Numbers drift between results.md, the KB, the pack and the paper** (has happened repeatedly: 40–180×, 19×, 10×) | High / medium | The paper takes every number from a generated macro file built from raw files (§5). No hand-typed numbers in `.tex`. | Low |
| R-9 | **Pre-registration contamination** (geopandas, pvlib and bottleneck were already looked at in Q3) | Certain / low–medium | Disclose. Treat them as "seen" projects, report them separately from "unseen" ones, and use the measured-profile measure, which differs from Q3's. | Low |
| R-10 | **Owner time** (course load; labelling; second rater) | Medium / high for the 15 Dec date | Labelling is the only owner-heavy task; do it first. The schedule has buffer to 20 Dec. | Medium |

---

## 4. Must-not-claim list for the paper

Builds on Review 1's list, updated to the current evidence.

1. **B1 generalises.** Not until (a) succeeds. Do not say "most" optimization edits are unbenchmarked. networkx is 9/15 true optimizations (60 %, CI 36–80 %), one project, one base profile.
2. **The Q3 static counts as replication** (geopandas 18/20, pvlib 14/14, bottleneck 4/8 or 0/8). They are a pilot that motivated (a), not evidence.
3. **Reduced selection is regression-safe**, or "0 of 50 slower" (withdrawn, no power), or P5 as safety evidence. P5 is a profile-completeness check with one unconfirmed flag (#9).
4. **A regression verdict that passes the 1 + 3σ floor**, until (b) has been run for that case. Until then, report the asv-rule verdict plus the deviation.
5. **A4 (our policy) beats testmon, batching or anything else.** N1, N4 and N5 are honest negatives. No accumulation benefit (N4 null). A4 behaves like periodic full checks at k ≈ 4.
6. **Wall-clock speed-ups or cost ratios from a single pass**, or as point values. R1 is 8–28×, with ≈ 8× at the median, and is "setup-dominated". The setup-cached ≈ 1.5–2× is an **estimate**.
7. **"10×" drift**, or any stated cause of the drift.
8. **Build savings for pure Python.** networkx build is ≈ 0.15 % of a pass. Bottleneck is ≈ 16–18 % of build + tests, noisy, 8 edits.
9. **H1 (stale-binary false pass) as a natural-edit hazard.** It is a replay artefact and a harness lesson. Do not call `iterators.h` an open upstream bug, and do not use B4 (invalid as specified).
10. **testmon "15–35×".** It is 3.5–4× end-to-end, under mixed load. Do not present the worked edit (≈ 6×) as a session result.
11. **"Iterative session" or accumulation effects** from replaying non-adjacent historical commits (T1). Use "replayed edit sequence".
12. **"Optimization commits" for regex hits.** Only manually confirmed optimizations count (R-4).
13. **Measured profiles as complete reach.** C7 shows 2.4 % nondeterministic attribution; profiles come from one state (S0) unless (a) measures per parent.
14. **Generality beyond the projects, Python versions, WSL and one laptop.**
15. **Any "first", "novel" or "gap"** without W1's recorded search (R-6).
16. **Anything about AI or LLM-based selection.** It is out of scope (Charter rule 2). LLM tools that helped write must be disclosed per the venue's policy (owner's call).

---

## 5. Workstream setup

**WIP limit: at most 3 active architect workstreams.** Support subagents (TPM, advisor persona, critics) do not count.

| Slot | Workstream | Owner | Scope | Status |
|---|---|---|---|---|
| 1 | **W3-EXP (phase 2)** | The **W3 architect**, restarted in a fresh chat from a hand-off file (`RESUME.md` + the KB). It keeps the harness knowledge, and the fresh chat avoids the context exhaustion of the current one. Sonnet implementer plus a critic. | (b), (c), (d) tonight; then (e) tooling and (a). Sole user of the machine's timing windows. Writes only in `03-experiment/`. | Active |
| 2 | **W6-PAPER** (new) | New architect, with a Sonnet implementer for figure and number scripts and a critic subagent | The paper | Active from tonight |
| 3 | **W1-LIT** | Existing | Novelty search, then the related-work section and `refs.bib` | Active until its search is recorded, then it hands related work to W6 and closes |
| — | W4 (pack), W5 (video) | — | Frozen after v11 and the meeting | **Closed**, so the WIP limit holds |

**W6-PAPER set-up**

- **Location:** `research-directions/build-test-reduction/04-paper/` (own folder; Rule 4).
  - `main.tex`
  - `sections/*.tex`
  - `refs.bib`
  - `figures/` (generated only, never edited by hand)
  - `generated/numbers.tex` (macros)
  - `scripts/make_figures.py`, `scripts/make_numbers.py`
  - `data-manifest.yaml`: every input path plus its sha256
  - `build.ps1` or a `Makefile`
  - `README.md` with the reproduce command
- **Format: LaTeX.** The target venues use IEEE or ACM LaTeX templates, and converting from Markdown later costs time and breaks numbers and cross-references. Pick the template class after the venue is chosen (IEEEtran or acmart). Switching between the two is cheap if the text stays in plain sections.
- **Toolchain:** **no LaTeX or pandoc was found on the Windows PATH** (checked 2026-11-22 ≈ 15:20 PKT, Windows PATH only: `pdflatex`, `latexmk`, `pandoc`, `tectonic`). WSL is not checked (unknown). The options all need the owner's approval, because each downloads software or uploads text:
  1. TeX Live in WSL via apt (the owner runs one sudo command);
  2. Tectonic (a single binary download);
  3. Overleaf (uploads the draft to a third party).
  
  Until then W6 writes `.tex` that compiles once a toolchain exists. Recommendation: option 1, which matches the earlier apt-first ranking.
- **Figures and numbers from raw data:**
  - The scripts read only the paths in `data-manifest.yaml` (raw JSON/JSONL/CSV under `03-experiment/results/`) and check each sha256 before use.
  - Every number in the text is a `\newcommand` macro in `generated/numbers.tex`, with a comment naming its raw file and computation.
  - A CI-style check (`make check`) fails if any digit sequence in `sections/*.tex` is not a macro, apart from an allow-list (years, section numbers).
  - Plots use matplotlib with a fixed style and a colour-blind-safe palette, and are written as vector PDF.
  - W6 does not compute anything new; analysis stays in W3. W6 only reformats W3's outputs.
- **Reviews:** a critic pass per section; an advisor-persona review at the outline stage (by 26 Nov) and the full draft (by 12 Dec); a TPM check of threats and the must-not-claim list on the full draft.
- **Experiments: W3 only.** No other workstream runs anything that uses CPU during a timing window. The PM holds the timing-window calendar.

---

## 6. Decisions needed from the PM or owner (tonight, before 21:45)

1. **Approve the overnight queue** (§2.2): (b), then (d), then (c-bottleneck), with a hard stop at 06:30.
2. **Back up data and push the branch** (R-2): name the backup target; push to a private remote, yes or no.
3. **Pause sessions:** W5 render done or stopped by 21:00; W1 paused during timing.
4. **Start W6-PAPER** and close W4/W5 (WIP limit).
5. **LaTeX toolchain:** apt in WSL, Tectonic, or Overleaf (can wait until 25 Nov).
6. **Second rater** for (e); the advisor or a labmate (owner).
7. **Venue:** after W1 or the PM verifies the 2027 CFPs.
