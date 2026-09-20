from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from network_math import original,check_backward
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'19-hidden-layer-backpropagation';out.mkdir(exist_ok=True)
net=original();A=check_backward([1,2],1);C=check_backward([1,2],0)
def E(s):return {'eq':s,'size':21}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('Continue backward from the output delta','Keep the original weights and the Lesson17 forward cache.',[
E(r'x=(1,2),\quad t=1,\quad\delta_1^{(3)}=-0.4533032667'),
E(r'y^{(1)}=(0.6681877722,0.5744425168)'),
E(r'y^{(2)}=(0.5627638384,0.4537407133)'),
E(r'W^{(2)}\ \mathrm{rows}:\ (0.4,-0.3),\ (-0.2,0.2)'),
E(r'W^{(3)}\ \mathrm{rows}:\ (0.3),\ (-0.4)'),
'The goal is four hidden deltas and all twelve hidden-layer parameter gradients. The three output gradients were calculated in Lesson18.',
'Each delta is the derivative of this one example loss with respect to one neuron preactivation. No batch averaging or parameter update happens here.']),
P('Sum downstream paths, then apply the local slope','Handout page 3, sections 5.3-6: every outgoing connection is a dependency.',[
E(r'\delta_j^{(l)}=\left(\sum_k w_{j,k}^{(l+1)}\delta_k^{(l+1)}\right)y_j^{(l)}(1-y_j^{(l)})'),
'The incoming backward derivative is also called the upstream gradient; it comes from downstream neurons in the forward graph. For each next-layer neuron k, multiply its delta by the connecting weight. Add all these path contributions, then multiply by the current neuron sigmoid slope.',
E(r'\frac{\partial\ell}{\partial w_{i,j}^{(l)}}=y_i^{(l-1)}\delta_j^{(l)},\quad\frac{\partial\ell}{\partial b_j^{(l)}}=\delta_j^{(l)}'),
'A hidden neuron has no direct target label. Do not use hidden activation minus target as its delta. The y-t shortcut was specific to the output sigmoid plus BCE.',
'Use original connecting weights. Updating the output weights before computing hidden deltas would mix two different parameter states.'])]
def hidden_pages(r,practice=False):
 ps=[];cache=r['cache'];stage='WORKED ANSWER' if practice else 'WORKED EXAMPLE';prefix='Practice: ' if practice else ''
 for l in [2,1]:
  for j in [0,1]:
   a=cache['y'][l][j];slope=a*(1-a);paths=r['paths'][l-1][j];up=sum(paths);delta=r['deltas'][l-1][j]
   terms='+'.join(rf'({net["weights"][l][j][k]:g})({r["deltas"][l][k]:.10f})' for k in range(len(paths)))
   pieces='+'.join(rf'({p:.10f})' for p in paths)
   blocks=[E(rf'\mathrm{{upstream\ sum}}={terms}'),E(rf'\approx {pieces}={up:.10f}'),
    E(rf'\mathrm{{local\ slope}}={a:.10f}(1-{a:.10f})\approx{slope:.10f}'),
    E(rf'\delta_{{{j+1}}}^{{({l})}}\approx({up:.10f})({slope:.10f})={delta:.10f}'),
    'Both path contributions are included before applying the local slope.' if l==1 else 'There is only one next-layer output neuron, so this upstream sum has just one term.',
    'This delta belongs to the destination neuron. All incoming parameter gradients for that neuron reuse it.']
   ps.append(P(prefix+f'Hidden layer {l}, neuron {j+1}: delta','Multiply each downstream delta by its original connecting weight.',blocks,stage))
  for j in [0,1]:
   delta=r['deltas'][l-1][j];src=cache['y'][l-1]
   blocks=[E(rf'\frac{{\partial\ell}}{{\partial w_{{i,{j+1}}}^{{({l})}}}}=y_i^{{({l-1})}}\delta_{{{j+1}}}^{{({l})}}')]
   for i in [0,1]:blocks.append(E(rf'\frac{{\partial\ell}}{{\partial w_{{{i+1},{j+1}}}^{{({l})}}}}\approx({src[i]:.10f})({delta:.10f})={r["weights"][l-1][i][j]:.10f}'))
   blocks+=[E(rf'\frac{{\partial\ell}}{{\partial b_{{{j+1}}}^{{({l})}}}}=1\delta_{{{j+1}}}^{{({l})}}\approx{delta:.10f}'),
    'Two ordinary incoming weights use two different source activations. The one bias uses constant source 1.',
    'For layer 1 the source activations are the measured inputs x1 = 1 and x2 = 2.' if l==1 else 'For layer 2 the sources are hidden-layer-1 activations, not the original inputs.']
   ps.append(P(prefix+f'Layer {l}, neuron {j+1}: three gradients','Formula, substitution and value for both incoming weights and the bias.',blocks,stage))
 return ps
