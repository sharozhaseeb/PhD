from pathlib import Path
import json,copy
from network_math import original,check_backward,check_forward,forward_scalar
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'20-complete-batch-update';out.mkdir(exist_ok=True)
net=original();A=check_backward([1,2],1);B=check_backward([-1,1],0)
def E(s):return {'eq':s.replace('-0.0000000000','0.0000000000').replace('-0.00000000','0.00000000'),'size':20}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
def indices():
 for l,W in enumerate(net['weights']):
  for j in range(len(W[0])):
   for i in range(len(W)):yield 'weights',l,i,j
   yield 'biases',l,None,j
def val(n,k,l,i,j):return n[k][l][j] if i is None else n[k][l][i][j]
def put(n,k,l,i,j,v):
 if i is None:n[k][l][j]=v
 else:n[k][l][i][j]=v
def label(k,l,i,j):return rf'b_{{{j+1}}}^{{({l+1})}}' if i is None else rf'w_{{{i+1},{j+1}}}^{{({l+1})}}'
records=[];updated={}
for k,l,i,j in indices():
 a=val(A,k,l,i,j);b=val(B,k,l,i,j);g=(a+b)/2
 plus=copy.deepcopy(net);minus=copy.deepcopy(net);v=val(net,k,l,i,j);h=1e-6
 put(plus,k,l,i,j,v+h);put(minus,k,l,i,j,v-h)
 def risk(n):return (forward_scalar([1,2],1,n)['loss']+forward_scalar([-1,1],0,n)['loss'])/2
 fd=(risk(plus)-risk(minus))/(2*h);assert abs(fd-g)<1e-8
 records.append(dict(kind=k,l=l,i=i,j=j,a=a,b=b,g=g,old=v,fd=fd))
for eta in [.1,.2]:
 n=copy.deepcopy(net)
 for r in records:put(n,r['kind'],r['l'],r['i'],r['j'],r['old']-eta*r['g'])
 ca=check_forward([1,2],1,n);cb=check_forward([-1,1],0,n)
 updated[str(eta)]=dict(net=n,A=ca,B=cb,J=(ca['loss']+cb['loss'])/2)
pages=[P('One batch means one common starting state','Continue the same 2-to-2-to-2-to-1 sigmoid network from Lessons16-19.',[
 E(r'A:\ x=(1,2),\ t=1;\qquad B:\ x=(-1,1),\ t=0'),
 E(r'J=\frac{\ell_A+\ell_B}{2},\qquad\eta=0.1'),
 {'table':[['layer','weight rows (source to destination)','bias vector'],['1','(0.1, -0.2); (0.3, 0.2)','(0, 0.1)'],['2','(0.4, -0.3); (-0.2, 0.2)','(0.1, -0.1)'],['3','(0.3); (-0.4)','(0.2)']],'widths':[65,425,200]},
 'These are the original study parameters. Calculate both examples here, average their gradients, and only then change any parameter. All fifteen parameters, including biases, will be updated.',
 'Writing the updates one at a time is fine: simultaneous means every gradient came from this same original state.']),
 P('Per-example loss first; mean loss second','A subscript A or B identifies an example, not a neuron.',[
 E(r'\ell_n=-[t_n\ln y_n+(1-t_n)\ln(1-y_n)]'),
 E(r'\delta_n^{(3)}=\frac{\partial\ell_n}{\partial z_n^{(3)}}=y_n-t_n'),
 E(r'\frac{\partial J}{\partial\theta}=\frac{1}{2}\left(\frac{\partial\ell_A}{\partial\theta}+\frac{\partial\ell_B}{\partial\theta}\right)'),
 'Theta here means any one weight or bias. The delta is a derivative of one example loss, so it does not contain the factor 1/2. Average each parameter gradient exactly once.',
 'The assignment writes a mean objective and the y minus target shortcut. We make the per-example meaning explicit before averaging. If you instead define a delta from J, its factor 1/2 is already included.']),
 P('Original forward values and starting cost','Lesson17 shows all five neuron calculations for both inputs.',[
 {'table':[['quantity','A','B'],['hidden1 y','0.6681877722, 0.5744425168','0.5498339973, 0.6224593312'],['hidden2 y','0.5627638384, 0.4537407133','0.5487054962, 0.4649430331'],['output y',f'{A["cache"]["y"][-1][0]:.10f}',f'{B["cache"]["y"][-1][0]:.10f}'],['BCE loss',f'{A["cache"]["loss"]:.10f}',f'{B["cache"]["loss"]:.10f}']],'widths':[120,285,285],'size':12},
 E(rf'J_{{old}}=\frac{{{A["cache"]["loss"]:.10f}+{B["cache"]["loss"]:.10f}}}{{2}}={risk(net):.10f}'),
 'A gradients were derived in Lessons18-19. Now derive B at the same state. Displayed decimals are approximate; retain full precision in your calculator.'])]
