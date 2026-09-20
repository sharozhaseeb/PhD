from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'38-early-stopping-model-selection';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
train=[.65,.50,.42,.35,.30,.25];val=[.60,.50,.51,.49,.495,.50]
def trace(vals):
 best=float('inf');ep=0;bad=0;rows=[]
 for e,v in enumerate(vals,1):
  prev=best;improve=v<best
  if improve:best=v;ep=e;bad=0
  else:bad+=1
  rows.append(dict(epoch=e,value=v,previous=prev if prev!=float('inf') else None,improve=improve,best=best,checkpoint=ep,bad=bad,stop=bad>=2))
  if bad>=2:break
 return rows
main=trace(val);fresh=trace([.4,.35,.35,.36,.30])
pages=[P('Choose when to stop and what to restore','Lecture 5 page160 motivates early stopping with held-out validation performance.',[
 'Training loss guides parameter gradients. Validation loss guides the stated checkpoint and stopping rule. The test set is reserved for final evaluation, outside repeated run or model selection.',
 'A checkpoint stores the actual model parameters at an epoch, not just its loss number. Stopping at one epoch does not mean its parameters are the best saved ones.',
 'The lecture gives the concept; the precise patience rule below is chosen for this study example. Different declared rules can stop at different epochs.']),
P('State the rule before reading future losses','Lower validation loss is better; min_delta=0 and patience=2.',[
 'Improvement means a strict decrease below the best validation loss seen so far. Equality is not improvement. With min_delta=0, even a tiny strict decrease counts.',
 'On improvement: replace the best loss, save that epoch checkpoint and reset the consecutive-failure counter to zero.',
 'Otherwise: leave the best checkpoint unchanged and add one to the counter. Stop immediately after an epoch makes the counter reach2.',
 'Restore the saved best checkpoint for evaluation. Because every strict decrease counts, the checkpoint reference and the patience reference are the same best loss.',
 E(r'\mathrm{improve}\Longleftrightarrow v_e<v_{best};\quad\mathrm{stop}\Longleftrightarrow\mathrm{bad\ count}\geq2')]),
P('Read the supplied training and validation history','Each row is evaluated after completing that epoch.',[
 {'table':[['epoch','training loss','validation loss'],['1','.65','.60'],['2','.50','.50'],['3','.42','.51'],['4','.35','.49'],['5','.30','.495'],['6','.25','.50']],'widths':[130,240,260]},
 'Training loss falls throughout. The rule will still stop when validation loss fails to improve for two consecutive epochs. Read rows in time order; do not choose actions using later values.'])]
for inds,title in [([0,1],'Epochs 1 and 2: save improvements'),([2,3],'Epochs 3 and 4: fail, then reset'),([4,5],'Epochs 5 and 6: patience is exhausted')]:
 blocks=[]
 for i in inds:
  r=main[i];e=r['epoch'];prev='no checkpoint' if r['previous'] is None else f'{r["previous"]:g}'
  if r['previous'] is None:blocks+=['Epoch1 is the first observation: save its checkpoint and initialize the best validation loss.']
  else:blocks+=[E(rf'\mathrm{{epoch}}\ {e}:\quad{r["value"]:g}'+('<' if r['improve'] else '>')+rf'{r["previous"]:g}\quad\Longrightarrow\quad\mathrm{{'+('improves' if r['improve'] else r'no\ improvement')+'}')]
  blocks += [E(rf'\mathrm{{best\ loss}}={r["best"]:g},\quad\mathrm{{checkpoint}}={r["checkpoint"]},\quad\mathrm{{counter}}={r["bad"]}')]
 blocks.append('The counter reaches2 after epoch6: stop now. The best checkpoint remains epoch4.' if inds[-1]==5 else 'Saving a new best checkpoint resets the counter; a failure does not erase the previously saved parameters.')
 pages.append(P(title,'Compare each new validation value with the best seen so far.',blocks))
