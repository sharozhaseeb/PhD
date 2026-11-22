# Codebook: is a mined commit a true performance optimization? (frozen 2026-11-22 15:44 PKT, before any labelling)

**Decision:** owner, 15:43 (via the PM). Two independent agent labellers label every row; a third agent adjudicates the rows where they disagree. The PM runs the agents.

## Input

- **File:** `frozen/labelling/sheet.jsonl`, sha256 `19d5cdaf74d672985646ac5fb5dcd4f09899ca8b05b541d94cad50aa3236b7e5`. Built 15:44 by `scripts/labelling_jsonl.py`.
- **Rows:** 81, one per mined commit record, whether or not the mining rule qualified it: networkx 21, bottleneck 16, geopandas 26, pvlib-python 18. No replication candidates have been mined yet. They will go into a **separate** sheet with its own codebook hash, labelled under this same codebook.
- **Order:** a seeded shuffle (seed 20261122).
- **Fields:** `id`, `repo`, `sha`, `date`, `subject`, `body`, `diffstat`, `diff`, `diff_lines_total`, `diff_truncated`, `link`.
  - `diff` is the first 300 lines of `git show`; 11 rows are truncated.
- **Blind by design:** the sheet has no mining-rule output, benchmark reach, replay status or earlier label. Labellers must not look these up.

## Definition

A commit is a **true performance optimization (OPT)** if its **main intent** is to **reduce the runtime or memory use of existing functionality**, keeping what it computes the same, and the diff changes code that runs in the library. Tests, docs or benchmarks alone do not count.

Evidence of intent, strongest first:
1. what the diff does, for example a faster algorithm or data structure, vectorization, avoided recomputation, caching, an early exit, fewer allocations or copies, or a cheaper check;
2. the body;
3. the subject.

When the subject and the diff disagree, the diff wins.

## Exclusions (label NOT_OPT)

- **Refactor or maintenance:** renames, moves, cleanup, style, typing only, deprecations, compatibility with new dependency versions. This applies even if the subject says "faster" or "optimize".
- **Bug fix:** a correctness fix. This includes fixes that mention performance only in passing.
- **Docs, tests, build or CI only:** this includes changes only to benchmarks or `asv` files.
- **New feature or API:** new functionality, including new options such as `method="fast"`, unless the main change is making an existing path faster.
- **"Coefficient"-type false matches:** subject words that matched the mining regex in a non-performance sense. Examples: "coefficient", "efficiency" as a computed quantity, `scipy.optimize` or an "optimizer" or "optimal" in the domain sense, `fast_`-named APIs that the commit does not speed up, and "performance" in the sense of model or PV-system performance.

**Edge cases:**
- **Fix of a performance regression** that restores speed: **OPT**.
- **Mixed feature plus speed-up:** OPT only if the speed-up is the main part of the diff.
- **Memory reduction** with no runtime intent: **OPT**.
- **Truncated diff:** label from what is shown plus the diffstat. Use UNSURE if the decisive part is cut off. The link may be opened; the labeller must say so in the reason.

## Labels

Exactly one of:
- **`OPT`**: meets the definition.
- **`NOT_OPT`**: any exclusion applies, or the intent is not performance.
- **`UNSURE`**: cannot be decided from the row (and the link).

Each label has a **one-line reason** of at most 25 words. Name the decisive evidence, for example "replaces O(n²) loop with set lookup", "bug fix; perf mentioned only in title", or "'coefficient' match, computes clustering coefficient".

**Output per labeller:** JSONL with fields `id`, `sha`, `label`, `reason`, `labeller`, and `opened_link` (true or false).

## Adjudication

- The third agent sees only the rows where labellers 1 and 2 disagree, including any row where either said UNSURE. It sees both labels and reasons and gives a final label and reason under this same codebook.
- Rows where both labellers agree keep their label.

**Reported:**
- per-project and pooled precision of the v1 mining rule: final OPT among the rule-qualified rows (joined on `sha` with `edits/*.json`), with Wilson 95 % CIs;
- agreement between labellers 1 and 2: Cohen's κ on the three labels, and the raw agreement rate;
- the number of rows that went to adjudication.

The codebook is not changed after labelling starts. Any change is a dated amendment with a new hash, and rows labelled before it are labelled again.
