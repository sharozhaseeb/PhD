from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
build=Path(__file__).resolve().parent
out=build.parent/'16-network-shapes-parameters';out.mkdir(exist_ok=True)
network=dict(name='N3.4 original study network',architecture=[2,2,2,1],convention='examples are rows; weight row is source i, column is destination j',weights=[[[.1,-.2],[.3,.2]],[[.4,-.3],[-.2,.2]],[[.3],[-.4]]],biases=[[0,.1],[.1,-.1],[.2]],examples=[dict(x=[1,2],target=1),dict(x=[-1,1],target=0)])
(build/'shared-network.json').write_text(json.dumps(network,indent=2))
(out/'parameters.json').write_text(json.dumps(network,indent=2))
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('One network for the next five lessons','Architecture and notation follow the backpropagation handout; numbers are study choices.',[
{'image':'network.png','width':660},
'Input layer 0 has two features. Hidden layers 1 and 2 each have two sigmoid neurons. Layer 3 has one sigmoid output neuron.',
'Lessons 16-20 reuse the original N3.4 numerical-practice parameters. This lesson checks connections, shapes and counts before the full forward pass.']),
P('Read the weight indices as an arrow','The handout writes the source index first and the destination index second.',[
E(r'w_{i,j}^{(l)}:\quad\mathrm{source}\ i\ \mathrm{in\ layer}\ l-1\ \longrightarrow\ \mathrm{destination}\ j\ \mathrm{in\ layer}\ l'),
E(r'w_{2,1}^{(1)}=0.3:\quad x_2\longrightarrow y_1^{(1)}'),
E(r'w_{1,2}^{(1)}=-0.2:\quad x_1\longrightarrow y_2^{(1)}'),
E(r'b_j^{(l)}=w_{0,j}^{(l)}'),
'The bias is the weight from constant input 1. We store it separately as b. Do not also add a second constant-input bias if it is already included in b.',
'z is the weighted sum before activation; y is the activation after sigmoid. Known target labels will be written t.']),
P('Count every weight and every bias','Each destination neuron has one weight per source neuron and one bias.',[
E(r'\mathrm{layer\ 1}:\quad 2(2)+2=4+2=6'),
E(r'\mathrm{layer\ 2}:\quad 2(2)+2=4+2=6'),
E(r'\mathrm{layer\ 3}:\quad 2(1)+1=2+1=3'),
E(r'\mathrm{weights}=4+4+2=10,\quad\mathrm{biases}=2+2+1=5'),
E(r'\mathrm{total\ trainable\ parameters}=10+5=15'),
'Input values are data, not trainable parameters. The sigmoid function adds no trainable parameter in this network.']),
P('Record all original parameter values','Reset to this table whenever a later exercise says original parameters.',[
{'table':[['layer','w1,1','w1,2','w2,1','w2,2','b1','b2'],['1','0.1','-0.2','0.3','0.2','0','0.1'],['2','0.4','-0.3','-0.2','0.2','0.1','-0.1'],['3','0.3','—','-0.4','—','0.2','—']],'widths':[65,95,95,95,95,95,95]},
'Layer 3 has only destination 1. Dashes mean those destination-2 connections do not exist; they are not additional zero-valued parameters.',
'These are chosen teaching values from numerical-practice.md, not numerical values supplied by the handout. The architecture and indexing come from the handout.']),
P('Arrange connection weights into a matrix','Rows are sources; columns are destinations. The convention determines the multiplication.',[
{'image':'matrix.png','width':490},
E(r'W^{(1)}\ \mathrm{has\ shape}\ 2\times2,\quad b^{(1)}=[0,0.1]'),
'Column 1 contains the two weights feeding hidden neuron 1. Column 2 contains the two weights feeding hidden neuron 2.']),
P('Matrix multiplication is a list of dot products','For a single example, place input values in one row.',[
E(r'Y^{(0)}=[1,2],\quad Z^{(1)}=Y^{(0)}W^{(1)}+b^{(1)}'),
E(r'z_1^{(1)}=1(0.1)+2(0.3)+0=0.1+0.6=0.7'),
E(r'z_2^{(1)}=1(-0.2)+2(0.2)+0.1=-0.2+0.4+0.1=0.3'),
E(r'Z^{(1)}=[0.7,0.3]'),
'Each output entry pairs the input row with one destination column of W. The bias for that destination is added exactly once.']),
P('Apply sigmoid to each entry separately','Activation changes the values, not the array shape.',[
E(r'Y^{(1)}=\sigma(Z^{(1)})'),
E(r'y_1^{(1)}=\sigma(0.7)=\frac{1}{1+e^{-0.7}}\approx0.668188'),
E(r'y_2^{(1)}=\sigma(0.3)=\frac{1}{1+e^{-0.3}}\approx0.574443'),
E(r'Y^{(1)}\approx[0.668188,0.574443],\quad\mathrm{shape}\ 1\times2'),
'This is elementwise activation, not a matrix inverse or a sigmoid of the sum of both entries. Lesson17 continues through the other two layers.']),
P('Add a second example as another row','Use the same weights and biases for both examples.',[
{'table':[['example','x1','x2','z1 in layer1','z2 in layer1'],['A','1','2','0.7','0.3'],['B','-1','1','0.2','0.5']],'widths':[110,90,90,190,190]},
E(r'z_{B,1}^{(1)}=(-1)(0.1)+(1)(0.3)+0=0.2'),
E(r'z_{B,2}^{(1)}=(-1)(-0.2)+(1)(0.2)+0.1=0.5'),
'Input X and output Z1 now both have shape 2 by 2. Each row keeps its own example; columns keep neuron identities.',
'Bias broadcasting means reuse [0,0.1] on each row. It does not create new learned biases for example B.']),
P('Check dimensions before multiplying','Inner dimensions must agree; the outer dimensions give the result shape.',[
'N counts examples; d(l) is the number of neurons in layer l, with d(0) equal to input features.',
E(r'(N\times d_{l-1})(d_{l-1}\times d_l)=N\times d_l'),
E(r'Z^{(l)}=Y^{(l-1)}W^{(l)}+b^{(l)}'),
{'table':[['stage','Y input','W','bias','Z and Y output'],['layer1','2 x 2','2 x 2','1 x 2','2 x 2'],['layer2','2 x 2','2 x 2','1 x 2','2 x 2'],['layer3','2 x 2','2 x 1','1 x 1','2 x 1']],'widths':[95,125,125,125,190]},
'N = 2 here counts examples. The final 2 by 1 array has one prediction per example. Increasing N changes activation shapes, not the 15-parameter count.']),
P('Your turn: a different small architecture','Use the same row-example and source-to-destination convention.',[
E(r'3\ \mathrm{inputs}\longrightarrow2\ \mathrm{hidden}\longrightarrow1\ \mathrm{output}'),
'1. Count all connection weights, all biases and total trainable parameters.',
'2. For a batch of four examples, give the shapes of X, W1, b1, Z1, W2, b2 and Z2.',
'3. For one input x = (1,0,-1), W1 has rows (1,2), (3,4), (5,6); b1 = (0.5,-0.5). Compute both entries of z1 by scalar multiplication.',
'Do not apply an activation in question 3: it asks for preactivation z.'],'INDEPENDENT PRACTICE'),
P('Practice answer: count and check shapes','A larger input width adds connections into every first-layer neuron.',[
E(r'\mathrm{weights}=3(2)+2(1)=6+2=8'),
E(r'\mathrm{biases}=2+1=3,\quad\mathrm{total}=8+3=11'),
E(r'X:4\times3,\quad W^{(1)}:3\times2,\quad b^{(1)}:1\times2'),
E(r'Z^{(1)}:4\times2,\quad W^{(2)}:2\times1,\quad b^{(2)}:1\times1'),
E(r'Z^{(2)}:4\times1'),
'Four examples share the same 11 parameters. Biases are broadcast over four rows, not trained separately for each row.'],'WORKED ANSWER'),
P('Practice answer: multiply one row by columns','The zero input still has associated weights, even though its contribution is zero here.',[
E(r'z_1=1(1)+0(3)+(-1)(5)+0.5=1+0-5+0.5=-3.5'),
E(r'z_2=1(2)+0(4)+(-1)(6)-0.5=2+0-6-0.5=-4.5'),
E(r'Z^{(1)}=[-3.5,-4.5],\quad\mathrm{shape}\ 1\times2'),
'Column 1 was (1,3,5); column 2 was (2,4,6). Multiplying by rows instead would mix up source and destination indices.',
'Checklist: identify rows and columns, check inner dimensions, add each bias once, and keep parameter count separate from batch size.'],'WORKED ANSWER')]
fig,ax=plt.subplots(figsize=(10,3),layout='constrained');ax.axis('off');ax.set(xlim=(-.6,3.6),ylim=(-1.1,1.3))
levels=[[(0,.6),(0,-.3)],[(1,.6),(1,-.3)],[(2,.6),(2,-.3)],[(3,.15)]]
for a,b in zip(levels,levels[1:]):
 for x,y in a:
  for u,v in b:ax.annotate('',xy=(u-.1,v),xytext=(x+.1,y),arrowprops=dict(arrowstyle='->',color='#8aa4b5'))
