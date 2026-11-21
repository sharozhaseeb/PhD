# Critic log, group A (2026-11-21)

Notes: swe-bench-harness.md, swe-perf.md, gso.md, swe-fficiency.md. Clones re-checked at the commits in each note header (all matched `git rev-parse HEAD`). Papers: SWE-Perf 2507.12415 v2, GSO 2505.23671 v3, SWE-fficiency 2511.06090 v3 were read as PDF text (pdftotext of the fetched PDF). SWE-bench 2310.06770: both PDF fetches timed out (300 s), so paper claims were NOT re-verified.

## swe-bench-harness.md

| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| v4.1.0 three image layers, env key = sha256 `[:22]`, builders at docker_build.py 162/270/336 | OK | `test_spec.py:90-103`, `docker_build.py:162,270,336` | none |
| `--cache_level` none/base/env/instance default env; semantics = which images are removed | OK | `run_evaluation.py:636-641`, `docker_utils.py:295-311` | none |
| Install in instance image via `setup_repo.sh` | OK | `dockerfiles/python.py:48-52`, `test_spec/python.py:274-303` | added note on tag stripping |
| Install re-run inside every eval script after patch | OK | `test_spec/python.py:443-444` (install precedes test patch and tests); patch applied before eval.sh in `run_evaluation.py:166-207` | none |
| `get_test_directives` = test-patch files only | OK | `test_spec/python.py:230-261` | none |
| F2P/P2P status rules FULL/PARTIAL/NO | OK | `grading.py:215-232` | none |
| HEAD: images prebuilt, TestSpec "assumes images exist", eval.sh is dataset data | OK | `types.py:25-29`, `image_spec.py:36-48`, `checks.py:66-69`, `CHANGELOG.md:45`, `utils.py:251-273`, `task/repo.py:3-17` | none |
| HEAD: `cache_level` in no .py file | OK | grep: only 4 docs files | none |
| HEAD: patch apply chain and cleanup | LINE-OFF/detail | chain is `git apply --verbose`, `--3way`, `--reject`, `patch --batch --forward --fuzz=5 -p1 -i` (`run_evaluation.py:64-68`); `git checkout -- . ; git clean -fd` between attempts at 303-309 | wording fixed |
| Per-prediction install at HEAD | UNSUPPORTED for HEAD | eval.sh is HF dataset data, not in clone | marked [unk] for HEAD; v4.1.0 is the evidence |
| anti-spoof exit-code cross-check `grading.py:162-176`; result cache `faq.md:103`, `run_evaluation.py:272-273` | OK (faq cite is the 102-105 paragraph) | seen | cite widened |
| All paper claims (App. A.3, A.4, A.1, Sec. 2.1, Sec. 7) | UNVERIFIED | PDF fetch timed out twice | downgraded to [inf] in header and one line; others flagged by blanket CRITIC note |
| `docker_setup.md` disk numbers (~100 GB env, ~2000 GB instance, 120 GB, 16 GB) | OK | `docker_setup.md:13-14,96-101` | none |

Counts: OK 10, WRONG 0, LINE-OFF 1, UNSUPPORTED 1 (HEAD install), UNVERIFIED 1 group (paper).

## swe-perf.md

| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Mann-Whitney p threshold | OPEN POINT RESOLVED | code `p_threshold=0.1` default (`evaluation/utils.py:365`, `data_collection/harness/utils.py:362`), never overridden (`check_evaluation.py:72,74`, `check_validation_single_runs2.py:114`); paper alpha = 0.1 (Alg. 1, App. B.1, Sec. 3.2 Phase 4) | note states 0.1 for both curation and evaluation |
| "0.001" | OPEN POINT RESOLVED | it is the x step in code (`step=0.001`); paper Alg. 1 default step 0.01. Not a p-value | explained in note |
| "0.01" in paper | not found | paper has 0.1 (alpha), 0.01 (step), 0.05 (min gain), 0.3 (Phase 3 ratio) | n/a |
| What it gates | RESOLVED | Curation Phase 4: ratio from `find_max_significant_improvement` must be >= 0.05 (`single_runs2.py:114,121,138`); a direct `mannwhitneyu` call at :136 is dead (p unused). Phase 3: plain mean ratio < -0.3, no test (`all_runs.py:160`). Evaluation: p only affects the Performance score x (0 if not significant); correctness is "all efficiency tests pass" and is independent; no 0.05 filter at evaluation | added |
| CPU count (code 10 vs paper 1) | RESOLVED | code: 2e9 x5 = 10 CPUs (`evaluation/docker_build.py:541-544`, `run_evaluation.py:110`); `data_collection/harness/check_validation_single_runs.py:109` also `is_large=True`; Phase-2 default is 2 CPUs. Paper Sec. 3.2: 1 core in collection, 5 cores in Phase 4 and evaluation. Code matches neither 1 nor 5. No cpuset | rewritten |
| "12 SWE-bench-style repos" | WRONG | paper Table 1 / Fig. 3: 9 repos in final dataset; README says crawl from 12 | fixed |
| Install re-run in each eval.sh, run twice (base, patched) | OK | `test_spec.py:352-353`; `run_evaluation.py:122-221` (eval.sh run, patch apply, eval.sh run again) | none |
| Tests = `efficiency_test` only, no test patch, no P2P | OK | `test_spec.py:302-321`; correctness `check_evaluation.py:49,54` | line cite +1 |
| 3 warm-ups + 20 repeats, IQR k=1 | OK | `test_spec.py:33,302-321`, `utils.py:345-361`; paper Phase 4 (note: paper warm-up wording is "three performance-related unit tests", code runs the whole efficiency set 3x) | none |
| `check_evaluation.py:66-69` run_failed | LINE-OFF | failures at 61-68 | fixed |
| Phase 3 selection wording "(paper) do not themselves be modified" | WRONG wording | paper: tests exercise patched code and execute no unit test modified in the PR | fixed |
| Base re-measured at eval time | OK, now [src] | paper Sec. 4 text "re-evaluated the original codebase runtime" | upgraded |
| Hardware 256 logical cores, 2 TiB | OK | App. B | none |
| Limitations (App. A, B.3) | OK | App. A limited repos, human patch not optimal | none |
| Cost per candidate not reported | not found in paper text; OK as [unk] | | none |

Counts: OK 9, WRONG 2 (repo count; selection wording), LINE-OFF 2, UNSUPPORTED 0; 3 open points resolved.

## gso.md

| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Eval script order: base runs, apply, install, patch runs, (main skipped), checkout opt_commit, install, commit runs | OK | `evalscript.py:168-213`, `SKIP_MAIN` at :126 | none |
| >= 2 installs per candidate; no reduced build | OK | same; install helper :111-124 | none |
| Per-instance install commands | [unk] confirmed | repo has none; HF dataset field `install_commands`; collection-time source `collect/execute/execute.py:259`, cleanup `collect/utils.py:4-29` | clarified [unk] |
| Tests per candidate fixed, no unit tests, eqcheck vs reference | OK | `evalscript.py:127-133`, `grade.py:131-139` (tests copied with patches applied, `apply_patches`) | none |
| Repeats 5 (1 for three repos), timeouts 300/0, fresh process | OK | `evalscript.py:84,138-146` | none |
| Opt@K success `opt_commit` = hm speedup vs commit > 0.95 | WRONG (incomplete) | `metrics.py:256-260`: `opt_commit` is nested inside `if base_mean > patch_mean and round(gm,1) >= 1.1` | fixed |
| Paper defines success as S >= p; code uses strict `>` and extra 1.1x gate | code-only detail | paper Sec. 2.3 | added |
| No statistical test, no pinning/limits in container | OK | `docker_build.py:326-341`; grep scipy/mannwhitney in harness: none | none |
| "--max_workers runs parallel containers" `README.md:36` | UNSUPPORTED as cited | README says "scale up parallel builds" | replaced with `run_evaluation.py:127-175` (low-resource parallel, high-resource repos sequential, retries up to 3, 330 s sleep) |
| Paper: 3-machine comparison App. D | OK, now verified | App. D: 16/32/64-core machines | resolved |
| Paper: 3 h / 20 min per-step | OK | Sec. 3 | none |
| 59% non-Python | OK | Table 1: 58.8%; Sec. 2.4 text says 60% | noted |
| mean 12.45 tests, max 20 | OK | Table 1; `constants.py:34` | none |
| dockerfile.py:81-82 pre-run of tests | OK | seen | none |
| Wall time per candidate not reported | not found | | stays [unk] |

