# 24 Newton updates: TA review

## Plan review — APPROVED

Source L4 PDF33–36,47–52. Scalar E=2(w-1)^2,start3,g8,H4 gives Newton1 versus GD2.2. Main E=1.5x^2+xy+1.5y^2,start(2,0),g(6,2),H[[3,1],[1,3]]. Define correction s by Hs=g then subtract s; explicit elimination gives(2,0), Newtonorigin E0. Optional inverse det8 agrees. GDeta.1 gives(1.4,-.2),E2.72. Indefinite saddle example(0,1) Newtonorigin raises loss-.5 to0. Singular x^4 at0 gives g=H=0, undefined0/0 despite minimum. Fresh Q=2x^2+xy+2y^2,start(1,-1),g(3,-3),s(1,-1),Newton0;GD(.7,-.7),loss3 to1.47.

TA conditions: contour arrows represent two alternative updates from same original point, not consecutive steps. Distinguish s from actual displacement -s. Qualify one-step minimum guarantee as exact positive-definite quadratic with full step; indefinite quadratics may reach stationary points without a minimum. Full separate practice answers required.

Final rendered review pending.

## Final TA verdict — PASS

Individually visually reviewed all 13 pages; rechecked revised07 after shared-start label moved clear of plot border. No remaining layout findings. Source L4 PDF50 visually checked: eta retained, full eta_N=1 versus damped eta_N=.5 explicit; column gradient mapping given.

Independently checked all scalar arithmetic, inverse determinant8, elimination steps, and NumPy linear solves for main, fresh practice and saddle. Main Newton(0,0), GD(1.4,-.2) loss2.72, damped(1,0) loss1.5; practice Newtonorigin and GD(.7,-.7) loss1.47. Saddle raises objective-.5 to0; singular quartic gives undefined0/0, not a computed zero correction.

Student perspective: starts scalar, defines correction versus displacement, solves two ordinary equations before optional inverse, explains alternative common-start arrows and contour meaning. Exact quadratic guarantee carefully scoped, counterexamples concrete, practice includes all working. No outstanding findings.
