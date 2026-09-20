from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'12-regions-function-approximation';out.mkdir(exist_ok=True)
def E(s):return {'eq':s}
def P(title,sub,blocks,stage='WORKED EXAMPLE'):return dict(title=title,subtitle=sub,blocks=blocks,stage=stage)
H=lambda s:int(s>=0)
pages=[P('Turn inequalities into neuron tests','A half-space is the set of points on one side of a line, including the line here.',[
'Study region: the closed rectangle 1 <= x <= 3 and 0 <= y <= 2. We need all four conditions to hold.',
E(r'x\geq1\Rightarrow x-1\geq0\Rightarrow h_1=H(x-1)'),
E(r'x\leq3\Rightarrow3-x\geq0\Rightarrow h_2=H(3-x)'),
E(r'y\geq0\Rightarrow y\geq0\Rightarrow h_3=H(y)'),
E(r'y\leq2\Rightarrow2-y\geq0\Rightarrow h_4=H(2-y)'),
'H(s) = 1 when s >= 0, else 0. This applies the half-space construction in Lecture 2, page 100.']),
P('Require all four tests at the output','Lecture 2, page 108 combines half-space decisions using AND.',[
E(r'R_1=H(h_1+h_2+h_3+h_4-3.5)'),
E(r'\mathrm{all\ four\ true}:\quad R_1=H(4-3.5)=H(0.5)=1'),
E(r'\mathrm{at\ most\ three\ true}:\quad\sum_jh_j-3.5\leq-0.5\Rightarrow R_1=0'),
'The four hidden neurons turn geometric tests into bits. The output checks those bits, not the original x and y values.',
'Their weights for (x, y) and biases are: (1, 0), -1; (-1, 0), 3; (0, 1), 0; (0, -1), 2.',
'Because equality passes each test, the rectangle includes its edges and corners.'])]
for x,y,desc in [(2,1,'Inside'),(0,1,'Left of the region'),(2,3,'Above the region'),(1,0,'At a corner')]:
 vals=[x-1,3-x,y,2-y];h=list(map(H,vals));R=H(sum(h)-3.5)
 pages.append(P(f'{desc}: point ({x}, {y})','Evaluate every half-space, then combine their Boolean outputs.',[
 E(rf'h_1=H({x}-1)=H({vals[0]})={h[0]},\quad h_2=H(3-{x})=H({vals[1]})={h[1]}'),
 E(rf'h_3=H({y})={h[2]},\quad h_4=H(2-{y})=H({vals[3]})={h[3]}'),
 E(rf'R_1=H({h[0]}+{h[1]}+{h[2]}+{h[3]}-3.5)=H({sum(h)-3.5})={R}'),
 'A single failed boundary test rejects the point. Scores equal to zero pass because H(0) = 1.']))
pages += [P('Picture the rectangle and its test points','The shaded region includes all four edges.',[
{'image':'regions.png','width':650},
'The corner (1, 0) passes both equality tests. The points (0, 1) and (2, 3) fail a different half-space each.']),
P('Combine separate regions using OR','Lecture 2, page 109: accept a point if either region accepts it.',[
E(r'R_2=H(H(x-5)+H(6-x)+H(y)+H(2-y)-3.5)'),
'R2 is the closed rectangle 5 <= x <= 6, 0 <= y <= 2.',
E(r'U=H(R_1+R_2-0.5)'),
{'table':[['point','R1 hidden bits','R2 hidden bits','(R1,R2)','U'],['(2,1)','1111','0111','(1,0)',1],['(5.5,1)','1011','1111','(0,1)',1],['(4,1)','1011','0111','(0,0)',0]],'widths':[90,150,150,130,70]},
'For (4,1): R1 = H(3 - 3.5) = 0 and R2 = H(3 - 3.5) = 0. U = H(0 + 0 - 0.5) = 0. The gap stays outside.']),
P('A pulse is the difference of two steps','Lecture 2, page 115 uses two threshold neurons and a summing output.',[
E(r'P(x)=H(x-a)-H(x-b),\qquad a<b'),
E(r'x<a:\quad P=0-0=0'),
E(r'a\leq x<b:\quad P=1-0=1'),
E(r'x\geq b:\quad P=1-1=0'),
'The interval [a, b) includes a but excludes b. At b, the second step turns on and cancels the first.',
'This differs from our closed rectangle: pulse subtraction intentionally switches the output off at the right endpoint.']),
P('Add two scaled pulses','Our study function has height 2 on [0,1) and height 0.5 on [1,3).',[
E(r'f(x)=2[H(x)-H(x-1)]+0.5[H(x-1)-H(x-3)]'),
E(r'=2H(x)+(-2+0.5)H(x-1)-0.5H(x-3)'),
E(r'=2H(x)-1.5H(x-1)-0.5H(x-3)'),
'Hidden outputs are H(x), H(x-1), H(x-3). Final weights are (2, -1.5, -0.5) and bias 0.',
'The final output is a LINEAR sum, not another threshold. Thresholding it would lose the requested heights.'])]
for xx in [[-.5,0,.5],[1,2,3]]:
 blocks=[]
 for x in xx:
  h=[H(x),H(x-1),H(x-3)];f=2*h[0]-1.5*h[1]-.5*h[2]
  blocks += [E(rf'x={x}:\quad h=(H({x}),H({x-1}),H({x-3}))=({h[0]},{h[1]},{h[2]})'),E(rf'f=2({h[0]})-1.5({h[1]})-0.5({h[2]})={f}')]
 pages.append(P('Calculate pulse values: '+', '.join(map(str,xx)),'First threshold the hidden scores, then take the unthresholded weighted sum.',blocks))