pages.append(P('B: start backward at the output','The target is zero, so the output delta is positive.',[
 E(rf'\delta_B^{{(3)}}={B["cache"]["y"][-1][0]:.10f}-0={B["deltas"][-1][0]:.10f}'),
 'For each hidden neuron, sum every outgoing weight times its destination delta. Then multiply by its local sigmoid slope y(1-y).',
 E(r'\delta_j^{(l)}=\left(\sum_k w_{j,k}^{(l+1)}\delta_k^{(l+1)}\right)y_j^{(l)}(1-y_j^{(l)})'),
 'Use B activations with B deltas. An A activation paired with a B delta would not be the gradient of either example.']))
for l in [1,0]:
 for j in [0,1]:
  paths=B['paths'][l][j];a=B['cache']['y'][l+1][j];up=sum(paths)
  terms='+'.join(rf'({net["weights"][l+1][j][k]:g})({B["deltas"][l+1][k]:.10f})' for k in range(len(paths)))
  pages.append(P(f'B: hidden layer {l+1}, neuron {j+1} delta','All quantities on this page belong to example B.',[
   E(rf'u={terms}'),
   E(rf'={"+".join(f"({p:.10f})" for p in paths)}={up:.10f}'),
   E(rf'y(1-y)={a:.10f}(1-{a:.10f})={a*(1-a):.10f}'),
   E(rf'\delta_{{B,{j+1}}}^{{({l+1})}}=({up:.10f})({a*(1-a):.10f})={B["deltas"][l][j]:.10f}'),
   'The symbol u is the incoming backward slope from downstream neurons. Add the paths before applying this neuron local slope.']))
for l,W in enumerate(net['weights']):
 for j in range(len(W[0])):
  blocks=[E(r'\mathrm{weight\ gradient}=\mathrm{source\ activation}\times\mathrm{destination\ delta}')]
  for i in range(len(W)):
   q=label('weights',l,i,j);a=B['cache']['y'][l][i];d=B['deltas'][l][j]
   blocks.append(E(rf'\frac{{\partial\ell_B}}{{\partial {q}}}=({a:.10f})({d:.10f})={B["weights"][l][i][j]:.10f}'))
  q=label('biases',l,None,j);d=B['deltas'][l][j]
  blocks.extend([E(rf'\frac{{\partial\ell_B}}{{\partial {q}}}=1({d:.10f})={d:.10f}'),
   'The bias has constant source 1. Here the input -1 reverses the first weight-gradient sign.' if l==0 else 'The bias has constant source 1. Ordinary weight gradients use the previous hidden layer activations shown in the products.'])
  pages.append(P(f'B: layer {l+1}, neuron {j+1} gradients','Two weights and one bias: every incoming parameter is included.',blocks))
def updates(eta,practice=False):
 ps=[];stage='WORKED ANSWER' if practice else 'WORKED EXAMPLE'
 for l,W in enumerate(net['weights']):
  for j in range(len(W[0])):
   blocks=[]
   for r in records:
    if r['l']!=l or r['j']!=j:continue
    q=label(r['kind'],l,r['i'],j);new=r['old']-eta*r['g']
    if not practice:blocks.append(E(rf'g_{{{q}}}=\frac{{({r["a"]:.8f})+({r["b"]:.8f})}}{{2}}={r["g"]:.8f}'))
    blocks.append(E(rf'({q})_{{new}}={r["old"]:g}-{eta:g}({r["g"]:.8f})={new:.8f}'))
   blocks.append('A negative gradient increases its parameter: subtracting a negative adds.')
   ps.append(P(('Practice: ' if practice else '')+f'update layer {l+1}, neuron {j+1}',f'Learning rate {eta:g}; the three incoming parameters are updated separately.',blocks,stage))
 return ps
