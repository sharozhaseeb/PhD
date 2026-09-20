from pathlib import Path
from fractions import Fraction as F
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'31-momentum-changing-batches';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
def trace(groups,nesterov):
 w=v=F(0);rs=[]
 for ts in groups:
  q=w+F(1,2)*v if nesterov else w
  gs=[q-F(t) for t in ts];g=sum(gs)/len(gs);nv=F(1,2)*v-F(1,10)*g;nw=w+nv
  rs.append(dict(targets=ts,w=float(w),v=float(v),q=float(q),gs=list(map(float,gs)),g=float(g),nv=float(nv),nw=float(nw)));w,v=nw,nv
 return rs
main={name:trace([[1,3],[-3,-1],[1,3]],nest) for name,nest in [('Momentum',False),('Nesterov',True)]}
practice={name:trace([[0,2],[2,4]],nest) for name,nest in [('Momentum',False),('Nesterov',True)]}
pages=[P('Keep memory when the mini-batch changes','Chosen small batches make the stored optimizer state visible.',[
 E(r'\widehat y=w,\quad\ell(w;t)=\frac{1}{2}(w-t)^2,\quad\frac{d\ell}{dw}=w-t'),
 E(r'A=(1,3),\quad B=(-3,-1),\quad w_0=0,\quad v_0=0'),
 E(r'\eta=0.1,\qquad\beta=0.5'),
 'w is the current parameter. v is the previous signed displacement: positive means the last update increased w. Beta retains half of that displacement.',
 'Process A then B in epoch1, followed by A in epoch2. This explicitly fixed order supports hand calculations; lecture algorithms shuffle the data.']),
P('Derive each batch gradient before updating','Average the two example gradients at one common evaluation point.',[
 E(r'g_A(w)=\frac{(w-1)+(w-3)}{2}=\frac{2w-4}{2}=w-2'),
 E(r'g_B(w)=\frac{(w+3)+(w+1)}{2}=\frac{2w+4}{2}=w+2'),
 'A pulls toward its target mean2; B pulls toward its target mean-2. The loss changes with the selected batch, even though the model and optimizer settings stay fixed.',
 'Reset the temporary sum of example gradients at the start of each batch. Divide by its actual size2 once. Do not reset w or v.']),
P('Map the lecture equations to our state','Lecture5 pages103,106 and109; v is the slide displacement Delta W.',[
 E(r'\mathrm{Momentum}:\quad v_{new}=\beta v-\eta g_B(w),\quad w_{new}=w+v_{new}'),
 E(r'\mathrm{Nesterov}:\quad q=w+\beta v,\quad v_{new}=\beta v-\eta g_B(q)'),
 E(r'w_{new}=w+v_{new}=q-\eta g_B(q)'),
 'Here B means whichever batch is current. The lookahead q is temporary; every example of that batch uses this same q. It is not an extra stored training update.',
 'The slide first moves in place to q, then applies the correction. Our saved-old-w form is algebraically identical. Do not add beta*v twice or insert an extra (1-beta) factor.'])]
def worked(r,name,label,nest=False,answer=False):
 stage='WORKED ANSWER' if answer else 'WORKED EXAMPLE';q=r['q'];w=r['w'];v=r['v'];ts=r['targets'];gs=r['gs']
 blocks=[E(rf'w={w:g},\quad v={v:g},\quad\mathrm{{targets}}=({ts[0]},{ts[1]})')]
 if nest:blocks.append(E(rf'q={w:g}+0.5({v:g})={q:g}'))
 else:blocks.append('Both methods use w here: the initial displacement is zero, so Nesterov also has q=w+0.5(0)=w.' if name=='Both methods' else 'Ordinary momentum evaluates this batch at the stored w, before adding the retained displacement.')
 blocks += [E(rf'g_1={q:g}-({ts[0]})={gs[0]:g},\quad g_2={q:g}-({ts[1]})={gs[1]:g}'),E(rf'g=\frac{{({gs[0]:g})+({gs[1]:g})}}{{2}}={r["g"]:g}'),'Both example gradients use the same evaluation point. Their average is the gradient supplied to this one optimizer update.']
 pages.append(P(f'{name}: {label} gradient','Carry the parameter and displacement shown below into this batch.',blocks,stage))
 pages.append(P(f'{name}: {label} update','Form a new displacement, then add it to the saved old parameter.',[
 E(r'v_{new}=\beta v-\eta g'),E(rf'v_{{new}}=0.5({v:g})-0.1({r["g"]:g})={r["nv"]:g}'),
 E(rf'w_{{new}}={w:g}+({r["nv"]:g})={r["nw"]:g}'),
 E(rf'(w,v)\ \mathrm{{to\ retain}}=({r["nw"]:g},{r["nv"]:g})'),
 'For Nesterov this is also q minus the gradient correction. Save both new values; discard the temporary gradient sum and temporary lookahead.' if nest else 'Save both new values for the next batch. Only the temporary gradient sum is discarded.'],stage))
