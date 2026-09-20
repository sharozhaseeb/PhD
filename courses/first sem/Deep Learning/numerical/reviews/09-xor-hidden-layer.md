# 09 XOR and hidden layers: TA review

## Plan review — APPROVED

Ten pages following exact L2 pp56–58 constructions. Inclusive H: OR H(x+y-1), NAND H(-x-y+1), output AND H(hOR+hNAND-2); all four rows fully substituted. Compare skip architecture hidden AND H(x+y-2), output H(x+y-2h-1), all rows. Diagrams and counts excluding input nodes: 3 neurons/6 weights/3 biases versus2 neurons/5 weights/2 biases; longest-path depth2. Independent XNOR via final NOT H(-q), full answer and depth/count implications.

Independent truth checks: both XOR give0110 in00,01,10,11 order; XNOR1001. State p57 NAND T=-1,b=+1; distinguish skip edges; explain why diagonal positive points lack a single separating line. Zero biases still count as parameters under stated convention.

Final rendered review pending.

## Final TA verdict — PASS

All ten rendered pages and source L2 pp57–58 visually reviewed. Exact OR/NAND/AND and skip-AND architectures agree with source. Independently evaluated four binary pairs: both XOR variants yield0110, XNOR1001. Counts6+3 and5+2, excluding input nodes, and depths2 then3 are correct. Hidden outputs versus scores, direct edges, threshold-to-bias mapping, and alternate architectures are clearly explained. No blocking maths, student-understanding, fidelity or layout findings.
