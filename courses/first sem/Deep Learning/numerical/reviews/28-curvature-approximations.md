# Lesson 28 — Curvature approximations

## Plan discussion — approved

The lecture names BFGS, L-BFGS and Levenberg-Marquardt without supplying full update algorithms, so this is an explicitly scoped conceptual companion. Approve exact-versus-approximate-curvature pipeline, scalar secant illustration, memory-entry comparison, illustrative diagonal loading, and fresh practice with full answers.

TA conditions: distinguish an approximate Hessian from its inverse; the scalar secant ratio is not the full BFGS update. Define residual and Jacobian with a concrete residual slope. State LM's nonlinear least-squares setting and distinguish illustrative diagonal loading from a complete LM iteration. Memory figures count scalar entries only. Final rendered-page and numerical review pending.

## Final TA verdict — PASS

All 10 rendered pages visually reviewed; text, diagrams, equations and tables have clear spacing. Actual Lecture4 PDF page 53 was visually checked. The lesson accurately limits itself to the concepts supplied there and clearly labels the scalar secant, memory and diagonal-loading arithmetic as illustrations, not complete optimizer algorithms.

Independent exact-fraction secant calculations give 3 and 4; NumPy matrix multiplication and eigensolver checks give original eigenvalues (0,2), loaded eigenvalues (0.5,2.5), and the stated direction actions. Memory arithmetic independently confirms 10,000 versus 1,000,000 entries and 600 versus 10,000 entries.

Student review: parameter/gradient changes are linked concretely to curvature; approximate Hessian versus inverse, residual, Jacobian, and diagonal loading are defined. LM's least-squares context and omitted algorithm steps are explicit. Fresh practice has complete arithmetic and conceptual answers. No unresolved findings.
