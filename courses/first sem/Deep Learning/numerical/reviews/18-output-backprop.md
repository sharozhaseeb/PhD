# 18 Output-layer backpropagation: TA review

## Plan review — APPROVED

Source handout p2 sections4–5.1 and p3 section5.2. Define per-example delta as loss sensitivity to preactivation, derive BCE derivative and sigmoid derivative cancellation, then each output weight/bias gradient. Retain original network and forward cache. Explain cancellation requires sigmoid plus BCE, no extra sigmoid derivative afterward, and not batch averaging. Add a fixed-other-parameters bias perturbation demonstration and fresh target-zero practice with unchanged forward values.

Independent scalar calculation and central finite differences: main output gradients (-.2551026863264517,-.20568214756853145,-.4533032666916722). BCE/output derivative -1.8291676885437265 times sigmoid slope .24781941509833091 gives delta -.4533032666916722. Bias+.001 actual loss change -.0004531793608464 versus local estimate -.0004533032666917. Practice target0 loss .7911939145939004 and gradients (.30766115208190337,.24805856572845067,.5466967333083278).

Final rendered review pending.

## Final TA verdict — PASS

Visually reviewed all 12 pages and the original handout pp2–3. BCE algebra, sigmoid cancellation and all six main/practice output gradients agree with independent scalar calculations and central finite differences. Bias perturbation independently matches the stated actual and linear-estimate loss changes. Delta, parameter sensitivity, source activation and per-example scaling are explicitly distinguished. Original parameters remain fixed for hidden backpropagation; target-flip practice includes full answers. Layouts readable; no blocking findings.
