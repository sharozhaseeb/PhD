# Final critic log (findings.md, survey-table.md, README.md)

Format: claim | verdict | evidence | fix. Primary-source checks marked PRIMARY.

## Primary-source checks (13)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| SWE-fficiency: 5 installs per candidate | OK PRIMARY | `test_spec.py:490-491` install in `_get_basic_eval_components`, used by perf script (1119) and correctness script (1196); `run_validation.py` runs perf.sh x4 (warm-up + measured, pre and post) + correctness.sh x1 | none |
| SWE-Perf Mann-Whitney p<0.1, one-sided | OK PRIMARY | `evaluation/utils.py` `find_max_significant_improvement(p_threshold=0.1, alternative='greater', step=0.001)`; no caller overrides | none |
| SWE-Perf 20 repeats, 3 warm-ups, IQR filter | OK PRIMARY | `test_spec.py:33` REPEAT_TIME=20; three warm-up commands 302-312; `filter_outliers` IQR (k=1) | none |
| GSO 1.1x gate + 0.95 harmonic mean | OK PRIMARY, wording tightened | `constants.py:33,39` (1.1, 0.95); `metrics.py:256-259` opt_commit nested inside gate `round(gm,1)>=1.1`; install after apply_patch and again after checkout (`evalscript.py:165-212`) | F4 cell now says the gate is on geometric-mean speed-up and precedes the 0.95 check |
| FormulaCode filename-mapped tests, once at end | OK PRIMARY | `pytest_runner.py` get_changed_files (git diff names, staged excluded by default); `run-tests.sh:114-146` single post-run snapshot verify + testrunner | none |
| PerfAgent testmon 66-99% GSO / 47-98% SWE-fficiency-Lite; "without missing"; §VI limitation | OK PRIMARY (arXiv HTML) | III-D quote "66%-99% on GSO and by 47%-98% on SWE-fficiency-Lite", "without missing any correctness regressions"; VI "tracks only Python coverage" | none |
| PerfAgent "no public code" | OVERCLAIM | note: none found (search), not proof | wording now "no public code found" (findings F2, README) |
| Codeflash no cumulative re-run | OK PRIMARY (absence) | `optimizer.py` ~686-722 only logs patch list; no combined run | none |
| Codeflash worktree "fresh baseline on modified tree; no full suite before PR" | LABEL UPGRADE | note marks both [inf] | findings F5 now [inf] on both |
| SysLLMatic Alg. 1 vs code | OK (note) | note: Alg. 1 l.19-21; `run_app_and_measure` no call site | none |
| Meta PTS all tests on master every few hours; >0.95 / >0.999 | OK PRIMARY (ar5iv) | quotes: "Once every few hours, all tests are exercised on the most recent version of master branch"; "<5% of individual test failures and <0.1% of faulty changes" | none |
| asv factor 1.1 + p<0.002 + CI fallback | OK PRIMARY | `common_args.py:44-49` default 1.1; `_stats.py:30` p_threshold=0.002; `compare.py:97` is_different before factor | none |
| SWE-bench v4.1.0 install per prediction; get_test_directives | OK PRIMARY | `test_spec/python.py:302-303` (setup), `:443-444` (eval script); `get_test_directives` reads test_patch files, drops non-test ext | none |

## Other claims checked against notes
| Claim | Verdict | Fix |
|---|---|---|
| Counts: 24 core critic-checked notes; 19 public code artifacts | OK (24 files; 19 repos counted) | none |
| README "28 notes (template, discovery log)" | AMBIGUOUS: 30 files = 28 notes + template + log; 4 notes pending | reworded |
| README SemOpt "private figshare link only" | note: private-share link, not opened | reworded |
| F2 regime 3 "Only two systems"; F3 "Nothing maps diff to benchmarks [src]" | absence claim labelled [src] | F3 now [src]/[unk] |
| "What nobody does" #1 | evidence list incomplete (several builds [unk]; 12 discovery queries) | added [unk] builds and query count; stays conditional |
| F1 header / README headline 1, 3 absolute "No system / Nobody" | overclaim vs sample | made conditional ("in this sample", "surveyed", "none found") |
| F4 SemOpt ">=5%" | note says >5% | fixed |
| F4 deterministic school "repeats unnecessary [src]" | interpretive | [inf] |
| F4 "threshold only" lists ECCO, SysLLMatic with no threshold | imprecise | caveat sentence added |
| F4 noise "SWE-fficiency and FormulaCode are the exceptions" | omits EffiBench-X (one core per worker) | added |
| F5 "Functional CI does periodic full validation / standard (Meta, Google)" | TAP does not re-run a full suite; two cases are not "standard" | reworded to precedent; TAP described accurately; README headline 5 likewise |
| F7 Mercury "scores can exceed 1" stated plain | note [inf], only when human spread <1 s | qualified with [inf] |
| Quick-compare ECO cumulative "yes (post-rollout GWP)" vs F5 (ECO is monitoring, not re-validation) | internal contradiction | changed to partial |
| survey-table PerfAgent "47-99%" | union of 66-99 and 47-98; consistent | none |

