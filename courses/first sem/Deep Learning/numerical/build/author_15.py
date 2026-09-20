from pathlib import Path
import json,math
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'15-loss-empirical-expected-risk';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('Start with one prediction and one target','Lecture 3 uses div to mean discrepancy or loss. It does not mean division.',[
E(r'\ell_i=\mathrm{div}(f(x_i;W),t_i)'),
'f(x;W) is the model prediction; W contains its parameters; t is the known target. A per-example loss measures their mismatch.',
E(r'\mathrm{Our\ chosen\ loss}:\quad\ell=\frac{1}{2}(\hat y-t)^2'),
'The lecture gives a general discrepancy function. Here we choose half-squared error, consistent with our earlier regression examples. The one-half is a stated scaling choice.',
'Reuse the three points (1,2), (2,3), (3,5). Model A predicts y-hat = x, with weight w = 1 and bias 0.']),
P('Compute all three losses before averaging','Each row has its own prediction, residual and nonnegative loss.',[
E(r'x_1=1,t_1=2:\quad\hat y_1=1,\quad\ell_1=\frac12(1-2)^2=\frac12(-1)^2=0.5'),
E(r'x_2=2,t_2=3:\quad\hat y_2=2,\quad\ell_2=\frac12(2-3)^2=0.5'),
E(r'x_3=3,t_3=5:\quad\hat y_3=3,\quad\ell_3=\frac12(3-5)^2=\frac12(4)=2'),
'A negative residual becomes positive after squaring. The value 2 is the third example loss, not the mean loss of the dataset.']),
P('Empirical risk: average the observed sample','Lecture 3, pages 105-107: give each observed example equal weight 1/N.',[
E(r'\widehat R(W)=\frac1N\sum_{i=1}^N\ell_i'),
E(r'N=3:\quad\widehat R(A)=\frac13(0.5+0.5+2)=\frac33=1'),
'The hat means this is an estimate based on observed examples. N counts examples, not features, classes or parameters.',
'One-half is already inside each chosen loss. Do not apply another factor of one-half after averaging.',
'With representative sampling, the sample mean estimates the population expected loss. One observed sample need not have exactly the population proportions.']),
P('Expected risk: specify a tiny population','This teaching population has exactly three possible outcome types.',[
{'table':[['type','(x,target)','probability q','loss of A'],['1','(1,2)','0.50','0.5'],['2','(2,3)','0.25','0.5'],['3','(3,5)','0.25','2']],'widths':[80,160,190,180]},
E(r'q_1+q_2+q_3=0.5+0.25+0.25=1'),
'The model remains fixed. q is the chance that a fresh example has that outcome type. The three rows are the complete illustrative population, not three independent population datasets.',
'In real learning problems the true distribution is usually unknown; we use samples to estimate its expected loss.']),
P('Weight each population loss by its probability','This finite sum is the discrete version of the expectation/integral on page 103.',[
E(r'R(W)=\mathbb{E}[\ell]=\sum_k q_k\ell_k'),
E(r'q_1\ell_1=0.5(0.5)=0.25'),
E(r'q_2\ell_2=0.25(0.5)=0.125'),
E(r'q_3\ell_3=0.25(2)=0.5'),
E(r'R(A)=0.25+0.125+0.5=0.875=7/8'),
'Do not divide this result by 3 again. Probability weights already sum to 1. Empirical risk is 1 here; expected risk is 0.875 because their weighting differs.']),
P('Compare a second fixed model','Model B predicts y-hat = 1.5x, with bias still zero.',[
E(r'x_1=1:\quad\hat y_1=1.5,\quad\ell_1=\frac12(1.5-2)^2=0.125'),
E(r'x_2=2:\quad\hat y_2=3,\quad\ell_2=\frac12(3-3)^2=0'),
E(r'x_3=3:\quad\hat y_3=4.5,\quad\ell_3=\frac12(4.5-5)^2=0.125'),
E(r'\widehat R(B)=\frac{0.125+0+0.125}{3}=\frac{0.25}{3}=1/12\approx0.083333'),
E(r'R(B)=0.5(0.125)+0.25(0)+0.25(0.125)=0.09375'),
'Use the same loss definition and the same population probabilities for a fair comparison.']),
P('What does argmin return?','Lecture 3, page 107 selects parameters that minimize empirical loss.',[
E(r'\widehat W=\operatorname{argmin}_W\widehat R(W)'),
'Argmin means the argument (here the parameter values) that gives the smallest objective value. Min means the smallest objective value itself.',
E(r'W\in\{1,1.5\}:\quad\operatorname{argmin}\widehat R(W)=1.5'),
E(r'\min\widehat R(W)=1/12\quad\mathrm{over\ those\ two\ choices}'),
'B is better than A on both criteria here. Checking these two candidates does not prove B is the best possible weight over all real values.',
'Do not treat low training loss as proof of equally low test loss: the sample is only an approximation to the true distribution.']),
P('A loss can distinguish two correct predictions','Binary cross-entropy is a smooth classification loss used in the logistic lesson.',[
E(r't=1:\quad\ell=-\ln p'),
E(r'p=0.6:\quad\ell=-\ln(0.6)\approx0.510826'),
E(r'p=0.9:\quad\ell=-\ln(0.9)\approx0.105361'),
'Both predictions become class 1 at threshold 0.5, so both have zero classification error for this example. Cross-entropy rewards the more confident correct probability.',
'Here p is the model probability of class 1. It is different from q, the population probability of an example type on earlier pages. All logarithms are natural.',
'A loss is not always a count of mistakes. Always identify the stated discrepancy before calculating its mean.']),
P('Your turn: sample mean versus population mean','Treat these three rows as the complete teaching population and also observe each once.',[
{'table':[['row','target t','prediction','probability q'],['1',2,1,'0.2'],['2',2,2,'0.5'],['3',3,4,'0.3']],'widths':[90,160,190,200]},
'Use half-squared error. Compute each individual loss, then the empirical risk of the three-row sample, then the population expected risk.',
'Verify that the probabilities sum to 1. Explain why the two averages differ and why you must not divide the probability-weighted sum by 3.'],'INDEPENDENT PRACTICE'),
P('Practice answer: losses and the sample mean','Square each residual, multiply by one-half, then average once.',[
E(r'\ell_1=\frac12(1-2)^2=\frac12(-1)^2=0.5'),
E(r'\ell_2=\frac12(2-2)^2=0'),
E(r'\ell_3=\frac12(4-3)^2=\frac12(1)^2=0.5'),
E(r'\widehat R=\frac{0.5+0+0.5}{3}=\frac13\approx0.333333'),
'This observed sample gives each row one-third of the total weight. The middle row is not given probability 0.5 in this particular sample average.'],'WORKED ANSWER'),
P('Practice answer: the population expectation','Population probabilities supply different weights for the same losses.',[
E(r'0.2+0.5+0.3=1'),
E(r'R=0.2(0.5)+0.5(0)+0.3(0.5)'),
E(r'R=0.1+0+0.15=0.25'),
'The zero-loss row occurs half the time in this population, but only one-third of the observed sample. Therefore the population average is lower here.',
'The weights already sum to 1, so no further division is required. Loss per example, empirical risk and expected risk are related quantities with different roles.'],'WORKED ANSWER')]
for p in pages:
 for b in p['blocks']:
  if isinstance(b,dict) and 'eq' in b:
   import re
   b['eq']=re.sub(r'\\frac([0-9])([0-9N])',r'\\frac{\1}{\2}',b['eq'])
lossA=[.5,.5,2];lossB=[.125,0,.125];q=[.5,.25,.25]
assert sum(lossA)/3==1 and sum(x*y for x,y in zip(q,lossA))==.875
assert abs(sum(lossB)/3-1/12)<1e-12 and sum(x*y for x,y in zip(q,lossB))==.09375
checks=dict(A=dict(losses=lossA,empirical=1,risk=.875),B=dict(losses=lossB,empirical=1/12,risk=.09375),practice=dict(losses=[.5,0,.5],empirical=1/3,risk=.25))
(out/'checks.json').write_text(json.dumps(checks,indent=2))
spec=dict(number=15,title='Loss, empirical risk and expected risk',description='Compute individual losses, compare two kinds of average, and interpret empirical risk minimization.',source_short='Lecture 3 / PDF pp.101-107 / original finite-population illustration',source='Lecture 3 - Learning Neural Network.pdf, pages 101-107; binary cross-entropy connection to earlier logistic lesson.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
