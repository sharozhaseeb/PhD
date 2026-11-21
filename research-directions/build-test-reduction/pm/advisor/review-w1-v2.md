# Advisor-persona review of W1 literature draft v2

Reviewed 2026-11-21. I read in full:
- `01-literature/README.md`
- `closest-works.md`
- `beyond-literature-claims.md`
- `gap-and-search-log.md`

I skimmed the outline of `review.md` and its §6 synthesis.

Reviewer: advisor-persona subagent (AI-SIM, not the advisor). I did not re-check the cited sources. The critic pass and evidence labels are taken as given.

## Verdict

**Strong and honest. Answers Q2. The claims list needs pruning and the contribution needs reframing before the meeting.**

The draft does several things an advisor rewards:
- it names what is *not* new (per-edit selection inside an optimization loop, periodic full runs, batching and bisection, comparison against a stable baseline);
- it labels every claim with an evidence level;
- it records the searches;
- it says plainly that it is not a systematic review.

The weak point is its own last line: "The contribution is the **combination**". The earlier AI-SIM reviews already warned that combining known parts is not a contribution (`2026-09-07-pivot-advisor-review.md`: "A novel name for combining familiar selectors is insufficient"). A sceptical advisor will go straight there.

## 1. Does it answer predicted Q2, "what's new compared with Ekstazi, STARTS, testmon and incremental builds"?

**Yes, explicitly.** There is a section with that title in README.md and in closest-works.md, with 19 works compared.

The advisor's follow-ups will hit the five answer points unevenly:

| Answer point | Will it hold up? |
|---|---|
| 1. State kept across edits, and a full check triggered by accumulated change | **Weakest of the "new" claims as stated.** Expect: "Isn't that batching with a variable batch size?" Both fixed-size batching (#8) and risk-aware batching (#17, Sayedsalehi 2026) are close. The useful part is *stale dependency and profile data across edits* (C7). That is a mechanism to measure, not a trigger to propose. Also, the W3 design currently gives accumulation little chance to matter: each injected fault sits in the function the edit changed (see `review-w3-readiness.md`, change 3). |
| 2. Choosing benchmarks, not tests, per edit, for Python | **Narrow it.** "Done for Java, Go or C/C++ but not for Python" is a language-transfer gap. The AI-SIM reviews call that weak novelty. The defensible part is a measured miss rate for *dropping* benchmarks per edit (C11), because the literature mostly orders benchmarks rather than dropping them. |
| 3. Two-sided oracle | **Not new.** SemOpt's acceptance gate already has two sides: more than 5% better on at least one test, and no more than 2% worse on the others (TOSEM p. 32). PerfAgent keeps a patch only if it is faster and the tests pass. Present this as part of the method, not as a contribution. |
| 4. Culprit finding over dependent edits with noisy verdicts | **Out of Study 1 scope and under-read.** BISCEPTER was not read. Defer it. |
| 5. Rebuild correctness for Python extensions (B4) | **Credible, small, and empirical.** Keep it, but as a finding W3 measures, not as a technique. |

## 2. Would the claims list survive a sceptical advisor?

| ID | Keep, narrow or strike | Reason and suggested wording |
|---|---|---|
| C1 accumulated-change trigger | **Narrow** | "We found no evaluation of a deterministic accumulated-change trigger against fixed-k batching at matched cost on optimization edit sequences." Fallahzadeh et al. (EMSE 2025, selection against batching) must be read before the meeting. It is the most direct threat and is so far abstract-only. |
| C2 PerfAgent per-edit selection | Keep (prior work) | Good. This is the honesty the advisor values. |
| C3 no optimization system reduces the build | Keep as **motivation** from the W2 survey | It is not a literature gap; the list already says so. Pair it with the SemOpt candidate counts (TOSEM Table 16) and the W3 RQ1 numbers. |
| C4 no Python benchmark-selection study | **Strike as a separate claim**; fold it into C11 | It is a language-transfer gap. |
| C5 Python RTS across the C-extension boundary | **Keep; lead with it** | It is concrete: PerfAgent names it as a limitation (§VI); RTSLinux and BinaryRTS show it matters on the JVM; W3 can measure it with `sys.monitoring`. Best "beyond the literature" item. |
| C6 cumulative drift as a selection problem | Narrow | "Named (Daly 2020) but not evaluated against per-edit selection." Fine at **partial**. Do not promote it. |
| C7 RTS safety with dependency data that is not refreshed across several revisions | **Keep; make it the core mechanism** | This is what "accumulation" actually means for safety. Ekstazi §5 states the limitation. It can be tested in W3: refresh the dependency map every k steps against every step, and count misses. |
| C8 rebuild correctness for Python extensions | Keep, small | Empirical finding (W3 §4.3). |
| C9 detection-delay metric | **Strike as a claim** | A metric definition is a method choice. Say only that the metric extends Jin & Servant's delayed-observation dimension. |
| C10 combined culprit finding | **Strike for Study 1** | Partial; BISCEPTER unread; not in the Study 1 RQs. |
| C11 miss rate when dropping benchmarks by coverage | **Keep, broadened** | Absorbs C4. Grambow and Ding are partial precedents. The claim is a reported, per-edit miss rate for Python benchmarks, including native code. |

**Suggested reframing** (one sentence for the meeting):

> Study 1 measures where existing deterministic build and test reduction becomes unsafe when edits are performance-motivated and accumulate. The suspected mechanisms are three: native-extension boundaries (C5), dependency and profile data going stale across edits (C7), and dropped benchmarks (C11), plus incremental-rebuild correctness (C8). It then tests whether simple rules that target those mechanisms close the gap at matched cost.

This leads with **empirical knowledge** and treats the policy as a consequence. Of the framings available, it is the one most likely to clear the "go beyond the literature" bar.

## 3. What is missing before the meeting

1. **Read the five threatening works in full**, not as abstracts or W2 summaries:
   - PerfAgent §III-D and §VI. It is the closest work, so the advisor will ask how it validates and whether it reports misses.
   - Fallahzadeh EMSE 2025.
   - Sayedsalehi 2026.
   - BISCEPTER, or drop C10.
   - arXiv 2512.22256.
2. **Forward-citation screening of PerfAgent and NameRTS.** Both are 2026, so there are few citers and this is cheap. Without it, "not found" means little for the newest area.
3. **Decide whether NameRTS is a baseline.** It is the strongest Python selector the draft found (−45.6% time, safe on 99.6% of commits). W3 uses testmon only, so expect "why not compare with NameRTS?" Record whether an artifact exists. If it does not, say so.
4. **One positioning figure.** A grid with rows for the decision unit (per revision against across edits) and columns for the object reduced (build, tests, benchmarks), with the 19 works placed in it. Our cells are: across edits, all three objects, Python with native code. This answers Q2 in ten seconds.
5. **A claim-to-evidence map.** For each kept claim (C1, C5, C7, C8, C11), the W3 measurement that will support or refute it. C1 and C7 currently have no W3 arm that can show an effect; see W3 review change 3.
