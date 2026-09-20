# Lesson 31 — Momentum across mini-batches

## Plan discussion — approved

Use two two-example batches with opposing target means, a signed-displacement state, explicit Momentum versus Nesterov evaluation points, then continue the first batch of the next epoch. Fresh practice changes both batches. Full per-example gradients and batch means at every update.

TA conditions: parameters and velocity persist between batches and epochs; only gradient accumulators reset per batch. All examples in a Nesterov batch share one temporary q. Map the lecture's in-place lookahead/correction to q-eta*g(q)=w+v_new without double momentum. Label the erroneous reset example clearly as fresh practice. Final visual and independent state review pending.

## Final TA verdict — PASS

All 24 pages visually reviewed, including revised first-batch explanations on pages 04 and 18. Actual Lecture5 PDF pages 103, 106 and 109 inspected: signed displacement, persistent state, batch averaging and in-place Nesterov lookahead map correctly to the lesson formulas.

Independent exact-fraction simulation verifies every main and practice evaluation point, batch gradient, displacement and parameter. Main Momentum states end (0.212,0.132); Nesterov ends (0.2045,0.1345). Fresh final parameters are 0.44 and 0.435, versus 0.39 if memory is mistakenly reset.

Student review: both per-example gradients use a common batch point; averaging occurs once; next-epoch continuation preserves each method's own state. Initial zero displacement now explicitly explains why the shared first step applies to both methods. The flow diagram distinguishes retained state from temporary sums and lookahead. Layout is clear and no unresolved findings remain.
