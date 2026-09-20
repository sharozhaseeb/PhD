from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'13-perceptron-learning';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':21}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('Learn a threshold neuron from mistakes','Lecture 3, PDF page 41: labels are +1 and -1, with a unit-size update.',[
'Original study data, always visited in this order: A = (1,0), target +1; B = (0,1), target -1; C = (1,1), target +1.',
E(r'X=(1,x_1,x_2),\quad W=(b,w_1,w_2),\quad s=W^T X=b+w_1x_1+w_2x_2'),
'The leading 1 is a bookkeeping input for the bias. It is not another measured feature.',
E(r'\hat y=+1\ \mathrm{if}\ s\geq0;\quad\hat y=-1\ \mathrm{if}\ s<0'),
'The slide does not define sign(0). We choose +1 explicitly. These labels differ from the 0/1 labels used in logistic regression.']),
P('Update only after a mistaken prediction','An epoch is one complete pass through A, B, C in that order.',[
E(r'\hat y\neq y:\quad W_{\mathrm{new}}=W_{\mathrm{old}}+yX'),
E(r'\hat y=y:\quad W_{\mathrm{new}}=W_{\mathrm{old}}'),
E(r'W_{\mathrm{start}}=(0,0,0)'),
'Use the newest weights for the very next example. The update is not a batch average and does not wait until the epoch ends.',
'Stop only after an entire epoch has no classification errors. With our tie rule, score zero is correct for target +1 and incorrect for target -1.'])]
D=[('A',[1,1,0],1),('B',[1,0,1],-1),('C',[1,1,1],1)]
W=[0,0,0];trace=[]
for epoch in range(1,5):
 for name,X,y in D:
  old=W[:];s=sum(a*b for a,b in zip(W,X));pred=1 if s>=0 else -1;wrong=pred!=y
  if wrong:W=[a+y*b for a,b in zip(W,X)]
  trace.append(dict(epoch=epoch,point=name,X=X,target=y,old=old,score=s,prediction=pred,new=W[:],mistake=wrong))
  tup=lambda v:'('+','.join(map(str,v))+')'
  blocks=[E(rf'W_{{\mathrm{{old}}}}={tup(old)},\quad X={tup(X)},\quad y={y:+d}'),
   E(rf's=({old[0]})+({old[1]})({X[1]})+({old[2]})({X[2]})={s}'),
   E(rf'\hat y={pred:+d},\quad y={y:+d}\quad\Rightarrow\quad\mathrm{{'+('mistake' if wrong else 'correct')+'}')]
  if wrong:
   blocks.extend([E(rf'yX=({y}){tup(X)}={tup([y*a for a in X])}'),E(rf'W_{{\mathrm{{new}}}}={tup(old)}+{tup([y*a for a in X])}={tup(W)}'),
   'Carry these updated values into the next visit. The bias changes too because the first input component is 1.'])
  else:blocks.extend([E(rf'W_{{\mathrm{{new}}}}=W_{{\mathrm{{old}}}}={tup(W)}'),'No update: a correctly classified point does not change any parameter.'])
  pages.append(P(f'Epoch {epoch}, point {name}: '+('correct the mistake' if wrong else 'keep the weights'),f'Visit {len(trace)} of 12. Target label {y:+d}; prediction follows the stated sign rule.',blocks))