for l,lev in enumerate(levels):
 for j,(x,y) in enumerate(lev):ax.text(x,y,f'x{j+1}' if l==0 else f'y{j+1}',ha='center',va='center',fontsize=13,bbox=dict(boxstyle='circle,pad=.45',facecolor='#dcefeb',edgecolor='#006E73'))
 ax.text(l,-.8,['input 0','hidden 1','hidden 2','output 3'][l],ha='center',fontsize=12)
ax.text(1.5,1.13,'Every computational neuron also has one bias (not drawn).',ha='center',fontsize=11)
fig.savefig(out/'network.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(6,2.7),layout='constrained');ax.axis('off');ax.set(xlim=(-1.4,2.8),ylim=(-.7,2.1))
for i,row in enumerate(network['weights'][0]):
 for j,v in enumerate(row):ax.text(j,1-i,f'{v:g}',ha='center',va='center',fontsize=23)
for x,d in [(-.5,.15),(1.5,-.15)]:ax.plot([x+d,x,x,x+d],[1.4,1.4,-.4,-.4],color='#172B43',lw=2)
for i in range(2):ax.text(-.7,1-i,f'source {i+1}',ha='right',va='center',fontsize=12);ax.text(i,1.8,f'destination {i+1}',ha='center',fontsize=12)
ax.text(2,0.5,'W1',fontsize=24,ha='center');fig.savefig(out/'matrix.png',dpi=180);plt.close(fig)
X=np.array([[1,2],[-1,1]]);Z=X@np.array(network['weights'][0])+np.array(network['biases'][0]);np.testing.assert_allclose(Z,[[.7,.3],[.2,.5]])
assert sum(np.size(a) for a in network['weights'])+sum(np.size(b) for b in network['biases'])==15
(out/'checks.json').write_text(json.dumps(dict(Z1=Z.tolist(),parameters=15,practice_z=[-3.5,-4.5]),indent=2))
spec=dict(number=16,title='Network shapes and parameter counts',description='Map scalar connections to matrices using the shared network for Lessons16-20.',source_short='Backpropagation handout / PDF p.1; Assignment 1 / pp.1-3 / study parameters',source='Backpropagation_Derivation.pdf page 1; Assignment 1.pdf pages 1-3; numerical-practice.md N3.4 chosen parameters.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
