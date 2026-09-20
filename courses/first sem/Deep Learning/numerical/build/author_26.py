from pathlib import Path
import json
from fractions import Fraction as F
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'26-rprop-state-trace';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':21}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
def trace(w,s,target,count):
 w=F(str(w));s=F(str(s));target=F(str(target));prev=w-target;rows=[]
 for a in range(1,count+1):
  old=w;oldp=prev;olds=s;delta=(1 if prev>0 else -1)*s;trial=w-delta;d=trial-target;product=prev*d
  if d==0:w=trial;prev=d;decision='stop'
  elif product>0:w=trial;prev=d;s=min(F('1.2')*s,F(1));decision='accept'
  else:s=max(F('.5')*s,F('.01'));decision='reject'
  rows.append(dict(attempt=a,old=float(old),prev=float(oldp),s=float(olds),delta=float(delta),trial=float(trial),d=float(d),product=float(product),decision=decision,w=float(w),nextprev=float(prev),nexts=float(s),trialloss=float((trial-target)**2/2)))
  if decision=='stop':break
 return rows
A=trace(0,.6,1,3);B=trace(1,.7,0,4)
pages=[P('RProp follows derivative signs and remembers state','Use the simplified rollback, shrink, retry convention in Lecture4 PDF page71.',[
 E(r'E(w)=\frac{1}{2}(w-1)^2,\qquad g(w)=w-1'),
 E(r'w=0,\quad prevD=-1,\quad s=0.6'),
 'Store three quantities: accepted parameter w, its derivative prevD, and a positive step magnitude s. Unlike ordinary gradient descent, the derivative magnitude does not directly set the move length.',
 E(r'\Delta=\mathrm{sign}(prevD)s,\qquad w_{trial}=w-\Delta'),
 'Sign is +1 for a positive derivative and -1 for a negative derivative. Delta is the signed quantity subtracted. A negative Delta therefore moves w upward.',
 'Attempt 1 uses the initial magnitude 0.6 immediately. There is no growth step before that first trial.']),
 P('Decide which state is carried to the next attempt','A trial is not an accepted parameter until the sign check passes.',[
 E(r'D=g(w_{trial}),\quad\mathrm{sign\ test}:\ prevD\cdot D'),
 'Same nonzero signs: accept the trial, replace prevD with D, and grow the positive magnitude by 1.2, capped at 1.',
 E(r's_{next}=\min(1.2s,1)'),
 'Opposite signs: undo the trial, keep the old accepted w and old prevD, and shrink the magnitude by 0.5, floored at 0.01.',
 E(r'w_{restored}=w_{trial}+\Delta,\quad s_{next}=\max(0.5s,0.01)'),
 'Here an exact zero derivative means stop at that point. Bounds apply to the positive magnitude before attaching its sign; this clarifies the signed min/max shorthand in the slide.'])]
def attempt_pages(rows,target,practice=False):
 ps=[];stage='WORKED ANSWER' if practice else 'WORKED EXAMPLE'
 for r in rows:
  q=r['attempt'];sign=1 if r['prev']>0 else -1
  blocks=[E(rf'w={r["old"]:g},\quad prevD={r["prev"]:g},\quad s={r["s"]:g}'),
   E(rf'\Delta=({sign})({r["s"]:g})={r["delta"]:g},\quad w_{{trial}}={r["old"]:g}-({r["delta"]:g})={r["trial"]:g}'),
   E(rf'D={r["trial"]:g}-{target:g}={r["d"]:g},\quad prevD\cdot D=({r["prev"]:g})({r["d"]:g})={r["product"]:g}')]
  if r['decision']=='accept':
   blocks.extend([E(rf's_{{next}}=\min(1.2({r["s"]:g}),1)={r["nexts"]:g}'),
    E(rf'(w,prevD,s)_{{next}}=({r["w"]:g},{r["nextprev"]:g},{r["nexts"]:g})'),
    'The sign product is positive. Accept this trial and store its derivative; the larger magnitude is for the next attempt.'])
  else:
   blocks.extend([E(rf'w_{{restored}}={r["trial"]:g}+({r["delta"]:g})={r["w"]:g}'),
    E(rf's_{{next}}=\max(0.5({r["s"]:g}),0.01)={r["nexts"]:g}'),
    E(rf'(w,prevD,s)_{{next}}=({r["w"]:g},{r["nextprev"]:g},{r["nexts"]:g})'),
    'The sign product is negative. Reject this trial; its derivative does not replace prevD. Retry from the restored accepted parameter.'])
  ps.append(P(('Practice: ' if practice else '')+f'attempt {q}: '+('accept and grow' if r['decision']=='accept' else 'rollback and shrink'),'Read the starting state first; use the next magnitude only on the next attempt.',blocks,stage))
 return ps
