# Lesson 29 — Batch, stochastic and mini-batch updates

## Plan discussion — approved

Use a constant-output half-squared-loss model to isolate batch timing. Main targets (0,2,4,6), initial w=0, eta=0.1; full batch, forward/reverse SGD and two fixed mini-batches. Fresh targets (1,3), eta=0.2; all updates and answers. Include retained partial-batch update counts and divisor.

TA conditions: derive per-example gradient w-target; all examples inside a batch use the same old parameter. Compare equal epoch/example-gradient work, not equal update count or runtime. All reported final losses must use the complete original dataset; distinguish this reporting mean from the final partial-batch mean. Explicit order, shuffling and retained-partial-batch policy. Rendered review pending.

## Rendered review findings

All 24 pages reviewed. Arithmetic independently checked with exact fractions for all main and fresh-practice batch sequences; final main J values 6.145, 4.263442, 4.61891698 and 5.40405 match. Actual Lecture5 PDF page 82 inspected; batch accumulation/mean/update and explicit fixed-rate study choice are consistent.

Fix before final pass: page 15's straight interpolation incorrectly suggests parameter movement before a batch finishes. Use held-value step paths with update markers. Also define B and |B| next to page 02's formula, and explain the ceiling brackets on page 17 as rounding up. Other rendered pages are clear; no arithmetic findings.

## Final TA verdict — PASS

All 24 pages reviewed, with latest pages 02, 15 and 17 rechecked. Page 15 now correctly holds parameters constant between completed updates; all batch-size and ceiling notation is explained. All earlier findings resolved. Exact-fraction arithmetic verifies every main and fresh-practice update, full-dataset reporting losses, and retained-partial-batch counts.

Student understanding: the simplified model exposes the timing distinction, the loss-to-gradient derivative is shown, each batch uses one old parameter, example order is explicit, and epoch/work/update counts are distinguished. Fresh practice changes targets and rate and supplies complete answers. No unresolved findings.