pages += [P('See stopping and restoration as different events','The best validation checkpoint is earlier than the stopping epoch.',[
 {'image':'history.png','width':650},
 'Stop after epoch6, then load epoch4 parameters. The smaller training loss at epoch6 is not the checkpoint criterion. This is a selection heuristic, not proof of best possible generalization.']),
P('Restore the model, not just a recorded score','The six-epoch run chooses checkpoint4 for final evaluation.',[
 {'table':[['decision','result'],['stopping epoch','6'],['restored checkpoint','4'],['validation loss of restored model','.49'],['training loss at that checkpoint','.35']],'widths':[345,320]},
 'For inference, restore the saved model parameters. If training is deliberately resumed, a faithful training checkpoint also needs optimizer state and counters.',
 'Use validation data for architecture, learning rate and checkpoint choices. Keep the test set out of these choices, then evaluate the selected procedure on it.']),
P('Count hyperparameter settings and seeded runs','A configuration chooses one value from each setting list.',[
 E(r'3\ \mathrm{rates}\times2\ \mathrm{regularization\ values}\times2\ \mathrm{batch\ sizes}=12'),E(r'12\ \mathrm{configurations}\times3\ \mathrm{seeds}=36\ \mathrm{runs}'),
 'A seed controls the pseudorandom realization, such as initialization or shuffling. Three seeds repeat a configuration; they do not create three new hyperparameter settings.',
 'Choose a validation-based comparison procedure in advance, such as mean validation score across seeds. Do not select settings by repeatedly looking at final test scores.']),
P('Bagging: sample training data for several models','A conceptual companion to lecture pages145-149.',[
 {'image':'bagging.png','width':680},
 'The illustrated bootstrap samples draw training IDs with replacement, so duplicates are allowed. Train separate models, then combine their predictions on a new example. Held-out test examples are not bootstrap training inputs.']),
P('Declare how the ensemble combines predictions','Two common aggregation choices are different procedures.',[
 E(r'\mathrm{hard\ predictions}=(1,0,1)\Longrightarrow\mathrm{majority}=1'),E(r'\mathrm{probabilities}=(0.8,0.4,0.7)'),E(r'\mathrm{mean\ probability}=(0.8+0.4+0.7)/3=1.9/3\approx0.633333'),E(r'\mathrm{threshold}\ 0.5\Longrightarrow\mathrm{mean\ probability\ prediction}=1'),
 'The two choices agree for these numbers but need not always agree. These are supplied model outputs, not a derivation of how their training produced them.',
 'Bagging can reduce variability when models make usefully different errors; it does not guarantee an improvement on every dataset.']),
P('Augmentation: split originals before creating variants','A conceptual companion to lecture page162.',[
 {'image':'augmentation.png','width':680},
 'Keep variants of the same original within its assigned partition. Transform training examples only in ways that preserve the target meaning; a digit rotation can change its label.']),
P('Count items, not independent originals','Suppose100 training originals each produce two additional variants.',[
 E(r'100\ \mathrm{originals}+2(100)\ \mathrm{variants}=300\ \mathrm{training\ items}'),
 'These are300 presented items, not300 independently collected examples. Sibling variants share information; the independent-sample variance formulas cannot be applied merely by counting files.',
 'Split original examples into training, validation and test groups before producing related variants. Otherwise an original can be in training while a near-copy appears in evaluation.',
 'Check whether a chosen transformation preserves the label for this task. A valid transformation for one image class may be invalid for another.']),
P('Your turn: equality and an unobserved future value','Use the same strict-improvement rule with patience2.',[
 E(r'\mathrm{listed\ validation\ values}=(0.4,0.35,0.35,0.36,0.30)'),
 'Trace the best loss, checkpoint and consecutive-failure counter. When does the run stop, which checkpoint is restored, and is the fifth value actually observed under this rule?',
 'Count runs for a4-by-3 configuration grid with two seeds per configuration. For bagging votes[0,1,0], state the majority.',
 'If40 training originals each have three additional label-preserving variants, how many items are presented? When must the split occur?'],'INDEPENDENT PRACTICE'),
P('Answer: equality does not reset patience','The observed run ends after the fourth epoch.',[
 {'table':[['epoch','validation','best / checkpoint','counter'],['1','.40','.40 / epoch 1','0'],['2','.35','.35 / epoch 2','0'],['3','.35','.35 / epoch 2','1'],['4','.36','.35 / epoch 2','2: stop']],'widths':[100,140,290,140]},E(r'0.35=0.35\quad\Longrightarrow\quad\mathrm{no\ strict\ improvement}'),E(r'\mathrm{stop}=4,\qquad\mathrm{restore}=2'),
 'The listed fifth value .30 is hypothetical for this stopped run: it would not have been observed. Using it to justify continuing changes the stated procedure.'],'WORKED ANSWER'),
P('Answer: configurations, votes and variants','Keep configuration count, run count and independent-data count distinct.',[
 E(r'4\times3=12\ \mathrm{configurations};\quad12\times2=24\ \mathrm{runs}'),E(r'\mathrm{votes}\ (0,1,0)\Longrightarrow\mathrm{majority}=0'),E(r'40+3(40)=160\ \mathrm{training\ items}'),
 'Split the original dataset first; the resulting training partition contains these 40 originals. Then add three variants per training original. The 160 items are not 160 independent originals.',
 'Common errors: restoring the last checkpoint instead of the best, treating equality as improvement, ignoring a counter reset, looking ahead past stopping, tuning on test data, or leaking augmented siblings across partitions.'],'WORKED ANSWER')]
