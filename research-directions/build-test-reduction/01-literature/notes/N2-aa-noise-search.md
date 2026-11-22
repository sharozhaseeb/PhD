# N2: A/A noise-floor and drift novelty search (N6, N7)
Date 2026-11-22. Categories: found / partial / not found. "Not found" means not found in these recorded searches only.
Labels: [read-in-source loc] = I read it; [abstract-only]; [unknown].

## 1. Exact asv rule (read in source, GitHub master, fetched 2026-11-22)
- `asv/commands/compare.py` L77-100 `_is_result_better(a, b, a_ss, b_ss, factor, use_stats=True)`: if use_stats and both have stats and neither has repeat==1, then `if not _stats.is_different(a_ss[1], b_ss[1], a_ss[0], b_ss[0]): return False`; then `return a < b / factor`. Verdict "worse/better" = statistical-difference gate AND strict ratio a < b/factor. Used at ~L375-395 (green '-' improved, red '+' worsened, else blank). L403-408 prefixes "~" on ratios that exceed factor but lack significance.
- `asv/_stats.py` L30-69 `is_different(samples_a, samples_b, stats_a, stats_b, p_threshold=0.002)`: NaNs dropped; `p_min = 1/binom(len(a)+len(b), min(len(a),len(b)))`; only if `p_min < p_threshold` it runs `mann_whitney_u(a,b)` and returns `p < p_threshold`; otherwise (too few samples) falls back to "99% CIs overlap => not different" (L63-69). `mann_whitney_u` L75-125: method auto = exact if max(m,n)<=20 else normal approximation (L113-117); ties broken conservatively (L79, L121-123). Two-sidedness [unknown: not verified in the function body].
- Default factor 1.1: `asv/commands/common_args.py` `add_compare` `--factor/-f` default=1.1; `--no-stats` = factor + median only. `asv/commands/continuous.py` L73 calls `common_args.add_compare`, so same default on current master. The Quansight 2021 post says continuous used 1.2 then: older asv differed. Check our installed asv version.
- Median: asv docs `docs/source/using.rst` L251 says timing results record median and IQR [read-in-source]; that compare uses the median as the result value is inferred, not verified in asv_runner.
- pyperf: `pyperf/_utils.py` `is_significant` = Student two-sample two-tailed t-test, "alpha=0.95" (critical value `tdist95conf_level`); `pyperf/_compare.py` L5-15 `is_significant_benchs`. No ratio condition in the significance flag [read-in-source].

