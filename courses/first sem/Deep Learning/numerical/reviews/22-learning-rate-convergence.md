# 22 Learning rate and convergence: TA review

## Plan review — APPROVED

Source L4 PDF31–49. Main E=2(w-1)^2, curvature4, start3; derive signed error factor r=1-4eta, magnitude factor |r| and loss factor r^2. Rates .1,.25,.4,.5,.6 each require two full gradient/subtraction/loss steps. Expected losses from8: (2.88,1.0368), (0,0), (2.88,1.0368), (8,8), (15.68,30.7328). Stable fixed-rate interval0<eta<.5. Explain constant-factor convergence and alternating signed error.

TA conditions: multi-dimensional example explicitly defines E=.5(x^2+100y^2), Hdiag(1,100), eta.01, starting(1,1); losses50.5,.49005,.480298005. Endpoint rate fails from nonoptimal initial point, not from an initial optimum. State quadratic assumptions and no universal neural-network guarantee. Fresh E=(w+2)^2, start0, rates.25/.75 gives paths0,-1,-1.5 and0,-3,-1.5, equal losses4,1,.25, complete separate answers.

Final rendered review pending.

## Final TA verdict — PASS

Visually reviewed all 17 pages individually, including final changed02–07,09,16–17. No clipping or equation/table/plot overlap. Corrected three student ambiguities: signed error is a signed difference, plot shows parameter paths, and same-side practice does not claim to cross the minimum. Initial loss is now typeset on each rate page.

TA independently recomputed all five main two-step traces, both practice traces and two-dimensional updates with exact rational arithmetic. All displayed weights/losses match, including divergence30.7328 and two-dimensional final loss .480298005. Error factor versus squared loss factor, stable intervals, endpoint oscillation and fixed-positive-quadratic assumptions are correct. Source L4 PDF31 visually checked; formula mapping follows scalar and multivariate quadratic source context.

Student readiness: initialization and update indices defined, fresh gradients used each step, sign reversals shown explicitly, linear convergence explained as constant error fraction, full fresh practice answers provided. No outstanding findings.
