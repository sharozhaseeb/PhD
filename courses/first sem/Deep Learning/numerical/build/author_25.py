from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'25-learning-rate-schedules';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('Read the exact schedule and its index','Lecture4 PDF page57 supplies these three formulas.',[
 E(r'\eta_k=\frac{\eta_0}{k+1},\qquad\eta_k=\frac{\eta_0}{(k+1)^2},\qquad\eta_k=\eta_0e^{-\beta k}'),
 'Eta-zero is the starting learning rate. k is the update index, beginning at zero. The rate at index k moves the current parameter to the next one.',
 'The slide calls the first schedule linear decay and the second quadratic decay. Their denominators are linear and quadratic in k+1: both are reciprocal schedules.',
 'In particular, linear here does not mean subtract a fixed amount from the rate. Beta is a positive exponential decay constant, separate from any momentum coefficient.',
 E(r'\eta_0=0.12,\qquad\beta=\ln2'), E(r'w_{k+1}=w_k-\eta_k g(w_k)')]),
 P('Reciprocal linear: substitute k before dividing','Every denominator uses k+1, including the first update.',[
 E(r'k=0:\quad\eta_0=0.12/(0+1)=0.12'),
 E(r'k=1:\quad\eta_1=0.12/(1+1)=0.06'),
 E(r'k=2:\quad\eta_2=0.12/(2+1)=0.04'),
 E(r'k=3:\quad\eta_3=0.12/(3+1)=0.03'),
 'The drops are 0.06, 0.02 and 0.01, so the rate does not decrease by a constant amount. Starting at k=1 would incorrectly skip the original rate.']),
 P('Reciprocal quadratic: square the whole denominator','Parentheses determine which quantity is squared.',[
 E(r'k=0:\quad\eta_0=0.12/(0+1)^2=0.12'),
 E(r'k=1:\quad\eta_1=0.12/(1+1)^2=0.12/4=0.03'),
 E(r'k=2:\quad\eta_2=0.12/(2+1)^2=0.12/9\approx0.01333333'),
 E(r'k=3:\quad\eta_3=0.12/(3+1)^2=0.12/16=0.0075'),
 'At k=2 the denominator is 9, not k-squared plus 1 = 5. It decays faster than the reciprocal-linear schedule with the same initial rate.']),
 P('Exponential: use the logarithm identity','Beta=ln2 means multiplying by one half at each update.',[
 E(r'e^{-k\ln2}=2^{-k}\quad\Longrightarrow\quad\eta_k=0.12(2^{-k})'),
 E(r'k=0:\quad0.12(2^0)=0.12'),
 E(r'k=1:\quad0.12(2^{-1})=0.12/2=0.06'),
 E(r'k=2:\quad0.12(2^{-2})=0.12/4=0.03'),
 E(r'k=3:\quad0.12(2^{-3})=0.12/8=0.015'),
 'The natural logarithm ln2 is the number whose exponential is 2. A negative exponent makes the multiplier smaller as k increases.']),
 P('Compare the first four scheduled rates','All three agree at initialization, then decay differently.',[
 {'table':[['k','reciprocal linear','reciprocal quadratic','exponential'],['0','0.12','0.12','0.12'],['1','0.06','0.03','0.06'],['2','0.04','0.01333333','0.03'],['3','0.03','0.0075','0.015']],'widths':[70,200,225,190]},
 'These are alternative schedules. Do not apply all three successively to one rate unless a different rule explicitly says to combine them.',
 'A rate table is not a parameter table: actual parameter changes also depend on the current gradient.']),
 P('See the rates over more update indices','The plotted points include k=0 rather than starting at k=1.',[
 {'image':'schedules.png','width':650},
 'Exponential decay has a constant multiplicative ratio. The reciprocal schedules have ratios that vary with the update index. A lower rate does not automatically imply better training.']),
 P('Apply the rate with the matching current gradient','Use only reciprocal-linear decay in this worked parameter trace.',[
 E(r'E(w)=\frac{1}{2}w^2,\quad g(w)=w,\quad w_0=1'),
 E(r'k=0:\quad\eta_0=0.12,\quad w_1=1-0.12(1)=0.88'),
 E(r'k=1:\quad\eta_1=0.06,\quad w_2=0.88-0.06(0.88)=0.8272'),
 E(r'k=2:\quad\eta_2=0.04,\quad w_3=0.8272-0.04(0.8272)=0.794112'),
 'Notice both the rate and the gradient change. At update k=2, use the gradient at w2, then obtain w3. The first rate is not reused for every step.']),
 P('A plateau rule responds to measured progress','The lecture says reduce the rate when training or held-out performance stagnates.',[
 'For this study example, measure validation loss after each epoch. An epoch means a pass through the training examples; its count here begins at 1, unlike the update index k.',
 'Chosen rule: improve only if the new validation loss is strictly below the best seen so far. After two consecutive epochs without improvement, multiply the current rate by 0.1.',
 'Reset the no-improvement counter after a new best or a rate drop. The reduced rate takes effect in the next epoch. Retain the learned parameters.',
 E(r'0.12(0.1)=0.012,\qquad0.012(0.1)=0.0012'),
 'This precise patience rule is an illustrative choice. Page57 gives the stagnation-triggered idea and multiplicative reduction, not these exact counter settings.']),
 P('Trace the plateau decision at every epoch','Best is the lowest validation loss observed; smaller is better.',[
 {'table':[['epoch','val loss','best','counter/action','next rate'],['1','0.500','0.500','new best; 0','0.12'],['2','0.450','0.450','new best; 0','0.12'],['3','0.460','0.450','1','0.12'],['4','0.470','0.450','2: drop; reset to 0','0.012'],['5','0.440','0.440','new best; 0','0.012'],['6','0.445','0.440','1','0.012'],['7','0.446','0.440','2: drop; reset to 0','0.0012']],'widths':[70,95,95,270,145]},
 'Epoch 4 used rate 0.12; its decision sets rate 0.012 for epoch 5. The decision after epoch 7 sets rate 0.0012 for epoch 8. No earlier update is changed retroactively.']),
 P('Your turn: new initial rate and decay constant','Calculate the scheduled rate before updating a supplied parameter state.',[
 E(r'\eta_0=0.2,\quad k=2,\quad\beta=\ln4'),
 'Calculate reciprocal-linear, reciprocal-quadratic and exponential rates at k=2. Show the substituted denominator or exponent.',
 E(r'E(w)=\frac{1}{2}w^2,\quad\mathrm{supplied}\ w_2=2'),
 'Using only the reciprocal-quadratic rate, calculate w3. This w2 is an independent supplied practice state, not the result of the earlier main-example updates.',
 'Explain the difference between an update-index schedule and the epoch-based plateau rule.'],'INDEPENDENT PRACTICE'),
 P('Practice: rates and the next parameter','Use k+1=3 before squaring the denominator.',[
 E(r'\eta_{2,linear}=0.2/(2+1)=0.2/3\approx0.06666667'),
 E(r'\eta_{2,quadratic}=0.2/(2+1)^2=0.2/9\approx0.02222222'),
 E(r'\eta_{2,exp}=0.2e^{-2\ln4}=0.2(4^{-2})=0.2/16=0.0125'),
 E(r'g(w_2)=2,\quad w_3=2-\frac{0.2}{9}(2)=2-\frac{0.4}{9}\approx1.95555556'),
 'The formula schedules change with k regardless of measured validation progress. The plateau rule changes only after its stated no-improvement trigger; it keeps the current learned parameters.'],'WORKED ANSWER')]
