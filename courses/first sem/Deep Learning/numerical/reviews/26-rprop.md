# 26 RProp: TA review

## Plan review — APPROVED

Source L4 PDF71 simplified RProp/N4.5. Define accepted parameter, retained prevD, positive step magnitude, signed Delta and trialw=w-Delta. Main E=.5(w-1)^2,start0,prevD-1,magnitude.6,grow1.2,shrink.5,bounds.01..1. Attempts: .6 accepted then magnitude.72;1.32 sign reversal rejected/rollback.6, retainprevD-.4, magnitude.36;.96 accepted then.432. Bound examples min(1.08,1)=1 and max(.0075,.01)=.01 before sign. Zero-gradient stop explicitly chosen. Fresh E=.5w^2,start1,magnitude.7 attempts .3 accept/.84;-.54 reject/.42;-.12 reject/.21;.09 accept/.252.

TA conditions: clamp positive magnitude before attaching sign, explicitly resolving slide signed-min/max ambiguity. No iRProp+ substitution. Distinguish attempted/rejected trials from accepted-update history. Initial magnitude used directly for first attempt. Explain main rejected1.32 loss.0512 is lower than accepted.6 loss.08 but sign reversal still drives rollback; loss is not the decision criterion. Full independent practice answer and source mapping required.

Final rendered review pending.

## Final TA verdict — PASS

Visually reviewed all 14 pages individually and actual source L4 PDF71. All equations, state table and accepted/trial plot readable without clipping. Source-specific rollback/shrink/retry and retained prevD followed; positive-magnitude clamping explicitly resolves signed-min/max ambiguity. Exact-zero stop convention stated.

TA independently simulated all seven attempts using exact fractions. Every trial, sign product, decision, accepted parameter, retained derivative and next magnitude matches. Main(.6,-.4,.72),(.6,-.4,.36),(.96,-.04,.432); fresh(.3,.3,.84),(.3,.3,.42),(.3,.3,.21),(.09,.09,.252). Checked loss.08 versus rejected.0512 and accepted.0008; bounds1/.01 correct.

Student perspective: three stored quantities defined first, initial magnitude applied before growth, negative signed subtraction shown, rejected attempts visibly separate from accepted history. The lower-loss rejected trial demonstrates decision criterion concretely. Four-attempt fresh practice includes every state transition and summary. No outstanding findings.