assert W==[-1,2,-1]
assert [sum(t['mistake'] for t in trace if t['epoch']==e) for e in range(1,5)]==[2,2,1,0]
pages.extend([
P('Why the mistake update helps this point','Examine the first mistaken visit: B in epoch 1.',[
E(r'X_B=(1,0,1),\quad y_B=-1,\quad W_{\mathrm{old}}=(0,0,0)'),
E(r'W_{\mathrm{new}}=(-1,0,-1),\quad s_{\mathrm{new}}=-1+0(0)-1(1)=-2'),
E(r'\Delta s=(yX)^T X=y\Vert X\Vert^2=(-1)(1^2+0^2+1^2)=-2'),
'Squared length means the sum of squared components. The score moves downward toward the negative target. A positive target moves its own score upward. Other points can become wrong again, which is why we repeat epochs.',
'Do not replace the mistake test by y times score <= 0 under this tie convention: a zero score with target +1 is already correct.']),
P('Verify the final neuron and stop','The fourth epoch has zero errors; the third still had one.',[
{'table':[['epoch','mistakes','weights at end'],[1,2,'(0,1,0)'],[2,2,'(0,2,0)'],[3,1,'(-1,2,-1)'],[4,0,'(-1,2,-1)']],'widths':[130,160,260]},
E(r's=-1+2x_1-x_2'),
E(r'A:s=1\Rightarrow+1;\quad B:s=-2\Rightarrow-1;\quad C:s=0\Rightarrow+1'),
'Five updates occurred over twelve visits. A visit, a mistake update and an epoch are different counts.']),
P('Picture the final separating boundary','Points on the line receive +1 because sign(0) = +1.',[
{'image':'boundary.png','width':640},
'The boundary is 2x1 - x2 - 1 = 0. C lies exactly on it; our tie convention matters.',
'Lecture 3, pages 53-54: a single perceptron cannot solve nonseparable data such as XOR. Repeating the loop then need not produce an error-free epoch.']),
P('Your turn: two points, one measured feature','Keep +1/-1 labels, sign(0) = +1 and the unit mistake update.',[
E(r'X=(1,x),\quad W=(b,w),\quad W_{\mathrm{start}}=(0,-1)'),
'Fixed order: first x = -1 with target -1; then x = 2 with target +1.',
'Show the old weights, score, predicted label and resulting weights for every visit. Repeat until a complete epoch has no errors.',
'How many visits, mistake updates and epochs are required? Explain why the first epoch alone is not enough.'],'INDEPENDENT PRACTICE'),
P('Practice answer: correct both first-epoch errors','The second point uses the weights already changed by the first.',[
E(r'x=-1:\quad s=0+(-1)(-1)=1\Rightarrow\hat y=+1\neq-1'),
E(r'W=(0,-1)+(-1)(1,-1)=(0,-1)+(-1,1)=(-1,0)'),
E(r'x=2:\quad s=-1+0(2)=-1\Rightarrow\hat y=-1\neq+1'),
E(r'W=(-1,0)+(+1)(1,2)=(-1,0)+(1,2)=(0,2)'),
'Both visits made an update. Even though the final weights may now be correct, the stopping rule requires another complete pass.'],'WORKED ANSWER'),
P('Practice answer: check the whole second epoch','The first correct point is not yet an error-free epoch.',[
E(r'x=-1:\quad s=0+2(-1)=-2\Rightarrow\hat y=-1=y'),
E(r'W\ \mathrm{stays}\ (0,2)'),
E(r'x=2:\quad s=0+2(2)=4\Rightarrow\hat y=+1=y'),
E(r'W\ \mathrm{stays}\ (0,2)'),
'Now stop: 2 epochs, 4 visits, 2 mistake updates. Remember to update the bias, preserve visit order, and distinguish a score from its predicted label.'],'WORKED ANSWER')])
fig,ax=plt.subplots(figsize=(8,2.8),layout='constrained');ax.plot([-.1,1.3],[-1.2,1.6],color='#006E73',label='score = 0');ax.scatter([1,1],[0,1],color='#006E73',marker='+',s=110,label='target +1');ax.scatter([0],[1],color='#ad5935',s=70,label='target -1')
for x,y,label in [(1,0,'A'),(0,1,'B'),(1,1,'C (on line)')]:ax.annotate(label,(x,y),xytext=(7,6),textcoords='offset points')
ax.set(xlim=(-.2,1.5),ylim=(-.4,1.6),xlabel='x1',ylabel='x2');ax.legend(loc='lower left');ax.grid(alpha=.2);fig.savefig(out/'boundary.png',dpi=180);plt.close(fig)
(out/'checks.json').write_text(json.dumps(trace,indent=2))
spec=dict(number=13,title='Perceptron learning',description='Every visit and mistake update across four epochs, with an independent practice problem.',source_short='Lecture 3 / PDF pp.41,53-54 / explicit sign(0)=+1 convention',source='Lecture 3 - Learning Neural Network.pdf, algorithm page 41 and nonseparable data pages 53-54. Original study dataset.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
