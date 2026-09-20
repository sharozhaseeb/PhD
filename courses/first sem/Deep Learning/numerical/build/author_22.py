from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'22-learning-rate-convergence';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':21}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('One loss, five learning rates','The starting point stays fixed so we can isolate the effect of step size.',[
 E(r'E(w)=2(w-1)^2=\frac{4}{2}(w-1)^2,\quad w_0=3'),
 E(r'g(w)=\frac{dE}{dw}=4(w-1),\quad w^*=1'),
 E(r'w_{k+1}=w_k-\eta g(w_k)'),
 'Eta is the learning rate: it multiplies the gradient to determine the parameter displacement. Iteration k=0 is initialization; k=1 means one completed update.',
 'The minimum is at w-star = 1, where loss and gradient are zero. The curvature, or second derivative, is a = 4. This quadratic is the N4.2 study example.']),
 P('Derive the signed parameter-error factor','Error here is the signed difference from the optimal parameter.',[
 E(r'e_k=w_k-1'),
 E(r'w_{k+1}-1=w_k-1-4\eta(w_k-1)'),
 E(r'e_{k+1}=(1-4\eta)e_k=re_k,\quad r=1-4\eta'),
 'A positive r keeps the error on the same side. A negative r switches sides of the minimum. Its magnitude tells us whether the distance shrinks or grows.',
 E(r'E_k=2e_k^2\quad\Longrightarrow\quad\frac{E_{k+1}}{E_k}=r^2'),
 'The loss ratio is defined when the old loss is nonzero. Absolute parameter-error ratio is |r|; do not confuse it with the squared ratio for loss.'])]
rates=[.1,.25,.4,.5,.6];checks=[]
names=['same-side convergence','minimum in one step','alternating convergence','nonshrinking oscillation','divergence']
for eta,name in zip(rates,names):
 w=3.;rows=[dict(k=0,w=w,g=4*(w-1),loss=2*(w-1)**2)];blocks=[]
 for k in range(2):
  g=4*(w-1);new=w-eta*g;loss=2*(new-1)**2
  blocks.extend([E(rf'g_{k}=4({w:g}-1)={g:g}'),E(rf'w_{{{k+1}}}={w:g}-{eta:g}({g:g})={new:g},\quad E_{{{k+1}}}=2({new:g}-1)^2={loss:g}')])
  rows.append(dict(k=k+1,w=new,g=4*(new-1),loss=loss));w=new
 r=1-4*eta
 blocks.extend([E(rf'r=1-4({eta:g})={r:g},\quad |r|={abs(r):g},\quad r^2={r*r:g}'),
  E(r'E_0=2(3-1)^2=8'), 'Compare the distance from 1 after each update, as well as the loss.'])
 pages.append(P(f'Learning rate {eta:g}: {name}','Evaluate each new gradient at the latest parameter, not at the original point.',blocks))
 for k in [1,2]:assert abs(rows[k]['w']-1-r*(rows[k-1]['w']-1))<1e-12
 checks.append(dict(eta=eta,r=r,rows=rows))
