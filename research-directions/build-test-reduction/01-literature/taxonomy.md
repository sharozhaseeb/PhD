# Taxonomy of reduction techniques

**Status:** draft v2 (critic fixes applied), 2026-11-21.

**Labels:** [R] read in source · [F] read through a web-fetch summary · [A] abstract only · [I] inferred · [U] unknown. Locations are in `review.md` and the `notes/` source cards.

**Overhead** means extra work the technique adds compared with running everything, as reported by its source. **Python support** means a tool or study that exists for Python today.

## Build

| Technique | What is reduced | Granularity | Safety assumption | Overhead (reported) | Python support |
|---|---|---|---|---|---|
| Timestamp rebuild (Make-style) | Targets whose inputs are newer | File/target | Declared deps complete; mtimes not tampered with [R mokhov2020buildsystems fn.5] | none | setuptools `build_ext` (sources + `depends` vs `.so`), Cython `cythonize` (.pyx/.pxd/include) [F] |
| Hash-based verifying traces (Shake, Bazel) | Tasks whose dependency hashes changed | Task/action | Deterministic tasks; deps tracked [R mokhov2020buildsystems §5.2, §8.3] | trace storage [U] | Only via Bazel rules [I] |
| Early cutoff | Dependents of an output that rebuilt byte-identical | Task | Output content hashes [R mokhov2020buildsystems §2.3] | none stated | Not in setuptools/Cython [I] |
| Remote / constructive cache (Bazel, CloudBuild) | Whole actions by cache hit | Action | Complete action key; hermetic tools [F bazel; R cloudbuild §3.4] | [U] | No native Python packaging support [I] |
| Traced / forward builds (Rattle, Kotinos) | Commands whose traced inputs are unchanged | Command/step | Complete tracing; graph structure unchanged [R spall2022forward §2; gallaba2020kotinos §4] | Kotinos: median CPU <1% [R]; ptrace 2× on a clean build [R licker2019incorrect] | Language-agnostic [I] |
| ccache / sccache | C compiler invocations | Translation unit | Hash covers flags, compiler identity, headers [F] | [U] | Usable for the C compile of extensions [I] |
| Rebuild-on-import editable install | Ninja incremental rebuild at import | Build target | Build dir and build deps present; new files need a reinstall [F meson-python] | "usually small" [F] | meson-python; scikit-build-core (experimental) [F] |
| Hash-based `.pyc` | Recompilation of bytecode | Module | Checked-hash mode verifies the source on import [F pep552] | Hash on import [U] | CPython native |

## Functional test selection

| Technique | What is reduced | Granularity | Safety assumption | Overhead (reported) | Python support |
|---|---|---|---|---|---|
| Safe modification-traversing RTS (Rothermel & Harrold) | Tests not traversing changed CFG edges | Statement/edge | Controlled regression testing; terminating, non-obsolete tests [R] | [U] | None [I] |
| Ekstazi (dynamic, file checksums) | Tests whose recorded files are unchanged | Class/file | Observed run covers dependencies; deterministic tests [R §3, §5] | End-to-end 68% of RetestAll; 46% for long suites [R §4.3] | Python analogue EkstaP saves 3.1% (eager imports) [R WangPradelLiu2026 §4.2] |
| Static class-level RTS (STARTS) | Tests not reaching changed types | Class | No reflection; libraries in the graph [R legunsen2016static §4.3] | 62.5–68.2% end-to-end [R]; ~81% [A STARTS] | None |
| Method-level static RTS | Tests not reaching changed methods by call graph | Method | Sound call graph | Unsafe in 10.6% of revisions [R legunsen2016static] | Python call graphs: PyCG recall 69.9% [F salis2021pycg] |
| Hybrid (HyRTS, GIBstazi) | Mixed | Method + file / module + class | Non-code changes fall back to coarser [R ShiZhaoMarinov2019 §I] | 76.0% total CI time [R] | None |
| pytest-testmon | Tests whose executed blocks are unchanged | Code block (function body) | coverage.py sees all relevant execution [F] | [U] | Native (Python ≥ 3.11 per PyPI) [F] |
| NameRTS | Tests not reaching changed names | Name/function; per test file | eval/exec not modelled; library callbacks not modelled [R §3.4, §5] | 10.04% of full-suite time; −45.6% end-to-end [R §4.3] | Native (preprint) |
| History windows (Google pre-submit) | Tests outside the failure/execution windows | Test suite | Recent history predicts failures [R Elbaum2014 §4.1] | Cheap, no coverage [R] | Implementable [I] |
| Prioritization (`--ff`, APFD-style) | Order only | Test | none (no test is dropped) | Small [I] | pytest cache [F] |