Counts: OK 11, WRONG 1 (opt_commit gate), UNSUPPORTED 1 (README cite), LINE-OFF 0.

## swe-fficiency.md

| Claim | Verdict | Evidence | Fix |
|---|---|---|---|
| Per-candidate flow = `run_evaluation.py` | WRONG for the leaderboard path | `swefficiency/cli.py:95-122` (documented `swefficiency eval`) calls `run_validation.main(run_perf=True, run_correctness=True, run_coverage=False, process_isolation=True, timeout=7200)`; `run_evaluation.py` is a legacy runner | note restructured with CRITIC header and flags |
| Correctness script vs eval_script (open point) | RESOLVED | leaderboard path uses `test_spec.correctness_script` (`run_validation.py:943-958`; script `test_spec.py:1184-1280`: covering test files, shuf, `xargs -P 4`, retry only if rc>1) | fixed |
| Graded by PASS_TO_PASS; FAIL_TO_PASS | partly WRONG | `report.py:60-135` only checks PASS_TO_PASS ids PASS; F2P unused | fixed |
| mem_limit 32g vs 16 GB (open point) | RESOLVED | `docker_build.py:785-840`: hard 32g, memswap 32g, soft reservation 16g, oom_kill_disable; paper Sec. 3/App. E/F.2 and README say 16 GB. Legacy path has no cpu_groups | fixed |
| Installs per candidate "up to three" | WRONG for leaderboard | perf_warmup=True: perf.sh x4 + correctness.sh x1, each with install = 5 (`run_validation.py:562,639,943-958`, `test_spec.py:490-491`) | fixed |
| Paper App. F.1 "no installation during evaluation" taken as fact | WRONG / code contradicts | App. F.1 text vs `_get_basic_eval_components` install in every script | fixed with explicit contradiction |
| `constants.py:3328` active `build_ext --inplace -j 4` | WRONG | lines 3328 and 3349 are commented out | fixed |
| `run_evaluation.py:274-276` improvement oddity | OK but legacy only | CLI uses `pre_mean/post_mean` (`run_validation.py:715`) | scoped |
| Warm-up "no policy" | incomplete | harness runs full perf.sh once unmeasured before each measurement; fork-per-repeat isolation transform on by default (`run_validation.py:522-532`, `run_to_run_isolation.py:220`, paper App. L.2) | added |
| AST/coverage anti-cheat part of evaluation | WRONG for CLI | `run_coverage=False` in CLI; AST check only under run_coverage; introspection guard does run (:890-935) | fixed |
| Median 7,723 covering tests, 74% > 1000 | OK | App. E.3 | none |
| Curation filter mu_pre-mu_post <= 2 sigma_post; 10 correctness runs for flakiness | OK | App. E.5 | none |
| Workload templates repeat=10; raw example number=5 repeat=1000 | OK | App. B.2/E.4/L.2 | none |
| 4 vCPUs, NUMA, daemon pinning, SR spread < 0.5% | OK from paper; daemon-pinning scripts not read | App. F.2, N Table 11 | [unk] marker added |
| README 37, 39, 66, 184, 28, 38-40, 141-154 | OK | seen | none |
| `report.py:140` adjusted ratio | LINE-OFF | logic at ~118-135 | fixed |
| install cites constants.py 169, 263, 1036, 3215 | OK | seen | none |
| Not verified | `scripts/vm/` pinning scripts, `_introspection_patch_check.py` body, cost per candidate | not opened / not reported | [unk] |

Counts: OK 9, WRONG 6, LINE-OFF 1, UNSUPPORTED 0 (plus 1 incomplete-claim extension).
