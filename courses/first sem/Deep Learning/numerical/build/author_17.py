from pathlib import Path
import json,math
from network_math import original,check_forward
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'17-complete-forward-pass';out.mkdir(exist_ok=True)
net=original();A=check_forward([1,2],1);B=check_forward([-1,1],0)
assert abs(A['loss']-.6038610483901865)<1e-12 and abs(B['loss']-.7864478888725223)<1e-12
def E(s):return {'eq':s,'size':21}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('Forward means calculate the prediction','Use the same 2-to-2-to-2-to-1 sigmoid network as Lesson16.',[
E(r'x=(1,2),\quad t=1,\quad y_1^{(0)}=1,\quad y_2^{(0)}=2'),
E(r'z_j^{(l)}=\sum_i w_{i,j}^{(l)}y_i^{(l-1)}+b_j^{(l)},\quad y_j^{(l)}=\frac{1}{1+e^{-z_j^{(l)}}}'),
'The handout uses y for each neuron activation and t for the known target. z is the weighted sum before sigmoid. The bias b is the handout weight w0,j.',
'Calculate both neurons of layer 1, then both neurons of layer 2, then the output. A later layer uses activations y from the previous layer, not its preactivations z.',
'Displayed decimals are rounded. Carry unrounded values internally, or at least 8-10 decimal places on a calculator. No parameter changes during this forward pass.']),
P('Start from the original study parameters','Weights use source index first, destination index second.',[
{'table':[['layer','w1,1','w1,2','w2,1','w2,2','b1','b2'],['1','0.1','-0.2','0.3','0.2','0','0.1'],['2','0.4','-0.3','-0.2','0.2','0.1','-0.1'],['3','0.3','—','-0.4','—','0.2','—']],'widths':[65,95,95,95,95,95,95]},
'These are the original N3.4 numerical-practice values, shared with Lesson16. They illustrate the handout equations; the handout does not supply these numbers.',
'A dash means that destination neuron does not exist. There are 10 ordinary weights and 5 biases. All five computational neurons use sigmoid.'])]
def neuron_pages(cache,practice=False):
 result=[]
 for l,(W,b) in enumerate(zip(net['weights'],net['biases']),1):
  for j in range(len(b)):
   prev=cache['y'][l-1];z=cache['z'][l-1][j];y=cache['y'][l][j];p1=W[0][j]*prev[0];p2=W[1][j]*prev[1];exp=math.exp(-z)
   name=f'Layer {l}, neuron {j+1}' if l<3 else 'Layer 3: the output neuron'
   if practice:name='Practice: '+name.lower()
   blocks=[E(rf'z_{{{j+1}}}^{{({l})}}=w_{{1,{j+1}}}^{{({l})}}y_1^{{({l-1})}}+w_{{2,{j+1}}}^{{({l})}}y_2^{{({l-1})}}+b_{{{j+1}}}^{{({l})}}'),
    E(rf'\approx({W[0][j]:g})({prev[0]:.8f})+({W[1][j]:g})({prev[1]:.8f})+({b[j]:g})'),
    E(rf'\approx({p1:.8f})+({p2:.8f})+({b[j]:g})={z:.8f}'),
    E(rf'e^{{-z}}=e^{{-({z:.8f})}}\approx {exp:.8f}'),
    E(rf'y_{{{j+1}}}^{{({l})}}=\frac{{1}}{{1+e^{{-z}}}}\approx\frac{{1}}{{1+{exp:.8f}}}={y:.8f}')]
   blocks.append('The preactivation is negative, so minus z is positive inside the exponential. Sigmoid still returns a positive number below 0.5.' if z<0 else ('Cache the output probability for the loss. Keep its preactivation separately; they are different quantities.' if l==3 else 'Cache this activation for the next layer. Keep its preactivation separately; they are different quantities.'))
   result.append(P(name,'First multiply and add, then apply sigmoid to this neuron only.',blocks,'WORKED ANSWER' if practice else 'WORKED EXAMPLE'))
 return result
pages+=neuron_pages(A)
pages+=[P('Use the probability in binary cross-entropy','The target first enters here; it did not enter any forward neuron calculation.',[
E(r'\ell=-[t\ln y+(1-t)\ln(1-y)]'),
E(r't=1,\quad y=0.5466967333'),
E(r'\ell=-[1\ln(0.5466967333)+0\ln(1-0.5466967333)]'),
E(r'\ell=-\ln(0.5466967333)\approx0.6038610484'),
'Use natural logarithms and the probability y. Do not threshold y into class 0 or 1 before calculating cross-entropy.',
'This is one example loss, not an average over a batch. Changing the target would change the loss, but not this prediction at fixed input and parameters.']),
P('Keep a forward cache for backpropagation','Later derivatives reuse these activations and preactivations.',[
{'table':[['neuron','z','y = sigmoid(z)'],['layer1 / 1','0.7000000000','0.6681877722'],['layer1 / 2','0.3000000000','0.5744425168'],['layer2 / 1','0.2523866055','0.5627638384'],['layer2 / 2','-0.1855678283','0.4537407133'],['layer3 / 1','0.1873328662','0.5466967333']],'widths':[180,220,260]},
'This table is a checkpoint, not a replacement for the substitutions. Lessons18-19 start from these same forward values and original weights.',
'Common mistakes: swapping weight indices, feeding z instead of y to the next layer, forgetting a bias, rounding too early, or changing parameters midway.']),
P('Your turn: a different input and target','Reset to the same original parameter table. No training update has happened.',[
E(r'x=(-1,1),\quad t=0'),
'Calculate all five z values and all five sigmoid activations. Then calculate the one-example binary cross-entropy.',
'Write each neuron as two weight-times-activation products plus its bias. Watch the negative input and the negative preactivation in hidden layer 2.',
'This is example B from numerical-practice N3.5. It will join example A in the later batch-update lesson.'],'INDEPENDENT PRACTICE')]
pages+=neuron_pages(B,True)
pages+=[P('Practice answer: loss for target zero','Keep the probability; use the other term of binary cross-entropy.',[
E(r'y=0.5445402309851674,\quad t=0'),
E(r'\ell=-[0\ln y+1\ln(1-y)]=-\ln(1-y)'),
E(r'1-y=1-0.5445402309851674=0.4554597690148326'),
E(r'\ell=-\ln(0.4554597690148326)\approx0.7864478889'),
'The model assigns more than half its probability to class 1, although the target is 0, so this is an incorrect thresholded prediction. The cross-entropy uses the probability, not just that mistake count.',
'Every parameter is still at its original value. Only the input, target and resulting cached quantities changed.'],'WORKED ANSWER')]
(out/'checks.json').write_text(json.dumps(dict(A=A,B=B),indent=2));(out/'parameters.json').write_text(json.dumps(net,indent=2))
spec=dict(number=17,title='A complete network forward pass',description='Every weighted sum, sigmoid and loss for the shared five-neuron network, followed by a full fresh-input practice.',source_short='Backpropagation handout / PDF pp.1-2; numerical-practice N3.4-N3.5',source='Backpropagation_Derivation.pdf pages 1-2; numerical-practice.md N3.4 and N3.5 chosen parameters and examples.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
