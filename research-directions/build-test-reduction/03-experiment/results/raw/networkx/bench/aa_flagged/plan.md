# (b) σ_noise for the 12 flagged verdicts — pre-registered plan (frozen before measurement, 2026-11-22 15:32 PKT)

**Why:** the pre-registered rule (readiness §4.2, §5; rules.md §5) needs ratio > 1 + 3·σ_noise(b) for a regression verdict. σ exists for none of the 12 flagged cases (deviation N8). Advisor E2, TPM (b).

**Cases (12), each A/A at its verdict's own state and in its verdict's protocol:**

| Block | Verdict | State | Cases | Protocol |
|---|---|---|---|---|
| s02 | slowdown #2 (`_dijkstra_multisource`) | `d3d79cc8` | 9: the 8 `UndirectedGraphAtlasSevenNodesConnected` multi-source cases + `NonNeighbors.time_complete(100)` | 2 processes × 3 values |
| s08 | slowdown #8 | `52b7255a` | `ManyComponentsBenchmark.time_single_source_all_shortest_paths` | 2 × 3 |
| s01 | slowdown #1 | `867fda8d` | `UndirectedAlgorithmBenchmarks.time_connected_components('Erdos Renyi (100, 0.1)')` | 2 × 3 |
| s09 | spot check #9 | `b85a9986` | `UndirectedAlgorithmBenchmarks.time_louvain_communities('Erdos Renyi (100, 0.9)')` | 5 × 3 |

- **Design:** two clean clones of the same state (A, B; no patch). **5 repeats**, order rotated per repeat (AB, BA, AB, BA, AB). Per repeat: 6 v 6 samples (2 × 3) or 15 v 15 (5 × 3).
- **Deviation from §5 (stated now):** §5 says "S0 vs S0". Here each A/A runs at **the verdict's own state**, because the verdicts were measured at S1–S11, and σ there is the relevant noise. The case code is the same in both clones; only the state differs from §5.

**Verdict rule (frozen in `scripts/night_analyse.py`):**
- σ_rep(b) = sample standard deviation (n − 1) of the 5 per-repeat A/A ratios, median(B) / median(A). Floor(b) = 1 + 3 σ_rep(b).
- The original verdict **survives** iff its original ratio > Floor(b). It needs all 5 repeats; with fewer, the case is reported as incomplete and the rule is not applied.
- **Sensitivity (not primary):** σ_boot, the bootstrap SD of the median ratio (6 v 6 or 15 v 15 resamples of the pooled samples, 300 draws, seed 20261122), as in `aa/sigma_noise.json`.
- Also reported: any A/A "slower" or "faster" verdict on pooled samples (a false verdict).
- Wording fixed now: a survivor is "slower, and above its 1 + 3σ floor (pre-registered rule)"; a non-survivor is "asv-slower, but within the noise floor". #9 stays a profile-completeness flag either way (C11).

**Stopping:** cap 2 h (PM), checkpointed, stall guard 700 s (longest expected run ≈ 215 s, #9 at 5 × 3). Blocks run in the order above (cheap first).

**Estimate:** s02 ≈ 2 min, s08 < 1 min, s01 ≈ 6–12 min (35–70 s per run), s09 ≈ 27–36 min (160–215 s per run). Total ≈ 35–55 min.
