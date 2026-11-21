# ECCO (Can We Improve Model-Generated Code Efficiency Without Sacrificing Correctness?)

Status: critic-checked 2026-11-21 (6 fixes) · Last checked: 2026-11-21
Artifact: https://github.com/CodeEff/ECCO @ e86544618118a481d17a932e2a39df25d85d34cb (local clone: `C:\Users\pc\study\bt-lab\survey\CodeEff_ECCO`) · Paper: arXiv 2407.14044 (read PDF via pdftotext; section numbers per paper)
Evidence labels: **[src]** read in source (file path + line or paper section quoted/paraphrased), **[inf]** inferred by us from sources, **[unk]** not found (say where you looked).

## 1. What it is
- Python benchmark from CodeNet/AlphaCode problems: 1,380 problems, two tasks: history-based editing (slow -> fast) and NL-instructed generation. Test split: 48 problems, 794 pairs. [src] paper §3.2, Table 1.
- Execution is by a Judge0 server (Docker, sandboxed) on AWS EC2 `m7i.large`, shipped as an AMI. [src] paper §3.1 Fig. 2; evaluation/README.md @e865446 (AMI id, instance type).

## 2. Build / environment
- No build: candidate is Python 3 source sent as `source_code` with `language_id: 71`. [src] evaluation/utils.py:29-37 @e865446.
- One shared Judge0 server (prebuilt AMI) for all candidates; each submission is sandboxed per request by Judge0. [src] paper §3.1; evaluation/README.md.
- Limits per submission: `wall_time_limit` 20 s, `memory_limit` 512000 KB. [src] evaluation/utils.py:35-36.
- No build reduction concept. [inf]

## 3. Correctness tests per candidate
- Each test is one HTTP request (`/submissions/?wait=true`, synchronous), tests run sequentially in sorted file order. [src] evaluation/utils.py:39-42, 88-105.
- Tests: CodeNet originals = "public" (avg 3.14 train / 3.29 test), AlphaCode-generated extras = "private" (avg 17.21 train / 20.00 test); Table 1 split is 1,262/69/48 problems; expected outputs come from running canonical solutions. [src] paper §3.2 "Test Case Collection", Table 1.
- Use: public tests give execution feedback to the model (exec-refine); private tests are the final evaluation. Models never see private tests. [src] paper §3.2, §4.2 and footnote 5.
- pass@1 = candidate passes all test cases. [src] paper §3.3.3. In code, the final pass count is `len(pass_tests)` of status-3 (accepted) tests; best sample is the one with most passes. [src] evaluation/edit_eval.py:87-95, 124-125 (denominator `num_tests`, l.52-55).
- Quirk: `accept` is set False only for runtime errors/timeouts, not for wrong answer (status 4), so the returned `accept` flag is not a full pass flag; the per-test `pass_tests` list is what counts. [src] evaluation/utils.py:109-122 (valid = status 3 or 4, l.109; `accept=False` only in the else branch, l.112-113). [inf] a reader using `input_accepted`/`output_accepted` would over-count.
- `--num_tests` can truncate to the first N test files (a fixed prefix, not a selection). [src] evaluation/utils.py:91-92.
- Test selection per edit: [inf] none; fixed per problem; public/private split is by test source, not by relevance.

## 4. Performance measurement per candidate
- Time and memory returned by Judge0 per test; `number_of_runs` default 3 in eval script (1 in the refinement loop). [src] evaluation/edit_eval.py:16; experiments/inference.py:214-216. [unk] how Judge0 aggregates the runs (average vs. other); not in this repo, would need the Judge0 docs.
- Speedup = sum over tests of input time / sum of output time, **only over tests the candidate passed**; requires the input program to pass all tests and the best sample to pass at least one. [src] evaluation/edit_eval.py:139-151. [inf] a candidate failing most tests can still get a speedup number.
- Best sample chosen by max pass count, then smallest summed time. [src] evaluation/edit_eval.py:87-105 (ranking uses summed time over all tests that executed, incl. wrong-answer ones, l.99-102).
- Also memory reduction, and runtime/memory percentile versus other human submissions for the NL task. [src] paper §3.3.1 eqs. 1-2 (speedup, memory reduction), §3.3.2 eqs. 3-4 (runtime/memory %).
- No statistical test, no threshold such as 1.1x in the harness; the paper's "% optimization" uses its own thresholds [unk exact value; not read in Table 8 text].
- Noise controls: claimed hardware independence "thanks to its agnostic nature"; fixed instance type; sandboxed. [src] paper §1. Variance study: 3 sample generations, speedup/runtime% have ~1% 95% CI, memory ~5% in NL setting. [src] paper App. C, Table 9 (pass@1 has no variance across runs due to low temperature; two models only).

## 5. Cost per candidate (if reported)
- [unk] No per-candidate wall time or dollar cost found. Searched paper text for "cost", "seconds", "time per", and README.

## 6. Iteration / cumulative re-validation
- Iterative refinement: self-refine (NL feedback), exec-refine (public-test results), NL+exec-refine, 1-4 iterations. [src] paper §4.2.
- Each iteration runs the candidate on public tests only (`number_of_runs=1`). [src] experiments/inference.py:213-218, 282-287.
- Final evaluation runs private tests on the last program; paper finds more iterations raise speedup but lower pass@1 (exec-refine degrades least). [src] paper §6 "Does multi-iteration refinement help?" (not §5).
- Bug noted: refinement passes the literal string `'args.test_cases_path'` rather than the variable (quoted). [src] experiments/inference.py:215. [inf] likely a bug unless a dir of that name exists; do not rely on this path.

## 7. Limitations the authors state
- Python only; competitive-programming only; results may not generalise; recommend inspecting outputs in addition to metrics. [src] paper "Limitations".

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- Cleanest existing example of a staged test design: a small public set used for in-loop feedback, a larger held-out set for final acceptance. This is a fixed split, not per-edit selection. [src] paper §3.2, §4.2.
- Speedup is computed only over passing tests, which couples correctness and measurement; a reduced test set would change the denominator. [src] evaluation/edit_eval.py:139-151.
- Time measured via Judge0 on cloud with 3 runs; noise reported as ~1% CI for aggregates. [src] paper App. C. Good citation for "wall-clock can be stable enough when averaged over many tests".
- Evidence that refinement without re-validation on the full set loses correctness across iterations. [src] paper §6.

## Sources
- evaluation/utils.py L1-136, evaluation/edit_eval.py L1-179, evaluation/README.md @ e865446
- experiments/inference.py L10, 57-58, 205-220, 275-290 @ e865446
- Paper arXiv 2407.14044: §1, §3.1, §3.2 (Test Case Collection, Table 1), §3.3, §4.2, §6 multi-iteration, App. C, Limitations