pages+=updates(.1)
def fresh(eta,practice=False):
 ps=[];n=updated[str(eta)]['net'];stage='WORKED ANSWER' if practice else 'WORKED EXAMPLE'
 for name in ['A','B']:
  c=updated[str(eta)][name]
  for l,W in enumerate(n['weights']):
   blocks=[]
   for j in range(len(W[0])):
    terms='+'.join(rf'({W[i][j]:.6f})({c["y"][l][i]:.6f})' for i in range(len(W)))
    z=c['z'][l][j];a=c['y'][l+1][j]
    blocks.extend([E(rf'z_{{{j+1}}}^{{({l+1})}}={terms}+({n["biases"][l][j]:.6f})'),E(rf'={z:.10f},\qquad y_{{{j+1}}}^{{({l+1})}}=\frac{{1}}{{1+e^{{-({z:.10f})}}}}={a:.10f}')])
   if l==2:
    p=c['y'][-1][0];loss=c['loss'];expr=rf'-\ln({p:.10f})' if name=='A' else rf'-\ln(1-{p:.10f})'
    blocks.append(E(rf'\ell_{{{name},new}}={expr}={loss:.10f}'))
   blocks.append('Recompute from the new parameters and the new previous-layer activations. Reusing an old hidden activation would mix two network states.')
   ps.append(P(('Practice: ' if practice else '')+f'fresh {name}, layer {l+1}',f'All fifteen parameters have now changed using learning rate {eta:g}.',blocks,stage))
 ca=updated[str(eta)]['A'];cb=updated[str(eta)]['B'];J=updated[str(eta)]['J']
 ps.append(P(('Practice: ' if practice else '')+'compare the new batch mean','The training objective is the average over both examples.',[
  E(rf'J_{{new}}=\frac{{{ca["loss"]:.10f}+{cb["loss"]:.10f}}}{{2}}={J:.10f}'),
  E(rf'J_{{new}}-J_{{old}}={J:.10f}-{risk(net):.10f}={J-risk(net):.10f}'),
  'The mean decreases for this chosen step. An individual example loss can increase: gradient descent follows the mean gradient, not a separate best direction for every example.',
  'A decrease here is a numerical check, not a guarantee for every possible learning rate. The calculations retain full precision internally; displayed decimals are rounded.'],stage))
 return ps
pages+=fresh(.1)
from practice_20 import build_practice
pra_pages,pra_checks=build_practice(E,P)
pages+=pra_pages
pages.append(P('Checks that prevent common batch mistakes','All fifteen mean gradients were independently checked by finite differences.',[
 E(r'\mathrm{mean}(a_n\delta_n)\ne\mathrm{mean}(a_n)\,\mathrm{mean}(\delta_n)\quad\mathrm{in\ general}'),
 'Multiply the source activation and destination delta for each example first, then average those parameter gradients. Do not average the activations and deltas separately.',
 'Do not divide by two twice, update after A before evaluating B, forget the biases, or reuse the old forward cache after updating.',
 f'For the main A/B batch, eta 0.1 gives mean {updated["0.1"]["J"]:.10f}. Its A loss increases even though the mean decreases. Judge this training step by the stated mean objective.',
 'Finite differences perturb one original parameter at a time, recompute both example losses, average, and compare the numerical slope with the calculated mean gradient.'],'WORKED ANSWER'))
(out/'checks.json').write_text(json.dumps(dict(A=A,B=B,parameters=records,updates=updated,practice=pra_checks),indent=2))
(out/'parameters.json').write_text(json.dumps(net,indent=2))
spec=dict(number=20,title='A complete two-example batch update',description='Derive both-example gradients, average and update all fifteen parameters, and recompute both full forwards and losses; includes a fresh full-network practice batch.',source_short='Backpropagation handout p.2-3 / Assignment 1 / N3.5 study example',source='Backpropagation_Derivation.pdf pages 2-3; Assignment 1.pdf mean BCE and backpropagation; numerical-practice.md N3.5.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
