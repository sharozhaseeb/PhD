# 27 Momentum and Nesterov: TA review

## Plan review — APPROVED

Source L4 PDF75–93, especially90. Signed displacement convention v_next=beta*v-eta*g, w_next=w+v_next; no1-beta coefficient. Nesterov temporary q=w+beta*v, evaluate gradient at q. Main E=.5w^2,w0=2,v0=0,beta.9,eta.1. Firststepv-.2,w1.8 for both; second momentumv-.36,w1.44; Nesterovq1.62,v-.342,w1.458. PlainGDsecond1.62. Fresh E=w^2,w0=1,beta.5,eta.1 gives firstw.8,v-.2;GDsecond.64,momentumv-.26,w.54,Nesterovq.7,v-.24,w.56.

TA conditions: map signed displacement to exact source convention; q is temporary gradient-evaluation point, not separately stored update; don't add beta*v twice. Retainedfraction refers previous displacement, not gradient averaging. Main second-step losses1.3122,1.0368,1.062882 respectively, without universal winner claim. Full separate worked practice, persistent velocity and no premature batch reset required.

Final rendered review pending.

## Final TA verdict — PASS

All 16 rendered pages visually reviewed; latest page 02 wording rechecked. Equations, the temporary-lookahead diagram, tables and practice answers are readable without clipping. Actual Lecture4 PDF page 90 was visually inspected: the signed-displacement and lookahead recurrences match the course after the stated index/name mapping.

Independent exact-fraction calculations verify both steps for GD, Momentum and Nesterov on both objectives. Main final parameters are 1.62, 1.44 and 1.458, with losses 1.3122, 1.0368 and 1.062882. Fresh practice final parameters are 0.64, 0.54 and 0.56, with losses 0.4096, 0.2916 and 0.3136.

Student-understanding check: displacement is defined before use, state persists within a method, q is explicitly temporary, the equivalent q-minus-gradient update avoids adding momentum twice, and the comparison does not claim a universal winner. Fresh practice changes objective curvature, initial value and momentum coefficient and includes every substitution. No unresolved findings.