## Notes possibly wrong (not edited)
- semopt.md: line 17 says 73.72% of 8,082 candidates compile "(C/C++)" while line 37 says 8,082 candidates "over the 10 projects"; scope (C/C++ only or incl. Python, which has 9,483 separate candidates) is unclear. findings F1 quotes it without scope.
- codeflash.md line numbers (`function_optimizer.py` 1187-1191, 1409-1412 etc.) did not open at the local path I tried (`codeflash/optimization/function_optimizer.py` missing; file is under a different package path), so line cites were not re-verified; the behaviour (no combined run, patch list only logged) was.

## Not done
- Late notes (perf-bench-reliability, perfopt-bench, swe-opt, codeevolve) ignored per instruction; no finding depends on them.

## PM-polish pass
Primary checks: Codeflash `critic.py:94-101` + `function_optimizer.py:3115-3116` + `config_consts.py:21`; GSO `evalscript.py:126-213`, `constants.py:34`; SWE-fficiency `run_validation.py:560-650,943-958`, `test_spec.py:490-491`; SysLLMatic `dacapo_benchmark.py:105-203` (git show); SemOpt PDF text lines 1610-1625, 1710-1713; survey-table A1/A2 vs Quick-compare.

| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Codeflash 5-250 loops, 10 s budget | OK PRIMARY | defaults 5/250 at 3115-3116; 10 s `config_consts.py:21`; 3/100 only in subagent mode | none |
| Codeflash 15% floor if <10 µs, x2 in CI | OK PRIMARY | `3 * MIN_IMPROVEMENT_THRESHOLD if runtime < 10000` (=0.15), `*2` if CI; docstring says 2x, code 3x | none |
| GSO 2 installs, <=20 scripts x 5 runs x 3 phases (<=300) | OK PRIMARY | `SKIP_MAIN=True`; install after patch and after commit checkout; MAX_TEST_COUNT 20; MAX_ITERS 5 (1 for llama-cpp, onnxruntime, tokenizers) | README: "5 runs (1 for 3 repos)" |
| SWE-fficiency 5 installs, 4 perf.sh, repeat=10 typically | OK PRIMARY | perf.sh at 562-571 and 639-647 (warm-up + measured, pre and post), correctness.sh once, install in each script `test_spec.py:490-491`; repeat=10 is the paper template (typical, not code) | none |
| SysLLMatic 1 make compile, 1 make measure on first unit test | OK PRIMARY | `compile` once; `run_tests` one `make test` per matched file, stop at first fail; `_run_rapl` runs `make measure TEST=unit_tests[0]` once | none |
| SemOpt 6 runs, first dropped, mean of 5 | OK PRIMARY (PDF 1619-1625) | "6 times each on both the original and optimized"; whether the original is re-measured per candidate not stated | README: stated original also 6x, per-candidate re-measure [unk] |
| SemOpt "full project unit suite" unlabelled in a [src] cell | LABEL UPGRADE | note: "reads as whole suite" [inf] | README: marked [inf] |
| SemOpt "assembled and re-measured" | LABEL UPGRADE | note: re-measure is [inf], unit re-run [unk] | README: assembled [src], re-measured [inf] |
| SemOpt 9,483 Python candidates all pass, 152 functions | OK PRIMARY | PDF 1712-1713 | none |
| PerfAgent 1 timed run, 10 s py-spy, testmon, /build.sh | OK (note) | notes III-A/B, IV-E4; no code exists | none |
| OpenEvolve 3-stage cascade, 300 s, <=3 retries | OK (note) | config.py:411-430; retries = max_retries+1 attempts | none |
| F7 counts 39/102, 11/140, 411/498, 4 machines x 3 rounds; no numeric advice | OK (note) | perf-bench-reliability.md lines 8, 25, 36 | none |
| F7 SWE-Opt gates (20% ceiling, SNR>=2, >=5%), RCIW 0.1 stop, cpuset=2 | OK (note, code-level) | swe-opt.md lines 24-27 | none |
| F7 "SWE-fficiency most stable" | PARTLY WRONG | by median noise std SWE-Perf is lowest (1.41 pp), SWE-fficiency 2.41, GSO 3.81; only by validity rate is SWE-fficiency best | findings F7 qualified |
| F3 header "never by a deterministic rule" | OVERCLAIM | body says "none found [unk]" | header: "no ... rule ... was found in this sample" |
| F3 FormulaCode all workloads, prompt `--bench=<regex>` "discouraged"; asv `-b` | OK (note) | formulacode.md 25-26; asv note 19 | none |
| survey-table A1 (7 rows) + A2 (14 rows) vs Quick-compare (21 systems before Table-B rows) | OK | no row lost or duplicated; A1/A2 headers and separators intact | none |

Left for architect: F3 lists "PerfAgent times the one benchmark-provided workload" under human/agent-picked subsets; it is neither, consider moving to "Fixed per task". Codeflash 5-250 are loop bounds with a stability early stop (not a count per candidate).
