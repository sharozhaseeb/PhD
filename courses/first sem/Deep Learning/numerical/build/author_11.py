from pathlib import Path
import json,itertools
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'11-parity-depth-width';out.mkdir(exist_ok=True)
def E(s):return {'eq':s}
def P(title,sub,blocks,stage='WORKED EXAMPLE'):return dict(title=title,subtitle=sub,blocks=blocks,stage=stage)
truth=[['ABC','ones','odd parity'],*[[ ''.join(map(str,r)),sum(r),sum(r)%2] for r in itertools.product([0,1],repeat=3)]]
fig,ax=plt.subplots(figsize=(9,2.7),layout='constrained');ax.axis('off');ax.set(xlim=(-.5,7.5),ylim=(-.4,3.5))
levels=[[(i,3,str(v)) for i,v in enumerate([1,0,1,1,0,0,1,0])],[(i*2+.5,2,'XOR') for i in range(4)],[(1.5,1,'XOR'),(5.5,1,'XOR')],[(3.5,0,'XOR')]]
for lev in range(3):
 for i,(x,y,l) in enumerate(levels[lev]):
  xx,yy,_=levels[lev+1][i//2];ax.annotate('',xy=(xx,yy+.2),xytext=(x,y-.2),arrowprops=dict(arrowstyle='->',color='#006E73'))
for level in levels:
 for x,y,l in level:ax.text(x,y,l,ha='center',va='center',fontsize=12,bbox=dict(boxstyle='round,pad=.25',facecolor='#edf3f7',edgecolor='#172B43'))
fig.savefig(out/'tree.png',dpi=180);plt.close(fig)
pages=[P('Parity counts whether the number is odd','Odd parity is 1 for an odd number of ones and 0 for an even number.',[
{'table':truth,'widths':[140,150,160]},
'XOR combines two parity bits. Combining all input bits by repeated XOR computes the parity of the whole input.']),
P('Why a parity K-map cannot merge pairs','Flipping one bit switches odd to even or even to odd.',[
{'table':[['A / BC','00','01','11','10'],['0',0,1,0,1],['1',1,0,1,0]],'widths':[170,100,100,100,100]},
'Every horizontal or vertical neighbor has the opposite output, including wraparound neighbors. There is no adjacent pair of ones to merge.',
E(r'2^3=8\ \mathrm{rows};\qquad 8/2=4\ \mathrm{true\ rows}'),
'For N inputs, pair every row with the row obtained by flipping its first bit. Each pair has one odd and one even row, so exactly half are true.']),
P('Eight inputs: count the shallow DNF','Lecture 2, pages 80 and 87: one hidden row detector per true row, then one OR.',[
E(r'2^8=256,\quad\mathrm{hidden}=256/2=128,\quad\mathrm{total}=128+1=129'),
'Depth is the longest number of computational neurons along an input-to-output path. Here: detector then OR, so depth = 2.',
E(r'\mathrm{weights}=8(128)+128(1)=1152'),
E(r'\mathrm{biases}=128+1=129,\quad\mathrm{parameters}=1152+129=1281'),
'Width is the largest number of neurons at one depth: 128. These counts describe the specified dense DNF construction, not every possible shallow network.']),
P('Reuse the lecture\'s three-neuron XOR','Each module uses the page-57 construction from Lesson09.',[
E(r'h_1=H(x+y-1),\quad h_2=H(-x-y+1),\quad q=H(h_1+h_2-2)'),
E(r'(x,y)=(1,1):\quad h_1=H(1+1-1)=H(1)=1'),
E(r'h_2=H(-1-1+1)=H(-1)=0'),
E(r'q=H(1+0-2)=H(-1)=0'),
'Per module: 2 hidden + 1 output = 3 neurons; 4 + 2 = 6 weights; 3 biases; 9 parameters; depth 2.',
'Use the same module throughout the comparison. Switching to the two-neuron skip variant would change the counts.']),
P('Balance the XOR modules in a tree','The boxes below are XOR modules, each containing three actual neurons.',[
{'image':'tree.png','width':670},
'First combine four pairs, then combine the two pairs of intermediate results, then combine the final pair.',
E(r'\mathrm{modules}=4+2+1=7=N-1\quad(N=8)')]),
P('Propagate an eight-bit input','Input: 1, 0, 1, 1, 0, 0, 1, 0. There are four ones, so parity should be 0.',[
E(r'\mathrm{level\ 1}:\quad1\oplus0=1,\quad1\oplus1=0,\quad0\oplus0=0,\quad1\oplus0=1'),
E(r'\mathrm{level\ 2}:\quad1\oplus0=1,\qquad0\oplus1=1'),
E(r'\mathrm{level\ 3}:\quad1\oplus1=0'),
'The symbol with a plus inside a circle means XOR. A module outputs 1 when its two input bits differ.',
'Three module levels are not three neuron layers: each module takes two computational layers.']),
P('Count neurons, depth and parameters','Lecture 2, pages 86-87 give the 3(N - 1) construction and balanced depth.',[
E(r'\mathrm{neurons}=3(8-1)=21'),
E(r'\mathrm{depth}=2\log_2(8)=2(3)=6'),
E(r'\mathrm{weights}=7(6)=42,\quad\mathrm{biases}=7(3)=21'),
E(r'\mathrm{parameters}=42+21=63'),
'First layer width = 4 modules times 2 hidden neurons = 8, the maximum. Total 21 is not the width.',
'A sequential chain of seven modules has the same neuron count but depth 14. The depth-6 result needs a balanced arrangement.']),
P('Your turn: four inputs','Use the same dense DNF and the same three-neuron XOR module.',[
E(r'(x_1,x_2,x_3,x_4)=(1,1,0,1)'),
'1. Compute parity through a balanced two-level XOR tree.',
'2. For DNF, calculate hidden neurons, total neurons, depth and all parameters.',
'3. For the tree, calculate modules, neurons, depth, weights, biases and total parameters.',
'Inputs have depth zero and are excluded from neuron counts. Compare these specific constructions, not a universal lower bound.'], 'INDEPENDENT PRACTICE'),
P('Practice answer: equal totals can mislead','Four-input DNF and the tree both have nine neurons, but different connections.',[
E(r'1\oplus1=0,\quad0\oplus1=1,\quad0\oplus1=1'),
E(r'\mathrm{DNF\ hidden}=2^{4-1}=8,\quad\mathrm{total}=8+1=9,\quad\mathrm{depth}=2'),
E(r'\mathrm{DNF\ parameters}=4(8)+8+8(1)+1=49'),
E(r'\mathrm{tree\ modules}=2+1=3,\quad\mathrm{neurons}=3(3)=9,\quad\mathrm{depth}=2(2)=4'),
E(r'\mathrm{weights}=3(6)=18,\quad\mathrm{biases}=3(3)=9,\quad\mathrm{parameters}=27'),
'For a non-power-of-two input count, balance an uneven tree and count actual levels; never report a fractional number of layers.'], 'WORKED ANSWER')]
for p in pages:
 for b in p['blocks']:
  if isinstance(b,dict) and 'eq' in b and (len(b['eq'])>120 or p is pages[-1]):b['size']=21
checks={str(n):dict(dnf_hidden=2**(n-1),dnf_total=2**(n-1)+1,dnf_params=(n+2)*2**(n-1)+1,tree_neurons=3*(n-1),tree_params=9*(n-1)) for n in [4,8]}
for n in [4,8]:assert sum(sum(r)%2 for r in itertools.product([0,1],repeat=n))==2**(n-1)
(out/'checks.json').write_text(json.dumps(checks,indent=2))
spec=dict(number=11,title='Parity and depth versus width',description='Propagate parity values and count two specified network constructions.',source_short='Lecture 2 / PDF pp.80,83-87 / construction-specific counts',source='Lecture 2 - Logistic Regression + Neural Network.pdf, pages 80 and 83-87.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
