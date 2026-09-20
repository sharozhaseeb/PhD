from pathlib import Path
import json,itertools,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'35-dropout';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
theta=np.array([1.,2.,1.,-1.,3.,-2.,.5]);names=['a_1','a_2','c_1','c_2','u_1','u_2','b']
def calc(p,mask,inverted=False):
 a=p[:2];c=p[2:4];u=p[4:6];b=p[6];z=a+c;h=np.maximum(z,0);scale=np.array(mask,dtype=float)/(0.5 if inverted else 1);d=h*scale;y=u@d+b;r=y-1;delta=r*u*scale*(z>0);g=np.r_[delta,delta,r*d,r]
 delta[delta==0]=0;g[g==0]=0
 return dict(z=z.tolist(),h=h.tolist(),scale=scale.tolist(),d=d.tolist(),y=float(y),r=float(r),loss=float(r*r/2),delta=delta.tolist(),g=g.tolist())
main=calc(theta,[1,0]);inv=calc(theta,[1,0],True);practice=calc(theta,[0,1])
pages=[P('Drop hidden activations with a fixed binary mask','The course convention is standard dropout: train with M*h; infer with q*h.',[
 'A mask entry is1 when its hidden unit is kept and0 when dropped. Each entry is an independent Bernoulli draw: it equals1 with keep probability q, called alpha in the lecture.',
 E(r'q=0.5,\quad M=(1,0),\quad x=1,\quad t=1,\quad\eta=0.01'),
 'Only the two hidden activations are eligible for dropout in this exercise. The input, linear output and bias constants are not masked.',
 'Cache the sampled mask for the entire forward/backward pass. A later example or update can receive a new mask under the chosen sampling policy.']),
P('Define all seven trainable parameters','Two ReLU hidden units feed one linear output.',[
 E(r'z_j=a_jx+c_j,\quad h_j=\max(0,z_j),\quad d_j=M_jh_j'),E(r'\widehat y=u_1d_1+u_2d_2+b,\quad L=\frac{1}{2}(\widehat y-t)^2'),E(r'(a_1,a_2,c_1,c_2,u_1,u_2,b)=(1,2,1,-1,3,-2,0.5)'),
 'a1 and a2 are input weights; c1 and c2 are hidden biases; u1 and u2 are output weights; b is the output bias. Count each bias once.',
 'The lecture uses general layer notation. This small network makes its mask and chain-rule equations explicit. There is no additional L2 penalty in this lesson.']),
P('Follow the two hidden paths','The second hidden unit is computed, then its activation is multiplied by zero.',[
 {'image':'network.png','width':680},
 'A dropped path sends zero activation to the output and zero data-loss derivative backward through the mask. Its parameters remain stored; they are not deleted.'])]
def forward(r,label,mask,inverted=False,answer=False):
 stage='WORKED ANSWER' if answer else 'WORKED EXAMPLE'
 pages.append(P(f'{label}: hidden activations','Use the original parameters for this separate pass.',[
 E(r'z_1=1(1)+1=2,\quad z_2=2(1)+(-1)=1'),E(r'h_1=\max(0,2)=2,\quad h_2=\max(0,1)=1'),
 E(rf'M=({mask[0]},{mask[1]}),\quad q=0.5'),
 'Both preactivations are positive, so each ReLU local derivative is1. A zero dropout mask is different from a ReLU being inactive because of a nonpositive preactivation.',
 'This is an inverted-dropout comparison, reset to original parameters; retained activations divide by q during training.' if inverted else 'Standard dropout multiplies the hidden activations by the fixed mask with no training-time division by q.'],stage))
 d=r['d'];scale='/0.5' if inverted else ''
 pages.append(P(f'{label}: mask, output and loss','Use the masked activations in the output weighted sum.',[
 E(rf'd_1={mask[0]}(2){scale}={d[0]:g},\quad d_2={mask[1]}(1){scale}={d[1]:g}'),E(rf'\widehat y=3({d[0]:g})+(-2)({d[1]:g})+0.5={r["y"]:g}'),E(rf'r=\widehat y-t={r["y"]:g}-1={r["r"]:g}'),E(rf'L=\frac{{1}}{{2}}({r["r"]:g})^2={r["loss"]:g}'),
 'The output is linear, so its derivative with respect to the weighted sum is1. The output bias is added once and is not scaled by the hidden mask.'],stage))