fig,ax=plt.subplots(figsize=(9.5,3),layout='constrained');k=np.arange(9)
for vals,lab in [(.12/(k+1),'reciprocal linear'),(.12/(k+1)**2,'reciprocal quadratic'),(.12*2.**(-k),'exponential; beta=ln2')]:ax.plot(k,vals,'o-',label=lab)
ax.set(xlabel='parameter-update index k',ylabel='learning rate eta_k');ax.legend();ax.grid(alpha=.2);fig.savefig(out/'schedules.png',dpi=180);plt.close(fig)
assert np.allclose(.12*np.exp(-math.log(2)*k),.12*2.**(-k))
w=1.;trace=[]
for i in range(3):rate=.12/(i+1);g=w;w=w-rate*g;trace.append(dict(k=i,rate=rate,gradient=g,new_w=w))
assert abs(w-.794112)<1e-12
best=float('inf');counter=0;rate=.12;plateau=[]
for epoch,loss in enumerate([.5,.45,.46,.47,.44,.445,.446],1):
 if loss<best:best=loss;counter=0
 else:counter+=1
 dropped=counter==2
 if dropped:rate*=.1;counter=0
 plateau.append(dict(epoch=epoch,loss=loss,best=best,counter=counter,dropped=dropped,next_rate=rate))
assert [r['epoch'] for r in plateau if r['dropped']]==[4,7]
(out/'checks.json').write_text(json.dumps(dict(update_trace=trace,plateau=plateau),indent=2))
spec=dict(number=25,title='Learning-rate schedules and indexing',description='Substitute every schedule index, apply changing rates to gradient descent, trace a plateau rule, and solve fresh practice.',source_short='Lecture4 PDF p.57 / exact reciprocal schedules / N4.4',source='Lecture4 PDF page57: reciprocal-linear, reciprocal-quadratic, exponential and stagnation-triggered multiplicative decay. numerical-practice.md N4.4; precise plateau counter is a labeled study extension.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
