from pathlib import Path
import json,itertools
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'09-xor-hidden-layer';out.mkdir(exist_ok=True)
def E(s):return {'eq':s}
def P(title,sub,blocks,stage='WORKED EXAMPLE'):return dict(title=title,subtitle=sub,blocks=blocks,stage=stage)
pages=[P('XOR asks whether the inputs differ','Exclusive OR returns 1 for exactly one active input.',[
E(r'(x,y)=(0,0)\Rightarrow0,\quad(0,1)\Rightarrow1'),
E(r'(x,y)=(1,0)\Rightarrow1,\quad(1,1)\Rightarrow0'),
'The two positive points lie at opposite corners of the unit square. No single straight line separates them from both negative corners.',
'Lecture 2, page 56: one threshold neuron cannot compute XOR. Hidden neurons create intermediate Boolean features that the output can combine.',
E(r'H(s)=1\ \mathrm{if}\ s\geq0;\qquad H(s)=0\ \mathrm{if}\ s<0'),
'Keep this inclusive equality convention for every neuron in the lesson.']),
P('The three-neuron construction','These are exactly the two hidden gates and output gate on Lecture 2, page 57.',[
E(r'h_{\mathrm{OR}}=H(x+y-1)'),
E(r'h_{\mathrm{NAND}}=H(-x-y+1)'),
E(r'q=H(h_{\mathrm{OR}}+h_{\mathrm{NAND}}-2)'),
'The hidden OR says at least one input is 1. Hidden NAND says they are not both 1. The output AND requires both statements to be true.',
'NAND has weights (-1, -1), threshold T = -1 and bias +1. OR has threshold 1; the output has threshold 2.',
'Compute hidden outputs first. Feed their 0/1 outputs, not their scores, into the final neuron.'])]
for pairs in [[(0,0),(0,1)],[(1,0),(1,1)]]:
 blocks=[]
 for x,y in pairs:
  u=x+y-1;v=-x-y+1;hu=int(u>=0);hv=int(v>=0);s=hu+hv-2
  blocks += [E(rf'(x,y)=({x},{y}):\quad h_{{\mathrm{{OR}}}}=H({x}+{y}-1)=H({u})={hu}'),E(rf'h_{{\mathrm{{NAND}}}}=H(-{x}-{y}+1)=H({v})={hv}'),E(rf'q=H({hu}+{hv}-2)=H({s})={int(s>=0)}')]
 pages.append(P('Three neurons: work through '+str(pairs[0])+', '+str(pairs[1]),'First the two hidden decisions, then the output decision.',blocks))
pages += [P('The two-neuron construction','Lecture 2, page 58 allows direct input-to-output connections.',[
E(r'h=H(x+y-2),\qquad q=H(x+y-2h-1)'),
'The hidden neuron h is AND. The output receives x, y and h, with weights 1, 1 and -2. Its threshold is 1.',
'If both inputs are 1, the hidden neuron subtracts 2 at the output. This suppresses the 11 case that a simple OR would accept.',
'The direct edges bypass the hidden neuron. This is why this construction can use fewer neurons than the previous adjacent-layer construction.',
'Both constructions compute the same XOR truth table. Their allowed connections are different.'])]
for pairs in [[(0,0),(0,1)],[(1,0),(1,1)]]:
 blocks=[]
 for x,y in pairs:
  s=x+y-2;h=int(s>=0);v=x+y-2*h-1
  blocks += [E(rf'(x,y)=({x},{y}):\quad h=H({x}+{y}-2)=H({s})={h}'),E(rf'q=H({x}+{y}-2({h})-1)=H({v})={int(v>=0)}')]
 blocks += ['The raw inputs go directly to the output as well as to h. Never replace x and y by h.']
 pages.append(P('Two neurons: work through '+str(pairs[0])+', '+str(pairs[1]),'Use the newly calculated hidden output in the output score.',blocks))
