# E5 — measured setup-cached networkx benchmark pass — pre-registered plan (frozen 2026-11-22 16:52 PKT, before any implementation or measurement)

**Request:** advisor draft review via PM 16:44 (E5). It **replaces the "≈ 1.5–2× build + tests, setup cached" estimate** in RQ1 with a measurement. **Scheduled for the night of 23→24 Nov, not tonight.**

## Question

How long does a FULL networkx benchmark pass take when import-time and setup work is paid **once per module**, not once per process, with the same timing loops and the same number of samples per case? And how does that compare, on the same night, with the standard asv-protocol pass?

## Design

- **State:** S0 `181f2951`, one clean clone. All 171 time cases.
- **Arms**, alternated in one night: **STD, CACHED, STD, CACHED, STD, CACHED** (3 passes each). Alternating spreads the drift (N7) over both arms.
  - **STD:** the RQ1 FULL protocol, `bth.benchrun` interleave on one state: 2 processes × 3 values per case, 1 warm-up value, CPUs 2–5. This is the same as tonight's (d).
  - **CACHED:** a new runner mode, `bth.benchrun measure-cached`.
    - One worker process per benchmark **module** imports the module once.
    - Then, for each case in discovery order: a fresh instance, `setup(*params)`, `number` calibration as in asv, 1 warm-up value, **6 values** (the same 6 samples per case as STD), `teardown`.
    - CPUs 2–5, `OMP_NUM_THREADS=1`.
- **Both arms:** the per-run postponing gate and per-run (per-module for CACHED) checkpoints, with telemetry on.
- **Recorded per CACHED module:** import seconds; per case: setup seconds, calibration seconds, loop seconds (Σ values × number × per-call time) and wall seconds.

## Outcomes (fixed now)

- **Primary:** the CACHED pass total (sum of module walls), and the ratio of the median STD pass to the median CACHED pass, over 3 + 3 passes.
  - Reported as a range and a median, next to build + tests (≈ 71–89 s per edit, RQ1).
  - The RQ1 sentence "≈ 1.5–2× build + tests (estimate)" is replaced by the measured CACHED / (build + tests) range.
- **Split of the CACHED total:** imports / setup / calibration / loops / other.
- **Validity check (pre-registered):** per case, the ratio of CACHED to STD median sample, pooled over passes.
  - A case is **sample-shifted** if that ratio falls outside [0.8, 1.25]. The count of such cases is reported.
  - Sample-shifted cases point to state leakage within a module (warm caches) or to process-level effects. The pass totals are still reported, with the shift count next to them.
- **Not claimed:** that any selection or acceptance rule would use CACHED as is. It is a cost lower bound for a suite with module-level `setup_cache`, not a drop-in asv replacement.

## Implementation gate (before the run)

- `measure-cached` will be implemented and unit-tested on the toy repo **before** the night. Tests cover one import per module, sample count = values, and checkpoint and resume.
- Its code sha256 is recorded in `FROZEN.md` before the first measurement. A change to the protocol above after this freeze is a dated amendment.

## Caps and estimates

- **STD pass:** 659–2444 s each (measured earlier); tonight's (d) will tighten this. 3 passes ≈ 35–125 min.
- **CACHED pass (inferred):**
  - loops 132–171 s (measured, Σ samples × number, RQ1);
  - plus 8 module imports, of which `benchmark_algorithms` takes 4–47 s and the others a few s each;
  - plus 171 setups and calibrations ≈ 1–3 min;
  - ≈ 4–7 min per pass, so 3 passes ≈ 12–21 min.
- **Total ≈ 50–150 min. Cap 2.5 h,** with the hard stop at 06:25 as tonight. Stall guard: 3 × the longest expected STD run, or 3 × the longest CACHED module run (≈ 5 min for `benchmark_algorithms`), whichever is larger: **900 s**.
- **Order and stopping:** if the cap cuts the night, only complete STD + CACHED pairs are reported as primary.
