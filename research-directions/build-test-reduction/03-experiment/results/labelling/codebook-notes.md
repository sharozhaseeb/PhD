# Codebook notes for v2 (adjudicator, 2026-11-22)

These are proposals only. The frozen v1 codebook is unchanged. Each rule should be adopted as a dated amendment with a new hash **before** the replication sheet is labelled. Per the v1 amendment rule, rows labelled under v1 must be labelled again.

## 1. Bug fix plus speed-up (ids 9, 39)

**Ambiguity:** v1 says a bug fix is NOT_OPT, "including fixes that mention performance only in passing". It does not say what to do when the diff contains a real speed-up *and* a correctness fix.

**Proposed rule:** If any change in the diff alters the output for some valid input (other than an exception that was a bug), label **NOT_OPT**, however large the speed-up. The exception is the existing regression rule: restoring earlier speed stays OPT. A test whose expected value changes is evidence that the output changed. Id 33 was decided this way at adjudication.

## 2. Opt-in faster backend or new faster function (ids 18, 25)

**Ambiguity:** v1 excludes new options "such as `method="fast"`, unless the main change is making an existing path faster". Raters split on whether an optional accelerated backend counts as a new feature or as a speed-up of existing calls.

**Proposed rule:** Label **OPT** when existing public calls, with unchanged signatures, get faster for users under the default configuration. This includes a backend that is used automatically when it is installed. Label **NOT_OPT** when the user must change their code to benefit, for example by calling a new function, passing a new argument or flipping an option that is off by default. Id 18 was adjudicated OPT under the first half: PyGEOS is used by default when installed and existing GeometryArray methods are rerouted.

## 3. Speed-up that changes output order (ids 40, 58, 23)

**Ambiguity:** v1 says "keeping what it computes the same" but does not say whether ordering counts.

**Proposed rule:** Order is part of the output when it is documented, tested, or used by callers in the library, as with lists, DataFrame row order or index order. If such an order changes, label **NOT_OPT**. If the result is a set, a dict used as a mapping, or an order the documentation calls arbitrary, a changed order does not count as changed output. Raters should name which case applies in the reason.

## 4. Meaning of `opened_link`

**Ambiguity:** Raters set it inconsistently. Some set it to true after an attempted fetch that returned HTTP 503 (rater2 on ids 33 and 67), and others set it to false.

**Proposed rule:** Replace the field with two fields:
- `link_attempted` (bool);
- `link_content_seen`: one of `none`, `partial` or `full_diff`.

The reason must say when a label relied on linked content beyond the sheet. Only `link_content_seen != none` counts as "opened" for analysis.

## Other observation

Truncated rows whose decisive file is cut off (ids 33 and 67) went to adjudication because both raters hit 503 errors. For v2, the sheet should either include the full diff of non-test, non-data source files (and drop binary or test-data lines first, which would have exposed `overlay.py` in id 67), or pre-fetch the `.diff`, so labels do not depend on network luck.