## 2. Query log (all 2026-11-22)
| # | Tool | Query / action | Hits / outcome |
|---|---|---|---|
| 1 | Bash curl | raw.githubusercontent asv master asv/statistics.py, commands/compare.py, continuous.py, results.py | statistics.py 404; others ok |
| 2 | Bash curl | asv master asv/_stats.py, common_args.py, docs/source/using.rst; asv_runner benchmarks/time.py | ok (time.py no "median" hit) |
| 3 | Bash curl | pyperf main pyperf/_compare.py, _utils.py | ok |
| 4 | WebSearch | airspeed velocity asv false positive benchmark noise same commit regression detection pandas | 10; Quansight A/A blog, pandas benchmarks page, Augspurger post, asv tuning docs, numpy benchmarking docs |
| 5 | WebSearch | A/A test benchmark identical versions false positive rate performance regression detection microbenchmarks | 10; Japke 2511.03533, Grambow 2212.09515, Japke 2311.04108, Koch 2605.18397, ElastiBench, Laaber PeerJ |
| 6 | WebFetch | labs.quansight.org blog (429), then dev.to mirror of same post | read via fetch summarizer |
| 7 | WebFetch | arxiv abs 2511.03533, 2605.18397, 2212.09515 | abstracts |
| 8 | WebSearch | pyperf compare_to significant t-test "not significant" same benchmark twice false positive | 10; pyperf docs, Go benchstat issues 19634/23471; no pyperf A/A study |
| 9 | WebSearch | asv github issue "false positive" OR "noise" Mann-Whitney factor 1.1 benchmark regression bot numpy scipy astropy | 14; no asv A/A issue; Mozilla bugs, LLVM LNT, CodSpeed blog |
| 10 | WebSearch | Laaber Scheuner Leitner "Software microbenchmarking in the cloud. How bad is it really?" A/A tests false positives | 10 |
| 11 | WebSearch | arXiv 2510.18640 benchmark noise | did not surface it |
| 12 | WebFetch | arxiv abs 2510.18640 | Japke et al. IC2E 2025 vision paper, no A/A results [abstract-only] |
| 13 | WebSearch | performance variability over time same machine hours days measurement drift benchmarks thermal long-term microbenchmark | 10; Henning 2504.11826, Duplyakin 2003.04824, Barrett |
| 14 | WebFetch | arxiv abs 2504.11826v1, 2003.04824; stefan-marr.de/2026/08/pitfalls... | abstracts; Marr data illustrative, not used |
| 15 | WebSearch | Costa Bezemer Leitner Hassan "What's Wrong With My Benchmark Results?" TSE | 10; JMH bad practices, not A/A |
| 16 | WebSearch | Maricq Duplyakin ... "Taming Performance Variability" OSDI 2018 pdf | 10; USENIX PDF |
| 17 | WebSearch | 2025 continuous integration performance regression detection false positives noise identical commits empirical study benchmarks Python | 10; nothing Python/asv-specific |
| 18 | WebSearch | asv "Mann-Whitney" "0.002" benchmark comparison false positives issue airspeed-velocity github | 10; no asv issue |
| 19 | WebSearch | WSL2 Windows benchmark timing variability CPU frequency drift hours same machine microbenchmark reproducibility | 10; blogs, WSL issue #77 |
| 20 | WebSearch | Python interpreter startup import time variability benchmark process setup cost machine speed drift pyperf system tune | 10; no drift study |
| 21 | Bash pdftotext+grep | local PDFs (Laaber 2019, Bulej 2020, Traini 2023, Daly 2020, Kalibera 2013, Japke 2023) for "A/A", "false pos", "drift" | see table |
| 22 | Bash curl | arxiv 2003.04824, usenix osdi18-maricq.pdf, arxiv 2511.03533 | 3 valid PDFs (N2-downloads.json) |

Not done: direct GitHub issue-tracker searches for asv/pandas/numpy/scipy/astropy; Scholar/DBLP/Zenodo queries.

