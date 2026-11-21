# asv (airspeed velocity) in numpy, scipy, pandas

Status: critic-checked 2026-11-21 (7 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/airspeed-velocity/asv @ 1f9db13755820bf3d7b7fbfc0f76f7fe0af4aa68 (local: `C:\Users\pc\study\bt-lab\survey\airspeed-velocity_asv`); numpy @ e092b9144edcdf1c52f46b4b2a0ad0869109c500 (benchmarks/, .github/); pandas @ ca8d2daa1bf8f30f4d1ce26dfad6792f590e298d (asv_bench/, .github/); scipy @ 73d740ca203cd4ce087a1a818fb2db576646eacc (benchmarks/, .github/) · Paper: none
Evidence labels: **[src]** read in source (file + lines @ commit), **[inf]** inferred by us, **[unk]** not found (where looked). Line numbers are those printed by grep/sed at the pinned commits; "~" marks approximate ranges.

## 1. What it is
asv is a Python benchmarking framework that runs benchmark functions across commits in isolated environments and compares results between two revisions (`asv run`, `asv continuous`, `asv compare`). numpy/scipy/pandas keep `asv.conf.json` and benchmark suites in-tree. **Headline finding: in all three repos the PR-time CI benchmark job is a smoke test (does the suite still run), not a regression gate.** [src] see section 4.

## 2. Build / environment
- Build command per project: numpy and scipy use `python -m build --wheel -o {build_cache_dir} {build_dir}` [src numpy benchmarks/asv.conf.json:21; scipy benchmarks/asv.conf.json:28]; pandas uses `python -m build -Cbuilddir=builddir --no-isolation --wheel --outdir {build_cache_dir} {build_dir}` [src pandas asv_bench/asv.conf.json:41]. The persistent meson `builddir` in pandas is plausibly an incremental-compile aid [inf; the config does not say so].
- asv logic for a commit: check out the commit into the env's project dir, uninstall the previous build, **build only if the commit is not in the build cache**, then install the wheel [src asv/environment.py ~865-890: `get_cache_dir` / `create_cache_dir` / `_build_project`]. So asv builds once per new commit and never reuses a build across different commits.
- Cache: keyed by commit hash, keeps the latest `build_cache_size` items [src asv/build_cache.py:15-35; default 2 at :35]. Configured: numpy 8 [src numpy asv.conf.json:77], pandas 8 [src pandas asv.conf.json:36], scipy 10 [src scipy asv.conf.json:66]. Docs: number of builds to cache for each environment [src docs/source/asv.conf.json.rst:499-500].
- Environment types: numpy/scipy `virtualenv`, pandas `rattler` (conda-like) [src asv.conf.json files]. A dependency matrix (Cython, meson-python, ...) is installed per env [src same].
- `--python=same` / `existing:same` skips env creation and uses the current interpreter [src asv/commands/common_args.py ~240-270]. pandas CI uses this [src pandas pixi.toml `ci-asv`]; numpy CI calls `spin bench --quick`, whose asv flags are not visible because `.spin/cmds.py` is not in the sparse clone [unk]. In both, the project is built beforehand by its own tooling (`spin build`; `build-pandas --editable`) [src numpy linux.yml:~213-215; pandas code-checks.yml:~118-123], so asv does no per-commit build there.

## 3. Correctness tests per candidate
- asv is not a correctness tool. Benchmarks only need to run without exception; a failing benchmark is recorded as failed (None) and `_isna` treats that as failure in compare [src asv/commands/compare.py:72-74]. Correctness for PRs comes from separate pytest jobs [inf; not read here].
- `-b/--bench REGEX` selects a subset of benchmarks by regex [src asv/commands/common_args.py:147-150 `add_bench`]; the numpy README documents `asv run ... -b $REGEXP` and `spin bench -t bench_core` for subsets [src numpy benchmarks/README.rst:36-54]. The subset is chosen by the developer per invocation [src].

## 4. Performance measurement per candidate
**CI jobs (trigger and content)**
- numpy: job `benchmark` in `.github/workflows/linux.yml`, `if: github.event_name != 'push'` (so on every pull_request to main/maintenance/**, except paths-ignore docs/pyi), runs `asv machine --yes` then `spin bench --quick` [src numpy .github/workflows/linux.yml:197-226; triggers :8-19]. `--quick` = each benchmark function run once, results not saved [src asv/commands/run.py:138-146].
- pandas: job `asv-benchmarks` in `code-checks.yml` on push/PR to main [src pandas .github/workflows/code-checks.yml:98-130] after building pandas editable (`pixi run ... build-pandas --editable`), runs pixi task `ci-asv` = `asv machine --yes` then `python -W error -m asv run --quick --dry-run --launch-method=forkserver --durations=30 --python=same --show-stderr` [src pandas pixi.toml:310-332 `[tasks.ci-asv]`; code-checks.yml:~118-130]. Smoke only.
- scipy: no benchmark workflow in `.github/workflows/` (16 files listed, none benchmark-related); `benchmarks/asv.conf.json` appears only in CODEOWNERS [src scipy .github/CODEOWNERS:63]. Benchmarks run locally via `spin bench` [src scipy benchmarks/README.rst:22-49].
- None of the three triggers by label, and none runs `asv continuous` or `asv compare` on PRs [src: absent in workflow files grepped for asv/benchmark]. Any dedicated-machine nightly/regression bot is outside these repos [unk; looked in .github/ of all three]. numpy's `spin bench --compare <rev>` is the documented manual PR-vs-main comparison [src numpy benchmarks/README.rst:56-61].

**asv measurement mechanics (when run for real)**
- `rounds` default 2; `repeat` default `(1,5,10.0)` if rounds>1 else `(1,10,20.0)` (min, max, max seconds); final value is the **median** of all samples [src docs/source/benchmarks.rst:138-162]. `warmup_time` default 0.1 s [src benchmarks.rst:138-141]; `sample_time` default 10 ms, used to pick `number` [src benchmarks.rst:169-171]. Each benchmark is run in its own process [src docs/source/using.rst:248; writing_benchmarks.rst:131 (not benchmarks.rst)].
- Comparison: `asv compare` / `asv continuous` flag a benchmark when `a < b / factor`, default **factor 1.1** (10%) [src asv/commands/common_args.py:44-52; asv/commands/compare.py:77-100]. Before applying the factor, if both results have raw samples (and repeat != 1) it requires `_stats.is_different(...)` [src compare.py:84-98].
- `is_different`: Mann-Whitney U test with **p < 0.002**, applied only if the sample sizes can reach that p (`p_min = 1/binom(n_a+n_b, min)`); otherwise falls back to non-overlap of 99% confidence intervals [src asv/_stats.py:30-69]. `--no-stats` uses only factor and median [src common_args.py:54-61]. (There is no asv/statistics.py; the file is `_stats.py`.)
- `asv continuous` default baseline = parent of the tested commit [src asv/commands/continuous.py ~30-33]; it supports `--interleave-rounds` against ordering bias [src continuous.py ~46-60]. `step_detect.py` (Potts-model step detection) serves `asv publish` history regressions, not PR compare [src asv/step_detect.py:19-89 function names; usage by publish is [inf]].
- Noise controls: docs recommend `python -m pyperf system tune` and `--cpu-affinity` [src docs/source/tuning.rst:61-71]; numpy/pandas CI does not apply them (and with `--quick` nothing is compared) [inf].

## 5. Cost per candidate
Not reported in the repos [unk]. Structure: per commit = one wheel build (cached up to `build_cache_size`) + install + selected benchmarks x rounds x repeats. CI smoke runs avoid both via `--python=same --quick` [src above].

## 6. Iteration / cumulative re-validation
asv stores results per commit (`results_dir`), so a series can be compared and regression-searched later (`asv publish`; `regressions_first_commits` in pandas and scipy confs) [src pandas asv_bench/asv.conf.json:37; scipy benchmarks/asv.conf.json:87-89]. Cumulative checking is a post-merge or maintainer activity, not part of PR CI [inf; no such workflow in the clones].

## 7. Limitations the authors state
- `--quick`: results "unlikely to be useful" [src asv/commands/run.py:138-146 help text].
- numpy workaround comment: asv#1333 needs a pseudo-tty for `asv machine` [src numpy linux.yml:219-224].
- pandas: asv >=0.6.6 defaults to "spawn", which re-imports pandas per benchmark, hence forkserver [src pandas pixi.toml:~322-324 comment, GH#66193].

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- [src] asv already has "reduced build" in the weak sense: one wheel build per new commit, cached by commit hash (`build_cache_size` 8-10), plus `--python=same` to skip env creation. It does a full `python -m build` per new commit, not an edit-level incremental build (only pandas shares a meson builddir, [inf]).
- [src] asv has "reduced benchmark" via `-b REGEX`, but the subset is chosen by humans, not derived from the diff. No tool in these repos maps a diff to the benchmarks it can affect [unk].
- [src] Statistical gate: Mann-Whitney U p<0.002 plus factor 1.1 on medians; defaults rounds=2, repeat up to 5. The only PR-time benchmark jobs are smoke-only, so these projects do not confirm speed-up per PR in CI (section 4).
- [inf] A deterministic alternative (instruction counts, CodSpeed-style) is not used by these three; wall-clock asv is run manually where a speed-up is claimed.

## Sources
- asv @ 1f9db13: asv/commands/compare.py 70-100; asv/_stats.py 30-69; asv/build_cache.py 15-35; asv/environment.py 865-890, 935-955; asv/commands/common_args.py 42-61, 147-150, 240-270; asv/commands/continuous.py 30-60; asv/commands/run.py 136-146; docs/source/benchmarks.rst 131-171; docs/source/asv.conf.json.rst 499-500; docs/source/tuning.rst 61-71
- numpy @ e092b91: benchmarks/asv.conf.json; benchmarks/README.rst 29-61; .github/workflows/linux.yml 1-30, 190-226
- pandas @ ca8d2da: asv_bench/asv.conf.json; .github/workflows/code-checks.yml 1-25, 98-130; pixi.toml (raw fetch at that SHA)
- scipy @ 73d740c: benchmarks/asv.conf.json; benchmarks/README.rst; .github/CODEOWNERS:63; workflow directory listing
