# Critic log, GROUP B (2026-11-21)

Notes: codeflash, perfagent, semopt, sysllmatic, formulacode. Verdicts: OK / WRONG / LINE-OFF / UNSUPPORTED. Sources re-opened: codeflash @ a3a38ef (verified HEAD), sysllmatic @ fd59fa4 (HEAD verified, working tree empty so read via `git show HEAD:`), fc-eval @ c08f665, datasmith @ b4874d3 (HEADs verified); papers as full PDF text (arXiv 2607.19653, 2506.01249, 2603.16011; local SemOpt PDF).

## codeflash.md (9 fixes)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Code "restored to the original after every candidate" (`finally` 1409-1412) | WRONG | 1409-1412 is a `finally` after the whole `while` candidate loop (1384-1405). Per candidate the file is rewritten with the un-instrumented candidate (3010-3013, 3052-3057); next candidate is applied in place over it (`replace_function_definitions_in_module`, python/function_optimizer.py 198-219) | Rewrote bullet |
| "commercial open-source", BSL-1.1 | WRONG wording | LICENSE: "is not an Open Source license"; README 84 | "source-available" |
| Test discovery = ast import filter + Jedi | OK, incomplete | `discover_tests_pytest` 711-765 runs a pytest collection pass first | Added |
| Count gate labelled "baseline-side" | LINE-OFF/WRONG label | `quantity_of_tests_critic` is applied to the candidate at 1237 and baseline at 1968-1969 | Fixed label and lines |
| Equivalence: pass/fail, return value, stdout, timeouts | OK (30-149) | verified 86-103, 105-119, 132-144, 59-61, 147-148 | Added: missing/one-sided invocations are skipped (48-58), empty results not equal (34-35) |
| Base-class hook pass/fail only; Go/JS too | OK; added that only the Python override compares values | 580-588, 188-196 | Added |
| Perf defaults 5/250 "3115-3116, 3159" | LINE-OFF | 3159 is the JS call (`target_duration_seconds`); Python loop args 1185-1193 | Fixed |
| `gc.disable()` at wrapper line 84 | LINE-OFF | 84 is the async wrapper; sync at 150, 187 | Fixed |
| Accepted edit reverted in `--all`/PR mode | OK but incomplete | 2709-2725: revert only if `raise_pr` and (all / PR number / replay / file-without-function) or staging review; worktree returns early; single-function case has no revert here | Clarified, [inf] for last case |
| Candidate counts 3/5/6 + 4/6/7; repairs 2/3/5; generated tests 2; thresholds 0.05/0.15/doubling in CI; coverage 60; min tests 6; stability 35%/0.25%; hash seed; seeds; min over loops summed; speedup (o-n)/n; 10 s loop; behaviour 1 loop; only passed tests count; no pinning grep | OK | config_consts 15-32, 75-97; critic.py 27-34, 94-104, 192-210; models.py 989-999; pytest_plugin 312-345, 164-187; function_optimizer 3256-3270; support.py 1086-1107, 1185-1193 | none |
| Not re-opened | unverified | refinement/ranking 1022-1101 (only header read), 2540-2630, replay_test.py internals, codeflash_capture | left as [src] by researcher, not re-checked |

