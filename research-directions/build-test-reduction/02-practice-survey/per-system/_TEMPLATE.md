# <System name>

Status: draft (researcher) · Last checked: 2026-11-21
Artifact: <repo URL> @ <full commit SHA> (local clone: `C:\Users\pc\study\bt-lab\survey\<dir>`) · Paper: <URL, version>
Evidence labels: **[src]** read in source (file path + line or paper section quoted/paraphrased), **[inf]** inferred by us from sources, **[unk]** not found (say where you looked).

## 1. What it is (2–3 lines)

## 2. Build / environment
- What counts as a "build" (pip install -e, compile C ext, Docker image build, none)?
- How environments are built and cached: one image per instance? prebuilt & pulled? rebuilt per candidate? reused across candidates?
- Is any build step reduced, incremental or skipped for a candidate?

## 3. Correctness tests per candidate
- Which tests run (full suite / FAIL_TO_PASS / PASS_TO_PASS / curated subset / generated tests / hidden tests / output equality)?
- How are they chosen, and by whom (dataset authors, at curation time, per instance)?
- Is this a form of test selection? (fixed per task vs. per edit)

## 4. Performance measurement per candidate
- Workloads/benchmarks (who wrote them, how many per instance)
- Repeats, warm-ups, statistic (mean/median/min), statistical test, threshold for "speed-up"
- Noise controls (CPU pinning, isolation, instruction counting/simulation, same machine)

## 5. Cost per candidate (if reported)

## 6. Iteration / cumulative re-validation
- Does the system accept several edits in sequence? Is anything re-validated after several accepted edits (cumulative or final check), or only per candidate?

## 7. Limitations the authors state

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- 2–4 bullets, each labelled [src]/[inf].

## Sources
- Files read (path @ commit, line ranges)
- Paper sections read (URL + section number/title)
