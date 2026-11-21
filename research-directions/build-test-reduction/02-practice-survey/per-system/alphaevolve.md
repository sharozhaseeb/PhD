# AlphaEvolve

Status: critic-checked 2026-11-21 (3 fixes) · Last checked: 2026-11-21
Artifact: none (closed) · Paper: "AlphaEvolve: A coding agent for scientific and algorithmic discovery", Google DeepMind 2025 (arXiv:2506.13131v1, 16 Jun 2025; critic re-read the full PDF text, 44 pp, incl. Discussion)
Evidence labels: **[src]** paper section, **[inf]** inferred, **[unk]** not found (searched the full text for noise/warm-up/repeat handling: none described).

## 1. What it is
An evolutionary loop in which Gemini models propose diffs (SEARCH/REPLACE blocks) to a program drawn from a program database; a user-written `evaluate` function scores each child; the database (MAP-elites with islands) feeds the next prompt [src Sec. 2.1-2.6].

## 2. Build / environment
Generic: the evaluator is arbitrary user code, "may take only seconds on a single device or spawn extensive computations" [src Sec. 2.1]. No build model; for kernels the evaluation runs on real TPUs [src Sec. 3.3.2]. No incremental or reduced build [unk].

## 3. Correctness tests per candidate
- Correctness is part of the evaluator, task specific: exact rounding checks for matrix-multiplication decompositions [src Sec. 3.1]; "must pass robust verification" for TPU circuit changes [src Sec. 3.3.3]; FlashAttention/XLA edits checked against the reference code on randomized inputs, then human experts confirmed [src Sec. 3.3.4]; Gemini tiling kernels are correct "by construction" since only tiling changes [src Sec. 3.3.2].
- **Evaluation cascade**: a sequence of increasingly expensive test stages; a candidate advances only if promising at every earlier stage, and a cheap small-scale check first filters faulty programs [src Sec. 2.4]. This is the clearest form of staged, reduced-then-full evaluation in the sources surveyed.
- Optional LLM-generated feedback grades qualities such as simplicity [src Sec. 2.4].

## 4. Performance measurement per candidate
- Objective is actual runtime on real hardware across a set of input shapes (training/evaluation split): average 23% kernel speedup, 1% cut in Gemini training time [src Sec. 3.3.2]. FlashAttention kernel +32%, pre/post-processing +15% [src Sec. 3.3.4].
- Repeats, warm-ups, statistical test, noise controls: not described anywhere in the paper text (full-text search for noise/warm-up/repeat found only unrelated code listings) [unk]. Kernel-shape set is split half training / half evaluation [src Sec. 3.3.2].
- Scheduling task: a simulator on historical workloads; held-out "unseen test dataset"; post-deployment measurements confirmed the simulator [src Sec. 3.3.1].

## 5. Cost per candidate
Evaluation "on the order of 100 compute-hours" per solution for expensive tasks, distributed asynchronously over an evaluation cluster; pipeline "optimized for throughput" under a fixed budget [src Sec. 2.4, 2.6]. No dollar figures [src].

## 6. Iteration / cumulative re-validation
Many generations of children are evaluated; the population is the memory. Final outputs for engineering results are re-verified by experts or against references outside the loop (Sec. 3.3.3-3.3.4) [src]; deployment confirmation for the scheduler [src Sec. 3.3.1].

## 7. Limitations the authors state
Main stated limitation: it handles only problems with an automated evaluator; LLM-provided evaluation of ideas is "not a setting we have optimized for" [src Sec. 6 Discussion; also Sec. 1].

## 8. Relevance to Study 1
- [src] Evaluation cascade (cheap check, then costlier evaluation) is the published precedent for a reduced-first test/benchmark per edit; the cascade is task-defined, not diff-derived.
- [src] Performance is measured on real hardware without a disclosed noise protocol; final validity is checked outside the loop. [inf] Supports the claim that per-edit acceptance in the loop and final (cumulative) verification are two separate stages.

## Sources
- https://ar5iv.labs.arxiv.org/html/2506.13131 (Sec. 2.1-2.6, 3.1-3.3.4); section numbers verified against the arXiv v1 PDF: 2.1, 2.4, 2.5, 2.6, 3.1, 3.3.1-3.3.4, 6 all match.
