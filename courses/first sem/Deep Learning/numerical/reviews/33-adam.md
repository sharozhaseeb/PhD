# Lesson33 — Adam

## Plan discussion — approved

Follow Lecture5 PDF121–122 with slide delta mapped to beta1 and gamma to beta2, source epsilon inside the radical. Work supplied gradients2,-1 through raw moments, both bias-correction denominators, corrected moments, normalized steps and parameters. Explain a negative current gradient can coexist with a positive history-weighted first moment. Supplied gradients isolate optimizer arithmetic and do not imply a loss guarantee.

TA conditions: distinguish Adam v (uncentered second-moment state) from earlier signed momentum displacement, variance and Hessians. Average the batch gradient before squaring. Start global update t at1 and retain moments/t across batches and epochs. Constant-gradient bias-correction derivation is an illustration; unbiased-expectation claims require stationarity assumptions. Show positive epsilon inside/outside comparison, restrict epsilon-zero example to positive denominators, and give full fresh negative-gradient practice answers. Final rendered review pending.

## Final TA verdict — PASS

Reviewed all21 rendered pages and actual Lecture5 PDF121–122. Rechecked revised pages01,02,03,05,08,10,11,13,14,16,19,21 after prose-spacing cleanup and the explanation that moment-estimate bias correction is unrelated to a network bias parameter b. No unresolved layout or mathematical findings.

Independent exact-fraction recurrences and square-root calculations confirmed main raw states(.2,.004),(.08,.004996), second corrected moments(.4210526316,2.4992496248), step.026633703966 and final w.873366296034. Fresh negative-gradient sequence gives raw second state(-.38,.007996), corrected moments(-2,4), parameters1.1 then1.2. Positive-epsilon comparison and uncorrected first step.316227766 versus corrected.1 are correct.

Student checks: raw states are retained while corrected values drive updates; global t starts1 and survives epoch boundaries; current gradient sign need not match historical first moment. Batch mean is squared after averaging. The constant-gradient derivation explains startup attenuation, with stationary-expectation qualification for random gradients. Uncentered second moment is distinguished from variance through an explicit zero-variance constant sequence. Epsilon placement matches course notation and has a positive-epsilon example. Ready for Lesson34 plan.
