# (d) Repeated FULL networkx passes with machine telemetry — pre-registered plan (frozen before measurement, 2026-11-22 15:32 PKT)

**Why:** R1's benchmark cost is a range from single passes under drifting machine states (N7). Advisor E6, TPM (d). **No root-cause hunting:** descriptive only.

**Design:**
- State S0 `181f2951`, one clean clone. **3 FULL passes**: all 171 time cases, 2 processes × 3 values (the RQ1 FULL protocol), CPUs 2–5.
- **Canary** before pass 0, between passes and after pass 2 (4 canaries): `GraphBenchmark.time_to_undirected('DiGraph')`, `GraphBenchmark.time_add_edges_from('MultiDiGraph')` (cheap) and `UndirectedAlgorithmBenchmarks.time_connected_components('Erdos Renyi (100, 0.9)')` (a `benchmark_algorithms` case: its per-process setup is what drifted). All three have A/A σ.
- **Telemetry** (`results/raw/telemetry/`) throughout, read-only.

**Reported (frozen in `scripts/night_analyse.py`):**
- Per pass: the sum of run wall times, the split between `benchmark_algorithms` and the other modules, the M5 label.
- Per canary: wall time per case.
- Per block: Windows CPU mean and max, `% Processor Performance` mean and min, WSL load mean and max.
- **R1 update:** the range of FULL-pass totals over these 3 passes, next to the earlier measured passes (659–2444 s). The paper reports a range over n passes, never one pass.
- **Not claimed:** any cause of drift.

**Stopping:** cap 2.5 h (PM), checkpointed, stall guard 450 s. **Estimate:** 3 × (659–2444 s) + 4 canaries (≈ 1–3 min each) ≈ 35–125 min.
