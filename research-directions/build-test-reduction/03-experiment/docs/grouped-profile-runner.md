# Grouped profile runner for the B1 replication (experiment (a)) — design, not built, not run

Written 2026-11-22 ≈ 15:40 PKT (PM 15:20; TPM plan §1 (a)). **Status: design only.** Nothing here has been implemented or run.

## Problem

- B1 needs a **measured reach set** (functions executed) per benchmark case, at each edit's parent, in 3–5 new projects.
- Today's `bth.benchrun profile` starts **one worker process per case**. Each process imports the benchmark module, runs `setup`, then makes one call under `bth.monitor.Recorder`.
- On networkx, `benchmark_algorithms` builds its graphs at import time (≈ 4–47 s per process, N7), so 49 cases pay that cost 49 times.
- The TPM estimate for (a) with per-case processes is ≈ 15–50 h, which is not feasible. Grouping targets ≈ 3–10 min per state.

## Design

**Unit of work:** one worker process per **(state, benchmark module)**, not per case.

1. **Import once.** Import the module the same way as `_import_module` (asv package semantics). Import-time code runs once, **before** recording starts. This is the same as today: today's Recorder also starts after import and setup, so module-level and import-time code are excluded in both. B1 also excludes `::<module>` lines.
2. **Per case, in discovery order:** instantiate the class (a fresh instance per case, as asv does), call `setup(*params)`, then `rec.reset()`, then `rec.start()`, make one call, then `rec.stop()`, then `teardown(*params)`. Emit `{case_id: sorted(funcs)}`.
   - `Recorder.reset()` already calls `sys.monitoring.restart_events()`. `PY_START` locations that earlier cases DISABLEd therefore fire again, so case 2 sees code that case 1 already ran. This is the property that makes grouping correct. **It must be unit-tested first** (see Validation).
3. **Isolation within a group:**
   - A case can leave state behind: caches such as `functools.lru_cache`, module globals, or lazily imported modules.
   - Consequence: a later case may then **not** execute a function that it would execute in a fresh process (for example, cache hits skip the function body). Grouping can therefore only **shrink** a reach set, never grow it, apart from nondeterminism.
   - That direction **inflates "unreached"**, which is the B1 claim. So it must be measured, not assumed (validation step 2).
4. **Fallback per case:** a case whose setup raises `NotImplementedError` is recorded as skipped, as today. A case that crashes or times out kills only its group. The runner then reruns the rest of the group one process per case and labels those results `fallback`.
5. **Timeouts:** the group timeout is the sum of the case timeouts, capped at 30 min. Per-case wall time is logged.
6. **Native code:** keep `--native-prefix` (CALL events for C functions, never DISABLEd), unchanged.
7. **Parallelism:** groups are independent, so run them with up to 4 workers (CPUs 2–5). This is legitimate because profiling measures sets, not times. The rule stays: it must not overlap any timing window (TPM parallelism rule).
8. **Output:** the same format as `orchestrate profile` (`profile/<label>.json`, `profiles: {BenchID: [FuncID]}`), plus `meta.runner = "grouped"`, `meta.group_of`, and per-case `fallback` flags. The B1 count scripts need no change.

**Interface (proposed):**

```
python -m bth.benchrun profile --grouped --jobs 4 --state DIR --bench-dir D --out F [--native-prefix P]
```

`_w_profile_group` is a new worker op. It takes the list of a module's cases and emits one record per case, flushed per case, so a killed group keeps the cases it finished. The output can also be checkpointed to JSONL, as `run_interleaved` is.

## Validation (before any use in (a); pre-register its pass rule)

1. **Unit tests** (toy repo):
   - two cases in one module that call the same function both record it (restart_events works);
   - a case after a crashing case falls back;
   - the output format equals the per-case runner's.
2. **Equivalence on networkx S0** (TPM: "it must reproduce 171/171 reach sets"):
   - Run grouped against the existing per-case profile `raw/networkx/profile/S0_181f2951.json`. The re-profile on 2026-11-22 confirmed 24 of 24 cases identical.
   - **Pass rule (proposed):**
     - all 171 sets are equal, except cases whose difference is within the known per-case nondeterminism, measured by a second per-case run for those cases only;
     - **no case loses a slowed or changed function of the 18 networkx edits**, because that would change B1.
   - Report every difference.
3. **Order sensitivity:** for networkx, also run each group in reverse case order. Any set that depends on order is evidence of within-group state leakage (step 3 of the design). Those cases go to the fallback list for every project.
4. **Cost check:** the wall time per state, grouped against per-case, on networkx S0. This is the number the (a) schedule needs.

## Risks

| Risk | Effect | Mitigation |
|---|---|---|
| State leakage between cases (caches) | Reach shrinks, so B1 inflates | Validation 2 and 3; reverse-order run; fallback per case |
| `restart_events` behaviour differs across Python versions (3.12+ only; `sys.monitoring` does not exist before 3.12) | Wrong sets | Unit test per interpreter. Projects whose parents need Python < 3.12 cannot be profiled with `sys.monitoring` at all. **This is an attrition rule for (a): pre-register it.** |
| A heavy group times out | Lost group | Fallback per case; checkpoint per case |
| Memory: all of a module's setups in one process | OOM on a 7 GB laptop | One instance per case, torn down after its call; `--jobs` ≤ 2 for heavy modules |

## Effort

Implementation 3–4 h, tests 1 h, networkx validation run ≈ 10–30 min of machine time (not a timing run, but CPU-heavy: outside timing windows). Matches TPM's 3–4 h.