pages += [P('Compare the actual connection patterns','Counts exclude input nodes. Every neuron contributes one bias parameter.',[
{'image':'architectures.png','width':590},
'Left: 2 hidden + 1 output = 3 neurons; 4 input edges + 2 output edges = 6 weights; 6 + 3 biases = 9 parameters.',
'Right: 1 hidden + 1 output = 2 neurons; 2 hidden-input + 3 output-input edges = 5 weights; 5 + 2 biases = 7 parameters.',
'Depth is 2 in both: the longest path from input to output crosses two computational neurons. These are construction-specific counts.']),
P('Your turn: equal inputs should return 1','XNOR is the complement of XOR. Add a NOT neuron after the XOR output q.',[
E(r'r=H(-q)'),
'1. Use the XOR outputs for 00, 01, 10 and 11. Calculate the new score -q and output r in each row.',
'2. How many neurons, weights and biases did this added gate introduce?',
'3. What is the new longest input-to-output depth?',
'The new gate uses weight -1 and bias 0. Count its bias as a parameter even though its chosen value is zero.'], 'INDEPENDENT PRACTICE'),
P('Practice answer: one more layer','q is XOR; r is XNOR, so r must be 1 precisely when the original inputs agree.',[
E(r'00:\ q=0\Rightarrow r=H(-0)=H(0)=1'),
E(r'01:\ q=1\Rightarrow r=H(-1)=0'),
E(r'10:\ q=1\Rightarrow r=H(-1)=0'),
E(r'11:\ q=0\Rightarrow r=H(-0)=H(0)=1'),
'Added: 1 neuron, 1 weight and 1 bias. Longest depth rises from 2 to 3 because every old path now ends at the extra NOT neuron.',
'Avoid: treating a circle threshold as a bias; forgetting direct edges in the two-neuron version; sending hidden scores instead of hidden outputs.'], 'WORKED ANSWER')]
fig,axs=plt.subplots(1,2,figsize=(9,2.6),layout='constrained')
for ax,skip in zip(axs,[False,True]):
 ax.set(xlim=(0,6),ylim=(-.3,3.3));ax.axis('off')
 nodes={'x':(.5,2.5),'y':(.5,.5),'q':(5,1.5)}
 if skip:nodes['AND']=(2.7,1.5);edges=[('x','AND'),('y','AND'),('AND','q'),('x','q'),('y','q')]
 else:nodes.update({'OR':(2.7,2.5),'NAND':(2.7,.5)});edges=[('x','OR'),('y','OR'),('x','NAND'),('y','NAND'),('OR','q'),('NAND','q')]
 for a,b in edges:
  x,y=nodes[a];xx,yy=nodes[b];ax.annotate('',xy=(xx-.4,yy),xytext=(x+.4,y),arrowprops=dict(arrowstyle='->',color='#006E73'))
 for label,(x,y) in nodes.items():ax.text(x,y,label,ha='center',va='center',bbox=dict(boxstyle='round,pad=.4',facecolor='#edf3f7',edgecolor='#172B43'))
 ax.set_title('Page 58: direct edges' if skip else 'Page 57: hidden layer',fontsize=12)
fig.savefig(out/'architectures.png',dpi=180);plt.close(fig)
checks=[]
for x,y in itertools.product([0,1],repeat=2):
 H=lambda s:int(s>=0);a=H(x+y-1);b=H(-x-y+1);q=H(a+b-2);h=H(x+y-2);qq=H(x+y-2*h-1);assert q==qq==(x^y);checks.append(dict(x=x,y=y,hOR=a,hNAND=b,q=q,h=h,q_skip=qq))
(out/'checks.json').write_text(json.dumps(checks,indent=2))
spec=dict(number=9,title='XOR with a hidden layer',description='Evaluate every input pair through both exact lecture architectures.',source_short='Lecture 2 / PDF pp.56-58 / inclusive thresholds',source='Lecture 2 - Logistic Regression + Neural Network.pdf, pages 56-58.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
