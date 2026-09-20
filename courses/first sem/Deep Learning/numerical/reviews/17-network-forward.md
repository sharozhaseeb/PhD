# 17 Full network forward pass: TA review

## Plan review — APPROVED

Use exact handout pp1–2 five-neuron sigmoid forward equations and Lesson16 shared original parameters. Main x=(1,2), target1; named scalar equation, substituted contributions, sum and sigmoid for every neuron, then BCE. Cache values for backprop, retain full precision, never threshold before loss. Independent practice x=(-1,1), target0 with all five calculations and full answer.

Independent scalar Python calculation confirms main hidden1=(.6681877721681662,.574442516811659), hidden2=(.5627638384083551,.4537407132969821), z3=.18733286620371367, output=.5466967333083278, BCE=.6038610483901865. Practice hidden1=(.549833997312478,.6224593312018546), hidden2=(.5487054962164872,.46494303306040646), z3=.17863443564078357, output=.5445402309851674, BCE=.7864478888725223. Explicitly handle negative preactivation in sigmoid exponent.

Final rendered review pending.

## Rendered review — minor fixes requested

All 16 pages visually reviewed; forward and loss arithmetic match independent scalar calculations. Page01 architecture arrows vanish in subtitle, leaving separated numbers: replace with readable 2-to-2-to-2-to-1. Output-neuron pages07/15 incorrectly say cache for the next layer; change to loss/backpropagation because output is final layer. Other layouts readable.

## Final TA verdict — PASS

Re-inspected revised pages01,07,15: architecture text renders clearly and output-cache wording correctly points to the loss. All 16 pages visually reviewed; every main/practice scalar preactivation, sigmoid and BCE matches independent scalar calculations. Source handout architecture, indexing and activation conventions are retained. Full substitutions, negative exponent explanation, cache, natural logs and no-threshold-before-loss guidance provide a clear student sequence. No remaining blocking findings.
