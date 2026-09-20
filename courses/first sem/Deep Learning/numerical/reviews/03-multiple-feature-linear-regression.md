# 03 Multiple-feature linear regression: TA review

## Plan review — APPROVED

Course L1 pages43–44; explicit theta/b/w mapping, feature versus example indexing, x0=1 as bias bookkeeping. Toy triples(1,0,2),(0,1,1),(1,1,3), all-zero parameters, alpha .3. Show expanded predictions, half-MSE, each residual times each feature, bias mean, two simultaneous updates, all recalculated second-step contributions, assignment connection clearly separated, and independent one-example practice with negative feature.

Independent arithmetic: gradient order(b,w1,w2). Initial(-2,-5/3,-4/3) ->(.6,.5,.4); residual(-.9,0,-1.5), cost .51. Nextgradient(-.8,-.8,-.5)->(.84,.74,.55), residual(-.42,.39,-.87), cost .1809. Practice x=(2,-1),y4,params(1,2,3),alpha .1: prediction2,residual-2,gradient(-2,-4,2),newparams(1.2,2.4,2.8),newprediction3.2,cost.32. Assignment first-row contribution(-11,-11,-22) is before averaging six rows.

Final rendered review pending.

## Final TA verdict — PASS

Visually inspected all twelve lesson pages and L1 p43; p44 reviewed earlier. Independently recomputed all three states with matrix arithmetic: costs2.333333,.51,.1809, gradients and parameter values agree. Practice and assignment first-row arithmetic correct. Parameter order, bias constant, feature/example indices, two full recomputations, and averaging are explicit. Assignment data are clearly separate. Readable layouts, no clipping or overlap. No blocking findings.