def backward(r,label,mask,inverted=False,answer=False):
 stage='WORKED ANSWER' if answer else 'WORKED EXAMPLE';rr=r['r'];g=r['g'];delta=r['delta'];d=r['d'];sc=r['scale']
 pages.append(P(f'{label}: output gradients','Derivative of the half-square with respect to prediction is the residual.',[
 E(r'\frac{\partial L}{\partial\widehat y}=r,\quad\frac{\partial L}{\partial u_j}=r d_j,\quad\frac{\partial L}{\partial b}=r'),E(rf'g_{{u_1}}={rr:g}({d[0]:g})={g[4]:g}'),E(rf'g_{{u_2}}={rr:g}({d[1]:g})={g[5]:g},\quad g_b={rr:g}'),
 'The outgoing weight of a dropped unit has zero data gradient because its source activation d is zero. The output bias can still have a nonzero gradient.'],stage))
 pages.append(P(f'{label}: hidden deltas','Multiply the backward derivative through the same cached mask and the local ReLU slope.',[
 E(r'\delta_j=\frac{\partial L}{\partial z_j}=r u_j\frac{\partial d_j}{\partial h_j}\mathrm{ReLU}^{\prime}(z_j)'),
 E(r'\partial d_j/\partial h_j=M_j/q' if inverted else r'\partial d_j/\partial h_j=M_j'),E(rf'\delta_1={rr:g}(3)({sc[0]:g})(1)={delta[0]:g}'),E(rf'\delta_2={rr:g}(-2)({sc[1]:g})(1)={delta[1]:g}'),
 'Use original output weights3 and-2, not values updated from the preceding gradient calculation. No parameter has been changed during this backward pass.'],stage))
 pages.append(P(f'{label}: input weights and hidden biases','An input weight contributes x; a hidden bias contributes1.',[
 E(r'\frac{\partial L}{\partial a_j}=\delta_jx,\qquad\frac{\partial L}{\partial c_j}=\delta_j'),E(rf'g_{{a_1}}={delta[0]:g}(1)={g[0]:g},\quad g_{{c_1}}={g[2]:g}'),E(rf'g_{{a_2}}={delta[1]:g}(1)={g[1]:g},\quad g_{{c_2}}={g[3]:g}'),
 'A dropped hidden bias has zero data gradient through the masked path. This does not mean that the bias constant itself was directly masked.',
 'These are data-loss gradients. If a separate regularizer penalized a dropped unit\'s weights, it could still contribute nonzero gradients.'],stage))
def updates(r,label,mask,answer=False):
 stage='WORKED ANSWER' if answer else 'WORKED EXAMPLE';g=np.array(r['g']);new=theta-.01*g
 for idxs,part in [([0,1,2,3],'hidden parameters'),([4,5,6],'output parameters')]:
  blocks=[E(rf'({names[j]})_{{new}}={theta[j]:g}-0.01({g[j]:g})={new[j]:g}') for j in idxs]
  blocks.append('All seven new values use the gradients from the original common state. Do not recompute later gradients using already updated parameters.')
  pages.append(P(f'{label}: update {part}','Subtract eta times each gradient; unchanged zero-gradient parameters remain stored.',blocks,stage))
 nr=calc(new,mask)
 pages.append(P(f'{label}: check the updated pass','Diagnostic only: reuse the cached mask to evaluate the same loss function.',[
 E(rf'z^{{new}}=({new[0]:g}+{new[2]:g},\ {new[1]:g}+({new[3]:g}))=({nr["z"][0]:g},{nr["z"][1]:g})'),E(rf'd^{{new}}=({nr["d"][0]:g},{nr["d"][1]:g})'),E(rf'\widehat y^{{new}}={new[4]:g}({nr["d"][0]:g})+({new[5]:g})({nr["d"][1]:g})+{new[6]:g}={nr["y"]:g}'),E(rf'L^{{new}}=\frac{{1}}{{2}}({nr["r"]:g})^2={nr["loss"]:.9f}'),
 'This same-mask diagnostic is not a requirement to reuse this mask forever. Later training examples or updates sample new masks under the declared policy.'],stage))
