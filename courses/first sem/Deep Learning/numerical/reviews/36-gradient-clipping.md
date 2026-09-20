# Lesson36 — Gradient clipping

## Plan discussion — approved

Begin with the literal Lecture5 PDF161 one-sided positive ceiling, then clearly label symmetric coordinate clipping and global Euclidean-norm clipping as supporting extensions. Use gradient(6,-8), threshold5, weights(1,1), eta.1 for every rule, full substitution and parameter update. Define vector length before deriving global factor. Plot gradient arrows, norm circle and coordinate square.

TA conditions: distinguish gradients from weights, coordinate bounds from total-length bounds, and nonzero direction preservation under global positive scaling. Handle zero gradient separately without division by zero; boundary and small-gradient cases remain unchanged. The plain-GD displacement bound eta*c does not silently extend to adaptive optimizer histories. Fresh(-12,5), threshold6 should test all three rules, including the literal source ceiling leaving it unchanged, with complete coordinate/norm update answers. Final rendered review pending.

## Final TA verdict — PASS

Reviewed all 13 rendered pages, plus Lecture 5 PDF page 161. Rechecked revised pages 01 and 07; page 11 was reviewed in its revised <= form. Requested plot-label relocation and subtitle spacing are fixed. No clipping or ambiguous diagram labels remain.

Independent NumPy calculations confirmed all three main and fresh-practice rules, parameter updates, norm lengths and common-direction ratios. Main global result (3,-4) has norm 5 and updates weights to (.7,1.4); fresh result (-72/13,30/13) has norm 6 and updates weights to (36/65,-3/13). Coordinate clipping exceeds the respective norm caps, as stated.

Student/source review: literal one-sided source ceiling is distinguished from labeled symmetric and global-norm extensions. Gradient versus weight, component versus length, subtraction signs, zero and exact-boundary cases, and plain-GD displacement scope are explained. Full fresh practice has separate worked answers.
