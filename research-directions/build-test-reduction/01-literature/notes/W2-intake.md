# Inputs from W2 for closest-works and the claims list (received 2026-11-21)

Checked against W2's per-system files on 2026-11-21. These points are not re-researched here; each one cites the W2 file.

1. **PerfAgent** (arXiv 2607.19653v1). It selects tests for every edit with pytest-testmon, using coverage (§III-D; reported test reduction 66–99% on GSO and 47–98% on SWE-fficiency-Lite). It states that testmon tracks only Python coverage, so regressions in native extensions can slip through (§VI). The W2 reader could not read supplemental Section B. Source: `02-practice-survey/per-system/perfagent.md` lines 20–25, 50.
   → It goes in closest-works. **Do not claim** "first per-edit test selection for optimization."
2. SWE-Perf, GSO and SWE-fficiency fully rebuild every candidate. Tag "no surveyed optimization system reduces the build" as **found-by-survey (W2)**, not as a literature gap. Sources: `02-practice-survey/per-system/{swe-perf,gso,swe-fficiency}.md`.
3. Precedents for cumulative or periodic re-checks:
   - **SysLLMatic.** Accepted candidates accumulate and the final app is rebuilt and re-measured (Algorithm 1 l.14–23, §6.4.1). No cumulative test re-run is described. Source: `sysllmatic.md` l.28–29.
   - **Meta.** All tests run on master every few hours (stabilization stage). Source: `industrial-ci-test-selection.md` l.31.
   - **Google.** Milestone batching plus culprit finding. Source: `industrial-ci-test-selection.md` l.41.
