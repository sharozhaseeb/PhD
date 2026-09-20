# 04-05 Logistic regression: TA review

## Plan review — approved

Reviewed roadmap and Lecture 2 PDF pages 9 and 22–25 visually. Preserve the existing detailed lesson. Add notation mapping before calculations: h_theta(x)=p, g=sigmoid, theta0=b, theta1=w, x0=1; explicitly expand theta^T x. Retain mean BCE and simultaneous full-batch updates.

Independent practice: x=(0,1,2), y=(0,0,1), w=b=0, alpha=0.1. Show p, each p-y, gradient contributions, mean gradients, simultaneous update and new loss. Independently calculated dw=-1/6, db=+1/6, w_new=1/60, b_new=-1/60. Distinguish practice answer pages from question. Update total page count.

Final rendered review pending.

## Rendered review — changes requested

Visually inspected all 13 PNG pages. Source fidelity, mathematical chain rule, mean gradients, update convention, interpretation, and independent exercise are sound. Independent Python arithmetic gives practice probabilities (0.4958334298, 0.5, 0.5041665702), losses (0.6848485690, 0.6931471806, 0.6848485690), mean 0.6876147729.

Required: page 12 long contribution equations extend beyond the intended right margin to the page edge. Split or resize consistently; split parameter updates if needed. Recommended: disambiguate feature x1 on notation page from example x_i later, preferably by using augmented vector (1,x).

Awaiting changed page recheck.

## Final TA verdict — PASS

Re-inspected revised pages 1 and 12 visually. Mapping avoids the feature/example index ambiguity, contribution rows now have comfortable right margins, and separate updates are easier to follow. All 13 pages reviewed; arithmetic independently confirmed. No blocking student-understanding, mathematical, course-fidelity, or rendering issues remain. Lesson 1 may begin.

Additional polish recheck: root moved the final two updates upward to increase space above the callout. Latest page 12 inspected; comfortable separation, PASS retained.
