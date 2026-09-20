# 16 Network notation, shapes and parameter counts: TA review

## Plan review — APPROVED

Use source handout architecture 2 to 2 to 2 to 1 with sigmoid units and original explicitly chosen numerical weights. Source index i to destination j maps to row-example matrices of shape (previous width, current width). Explain layer indices, weight entries, bias as a constant-input connection, matrix multiplication compatibility and entrywise activation. Count 10 weights plus 5 biases, not duplicated biases per batch example. Preserve chosen parameters for sequential forward/backprop lessons17–20.

Independent arithmetic: x=(1,2), W1=[[.1,-.2],[.3,.2]], b1=(0,.1) gives z=(.7,.3). Second row(-1,1) gives(.2,.5). Layer counts6,6,3 total15. Practice3-to-2-to-1 has11 parameters; batch4 matrices4x3 ->4x2 ->4x1. Given practice weights and x=(1,0,-1), z=(-3.5,-4.5).

Final rendered review pending.

## Rendered review — minor clarification requested

All 12 pages visually reviewed. Source handout p1 indexing and architecture checked; arithmetic, sigmoid values, counts and practice agree. Page09 introduces d_l and d_(l-1) without defining layer width. Add a short definition of d_l and d_0, then recheck that page.

## Final TA verdict — PASS

Re-inspected revised page09: layer-width definition is clear and layout remains readable. All 12 pages reviewed, with handout p1 source-to-destination notation and two-hidden-layer architecture verified. Independently confirmed scalar products, sigmoid values, parameter counts, batch shapes and practice. Bias reuse and activation-versus-target distinctions are explicit; no remaining blocking findings.
