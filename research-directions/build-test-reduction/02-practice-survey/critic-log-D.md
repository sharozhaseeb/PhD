# Critic log, group D (2026-11-21)

Method: re-opened cited files in local clones (asv @1f9db13, numpy @e092b91, pandas @ca8d2da, scipy @73d740c, pyperformance @1c80986, pytest-codspeed @15d46b4, openevolve @4167db4); read PDFs of ECO (arXiv v1 and v2), AlphaEvolve (v1), Meta PTS (1810.05286) and Google TAP (45861.pdf) as extracted text; docs pages (pyperf, CodSpeed, Bazel) via a summarising fetch tool, so docs quotes are second-hand.

## asv-numpy-scipy-pandas.md (7 fixes)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Build cmd per project | OK | numpy conf:20-22, scipy :27-29, pandas :40-41 | none |
| Build only if commit not in cache; install; finalize | OK | environment.py:853-895 | none |
| Cache keyed by commit, latest build_cache_size kept, default 2 | OK | build_cache.py:10-35,82; docs asv.conf.json.rst:499-501 | none |
| build_cache_size numpy 8 / pandas 8 / scipy 10 | OK | numpy conf:77, pandas conf:36, scipy conf:66 | none |
| env types virtualenv / rattler | OK | scipy conf:64, pandas conf:7 | none |
| `--python=same` -> existing:same | OK | common_args.py:251-252 | none |
| "CI uses --python=same" (numpy too) | UNSUPPORTED for numpy | numpy runs `spin bench --quick`; `.spin/cmds.py` not in the sparse clone, so asv flags unseen | split: pandas [src], numpy [unk] |
| compare `_isna` 72-74; factor logic 77-100 | OK | compare.py:72-100 | none |
| is_different: Mann-Whitney p<0.002, p_min check, 99% CI fallback | OK | _stats.py:30-69 | none |
| factor default 1.1; --no-stats | OK | common_args.py:42-61 | none |
| rounds 2; repeat defaults; median; warmup 0.1 s; sample_time 10 ms | OK | benchmarks.rst:138-171 | none |
| "Different benchmarks run in separate processes [benchmarks.rst:131]" | WRONG cite | text is in using.rst:248 and writing_benchmarks.rst:131 | fixed |
| --quick = run once, results not saved | OK | run.py:138-146 | none |
| continuous default baseline = parent; interleave-rounds | OK | continuous.py:28-33, 49-70 | none |
| step_detect serves publish, not PR compare | OK (inf) | used by graph.py and plugins/regressions.py | none |
| tuning.rst recommends pyperf system tune, --cpu-affinity | OK | tuning.rst:60-71 | none |
| numpy CI job: `if != push`, asv machine, `spin bench --quick` | OK | linux.yml:~197-226; also `needs: smoke_test`, `spin build` first | build step noted |
| pandas ci-asv; "pixi.toml is not in the sparse clone" | WRONG | pixi.toml is in the clone, `[tasks.ci-asv]` at :310-332; it also runs `asv machine --yes`; pandas builds editable first (code-checks.yml ~118-123) | fixed |
| scipy "17 workflow files, none benchmark" | WRONG count | 16 files; none benchmark-related | fixed |
| scipy CODEOWNERS:63 | OK | CODEOWNERS:63 | none |
| regressions_first_commits "scipy ~70-72" | LINE-OFF | pandas conf:37, scipy conf:87-89 | fixed |
| pandas forkserver comment | OK | pixi.toml:~322-324 | line added |
| numpy README 36-61, scipy README 22-49 | OK | numpy README:29-61 | none |
| Cost per candidate not reported | [unk] kept | no figures found | none |
Not verifiable: numpy `spin bench` internals; whether any nightly bot exists outside these repos.