forward(main,'Main pass',[1,0]);backward(main,'Main pass',[1,0]);updates(main,'Main pass',[1,0])
pages.append(P('Standard-dropout inference: reset original parameters','Use the original h=(2,1), u=(3,-2), b=.5 for this comparison.',[
 E(r'\mathbb{E}[M_jh_j]=q h_j\quad\mathrm{for\ fixed}\ h_j'),E(r'd_{test}=q h=(0.5(2),0.5(1))=(1,0.5)'),E(r'\widehat y_{test}=3(1)+(-2)(0.5)+0.5=2.5'),E(r'\mathrm{equivalently}:\quad(qu)=(1.5,-1)'),E(r'1.5(2)+(-1)(1)+0.5=2.5'),
 'Scale the activations OR their outgoing weights, not both. The next additive output bias stays .5. No random mask is sampled for this standard deterministic inference rule.']))
forward(inv,'Inverted comparison',[1,0],True);backward(inv,'Inverted comparison',[1,0],True)
pages.append(P('Inverted-dropout inference: original parameters','Training uses M*h/q; inference uses the unscaled h.',[
 E(r'\mathbb{E}[M_jh_j/q]=h_j'),E(r'\widehat y_{test}=3(2)+(-2)(1)+0.5=4.5'),
 {'table':[['convention','training activation','inference activation'],['standard','M*h','q*h'],['inverted','M*h/q','h']],'widths':[180,235,265]},
 'The standard result2.5 and inverted result4.5 use the same fixed original parameters under different conventions. They are not two separately trained models whose parameters or outputs must match.',
 'Choose one convention and keep its training, backward and inference scaling consistent.']))
pages.append(P('Enumerate all masks at the original state','Two independent mask entries with q=.5 give four equally likely masks.',[
 {'table':[['M','probability','active units','standard output'],['(0,0)','.25','0','.5'],['(0,1)','.25','1','-1.5'],['(1,0)','.25','1','6.5'],['(1,1)','.25','2','4.5']],'widths':[135,155,175,215]},E(r'\mathbb{E}[\mathrm{active}]=0.25(0+1+1+2)=1'),E(r'\mathbb{E}[\widehat y]=0.25(0.5-1.5+6.5+4.5)=2.5'),
 'The mean output equals standard inference exactly here because the output is linear in the masked, fixed hidden activations. These masks share parameters; four masks do not mean four independently trained models.']))
pages.append(P('Nonlinear output: expectation is only approximated','The lecture page155 uses an approximation for a general network.',[
 E(r'Z=2M,\quad P(M=0)=P(M=1)=0.5'),E(r'\mathbb{E}[\sigma(Z)]=0.5\sigma(0)+0.5\sigma(2)'),E(r'=0.5(0.5)+0.5(0.880797)\approx0.690399'),E(r'\mathbb{E}[Z]=0.5(0)+0.5(2)=1'),E(r'\sigma(\mathbb{E}[Z])=\sigma(1)\approx0.731059'),
 'A function of the mean is not generally the mean of the function. Replacing random activations by their expectations is not an exact ensemble-output identity for arbitrary nonlinear networks.']))
pages.append(P('Your turn: keep the other hidden unit','Reset to the original seven parameters; use standard dropout.',[
 E(r'M=(0,1),\quad q=0.5,\quad x=1,\quad t=1,\quad\eta=0.01'),
 'Compute the hidden activations, masked values, prediction, loss, all seven gradients and all seven simultaneous updates. Recompute the loss with the same mask as a diagnostic.',
 'Separately, consider three independently masked eligible units with keep probability .8. Find the number of possible masks, expected active count and probability of the particular ordered mask(1,1,0).'],'INDEPENDENT PRACTICE'))
