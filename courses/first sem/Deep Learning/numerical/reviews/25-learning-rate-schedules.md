# 25 Learning-rate schedules: TA review

## Plan review — APPROVED

Source L4 PDF57/N4.4. eta0=.12,k0 first update: reciprocal eta0/(k+1), reciprocal-square eta0/(k+1)^2, exponential eta0 exp(-beta k), beta ln2. Fully substitute k0–3, table/plot, explain names and beta distinct from momentum. Apply reciprocal schedule to E=.5w^2,w0=1: .88,.8272,.794112. Plateau worked policy uses two consecutive non-improvements, factor.1, values .50,.45,.46,.47,.44,.445,.446; drops after epochs4 and7 to .012/.0012, retains parameters.

TA conditions: precise plateau trigger is chosen study policy, not claimed exact lecture algorithm; best-loss comparison strict (min_delta0), counters reset on improvement/drop; changed rate applies to subsequent epoch. Distinguish one-based epochs from zero-based update index. Fresh eta0=.2,beta ln4,k2 gives1/15,1/45,.0125; supplied independent w2=2 using reciprocal-square gives nextw88/45=1.9555556. Complete answers and indexing explanation required.

Final rendered review pending.

## Final TA verdict — PASS

Individually visually reviewed all 11 pages and source L4 PDF57. All formulas, comparison table, schedule plot and seven-epoch plateau table are readable without overlap or clipping. No changes required.

Independently recomputed schedules with exact fractions, parameter trace .88,.8272,.794112, fresh practice88/45, and simulated plateau policy: drops only after epochs4 and7, next rates.012/.0012. Correct source reciprocal denominators and exponential beta mapping; no mistaken fixed-subtraction linear schedule.

Student perspective: zero-based update indexing and one-based epoch timing explicitly distinguished; rate versus learned parameter separate; plateau counter, best-loss comparison, next-epoch effect and retained parameters clear. Fresh supplied state is labeled independent; complete worked answer includes all schedules and update. No outstanding findings.

Final author refinements on01 (typeset indexed update) and09 (counter/epoch spacing) also visually rechecked; PASS unchanged.
