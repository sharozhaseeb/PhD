# Critic log, GROUP C (2026-11-21)

Notes: pie, ecco, effibench, mercury, evalperf, coffe, kernelbench, effibench-x. Code re-opened in local clones at the commits in each note header (verified with `git rev-parse`). Papers: PIE from the local PDF (pdftotext); ECCO and EffiBench PDFs fetched and read with pdftotext; Mercury, EvalPerf, COFFE, EffiBench-X only via arXiv-HTML summarising fetch (Mercury PDF fetch timed out twice); KernelBench paper not fetched. Verdicts: OK / WRONG / LINE-OFF / UNSUPPORTED / UNVERIFIED (could not open source).

## pie.md (10 fixes)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Image `alexshypula/gem5-skylake:api` at simulator.py:416-440 | LINE-OFF | string is in DOCKERFILE_TEMPLATE, simulator.py:31 | cited l.31 |
| Compile `--std=c++17 -O3`, gem5_api.py:98-99 | OK | l.98-99 | added compile timeout = binary timeout (10 s), l.104,129 |
| Fresh temp dir per candidate, gem5_api.py:112-128 | LINE-OFF | l.112-132 | fixed |
| "Workers pinned to CPUs via queue and taskset" | WRONG | `cpu_number = queue.get(...) if timing_env in ("binary","both") else None` gem5_api.py:117; gem5_eval.py:387 uses "gem5" | now: pinning only for binary/both, gem5-only path unpinned |
| Compile failure => acc 0, benchmarking.py:127-131 | OK | l.127-131 | - |
| Output equality, 1e-3 float tolerance, 10 s timeout | OK (nuance) | get_accuracy l.33-51 divides by ground-truth lines, zip => partial credit per test | added |
| Gate mean acc >= 0.95: gem5_api.py:136-146, simulator.py:429 | LINE-OFF | gate l.135-143; default at gem5_api.py:93 and simulator.py:418 (429 is exit_early_on_fail) | fixed |
| Tests from dataset `tests` column, gem5_eval.py:381-383 | LINE-OFF | l.385 (381-383 are comments); `testcases` subset is a real API parameter | fixed |
| Early exit after first failing test | OK (nuance) | benchmarking.py:229-231,238,245: triggered by gem5 non-zero exit/timeout, not output mismatch | clarified |
| gem5 timeout 120 s | OK (nuance) | gem5_api.py:105, gem5_eval.py:374; PieEnvironment class default is 60 (simulator.py:425) | added |
| agg_stdev hard-coded 0, simulator.py:260 | LINE-OFF | l.271 | fixed |
| sim_ticks/sim_freq; speedup floored at 1.0; thresholds | OK | benchmarking.py:168-169; gem5_eval.py:176-177,192 | - |
| hyperfine prototype, README | OK/LINE-OFF | README.md:59; gem5_api.py:159-173 | fixed lines |
| Paper: 978 pairs/41 problems, median 104 tests, 42.8M sims, hyperfine 1.12x sd 0.36 top5% 1.91x, footnote 2, GCC 9.3.0, best@k temp 0.7 | OK | pdftotext of PDF, lines on pp.3-5 | - |
| Spurious speedups "§5/Appendix" | WRONG section | 10 of 120 in App. A.1 | fixed |
| README.md:77-82 self-play | LINE-OFF (minor) | l.77-81 | fixed |
Not verifiable: per-candidate cost (confirmed absent).

