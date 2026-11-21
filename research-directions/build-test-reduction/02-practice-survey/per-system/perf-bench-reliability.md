# Performance-benchmark reliability audit (Chen et al.)

Status: critic-checked 2026-11-21 (5 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/chenzhi-cz/performance-optimization-benchmark-reliability @ 44a1cb86a9f765b0375b4cfb479641f3c19f0774 (main; data CSVs + README only, no harness code; no local clone) · Paper: arXiv 2607.01211v2, "Are Performance-Optimization Benchmarks Reliably Measuring Coding Agents?" (Chen, Sun, Shi, Lo, Jiang). Critic re-read the full arXiv HTML text (v2, 16 Jul 2026) and the repo's data/cross_machine_benchmark_summary.csv @ 44a1cb8 (HEAD of main on 2026-11-21); all headline counts match.
Evidence labels: **[src]** read in source, **[inf]** inferred, **[unk]** not found.

## 1. What it is
An audit, not a system. Replays official reference patches of GSO (102 tasks), SWE-Perf (140), SWE-fficiency (498) = 740 patches on 4 GCP profiles (n2, n2d, n4, n4d-standard-64; 64 vCPU/256 GB), 3 rounds each = 12 machine-round replays (one replay per machine-round; each benchmark's own internal repeats/workloads are reused unchanged), then re-checks each benchmark's own validity rule. A task counts as valid only if it passes in ALL 12 replays (Sec. VII calls this conservative). [src Sec. III-A, Table II, Fig. 1, Sec. VII]

## 2. Build / environment
- Uses each benchmark's own images; latest public repo version before 2026-04-30. [src III-A]
- Failures: missing external data, missing image deps, image-decoding failure, x86_64 CPU-instruction portability issue. [src III-B]
- Build reduction/caching: [unk] not discussed.

## 3. Correctness tests per candidate
- Audited rules: GSO equivalence checks; SWE-Perf efficiency unit test on both commits; SWE-fficiency correctness guards. All fixed per task. [src Table III]
- Not a selection study. [inf]

## 4. Performance measurement (audited rules, Table III)
- GSO: each selected generated test passes equivalence and keeps speedup >= 1.2x over base; 1.1x fallback for low-test tasks (CSV: <=5 selected tests). [src Table III; repo CSV]
- SWE-Perf: each efficiency unit test passes on both commits; 20 timing repeats, IQR outlier filter, Mann-Whitney min-gain delta_i > 0.05. [src Table III]
- SWE-fficiency: workload and correctness guards run; base mean workload time minus patched mean > 2x post-edit std. [src Table III]
- Noise (within-task std over 12 replays): GSO median 3.81 pp; SWE-Perf 1.41 pp; SWE-fficiency 2.41 pp. [src Table V]
- SWE-Perf is a small-signal problem: 101/138 tasks have median change within 5 pp of zero. [src III-D]
- Reference-patch validity (denominator = official task count; not-evaluable tasks count as failing): faster-than-base in every replay 91/102 GSO, 48/140 SWE-Perf, 470/498 SWE-fficiency; original-rule valid in every one of the 12 replays 39/102, 11/140, 411/498 (= 39+411 = 450 replay-valid tasks used in RQ3). Not evaluable at all: 4 GSO, 2 SWE-Perf, 0 SWE-fficiency. [src III-B, III-C, abstract; repo CSV]
- Table V noise is the within-task std of runtime change over the 12 replays, computed on 98 GSO / 138 SWE-Perf / 498 SWE-fficiency tasks; median reference change -54.20% / -0.03% / -56.04%. [src Table V]

## 5. Cost per candidate
[unk] not reported.

## 6. Iteration / cumulative re-validation
Not applicable (reference patches only). Leaderboard check: across 10 public (OpenHands-based) submissions per task, on the 450 replay-valid GSO+SWE-fficiency tasks all have a passing patch, 449 have one that beats base, 384 have one that matches/beats the reference. [src Sec. V-A]

## 7. Limitations the authors state
Threats (Sec. VII): replay/recomputation may be affected by implementation choices, hardware variation and artifact quality; all-12-replays rule is conservative; results cover three benchmarks and specific leaderboard snapshots; SWE-Perf excluded from RQ2/RQ3 for lack of public agent outputs. [src VII]
Recommendations are qualitative: future benchmarks should validate that workloads stress the optimized path and that reference patches have clear margin over noise [src III-E]; users should separate cross-machine-verified from unstable tasks and show per-task score weight [src VI]; designers should add validation against workloads not fully visible during search and resource metrics beyond runtime [src VI]. The paper recommends NO concrete repeat count, statistic or test. [src, absence checked in full text]

## 8. Relevance to Study 1
- Strong motivation: a speed-up verdict from one machine or run is unstable; "accept edit" needs margin over measured noise. [src+inf]
- The paper does not argue for instruction counts; any such conclusion is the survey's own inference. [inf]
- No per-edit selection or cumulative check. [src]

## Sources
- arxiv.org/html/2607.01211v2 (Sec. I, III-A..E, V, VI, Tables II-V; via summarising fetch)
- GitHub README.md and tree @ 44a1cb8; data/cross_machine_benchmark_summary.csv opened by critic (counts match paper)
