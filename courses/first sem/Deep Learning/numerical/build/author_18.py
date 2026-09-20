from pathlib import Path
import json,copy
from network_math import original,check_forward,forward_scalar
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'18-output-layer-backpropagation';out.mkdir(exist_ok=True)
net=original();A=check_forward([1,2],1);C=check_forward([1,2],0)
y=A['y'][-1][0];h=A['y'][-2];d=y-1;grads=[d*v for v in h]+[d]
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('Start from the saved forward pass','Keep the original parameters from Lessons16-17 fixed throughout backpropagation.',[
E(r'x=(1,2),\quad t=1,\quad y=0.5466967333'),
E(r'y_1^{(2)}=0.5627638384,\quad y_2^{(2)}=0.4537407133'),
E(r'w_{1,1}^{(3)}=0.3,\quad w_{2,1}^{(3)}=-0.4,\quad b_1^{(3)}=0.2'),
E(r'z_1^{(3)}=w_{1,1}^{(3)}y_1^{(2)}+w_{2,1}^{(3)}y_2^{(2)}+b_1^{(3)}'),
'Our goal is all three output-parameter gradients: how sensitive this one example loss is to each parameter when the others stay fixed.',
'The handout calls its per-example loss L. We write ell to keep it distinct from a later batch mean J.']),
P('Delta measures sensitivity to preactivation','The backward calculation follows the same dependencies as the forward calculation.',[
E(r'w\longrightarrow z\longrightarrow y=\sigma(z)\longrightarrow\ell'),
E(r'\delta_1^{(3)}=\frac{\partial\ell}{\partial z_1^{(3)}}'),
E(r'\frac{\partial\ell}{\partial w}=\frac{\partial\ell}{\partial z}\frac{\partial z}{\partial w}=\delta\frac{\partial z}{\partial w}'),
'Delta is a derivative with respect to z. A weight gradient is a derivative with respect to a weight. They are connected by the chain rule but are not usually the same number.',
'First calculate delta at the output; then multiply by each source activation to get that connection gradient. The bias has constant source activation 1.']),
P('Differentiate binary cross-entropy','Handout page 2, section 4.2; assume 0 < y < 1.',[
E(r'\ell=-[t\ln y+(1-t)\ln(1-y)]'),
E(r'\frac{\partial\ell}{\partial y}=-\frac{t}{y}+\frac{1-t}{1-y}'),
E(r'=\frac{-t(1-y)+(1-t)y}{y(1-y)}'),
E(r'=\frac{-t+ty+y-ty}{y(1-y)}=\frac{y-t}{y(1-y)}'),
'The plus sign in the second term comes from two negatives: the loss has a minus sign and the derivative of (1-y) is -1.']),
P('Cancel the sigmoid derivative once','Handout page 2, section 5.1: this shortcut needs sigmoid output and BCE loss.',[
E(r'\frac{\partial y}{\partial z}=y(1-y)'),
E(r'\delta=\frac{\partial\ell}{\partial y}\frac{\partial y}{\partial z}'),
E(r'\delta=\frac{y-t}{y(1-y)}\,y(1-y)=y-t'),
'Do not multiply by y(1-y) again after using delta = y-t. That sigmoid factor has already cancelled.',
'This is a per-example derivative. There is no division by the number of examples here. We will average parameter gradients once in the batch lesson.']),
P('Check both factors numerically','Target t = 1 means the BCE derivative with respect to y is -1/y.',[
E(r'\frac{\partial\ell}{\partial y}=-\frac{1}{0.5466967333}\approx-1.8291676885'),
E(r'\frac{\partial y}{\partial z}=0.5466967333(1-0.5466967333)'),
E(r'\frac{\partial y}{\partial z}\approx0.2478194151'),
E(r'\delta\approx(-1.8291676885)(0.2478194151)=-0.4533032667'),
E(r'\mathrm{shortcut}:\quad y-t=0.5466967333-1=-0.4533032667'),
'The two routes agree. Negative delta means a tiny increase in this output preactivation decreases this example loss locally.']),
P('First output weight: use its source activation','Handout page 3, section 5.2. The source is hidden-layer-2 neuron 1.',[
E(r'\frac{\partial z_1^{(3)}}{\partial w_{1,1}^{(3)}}=y_1^{(2)}'),
E(r'\frac{\partial\ell}{\partial w_{1,1}^{(3)}}=\delta_1^{(3)}y_1^{(2)}'),
E(r'=(-0.4533032667)(0.5627638384)'),
E(r'\approx-0.2551026863'),
'The source activation multiplies the weight in the forward weighted sum. That is why it becomes the local derivative with respect to the weight.',
'Use the activation 0.5627638384, not the hidden preactivation 0.2523866055.']),
P('Second output weight: keep its own source','This connection starts at hidden-layer-2 neuron 2.',[
E(r'\frac{\partial z_1^{(3)}}{\partial w_{2,1}^{(3)}}=y_2^{(2)}'),
E(r'\frac{\partial\ell}{\partial w_{2,1}^{(3)}}=\delta_1^{(3)}y_2^{(2)}'),
E(r'=(-0.4533032667)(0.4537407133)'),
E(r'\approx-0.2056821476'),
'The current weight is -0.4, but this derivative uses its source activation, not the weight itself. The weight will matter when propagating a derivative back to the source neuron.',
'Keep the original -0.4 for the hidden-layer calculation in Lesson19. Do not update it yet.']),
P('Output bias: the source is constant one','Adding one unit to the bias adds one unit to the preactivation.',[
E(r'\frac{\partial z_1^{(3)}}{\partial b_1^{(3)}}=1'),
E(r'\frac{\partial\ell}{\partial b_1^{(3)}}=\delta_1^{(3)}(1)=-0.4533032667'),
{'table':[['output parameter','one-example gradient'],['w1,1 in layer3','-0.2551026863'],['w2,1 in layer3','-0.2056821476'],['bias in layer3','-0.4533032667']],'widths':[270,310]},
'The bias gradient equals delta because its multiplier is 1. This equality does not hold for the other two weight gradients.']),
P('What does a negative gradient predict?','Diagnostic experiment: vary only the output bias; this is not a training update.',[
E(r'\Delta b=+0.001,\quad\Delta\ell\approx\frac{\partial\ell}{\partial b}\Delta b'),
E(r'\Delta\ell\approx(-0.4533032667)(0.001)=-0.0004533033'),
E(r'\mathrm{actual\ fresh\ loss\ change}\approx-0.0004531794'),
'The local estimate is close, not exact, for a finite perturbation. All other weights and biases are held fixed.',
'Return the bias to its original 0.2. Backpropagation in Lesson19 continues from the original parameter state and forward cache.',
'Central finite-difference checks of all three output gradients agree with the analytic results.']),
P('Your turn: flip only the known target','Use the same original input (1,2), parameters and forward prediction; set t = 0.',[
'1. Explain which forward quantities change when only the target changes.',
'2. Calculate BCE, the output delta and all three output-parameter gradients.',
'3. Explain the sign of the bias gradient using a tiny positive bias change with every other parameter fixed.',
'Do not update any parameters. This is the target-flip retry from numerical-practice N3.6.'],'INDEPENDENT PRACTICE'),
P('Practice answer: prediction stays the same','Targets enter the loss; this feedforward model does not use them as inputs.',[
E(r'y=0.5466967333,\quad\ell=-\ln(1-y)\approx0.7911939146'),
E(r'\delta=y-t=0.5466967333-0=0.5466967333'),
E(r'\frac{\partial\ell}{\partial y}=\frac{1}{1-y}\approx2.2060286644'),
E(r'\delta\approx(2.2060286644)(0.2478194151)=0.5466967333'),
'All forward z and y values remain unchanged. The target changes the loss and the backward derivatives. Positive delta means increasing z locally increases the loss for target zero.'],'WORKED ANSWER'),
P('Practice answer: all three output gradients','Use the same two hidden activations and the new positive delta.',[
E(r'\frac{\partial\ell}{\partial w_{1,1}^{(3)}}=(0.5466967333)(0.5627638384)\approx0.3076611521'),
E(r'\frac{\partial\ell}{\partial w_{2,1}^{(3)}}=(0.5466967333)(0.4537407133)\approx0.2480585657'),
E(r'\frac{\partial\ell}{\partial b_1^{(3)}}=(0.5466967333)(1)=0.5466967333'),
'A tiny positive bias change now increases the loss: it raises the probability of class 1 when the known target is 0.',
'Checklist: distinguish delta from a weight gradient, use source activations, cancel sigmoid only once, and keep every parameter unchanged until all required gradients are ready.'],'WORKED ANSWER')]
checks=[]
for target in [1,0]:
 cache=check_forward([1,2],target);delta=cache['y'][-1][0]-target;gg=[delta*v for v in cache['y'][-2]]+[delta]
 for i,g in enumerate(gg):
  plus=copy.deepcopy(net);minus=copy.deepcopy(net);step=1e-6
  if i<2:plus['weights'][2][i][0]+=step;minus['weights'][2][i][0]-=step
  else:plus['biases'][2][0]+=step;minus['biases'][2][0]-=step
  fd=(forward_scalar([1,2],target,plus)['loss']-forward_scalar([1,2],target,minus)['loss'])/(2*step)
  assert abs(fd-g)<1e-8;checks.append(dict(target=target,parameter=i,analytic=g,finite_difference=fd))
pert=copy.deepcopy(net);pert['biases'][2][0]+=.001;change=forward_scalar([1,2],1,pert)['loss']-A['loss'];assert abs(change+.0004531793608464)<1e-12
(out/'checks.json').write_text(json.dumps(dict(gradients=checks,bias_perturbation_change=change),indent=2));(out/'parameters.json').write_text(json.dumps(net,indent=2))
spec=dict(number=18,title='Output-layer backpropagation',description='Derive sigmoid/BCE delta, calculate every output gradient, and verify sensitivity with a target-flip practice.',source_short='Backpropagation handout / PDF pp.2-3, sections4-5.2 / original N3.4 network',source='Backpropagation_Derivation.pdf pages 2-3, sections 4-5.2; numerical-practice.md N3.4 and N3.6.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