## ecco.md (6 fixes)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| utils.py:29-37 language_id 71, limits 20 s / 512000 KB | OK | l.29-37 | - |
| Tests sequential sorted; `--num_tests` prefix | OK | utils.py:88-92 | - |
| `accept` quirk (status 4 does not set False) | OK | utils.py:109-122 | line detail added |
| Best sample = most passes then min summed time; edit_eval.py:89-95 | LINE-OFF | l.87-105; sum over all tests that executed incl. wrong-answer | fixed |
| Speedup only over passed tests; input must pass all, edit_eval.py:139-151 | OK | l.138-151, `sum(in_time_passed)/sum(out_time_passed)` | - |
| number_of_runs 3 in eval, 1 in loop | OK | edit_eval.py:16; inference.py:215 | - |
| Literal `'args.test_cases_path'` bug | OK | inference.py:215,284 | - |
| Public avg 3.1/3.3, private 17.2/20.0 | LINE-OFF/value | Table 1: 3.14/3.29, 17.21/20.00 (intro says 17.3); splits 1262/69/48 | fixed |
| Eqs. 1-4 all in §3.3.2 | WRONG | eqs 1-2 in §3.3.1; 3-4 in §3.3.2 | fixed |
| Multi-iteration finding in "§5" | WRONG | §6 Additional Analysis | fixed |
| App. C: ~1% CI, memory 5% in NL | OK | Table 9; also "pass@1 no variance (low temperature)", two models only | added |
| Judge0 aggregation of 3 runs | UNVERIFIED | not in repo or paper (kept [unk]) | - |

## effibench.md (7 fixes)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Candidate file composition, calculator.py:9-51,94-97; max_execution_time=5 :66 | OK | l.53,66,94 | added :53 |
| Dockerfile:1-8 | LINE-OFF | l.1-11 | fixed |
| Quirk: exit_status always 0, run_code.sh:29-34 | claim OK, LINE-OFF | `exit_status=$?` l.42 after `execution_time=$(( ... ))` l.41; check l.46; mprof l.39 | cited 39-42,46-48 |
| Failure detection by stderr; .dat removed, run_code.sh:36-43 | LINE-OFF | l.46-48 | fixed |
| pass = has .dat (report_overhead.py) | OK, detail added | pass1 = len(list)/1000*100, l.110-112,143 | added |
| NET = ratio of sums in the script | OK + new divergence | script l.136 ratio of sums; paper §3.4 defines NET as mean of per-problem ratios (l.121-122 computed, unused) | added |
| Paper: 100 tests, Xeon 8336C/128 cores, 10 s, Kruskal-Wallis p>>0.05, 210-problem subset, Appx A.1 limitations | OK | pdftotext l.251,386-392,558,1163 | added Kruskal-Wallis, Table 26 |
| "Table 24 numbers not read" | UNSUPPORTED omission | Table 24: NET 2.36/3.18/3.95 and ET 0.27/0.39/0.56 for 10/100/1000 tests | filled in; softened "stable rankings justify fewer tests" (stability claim is about environments, Table 26) |
| 984/1000 rows with assert, ~100 lines | OK | recomputed from results/gpt-3.5-turbo.json | - |
| ThreadPoolExecutor concurrency | OK | calculator.py:64-67 | - |

## mercury.md (6 fixes; paper not fully re-readable)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| exec in forked process, tempdir, guard, limits | OK | sandbox.py:91-97,113,162-203,252-264 | - |
| Runtime wall-clock around loop, one run | OK | sandbox.py:218-228 | - |
| "Fully serial in-process" | OK for Beyond path; added | evaluator.py:438,459 use run_sample; threaded run_samples (sandbox.py:267) is a stale path with undefined `n_samples` (l.275) and caller kwarg mismatch (evaluator.py:185) | clarified |
| Beyond in code vs Eq. 1 "gap small" | WRONG conclusion | code clips (max-runtime) to [0,1] seconds, not runtime to [min,max]; faster-than-all candidate gives beyond_p > 1 when max-min < 1 s; max==min divides by zero (evaluator.py:461-466); paper Eq. 1 clips to [min,max] (summary) | rewritten |
| K=5 for Beyond | WRONG/incomplete | score uses `cases[0]` only (evaluator.py:481), sampling count from `--samples 5` | fixed |
| Reference solutions all re-executed (~18.4/task) | OK | evaluator.py:428-441 (all `instance['solutions']`) | - |
| Timeout 30 s | OK | evaluator.py:331,436,456; paper App. A.3 | - |
| Section numbers §3.1/§3.3 | UNVERIFIED | summary gives dataset §2, metric §3, K §4.3; tiers App. A.10 | header notes limits of verification |
| Hardware tiers 0.25/0.5/1 CPU consistent Beyond | OK (summary) | Fig. 10 | - |
| Tests per task [unk], Fig. 1 "100 test cases" | OK (summary) | | - |

