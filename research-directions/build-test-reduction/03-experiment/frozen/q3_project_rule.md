# Q3 — B1 replication by static reach: project-selection rule (frozen 2026-11-22 ≈ 07:53 PKT [file time; header first said ≈ 07:58 in error], before any candidate repo was cloned or mined)

**Request:** PM 07:50 (advisor review). For each project, count how many replayed optimization edits change **no function reached by any asv benchmark**, using static call-graph reach from the benchmarks. No timing.

## Selection rule (all must hold)

1. **asv in the main repository:** an `asv.conf.json` and an asv benchmark directory in the project's own repository, not a separate benchmarks repository.
2. **Pure Python or light C:** the main package imports without compiling extensions, or C/Cython/C++ source is < 10 % of the package's source lines. This is checked on the clone at mining HEAD.
3. **Enough edits:** ≥ 10 commits match **the same mining rule as networkx** (`configs/networkx.toml [mine]`):
   - the subject-only regex `(\bperf\b|speed ?up|faster|optimi[sz](e|ation|ing|ed)\b|performance|vectori[sz]|efficien)`;
   - they touch the package's non-test `.py` files, with ≤ 200 changed lines;
   - first-parent, before 2026-11-21, the most recent 20.
4. **Order:** candidates are tried in the fixed order below, and **the first 2 that pass are used.** If a candidate fails, the next one is tried. The reason for each failure is recorded.

## Candidate list (fixed now, alphabetical)

Python projects known to keep an asv suite in their own repository:
1. `geopandas/geopandas`
2. `pvlib/pvlib-python`
3. `pydata/xarray`

**Considered and excluded a priori, with the reason (from general knowledge, not checked):**

| Project | Reason |
|---|---|
| pandas, numpy, scipy, scikit-image, scikit-learn, MDAnalysis | heavy C / Cython (fails rule 2) |
| astropy, dask, sympy | asv suite in a separate repository (fails rule 1) |
| shapely | C / GEOS core |
| networkx | already the pilot |

## Bottleneck (C extension)

- **Edits:** the amended window, **states 1–8** (PM 06:10 ruling; states 9–13 held out). The 13-state count is reported as sensitivity.
- **Reach:** static Python reach cannot follow calls into the C extension. A changed native function `native::<ext>.<name>` therefore counts as reached if its Python name appears in the asv benchmark sources as an identifier, an attribute or a string literal (bottleneck's benchmarks pass function names as parameters).
  - A header edit counts as reached if any function of an extension it feeds is reached.
  - This is labelled **W3-new name-based reach**, an approximation.

## Counting (same for every project)

- **Unit:** one mined edit. Changed functions come from `bth.changed_fns` on the commit's own diff (parent → commit), as in networkx.
- **Module-level lines are excluded** (`::<module>`), as in networkx B1.
- An edit is **"unreached"** if none of its changed functions is in the static reach of any benchmark case. Reach is computed with `bth.staticgraph.build` at the parent of the oldest mined edit (the base), as networkx's S0.
- **Reported:** k unreached of N edits, with a Wilson 95 % CI, next to networkx: 12/18 by S0 profile reach (measured), and networkx by static reach (computed the same way).
- **Frozen first:** each project's edit list is written to `edits/<project>.q3.candidates.json`, with its sha256 in `frozen/FROZEN.md`, before any reach is computed.

**Cap:** 1 h total for counting, after the spot-check top-up. Cloning and scripting can happen earlier (network and disk only: no builds, no xdist).

## Addendum (PM 07:52; reporting only, does not change the rule)

- **networkx: the two reach measures already differ.** Static reach (S0, module-level lines excluded) leaves **7/18** edits unreached (steps 1, 6, 8, 13, 15, 17, 18). S0 profile reach leaves **12/18** (finding B1). Static reach is a superset of profile reach, so its count is the lower one.
- **The Q3 report shows both side by side** wherever profiles exist. For geopandas, pvlib-python and xarray no profiles exist (only static reach is computed, with no timing and no execution), so their count is a static-reach count and is **expected to under-count** profile-unreached edits, as it does on networkx.
- **Bottleneck:** name-based native reach, as stated above. Its benchmark profiles (`sys.monitoring` of the C extension) were not measured.
