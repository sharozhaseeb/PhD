# Critic log, group E (perf-bench-reliability, perfopt-bench, swe-opt, codeevolve)

Date 2026-11-21. Sources re-read in full: arXiv HTML of 2607.01211v2, 2607.07744v1, 2606.25530v2, 2605.04677v1 (fetched with curl, converted to text); repos at pinned SHAs via raw.githubusercontent.com. Pinned: chenzhi-cz/performance-optimization-benchmark-reliability @ 44a1cb86a9f765b0375b4cfb479641f3c19f0774 (still HEAD of main); SWE-Opt/SWE-Opt @ 48fa73e84b369d84c32290ab8d1c7ba0a800308a (still HEAD). PERFOPT-Bench anonymous mirror: expired.

## perf-bench-reliability.md (OK 12, WRONG 1, UNSUPPORTED 1, LINE-OFF 0; 5 edits)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| 740 patches = 102+140+498; 4 GCP profiles, 64 vCPU/256 GB; 3 rounds = 12 replays | OK | III-A, Table II | clarified one replay per machine-round and all-12 rule |
| Valid in every replay 39/102, 11/140, 411/498 | OK | abstract, III-C, repo summary CSV (construction_valid_cross_machine_tasks 39/11/411) | denominator note added |
| Faster-than-base 91/48/470 | OK | III-C, CSV | none |
| Not evaluable 4/2/0 | OK (was missing) | Table IV | added |
| GSO >=1.2x, 1.1x fallback | OK | Table III; CSV: fallback for <=5 selected tests | detail added |
| SWE-Perf 20 repeats, IQR, MWU delta>0.05 | OK | Table III | none |
| SWE-fficiency mean diff > 2 sigma_post | OK | Table III | none |
| Noise 3.81/1.41/2.41 pp; 101/138 within 5 pp | OK | Table V, III-D | added task counts 98/138/498 |
| Leaderboard check 450 all pass, 449 beat base | OK | V-A (also 384 match reference) | added 384 and 10 OpenHands submissions |
| Limitations [unk] | UNSUPPORTED (findable) | Sec. VII | filled in |
| Recommendations: no repeat count/statistic | OK (verified by absence in full text) | III-E, VI are qualitative only | stated explicitly |
| "Argues for deterministic measurement (instruction counts)" | WRONG | no such argument in text | marked as survey inference |
| Cost [unk], build reduction [unk] | OK | not found | none |

Priority answer: 12 machine-round replays per patch (4 machines x 3 rounds); benchmarks' own repeats/workloads/rules reused unchanged; no concrete repeat count, statistic or test recommended; recommendations are qualitative (workloads must stress the optimized path, clear margin over noise, separate cross-machine-verified from unstable tasks, hidden workloads, resource metrics).

## perfopt-bench.md (OK 9, WRONG 2, UNSUPPORTED 2, LINE-OFF 1; 6 edits)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| "7 long-horizon C tasks" | WRONG | abstract, B.6: 12 tasks; 7 is the stack count | fixed |
| cpuset isolation / serial GPU tasks as noise control | WRONG (misattributed) | A.4 Stage 3 is difficulty calibration of a pilot solver during task construction, not evaluation of the stacks | reworded |
| i7 Windows 11, build.ps1, GCC/MSVC | OK | App. A, B.3, B.6 | cites corrected |
| Agent rebuild in loop [unk] | UNSUPPORTED | A.3.1: agent runs test.ps1 in loop; B.5: test.sh checks correctness and speedup threshold | updated; build call inside test.ps1 stays [unk] |
| test.ps1 "not the scoring check" | LINE-OFF | final scoring is the hidden evaluator (A.2.1) | clarified |
| Threshold "expert-refined" | UNSUPPORTED | A.4: from private reference run, may be raised in calibration; expert selects the 12 tasks | fixed |
| Metric, single run per cell, "descriptive snapshots" | OK | 3.1, Limitations | none |
| Relay pilot 8 sequences, 1.02-2.48 | OK | 3.5, Table 5 | detail added |
| Shortcut audit, hidden tests, randomized API tests | OK | 3.1, A.3.2 | none |
| Repo not opened | checked | mirror API returns repository_expired | recorded |
Not verified: repeats and warm-up inside the hidden evaluator (paper says only "repeated").

## swe-opt.md (OK 11, WRONG 1, UNSUPPORTED 1, LINE-OFF 1; 9 edits)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| 102 tasks, 3 libs, runtime+peak+TWMU | OK | 2.2-2.3 | none |
| Median 10 unit tests, 6 configs, <=24 workloads, seed 42 | OK | Table 2, App. B, config.yaml L4 | none |
| warmup 5-12, CV 0.08, samples 5-15, 30 s, k=3.5 | OK | config.yaml L16-19, 26-28, 51-54 | line cites added |
| "RCIW threshold 0.1" as acceptance gate | WRONG (role) | 0.1 is the adaptive-sampling stop rule (measurement_utils.py L396-448; paper E.4). Acceptance gates in report_analyzer.py L335-345, L436-445, L490-520: within-run RCIW <= 20% ceiling, SNR >= 2, effect >= 5% | rewritten |
| SNR 2.0 gate | OK | config.yaml L60; paper 2.4 | defined SNR |
| Single-core pinning | OK | config.yaml cpuset "2", cpuset_mems "0", thread vars; paper E.6 | made explicit; host M4 Max 36 GB |
| correctness_test_runner L9-80 | LINE-OFF | status mapping L25-27, L72-80; json-report L59-60 | fixed |
| Tests fixed per task | OK | core_tests from dataset row (run_evaluation.py L229) | cites added |
| Rebuild after patch [unk] | UNSUPPORTED | patch applied inside container (entrypoint L117), no rebuild call; editable install in Dockerfile.pandas | documented; compiled-extension rebuild still [unk] |
| Perf failure flips correctness | new fact | entrypoint L165-182 | added |
| OpenCode 50 steps, hidden perf tests | OK | 3.1 (App. D.2 cite dropped, not verified) | trimmed |
| Harmonic mean per PR, arithmetic across PRs | OK | E.5 | none |
| Limitations | OK | Sec. 6 | none |
Not verified: number of fresh containers per workload; paper text calls the stability bound "configured system-noise threshold" (code value 20%).

## codeevolve.md (OK 10, WRONG 0, UNSUPPORTED 3, LINE-OFF 1; 4 edits)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| OpenEvolve extension, JFR, MCTS, islands K=5, migration every 50 gens | OK | 1.2, App. C | none |
| 15.22 over 7 functions | OK but incomplete | 5.2: average over 4 LLMs, vs RPBD 7.12, wins 5/7 | context added |
| Cascade; tau 0.5/0.75/0.9, weight 0.1 | OK | 3.3 | noted stage mapping not stated |
| "first stage build validation" cited 3.2, 3.3 | LINE-OFF | 3.2 filters, 3.3 cascade | reworded |
| Speedup via prod traffic in sandbox | OK | 5.1 | added no repeat/CI |
| Perf test as per-candidate check | UNSUPPORTED | cascade lists "performance tests"; per-candidate use of replay not stated | marked [unk] |
| Limitations cited 5.3, 6.2 incl. "7 functions" | UNSUPPORTED | 5.3 is an observation; 7-function scope not a stated limitation | split |
| Refinement agent re-runs validation | OK | 3.2 | none |
| No repo | OK | none found in text | none |
No cross-system conclusion changes.