pages += [P('Compare paths and costs','Different parameter paths can produce exactly the same loss sequence.',[
 {'table':[['eta','r','w0, w1, w2','E0, E1, E2'],['0.1','0.6','3, 2.2, 1.72','8, 2.88, 1.0368'],['0.25','0','3, 1, 1','8, 0, 0'],['0.4','-0.6','3, -0.2, 1.72','8, 2.88, 1.0368'],['0.5','-1','3, -1, 3','8, 8, 8'],['0.6','-1.4','3, -1.8, 4.92','8, 15.68, 30.7328']],'widths':[80,80,255,270]},
 'Rates 0.1 and 0.4 have the same |r| and r-squared. One stays on one side; the other alternates, but their error magnitudes and losses match.',
 'At rate 0.5, this nonoptimal starting point never converges: it keeps switching between 3 and -1. Starting at the optimum would stay there for any finite rate.']),
 P('Picture the parameter paths after each update','The horizontal reference w=1 marks the minimum.',[
 {'image':'paths.png','width':665},
 'A crossing of the minimum does not by itself mean failure. Crossing with shrinking distance converges; crossing with constant or growing distance does not.']),
 P('Derive the stable interval','We need the error magnitude to shrink after each step.',[
 E(r'|r|<1\quad\Longleftrightarrow\quad -1<1-4\eta<1'),
 E(r'-2<-4\eta<0\quad\Longleftrightarrow\quad0<\eta<0.5'),
 'Dividing inequalities by a negative number reverses the signs. Rate zero makes no progress; the upper endpoint gives the oscillation seen earlier.',
 E(r'E=\frac{a}{2}(w-w^*)^2,\quad a>0\quad\Longrightarrow\quad0<\eta<\frac{2}{a}'),
 'This statement assumes a fixed learning rate and a positive-curvature quadratic. It is not an unconditional convergence guarantee for every neural-network loss.']),
 P('What linear convergence means','The name refers to a constant ratio of error magnitudes.',[
 E(r'|e_{k+1}|=q|e_k|,\quad0<q<1'),
 E(r'\eta=0.1:\quad|e_0|=2,\ |e_1|=1.2,\ |e_2|=0.72'),
 E(r'q=0.6,\qquad E_1/E_0=E_2/E_1=0.36'),
 'Each iteration removes the same fraction of the remaining distance: 40 percent here. The error shrinks geometrically, not by subtracting the same amount each time.',
 'An alternating path can have linear convergence too: rate 0.4 also has q=0.6. The one-step exact solution at rate 0.25 is a special case, not an asymptotic nonzero error ratio.']),
 P('Two directions can need different step sizes','A narrow bowl has one steep direction and one shallow direction.',[
 E(r'E(x,y)=\frac{1}{2}(x^2+100y^2)'),
 E(r'\nabla E=(x,100y),\qquad H=\mathrm{diag}(1,100)'),
 E(r'x_{k+1}=(1-\eta)x_k,\qquad y_{k+1}=(1-100\eta)y_k'),
 'The diagonal Hessian has eigenvalues 1 and 100. With rate 0.01, the error factors are 0.99 and 0: the steep direction finishes immediately, while the shallow direction moves slowly.',
 E(r'0<\eta<\min(2/1,2/100)=0.02'),
 'For a positive-definite quadratic, the largest eigenvalue sets the stable shared-rate bound 2/lambda-max.']),
 P('Work the two-direction example','Start at (1,1) and use eta = 0.01 for both coordinates.',[
 E(r'g_0=(1,100),\quad(x_1,y_1)=(1,1)-0.01(1,100)=(0.99,0)'),
 E(r'E_0=\frac{1+100}{2}=50.5,\quad E_1=\frac{0.99^2}{2}=0.49005'),
 E(r'g_1=(0.99,0),\quad(x_2,y_2)=(0.99,0)-0.01(0.99,0)'),
 E(r'=(0.9801,0),\quad E_2=\frac{0.9801^2}{2}=0.480298005'),
 'Most of the initial loss disappears in the steep direction. After that, the shallow-direction error shrinks by only 1 percent per update. This explains why a stable rate can still be slow.']),
 P('Your turn: same loss speed, different paths','Use a fresh quadratic and keep initialization separate from updates.',[
 E(r'F(w)=(w+2)^2,\quad w_0=0'),
 'Calculate two updates and all three losses for rates 0.25 and 0.75. Find the minimum, curvature, signed error factors, absolute error ratios and loss ratios.',
 'Explain why one path alternates but both losses can be identical. Derive the stable-rate interval and decide whether both chosen rates lie inside it.'],'INDEPENDENT PRACTICE'),
 P('Practice: derivatives and stability','Here the optimum is -2, so the signed error is w+2.',[
 E(r'g(w)=2(w+2),\quad a=2,\quad w^*=-2'),
 E(r'e_{k+1}=(1-2\eta)e_k,\quad e_0=2'),
 E(r'\eta=0.25:\ r=0.5;\qquad\eta=0.75:\ r=-0.5'),
 E(r'|r|=0.5,\quad r^2=0.25,\quad0<\eta<2/2=1'),
 'Both rates are stable for this quadratic. Both halve the error magnitude and quarter the loss each step, but only the negative factor switches sides.'],'WORKED ANSWER')]
for eta in [.25,.75]:
 w=0.;blocks=[E(r'F_0=(0+2)^2=4')]
 for k in range(2):
  g=2*(w+2);n=w-eta*g
  blocks.extend([E(rf'g_{k}=2({w:g}+2)={g:g},\quad w_{{{k+1}}}={w:g}-{eta:g}({g:g})={n:g}'),E(rf'F_{{{k+1}}}=({n:g}+2)^2={(n+2)**2:g}')]);w=n
 blocks.append('Distances from -2 are 2, 1 and 0.5. Squaring them gives losses 4, 1 and 0.25 in either path.')
 pages.append(P(f'Practice: full working at rate {eta:g}','Evaluate the gradient again at each new parameter.',blocks,'WORKED ANSWER'))
fig,ax=plt.subplots(figsize=(10,3.2),layout='constrained')
for eta in [.1,.4,.5,.6]:
 ws=[3.]
 for k in range(5):ws.append(ws[-1]-eta*4*(ws[-1]-1))
 ax.plot(range(6),ws,'o-',label=f'eta = {eta:g}')
ax.axhline(1,color='black',ls='--',lw=1);ax.set(xlabel='completed updates k',ylabel='parameter w');ax.legend(ncol=2);ax.grid(alpha=.2);fig.savefig(out/'paths.png',dpi=180);plt.close(fig)
(out/'checks.json').write_text(json.dumps(dict(main=checks,multidimensional_losses=[50.5,.49005,.480298005]),indent=2))
spec=dict(number=22,title='Learning rate and convergence',description='Calculate converging, oscillating and diverging steps, separate parameter-error ratios from loss ratios, and solve a fresh quadratic practice.',source_short='Lecture4 PDF p.31-49 / numerical-practice N4.2-N4.3',source='Lecture4 PDF pages31-36: scalar convergence; pages37-49: multivariate curvature; numerical-practice.md N4.2-N4.3. Original study values.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
