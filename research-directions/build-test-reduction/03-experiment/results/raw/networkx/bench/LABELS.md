# Timing labels for networkx benchmark runs

| Run | Label | Why | Usable for |
|---|---|---|---|
| `S0_181f2951.json` (started 18:35 PKT) | **concurrent (CPU-pinned)** | Bench on CPUs 2-5 while the RQ2 chain (depmaps, testmon, kill sets) ran on CPUs 6-11 from 18:52; shared cache, memory bandwidth and thermals (`../../concurrency_log.json`) | Selection counts; *provisional* per-benchmark cost weights. **Not** for regression decisions, noise floor or oracle repeatability. |

Rule (PM, 18:52): this run is re-run on an idle machine before any regression decision or the oracle-repeatability analysis uses it. The idle re-run will be stored as `S0_181f2951.idle.json`.
