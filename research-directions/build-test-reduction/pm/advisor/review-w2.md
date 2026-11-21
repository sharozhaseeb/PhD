# Advisor-persona review of the W2 practice survey (draft 2026-11-21)

Reviewed:
- `02-practice-survey/README.md`
- `findings.md` (F1–F8 and "what nobody does")
- `survey-table.md` (Tables A–C, quick-compare, discrepancies)
- the per-system file list

Reviewer: advisor-persona subagent (AI-SIM, not the advisor). I did not re-check citations; the critic logs A–E are taken as given.

## Verdict

**It answers "how do existing optimizers build and verify each candidate" thoroughly and with good evidence discipline.** It covers 28 systems, cites code at the line and commit, and records where papers and code disagree. The SWE-fficiency install conflict and the SysLLMatic missing final rebuild are the kind of detail an advisor respects.

**It is not yet readable in 2 minutes.**
- Table A has 10 dense columns.
- The quick-compare table has 27 rows and treats one-shot benchmark harnesses the same as iterative optimizers.
- The column the advisor cares most about, cost per candidate, is almost entirely `[unk]`.

## Does it answer the question? Can the advisor read the table in 2 minutes?

| Aspect | State |
|---|---|
| What is rebuilt per candidate | Answered (F1) |
| Which tests are run | Answered (F2) |
| Which benchmarks are run | Answered (F3) |
| How speed-up is confirmed | Answered (F4); more than Study 1 needs |
| Cumulative or final re-validation | Answered (F5) |
| **What it costs** | **Not answered.** Only a few aggregate numbers are given (FormulaCode about 38 min per task, EvalPerf about 15 min per model). Seconds per candidate are never reported, which is a finding in itself. But the work units per candidate (installs × tests × timing runs) *can* be counted from the code already read, and they are not. |
| 2-minute readability | No. The quick-compare table is closest, but 27 rows mixing harnesses, CI systems and optimizers buries the point. |

## Findings I would challenge

1. **F1 ("full install per candidate") mixes two populations.**
   - The repository-level harnesses (SWE-bench, SWE-Perf, GSO, SWE-fficiency) score **one final patch** per task in a fresh container. They rebuild for isolation and reproducibility, on purpose; they were never trying to save time.
   - The relevant population for Study 1 is the **iterative optimizers** that validate many edits: SemOpt, PerfAgent, Codeflash, SysLLMatic, OpenEvolve and AlphaEvolve.
   - Expect the advisor to say: "of course a benchmark harness rebuilds; that's not a gap".
   - Re-state F1 for optimizers only, and use the harnesses as context for what a full check costs.
2. **"Re-runs install" does not mean a full rebuild.**
   - `pip install -e .` on an already-built tree may reuse the build directory (setuptools) or rebuild incrementally (meson-python). F1's own bullet says this, labelled [inf].
   - The headline "SWE-fficiency up to 5×" invites the inference that the build cost is five times larger. Label that headline [inf], or measure it in W3.
3. **F3 ("benchmarks are never selected per edit") is overstated.**
   - FormulaCode's prompt tells agents to run `--bench=<regex>` and calls full-suite runs "discouraged"; asv users pick benchmarks with `-b`.
   - So per-edit benchmark selection **does** happen in practice, by human or agent judgment. What is absent is a *deterministic rule derived from the diff*.
   - Narrow the wording to that, and add "ad-hoc human or agent subset" as a practice baseline. The same applies to tests in agent trajectories (PerfAgent aside).
4. **F5 needs care.**
   - The gap "periodic checkpoint across accepted optimization edits" stands only for this sample.
   - W1 shows periodic full runs and batching are not new in functional CI, so frame F5 as "not applied to performance edit sequences, and its catch rate is not measured".
   - SemOpt's assembled final project and FormulaCode's final-tree check are final checks, so "absent" should read "final-only".
5. **F4 (speed-up statistics) is off the Study 1 path.** It belongs to the earlier acceptance-statistics direction. Keep one line in the meeting pack: W3 fixes one rule and adds a deterministic proxy. Otherwise it invites a detour.
6. **F8 is underplayed and is the most useful finding for W3.** Only 11 of 140 SWE-Perf and 39 of 102 GSO reference patches pass their own speed-up rule in all 12 replays. So the "full validation" oracle is unstable. Pair it with F7: SysLLMatic's coverage was about 10%, and in SemOpt all 9,483 Python candidates passed the unit tests (TOSEM Table 16). The ground truth for "missed" must have its repeatability measured before any miss is counted.

## Three changes that matter

1. **Add a one-screen table for iterative optimizers only**, about 6–8 rows:
   - rows: SemOpt, PerfAgent, Codeflash, SysLLMatic, OpenEvolve, plus GSO and SWE-fficiency as "what a full check looks like" and Meta/TAP as the CI reference;
   - columns: build per edit; how tests are chosen; how benchmarks are chosen; final or cumulative check; **work units per candidate** (installs, test count, timing runs, counted from code) and any reported time.
   - Put it at the top of the README.
2. **Narrow F1 and F3**:
   - F1: "no *deterministic diff-derived* reduction among *iterative optimizers*"; label repeated install = full build cost as [inf].
   - F3: name agent- or human-chosen subsets (FormulaCode prompt, asv `-b`) as the existing practice baseline.
3. **Promote F8 and F7 to one "oracle weakness" message for W3**: measure how repeatable the full-validation verdict is, and how strong the tests are, before reporting misses by reduced arms. This also pre-empts the advisor's question P04.
