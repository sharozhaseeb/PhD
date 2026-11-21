# SysLLMatic

Status: critic-checked 2026-11-21 (12 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/sysllmatic/sysllmatic @ fd59fa4deed3595a543892279f5dc656d75d1125 (main, 2026-03-26; local clone `C:\Users\pc\study\bt-lab\survey\sysllmatic_sysllmatic`, HEAD verified; its working tree is empty/staged-deleted, so files were read with `git show HEAD:<path>`) · Paper: https://arxiv.org/abs/2506.01249 (v2; critic re-read the full PDF text)
Evidence labels: **[src]**, **[inf]**, **[unk]**. Line numbers below are file lines at fd59fa4. Paper section numbers are from the PDF text (v2).

## 1. What it is
Pipeline: 43-pattern optimization catalog + profiler hotspots + iterative "Diagnosis Cycle" LLM refinement; evaluated on HumanEval-C++, SciMark2 (Java), five DaCapo Java apps (BioJava, Fop, PMD, GraphChi, ZXing). [src] paper abstract, §6.2; `README.md` (43 patterns).
Unit of optimization on DaCapo is one source class (`--method_level` defaults to False; the paper adopts class level, §7.4.3). A "program" in the main loop is one class from the top-50 profiler hotspots (`get_hotspots(..., top_K=50)`). [src] `src/main.py` 37-69, `src/benchmarks/dacapo/dacapo_benchmark.py` 264; paper §6.4.1, §7.

## 2. Build / environment
- Each candidate is written over the class's source file, then `sudo make compile BENCHMARK=<app>` is run in the app's module build directory (BioJava: the per-module `biojava-<group>` dir; Fop: `fop-core`). [src] `dacapo_benchmark.py` 109-133; `dacapo_apps.py` 60-62, 100-102.
- What `make compile` actually runs (Maven, incremental or not, offline or not) is [unk]: the Makefile is copied from `benchmark_dacapo/benchmarks/bms/makefile_template.mak` (`dacapo_benchmark.py` 303-306) and that file is not in the repo at fd59fa4 (`git ls-tree` finds only `benchmark_human_eval/makefile_template.mak` and an eval copy). The paper (§6.2.2) says the 5 apps use Maven. [src] paper; build command [unk].
- The app is first built with `ant <app>` under Java 8 (`get_app(check=True)` -> `_build_app`). [src] `dacapo_apps.py` 227-250, 257-261. README says to prebuild per the DaCapo instructions. [src] README.
- C++ (HumanEval) baseline compile is gcc -O3. [src] paper §6.4.2.
- Incremental build reuse beyond the above: [unk].

## 3. Correctness tests per candidate
- Paper: code is correct if it "compiles and passes all test cases" of the benchmark: HumanEval avg 9.6 tests; SciMark2 output quality threshold; DaCapo JUnit with JaCoCo coverage; classes without dedicated tests are skipped. [src] paper §5.6.3.
- Code, DaCapo: per candidate, run `make test BENCHMARK=<app> TEST=<t>` once per test in `self.unit_tests`; stop at the first failing test. [src] `dacapo_benchmark.py` 138-167.
- Who picks the tests: `find_unit_test` returns every `*.java` under the app's test root whose text contains the target class name and has an uncommented test (a textual match, not coverage). [src] `src/flamegraph_profiling.py` 175-199 (`contains_uncommented_test` at 147). So selection is per target class, computed once when the hotspots are listed (`dacapo_benchmark.py` 285), then identical for every candidate of that class. Not per edit. [src]
- Order per candidate: compile -> tests -> measure; compile or test failure skips measurement. [src] `src/benchmarks/benchmark.py` 80-89.
- Coverage is weak: avg instruction coverage 59.4%, GraphChi about 10%, ZXing about 94% (the Table 3 caption says 90%, the text says "nearly 94%"). [src] paper §5.6.3, Table 3.
- Passing-but-wrong cases found by manual review: 1 of 145 correct HumanEval programs had its core function removed yet passed; PMD output had 2 of 601 files mismatching the ground truth. [src] paper §7.1.4. Separately §8.2.1 says some optimized programs passed all tests but failed output validation because of parallelism-induced nondeterminism and races. [src] paper §8.2.1. (Researcher cited §5.6.3/Table 3/threats for these; wrong sections.)

## 4. Performance measurement per candidate
- Paper: 2 warm-up + 5 measured runs, average of the 5; dedicated bare-metal Intel Xeon W-2295 (36 CPUs, 188 GB); `perf stat -e cycles`, `/usr/bin/time` peak RSS, RAPL energy. [src] paper §6.4.1, §6.3, §6.7, §9.
- Code, DaCapo: the per-candidate perf run is `sudo make measure TEST=<self.unit_tests[0]>` with a 120 s timeout, i.e. the FIRST discovered unit test of the class is the workload, not the DaCapo application workload. [src] `dacapo_benchmark.py` 189-203. `_compute_avg` averages rows 0-4 of `java.csv` and reads row 5 as throughput. [src] `dacapo_benchmark.py` 205-226. What `make measure` runs is [unk] (template missing).
- The repo's C measurer `MEASURE/main.c` at this commit has `WARMUP_RUNS 10`, `ntimes = 20`, and a hard-coded path `/home/hpeng/E2COOL/src/runtime_logs/`; it does not match the paper's 2+5 protocol. Whether DaCapo candidates use it is [unk]. [src] `MEASURE/main.c` 11, 15, 31. `dacapo_apps.py` 253 sets `RAPL_TOOL = MEASURE/main` for the whole-app run path.
- Profilers: async-profiler (Java), Linux perf (C++). [src] paper §5.6.2.
- Reporting threshold: "Percentage Optimized" counts programs with >= 10% relative improvement; this is a reporting metric, not an acceptance rule. [src] paper §6.3, Table 5. No statistical test. [src]
- Code: there is NO performance acceptance gate. `static_analysis` returns `PERFORMANCE_IMPROVED` or `ALL_TEST_PASSED` whenever compile and tests pass, and the main loop treats both as success; a slower candidate still becomes `last_working_optimized_code`. [src] `benchmark.py` 80-89; `src/main.py` 219-234; `status.py`. The result written is the iteration with the best speed-up among those measured (`max_avg_speedup`), which need not be the code left on disk. [src] `dacapo_benchmark.py` 234-246; `main.py` 80-98. [inf] for the on-disk mismatch.

## 5. Cost per candidate
- No per-candidate cost in the code; DaCapo wall time is logged only per whole run (`main.py` 270-278). [src] Paper reports end-to-end time including build and test execution per application: GraphChi 11 min (18 queries), PMD 45 (65), BioJava 47 (54), ZXing 90 (60), Fop 206 (116); the authors say build and test overhead can dominate. [src] paper §7.5.1, Table 12.

## 6. Iteration / cumulative re-validation
- Iteration budget: `--self_optimization_step` default 2 = number of SUCCESSFUL (compile+tests) iterations per class; paper T=2 ("one round of feedback"). Up to 3 error-repair attempts, then re-optimize from the last working version; after 2 such failures the class is abandoned and, on DaCapo, the last working code is restored. [src] `main.py` 29, 167-182, 219-242; paper §6.4.1.
- Accepted code stays in the source tree, so edits to later classes build on earlier ones (accumulating). [src] `dacapo_benchmark.py` 119-120 (writes in place); `main.py` 233. [inf] that each later class is compiled and tested against the already-modified tree.
- Paper claims a final check: Algorithm 1 lines 19-21 (return A*; BuildAndRun(A*); Measure(A*, M)) "Verify final optimized application builds and runs". [src] paper Algorithm 1 (p.12; the researcher's "l.14-23" was wrong, the algorithm has 21 lines).
- In the artifact code the final whole-app rebuild/re-measure is NOT in the pipeline: `main()` ends after `master_script`; `run_app_and_measure` is imported (`dacapo_benchmark.py` 13) but has no call site (git grep over `src` and `eval`). The whole-app numbers in `eval/EQ1/dacapo/data/` may come from separate runs, but no script that produces them is in the repo. [src] absence; [unk] how final numbers were produced. Cumulative re-validation of all accepted class edits together with the full test suite: [unk] (neither paper nor code states a full-suite run).

## 7. Limitations stated
- Test coverage limits correctness; test validation is questionable at scale and "decomposing into smaller patches" is suggested. [src] paper §8.2.1.
- Only 5 of 22 DaCapo apps (Maven ones; 20 build, 8 have source+tests); files > 1,000 lines skipped (Fop 11%); context loss on long files. [src] paper §6.2.2.
- Controlled pipeline rather than autonomous agent. [src] paper §3.2.
- Temperature 0.7 so non-deterministic; pass@1. [src] paper §6.4.1, §9.

## 8. Relevance to Study 1
- [src] Multi-file, build-requiring (Maven/Java) optimization with accumulated in-place edits: closest to "build + test per edit" among the discovered systems. Test set is per target class by textual name match; one test as the perf workload.
- [src] Measured evidence that test-suite validation misses wrong edits when coverage is low (§7.1.4, §8.2.1) -> risk of reducing tests further.
- [src] No perf-based acceptance of a candidate in code: speed is measured only as feedback to the LLM, so Study 1's acceptance rule has no counterpart here.
- [inf] Hardware-counter measurement (RAPL/perf cycles) is an alternative noise strategy.

## Sources
- arXiv 2506.01249v2 full PDF text: §3.2, §5.5-5.6, §6.1-6.7, §7.1.4, §7.4.3, §7.5.1, §8.2.1, §9, Algorithm 1, Tables 3, 5, 12.
- Repo @ fd59fa4 via `git show HEAD:`: `src/main.py`, `src/benchmarks/benchmark.py`, `src/benchmarks/dacapo/dacapo_benchmark.py`, `dacapo_apps.py`, `src/flamegraph_profiling.py`, `src/status.py`, `MEASURE/main.c`, `README.md`. Not read: `humaneval_benchmark.py`/`scimark_benchmark.py` internals, `llm/*`, `eval/` scripts (only listed).