## Performance tests and benchmarks

| Technique | What is reduced | Granularity | Safety assumption | Overhead (reported) | Python support |
|---|---|---|---|---|---|
| Coverage-based benchmark prioritization (Laaber 2021) | Order (early stop possible) | Benchmark | Changes show up in benchmarks covering the change | 11% best [R] | None |
| History-based greedy order | Order | Benchmark | Past change frequency predicts the future | <1% [R laaber2022searchbased] | None |
| PerfRanker | Order plus extra repetitions on top-ranked tests | Test | Call-graph impact model; collection-intensive Java [R] | Reported, not extracted [U] | None |
| Perphecy / PerfScope / PRICE | Commits/tests skipped | Commit/test | Perphecy: details [U]; PerfScope: learned [A]; PRICE: evolved rules decay over time [A] | [U] | None |
| Reduced microbenchmark suite (Grambow) | Benchmarks dropped | Benchmark | Micro change maps to application change — found weak [R] | — | None |
| Dynamic reconfiguration (CV/RCIW/KLD) | Iterations/forks stopped early | Run of one benchmark | Steady state reachable; stability means correctness [A laaber2020dynamic; R traini2023steady] | 48–86% time saved [A] | None packaged [U] |
| µOpTime | Repetitions fixed from an old full run | Benchmark | Old run representative [R] | Median 13–77% saved; 3/29 false positives, 2/7 false negatives [R] | None |
| Duet / interleaved A/B (RMIT) | Variance, hence repetitions | Pair | Interference shared by both versions [R bulej2020duet §4.2] | — | asv `--interleave-rounds` [F] |
| Instruction-count simulation (CodSpeed) | Noise (deterministic count) | Benchmark | I/O and system calls excluded; model fidelity [F] | Single run [F] | pytest-codspeed [F] |
| Change-point detection (MongoDB, Hunter) | Analysis of a series, not runs | Metric time series | Noise model; Hunter is deterministic via t-test [R] | — | Hunter is open source [R] |

## CI scheduling

| Technique | What is reduced | Granularity | Safety assumption | Overhead (reported) | Python support |
|---|---|---|---|---|---|
| Constant batch + bisection | Runs per commit | Batch of n commits | Low culprit/flake rate; single culprit; monotone [R najafi2019bisecting] | 2·log2(n)+1 per failing batch [R] | git bisect, `asv find` [F] |
| Risk-ordered batching (TopK) | Bisection steps | Commit | Risk model ranks culprits [R] | 7.6–9.0% fewer runs [R] | — |
| Milestones (Google TAP) | Per-change runs | Milestone (~45 min) | Reverse dependencies complete [R memon2017taming] | — | — |
| Flake-aware culprit finding | Reruns during bisection | Commit | Flake rate estimated [R henderson2023flake] | Log best case [R] | — |
| Delta debugging | Probe count for interacting changes | Change subset | Monotone, consistent configurations [R zeller1999yesterday] | Up to about quadratic in the number of changes [R zeller2002simplifying] | — |
| CI skip rules | Whole builds | Commit | Rules identify no-risk commits — violated in practice [F jin2021helped] | 18% fewer CI-triggering commits [A abdalkareem2021ciskip]; median 21% build time saved [F jin2021helped] | — |
| Periodic full run (Meta master, Google, Grambow daily) | Nothing per change; catches misses later | Time window | — | — | — |