forward(practice,'Practice',[0,1],answer=True);backward(practice,'Practice',[0,1],answer=True);updates(practice,'Practice',[0,1],answer=True)
pages.append(P('Answer: mask count and probability','Independent entries can each be kept or dropped.',[
 E(r'\mathrm{possible\ masks}=2^3=8'),E(r'\mathbb{E}[\mathrm{active}]=0.8+0.8+0.8=2.4'),E(r'P(M=(1,1,0))=0.8(0.8)(1-0.8)=0.128'),
 'The expected count2.4 is an average across masks; each actual count is an integer. The eight masks are not equally probable because q is not .5.',
 'There is no combinatorial factor for one specified ordered mask. If asked for any mask with exactly two active units, three different masks qualify, so that probability would be3(.128)=.384.',
 'Before an exam calculation, name the dropout convention, cache the mask, keep original weights during backpropagation and scale only eligible activations.'],'WORKED ANSWER'))
fig,ax=plt.subplots(figsize=(10,3),layout='constrained');ax.set(xlim=(0,10),ylim=(0,3));ax.axis('off')
for x,y,txt,col in [(1,1.5,'x=1','#147d92'),(3.5,2.3,'h1=ReLU(a1*x+c1)\n=2','#147d92'),(3.5,.6,'h2=ReLU(a2*x+c2)\n=1','#777777'),(6.5,2.3,'M1=1\nd1=2','#147d92'),(6.5,.6,'M2=0\nd2=0','#777777'),(9,1.5,'linear output\nu1*d1+u2*d2+b','#147d92')]:
 ax.text(x,y,txt,ha='center',va='center',fontsize=10,bbox=dict(boxstyle='round,pad=.35',fc='#eef5f7',ec=col))
for a,b,c in [((1.4,1.7),(2.2,2.2),'#147d92'),((1.4,1.3),(2.2,.7),'#777777'),((4.8,2.3),(5.9,2.3),'#147d92'),((4.8,.6),(5.9,.6),'#777777'),((7.1,2.2),(8,1.8),'#147d92'),((7.1,.7),(8,1.2),'#777777')]:ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='->',color=c,lw=2))
fig.savefig(out/'network.png',dpi=180);plt.close(fig)
checks=[]
for mask,inverted in [([1,0],False),([1,0],True),([0,1],False)]:
 r=calc(theta,mask,inverted);h=1e-6;fd=[]
 for j in range(7):
  v=np.eye(7)[j]*h;fd.append((calc(theta+v,mask,inverted)['loss']-calc(theta-v,mask,inverted)['loss'])/(2*h))
 assert np.max(np.abs(np.array(fd)-r['g']))<1e-7
 checks.append(dict(mask=mask,inverted=inverted,trace=r,finite_differences=fd,updated=(theta-.01*np.array(r['g'])).tolist()))
assert abs(calc(theta-.01*np.array(main['g']),[1,0])['loss']-9.122001845)<1e-10
assert abs(calc(theta-.01*np.array(practice['g']),[0,1])['loss']-2.536878125)<1e-10
(out/'checks.json').write_text(json.dumps(checks,indent=2))
spec=dict(number=35,title='Dropout: full masked forward and backward passes',description='Trace all seven parameter gradients and updates under a fixed mask, compare standard/inverted scaling and inference, enumerate masks, and solve the opposite-mask practice.',source_short='Lecture 5 PDF p.153-156 / declared hidden-only mask; fixed mask for derivatives',source='Lecture 5 pages144-158; forward153, backward154, expectation approximation155, inference scaling156. numerical-practice.md N6.8 seven-parameter study network. Inverted dropout is a labeled comparison.',pages=pages)
# Keep natural-language number spacing readable without touching math blocks.
for page in pages:
 for key in ['title','subtitle']:
  page[key]=page[key].replace('page155','page 155').replace('result2.5','result 2.5').replace('result4.5','result 4.5').replace('contributes1','contributes 1')
 for i,b in enumerate(page['blocks']):
  if isinstance(b,str):
   for old,new in [('is1','is 1'),('and0','and 0'),('equals1','equals 1'),('derivative is1','derivative is 1'),('contributes1','contributes 1'),('weights3 and-2','weights 3 and -2'),('result2.5','result 2.5'),('result4.5','result 4.5'),('count2.4','count 2.4'),('be3','be 3'),('mask(1','mask (1')]:b=b.replace(old,new)
   page['blocks'][i]=b
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
