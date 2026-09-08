# Methods and novelty map

Checked 7 September 2026. This document records primary-source methods relevant to validating LLM-generated Python performance changes. Entries distinguish peer-reviewed publications, preprints, and implementation documentation. The methods were not experimentally reproduced in this review. Claimed gaps below are advisory inferences, not assertions that no related work exists.

Follow-up: see the [benchmark plan](./2026-09-07-benchmark-plan.md) for concrete comparisons, including algorithm racing, a stronger characterization of SWE-Pro's noise handling, and the distinction between final-only and repeated approvals.

Latest follow-up: the [pivot advisor review](./2026-09-07-pivot-advisor-review.md) adds PerfAgent, Perun, APOLLO, performance-evolution studies, and iterative code-quality research. These further limit novelty claims based on iteration, profiling histories, and regression diagnosis alone.

| Work | Status verified in this review | Implemented or described method | Implication for the proposed PhD |
|---|---|---|---|
| [PerfAgent](https://arxiv.org/html/2607.19653v1) | July 2026 preprint; complete public implementation not located in this search | Profiler-guided iterative optimization, selective behavioral validation, best-patch selection | Particularly close overlap; workload generalization is explicitly discussed as a limitation |
| [Perun](https://github.com/Perfexionists/perun) | Public tool and 2022 paper | Version-linked performance profiles, degradation detection, modeling, and performance fuzzing | Tracking and diagnosing performance across versions is established |
| [APOLLO](https://github.com/sslab-gatech/apollo) | PVLDB paper and public repository | SQL performance-regression fuzzing, query reduction, and diagnosis | Input minimization and regression diagnosis need differentiation beyond a language change |
| [Performance evolution of configurable systems](https://link.springer.com/article/10.1007/s10664-023-10338-3) | Empirical Software Engineering, 2023 | Performance-influence analysis across releases and configurations | Longitudinal and configuration-specific performance change is established research |
| [SlopCodeBench](https://arxiv.org/abs/2603.24755) | March 2026 preprint | Iterative coding benchmark measuring structural quality and functionality | Iteration alone is not novel; runtime-policy mechanisms need distinct evidence |
| [PerfCodeGen](https://arxiv.org/abs/2412.03578) | Research paper; inspected arXiv version | Iterative code refinement using correctness and runtime execution feedback, including a costly test as feedback | Execution feedback and selecting among optimized candidates are established |
| [ECCO](https://arxiv.org/abs/2407.14044) | Research paper; inspected arXiv record | Efficiency/correctness benchmark; studies prompting, execution-informed refinement, and fine-tuning | A combined correctness-efficiency evaluation is not itself a gap |
| [COFFE](https://www.yunpeng.site/projects/coffe/) | FSE 2025 | Contract-based stress-test generation; CPU instruction counts for efficiency comparison | Generating large valid inputs and reducing timing noise already have dedicated methods |
| [WEDGE / PERFFORGE](https://proceedings.neurips.cc/paper_files/paper/2025/hash/6a4d5d85f7a52f062d23d98d544a5578-Abstract-Conference.html) | NeurIPS 2025 | Synthesizes branch constraints to guide fuzzing into performance-specific regions | New test generation must outperform a strong performance-directed search baseline |
| [Mokav](https://www.sciencedirect.com/science/article/pii/S0164121225002407) | Journal of Systems and Software, 2025 | Execution-guided LLM search for inputs exposing behavioral differences between Python program versions | Differential correctness testing with an LLM is already implemented |
| [Codeflash](https://docs.codeflash.ai/codeflash-concepts/how-codeflash-works) | Product documentation and public source | Candidate generation, existing/generated/concolic tests, behavioral comparison, benchmarking | The broad proposed pipeline has close industrial prior art |
| [FormulaCode](https://formulacode.org/) | Project identifies acceptance at ICML 2026 | Repository-level benchmark with many workloads and measures of aggregate improvement and regressions | Multi-workload evaluation and aggregate-versus-worst-workload trade-offs are established |
| [SWE-Pro](https://arxiv.org/html/2606.25530v1) | June 2026 preprint; publication acceptance not verified | Parameterized workloads, runtime/memory measurement, calibration, adaptive repetitions and time cap | Especially close overlap with the earlier proposed adaptive testing pipeline |
| [Rethinking Code Performance Benchmarks for LLMs](https://arxiv.org/html/2607.07619v1) | July 2026 preprint; publication acceptance not verified | Repeated statistical comparisons and a generate/diagnose/repair test-generation workflow | A generic benchmark re-evaluation or multi-agent performance-test generator needs stronger differentiation |
| [Applying test case prioritization to software microbenchmarks](https://link.springer.com/article/10.1007/s10664-021-10037-x) | Empirical Software Engineering, 2021 | Greedy total/additional coverage ranking, static/dynamic coverage, and change-aware ordering | "Run relevant tests first" is established, with substantial comparative evidence |
| [Dynamically reconfiguring software microbenchmarks](https://www.ifi.uzh.ch/dam/jcr%3A2e51ad81-856f-4629-a6e2-67d382d337c2/fse20_author-version.pdf) | ESEC/FSE 2020 | Stops microbenchmarks dynamically using statistical stability criteria | Adaptive stopping in software performance measurement predates LLMs |
| [µOpTime](https://arxiv.org/html/2501.12878v1) | TOSEM 2025, DOI 10.1145/3715322 | Uses earlier benchmark runs and stability metrics to select repetition counts | Repetition-budget reduction and historical calibration already exist |
| [Stop When It Matters / TT-MDE](https://zenodo.org/records/21760554) | Authors' lab lists ASE 2026; public artifact inspected, full paper not retrieved | Detectability-guided stopping; artifact includes tracker and hypothesis-decision code, A/A and power/FPR studies | Do not claim detection-based stopping or error-rate evaluation as absent; full-paper comparison is a priority |
| [Rapid Regression Detection](https://arxiv.org/abs/2205.14762) | KDD 2022 | Sequential tests for software deployment regressions with false-detection control | Continuous monitoring and early stopping with statistical guarantees are established tools |
| [Efficient Sequential Evaluation of Large Language Models](https://arxiv.org/abs/2607.17409) | July 2026 preprint | Confidence sequences and active querying on a fixed question set using historical model data | Active selection plus sequential uncertainty is already being studied in adjacent LLM evaluation |
| [Differential Performance Fuzzing of Configuration Options](https://doi.org/10.1109/SBFT66712.2025.00014) | SBFT 2025 workshop | Uses comparative performance feedback to find input-dependent violations of configuration expectations | A relative-slowdown fuzzing objective is not a new idea by itself |
| [Beyond Reproduction](https://socs.uoguelph.ca/~lliao01/web-home/publications/Renmin_ICPE_2026.pdf) | ICPE Companion 2026, work in progress | Uses issue context and LLM-generated structured mutations to explore latent performance regressions | LLM-guided regression discovery is active prior art; evidence is preliminary |
| [ACCLAIM](https://arxiv.org/html/2604.04238v1) | April 2026 preprint inspected | Compiler/LLM cooperation across abstraction levels, testing, and budgeted agent calls | Generic orchestration and computational-budget allocation are also established; its budget is not a validation-time policy |

## Available implementation material

These links were observed in primary sources or inspected directly. No private access, installation, or benchmark execution was attempted.

| Artifact | Availability established | Likely use |
|---|---|---|
| [Codeflash source](https://github.com/codeflash-ai/codeflash) | Public repository; selected verification/comparison files read at commit `a3a38efc9ec3d0a52a23056fd0a069863398a7ce` | Industrial baseline and implementation reference; full end-to-end behavior was not audited |
| [Mokav](https://github.com/ASSERT-KTH/mokav) | Public implementation with experiments and data described | Behavioral differential-testing comparator |
| [PERFFORGE](https://github.com/cirrus-uchicago/perfforge) | Public author repository describing tests and synthesis traces | Performance stress inputs and WEDGE comparison material; check completeness before reproducing the generator |
| [SWE-Pro](https://github.com/probench-swe/SWE-Pro) | Paper links an open evaluation pipeline | Candidate measurement baseline and practical optimization tasks; environment reproduction remains untested |
| [FormulaCode](https://formulacode.org/) | Project exposes evaluation tooling, repository, and dataset links | Multi-workload tasks and evaluation infrastructure |
| [TT-MDE](https://github.com/chenzongxiong/ASE-2026) | Repository README documents Python scripts, cached results, and a JMH fork | Direct stopping-method comparator; fetching individual files from an API-reported tree hash failed, so code-level inspection was not completed |
| [Microbenchmark prioritization replication package](https://doi.org/10.5281/zenodo.5206117) | Linked by published paper | Established prioritization techniques and historical measurement data |
| [July benchmark-study replication package](https://doi.org/10.5281/zenodo.21227455) | Linked by the paper; package contents not inspected | Stronger-test-generation comparison; artifact existence in the paper is not proof of successful reproduction |

## Nuances that affect method comparisons

Codeflash's timing documentation describes repeated execution and aggregation of minimum timings. Its general and detailed documentation give different improvement-threshold descriptions, so a reproduction must pin the actual version and configuration instead of treating a single threshold as universal. Peak-runtime comparisons should not be judged against a mean-latency requirement without first acknowledging the different objective. [Timing documentation](https://docs.codeflash.ai/codeflash-concepts/benchmarking)

µOpTime's historical configuration and dynamic benchmark stopping solve related but distinct problems. Using history to choose repetitions is different from choosing the next workload during a live optimization session. However, a new proposal must test a sensible combination of those techniques, not treat that distinction alone as proof of novelty.

The TT-MDE artifact is particularly relevant because it includes detection-power and false-positive evaluation, rather than only precision of runtime estimates. The complete paper must be obtained before making detailed claims about its statistical assumptions or limitations. This review does not infer omissions from a paper title or repository README.

SWE-Pro's inspected version uses confidence interval width as a convergence criterion. That establishes adaptive measurement prior art; it does not by itself establish a guarantee for arbitrary repeated candidate selection. Conversely, the absence of such a guarantee in the inspected appendix is not evidence that the tool produces unacceptable decisions. That is an empirical and theoretical question to investigate.

WEDGE's target is performance-stressing input discovery. A proposed regression validator may have a different decision objective, but it must demonstrate an advantage against WEDGE-style and differential-fuzzing approaches. A change of language, terminology, or prompt does not establish that advantage.

The July benchmark paper's non-significance results do not establish that implementations are equally fast, nor that all benchmark labels are wrong. Its findings concern detection under specified tests and measurement conditions. Treat its proposed testing framework as relevant prior art while independently checking its measurement assumptions.

## Claims to avoid in a proposal

- "No one has tested the correctness and performance of LLM-optimized code."
- "Existing methods only use one workload."
- "Adaptive measurement stopping is missing from this field."
- "Using an LLM to generate challenging tests is the novel contribution."
- "Passing our tests guarantees semantic equivalence."
- "A confidence interval handles every form of adaptivity automatically."
- "A small budget makes the proposed method new."
- "No search result exactly matches our title, therefore the gap is verified."

## Reading order before topic approval

1. SWE-Pro, especially measurement Appendix E, and the complete TT-MDE paper: nearest threats to the adaptive-validation proposal.
2. Codeflash's verification and benchmarking documentation: closest existing product behavior.
3. WEDGE and the July 2026 benchmark re-evaluation: strongest threats to generic test-generation and benchmark-quality contributions.
4. Microbenchmark prioritization, dynamic stopping, and µOpTime: essential non-LLM baselines.
5. Sequential regression detection and sequential LLM evaluation: tools and competing formulations for statistical decision-making.
6. FormulaCode and Mokav: practical workload and behavioral-validation resources.

The novelty review should record the exact problem definition, available evidence, cost definition, stopping rule, guarantees, datasets, and limitations of each nearest competitor. A gap is defensible only when that comparison and a practical pilot support it.
