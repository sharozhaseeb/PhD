# SemOpt

Status: critic-checked 2026-11-21 (5 fixes) · Last checked: 2026-11-21
Artifact: figshare package (private link, not opened): https://figshare.com/s/0391db49a3620ed53a1f · Paper: "SemOpt: LLM-Driven Code Optimization via Rule-Based Analysis", Zhao, Xiao, Xiao, Zhang, Xiong (Peking Univ.), TOSEM 2026; arXiv:2510.16384 (local: `C:\Users\pc\study\PhD\research-directions\llm-optimization-validation\papers\2026-SemOpt-TOSEM-author-version.pdf`, 47 pp., "Manuscript submitted to ACM")
Evidence labels: **[src]** read in source (file path + line or paper section quoted/paraphrased), **[inf]** inferred by us from sources, **[unk]** not found (say where you looked).
Page numbers are the manuscript's own page numbers, approximate (+-1), since the text was extracted with pdftotext.

## 1. What it is (2–3 lines)
Function-level LLM optimizer for C/C++ and Python. It builds a strategy library from mined optimization commits, generates Semgrep rules that locate where each strategy applies, then prompts an LLM with the matched strategies. [src] Abstract, Sec. 3.
It is not an iterative agent. Candidate validation is split in two: Sec. 4 (benchmark, no tests) and Sec. 5 (in-the-wild, build + tests + perf runs). [src] Sec. 4.1.5, 5.1.2.

## 2. Build / environment
- Sec. 4 benchmark: no build or test run per candidate. Success is Exact Match with the developer's patch, or Semantic Equivalence judged by the authors manually. [src] Sec. 4.1.5 (p.17-18). (The authors compare patches manually; the "at least one solution" rule means a task counts as solved if any candidate qualifies.)
- Sec. 5 in-the-wild: for each project "apply the optimization, compile the code (for C/C++) or install the package (for Python)", then run the unit tests. C/C++ builds in release mode with the project's default optimization level. [src] Sec. 5.1.1-5.1.2 (p.31-32).
- Repos: RocksDB, Redis, gRPC, LevelDB, spdlog (C/C++); click, flask, jinja, requests, scrapy (Python). [src] Sec. 5.1.1.
- A scripted compile / install per project is used. Incremental builds, caching and skipped build steps are not mentioned. [unk]
- Candidate compile success: 73.72% of 8,082 candidates compile (C/C++). [src] Sec. 5.3, Table 16 (p.34). Compilation failures are also a listed failure mode of the applicability metric. [src] Sec. 4.7.

## 3. Correctness tests per candidate
- Sec. 4 (benchmark of 151 C/C++ and 150 Python tasks): no tests run. Equivalence is by exact string match after normalization, or by manual review of the diff. [src] Sec. 4.1.5.
- A manual applicability check was done only for DeepSeek-V3 on C/C++: 89.86% of suggestions preserve semantics and improve performance. [src] Sec. 4.3.6.
- Sec. 5: after the build, "execute the unit tests on the optimized code. If the tests are passed" the perf tests run. Test pass rate: 72.43% for C/C++ and 100% for Python (of the candidates produced; 9,483 Python candidates from 152 hotspot functions, all pass). [src] Sec. 5.1.2, 5.3, Table 16 (p.33-34); not Sec. 4.3.6, which is the manual applicability check. The 100% Python pass rate is unusually clean and the paper does not say how many tests exist per project or what they cover. [unk]
- In addition the authors "manually validated the optimized code for semantic correctness" and report all final C/C++ and Python optimizations equivalent. [src] Sec. 5.3 (p.33). Sec. 6.2 adds that human review is still required before adoption. [src]
- Which tests: the project's built-in unit test suite and built-in performance tests. No per-edit selection is described; this reads as the whole project suite per candidate. [inf] from Sec. 5.1.2 (text says "the built-in unit and performance tests").
- Hotspot functions are chosen from a profile of the perf tests: functions with >0.1% of runtime (perf + gcov for C/C++; cProfile + line_profiler for Python). That chooses WHAT to optimize, not which tests to run. [src] Sec. 5.2.1.

