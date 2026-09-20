from pathlib import Path
import json
from fractions import Fraction as F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'29-batch-sgd-minibatch';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
def run(groups,eta):
 w=F(0);eta=F(str(eta));rows=[]
 for n,ts in enumerate(groups,1):
  gs=[w-F(t) for t in ts];g=sum(gs)/len(gs);nw=w-eta*g
  rows.append(dict(update=n,targets=ts,w=float(w),gradients=list(map(float,gs)),mean=float(g),new=float(nw)));w=nw
 return rows
A={'Full batch':run([[0,2,4,6]],.1),'SGD forward':run([[0],[2],[4],[6]],.1),'SGD reverse':run([[6],[4],[2],[0]],.1),'Mini-batch':run([[0,2],[4,6]],.1)}
B={'Full batch':run([[1,3]],.2),'SGD forward':run([[1],[3]],.2),'SGD reverse':run([[3],[1]],.2)}
loss=lambda w:sum(.5*(w-t)**2 for t in [0,2,4,6])/4
pages=[P('Keep the model simple to isolate batching','One trainable number predicts the same output for every example.',[
 E(r'\widehat y_i=w,\qquad(t_1,t_2,t_3,t_4)=(0,2,4,6)'),
 E(r'\ell_i(w)=\frac{1}{2}(w-t_i)^2,\qquad J(w)=\frac{1}{4}\sum_{i=1}^4\ell_i(w)'),
 E(r'\frac{d\ell_i}{dw}=\frac{1}{2}\cdot2(w-t_i)\cdot1=w-t_i'),
 E(r'w_0=0,\qquad\eta=0.1'),
 'This constant-output model intentionally removes network details so we can see when gradients are evaluated and when parameters change.',
 'Use the same data and initial parameter for each method. The learning rate is fixed here to isolate batching; lecture algorithms can also schedule it.']),
 P('Examples, batches, updates and epochs','An epoch is one pass through all training examples.',[
 'An example is one data item with a target. Its gradient is computed at the current parameter. An update changes the parameter using a gradient or an average of gradients.',
 'Full batch: evaluate all four example gradients at the same old w, average once, then update once.',
 'SGD here means batch size one: evaluate one example gradient, update immediately, then evaluate the next example at the changed parameter.',
 'Mini-batch: average gradients from a small group at one common w, update once, then use the new w for the next group.',
 E(r'g_B(w)=\frac{1}{|B|}\sum_{i\in B}(w-t_i),\quad w_{new}=w-\eta g_B(w)'),
 'B is the set of example indices in this batch; |B| is its number of examples. Our chosen orders are fixed for reproducibility; the lecture shuffles examples.'])]
def worked(rows,eta,name,practice=False):
 ps=[];stage='WORKED ANSWER' if practice else 'WORKED EXAMPLE'
 for r in rows:
  ts=r['targets'];w=r['w'];blocks=[E(rf'w_{{old}}={w:g},\quad\mathrm{{targets}}=({",".join(str(t) for t in ts)})')]
  for t,g in zip(ts,r['gradients']):blocks.append(E(rf'g_{{t={t}}}={w:g}-{t}={g:g}'))
  if len(ts)>1:
   terms='+'.join(f'({g:g})' for g in r['gradients'])
   blocks.append(E(rf'\overline{{g}}=\frac{{{terms}}}{{{len(ts)}}}={r["mean"]:g}'))
  blocks.append(E(rf'w_{{new}}={w:g}-{eta:g}({r["mean"]:g})={r["new"]:g}'))
  blocks.append('Every gradient above uses exactly the same old parameter. Only after averaging do we change w.' if len(ts)>1 else 'The next example will use this newly updated parameter. Do not return to the original w when computing its gradient.')
  ps.append(P(('Practice: ' if practice else '')+f'{name}, update {r["update"]}','Reset to the original start only when beginning a different method.',blocks,stage))
 return ps