worked(main['Momentum'][0],'Both methods','first A')
worked(main['Momentum'][1],'Momentum','B')
worked(main['Nesterov'][1],'Nesterov','B',True)
pages.append(P('Continue into a new epoch without resetting state','Each method carries its own state from B into the next A.',[
 E(r'\mathrm{Momentum}:\quad(w,v)=(0.08,-0.12)'),E(r'\mathrm{Nesterov}:\quad(w,v)=(0.07,-0.13)'),
 'An epoch boundary is a data-pass boundary. It does not restart optimizer memory. The next two calculations continue these states; they are not new comparisons from zero.',
 'A new batch starts with a fresh gradient accumulator. A new training run initializes w and v once. Confusing these two resets changes the algorithm.']))
worked(main['Momentum'][2],'Momentum','next-epoch A')
worked(main['Nesterov'][2],'Nesterov','next-epoch A',True)
pages.append(P('Persistent state versus temporary batch quantities','Keep the saved state across batches and across epochs.',[
 {'image':'state-flow.png','width':680},
 'The flow applies to each batch. Momentum uses q=w; Nesterov uses q=w+beta*v. There is one final stored parameter update per batch.']))
pages.append(P('Read the three-batch traces together','Each row starts from the preceding row of the same method.',[
 {'table':[['method / batch','gradient point','mean gradient','new v','new w']]+[[f'{n} / {lab}',f'{r["q"]:g}',f'{r["g"]:g}',f'{r["nv"]:g}',f'{r["nw"]:g}'] for n,rs in main.items() for lab,r in zip(['A','B','A again'],rs)],'widths':[205,135,150,95,95],'size':13},
 'After B, negative displacement is retained. On the next A, the new batch gradient reverses the update again. Momentum smooths changing directions; it does not eliminate every reversal or guarantee a better loss.']))
pages.append(P('Your turn: change both mini-batches','Start a fresh run for each method; retain eta=.1 and beta=.5.',[
 E(r'A=(0,2),\quad B=(2,4),\quad w_0=v_0=0'),
 'Calculate A then B using ordinary momentum, then repeat from the same initial state using Nesterov. Show both example gradients, their average, each displacement and each parameter.',
 'For Nesterov, explicitly calculate the common lookahead before both B gradients. Compare the correct B update with the mistaken procedure that resets v to zero just before B.'],'INDEPENDENT PRACTICE'))
worked(practice['Momentum'][0],'Both methods','practice A',answer=True)
worked(practice['Momentum'][1],'Momentum','practice B',answer=True)
worked(practice['Nesterov'][1],'Nesterov','practice B',True,True)
pages.append(P('Answer: why resetting memory gives a different result','This comparison concerns the fresh practice batches, not the main example.',[
 E(r'w_{Momentum}=0.44,\qquad w_{Nesterov}=0.435'),
 E(r'\mathrm{wrong\ reset}:\quad w=0.1,\quad v=0\quad\Longrightarrow q=0.1'),
 E(r'g_B(0.1)=\frac{(0.1-2)+(0.1-4)}{2}=-2.9'),
 E(r'v_{new}=0.5(0)-0.1(-2.9)=0.29'),
 E(r'w_{new}=0.1+0.29=0.39'),
 'Both mistaken reset procedures give .39 here. The missing old displacement also removes the Nesterov lookahead shift. Keep optimizer memory; reset only batch-local accumulators.'],'WORKED ANSWER'))
fig,ax=plt.subplots(figsize=(10,3),layout='constrained');ax.set(xlim=(0,10),ylim=(0,3));ax.axis('off')
for x,y,t in [(1.2,2,'Saved w, v'),(5,2,'Current batch\nnew gradient sum = 0'),(8.8,2,'Evaluate all gradients\nat common q'),(8.8,.6,'Average; form v_new'),(3.3,.6,'Save w_new, v_new\ncarry to next batch')]:
 ax.text(x,y,t,ha='center',va='center',fontsize=11,bbox=dict(boxstyle='round,pad=.5',fc='#eaf3f7',ec='#147d92'))
for a,b in [((2.1,2),(3.3,2)),((6.5,2),(7.3,2)),((8.8,1.5),(8.8,1)),((7.2,.6),(5.2,.6)),((1.7,.6),(1.2,1.6))]:ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='->',color='#147d92',lw=2))
fig.savefig(out/'state-flow.png',dpi=180);plt.close(fig)
assert main['Momentum'][-1]['nw']==.212 and main['Nesterov'][-1]['nw']==.2045
assert practice['Momentum'][-1]['nw']==.44 and practice['Nesterov'][-1]['nw']==.435
(out/'checks.json').write_text(json.dumps(dict(main=main,practice=practice,arithmetic='Exact Fraction recurrence, converted to float only for display'),indent=2))
spec=dict(number=31,title='Momentum across changing mini-batches',description='Trace batch gradients and persistent displacement through different data groups and an epoch boundary, with a fresh fully worked practice run.',source_short='Lecture 5 PDF p.103,106,109 / signed displacement convention',source='Lecture 5 PDF pages93-109, specifically103,106,109. Chosen fixed-order numerical-practice.md N6.4 example with an added next-epoch continuation.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