## perfagent.md (10 fixes)
Paper read as full PDF text (the HTML fetch was truncated for the researcher; Appendix B exists and is now read).
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Selection by pytest-testmon, 66-99% GSO, 47-98% SWE-fficiency-Lite | OK | §III-D | kept, labelled "authors' figures"; Tables X/XI per-repo counts added |
| Per-patch selection stated only as [inf] | UNSUPPORTED -> now [src] | §III-D "after each iteration"; App. B: "selecting tests based on the specific changes made by the agent" | Upgraded to [src] |
| Testmon DB build / fallback "in supplemental Section B, not read" | WRONG pointer | Appendix B is only about filtering flaky/failing base tests (5 runs, random seed + order) and Tables X/XI; it does not describe the testmon DB, seeding or fallback | Documented App. B; kept DB/fallback/cost as [unk] (searched whole paper for "testmon") |
| Paper says "without missing any correctness regressions" | New | §III-D vs §VI (testmon only Python coverage) | Added contradiction |
| Build exits early on build failure | Incomplete | §III-A: build OR any test failure exits outer phase early (no profile) | Fixed |
| Timing "first run only", "<3% variance", averaged variant rejected | OK | §IV-E4 ("only times the execution time of the first run"; "< 3% of overall runtime on average") | Added: 18 -> 3 hacks was SWE-fficiency-Lite loop-only ablation; <3% is unsupported by shown data |
| Timing repeats/statistic, pinning | [unk] confirmed | no hit for median/noise/repeat in measurement context; only instance types (c6i.8xlarge agent, m8i.16xlarge eval) | Added hardware |
| $5/task, 200 steps, 5 iterations, $2.88/$4.25, $11.01/$9.91, $10 -> 75->79 | OK | §IV-A, Table VI, §IV-E5 | none |
| Best-patch selection, Turn 4 5.87x over Turn 5 5.85x | OK | §III-A, Fig. 3 | none |
| Final selected patch not re-run on full suite | still [inf]; consistent with §VI | | none |
| Sec. numbering "IV-E4/E5" | OK | headings "4) Reward Hacking", "5) Ablation ... Budget" | none |
| Open question: "py-spy fixed 10 s window" | OK | §III-B | none |

## semopt.md (5 fixes)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Test pass 72.43% / 100% Python cited to Sec. 4.3.6 | WRONG cite | 4.3.6 is the manual 89.86% applicability check; rates are Sec. 5.3 Table 16 (and 6.2) | Fixed; added 9,483 Python candidates all pass |
| Missing: authors manually validated final optimizations equivalent | UNSUPPORTED omission | Sec. 5.3 "Semantic Correctness Validation"; Sec. 6.2 human review still needed | Added |
| Sec. 7: iterative methods "(PerfCodeGen, EffiCoder)" orthogonal | WRONG wording | text names SBLLM, EffiCoder, PerfCodeGen; EffiCoder is profiling-guided | Fixed |
| Build/compile/unit tests/6 runs, discard first, 5% / 2% rule, hotspot >0.1%, perf/gcov, cProfile, Xeon 8270 | OK | Sec. 5.1.1-5.2.3 lines read | none |
| 73.72% compile, 72.43% test, 8,082 candidates | OK | Table 16 text of Sec. 5.3 | none |
| Limitations 6.4/6.5, 1.56%/82.78% | OK | Sec. 6.4, 6.5, 4.8 table | none |
| No per-edit test selection; "reads as whole suite" | still [inf]; paper says only "built-in unit and performance tests" | 5.1.1-5.1.2 | wording softened |
| Final assembled version re-tested | [unk] confirmed | 5.2.2 only says assemble; 5.3 reports after-assembly Table 15 without stating a re-run | none |
Page numbers not independently re-verified (approximate).

