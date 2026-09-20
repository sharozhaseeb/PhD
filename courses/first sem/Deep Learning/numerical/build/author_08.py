from pathlib import Path
import json,itertools
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'08-neurons-logic-gates';out.mkdir(exist_ok=True)
def E(s):return {'eq':s}
def P(title,sub,blocks,stage='WORKED EXAMPLE'):return dict(title=title,subtitle=sub,blocks=blocks,stage=stage)
pages=[P('A neuron can make a Boolean decision','A threshold gate returns 0 or 1 directly; it does not return a probability.',[
E(r's=\sum_i w_ix_i-T=\sum_i w_ix_i+b,\qquad b=-T'),
'x values are inputs; w values are weights; T is a threshold; b is the equivalent bias; s is the score before the decision.',
E(r'H(s)=1\ \mathrm{if}\ s\geq0,\qquad H(s)=0\ \mathrm{if}\ s<0'),
'We choose H(0) = 1. This inclusive rule reproduces the integer thresholds shown inside the circles on Lecture 2, pages 54-55.',
'The generic wording "positive" on page 40 can suggest a strict rule. If using a strict rule, shift the thresholds; do not silently mix conventions.',
'Here we construct fixed weights by hand. Learning those weights is a later topic.']),
P('AND: both inputs must be 1','Lecture 2, page 54: weights (1, 1), threshold T = 2, bias b = -2.',[
E(r'y=H(1x_1+1x_2-2)'),
E(r'(0,0):\ s=1(0)+1(0)-2=-2\Rightarrow H(-2)=0'),
E(r'(0,1):\ s=1(0)+1(1)-2=-1\Rightarrow H(-1)=0'),
E(r'(1,0):\ s=1(1)+1(0)-2=-1\Rightarrow H(-1)=0'),
E(r'(1,1):\ s=1(1)+1(1)-2=0\Rightarrow H(0)=1'),
'Only the final row reaches the threshold. This is the complete two-input AND truth table.']),
P('OR: at least one input must be 1','Lecture 2, page 54: weights (1, 1), threshold T = 1, bias b = -1.',[
E(r'y=H(1x_1+1x_2-1)'),
E(r'(0,0):\ s=1(0)+1(0)-1=-1\Rightarrow H(-1)=0'),
E(r'(0,1):\ s=1(0)+1(1)-1=0\Rightarrow H(0)=1'),
E(r'(1,0):\ s=1(1)+1(0)-1=0\Rightarrow H(0)=1'),
E(r'(1,1):\ s=1(1)+1(1)-1=1\Rightarrow H(1)=1'),
'Changing only the threshold changed AND into OR. The weights still count the number of active inputs.']),
P('NOT: reverse a single Boolean input','Lecture 2, page 54: weight -1, threshold T = 0, bias b = 0.',[
E(r'y=H(-x)'),
E(r'x=0:\quad s=(-1)(0)-0=0\Rightarrow H(0)=1'),
E(r'x=1:\quad s=(-1)(1)-0=-1\Rightarrow H(-1)=0'),
'A negative weight lets an input inhibit the neuron: turning the input on lowers the score.',
'NOT means 0 becomes 1 and 1 becomes 0. The thresholded output is a Boolean value, not the signed score.']),
P('Majority of three: first four rows','Lecture 2, page 55: at least K inputs active. Here K = 2 and all weights are 1.',[
E(r'y=H(x_1+x_2+x_3-2),\qquad b=-2'),
E(r'(0,0,0):\ s=0+0+0-2=-2\Rightarrow0'),
E(r'(0,0,1):\ s=0+0+1-2=-1\Rightarrow0'),
E(r'(0,1,0):\ s=0+1+0-2=-1\Rightarrow0'),
E(r'(0,1,1):\ s=0+1+1-2=0\Rightarrow1'),
'The final arrow applies H. The first three rows have fewer than two ones; the fourth row has exactly two.']),
P('Majority of three: remaining four rows','Together with the previous page, these cover all 2 cubed = 8 possible inputs.',[
E(r'(1,0,0):\ s=1+0+0-2=-1\Rightarrow0'),
E(r'(1,0,1):\ s=1+0+1-2=0\Rightarrow1'),
E(r'(1,1,0):\ s=1+1+0-2=0\Rightarrow1'),
E(r'(1,1,1):\ s=1+1+1-2=1\Rightarrow1'),
'With unit weights, only the number of ones matters, not their positions.',
'For Boolean inputs, T = 1.5 would give the same majority table while avoiding ties. We used T = 2 to match the lecture\'s integer-threshold notation.']),
P('Your turn: NAND and a larger vote','NAND returns 0 only when both inputs are 1.',[
E(r'(w_1,w_2)=(-1,-1),\quad b=1.5,\quad T=-1.5'),
'1. Calculate the score and output for all four pairs 00, 01, 10, 11. Verify that this is NAND.',
'2. Construct a unit-weight neuron that returns 1 if at least three out of four inputs are 1. State its threshold and bias.',
'3. Check the larger gate for input counts 2, 3 and 4.',
'Remember: b = -T, even if the threshold itself is negative.'], 'INDEPENDENT PRACTICE'),
P('Practice answer: check the signs','NAND uses a positive bias and negative input weights.',[
E(r'00:\ s=-0-0+1.5=1.5\Rightarrow1,\quad01:\ s=-0-1+1.5=0.5\Rightarrow1'),
E(r'10:\ s=-1-0+1.5=0.5\Rightarrow1,\quad11:\ s=-1-1+1.5=-0.5\Rightarrow0'),
E(r'y=H(x_1+x_2+x_3+x_4-3),\quad T=3,\quad b=-3'),
E(r'\mathrm{count}=2:\ s=2-3=-1\Rightarrow0'),
E(r'\mathrm{count}=3:\ s=3-3=0\Rightarrow1,\quad\mathrm{count}=4:\ s=4-3=1\Rightarrow1'),
'Avoid: using T as the bias without changing its sign; treating score 0 as output 0 under our inclusive convention.'], 'WORKED ANSWER')]
for block in pages[-1]['blocks']:
 if isinstance(block,dict) and 'eq' in block:block['size']=21
rows=[]
for a,b in itertools.product([0,1],repeat=2):
 vals=dict(x=[a,b],AND=int(a+b-2>=0),OR=int(a+b-1>=0),NAND=int(-a-b+1.5>=0));assert vals['AND']==int(a and b);assert vals['OR']==int(a or b);assert vals['NAND']==int(not(a and b));rows.append(vals)
(out/'checks.json').write_text(json.dumps(rows,indent=2))
spec=dict(number=8,title='A neuron and logic gates',description='Score-by-score truth tables for AND, OR, NOT and majority; NAND practice.',source_short='Lecture 2 / PDF pp.39-40,54-55 / inclusive threshold H(0)=1',source='Lecture 2 - Logistic Regression + Neural Network.pdf, pages 39-40 and 54-55.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
