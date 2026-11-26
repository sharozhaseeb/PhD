# Comparison report — maximum six pages

1. Setup and tokenizer tables: track, group number, seeds, data cleaning, split class counts, max_length rule, settings and tokenization statistics.
2. Main results: paired seed means ± sample SD for test macro-F1, accuracy, runtime, GPU peak allocated memory and trainable params. Include both models, all conditions and both tasks for Track 2. Place the complete seed-level data in the results CSV.
3. LoRA rank plot and memory Pareto plot; mark which configurations are nondominated (no other configuration is at least as accurate and no more costly, with at least one strict improvement).
4. Time Pareto plot, scarcity plot and fertility plot; use panels if needed. Caption each and name the metric, units and population.
5. Discussion using exact results: RQ1 accuracy/cost, rank, FFN placement, memory and paging; RQ2 fertility and truncation with the two-point limitation; RQ3 absolute macro-F1 drops against each method’s own 100% point. Separate observed outcomes from hypotheses.
6. Reserve space for layout or Track 2. Include one or two lines of actual contribution per member. Keep the discussion about a page.

Submission checklist: executed Colab notebooks, complete results CSV, and report PDF. Check that numbers, configurations and captions reproduce from the saved run rows. For the individual viva, everyone should be able to locate one run, show its trainable-parameter audit and explain its split, macro-F1, memory measurement and matched comparator.