pages += [P('Read the endpoints on the graph','Filled circles are included; open circles are excluded at each jump.',[
{'image':'pulse.png','width':650},
'At x = 1 the first pulse ends and the second begins: f(1) = 0.5. At x = 3 both contributions cancel: f(3) = 0.',
'Narrow, scaled pulses are building blocks for approximation (page 116). This finite example is not a proof that one fixed small network exactly fits every function.']),
P('Your turn: shift the region and pulses','Use the same H(0) = 1 convention.',[
'A. Build the closed rectangle -1 <= x <= 1 and 2 <= y <= 4. Write its four hidden tests and AND output. Classify (-1,2), (0,3), (2,3).',
'B. Build a function of height 1.5 on [-1,0) and height 3 on [0,2), zero elsewhere. Give the three hidden steps, output weights and bias.',
'Calculate the function at x = -1, 0, 1 and 2. Show the hidden outputs before the weighted sum.',
'Do not threshold the final function-approximation output.'], 'INDEPENDENT PRACTICE'),
P('Practice answer: the shifted rectangle','Translate each lower and upper bound separately.',[
E(r'h=(H(x+1),H(1-x),H(y-2),H(4-y))'),
E(r'R=H(h_1+h_2+h_3+h_4-3.5)'),
E(r'(-1,2):\quad h=(H(0),H(2),H(0),H(2))=(1,1,1,1)\Rightarrow R=1'),
E(r'(0,3):\quad h=(H(1),H(1),H(1),H(1))=(1,1,1,1)\Rightarrow R=1'),
E(r'(2,3):\quad h=(H(3),H(-1),H(1),H(1))=(1,0,1,1)\Rightarrow R=0'),
'The first point is an included corner. The last point fails the x <= 1 test.'], 'WORKED ANSWER'),
P('Practice answer: derive the pulse weights','Combine the repeated step at x = 0 before reading off the weights.',[
E(r'f=1.5[H(x+1)-H(x)]+3[H(x)-H(x-2)]'),
E(r'=1.5H(x+1)+1.5H(x)-3H(x-2)'),
'Hidden steps: H(x+1), H(x), H(x-2). Weights: (1.5, 1.5, -3), bias 0.',
E(r'x=-1:\ h=(1,0,0)\Rightarrow f=1.5(1)+1.5(0)-3(0)=1.5'),
E(r'x=0,1:\ h=(1,1,0)\Rightarrow f=1.5(1)+1.5(1)-3(0)=3'),
E(r'x=2:\ h=(1,1,1)\Rightarrow f=1.5+1.5-3=0')], 'WORKED ANSWER')]
for p in pages:
 for b in p['blocks']:
  if isinstance(b,dict) and 'eq' in b and len(b['eq'])>95:b['size']=21
fig,ax=plt.subplots(figsize=(8,3),layout='constrained');ax.add_patch(Rectangle((1,0),2,2,facecolor='#dcefeb',edgecolor='#006E73',lw=2))
for x,y in [(2,1),(0,1),(2,3),(1,0)]:ax.scatter(x,y,color='#172B43');ax.annotate(f'({x},{y})',(x,y),xytext=(5,6),textcoords='offset points')
ax.set(xlim=(-.3,3.5),ylim=(-.5,3.5),xlabel='x',ylabel='y');ax.grid(alpha=.2);fig.savefig(out/'regions.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,2.8),layout='constrained')
for a,b,h in [(-1,0,0),(0,1,2),(1,3,.5),(3,4,0)]:
 ax.plot([a,b],[h,h],color='#006E73',lw=2)
for x,y,fill in [(0,0,False),(0,2,True),(1,2,False),(1,.5,True),(3,.5,False),(3,0,True)]:ax.scatter(x,y,facecolor='#006E73' if fill else 'white',edgecolor='#006E73',s=55,zorder=4)
ax.set(xlim=(-1,4),ylim=(-.3,2.5),xlabel='x',ylabel='f(x)');ax.grid(alpha=.2);fig.savefig(out/'pulse.png',dpi=180);plt.close(fig)
checks=[]
for x in [-.5,0,.5,1,2,3]:
 f=2*(H(x)-H(x-1))+.5*(H(x-1)-H(x-3));expected=2 if 0<=x<1 else(.5 if 1<=x<3 else 0);assert f==expected;checks.append(dict(x=x,f=f))
(out/'checks.json').write_text(json.dumps(checks,indent=2))
spec=dict(number=12,title='Geometric classification and function approximation',description='Half-space tests, rectangle intersections, region unions and sums of pulses.',source_short='Lecture 2 / PDF pp.100,108-109,115-116 / original study examples',source='Lecture 2 - Logistic Regression + Neural Network.pdf, pages 100, 108-109 and 115-116.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