fig,ax=plt.subplots(figsize=(9.5,3),layout='constrained');ax.plot(range(1,7),train,'o-',label='training');ax.plot(range(1,7),val,'o-',label='validation');ax.axvline(4,color='#147d92',ls='--',label='restore epoch 4');ax.axvline(6,color='#c86c28',ls=':',label='stop after epoch 6');ax.set(xlabel='epoch',ylabel='loss',xticks=range(1,7),ylim=(.2,.7));ax.legend(fontsize=9);ax.grid(alpha=.2);fig.savefig(out/'history.png',dpi=180);plt.close(fig)
def diagram(file,boxes,edges):
 fig,ax=plt.subplots(figsize=(10,3.1),layout='constrained');ax.set(xlim=(0,10),ylim=(0,3));ax.axis('off')
 for x,y,t in boxes:ax.text(x,y,t,ha='center',va='center',fontsize=10,bbox=dict(boxstyle='round,pad=.35',fc='#eaf3f7',ec='#147d92'))
 for a,b in edges:ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='->',color='#147d92',lw=1.7))
 fig.savefig(out/file,dpi=180);plt.close(fig)
diagram('bagging.png',[(1,1.5,'training IDs\n[A,B,C,D]'),(3.5,2.5,'[A,A,C,D]'),(3.5,1.5,'[B,C,C,D]'),(3.5,.5,'[A,B,D,D]'),(6.2,2.5,'model 1'),(6.2,1.5,'model 2'),(6.2,.5,'model 3'),(9,1.5,'new example\ncombined prediction')],[((1.9,1.7),(2.6,2.4)),((1.9,1.5),(2.6,1.5)),((1.9,1.3),(2.6,.6)),((4.4,2.5),(5.6,2.5)),((4.4,1.5),(5.6,1.5)),((4.4,.5),(5.6,.5)),((6.8,2.5),(8,1.8)),((6.8,1.5),(8,1.5)),((6.8,.5),(8,1.2))])
diagram('augmentation.png',[(1,1.5,'original\nexamples'),(3.5,2.5,'training originals'),(3.5,1.5,'validation originals'),(3.5,.5,'test originals'),(7.5,2.5,'original + valid variants\nused for training'),(7.5,1.5,'validation selection'),(7.5,.5,'final evaluation')],[((1.8,1.7),(2.3,2.4)),((1.8,1.5),(2.3,1.5)),((1.8,1.3),(2.3,.6)),((4.8,2.5),(5.8,2.5)),((4.8,1.5),(6.1,1.5)),((4.8,.5),(6.2,.5))])
assert main[-1]['epoch']==6 and main[-1]['checkpoint']==4
assert fresh[-1]['epoch']==4 and fresh[-1]['checkpoint']==2
(out/'checks.json').write_text(json.dumps(dict(main=main,fresh=fresh,main_configurations=12,main_runs=36,practice_runs=24),indent=2))
spec=dict(number=38,title='Early stopping, selection, bagging and augmentation',description='Trace every checkpoint and patience decision, restore the correct model, count experimental runs, and distinguish training-data bagging from augmentation.',source_short='Lecture 5 PDF p.145,160,162,164 / explicit strict-improvement stopping rule',source='Lecture 5 pages145-149 bagging,160 early stopping,162 augmentation,164 setup. numerical-practice.md N6.11. Patience2 and min_delta0 are chosen exercise rules, not supplied pseudocode.',pages=pages)
for p in pages:
 for key in ['title','subtitle']:
  for a,b in [('page160','page 160'),('pages145','pages 145'),('page162','page 162'),('checkpoint4','checkpoint 4'),('Suppose100','Suppose 100'),('patience2','patience 2')]:p[key]=p[key].replace(a,b)
 for i,b in enumerate(p['blocks']):
  if isinstance(b,str):
   for a,z in [('reach2','reach 2'),('Epoch1','Epoch 1'),('reaches2','reaches 2'),('epoch6','epoch 6'),('epoch4','epoch 4'),('are300','are 300'),('not300','not 300'),('a4-by-3','a 4-by-3'),('votes[','votes ['),('If40','If 40'),('the40','the 40'),('The160','The 160'),('not160','not 160')]:b=b.replace(a,z)
   p['blocks'][i]=b
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
