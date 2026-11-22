# What to avoid (toolkit §5) and the must-not-claim list (TPM §4)

## 5. What to avoid

1. **Fabricated or misattributed citations.**
   - Never cite from model memory. This applies even to titles that look certain, such as the "titles from memory" in TPM R-6. Every `refs.bib` entry needs a fetched source: a DOI that resolves, or a publisher or arXiv page that was read.
   - Each entry gets a `note = {verified <date> via <URL>}` field.
   - Template 4.4 enforces sentence → citekey → quote.
   - The pages behind the [S] items in §1e must be fetched before they are cited. Georges et al. has two candidate DOIs.
2. **Unverifiable or hand-typed numbers.**
   - Every number comes from `numbers.tex`, and every macro carries a comment naming its raw file and its computation, plus the sha256 from `data-manifest.yaml`.
   - The text never shows a point value for something the data gives only as a range (drift, R1 8–28×).
   - `make check` must pass before any review.
3. **Claims beyond evidence.**
   - The 16-item must-not-claim list (TPM §4) is pasted into every drafting and review prompt.
   - Banned without a recorded novelty search: "most", "first", "novel", "gap", "significant" (unless it names a test).
4. **Models filling silence.**
   - Every template lets the model say "missing" or "not supported", and asks for `<missing_macros>`, `<search_requests>` and `<unmitigated>` instead of invented content (Reduce hallucinations: allow "I don't know").
5. **Style tools that change meaning.**
   - Do not run anti-ai-writing-style rewriters over claims, hedges or numbers.
   - Language polishing is the last step, and a diff is checked against macros and hedges afterwards.
6. **Reviewer echo.**
   - The reviewer subagent must not see the drafting conversation or the PM's notes. It sees only the paper and the standards.
   - Do not hand it our own threats table (advisor §3) first, or it will confirm that table instead of finding new attacks. Compare the two afterwards.
7. **Running downloaded code**, such as K-Dense's scripts, without the owner's approval.
8. **Uploading the draft** to third-party services (letX, Overleaf, remote citation checkers) without the owner's approval.
9. **AI-use disclosure.**
   - Follow the chosen venue's policy, and check it when the CFP is verified.
   - The owner re-derives every headline number from the raw files before submission (advisor §3, last row).


## Must-not-claim (pm/tpm-paper-plan.md §4, copied 2026-11-22)

1. **B1 generalises.** Not until (a) succeeds. Do not say "most" optimization edits are unbenchmarked. networkx is 9/15 true optimizations (60 %, CI 36–80 %), one project, one base profile.
2. **The Q3 static counts as replication** (geopandas 18/20, pvlib 14/14, bottleneck 4/8 or 0/8). They are a pilot that motivated (a), not evidence.
3. **Reduced selection is regression-safe**, or "0 of 50 slower" (withdrawn, no power), or P5 as safety evidence. P5 is a profile-completeness check with one unconfirmed flag (#9).
4. **A regression verdict that passes the 1 + 3σ floor**, until (b) has been run for that case. Until then, report the asv-rule verdict plus the deviation.
5. **A4 (our policy) beats testmon, batching or anything else.** N1, N4 and N5 are honest negatives. No accumulation benefit (N4 null). A4 behaves like periodic full checks at k ≈ 4.
6. **Wall-clock speed-ups or cost ratios from a single pass**, or as point values. R1 is 8–28×, with ≈ 8× at the median, and is "setup-dominated". The setup-cached ≈ 1.5–2× is an **estimate**.
7. **"10×" drift**, or any stated cause of the drift.
8. **Build savings for pure Python.** networkx build is ≈ 0.15 % of a pass. Bottleneck is ≈ 16–18 % of build + tests, noisy, 8 edits.
9. **H1 (stale-binary false pass) as a natural-edit hazard.** It is a replay artefact and a harness lesson. Do not call `iterators.h` an open upstream bug, and do not use B4 (invalid as specified).
10. **testmon "15–35×".** It is 3.5–4× end-to-end, under mixed load. Do not present the worked edit (≈ 6×) as a session result.
11. **"Iterative session" or accumulation effects** from replaying non-adjacent historical commits (T1). Use "replayed edit sequence".
12. **"Optimization commits" for regex hits.** Only manually confirmed optimizations count (R-4).
13. **Measured profiles as complete reach.** C7 shows 2.4 % nondeterministic attribution; profiles come from one state (S0) unless (a) measures per parent.
14. **Generality beyond the projects, Python versions, WSL and one laptop.**
15. **Any "first", "novel" or "gap"** without W1's recorded search (R-6).
16. **Anything about AI or LLM-based selection.** It is out of scope (Charter rule 2). LLM tools that helped write must be disclosed per the venue's policy (owner's call).