## 3. Closest works
| Work | Measured / platform | A/A? | Read | Closeness | Difference |
|---|---|---|---|---|---|
| Rodriguez-Guerra, Quansight blog 2021 (scikit-image asv, GitHub Actions) | `asv continuous` on two commits with identical code, every 6 h for ~16 days, 3 configs; FP 3.7% default, 9.99% no-interleave, 12.5% single pass; ratios 0.51-1.36 | yes | [partial, via fetch summarizer; FP cutoff unclear in post] | closest to N6 (asv verdict A/A) | CI cloud VMs, interleaved continuous runs, not per-repeat on a dev box; no p-gate vs ratio-gate decomposition; threshold then 1.2 |
| Laaber, Scheuner, Leitner, EMSE 2019 | microbenchmarks on AWS/GCP/Azure/bare metal; A/A of Wilcoxon+Cliff delta vs CI overlap, FP bar 5% | yes | [read-in-source §5.3, local text L1323-1345, L1716-1740] | A/A template and 5% bar for N6 | Java, cloud, different tests, not asv; few samples gave high FP |
| Bulej et al. ICPE 2020 (duet) | A/A duet vs isolated on private/public cloud, 99% CI of mean ratios | yes | [read-in-source L266, L444-481] | A/A accuracy method | duet scheduling, cloud |
| Japke et al. UCC 2025 (arXiv 2511.03533) | A/A duet on GCP with noise generator; bootstrap CI and Wilcoxon p<0.01; FPs in Table 1 | yes | [read-in-source L161-215, L336] downloaded | A/A FP with rank test | Go service latency, injected noise |
| Japke et al. 2023 (Early Microbenchmark) | A/A at severity 0 | yes | [read-in-source L166, L303] | FP in A/A | Go, injected regressions |
| Grambow et al. 2022 (arXiv 2212.09515) | micro vs application benchmarks, 70/110 commits | no | [abstract-only] | FP tolerance | not A/A |
| Daly et al. ICPE 2020 | MongoDB change-point detection; noise level varies over time | no | [read-in-source excerpts L18-110] | industrial noise/FP, N7-adjacent | e-divisive, production |
| Georges 2007; Kalibera & Jones 2013 | CI-based comparison; K&J note drift/auto-dependence (L496) | no | [read-in-source, grep] | method background | JVM |
| Traini et al. EMSE 2023 | steady state in Java microbenchmarks | no (grep empty) | [read-in-source grep] | warmup only | no machine drift |
| Costa et al. TSE 2021 | JMH bad practices | no | [abstract-only] | none | not A/A |
| Japke et al. arXiv 2510.18640 (IC2E 2025) | vision paper on CI benchmarking platform | no | [abstract-only] | none | conceptual, no data |
| Koch et al. arXiv 2605.18397 (2026) | duet instrumentation, keeps A/A latency distributions | partly | [abstract-only] | low | cloud services |
| Duplyakin et al. 2020 (arXiv 2003.04824) | 6.9M results, 1,600+ bare-metal machines, 2y9m, changepoints | n/a | [abstract-only + grep] downloaded | N7 context: drift is the norm | months-years, CloudLab, not WSL, no setup-vs-timed split |
| Maricq et al. OSDI 2018 | variability across runs and identical servers | n/a | [abstract-only] downloaded | N7 context | testbed |
| Henning et al. arXiv 2504.11826 (2025) | 591 h on AWS, CV<3.7%, daily/weekly patterns <=2.5% | n/a | [abstract-only] | closest to time-of-day effect | cloud stream processing |
| Barrett et al. OOPSLA 2017 | VM warmup, non-steady-state | n/a | [abstract-level] | within-run, not machine drift | VMs |
| pandas/numpy asv docs, asv tuning docs | noise guidance | no numbers | [unknown: snippets only] | N6 background | docs |

## 4. Verdicts
(1) asv rule or pyperf t-test evaluated with A/A: **partial.** One public asv-in-CI A/A experiment (Quansight 2021, 3.7-12.5% FP); none found that evaluates the p<0.002 gate versus factor 1.1 separately; nothing for pyperf compare_to; no asv/pandas/numpy/scipy/astropy issue found (trackers not directly searched).
(2) General A/A FP studies: **found** (Laaber 2019, Bulej 2020, Japke 2023/2025); none on asv's rule or Python/networkx.
(3) Single-machine hour/day drift: **partial.** Long-horizon (Duplyakin) and cloud daily patterns (Henning) found; per-process setup-cost drift vs stable timed samples, and WSL, not found.

**N6: partial, novelty modest.** Safe wording: "In same-commit comparisons on networkx we observed 0 false verdicts in 46 per-repeat comparisons (95% Wilson upper bound 7.7%) under asv's rule (ratio of medians > 1.1 and Mann-Whitney p < 0.002); in some cases p < 0.002 held and the verdict stayed 'same' only through the ratio condition. Comparable A/A checks exist for cloud benchmarks (Laaber 2019) and for asv in CI (Quansight 2021)." Caveat: 0/46 is weak evidence and per-repeat comparisons from one machine/session are not independent.

**N7: not found as a specific claim in recorded searches; context found.** Safe wording: "On our WSL developer machine, per-process setup cost of one benchmark module varied 1.7-3x within a day at low load while timed samples stayed stable; we did not find a prior report of this setup-versus-timing divergence, though longer-term machine drift is documented (Duplyakin 2020; Henning 2025)." Single machine; do not generalize.

## 5. Open gaps
Confirm installed asv version's factor default; verify two-sided test in `_stats.mann_whitney_u`; read the Quansight post in full; search asv/pandas GitHub issues directly.