## sysllmatic.md (12 fixes) — rewritten from repo + paper
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| "Fixed per benchmark; not selected per edit [inf]" | WRONG detail | Tests are chosen per target class by textual name match: `find_unit_test` (flamegraph_profiling.py 175-199); `run_tests` loops `self.unit_tests` (dacapo_benchmark.py 138-167) | Now [src]: per class, not per edit |
| Perf workload / protocol | UNSUPPORTED | per-candidate measure is `make measure TEST=<unit_tests[0]>` (dacapo_benchmark.py 189-203), the first unit test of the class, 120 s timeout; MEASURE/main.c has WARMUP_RUNS 10, ntimes 20 and a hard-coded /home/hpeng path, not the paper's 2+5 | Added; DaCapo make targets [unk]: `bms/makefile_template.mak` (read at dacapo_benchmark.py 303) is not in the repo |
| ">=10% counts as optimized" as threshold | MISLEADING | paper §6.3: reporting metric. Code has no performance gate: `static_analysis` returns success statuses whenever compile + tests pass (benchmark.py 80-89; main.py 219-234) | Fixed; added |
| "accepted candidates accumulate; final app rebuilt and re-measured [Alg.1 l.14-23]" | LINE-OFF + code gap | Algorithm 1 has 21 lines; final build/measure is lines 19-21. In the artifact, `run_app_and_measure` is imported (dacapo_benchmark.py 13) but never called; `main()` ends after `master_script` | Fixed; marked [unk] how final numbers were produced; accumulation OK (main.py 233, in-place writes) |
| Iteration budget T=2 | OK | paper §6.4.1; main.py 29, 238 (2 successful iterations per class) | clarified unit is per class |
| Build: "Maven-built, prebuilt per README" | PARTLY | README says prebuild per DaCapo instructions; code runs `ant <app>` under Java 8 (dacapo_apps.py 227-261); paper says Maven apps | Fixed; compile internals [unk] |
| 2 warm-up + 5 measured, bare-metal Xeon | OK for paper (§6.4.1, §6.7: Xeon W-2295) | | cited |
| Passing-but-wrong cases cited to §5.6.3/Table 3/threats | WRONG cites | §7.1.4 (1/145 HumanEval core function removed; PMD 2/601 files mismatch); §8.2.1 (races) | Fixed |
| Cost [unk] | WRONG | paper §7.5.1 Table 12 gives end-to-end time (11-206 min) incl. build and tests | Added |
| "§3.2 controlled pipeline" "§6.2.2 5/22 apps" | OK | | none |
| Table 3: GraphChi ~10%, avg 59.4% | OK; ZXing: text says "nearly 94%", caption 90% | | noted |
| Class-level adoption | new, §7.4.3 | | added |
Not read: humaneval/scimark benchmark internals, llm/*.py, eval scripts.

## formulacode.md (10 fixes)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| "A.5 pytest check implies full suite" [inf] for harness correctness | WRONG | harness pytest step runs only tests mapped from changed files by name heuristic; no `--all`/`--fallback` => 0 tests, exit 5 (run-tests.sh 146; pytest_runner.py 39-87, 107-184, 363-427, 485-540). A.5's pytest check is env validation only | Rewrote §3 |
| ASV Mann-Whitney / Holm listed as per-candidate performance measurement | WRONG context | paper A.6: used for dataset inclusion on the EXPERT patch; harness advantage uses medians, `use_stats`/`factor` "Unused" (parser.py 985-1032, 1059-1076); `is_different` only in classification (704-727) | Fixed |
| Holm-Bonferroni "incorporated in codebase" | UNSUPPORTED | grep of datasmith for holm/bonferroni/multipletests found nothing | marked [unk] |
| "No pinning/instruction counting: [unk] (B.1 not read)" | OK, resolved | B.1: asv safeguards (CPU affinity, warm-ups, repeated trials); B.5: EC2 c5ad.large; sequential nop/oracle/agent runs | Added |
| ASV protocol numbers | OK + more | fc-eval profile.sh 110-121: rounds=4, repeat=0, num_cpu 1; datasmith profile.sh uses rounds=1 (115); paper 2-40 samples | Added |
| Per-edit rebuild "not described" | CONFIRMED + sharpened | run-tests.sh never rebuilds; ASV uses `environment_type: existing`, `--python=same` | Added |
| Failing workload speedup = 1 (§2.1) | OK in paper; App. B.7 says whole final patch is rolled back (Table 16, 47-56/108 rejected); parser has no such gate | | Added; where applied [unk] |
| Snapshot tests "return values" | OK §3.1; App. B.7 says "local variables" | | both noted |
| $446, 1232/3181, nearest-neighbour script reuse | OK | A.5 | expanded |
| Agent cost/time | [unk] -> found | Table 12: 6 h cap, avg 38 min; sample task.yaml says 3000 s | Added |
| Limitations | OK | A.9 | named |
Not read: datasmith synthesizer, `asv_discover_and_cover.py`, external snapshot-tester.
