# Codebook v2: is a mined commit a true performance optimization? (frozen 2026-11-22 15:53 PKT, before any v2 labelling)

**Status:** v2 is for the **replication sheet** (experiment (a)) and every later sheet. v1 (`frozen/labelling/codebook.md`, sha256 `8cf954cc5a4f75e186a2ccae45a0222b329969f2b6965d527543e4d6c417b303`) is unchanged and remains the codebook of record for the 81-row v1 sheet (labelled 15:55, D26).

**What changed:** v2 adopts all four rules proposed in `results/labelling/codebook-notes.md` (adjudicator, sha256 `d58ba58571ba5ef7c9c79a81a4bcc83f9881a53c211881ece99253689cab8ae6`), plus that file's sheet recommendation. Each change is marked **[v2]**.

**Re-labelling the v1 sheet:** under the v1 amendment rule, the 81 v1 rows would be labelled again under v2 if v2 were applied to them. That is optional, and it is the PM's call. If it is done, results under v1 and v2 are reported separately.

## Input (for a v2 sheet)

- The fields are as in v1, with these changes:
  - **[v2] diff:** first drop binary, test-data and fixture lines. Then include the **full diff of non-test, non-data source files**, and truncate only test files and data to the first 300 lines. The full `.diff` is pre-fetched into the sheet, so a label never depends on a network fetch.
- Blind by design, as in v1: no mining-rule output, benchmark reach, replay status or earlier label.
- Each sheet's sha256 is recorded in `frozen/FROZEN.md` before labelling, together with this codebook's sha256.

## Definition (unchanged from v1)

A commit is a **true performance optimization (OPT)** if its **main intent** is to **reduce the runtime or memory use of existing functionality**, keeping what it computes the same, and the diff changes code that runs in the library. Tests, docs or benchmarks alone do not count.

Evidence of intent, strongest first:
1. what the diff does;
2. the body;
3. the subject.

When the subject and the diff disagree, the diff wins.

## Exclusions (label NOT_OPT)

- **Refactor or maintenance**, as in v1.
- **Bug fix**, as in v1. **[v2] Bug fix plus speed-up:**
  - If any change in the diff alters the output for some valid input, label **NOT_OPT**, however large the speed-up.
  - A changed exception counts only when the old exception was a bug.
  - A test whose expected value changes is evidence that the output changed.
  - The exception is a fix of a performance regression that restores earlier speed, which stays OPT.
- **Docs, tests, build or CI only**, as in v1.
- **New feature or API**, as in v1. **[v2] Opt-in faster backend or new faster function:**
  - Label **OPT** when **existing public calls with unchanged signatures get faster under the default configuration**. This includes an accelerated backend that is used automatically when it is installed.
  - Label **NOT_OPT** when the user must change their code to benefit, for example by calling a new function, passing a new argument or enabling an option that is off by default.
- **"Coefficient"-type false matches**, as in v1.

**Edge cases:**
- As in v1: a regression fix that restores speed is OPT; a mixed feature plus speed-up is OPT only if the speed-up is the main part; a memory reduction is OPT.
- **[v2] Output order:**
  - **Order is part of the output** when it is documented, tested, or used by callers in the library: lists, DataFrame row order, index order. A speed-up that changes such an order is **NOT_OPT**.
  - For sets, dicts used as mappings, or an order the documentation calls arbitrary, a changed order does **not** count as changed output.
  - The reason must name which case applies.
- **Truncated diff:** with the v2 sheet, the source diff is complete. Use UNSURE only if the decisive evidence is absent from the sheet.

## Labels (unchanged)

`OPT` / `NOT_OPT` / `UNSURE`, with a one-line reason of at most 25 words naming the decisive evidence.

**[v2] Output per labeller:** JSONL with fields `id`, `sha`, `label`, `reason`, `labeller`, `link_attempted` (bool) and `link_content_seen` (`none`, `partial` or `full_diff`).
- If the label relied on linked content beyond the sheet, the reason must say so.
- Only `link_content_seen != none` counts as "opened" in the analysis.

## Adjudication and reporting (unchanged from v1)

- Disagreements, including any UNSURE, go to the third agent. Agreed rows keep their label.
- **[v2]** The adjudicator decides from the sheet only. If its reason relies on facts that are not in the sheet, it must say where they came from. Otherwise the label is UNSURE.
- **Reported:**
  - precision of the mining rule, per project and pooled, with Wilson 95 % CIs;
  - Cohen's κ and the raw agreement between raters 1 and 2;
  - the number of rows adjudicated;
  - **[v2]** a threat note that same-model raters may share biases, which inflates κ.

The codebook is not changed after labelling starts. Any change is a dated amendment with a new hash.
