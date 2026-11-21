# CodSpeed (pytest-codspeed)

Status: critic-checked 2026-11-21 (9 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/CodSpeedHQ/pytest-codspeed @ 15d46b4f01dc52edab2345e8d9d2820b704d7bdf (local: `C:\Users\pc\study\bt-lab\survey\CodSpeedHQ_pytest-codspeed`) · Docs: pages fetched directly 2026-11-21 via a summarising fetch tool: https://codspeed.io/docs/instruments/cpu, /docs/features/customization.md, /docs/features/understanding-the-metrics.md, /docs/features/performance-checks (earlier 404s were wrong URLs; `.md` suffix works)
Evidence labels: **[src]** read in source or docs, **[inf]** inferred by us, **[unk]** not found.

## 1. What it is
A pytest plugin plus a hosted service. Benchmarks are ordinary pytest tests (`@pytest.mark.benchmark` or the `benchmark` fixture) executed under `--codspeed` by the CodSpeed GitHub Action, which uploads results and compares PR vs base [src README.md:~30-135].

## 2. Build / environment
- The plugin does no build; the user installs dependencies in CI, then the Action wraps `pytest tests/ --codspeed` [src README.md:~95-135 example workflow; .github/workflows/codspeed.yml:35-44].
- No incremental or reduced build in the plugin [src: none present]. Build reduction is the project's own concern [inf].

## 3. Correctness tests per candidate
- Benchmarks are pytest tests, so a benchmark also asserts correctness of its output (README example asserts `output == 55`) [src README.md:~40-50]. The Action runs only the command the user gives; subset selection is by pytest path/markers/test-group sharding [src codspeed.yml:~38 `--test-group=${{ matrix.shard }} --test-group-count=${{ env.SHARDS }}`]. Nothing selects benchmarks from the diff [unk; searched plugin.py and docs summaries].
- With `--codspeed` only benchmark-marked tests are run as benchmarks; pytest-benchmark is blocked [src plugin.py:141-168 (enable flag, blocks pytest-benchmark/pytest-speed); which tests are run as benchmarks is decided in `pytest_collection_modifyitems` ~257 / `should_benchmark_item` ~321, not read in detail: [inf]].

## 4. Performance measurement per candidate
Three modes, `MeasurementMode` = simulation, walltime, memory [src instruments/__init__.py:58-77; plugin.py:145-156]. In CodSpeed CI (`CODSPEED_ENV` set) the default is simulation unless `CODSPEED_RUNNER_MODE` is walltime/memory; locally the default is walltime [src plugin.py:145-156].
- **Simulation (formerly "instrumentation")**: the plugin loads `InstrumentHooks`, calls `start_benchmark`, `callgrind_start_instrumentation`, runs the function, then stops (with perf-trampoline support it first calls the function once as a cache warmup, so it executes twice but measures once [src analysis.py:75-77]); measurement is done by CodSpeed's Valgrind (callgrind) fork outside the plugin [src instruments/analysis.py:58-91]. The function is run once (or a few warmup rounds with `pedantic`) [src analysis.py:93-143 `measure_pedantic`: warmup_rounds, rounds/iterations ignored with a warning; docs cpu page "run once"]. Docs: the model counts executed instruction cycles weighted per instruction plus L1 and last-level cache-miss penalties (about 10-40 and 100+ cycles), converts cycles to time with a constant frequency, excludes system calls, does not follow child processes, no statically linked executables [src docs cpu page: weights, 10-40 / 100+ cycle penalties, constant frequency, syscalls excluded, run once; "does not follow child processes" and "no statically linked executables" NOT found on that page: [unk]]. This is deterministic by construction and hardware-independent [src cpu page says hardware-agnostic; no formal determinism claim; determinism of Python-level runs given hash seeds / ASLR is [inf, not verified]].
- **Walltime**: on CodSpeed Macro runners (`runs-on: codspeed-macro`) [src codspeed.yml:~24 `runs-on: ... 'codspeed-macro'`]. Plugin loop: warmup 1 s (`DEFAULT_WARMUP_TIME_NS`), then rounds sized so each round >= timer resolution x 1e6 ns, total <= `max_time` default 3 s, `max_rounds` optional; reports best time, relative stddev, IQR/stdev outlier counts [src instruments/walltime.py:30-75, 205-240; README table].
- Regression decision: baseline = latest base-branch commit with a CodSpeed run (merge-commit logic for `pull_request`); **default regression threshold 10%**, changeable in repo Settings, per-benchmark override from the benchmark's dashboard page [src docs customization.md; the "0-50%" range is not on the page: [unk]]. Impact = relative speed change vs baseline; commit-level impact is a geometric mean of changed benchmarks [src docs understanding-the-metrics.md]. No statistical test is described [src], consistent with the deterministic mode [inf]. That a breach fails the status check is not stated on the performance-checks page [unk].
- Per-PR trigger: user-defined; README recommends `on: push main` + `pull_request` so every PR runs the whole configured benchmark job; `workflow_dispatch` for backtests [src README.md:~100-112]. CodSpeed repo itself shards benchmarks 4 ways (`SHARDS: 4`) x 3 modes (simulation, walltime, memory); triggers push/PR on master and workflow_dispatch [src codspeed.yml:2-9, 18-39].

## 5. Cost per candidate
Simulation mode runs each benchmark once under Valgrind (slowdown factor not stated in sources read) [unk]. Walltime default <= 4 s per benchmark (1 s warmup + 3 s max) [src walltime.py:30-31].

## 6. Iteration / cumulative re-validation
Every push to the default branch is also benchmarked, which provides the baselines for later PRs and a history chart [src README.md workflow; docs summary]. This is the cumulative record; there is no batched re-validation logic in the plugin [inf].

## 7. Limitations the authors state
- Simulation excludes syscalls, child processes and static executables [docs: syscalls confirmed on cpu page; child processes and static executables [unk]]. Perf-trampoline support enables the call graph (analysis.py:46) and also triggers the extra warmup call (analysis.py:75-77).
- Baseline exists only if base branch already has runs [src docs understanding-the-metrics.md].

## 8. Relevance to Study 1
- [src] Closest existing system to a deterministic speed oracle: instruction + simulated-cache cost from callgrind with single execution, no repeats or noise tests, threshold 10%.
- [src] It measures only the benchmarks the user wrote; no diff-to-benchmark selection (unk).
- [inf] Cost-effective for per-edit use: one run per benchmark and deterministic, but cycle model is a proxy; results for C-extension/IO/syscall-heavy code may not track wall time (docs exclude syscalls).

## Sources
- pytest-codspeed @ 15d46b4: README.md 30-135; src/pytest_codspeed/plugin.py 72-160; instruments/__init__.py 58-77; instruments/analysis.py 22-139; instruments/walltime.py 30-75, 158-240; .github/workflows/codspeed.yml
- Docs fetched via summarising tool 2026-11-21: https://codspeed.io/docs/instruments/cpu, https://codspeed.io/docs/features/customization.md, https://codspeed.io/docs/features/understanding-the-metrics.md, https://codspeed.io/docs/features/performance-checks
