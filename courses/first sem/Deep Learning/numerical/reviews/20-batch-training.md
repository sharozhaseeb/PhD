# 20 Batch gradients and a complete training update: TA review

## Main-example plan review — APPROVED

Original shared network; A=((1,2),1), B=((-1,1),0), mean BCE J, eta=.1. Show full B backward, all15 mean gradients and simultaneous updates, refreshed forwards/losses. Define per-example ell and delta explicitly to reconcile Assignment notation; average parameter gradients exactly once. Same common original state for every derivative; do not multiply averaged activations and deltas.

Independent scalar computation: old J=.6951544686313544. eta.1 updated probabilities A=.5449724154032549,B=.5428071933369149; losses .6070200995388034,.7826500806430726; J=.694835090090938. Individual A loss rises although batch mean falls, which must be explained. Independent central finite differences for all15 mean gradients have max absolute error1.35e-10.

## Practice revision requested

Root correctly notes roadmap requires fresh full-network practice: changing only eta reuses every gradient. Asked author to replace this with new input/target examples, suggested C=((0,1),1),D=((1,-1),0), original weights and eta=.1; complete forward/backward/average/update/refreshed-loss answers. A separate practice PDF inside20 is acceptable if every page is reviewed before proceeding. Revised practice plan pending author confirmation.

Final rendered review pending.

## Revised independent practice — APPROVED

Author confirms fresh C=((0,1),1), D=((1,-1),0) batch, original parameters, eta=.1, full forward/backward/mean/update/refreshed-loss answers in the same PDF. C's zero input tests zero connection gradients despite nonzero delta; D's negative second feature tests sign reversal.

Independent scalar result: old pC=.5453170204278609,pD=.54476513530348,J=.6966648858195239. New pC=.543623952260864,pD=.5430633667117561; losses .6094975353858257,.7832105557144388; J=.6963540455501323. All15 fresh-batch mean gradients independently checked by central finite differences, max error1.33e-10.

## Rendered review checklist (in progress)

- Pages01–44: visually reviewed, math cross-checked against independent scalar results. Pages35–36 correctly show zero first-input gradients for C; its nonzero hidden deltas remain explicit.
- Pages45–66: pending.
- Requested fixes: pages11–13 copied layer1 source description into layer2/output gradient pages; author fixed09–13 with conditional descriptions. First u definition requested; author fixed05–08. Author also updated03 rounding and66 conclusion.
- Latest changed-page rechecks pending:03,05–13,66. All other01–44 reviewed versions valid.
- Independent calculations already cover every parameter mean/update and both refreshed forwards for mainA/B and practiceC/D; all30 batch finite differences passed.

## Rendered review checklist — all pages read

- Pages01–66: every rendered page visually reviewed.
- Latest changed03,05–13,35,66: re-inspected and approved; u, source-activation descriptions, rounded decimals and exact zero are clear.
- Remaining finding: updated practice-forward pages59–64 retain subtitle 'original parameters', contradicting their correct updated calculations. Requested subtitle change to updated parameters after C/D step; final recheck of those6 pending.
- All numerical calculations and update arithmetic match independent main and fresh-practice results. No clipping or overlapping equations found.

## Final TA verdict — PASS

All66 rendered pages visually reviewed. Final changed-page rechecks03,05–13,35,59–66 complete: source descriptions and u definition corrected, zero display clear, updated-practice subtitles consistent, no remaining layout issues. Main A/B and fresh C/D practice each include all15 gradients/means/updates and refreshed forwards/losses. Independent scalar arithmetic and all30 batch finite differences confirm results (max error below1.35e-10). Main mean .6951544686313544 to .694835090090938; practice .6966648858195239 to .6963540455501323. Handout formula/indexing and Assignment mean-loss convention reconciled by explicit per-example deltas and exactly one averaging factor. Fresh practice genuinely changes inputs, tests zero/negative feature gradients and provides full answers. Individual loss can rise while mean falls is explicit. No blocking mathematical, source-fidelity, student-understanding or rendering findings remain.