pages+=attempt_pages(A,1)
pages+=[P('Why rollback is not a loss-improvement test','The rejected trial can have lower loss than the accepted point.',[
 E(r'E(0.6)=\frac{1}{2}(0.6-1)^2=0.08'),
 E(r'E(1.32)=\frac{1}{2}(1.32-1)^2=0.0512'),
 'Even though 0.0512 is lower than 0.08, attempt2 is rejected because the derivative changes from -0.4 to +0.32. This simplified rule uses the sign change, not a loss comparison.',
 E(r'\mathrm{retry}:\quad0.6-(-0.36)=0.96'),
 E(r'E(0.96)=\frac{1}{2}(-0.04)^2=0.0008'),
 'Accepted parameters after the attempts are 0.6, 0.6, 0.96. Rejected attempts count as work, but do not advance the accepted parameter.']),
 P('Separate attempted points from accepted history','Crosses mark trials; a separate cross marks a rejected trial.',[
 {'image':'trace.png','width':650},
 'Attempt2 visits 1.32, then returns to the accepted 0.6. Attempt3 starts from 0.6 with the smaller magnitude, not from the rejected point.']),
 P('Clamp a magnitude, then attach its direction','A signed quantity and a positive magnitude are different objects.',[
 E(r's=0.9:\quad s_{grow}=\min(1.2(0.9),1)=\min(1.08,1)=1'),
 E(r's=0.015:\quad s_{shrink}=\max(0.5(0.015),0.01)=0.01'),
 E(r'prevD<0,\ s=1\Rightarrow\Delta=-1'),
 E(r'prevD>0,\ s=0.01\Rightarrow\Delta=+0.01'),
 'The lower and upper bounds protect the step length. Applying min or max directly to a negative signed step would give the wrong bound behavior.',
 'The lecture gives separate state for each parameter. In a network, each coordinate has its own derivative sign and step magnitude; they are not one shared learning rate.']),
 P('Your turn: four attempts with two reversals','Keep the same growth, shrink and bounds, but use a fresh quadratic.',[
 E(r'E(w)=\frac{1}{2}w^2,\quad g(w)=w'),
 E(r'w=1,\quad prevD=1,\quad s=0.7'),
 'Trace four attempts. For each, write the signed step, trial, trial derivative, sign product, decision, and full next state (w,prevD,s).',
 'Explain why a rejected negative derivative must not become prevD. Separately compute the bounded growth of 0.9 and bounded shrink of 0.015.',
 'The following pages show every attempted move. This practice follows the stated lecture variant; other RProp variants can use different reversal rules.'],'INDEPENDENT PRACTICE')]
pages+=attempt_pages(B,0,True)
pages.append(P('Practice checkpoint: track accepted state','Rejected moves keep the same accepted position and derivative.',[
 {'table':[['attempt','trial','decision','accepted w','prevD','next s'],['1','0.3','accept','0.3','0.3','0.84'],['2','-0.54','reject','0.3','0.3','0.42'],['3','-0.12','reject','0.3','0.3','0.21'],['4','0.09','accept','0.09','0.09','0.252']],'widths':[85,105,105,135,100,130]},
 'The bound answers are 1 and 0.01, as worked earlier. There are four attempts but only two accepted moves in this practice.',
 'Common errors: growing before the first trial, replacing prevD after rejection, continuing from a rejected parameter, using loss improvement as the sign test, or confusing the signed Delta with its positive magnitude.'],'WORKED ANSWER'))
fig,ax=plt.subplots(figsize=(9.5,3),layout='constrained');ax.plot([0,1,2,3],[0,.6,.6,.96],'o-',label='accepted parameter after attempt',color='#006E73');ax.scatter([1,2,3],[.6,1.32,.96],marker='x',s=100,color='#BD6A24',label='trial parameter');ax.axhline(1,ls='--',color='gray',label='minimum w=1');ax.set(xlabel='attempt number (0 = initialization)',ylabel='parameter w',xticks=[0,1,2,3]);ax.legend(fontsize=9);ax.grid(alpha=.2);fig.savefig(out/'trace.png',dpi=180);plt.close(fig)
assert [(r['w'],r['nextprev'],r['nexts']) for r in A]==[(.6,-.4,.72),(.6,-.4,.36),(.96,-.04,.432)]
assert [(r['w'],r['nexts']) for r in B]==[(.3,.84),(.3,.42),(.3,.21),(.09,.252)]
(out/'checks.json').write_text(json.dumps(dict(main=A,practice=B,arithmetic='exact fractions before display'),indent=2))
spec=dict(number=26,title='RProp: signs, rollback and stored state',description='Trace every attempted move in the lecture rollback variant, distinguish trial and accepted states, and solve a four-attempt practice.',source_short='Lecture4 PDF p.64-72; simplified bounded rule p.71 / N4.5',source='Lecture4 PDF pages64-72, especially page71: simplified RProp. Positive-magnitude bounding clarifies signed pseudocode; exact-zero stop convention stated. numerical-practice.md N4.5.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
