# Mining-precision labelling sheet (e) — rater guide

**File:** `mining_precision_sheet.csv` (UTF-8, opens in Excel). 81 rows: every commit record mined so far, whether or not the v1 rule qualified it. networkx 21, bottleneck 16, geopandas 26, pvlib-python 18. Made by `scripts/labelling_sheet.py` (seeded shuffle 20261122, so projects are mixed). Generated 2026-11-22 15:34 PKT.

**Raters are blind on purpose:** the sheet shows no benchmark reach, replay status, rule output or earlier label. Rater 2 must not see rater 1's columns. Give rater 2 a copy with the `rater1_*` columns deleted.

## The question for each row

**Is this commit an optimization?** That is, is its main intent to make existing code run faster or use fewer resources (time, memory, I/O) without changing what it computes?

Fill `raterN_is_optimization` with one of:
- `yes`: the main intent is performance, and the diff changes source code that runs (not only tests, docs or benchmarks).
- `no`: the main intent is something else, such as a bug fix, a feature, a refactor or a docs change. This includes subjects matched only by words such as "coefficient" or "efficiency" used in another sense, and "optimize" in the sense of `scipy.optimize` or a numerical optimizer.
- `unclear`: you cannot tell from the subject, body, diff summary and diff (open the link).

Put a few words in `raterN_reason`, for example "vectorises loop", "bug fix, mentions perf", or "test-only".

**Rules:**
- Judge from the diff when the subject and the diff disagree. Open the link for every row whose summary leaves doubt.
- Fix-ups of an earlier performance regression count as `yes` if the change restores speed.
- A commit that mixes a feature with a speed-up is `yes` only if the speed-up is the main part of the diff.

## Afterwards (W3, not raters)

- Precision of the v1 rule = `yes` / (rule-qualified rows), per project, with Wilson CIs. Join on `sha` with `edits/*.json`.
- Cohen's κ between raters on the doubly labelled rows. The TPM plan asks for a second rater on ≥ 20 %. Labelling all 81 twice is better, since the set is small.
- Rule v2 may be tuned on these rows, but its precision must be reported on a **held-out** labelled sample (TPM R-4).
