# 21 Gradients, Hessians and stationary points: TA review

## Plan review — APPROVED

Source L3 stationary/second-derivative discussion and L4 pp37–49. Define partial derivative, gradient, curvature, Hessian and eigenvector/eigenvalue concretely. E=1.5x^2+xy+1.5y^2 has gradient(3x+y,x+3y), Hessian[[3,1],[1,3]], g(2,0)=(6,2), stationary origin and eigenvalues2,4. Verify directions(1,-1),(1,1). Contrast -E maximum, (x^2-y^2)/2 saddle and x^4+y^4 minimum whose zero Hessian test is inconclusive. Fresh Q=2x^2+xy+2y^2 gives g(1,-1)=(3,-3), eigenvalues3,5 and origin minimum; R=-x^2-2y^2 gives negative diagonal Hessian and maximum.

TA condition: directional curvature plots must use unit vectors (1,+/-1)/sqrt2 if equating second derivative with eigenvalues. Along unnormalized(1,1), E(t,t)=4t^2 has second derivative8, not4. Define 2x2 determinant and identity before characteristic polynomial. Positive definite Hessian at stationary point suffices for strict local minimum; semidefinite test is inconclusive without further analysis.

Final rendered review pending.

## Final TA verdict — PASS

Individually visually reviewed all 15 final rendered pages: 01–04 definitions/partial slopes/Hessian; 05–08 stationarity/eigenvalues/eigenvectors/full normalized-coordinate substitution; 09 directional plot; 10–11 maximum/saddle/inconclusive Hessian; 12–15 independent Q/R practice and answers. All equations and labels readable, no clipping or overlap.

Independent TA central differences recover E gradient (6,2), H [[3,1],[1,3]] and Q gradient (3,-3), H [[4,1],[1,4]], with Hessian error below 5e-8. Independent eigensolver gives (2,4) and (3,5). Checked exact algebra, normalized curves t^2 and 2t^2, increments 6.06015 and 6.02015, saddle values +/-0.005 and fourth-power minimum argument. Visually checked L4 PDF37 source quadratic form; notation mapping and source scope are explicit.

Student perspective: concrete small changes precede curvature; determinant and identity are defined; unit-vector scaling is fully worked; local/global/strict meanings are stated; zero gradient and zero Hessian are not misclassified. Practice is separate and has complete derivative/classification answers. Plan normalization concern resolved; no outstanding findings.
