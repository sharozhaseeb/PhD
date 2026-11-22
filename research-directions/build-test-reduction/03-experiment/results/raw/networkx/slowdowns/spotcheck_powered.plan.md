# Powered out-of-reach spot check — plan (written 2026-11-22 before any measurement; PM approval 06:10)

**Why:** the first spot check ran 1 process × 3 values × 2 repeats, which gives 6 vs 6 samples. The smallest possible exact two-sided Mann-Whitney p for 6 vs 6 is 2/924 = 0.00216, above α = 0.002, so no "slower" verdict was possible (critic review; `../bench/LABELS.md`).

**Frozen sample (unchanged):**
- **Sample file:** `frozen/networkx.slowdown_spotcheck.json`, seed 20261121, frozen 2026-11-21 19:30, before any slowdown measurement. It holds 10 cases; 5 are in `benchmark_algorithms`.
- **Slowdowns covered:** the 5 whose reach was empty, #0, #5, #6, #7 and #9, so all 10 sample cases are out of reach for each. The other 5 slowdowns have static reach = all 171 cases, so they have no out-of-reach members, as before.
- **Patches and states:** the same frozen slowdown patches and states (`frozen/networkx.slowdowns.json`).

**Protocol:**
- Interleaved A/B with `bth.benchrun interleave`, base clone vs patched clone at S_s.
- **5 processes × 3 values × 1 repeat, + 1 warmup value per process, giving 15 vs 15 samples per case.** This meets readiness §5 (≥ 5 processes × ≥ 3 values).
- CPUs 2–5, `OMP_NUM_THREADS=1`.
- Verdict: `bth.stats.asv_rule` (ratio > 1.1 and MWU p < 0.002), unchanged.

**Power (computed with `bth.stats.asv_rule` before measuring):**

| Samples | Smallest possible p (full separation) | Can return "slower"? |
|---|---|---|
| 6 vs 6 (old) | 0.00216 | **no** |
| 15 vs 15 (this plan) | 3.4 × 10⁻⁶ (scipy "auto" → normal approximation) | yes |

- **Simulated power** (200 draws, Gaussian noise with a 5 % coefficient of variation, 15 vs 15): **1.00 at a 1.20× slowdown, 0.81 at 1.12×.**
- **Caveat:** the samples within one process are not independent, so the real power and false-positive rate differ from this simulation. The minimum-p argument holds regardless.

**Idle gate (fixed — postpones, does not only label):**
- **Rule:** before **each** slowdown block, wait until WSL `loadavg(1m) ≤ 1.0` **and** Windows total CPU ≤ 20 % for **3 consecutive 60 s checks**. A block never starts above the gate.
- **Recorded:** load before and after each block, plus the per-run `loadavg_before/after` that `benchrun` already logs.
- **During a run:** if the load goes above 1.5, the block is kept and labelled **noisy** (M5).
- Nothing else of this session runs concurrently.

**Cap:** the whole driver runs under `timeout 5400` (1.5 h, gate waits included). On overrun it stops, and the completed blocks are kept and reported as partial.

**Outputs:** `spotcheck_powered/<i>.json` (one per slowdown, written as each finishes), `spotcheck_powered/driver.log`. Driver: `scripts/spotcheck_powered_nx.py` via `scripts/wsl/spotcheck_powered.sh`.

**Reporting:** per slowdown, out-of-reach verdicts, slower / same / faster over 10 cases. Any "slower" verdict means reach-based selection is unsafe for that slowdown (C11). This is reported as a spot check over 50 comparisons, never as a miss rate.
