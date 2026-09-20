# 23 Saturation and loss choice: TA review

## Plan review — APPROVED

Source L4 PDF8–26 and handout2. Main p=.01,t1,z=ln(.01/.99),x2,b0,w=z/2. Half-squared loss .49005 versus BCE4.60517019; compare gradient responsiveness, not raw different-scale loss values. Sigmoid slope .0099; deltas -.009801 versus-.99; weight gradients-.019602 versus-1.98, bias gradients equal deltas. Full chain-rule cancellation and both simultaneous parameter updates with eta.1, then recompute output. Explain output cancellation does not remove hidden-layer vanishing gradients.

TA conditions: explicitly distinguish lecture unhalved square (factor2) from chosen half-square; show separate w/b updates before collecting x^2+1. Fresh p.9,t0,x2 deltas .081/.9, weight gradients .162/1.8. The proposed logit shifts-.0405/-.45 are both-parameter updates, not bias-only updates; label accordingly. Separate full answers and independent derivative checks required.

Final rendered review pending.

## Final TA verdict — PASS

Visually reviewed all 14 rendered pages individually and rechecked revised05. All math, tables and plot labels readable with no clipping. TA caught gradient/descent direction reversal in prose on05; corrected to subtracting the negative gradient increases z. Delta=dL/dz now explicitly defined at first use.

Independently computed both main and practice derivatives, all four simultaneous w/b updates, logits and probabilities using scalar Python; eight central finite-difference checks confirm both parameter gradients for both losses/targets within1e-8. New probabilities match .01004863/.01630058 and .89629549/.85160240. Verified chain-rule cancellation, x^2+1 derivation and factor2 conversion to the lecture unhalved square. Visually inspected L4 PDF12 source convention.

Student understanding: explicit source loss scaling, alternative steps from same original parameters, full logit recomputation, target-zero practice and separate answers. Distinguishes different raw loss scales and limits cancellation claim to output sigmoid, without claiming hidden-layer vanishing is removed. No outstanding findings.
