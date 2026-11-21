# RQ1 — bottleneck build cost: clean vs incremental vs null (PRELIMINARY)

**Status:** PRELIMINARY, 2026-11-21 18:30 PKT. Single runs. Each build ran under `nice -n 19` with a single job while the networkx timing runs used the machine, so the wall times are labelled **noisy**. These are setup probes, not the replay-state measurements (those follow on the amended 13-edit replay).

- **State:** bottleneck base `22657acaad5f27d9f692dd64362439ada8032c1b` (the original window's base; the scratch copy `~/bt-lab/exp/work/bn-scratch`).
- **Environment:** CPython 3.8.20 (uv-managed) and numpy 1.19.5, per M4. CPython 3.12 fails before compiling: the 2019 `versioneer.py` calls `configparser.SafeConfigParser`, which was removed in 3.12. Package versions are in `raw/bottleneck/env-freeze.txt`.
- **Build command:** `nice -n 19 python setup.py build_ext --inplace` (setuptools 59.8.0, gcc 13.3).
- **Evidence:** raw timing logs in `raw/bottleneck/incr_<X>_*.log` (bash `time`), and artefact mtimes before/after in `raw/bottleneck/incr_<X>_*.{before,after}.txt`. setuptools prints no compile lines, so "what was rebuilt" = the `.so` and generated `.c` files whose mtime changed.

| Probe | Edit (one line appended/changed) | Rebuilt (from mtime diff) | Wall (s) | Raw |
|---|---|---|---|---|
| Clean build | `git clean -fdx`, then build | all 4 `.so` | **9.90** | `raw/bottleneck/setup-build.log` |
| B | `src/reduce_template.c` | `reduce.c` regenerated, `reduce.so` | 2.64 | `incr_B_reduce_template.*` |
| C | `src/bottleneck.h` (listed in `depends=`) | all 4 `.so` | 4.86 | `incr_C_bottleneck_h.*` |
| **D** | **`src/iterators.h` (included by templates, NOT in `depends=`)** | **nothing** | **0.20** | `incr_D_iterators_h.*` |
| E | `src/move_median/move_median.c` | `move.so` | 1.83 | `incr_E_move_median_c.*` |
| F | `src/move_template.c` | `move.c` regenerated, `move.so` | 1.79 | `incr_F_move_template.*` |
| G | null rebuild (no change) | nothing | 0.20 | `incr_G_noop.*` |

For comparison at the same state, the full test suite takes **34.4 s** (168 passed; `raw/bottleneck/setup-test.log`).

## Reading (measured; noisy timing)

- **Build share:** a clean build (9.9 s) is about 22 % of clean build + full tests (9.9 + 34.4 s), before any benchmarks. Unlike pure-Python networkx (about 1.3 %), build cost here is not negligible.
- **Incremental builds:** an edit to one template rebuilds one extension, saving about 73–82 % of the clean build time (1.8–2.6 s vs 9.9 s). A shared-header edit rebuilds everything (4.9 s).
- **Stale-build hazard (mechanism; historical upstream bug, since fixed):** probe D shows that an `iterators.h` edit triggers **no rebuild at this state**, because the base's `setup.py` lists only `bottleneck.h`/`bn_config.h` in `depends=`.
  - Upstream fixed exactly this on 2019-09-20 in `52f6cd1` ("FIX: add proper dependency on iterators.h in setup.py"). Current upstream `setup.py` (`b0815406`) lists `iterators.h`. This is **not an open upstream bug**.
  - It is still a real-world instance of an unsafe incremental build that the maintainers had to fix (C8 / B4 / B6).
  - **Consequence for the replay:**
    - The amended 13-edit window's base `f51ed86` already contains the fix. All 3 mined `iterators.h` commits (`c5720c8d`, `a638b282`, `98b59df2`) are among the 13 replayed edits, so with the fixed `depends` the incremental build is *expected* to be correct.
    - The consequence study (`build-hazard-iterators-h.md`, pending) measures incremental vs clean on those 3 edits.
    - It also runs a **counterfactual probe** with the pre-fix `depends` list (labelled probe, not a natural miss), to show what the stale build would have done to tests and benchmarks.
