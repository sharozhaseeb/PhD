# W2-PRACTICE: practice survey (RQ1)

**Status: draft 2026-11-21.** All 28 per-system notes are critic-checked (critic logs A–E), and findings/table/README had a final critic pass (`critic-log-final.md`). Nothing is committed (the PM integrates).

RQ1: how do real code-optimization systems and benchmarks build the code and confirm correctness and speed-up for each candidate edit? This covers what they rebuild, which tests and benchmarks they run, what it costs, and whether accepted edits are re-validated together.

## At a glance: how iterative optimizers validate each candidate edit

Optimizers first; two benchmark harnesses as **full-check reference rows**. "Work per candidate" = builds/installs × correctness tests × timed runs, counted only from code or paper text we read. Anything else is [unk]. Citations are in the linked notes and in [survey-table.md](survey-table.md).

| System | Work per candidate (builds × tests × timed runs) | How tests are chosen | Speed-up rule | Re-checks accepted edits together? |
|---|---|---|---|---|
| [SemOpt](per-system/semopt.md) | **1** compile/install × project unit suite (whole suite, size [unk]; selection not described [inf]) × **6** runs of the project perf tests (2–45 C/C++, 4–11 Python), first run dropped; original also run 6×, but per-candidate re-measure of the original [unk] [src §5.1.1–5.1.2] | Whole suite, no selection [inf] | Mean of 5 runs; >5% on one perf test, ≤2% loss elsewhere; no stat test [src §5.2.2] | Best variant per function assembled [src]; re-measured [inf]; combined unit-test re-run [unk] |
| [PerfAgent](per-system/perfagent.md) | **1** `/build.sh` (incremental? [unk]) × **testmon-selected** tests × **1** timed run (first run only) + a 10 s py-spy profile [src §III-A–D, IV-E4] | **Per edit**, Python coverage (pytest-testmon) [src §III-D] | Benchmark rules (Opt@1 ≥0.95× expert; Sp@1 ≥1.2×) [src §IV-A] | Best of ≤5 patches kept; no full-suite re-run inside PerfAgent [inf] |
| [Codeflash](per-system/codeflash.md) | **0** builds × discovered + generated tests (1 behaviour pass) × **5–250** loops in a ≤10 s perf pass [src] | Per target function (Jedi call resolution), fixed across its candidates [src] | Min over loops, summed over tests; gain >5% (15% if <10 µs; ×2 in CI); no stat test [src] | No combined re-run across functions found [src]/[inf] |
| [SysLLMatic](per-system/sysllmatic.md) | **1** module `make compile` × class-matched test files (stop at first failure) × **1** `make measure` on the first unit test (paper: 2 warm-up + 5 runs; code's measure step [unk]) [src] | Per target class, by name match [src] | None in code; ≥10% is a reporting metric only [src] | Paper: final rebuild + re-measure; not in the artifact code [src] |
| [OpenEvolve](per-system/openevolve.md) | **0** builds × user evaluator × user-defined; optional 3-stage cascade, 300 s timeout, ≤3 retries [src] | User-defined [src] | User-defined score [src] | None in framework [src] |
| *Reference:* [GSO](per-system/gso.md) | **2** full installs (patch, then reference commit) × **0** unit tests (output-equivalence checks inside the perf scripts) × ≤20 perf scripts × **5** runs (1 for 3 repos) × **3** phases (base, patch, reference): ≤300 timed process runs [src] | Fixed per task (LLM-written perf scripts) [src] | ≥~1.1× gm over base, then hm ratio vs reference >0.95; no stat test [src] | — (one patch per task) |
| *Reference:* [SWE-fficiency](per-system/swe-fficiency.md) | **5** installs × **covering tests** once (median 7,723; up to 2 retries on error) × **4** perf.sh runs (2 warm-up), each workload typically `timeit` repeat=10 [src] | Fixed per task, from coverage of the **expert** diff [src] | Ratio vs gold, harmonic mean; no stat test; pinned cores [src] | — (one patch per task) |

Reading: the optimizers pay **one build per edit** (except pure-Python Codeflash). Only PerfAgent cuts tests per edit, and none re-checks accepted edits together in its code. The harnesses re-install and time far more per patch, which is the price of isolating each submission. "Install = full build cost" is our inference [inf]; no system reports build seconds.

## Files

| File | What |
|---|---|
| [findings.md](findings.md) | Cross-system patterns F1–F7, what nobody does (with the search record), and consequences for W3 |
| [survey-table.md](survey-table.md) | Full table split into optimizers (A1), benchmark harnesses (A2), classical/industrial practice (B) and late additions (C): one row per system, with every cell cited and labelled, plus a yes/no quick-compare table and the discrepancies |
| [per-system/](per-system/) | 28 system notes, all critic-checked, plus `_TEMPLATE.md` and `_discovery-log.md` (queries and kept/dropped candidates) |
| [sources.json](sources.json) | Repo URLs + commits, papers, docs, and the systems with no public code |
| critic-log-A…E.md, critic-log-final.md | The fresh critics' claim-by-claim verdicts (OK / WRONG / LINE-OFF / UNSUPPORTED) and fixes |

## Systems covered

- **Repo-level benchmarks:** SWE-bench harness (classic v4.1.0 + HEAD), SWE-Perf, GSO, SWE-fficiency, FormulaCode.
- **Function/program benchmarks:** PIE, ECCO, EffiBench, EffiBench-X, Mercury, EvalPerf, COFFE, KernelBench.
- **Iterative optimizers:** Codeflash, PerfAgent, SemOpt, SysLLMatic, OpenEvolve; paper-level only: AlphaEvolve, Google ECO.
- **Classical practice:** asv in numpy/scipy/pandas CI, pyperformance/pyperf, CodSpeed.
- **Industrial CI (paper-level):** Meta Predictive Test Selection, Google TAP, Bazel affected targets.
- **Late search (critic-checked, paper-level plus repo where public):** performance-benchmark reliability audit (arXiv 2607.01211), PERFOPT-Bench (artifact expired), SWE-Opt, CodeEvolve (no public code).
- **No public code:** PerfAgent (none found: searched arXiv links, web, GitHub); SemOpt (private-share figshare link, not opened); ECO, AlphaEvolve, Meta PTS and TAP (internal). These are covered from their papers.

## Evidence boundary

- **Code.** Shallow clones live in `C:\Users\pc\study\bt-lab\survey\`, outside this repo, at the commits in `sources.json`.
  - They were read only and never executed. Nothing was built or run, so every behaviour claim is from reading the code, not from observing it.
  - Per-instance data held only in Hugging Face datasets was **not** downloaded. Examples: GSO `install_commands`, SWE-bench HEAD `eval.sh`, Mercury/EvalPerf test counts. Those claims are [unk].
- **Papers** were read as arXiv HTML or PDF text.
  - Some reads went through a summarising fetch tool, and each note says where.
  - The SWE-bench paper could not be re-read by the critic (PDF fetch timeouts). Its paper-only claims are marked unverified.
  - ECO section numbers follow arXiv v1, because v2 (Sep 2026) is renumbered.
- **Labels:** [src] read in source, [inf] our inference, [unk] not found (the note says where we looked).
- **Novelty.** "Nobody does X" statements hold only for this sample and the searches recorded in `per-system/_discovery-log.md` and `findings.md`. W1 owns the methods literature and may find precedents.
- **Precedence.** Where a paper and its code disagree, the notes report both. findings.md prefers the code for "what the harness does".

## Headline (details and citations in findings.md)

1. No surveyed optimizer decides by rule what to rebuild for an edit; those with native code rebuild once per candidate (SemOpt, PerfAgent, SysLLMatic). Harnesses re-install per patch for isolation (SWE-fficiency 5×). That this equals full build cost is inferred.
2. Test subsets are common but fixed per task, chosen from the expert diff at curation. Among optimization systems only PerfAgent (testmon, no public code found) selects per edit; FormulaCode does a filename-mapped selection once at the end.
3. Benchmark subsets are picked by people or agents (asv `-b`, FormulaCode's prompt). No deterministic diff-to-benchmark rule was found.
4. Speed-up rules disagree: Mann-Whitney (SWE-Perf p<0.1, asv p<0.002), thresholds only (GSO, Codeflash, SemOpt), or deterministic metrics (gem5, instruction counts).
5. Oracle warning: full benchmark verdicts don't repeat across machines (reference patches pass their own rule in all 12 replays: GSO 39/102, SWE-Perf 11/140), and tests are weak (all 9,483 SemOpt Python candidates pass).
6. Cumulative or periodic full re-validation of accepted optimization edits is essentially absent. Functional CI has precedents (Meta: all tests on master every few hours; Google TAP: batched milestones).