## evalperf.md (6 fixes)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| exec in forked process, profile.py:85-100; perf_event_open check :31-43 | OK | | - |
| Parallelism formula profile.py:27-28 | OK | | - |
| `untrusted_check` fast_check=True, limit max(4 s, 4x ref) | OK | evalperf.py:76-92; eval/__init__.py:209,237; config.py:2-3 | - |
| PERF_PROFILE_ROUNDS=1, profile.py:183 | OK | config.py:8; profile.py:138,183 | paper "multiple times" with no number (§2.5); App. A.1 5 runs is the variation study |
| Warm-up supported, not used | OK | profile.py:103-106 (3 calls); evalperf.py:189-194,249-254 pass none | - |
| DPS scan and 0 on failure | OK | evalperf.py:257-278 | - |
| "min_correct" semantics, evalperf.py:417-423 | LINE-OFF/incomplete | tasks with n_pass < min_correct skipped (l.438-440); table l.418-428; docstring says all correct evaluated but perf_worker stops at max_profile (l.238) | fixed |
| Cost: "no more than 15 minutes for most", plus assumed 10 solutions x 121 tasks and 0.7 s | UNSUPPORTED | paper §4.2 gives only the 15-minute statement; the rest was our assumption | marked [inf] |
| Noise: 4 test beds, max CV 0.4% | OK | §4.2 Table 2 (summary): i7-10700K, i9-12900K, TR Pro 5975WX, Xeon 6442Y | section fixed (§4.2, not §3) |
| 121 vs 118 tasks | OK | paper 121, docs 118 | - |
| Limitations "not located" | refined | no section; DPS needs diverse references §2.5, counters/platform variance App. A.2 | added |

## coffe.md (12 fixes; first pass had no code reading)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Docker image built once; `-x` host | OK | README.md; sandbox.py:5-30 | cited |
| "One process at a time in Docker" (paper §7.1) | PARTLY WRONG for code | evaluate.py:197-215 launches `-n` parallel containers incl. instr_count | added caveat |
| 12 repeats, drop max/min, mean | OK + detail | code_execution.py:1012-1020; each repeat a fresh Process (l.764-782) | cited |
| 5 s cap per measurement | CODE MISMATCH | evaluator.py:946 passes ref_time=5; limit = max(0.1, 10 x 5) = 50 s (code_execution.py:998-1006); paper §3.4 says 5 s | flagged |
| 20 generated, top 5 by avg instruction count | paper OK; repo not found | stgen has `iteration=20` only (st_generator.py:33); selection step not in repo | [unk] |
| efficient@1 rule | OK, detailed | strict `gt > sum(cic)` over stressful tests; speedup = sum gt / sum cand (evaluator.py:1273-1288,1317-1327) | cited |
| "~1000x more stable" "check §3.3.1" | UNSUPPORTED section | §5.1 Table 4: RSD 0.003-0.005% vs 2.37-5.65% (ratios ~470-1900x); on correctness tests, stressful excluded | fixed |
| Cirron, perf_event_paranoid | OK | main.py:34-40; code_execution.py:26,336,752 | cited |
| Correctness limit | new | max(0.1, 10x ref time), fast_check (code_execution.py:603-615) | added |
| Cost [unk]; ~1 min per test | paper bound only | with 50 s code limit worst case larger | noted |
| Limitations | OK (summary) | §7.1/7.2/§2; no limitations section | cited |
| 398/358 | OK | README stats; paper Table 1/2 (summary) | - |
Header: clone verified at 7979acb.

