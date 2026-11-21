# Study 1 charter — Reduced build and test validation for iterative code optimization

Owner: PhD student. PM: main Claude session (orchestrator). Date opened: 2026-11-21. Advisor meeting: ~2026-11-23/24.

## Problem (owner's words, condensed)

When a codebase is optimized through many small successive edits, each edit must be re-validated: build the code, run the tests, confirm the speed-up is real and nothing regressed. A full build plus a full test (and benchmark) run after every small edit makes iterative optimization slow. Study 1 asks how to validate each edit with a **reduced build** and a **reduced test/benchmark set**, chosen by **deterministic rules, without AI**, while still being confident that the optimized codebase is correct and actually optimized. AI-based selection is explicitly a later study; this one sets the deterministic baseline and its limits.

## Research questions — revised 2026-11-21 after advisor-persona and TPM review (supersedes the list below)

Background chapters (not RQs): how optimization systems validate candidates (W2) and what deterministic reduction techniques exist (W1).

- **RQ1 — Cost.** On real projects, what share of per-edit validation time goes to build, tests and benchmarks, and how does it accumulate over a sequence of optimization edits?
- **RQ2 — Existing techniques, unchanged.** Applied to optimization edit sequences, how much end-to-end time do incremental builds, RTS (pytest-testmon, changed-module rule) save including their own overhead, and how many functional failures and performance regressions do they miss, and why?
- **RQ3 — New deterministic policy.** Does a policy using (a) changes accumulated since the last full check, (b) profile/call-graph-based benchmark selection, and (c) a full check triggered by accumulated change, miss fewer failures/regressions than the best existing combination at matched cost? Ablate each part.

Definitions fixed before runs: a *performance regression* is a slowdown beyond a stated threshold relative to the **original** code (and to the previous accepted state), above the measured noise floor; *safe* means k of N frozen injected faults/regressions detected, reported with a CI — never a general guarantee.

## Research questions (original working list, kept for history)

- **RQ1 (practice).** How do existing code-optimization systems and benchmarks (LLM-based and classical) build the code and confirm correctness and speed-up per candidate edit? What do they rebuild, which tests/benchmarks do they run, and what does it cost?
- **RQ2 (methods).** What deterministic techniques exist for reducing build work (incremental builds, build avoidance, caching) and for reducing validation work (regression test selection, performance-test/benchmark selection, change-impact analysis), and which assumptions break when edits are performance-motivated and accumulate across iterations?
- **RQ3 (experiment).** On real Python codebases, replaying real historical optimization edits as an iterative session, how much validation time do deterministic reduced build + selection rules save against full build + full tests + full benchmarks, and how many functional failures or performance regressions do they miss (measured with injected faults/regressions and periodic full checks)?
- **RQ4 (beyond the literature).** What does the iterative-optimization setting allow that classical CI test selection does not use, e.g. accumulated evidence across successive edits, performance-aware selection via profiles/call graphs, and a schedule of periodic full "checkpoint" validations with a final full validation?

## Workstreams

| ID | Owner | Output folder | Goal |
|---|---|---|---|
| W1-LIT | Architect session | `research-directions/build-test-reduction/01-literature/` | Methods literature: reduced/incremental builds; functional RTS; performance test & benchmark selection; change impact; checkpointing. Cited, primary sources. |
| W2-PRACTICE | Architect session | `research-directions/build-test-reduction/02-practice-survey/` | How real optimization codebases/benchmarks build and verify (SWE-Perf, GSO, SWE-fficiency, PIE, SemOpt, PerfAgent, Codeflash, ECCO, EffiBench, asv/codspeed CI practice, …), from their code and papers. |
| W3-EXP | Architect session | `research-directions/build-test-reduction/03-experiment/` | Reproducible experiment harness and first results: full vs reduced build/test/benchmark per edit, cost and safety. |
| W4-REPO | Later (after W1–W3) | repo root + `research-directions/` | Restructure and format the repository; advisor meeting pack. |

Support roles (subagents of the PM): **TPM** (feasibility, risk, cost, validity threats, schedule to the meeting) and **Advisor persona** (the student's PhD advisor, built from existing advisor-review material; reviews every deliverable as the advisor would and predicts the meeting's questions).

## Rules for every workstream

1. **Evidence, not claims.** Every cited fact links a primary source (paper section/page, repository file + commit). Every experimental number comes with the command, raw output file, and commit SHA. Label each claim *read in source*, *inferred*, or *unknown*.
2. **No AI in the method.** Rules for choosing what to build and what to test are deterministic. LLMs may help us read and write, not decide in the experiment.
3. **Honest novelty.** Do not claim a gap unless a targeted search failed to find it; record the search. The prior package's style (status line, evidence boundary) applies.
4. **Own folder only.** Each workstream writes only inside its output folder (plus its branch). External repositories cloned for experiments live outside this repo at `C:\Users\pc\study\bt-lab\` (never committed). No destructive git.
5. **Report to the PM** in ≤5 lines (STATE · DONE · BLOCKER · ASK · NEXT+ETA) with branch + head SHA, via SendMessage to the PM session; detail goes in files.
6. **Deadline.** Usable draft within ~24 h; final within ~40 h, so the PM can integrate before the advisor meeting.