## pyperformance.md (4 fixes)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| 77 benchmark directories | WRONG | 76 `bm_*` dirs + MANIFEST file | fixed (also "77 benchmarks" in cost) |
| User supplies baseline/changed python; `--output` help | OK | cli.py:61, 108-113 | none |
| venv per benchmark / common venv first; install_pyperformance, ensure_reqs | OK | run.py:78-104; venv.py:213, 243 | none |
| requirements.in major-version comment | OK | requirements.in:1-3 | none |
| CLI flags --fast/--rigorous/--affinity/--min-time/--same-loops/--warmups | OK | cli.py:76-150; run.py:224-245 | none |
| compare: t-test, 1% floor, "alpha=0.95" comment | OK | compare.py:136-178 | none |
| "alpha=0.95 means p<0.05" | inf only | neither code nor docs state a p threshold (pyperf docs also say "alpha equals to 0.95") | relabelled |
| pyperf 20x3 values, 1 warmup, JIT 6x10, min-time 100 ms | OK | pyperf docs runner.html; pyperf main `_runner.py` via raw fetch (pyperf @aa51cd48a6, 2026-11-16): warmups=1, min_time=0.1 | version recorded |
| --fast = 10x2, --rigorous = 40x3 | OK | docs and `_runner.py` (max(n//2,3), max(v*2//3,2); rigorous doubles procs) | none |
| calibration worker; first value ignored | OK | run_benchmark.html | none |
| pyperf compare_to uses the same t-test | OK | analyze.html | none |
| system tune details; "does not change ASLR / isolcpus" | OK with caveat | system.html: only checks them; docs do not say which turbo/IRQ values tune writes | wording fixed, [unk] added |
| ASLR/hash-seed rationale | [inf] kept | not read | none |
No pyperf release number is shown in the docs; recorded the repo commit instead.

## codspeed.md (9 fixes)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Docs 404 / search-summary only | WRONG premise | pages exist: /docs/instruments/cpu, /docs/features/customization.md, /understanding-the-metrics.md, /performance-checks | upgraded to fetched |
| MeasurementMode; default mode by CODSPEED_ENV / CODSPEED_RUNNER_MODE | OK | instruments/__init__.py:58-77; plugin.py:145-156 | lines tightened |
| Simulation: start_benchmark, callgrind start/stop, run once | OK, imprecise | analysis.py:58-91; with perf-trampoline it first calls fn once as warmup (:75-77) | added |
| trampoline "affects call graph only" | WRONG | it also triggers the warmup call | fixed |
| cycles weighted, 10-40 / 100+ cycle penalties, constant frequency, syscalls excluded, run once | OK | cpu page | none |
| "does not follow child processes; no static executables" | UNSUPPORTED | not on cpu page | marked [unk] |
| "hardware-agnostic" -> deterministic | softened | page makes no determinism claim | fixed |
| Walltime: warmup 1 s, max_time 3 s, best time, IQR/stdev outliers | OK | walltime.py:30-35, 205-240 | none |
| Regression threshold default 10% | OK | customization.md | none |
| "admin-settable 0-50%" | UNSUPPORTED | page gives no range | [unk] |
| per-benchmark override | OK | customization.md | none |
| baseline = latest base commit with a run; merge commit | OK | understanding-the-metrics.md | none |
| "exceeding it fails the status check" | UNSUPPORTED | performance-checks page says only "based on threshold" | [unk] |
| no statistical test | OK | metrics page: relative change vs threshold; geometric mean at commit level | added |
| Repo CI shards 3 ways x 3 modes | WRONG | `SHARDS: 4`; modes simulation, walltime, memory | fixed |
| README example asserts output==55; workflow recommendation | OK | README:38-53, 88-119 | none |
| plugin.py "~143-160" | LINE-OFF | 141-168 | fixed |

## google-eco.md (5 fixes)
Verified against arXiv v1 PDF (Mar 2025; section numbers in the note match v1) and v2 PDF (Sep 2026; renumbered).
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| "arXiv v2, Mar 2025" | WRONG | arXiv: v1 19 Mar 2025, v2 17 Sep 2026 (retitled AI-Driven) | fixed |
| Sec 5: build failure -> fixes -> "abandoned"; unit+integration via CI | OK | v1 p.13 | none |
| "ECO does not choose tests" | OK, incomplete | v2 Sec 6: all monorepo tests affected by the change are run automatically; mechanism not described | added |
| Self-review quote; "most tests provide no indication on code performance" | OK | v1 Sec 5 | none |
| Quote "cannot perform isolated performance tests" | OK | v1 Sec 6.3 (v2 Sec 7.3) | none |
| Cmin 0.1% / Cmax 25%; >10M candidates | OK | v1 Sec 3.1.3 | section sharpened |
| top-K = 500 | OK | v1 Sec 3.2 | none |
| Microbenchmark: 10 runs, five samples, T=0.3 | OK | v1 Sec 6.1 | none |
| GWP monitoring, reverts <0.5% | OK | v1 Sec 5.1 | none |
| 55k commits; 25k lines / 6.4k commits; >99.5% | OK | v1 Sec 2.2, 6.4, abstract | none |
| ">2M cores over the past year; ~500k per quarter" | OK for v1 | v1 Sec 6.4; v2 says "several hundred thousand" normalized cores | version caveat added |
| Limitations (single-file, C++, reactive) | OK | v1 Sec 1 and 8 | none |

## alphaevolve.md (3 fixes)
All section numbers confirmed against the arXiv v1 PDF.
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Evaluator "seconds on a single device or extensive computations" | OK | Sec 2.1 | none |
| Evaluation cascade; small-scale check first | OK | Sec 2.4 | none |
| LLM feedback; parallelized eval, ~100 compute-hours | OK | Sec 2.4 | none |
| MAP-elites + islands | OK | Sec 2.5 | none |
| Throughput-optimised pipeline | OK | Sec 2.6 | none |
| Rounding check for matmul decompositions | OK | Sec 3.1 | none |
| Scheduling: simulator, unseen test set, post-deployment confirmation | OK | Sec 3.3.1 | none |
| Kernels: real TPUs, 23%, 1% | OK | Sec 3.3.2 | none |
| Circuit: robust verification | OK | Sec 3.3.3 | none |
| FlashAttention: randomized-input checks, experts, 32% / 15% | OK | Sec 3.3.4 | none |
| Repeats/warm-up/statistical test/noise "not described" | confirmed absent | full-text search | now a full-paper statement |
| Limitations "not read" | filled | Sec 6 Discussion: only tasks with automated evaluators | added |

## industrial-ci-test-selection.md (4 fixes)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Meta: ~10^4 tests/change from build deps | OK | Sec I | none |
| GBDT features (3/14/56 days, authors, 7-56 day fail rates) | OK | Sec IV-A | none |
| Selection = LikelyFailing union HighlyRanked | OK | Sec IV-B | none |
| Calibrated TestRecall >0.95, ChangeRecall >0.999 at land time | OK | Sec VI-A | none |
| Stabilization: all tests on master every few hours | OK | Sec II-B4 | none |
| Retry up to ten times | OK, scoped | Sec V: stated for runs producing training/eval data | scope added |
| Un-deflaked training: ~3x missed failures | OK | Sec VI-C | none |
| 3x fewer executions, 2x infra cost, <1/3 selected | OK | Sec I, VI-A | none |
| Weekly retraining | OK | Sec IV-D | none |
| TAP: milestone 45 min, 4.2M tests, 9 h delays, 5.5M/63K | OK | Sec I, II | none |
| TAP affected = reverse deps; milestone batching, t14 example | OK | Sec II | none |
| 1.23% "of executions" | imprecise | Intro says executions; Sec III Table II is about target histories (91.3% never fail, 2.07% pass+fail, 1.23% real after flake filter) | fixed |
| MinDist closeness model | OK | Sec IV | none |
| Bazel action cache, local then remote, hermeticity, untracked tools/env | OK | caching docs | none |
| `tests(allrdeps(//foo/bar:changed.cc))` with --universe_scope | UNSUPPORTED | exact expression not on docs page; allrdeps is Sky Query only | fixed |
Not verified: TAP culprit-finding procedure details.

## openevolve.md (8 fixes)
| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| "not cloned", WebFetch-derived | WRONG | clone exists at 4167db4 (v0.4.1) | re-read, line numbers now exact |
| Fresh temp file per candidate | OK | evaluator.py:258-271, 391-393 | cite added |
| Evaluator runs in-process in a thread pool | missing | evaluator.py:64-72, 452-461 (thread executor, orphaned on timeout) | added |
| No result cache | OK | no "cache" in evaluator.py | none |
| Cascade thresholds; failed gate returns partial result | OK | evaluator.py:467-660 (531-535, 596-598); config.py:420-421 defaults [0.5,0.75,0.9], cascade on by default | cites fixed |
| "smoke -> quality -> benchmark" from release notes | UNSUPPORTED | only an example README (background_blur:172); not enforced | downgraded |
| LLM feedback blend "0.7/0.3 default" | WRONG | 0.7/0.3 hard-coded in the combined_score recompute (:316); `llm_feedback_weight` default 0.1 (config.py:430); only when use_llm_feedback | fixed |
| Timeout -> {"error":0.0,"timeout":True}, no retry; retries max_retries+1, 1 s sleep | OK | :356-368, 258, 373-388, 399 | exact cites; defaults timeout 300, retries 3 added |
| parallel_evaluations | OK | :64-69; default 1 | none |
| Past bug "timeout averaged to 0.5, fixed v0.3.2" | UNSUPPORTED | no changelog in clone; search snippets only | marked [unk] |
| Noise control none | OK | no repeat/noise logic in evaluator.py | none |