pages+=hidden_pages(A)
pages+=[P('Why the first hidden neuron needs both paths','The diagram isolates its two outgoing connections to hidden layer 2.',[
{'image':'branch.png','width':660},
E(r'0.4\delta_1^{(2)}+(-0.3)\delta_2^{(2)}=-0.0268675083'),
'The two next-layer neurons both depend on this first-hidden activation. The chain rule adds the effects through both branches, even when a connecting weight is negative.']),
P('Checkpoint: every hidden parameter is covered','All values are derivatives of the same one-example loss at the same original state.',[
{'table':[['parameter','layer1 gradient','layer2 gradient'],['w1,1',f'{A["weights"][0][0][0]:.10f}',f'{A["weights"][1][0][0]:.10f}'],['w1,2',f'{A["weights"][0][0][1]:.10f}',f'{A["weights"][1][0][1]:.10f}'],['w2,1',f'{A["weights"][0][1][0]:.10f}',f'{A["weights"][1][1][0]:.10f}'],['w2,2',f'{A["weights"][0][1][1]:.10f}',f'{A["weights"][1][1][1]:.10f}'],['b1',f'{A["biases"][0][0]:.10f}',f'{A["biases"][1][0]:.10f}'],['b2',f'{A["biases"][0][1]:.10f}',f'{A["biases"][1][1]:.10f}']],'widths':[180,240,240]},
'The twelve hidden gradients plus three output gradients cover all fifteen trainable parameters. Independent finite-difference checks of all fifteen agree.']),
P('Your turn: propagate the target-flip delta','Use the original input (1,2), original parameters, but target t = 0.',[
E(r'\delta_1^{(3)}=+0.5466967333'),
'The forward cache is unchanged, as shown in Lesson18. Recalculate both layer-2 deltas, both layer-1 deltas, and all twelve hidden-parameter gradients.',
'Write the separate downstream contributions at layer 1 before adding them. Then apply each neuron local sigmoid slope.',
'Explain why hidden deltas are not hidden y minus target, and why you cannot update an output weight before this calculation.'],'INDEPENDENT PRACTICE')]
pages+=hidden_pages(C,True)
pages+=[P('Practice check: what changed and what did not?','The known target changed the output delta; all forward values stayed fixed.',[
E(r'\delta^{(2)}\approx(0.0403561744,-0.0542017181)'),
E(r'\delta^{(1)}\approx(0.0071841589,-0.0046230925)'),
'All twelve hidden gradients were recalculated on the preceding pages. Their signs reverse relative to target 1 because the output delta changes sign and all other factors stay fixed.',
'Here every gradient is multiplied by the same ratio of new to old output delta. That is a check for this fixed-input, fixed-parameter, single-output example; it does not replace the chain-rule working.',
'Common mistakes: dropping a downstream path, using an incoming instead of outgoing weight in the delta, using a preactivation as a source, or changing weights before all gradients are ready.'],'WORKED ANSWER')]
fig,ax=plt.subplots(figsize=(10,2.7),layout='constrained');ax.axis('off');ax.set(xlim=(-.3,3.6),ylim=(-1,1))
ax.text(0,0,'layer1 / 1',ha='center',bbox=dict(boxstyle='round',facecolor='#dcefeb'),fontsize=12)
for yy,label,weight in [(.55,'layer2 / 1\ndelta = -0.033462','0.4'),(-.55,'layer2 / 2\ndelta = +0.044942','-0.3')]:
 ax.text(2.8,yy,label,ha='center',va='center',fontsize=12,bbox=dict(boxstyle='round',facecolor='#edf3f7'));ax.annotate('',xy=(2.3,yy),xytext=(.5,0),arrowprops=dict(arrowstyle='->',color='#006E73',lw=2));ax.text(1.4,yy*.6,weight,fontsize=14,bbox=dict(facecolor='white',edgecolor='none',pad=2))
ax.text(0,-.7,'sum both weighted\ndownstream deltas',ha='center',fontsize=10)
fig.savefig(out/'branch.png',dpi=180);plt.close(fig)
(out/'checks.json').write_text(json.dumps(dict(A=A,practice=C),indent=2));(out/'parameters.json').write_text(json.dumps(net,indent=2))
spec=dict(number=19,title='Hidden-layer backpropagation',description='Calculate every hidden delta and all twelve hidden gradients, including every branching path and a full target-flip practice.',source_short='Backpropagation handout / PDF p.3, sections5.3-6 / original N3.4 network',source='Backpropagation_Derivation.pdf page 3, sections5.3-6; numerical-practice.md N3.4 and N3.6.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
