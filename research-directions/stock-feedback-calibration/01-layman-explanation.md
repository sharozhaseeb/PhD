# The idea in everyday language

Suppose each evening we publish a range for an equity fund's return over the next five trading days. A 90% target means we want approximately nine out of ten realized returns to fall inside their previously published ranges over the specified evaluation population. It does not promise 90% reliability for every day, every market regime, or every selected trade.

We want both reliable and informative ranges. An enormous range can contain nearly everything and still be useless. Our main score therefore penalizes both excessive width and outcomes outside the range.

## What is delayed?

Monday's five-day outcome takes five trading sessions to become fully known. Meanwhile Tuesday's daily return is observable. We can score a separate one-day forecast, but cannot pretend that its error is Monday's five-day error.

The research asks whether that daily surprise helps us set the range for a **new** five-day forecast issued on Tuesday evening. Monday's original forecast stays in the record unchanged. Revising Monday's range would instead create a remaining-horizon problem, and must not be silently substituted.

Daily updates are not automatically novel. Existing models can use recent daily prices and volatility. Our proposal must improve on those methods when they receive the same inputs.

## A plausible failure and an equally plausible rival

Perhaps daily surprises warn that a five-day uncertainty estimate is stale. A fast scale adjustment could respond before enough new five-day errors mature.

Alternatively, ordinary recent-volatility scaling already captures that warning. Or responding quickly could widen intervals after an isolated shock just as markets become calm. Those rival explanations are central experiments.

## What success would look like

The method should improve an interval score on unseen data, maintain acceptable overall coverage, and show consistent transition-period benefits. A wider range with higher coverage alone is not enough.

We first test with simple models and a few equity ETFs. This examines uncertainty in equity-market returns, not which individual stock to buy. No agent, news analysis, or trading strategy is necessary for the pilot.

## Why this might support a PhD

A defensible sequence is to characterize a reproducible failure, develop a correction that survives strong comparisons, and demonstrate its limits on independent data. Each step is conditional on evidence. If existing methods already solve the problem, this particular method claim ends; a negative finding is not automatically a publication.
