# 19 Hidden-layer backpropagation: TA review

## Plan review — APPROVED

Source handout p3 sections5.3–6. Retain original shared parameters and Lesson17 cache. Explain hidden units have no direct target; sum weighted downstream deltas, then multiply by this neuron's local sigmoid slope. Show all four hidden deltas and all twelve hidden parameter gradients, with source indices and bias1. Branching diagram and fresh target-zero practice must include full scalar substitutions, not only summary tables. No parameter updates before Lesson20.

Independent scalar calculation: target1 d2=(-.03346203581432854,.04494231328733234), d1=(-.005956872466064737,.0038333189621207733). Layer2 weight-gradient rows=(-.022358923162987578,.030029904191546372),(-.01922201607082476,.025816775556113256); layer1 rows=d1 and2*d1. Target0 d2=(.040356174362146426,-.054201718070158854), d1=(.007184158944407059,-.004623092548207301); layer2 rows=(.026965502240272683,-.03621692524498648),(.02318230236948154,-.03113577134373803). Bias gradients equal layer deltas. Asked author to correct small main d1-neuron2 rounding/value discrepancy in proposal.

Final rendered review pending.

## Rendered review — minor fixes requested

All 22 pages visually reviewed. Independent scalar backpropagation and 30 central finite-difference calculations across both labels/all15 parameters agree (maximum error below2.4e-10). Page11 diagram negative weight label intersects its arrow; move or white-back the text. Define upstream backward gradient versus downstream forward-graph neurons on page02 to connect terminology used by subsequent worked pages.

## Final TA verdict — PASS

Re-inspected revised pages02 and11: upstream/downstream terminology now explicitly connected and negative weight label is unobscured. All22 pages visually reviewed; handout p3 recurrence/indexing verified. Independently recomputed all four deltas and twelve hidden gradients for each target, and central finite differences for all15 parameters/both targets (max error below2.4e-10). Full substitutions, original-weight rule, source/destination distinctions and fresh target-flip answers satisfy student understanding. No remaining blocking findings.
