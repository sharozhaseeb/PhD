# Post-hoc re-check of spot-check #9's "slower" verdict — plan (written 2026-11-22 12:32 PKT, before measuring; PM approval 12:31)

**Status: POST HOC.** The **primary result stays the pre-registered C11 flag:** in the powered profile-completeness check, `time_louvain_communities('Erdos Renyi (100, 0.9)')` was "slower" (1.13×, p = 0.0019) under slowdown #9 (`isomorphvf2.DiGMState.__init__`), so reach-based selection is flagged unsafe for #9.
- This re-check can **confirm** or **fail to confirm** that verdict. It can **never withdraw** the flag.
- **Multiplicity:** the flag is 1 of 50 out-of-reach comparisons at α = 0.002. With 50 independent nulls, the chance of ≥ 1 false "slower" is about 1 − 0.998⁵⁰ ≈ 9.5 %, before the ratio condition, which lowers it. The A/A gave 0 false verdicts in 46.

**Case:** `benchmark_algorithms.UndirectedAlgorithmBenchmarks.time_louvain_communities('Erdos Renyi (100, 0.9)')`

**States:** all three are clones at #9's state (`frozen/networkx.slowdowns.json` entry 9):
- **base** = `nx-slow-A`, unpatched;
- **slow** = `nx-slow-B`, with the frozen #9 patch;
- **base2** = `nx-slow-C`, unpatched: a second independent base, the **drift and noise control** (PM).

**Protocol:**
- `bth.benchrun interleave` with states base, slow, base2: 5 processes × 3 values + 1 warmup, CPUs 2–5, `OMP_NUM_THREADS=1`.
- **2 repeats.** The runner rotates the order per repeat: repeat 0 runs base → slow → base2, repeat 1 runs slow → base2 → base. So each pair sees both orders. Each state gets 30 samples.
- **Safeguards:**
  - per-run checkpoint `recheck9/runs.partial.jsonl`;
  - postponing idle gate (WSL load ≤ 1.0 and Windows CPU ≤ 20 %, 3 × 60 s);
  - cap 25 min (`timeout 1500`, gate included);
  - detached watcher `stall_watch_wsl2.sh`, stall limit 650 s (3 × 216 s, the longest louvain run today).

**Verdict rule (unchanged):** `bth.stats.asv_rule` (ratio > 1.1 and MWU p < 0.002) on the pooled samples, for **slow vs base** and **base2 vs base**. Per-repeat verdicts are also reported.

**What each outcome means (fixed now):**

| slow vs base | base2 vs base (control) | Reading |
|---|---|---|
| slower | same | **confirms** the original verdict; C11 flag stands (and is reinforced) |
| same | same | **fails to confirm**; C11 flag **still stands** as the primary result; the original verdict is not reproduced |
| any | slower or faster | **inconclusive**: base-vs-base drift or noise is as large as the effect; C11 flag stands |
| faster | same | fails to confirm (opposite direction); C11 flag stands |

**Outputs:** `recheck9/{runs.partial.jsonl, result.json, driver.log}`. Driver: `scripts/recheck9_nx.py`.