for name in A:pages+=worked(A[name],.1,name)
table=[['method','parameter after each update','updates']]
for name,rows in A.items():table.append([name,', '.join(f'{r["new"]:g}' for r in rows),str(len(rows))])
pages+=[P('Same epoch, different sequences of parameter states','Each method evaluates four example gradients in this one epoch.',[
 {'table':table,'widths':[165,420,95]},
 'Full batch evaluates all four gradients at w=0. SGD changes w between examples, which is why reversing the order changes the result. Mini-batches change w only between groups.',
 'The comparison uses equal one-epoch example-gradient counts, but different numbers of updates. It is not an equal-runtime claim, and the same rate is not guaranteed to be optimal for every method.']),
 P('Compare paths by examples processed','Each curve advances through the same four training examples.',[
 {'image':'paths.png','width':650},
 'Full batch first changes w after four examples. Mini-batches change it after two and four examples. SGD changes it after each example; the zero first forward-order gradient leaves w unchanged.']),
 P('Report the full objective at the final parameter','All reported J values use all four targets, even for SGD or mini-batch training.',[
 E(r'J(0.3)=\frac{(0.3-0)^2+(0.3-2)^2+(0.3-4)^2+(0.3-6)^2}{8}'),
 E(r'=\frac{0.09+2.89+13.69+32.49}{8}=6.145'),
 'The divisor is 8 because each loss has factor 1/2 and the objective averages four losses.',
 {'table':[['method','final w','J on all four examples']]+[[n,f'{rs[-1]["new"]:g}',f'{loss(rs[-1]["new"]):.8f}'] for n,rs in A.items()],'widths':[190,170,320]},
 'These values describe this fixed-rate, one-epoch example. They do not prove a universal ranking of the methods.']),
 P('Count updates and retain the last partial batch','Batch size is 20, but the dataset has 103 examples.',[
 E(r'103=5(20)+3\quad\Longrightarrow\quad\mathrm{sizes}:20,20,20,20,20,3'),
 E(r'\mathrm{updates/epoch}=\lceil103/20\rceil=6'),
 E(r'20\ \mathrm{epochs}:\quad\mathrm{mini}=20(6)=120'),
 E(r'\mathrm{SGD}=20(103)=2060,\qquad\mathrm{full\ batch}=20(1)=20'),
 'For the last mini-batch gradient, divide its gradient sum by its actual size 3. That divisor is distinct from the 103-example mean used to report the full dataset objective.',
 'The ceiling brackets mean round up to the next integer. We retain the partial batch; dropping it would change the update count.']),
 P('Your turn: fresh targets and a different rate','Restart each method from w0=0.',[
 E(r'(t_1,t_2)=(1,3),\quad\eta=0.2,\quad\widehat y=w'),
 'Calculate one full-batch update and one complete SGD epoch in each order: [1,3] and [3,1]. Use the same half-squared per-example loss as before.',
 'List every gradient and intermediate parameter. Explain why the full-batch average uses the original w throughout, while SGD does not.',
 'Separately, retain all examples in a dataset of size10 with batch size4. Give each batch size, updates per epoch, and the divisor of the last gradient mean.'],'INDEPENDENT PRACTICE')]
for name in B:pages+=worked(B[name],.2,name,True)
pages.append(P('Practice checkpoint and remainder calculation','Different orders can produce different parameter states after one epoch.',[
 E(r'w_{full}=0.4,\qquad w_{forward}=0.76,\qquad w_{reverse}=0.68'),
 E(r'10=2(4)+2\quad\Longrightarrow\quad\mathrm{batch\ sizes}=4,4,2'),
 E(r'\mathrm{updates/epoch}=3,\qquad g_{last}=\frac{g_9+g_{10}}{2}'),
 'The last gradient mean divides by 2, not by 4 or 10. A full-dataset mean loss would instead average all ten example losses.',
 'Common errors: changing w partway through a full-batch average, averaging gradients from different parameter states, using the nominal size for a shorter last batch, or confusing an epoch with an update.'],'WORKED ANSWER'))
fig,ax=plt.subplots(figsize=(9.5,3),layout='constrained')
for name,rs in A.items():
 xs=[0];ys=[0];n=0
 for r in rs:n+=len(r['targets']);xs.append(n);ys.append(r['new'])
 ax.step(xs,ys,where='post',marker='o',label=name)
ax.set(xlabel='examples processed within epoch',ylabel='parameter after completed update',xticks=[0,1,2,3,4]);ax.legend(fontsize=9);ax.grid(alpha=.2);fig.savefig(out/'paths.png',dpi=180);plt.close(fig)
assert [rs[-1]['new'] for rs in A.values()]==[.3,1.122,.9414,.59]
assert [rs[-1]['new'] for rs in B.values()]==[.4,.76,.68]
(out/'checks.json').write_text(json.dumps(dict(main=A,practice=B,final_full_objectives={n:loss(rs[-1]['new']) for n,rs in A.items()},arithmetic='exact fraction traces'),indent=2))
spec=dict(number=29,title='Full batch, SGD and mini-batches',description='Trace identical data through different update groupings and orders, report the full objective, count remainder batches, and solve fresh practice.',source_short='Lecture5 PDF p.6-39,77-82 / explicit fixed-rate N6.1 example',source='Lecture5 PDF pages6-39: batch/incremental/SGD; pages77-82: mini-batch, especially algorithm page82. numerical-practice.md N6.1; fixed rate and retained partial batch explicitly stated.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
