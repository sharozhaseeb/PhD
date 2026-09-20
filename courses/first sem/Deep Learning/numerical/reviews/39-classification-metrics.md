# Lesson 39 TA review

## Plan discussion — approved

Assignment positive class is digit zero encoded t=1; other digits t=0. Use explicit p>=.5 prediction and actual-row/predicted-column matrix. Every row, totals, metric denominator subsets and formula substitutions needed. Main TP2/FN1/FP2/TN3; fresh TP2/FN2/FP1/TN3; both accuracy5/8 and F1 4/7 but swapped precision/recall. Always-negative baseline matches accuracy but misses every positive. Distinguish undefined precision 0/0 from direct-count F1=0 when positives exist, and all-negative truth/prediction undefined F1. No undeclared software zero substitution. Include fresh threshold tie and separate full worked answers, plus supplied-count challenge.

Final rendered review pending.

## Final TA verdict — PASS

Reviewed all 20 rendered pages. Assignment 1 page 4 was visually inspected during the preceding source review and confirms digit zero is positive t=1, threshold .5 and requested accuracy/precision/recall/F1/confusion matrix. The exact tie convention is explicitly chosen. All pages are readable with clear matrix axes, row/column totals and no layout findings.

Independent Python threshold enumeration and exact Fraction metrics confirm main TP2/TN3/FP2/FN1 gives accuracy5/8, precision1/2, recall2/3, F1 4/7; fresh TP2/TN3/FP1/FN2 gives accuracy5/8, precision2/3, recall1/2, F1 4/7. Supplied-count challenge gives .7, .75, .6 and2/3. Every displayed threshold and outcome row matches these counts.

Student understanding: positive digit versus encoded label is prominent; metric denominators are tied to concrete subsets and IDs; harmonic F1 arithmetic and direct-count equivalence are fully worked. The equally accurate always-negative baseline detects no positives. Undefined precision and all-negative undefined F1 are distinguished from a genuine zero score, without an undeclared software convention. Both fresh exercises have separate worked answers and an exam workflow.
