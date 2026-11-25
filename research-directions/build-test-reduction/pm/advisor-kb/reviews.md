# Advisor KB reviews

All reviewers are AI subagents (AI-SIM for the advisor persona). None of this is the real advisor's view.

## Design review, round 1 (design.md v1), 2026-11-24

| Reviewer | Verdict | Required changes (summary) |
|---|---|---|
| TPM (truthfulness, sources) | **FAIL** | (1) §1 takeaway overclaimed: not every system builds, tests and benchmarks every candidate (GSO 0 unit tests; FormulaCode no per-edit rebuild, tests once on final tree); fill chips from the practice survey. (2) E1 is not pre-registered yet: say "planned, to be pre-registered", retitle "extension plan". (3) Cost tile must give the range: ≈ 8× fastest, ≈ 14× median, up to ≈ 34×; mark 2.2–2.3× as 3 pairs, one fast night. (4) Tag 484–504 s as R §E5 inferred; drop the 72 %; 35 h is inferred; never use stale NxSetupCached (1.5–2×) or NxBuildShareBench (0.15 %). |
| Advisor persona (AI-SIM) | **FAIL** | (1) Add the worked bidirectional_dijkstra example and make it the A1 token. (2) Show the four RQs. (3) D3 as three separate panels with own n, no funnel; show static 3/14 beside profile 8/14. (4) "What this is not" box at the top, scope chip on every tile, A14 as a decision with options and costs; §5 says the swap did not remove the flips and #8 is uncounted. (5) E5 fast night, 3.54× not a strict lower bound, gap inferred; label the A2 morph "inferred". (6) Keep the cost range, never "at least". (7) Cut D1 to 3 rows + ours; benchmark studies only in §6. (8) Say the 3–4-project TODO is not the plan. |

All items were addressed in design.md §3 (v2 revisions).

## Design review, round 2 (design.md v2), 2026-11-24

| Reviewer | Verdict | Notes |
|---|---|---|
| TPM | **PASS** | All four items covered; row 5 (step-2 edit) checked against `03-experiment/edits/networkx.candidates.json` and results.md (0/171 profile, 171/171 static). Optional: add "in our recorded searches" to the §1 takeaway. **Applied.** |
| Advisor persona (AI-SIM) | **PASS** | All 8 items covered; A1 labelled as a schematic of the real edit is right. Non-blocking: one machine wording everywhere (applied: "one laptop, WSL2"); Wilson-too-narrow caveat on the trust figure itself (applied, in its caption); keep the cost tile as a range (kept). |

## Build: critic number check (published v1), 2026-11-24

Independent critic subagent, against numbers.tex > findings.md > results.md, plus the practice survey and deck-brief: **CLEAN**. Every value, every overclaim guard and every SVG position (cost bars at 0.8 px/s, ratio axis, interval axis, dot counts) matched. Minor notes applied in v2: "most of the loss" became "much of the loss"; the E1 dashed band narrowed to ±14; the evidence-trail list of surveyed systems now names them. Note 3 (80–95 mined vs the brief's 70–85): the page follows deck-factsheet §3, which adds ≈ 10 % replay loss. Kept.

## Final advisor-persona review of the published page (v2), 2026-11-24

Advisor persona (AI-SIM): **PASS**, no required changes. Read the text only; did not render animation timing, SVG layout or dark theme (the architect checked the rendered page once in the browser pane before publishing). Optional notes, not applied: "measured on agent labels" on the 8/14 tile (the scope chip already says agent labels); 80–95 sourced from factsheet §3 (confirmed by the critic).

Artifact (private): https://claude.ai/artifact/EB7upXGnxjGu1SQh7ihM4y. Source copy: `pm/advisor-kb/kb.html`.
