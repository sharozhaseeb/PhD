# pyperformance / pyperf

Status: critic-checked 2026-11-21 (4 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/python/pyperformance @ 1c8098680463a139c3d3167551e7c6a147a9f335 (local: `C:\Users\pc\study\bt-lab\survey\python_pyperformance`); pyperf is a separate repo, cited via https://pyperf.readthedocs.io (latest; docs show no release number); pyperf source main @ aa51cd48a64052c7036b12676285d5bfb06b83da (2026-11-16) consulted for defaults (_runner.py: warmups=1, min_time=0.1, 20x3 non-JIT, 6x10 JIT; --fast = max(n//2,3) procs and max(v*2//3,2) values; --rigorous doubles processes) · Paper: none
Evidence labels: **[src]** read in source or docs (file/URL), **[inf]** inferred by us, **[unk]** not found.

## 1. What it is
pyperformance is the CPython benchmark suite (76 `bm_*` benchmark directories plus a MANIFEST file under `pyperformance/data-files/benchmarks` [src, ls]). It drives pyperf, which runs each benchmark in many worker processes and stores all values in JSON. It benchmarks interpreters/builds (baseline vs changed Python), not individual library patches.

## 2. Build / environment
- It does not build Python; the user supplies `baseline_python` and `changed_python` executables [src pyperformance/cli.py `--output` help text "Provide only baseline_python, not changed_python"; cli.py:~100-110].
- It creates a virtualenv per benchmark (or a common venv first) and installs pyperformance, pyperf and the benchmark requirements [src pyperformance/run.py:81-102 (venv creation prints), pyperformance/venv.py:213-250 `install_pyperformance`, `ensure_reqs`]. pyperformance pins deps; changing them changes the major version so results of different major versions are not comparable [src requirements.in:1-3].
- Nothing is reduced or incremental in the build; builds of CPython itself happen outside (e.g. the faster-cpython benchmarking infrastructure) [unk; not in this repo].

## 3. Correctness tests per candidate
None in pyperformance proper: it is a speed suite, benchmarks assert nothing about the interpreter other than running [inf]. Benchmark subset selection: `filter_opts` / `-b` style benchmark selection on the CLI [src cli.py:~137 `filter_opts(cmd)`; flag details not read] [inf].

## 4. Performance measurement per candidate
- pyperf defaults on CPython (no JIT): **20 processes x 3 values = 60 values, 1 warmup** per process; with JIT (PyPy) 6 x 10 with 10 warmups [src pyperf docs, runner.html "Runner CLI"]. One extra calibration process picks loops so that a value takes >=100 ms (`--min-time`, default 100 ms) [src pyperf docs run_benchmark.html, runner.html]. The first value per worker is skipped as warmup [src same].
- pyperformance passes through `--fast` (processes /2, values x0.6 -> 10 x 2), `--rigorous` (processes x2 -> 40 x 3), `--debug-single-value`, `--affinity`, `--min-time`, `--warmups`, `--same-loops FILE` (reuse loop counts from a previous run so no recalibration) [src pyperformance/cli.py:76-150; run.py:224-245 `get_pyperf_opts`; pyperf factor numbers from pyperf docs runner.html].
- Statistic and significance: `pyperformance compare` reports mean ratios and calls "Significant" only if |mean_a - mean_b| > 1% of the mean sum AND a **Student two-sample two-tailed t-test** at "alpha=0.95" passes (critical value from a t-table) [src pyperformance/compare.py:136-178: `is_significant`, `significant_msg`]. pyperf's own `compare_to` uses the same test (docs: "alpha equals to 0.95") [src pyperf docs analyze.html]. Differences <1% are always "Not significant" [src compare.py:~165-170]. Note: the code comment says alpha=0.95; reading it as a 95% confidence level (p<0.05) is our interpretation; neither code nor docs state a p threshold [inf].
- Noise controls: `--affinity` (pins workers to CPUs; by default uses isolated CPUs if they exist) [src pyperf runner.html]; `python -m pyperf system tune` sets CPU governor to performance, raises min frequency to max, stops irqbalance and sets IRQ affinity, lowers perf_event sample rate, and controls turbo boost; it does not set isolcpus or change ASLR (it only checks them) [src pyperf docs system.html]; the page does not say which IRQ affinity or turbo value `tune` writes [unk]. Separate processes with different random hash seeds/ASLR are the pyperf design for averaging out layout noise [inf; docs "20 processes" rationale not read in detail].

## 5. Cost per candidate
Default 21 process launches per benchmark (1 calibration + 20 workers) x ~3 values x >=100 ms x loops, times ~76 benchmarks, so on the order of tens of minutes to hours per interpreter [inf]. `--fast` roughly halves it [src above]. No cost figures in repo [unk].

## 6. Iteration / cumulative re-validation
Results are JSON files (`-o`, `--append`) compared offline via `pyperformance compare` [src cli.py:~110-125, 160-175]. Re-validation across many commits is done by external infrastructure [unk; not in this repo].

## 7. Limitations the authors state
- Results from different pyperformance major versions are not reliable to compare [src requirements.in:1-3].
- Variations under 1% are treated as noise by design [src compare.py comment ~165-168].

## 8. Relevance to Study 1
- [src] The speed-up gate is strictly statistical on wall-clock: t-test plus a 1% floor, on 60 values per benchmark. This costs 20 fresh processes per benchmark per side [src pyperf docs], i.e. the expensive end of the spectrum.
- [src] `--same-loops` and `--fast` are existing "reduce measurement" levers; calibration can be shared between baseline and candidate [src cli.py:~125-130].
- [inf] pyperf-style repeats give a defensible confidence story but are non-deterministic; a study that wants determinism must contrast with instruction counting (see codspeed.md).

## Sources
- pyperformance @ 1c80986: pyperformance/cli.py 70-175; pyperformance/compare.py 136-178; pyperformance/run.py 81-102, 215-245; pyperformance/venv.py 204-250; requirements.in 1-3; ls of data-files/benchmarks
- pyperf docs (fetched 2026-11-21): https://pyperf.readthedocs.io/en/latest/runner.html, run_benchmark.html, analyze.html, system.html
