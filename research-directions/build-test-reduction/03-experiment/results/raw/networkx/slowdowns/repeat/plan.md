# E3 — slowdown-oracle repeatability for the 5 reached slowdowns — pre-registered plan (frozen before measurement, 2026-11-22 15:32 PKT)

**Why:** advisor must #3 (E3, P20). Is #1's verdict noise? Is #3 a power miss? Do #2's and #8's verdicts recur?

**Slowdowns:** #1 `bidirectional_dijkstra`, #2 `_dijkstra_multisource`, #3 `is_connected`, #4 `_single_shortest_path`, #8 `_build_paths_from_predecessors` (the five with non-empty reach; frozen `frozen/networkx.slowdowns.json`). Each at its own state, base clone vs base + slowdown patch, as in the original oracle.

**Two tiers (case lists frozen in `frozen/night-2026-11-22.cases.json`):**

| Tier | Cases | Repeats | Order |
|---|---|---|---|
| 1 (primary) | the cases with an original "slower" verdict ∪ the cases whose S0 profile executes the slowed function: #1: 1, #2: 9, #3: 3, #8: 1, #4: none (empty profile reach). **14 cases.** | **4** | base-first, slow-first, base-first, slow-first |
| 2 | all other time cases (171 minus tier 1) | **2** | base-first, slow-first |

- **Protocol:** as the original oracle, 2 processes × 3 values per repeat, CPUs 2–5, asv rule on pooled samples. Tier 1 pools 24 v 24 (original: 18 v 18). Tier 2 pools 12 v 12; the smallest attainable MWU p at 12 v 12 is ≈ 7 × 10⁻⁷, below α.
- **Not done (cost):** the advisor's 5-process variant. At 5 × 3, a `benchmark_algorithms` run takes 132–235 s, which would roughly triple tier 1 and is not affordable for tier 2.

**Outcomes (frozen in `scripts/night_analyse.py`):**
- Per case: pooled verdict now vs the original; **agree** = same status. Also the two order-balanced pairs (rep 0 + 1, rep 2 + 3) against each other.
- Per slowdown and tier: transition counts (slower→slower, slower→same, same→slower, …).
- Questions and how each is read:
  - **#2 on-target (8 atlas cases):** slower again → the on-target detection repeats.
  - **#1 off-target `connected_components ER(100, 0.1)` and #2 off-target `NonNeighbors`:** same now → the original was consistent with noise.
  - **#8 (1 case):** slower again or not.
  - **#3's 3 on-target cases:** slower now (with 24 v 24) → **power miss** in the original; same again → no evidence of a detectable effect at this protocol.
  - **Tier 2:** count of new "slower" verdicts (off-target, expected ≈ 0 from the A/A: 0/46 false verdicts) and of vanished ones.
- The (b) floors are applied to every slower verdict whose case has σ.

**Stopping:** tier 1 cap 75 min; tier 2 runs last, until the hard stop (≤ 6 h). Tier-2 order: #3, #4 (the misses), #2, #8, #1 (the slowest: its original pass took 4782 s per repeat under drift). A tier-2 slowdown counts only if both repeats finished for all its cases; otherwise it is reported as partial.

**Estimate:** tier 1 ≈ 17–40 min. Tier 2 ≈ 44–51 min per slowdown for #2, #3, #4, #8 at recorded rates; #1 ≈ 50 min to 2.7 h. Total tier 2 ≈ 3.7–5.4 h.
