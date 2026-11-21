# SWE-Opt

Status: critic-checked 2026-11-21 (9 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/SWE-Opt/SWE-Opt @ 48fa73e84b369d84c32290ab8d1c7ba0a800308a (main, pushed 2026-10-22; no local clone) · Paper: arXiv 2606.25530v2 (Sarikayak, Gu, Ghonim, Chen), "SWE-Opt: A Benchmark for Evaluating LLMs on Performance-Oriented Repository-Level Optimization". Critic re-read the full arXiv HTML (v2, 31 Oct 2026) and the repo files named below @48fa73e (HEAD of main on 2026-11-21).
Evidence labels: **[src]**, **[inf]**, **[unk]**.

## 1. What it is
102 expert-written optimizations (pandas, scikit-learn, xarray) with parameterized scenario tests for runtime, peak memory and time-weighted memory (TWMU). LLMs show sparse runtime gains and almost no memory gains. [src abstract, 2.2]
Note: the earlier discovery log said "slides only"; a full paper and repo now exist.

## 2. Build / environment
- Baseline and optimized states built in isolated Docker images matching the target commit; images built once, stored in a registry, referenced by immutable tags/digests. [src 2.2; App. E summary]
- Repo has docker/Dockerfile.pandas|sklearn|xarray; the pandas image installs meson-python, ninja, pytest-json-report, coverage and clones the repo at ARG SHA (per-build layers). [src repo @48fa73e]
- Patch flow for LLM runs: the baseline image is reused; the patch is applied INSIDE the running container by apply_patch(), then correctness, then perf. container_entrypoint.py contains no rebuild/pip/meson call [src container_entrypoint.py L100-165, grep]. The pandas image installs the repo editable (meson-python editable install or setup.py develop by commit date) [src docker/Dockerfile.pandas], so whether compiled-extension edits are rebuilt depends on editable-install behavior: [unk], not tested. Paper: "Rather than rebuilding environments during benchmarking", pre-built images are used. [src App. E.6]

## 3. Correctness tests per candidate
- Unit tests tied to the target function, median 10 per instance, fixed at curation; a patch is correct only if all pass. [src 2.2, 3.1, Table 2]
- Runner executes a predefined list of pytest nodeids with pytest-json-report; exit code 0/1/other = passed/test_failed/run_failed. [src swe_opt/harness/evaluation/correctness_test_runner.py L25-27, L59-60, L72-80]
- Fixed per task (core_tests list from the dataset row), not per edit. Performance is scored only for patches that apply and pass. [src 3.1; run_evaluation.py L229; container_entrypoint.py]
- If correctness fails, perf is skipped; if a perf sweep raises PerfTestFailedError, is_correct is overwritten to False ("Code is broken on edge cases"). So perf workloads also act as extra correctness checks. [src container_entrypoint.py L156-182]

## 4. Performance measurement per candidate
- Scenario: setup(), optional warmup(), run(); Cartesian product of params, cap 24 workloads (median 6); fixed seed 42. [src 2.3, config/config.yaml]
- config/config.yaml: warmup 5-12 calls, window 4, CV < 0.08 (L16-19); 5-15 samples, 30 s budget, rciw_threshold 0.1 (L26-29); MAD cleaning k=3.5 (L51-54); snr_threshold 2.0, max_total_system_noise_pct 20.0, min_practical_effect_pct 5.0 (L56-61). [src]
- IMPORTANT role of each number: rciw_threshold 0.1 (RCIW = 2*1.96*std/sqrt(n)/mean <= 10%) is the ADAPTIVE-SAMPLING STOP rule, required on runtime, TWMU and peak memory [src utils/measurement_utils.py L396-448; paper App. E.4]. It is NOT the per-workload acceptance gate. The report-time gates (report_analyzer.py, header L335-345): within-run RCIW of baseline and target must be <= 20% ("noise ceiling"), then SNR = |change_pct| / max noise-% must be >= 2.0, then |change_pct| >= 5%; only then "improved"/"regressed" [src report_analyzer.py L335-345, L436-445, L490-520]. The paper text says only "RCIW" and "SNR threshold of 2" and does not state the 20% ceiling or 5% effect floor. [src 2.4, E.5]
- Multiple fresh containers per workload; the count of containers is not stated in the files read. [src 2.4; unk count]
- Noise control: container pinned to one core (cpuset=2) and memory node 0 (cpuset_mems=0), 30 GB limit, OMP/OPENBLAS/MKL/NUMEXPR/VECLIB/BLIS threads = 1, PYTHONHASHSEED=0; host a MacBook Pro Apple M4 Max (10P+4E cores, 36 GB), Docker on that host. [src config.yaml L68-82; paper App. E.6]
- Aggregation: harmonic mean over workloads per PR, arithmetic mean across PRs. [src 3.1]
- Only results passing stability (RCIW) and detectability (SNR) gates are reported; PR classes: not measurable / no signal / improved / regressed / conflicting. [src 2.4, E.5]

## 5. Cost per candidate
[unk] not reported.

## 6. Iteration / cumulative re-validation
Agent = OpenCode, 50 steps max, web tools off, parameterized perf tests and reference patches hidden; final repo state extracted as one git patch and evaluated once. The agent can run commands in its own container, but no harness in-loop re-validation is described. [src 3.1]

## 7. Limitations the authors state
Python data-science libraries only; perf-labelled PRs only; may not transfer to low-level, I/O-bound or non-Python code. [src Sec. 6]

## 8. Relevance to Study 1
- Best-specified noise protocol of the four (adaptive RCIW<=10% sampling, then 20% noise ceiling, SNR>=2 and 5% effect gates, single-core pinning): a template for "is this speed-up real". No formal hypothesis test (no p-value); decisions are threshold-based on medians. [src config.yaml, report_analyzer.py]
- Fixed per-task test list; no per-edit selection or incremental build. [src/inf]
- Wall-time on a laptop host, not deterministic counting. [src+inf]

## Sources
- Repo @48fa73e: config/config.yaml, harness/evaluation/correctness_test_runner.py, harness/evaluation/report_analyzer.py, harness/container_entrypoint.py, harness/run_evaluation.py, utils/measurement_utils.py, docker/Dockerfile.pandas, tree listing.
- Paper Sec. 2.2-2.4, 3.1, 6, App. D-E (full text read by critic).