## 4. Performance measurement per candidate
- Workload: each project's own performance test suite: 2-45 test cases for C/C++ and 4-11 for Python. [src] Sec. 5.1.1.
- Repeats: 6 runs of the perf tests on both original and optimized; the first run is discarded for cold start; the reported number is the average improvement over the remaining 5 runs. [src] Sec. 5.1.2.
- Effective candidate: improvement > 5% on at least one test case and no more than 2% degradation on any other. [src] Sec. 5.2.2 (p.33).
- Noise control: no other resource-heavy program on the server during runs; server was 4x Xeon Platinum 8270 (104 cores), 256 GB. No pinning, isolation or instruction counting mentioned. [src] Sec. 5.2.3.
- Perf is measured only in Sec. 5, not in the 301-task benchmark. [src] Sec. 4.1.5, 5.

## 5. Cost per candidate (if reported)
- No dollar, token or time cost per candidate reported in the text searched (searched for overhead, tokens, seconds, minutes, USD). [unk]
- Overhead remarks: skipping clustering "would increase by 5x" the optimization overhead (Sec. 6.1); Semgrep ranking (top-N) is used to avoid wasted LLM calls (Sec. 4.2.4, 4.8). Each task is run 3 times at temperature 0 (Sec. 4.1.6). [src]
- Scale in Sec. 5: 8,082 candidates from 226 hotspot functions in the C/C++ projects (not all 10 projects; architect fix 2026-11-21 against PDF text, Sec. 5.3 lines 1710-1711). [src] Sec. 5.3.

## 6. Iteration / cumulative re-validation
- No LLM iteration or feedback loop per candidate: generation is single-pass (several candidates per function, from top-N strategies). [src] Sec. 3.3, 4.2.4; related work states SBLLM, EffiCoder (profiling-guided) and PerfCodeGen (iterative test feedback) are called "orthogonal" and could be combined. [src] Sec. 7 (p.37-38).
- Composition step (Sec. 5.2.2): per function, pick the variant that meets the criteria with the highest summed improvement; if none meets them, keep the original; "assemble the selected optimizations for all hotspot functions" into the final project version. [src] p.33.
- Whether the assembled whole-project version is rebuilt and re-tested before the final numbers are reported is not stated explicitly. The reported Table 15 figures are measured on the final project versions, so a perf measurement of the combined result presumably exists. [inf] The unit-test pass of the combined version is not stated. [unk]
- Interactions between edits in different functions are not discussed. [unk] (searched Sec. 5.2, 6.4).

## 7. Limitations the authors state
[src] Sec. 6.4, 6.5 (p.36-37) unless noted:
- Single-function scope only; multi-function edits are future work.
- Strategy types limited by what Semgrep can express.
- Data leakage via LLM training data; benchmark drawn from top-100 starred repos, three LLMs.
- Sec. 4 correctness rests on EM and manual equivalence, which can undercount valid but different optimizations (Sec. 4.3.6).
- Raw Semgrep scan precision is 1.56%; recall 82.78% (Sec. 4.8).

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- The in-the-wild protocol is a full compile/install + full unit tests + 6x perf runs per candidate, with 8,082 candidates produced. [src] Sec. 5.1.2, 5.3. That is the cost profile that reduced build and test would attack. [inf]
- Candidate filtering is staged: build, then unit tests, then perf (build 73.72% pass, tests 72.43% pass). [src] Table 16. So failures are caught early and perf is only spent on survivors. [inf]
- Accept rule (>5% on one test, <=2% regression on the rest) and per-function composition is a ready-made per-edit acceptance rule, and the composition is a place where cumulative re-validation would matter. [src] Sec. 5.2.2. [inf] on the second part.
- No test selection, no incremental build, no deterministic metric (none described; the text only says unit and performance tests are run). [inf] Timing is wall clock, quiet machine. [src] Sec. 5.2.3.

## Sources
- Paper read via `pdftotext -layout` on the local PDF, text parsed in a pipe (no file written): Abstract; Sec. 1; Sec. 4.1.1, 4.1.5, 4.1.6, 4.3.6; Sec. 4.8 (end), Table 15; Sec. 5.1-5.3; Sec. 6.1, 6.4, 6.5; Sec. 7; Data Availability. Read with the `Read` tool failed (pdftoppm not installed), so text came from pdftotext.
- Sections 3.x, 4.2, 4.4-4.7 and the appendix prompts were searched by keyword but not read in full.
- Public artifact search: Data Availability states the implementation, baselines and results are at the figshare URL above. The link is a private-share link and was not opened (not fetched). A web search for "SemOpt ... github replication package" found the arXiv (2510.16384), alphaXiv and other pages but no GitHub repository. [unk] for GitHub.
