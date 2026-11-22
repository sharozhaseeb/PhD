# (c) FULL asv benchmark passes for bottleneck — pre-registered plan (frozen before measurement, 2026-11-22 15:32 PKT)

**Why:** R1 second-project row (C extension). TPM (c), advisor E4 (limited form).

**Design:**
- State: the amended base `f51ed862`, in a dedicated clone `~/bt-lab/exp/work/bn-bench`, clean build with the `bn38` venv (`setup.py build_ext --inplace`, done in prep: `prep-build.log`, `prep.json`).
- Discovery found **840 time cases** (move 280, nonreduce 8, nonreduce_axis 60, reduce 492) and 1 `peakmem` case (not timed).
- **2 FULL passes**, all 840 time cases, 2 processes × 3 values, CPUs 2–5, the same harness and per-run gate as networkx.

**Reported:** per pass, the sum of run wall times and per module, and the M5 label. Compared with clean build 4.7–5.4 s and full tests ≈ 24 s (results.md RQ1), this gives benchmarks / (build + tests) for bottleneck. One state and two passes: a cost row, not a detection result.

**Stopping:** cap 40 min (PM), checkpointed, stall guard 300 s. Pass 1 starts only after pass 0 has finished. If the cap cuts pass 1, pass 0 is the result, and pass 1 is reported as partial.

**Estimate (unknown):** ≈ 1.2 s per run (two worker processes, each importing numpy and bottleneck, plus timing) × 840 ≈ 17 min per pass, so ≈ 35 min for both. Nothing from bottleneck has been timed under asv yet, so this is a guess.
