# Group 3 status and verification

## Completed checks

The TA independently checked the 64-run roster, source TSV/hash, cleaning arithmetic, fixed 697/149/150 split, nested reduced-data subsets, and tokenizer measurements. All reconcile with the saved audit.

A second TA pass checked the Trainer/PEFT implementation and the results collector. Its main findings were addressed by logging exact classifier/adapter parameters and targets, recording a bundle hash, capturing raw validation predictions, testing a weight round trip during smoke runs, and excluding held-out metrics from the validation ranking. The runner evaluates the in-memory parameters after the fixed third epoch. No claim is made that it writes a durable model checkpoint.

For local wiring, tiny synthetic BERT and XLM-R models passed backward tests for both LoRA ranks, FFN LoRA, and both IA3 placements. The adapter and classifier each received gradients. These tests do not use pretrained weights and are not experiment results.

## Colab debugging

An initial T4 smoke run passed XLM-R Full FT and LoRA. QLoRA stopped because the Colab runtime uses CUDA 13.0 and bitsandbytes 0.47.0 did not ship the requested CUDA 13 binary. The revised notebook pins bitsandbytes 0.48.2, which includes CUDA 13 support. Treat these attempts as debugging, not rows in the training results CSV.

## Final gate

1. Run the revised notebook on T4. Eight smoke cases should pass; inspect the tensor round trip and exact targets.
2. Mount Drive in Colab before the pilot and full run so each job's evidence survives disconnects. Review the pilot before enabling all runs.
3. Verify all 64 jobs and regenerate the CSV/plots from the logged predictions. Build and render the report, check the six-page limit, and include the executed notebook.
4. Have the TA inspect the **actual** submission package, compare the report and figures to the result rows, and fix any findings. The TA has reviewed design and source so far; there is no final grading verdict yet.
