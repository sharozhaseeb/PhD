# W1 verification of refs.bib entries

W1-LIT checked these on 2026-11-22, **by reading only**. Sources:
- Crossref API (`api.crossref.org/works/<DOI>`, publisher-deposited metadata);
- the arXiv API (`export.arxiv.org/api/query`, abstract-page metadata);
- the publisher's or conference's own pages, found through search.

Nothing was downloaded or executed. `main.tex` and `refs.bib` were **not** edited; W6 applies the fields below.

Each entry's suggested note is `verified 2026-11-22 via <URL>`.

| Key | Status | Corrected fields | Source URL |
|---|---|---|---|
| `zhao2026semopt` | **verified, fields added** | Authors: Yuwei Zhao, Yuan-An Xiao, Qianyu Xiao, **Zhao Zhang**, **Yingfei Xiong**. Title as in bib. ACM TOSEM **35**(**11**), pp. **1–46**, **2026**. DOI **10.1145/3820167**. arXiv 2510.16384 (v2) has the same author list. | https://doi.org/10.1145/3820167 (Crossref); https://arxiv.org/abs/2510.16384 |
| `he2025sweperf` | **verified, authors added; venue note** | Authors: **Xinyi He, Qian Liu, Mingzhe Du, Lin Yan, Zhijie Fan, Yiming Huang, Yin Zheng, Zejian Yuan, Zejun Ma**. Title exact: "SWE-Perf: Can Language Models Optimize Code Performance on Real-World Repositories?". arXiv 2507.12415 (v2). The arXiv comment says "Accepted by ICML 2026". That is author-stated and not checked against ICML proceedings, so keep it as `@misc` with arXiv, or add the venue only after checking. | https://arxiv.org/abs/2507.12415 |
| `gso2025` | **verified, authors added** | Authors: **Manish Shetty, Naman Jain, Jinjian Liu, Vijay Kethanaboyina, Koushik Sen, Ion Stoica**. Title exact: "GSO: Challenging Software Optimization Tasks for Evaluating SWE-Agents". arXiv 2505.23671 (v3). No journal ref or DOI on arXiv. Suggested key: `shetty2025gso`. | https://arxiv.org/abs/2505.23671 |
| `yang2025wedge` | **verified; title fix** | The venue is confirmed by the NeurIPS proceedings: Advances in Neural Information Processing Systems 38 (NeurIPS 2025), Main Conference Track. The proceedings title has a prefix: "**WEDGE:** Synthesizing Performance Constraints for Evaluating and Improving Code Efficiency". Authors as in bib. | https://papers.nips.cc/paper_files/paper/2025/hash/6a4d5d85f7a52f062d23d98d544a5578-Abstract-Conference.html; arXiv comment "Accepted by Neurips 2025 (main poster)" |
| `henning2025when` | **verified, fields added** | Authors: **Sören Henning, Adriano Vogel, Esteban Perez-Wohlfeil, Otmar Ertl, Rick Rabiser**. Pages **400–410**. Crossref gives the title as "When Should I Run My Application Benchmark?". The arXiv title adds ": Studying Cloud Performance Variability for the Case of Stream Processing Applications"; either is defensible, so use the Crossref one for the published version. Container: Proceedings of the 33rd ACM International Conference on the Foundations of Software Engineering (FSE Companion '25). The arXiv comment says Industry Track. DOI 10.1145/3696630.3728563 resolves. | https://doi.org/10.1145/3696630.3728563 (Crossref); https://arxiv.org/abs/2504.11826 |
| `rodriguezguerra2021quansight` | **partly verified** | Author: **Jaime Rodríguez-Guerra** (handle jaimergp). Title exact: "Is GitHub Actions suitable for running benchmarks?". Published **18 August 2021**, Quansight Labs blog. URL confirmed. Basis: search-result metadata for the labs page and the dev.to cross-post. The labs page itself returned 429 earlier, so the body is still read only via the mirror. Keep "not peer-reviewed". | https://labs.quansight.org/blog/github-actions-benchmarks; https://dev.to/quansightlabs/is-github-actions-suitable-for-running-benchmarks-111h |
| `wohlin2024experimentation` | **verified, fields added** | Authors per Crossref: **Claes Wohlin, Per Runeson, Martin Höst, Magnus C. Ohlsson, Björn Regnell, Anders Wesslén**. Springer Berlin Heidelberg, **2024**, **2nd edition** (Springer listing: Edition Number 2; eBook 3 Sep 2024). DOI 10.1007/978-3-662-69306-3 resolves. Note: one search summary said Springer's page shows five authors; Crossref lists six. Use Crossref. | https://doi.org/10.1007/978-3-662-69306-3 (Crossref); https://link.springer.com/book/10.1007/978-3-662-69306-3 |
| `verdecchia2023threats` | **verified; no change** | All fields match Crossref. Authors Verdecchia, Engström, Lago, Runeson, Song; Information and Software Technology **164**, article **107329**, December **2023**. Crossref title casing: "Threats to validity in software engineering research: A critical reflection". | https://doi.org/10.1016/j.infsof.2023.107329 (Crossref) |
| `sjoberg2022construct` | **verified; year and fields fix** | Authors: **Dag I. K. Sjøberg, Gunnar Rye Bergersen**. Title exact. IEEE TSE **49**(**3**), pp. **1374–1396**. The issue year is **2023** (published 1 Mar 2023; the DOI suffix shows 2022 online early access). Use `year = {2023}`, and either rename the key to `sjoberg2023construct` or keep it and note the early access in 2022. | https://doi.org/10.1109/TSE.2022.3176725 (Crossref) |

**Summary.** All 9 entries were checked; none was invented. These need field changes:
- `zhao2026semopt`: last two authors, volume, issue, pages, DOI.
- `he2025sweperf`: author list.
- `gso2025`: author list.
- `yang2025wedge`: "WEDGE:" title prefix.
- `henning2025when`: given names and pages.
- `wohlin2024experimentation`: co-authors.
- `sjoberg2022construct`: year 2023, volume, issue, pages.

`verdecchia2023threats` is correct as is. `rodriguezguerra2021quansight` is verified for metadata only; its body is still read through the mirror.

**Not done here:**
- SWE-Perf's "ICML 2026" is author-stated on arXiv only; check it in the ICML proceedings before using it as the venue.
- The other "citations the draft still needs" in `W1-verify.md` are not covered here:
  - Wilson and Mann-Whitney primary sources;
  - the W2 survey artifact;
  - the B1/C11 search results.

  The B1/C11 results with safe wordings are in `01-literature/beyond-literature-claims.md`, section "Measured findings vs literature (2026-11-22)". Laaber & Leitner MSR 2018 remains abstract-only.


## Addendum (2026-11-22, 16:40): Laaber & Leitner MSR 2018 in full, and three [verify] candidates

All read-only. Details are in `01-literature/notes/N5-laaber-and-candidates.md`. Metadata for all four was confirmed through Crossref.

| Key / candidate | Status | What it measures, and how it differs from our B1 | Source URL |
|---|---|---|---|
| `laaber2018evaluation`: Laaber & Leitner, "An Evaluation of Open-Source Software Microbenchmark Suites for Continuous Performance Assessment", MSR 2018, pp. 119–130, DOI 10.1145/3196398.3196407 | **now read in full** (author version, saved to `01-literature/papers/2018-Laaber-Leitner-Microbenchmark-Suites-MSR.pdf`); was [A] | Ten Java and Go libraries. **Suite duration** under the authors' own JMH settings runs from 11 min (gin) to 8.75 h (RxJava). **Injected slowdowns**: a sleep slowdown is added to each of 20 frequently used API methods per project. A method counts as "covered" if some benchmark **detects** that slowdown (Wilcoxon p < 0.01 and a mean change of at least half the slowdown). ABS is the share of covered methods, 10–100%. No real commits are studied. **Difference from B1:** their "covered" means *detected*, not *executed*, and the methods are sampled API methods, not those changed by real optimization commits. Reach (B1) is necessary for ABS but a weaker property. | http://www.ifi.uzh.ch/dam/jcr:ccf1399a-2d57-4ff9-a3b0-59d69616d5d3/msr18-author-version.pdf |
| **Traini et al.**, "How Software Refactoring Impacts Execution Time", ACM TOSEM 31(2), Article 25, 2021 (issue 2022), DOI **10.1145/3485136**. Nine authors: Traini, Di Pompeo, Tucci, Lin, Scalabrino, Bavota, Lanza, Oliveto, Cortellessa. | **verified; read in full** (author-hosted PDF). **Closest prior work to B1.** Not in `refs.bib`; suggested key `traini2021refactoring`. | 31 Java projects with JMH suites. They profile, per commit, which methods each benchmark executes at the pre- and post-commit snapshots (Java Flight Recorder). A benchmark is "suitable" for a refactoring if it executes at least one method the refactoring touched. Of 3,343 retained commits, 201 have a suitable benchmark (3,533 data points). Benchmark execution is measured per commit, as in B1, but: (i) the commits are **refactorings**, not performance-improving commits; (ii) Java/JMH, not Python/asv; (iii) the paper reports no covered/uncovered rate as a finding. The ≈ 6% (201/3,343) is **our derivation** and is unconfirmed; do not quote it as theirs. | https://rocoli.github.io/pubs/tosem2021refactoring.pdf; https://doi.org/10.1145/3485136 |
| `chen2017exploratory`: Chen & Shang, "An Exploratory Study of Performance Regression Introducing Code Changes", ICSME 2017, pp. 341–352 | **verified**; local PDF read | Java (Hadoop, RxJava). It reports **no** count of commits covered or uncovered by the tests or benchmarks run; uncovered changes are only a threat to validity. **Difference from B1:** does not measure reach. | `01-literature/papers/2017-Chen-Exploratory-Perf-Regression-Changes-ICSME.pdf` (Crossref-confirmed) |
| **Jangali et al.**, "Automated Generation and Evaluation of JMH Microbenchmark Suites from Unit Tests" (ju2jmh), IEEE TSE 2023 | **verified; read** | It measures execution coverage of **injected mutants** by manual vs generated JMH suites. Manual JMH covers 29.7% per Table 7, while the text says 66%; this inconsistency is in the source. It checks one real bug and no real optimization commits. **Difference from B1:** injected mutants and generated benchmarks, not the project's own suite on real optimization commits. | see `notes/N5` for the DOI and URL |

**Suggested changes for W6** (the text is W6's to edit):
1. In `sections/background.tex` line 42, Laaber & Leitner's ABS measures *detection* of injected slowdowns, which is stronger than execution. Suggested wording: "...evaluate how well suites detect slowdowns injected into sampled API methods; we measure a weaker, necessary property, whether the suite executes the functions that real optimization commits change."
2. Cite **Traini et al. (TOSEM 2021)** as the closest method precedent. They profile which methods JMH benchmarks execute, per commit, for refactoring commits in Java. Our B1 applies the same kind of measurement to real performance-improving commits in Python with asv, and reports the uncovered fraction. B1 stays "not found in our recorded searches" only as *the rate for performance-improving commits*. Do not claim "first to profile benchmark reach per commit".
3. Chen & Shang and Jangali can be cited as context; neither measures B1's quantity.