## kernelbench.md (11 fixes; first pass had no code reading; paper not fetched)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Build = `build_compile_cache*` writes temp file, runs subprocess | PARTLY WRONG | only `_with_capturing` uses subprocess (eval.py:330-367); the eval path execs source in-process with TORCH_EXTENSIONS_DIR (184-207, 522); `build_compile_cache` pre-compiles on CPU into the cache dir (289-327; compile.py:30-52) | rewritten |
| "No explicit reuse of compiled artifacts" | WRONG | explicit precompile-then-load design per run/problem/sample build_dir | fixed |
| Lock errors retry | OK | eval.py:530-537 | line cited |
| `num_correct_trials` default 1 (paper 5) | OK/UNVERIFIED paper | scripts use 5 (eval_from_generations.py:120,182; run_and_check.py:107; generate_and_eval_single_sample.py:266) | cited scripts, dropped paper |
| allclose tol 1e-4 fp32, 1e-2 fp16/bf16 | OK | eval.py:83-102,802-805 (comment l.800 says v0 used 1e-2) | - |
| timing: warmup 3, L2 flush 256 MB, mean/std/min/max | OK + detail | timing.py:126-142,201-281,602-625; first trial discarded | added |
| num_perf_trials default 10; 100 baseline | incomplete | scripts use 100 for candidates too; baseline defaults warmup 5, trials 100 (timing.py:9-15) | fixed |
| "Baselines precomputed, re-time" | OK | README.md:153-154 | cited |
| Reference timed per candidate | NEW | eval.py:654-680 (default check_for_excessive_speedup) | added |
| Excessive-speedup flag only, 10x | OK | eval.py:411-412,691-695 | - |
| EVAL.md "[unk]" for refinement; unit tests path | WRONG/garbled | EVAL.md has no refinement text; refinement is Caesar (README.md:164); tests exist at src/kernelbench/unit_tests | fixed |
| "compile dominates" | UNSUPPORTED | no source | marked [inf] |

## effibench-x.md (12 fixes; first pass had not read the sandbox code)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| C++ `-O2 -fsanitize=address` | UNSUPPORTED for execution | registry only (utils.py:309, no consumer); executed `g++ -std=c++20 -O2` (llm_sandbox/utils.py:123) | flagged, [inf] |
| Build reuse [unk] | WRONG omission | compile skipped for later tests in a batch if code unchanged (llm_sandbox/docker.py:327-331,358-359) | added |
| 100 tests; candidate must pass all | OK + detail | evaluate_solution.py:63-73 early_stop=False; all tests always run; is_passed also accepts empty output exit 0 or output == input+output (l.232-246) | added |
| Tests one process? | NEW | each test a separate submission, batch run sequentially by one worker (backend_utils.py:353-369) | added |
| Profiler 0.1 ms; runtime/memory/integral definitions | OK, detailed | profiler.cpp:39,100-158; statistics.cpp:73-91 | cited |
| Limits 10 s, 1024 MiB | OK | run_tests.py:49-50; paper §5 | - |
| ET/MP/MI clipped ratios | OK | evaluate_solution.py:311-340 | cited |
| Core pinning with topology | OK | backends/docker.py:47-57; start_sandbox.py:40-44 | cited |
| Repeat study (3 runs, +/-1.7 pts) | UNVERIFIED | App. C.2 text not available to critic | demoted to [unk] |
| Repeats in main tables [unk] | refined | none in code path (single run per test) | [src] |
| Limitations/cost (§A) | UNVERIFIED | App. A not read | demoted |
Header: clone verified at 21b6668.

## Notes for cross-system synthesis
- Per-edit test selection: none in any of the 8 (all fixed per task/problem); PIE service accepts a `testcases` subset parameter, so selection is mechanically possible.
- Cumulative re-validation: none in any of the 8.
- Build reduction: KernelBench has an explicit precompile-and-cache split; EffiBench-X reuses the compiled binary across the tests of one candidate; others have no build.
- Statistical test: none in any of the 8 (EffiBench paper uses Kruskal-Wallis only across environments).
