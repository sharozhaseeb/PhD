from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
from check_math import finite_difference
out=Path(__file__).resolve().parent.parent/'07-computation-graphs-chain-rule';out.mkdir(exist_ok=True)
def E(s):return {'eq':s}
def P(title,sub,blocks,stage='WORKED EXAMPLE'):return dict(title=title,subtitle=sub,blocks=blocks,stage=stage)
def graph(extension=False):
 fig,ax=plt.subplots(figsize=(8,2.4),layout='constrained');ax.set(xlim=(0,10),ylim=(0,4));ax.axis('off')
 nodes={'a':(1,3.5,'a = 5'),'b':(1,2,'b = 3'),'c':(1,.5,'c = 2'),'u':(3,1.2,'u = bc'),'v':(5,2.7,'v = a + u'),'J':(7,2.7,'J = 3v')}
 edges=[('a','v'),('b','u'),('c','u'),('u','v'),('v','J')]
 if extension:nodes.update({'q':(5,.5,'q = b squared'),'F':(9,1.7,'F = J + q')});edges += [('b','q'),('J','F'),('q','F')]
 for a,b in edges:
  x,y,_=nodes[a];xx,yy,_=nodes[b]
  if (a,b)==('b','q'):
   ax.plot([x+.55,2.2,4.1],[y,.1,.1],color='#006E73',lw=1.5)
   ax.annotate('',xy=(xx-.6,yy),xytext=(4.1,.1),arrowprops=dict(arrowstyle='->',color='#006E73',lw=1.5))
  else:ax.annotate('',xy=(xx-.55,yy),xytext=(x+.55,y),arrowprops=dict(arrowstyle='->',color='#006E73',lw=1.5))
 for x,y,label in nodes.values():ax.text(x,y,label,ha='center',va='center',fontsize=11,bbox=dict(boxstyle='round,pad=.4',facecolor='#edf3f7',edgecolor='#172B43'))
 fig.savefig(out/('branch.png' if extension else 'graph.png'),dpi=180);plt.close(fig)
graph();graph(True)
pages=[P('Break one expression into small steps','Lecture 2, page 27: a computation graph records which values depend on which.',[
E(r'J(a,b,c)=3(a+bc),\qquad a=5,\ b=3,\ c=2'),
{'image':'graph.png','width':650},
'Arrows show the forward flow of values. u and v are intermediate results. We compute values forward and sensitivities backward.']),
P('Forward pass: save every node value','Compute a node only after its inputs are known.',[
E(r'u=bc=3\times2=6'),
E(r'v=a+u=5+6=11'),
E(r'J=3v=3\times11=33'),
'Saving u and v avoids repeatedly expanding the full expression. Saving b and c matters because the backward calculation needs their values.',
'A node value answers "what number did we compute?" A derivative answers "how sensitive is the final result to a small change?"']),
P('Local derivatives: inspect one operation','Hold the other inputs fixed when differentiating an operation.',[
E(r'J=3v\Rightarrow\frac{\partial J}{\partial v}=3'),
E(r'v=a+u\Rightarrow\frac{\partial v}{\partial a}=1,\quad\frac{\partial v}{\partial u}=1'),
E(r'u=bc\Rightarrow\frac{\partial u}{\partial b}=c=2,\quad\frac{\partial u}{\partial c}=b=3'),
'An addition node passes sensitivity to each input unchanged: multiply by 1.',
'A multiplication node uses the OTHER input as its local derivative. Changing b affects u in proportion to c.']),
P('Backward pass: multiply along each path','The chain rule multiplies upstream sensitivity by the next local derivative.',[
E(r'\frac{\partial J}{\partial u}=\frac{\partial J}{\partial v}\frac{\partial v}{\partial u}=3(1)=3'),
E(r'\frac{\partial J}{\partial a}=\frac{\partial J}{\partial v}\frac{\partial v}{\partial a}=3(1)=3'),
E(r'\frac{\partial J}{\partial b}=\frac{\partial J}{\partial u}\frac{\partial u}{\partial b}=3(2)=6'),
E(r'\frac{\partial J}{\partial c}=\frac{\partial J}{\partial u}\frac{\partial u}{\partial c}=3(3)=9'),
'Near these inputs, increasing b by 0.01 increases J by about 6 times 0.01 = 0.06. The derivative and the node value u both happen to equal 6 here; they mean different things.']),
P('A shared input can affect two paths','Original study extension: add b squared to the lecture expression.',[
E(r'q=b^2=3^2=9,\qquad F=J+q=33+9=42'),
{'image':'branch.png','width':650},
'b now influences F through u and through q. Both effects matter. F and q are new extension nodes, not nodes from the lecture slide.']),
P('At a branch, add the path contributions','Changing b changes both J and q, so their effects on F add.',[
E(r'\frac{\partial F}{\partial b}=\frac{\partial F}{\partial J}\frac{\partial J}{\partial b}+\frac{\partial F}{\partial q}\frac{\partial q}{\partial b}'),
E(r'=(1)(6)+(1)(2b)=6+2(3)=12'),
E(r'\frac{\partial F}{\partial a}=1(3)=3,\qquad\frac{\partial F}{\partial c}=1(9)=9'),
'Multiply derivatives ALONG a path; add contributions FROM different paths. Do not discard one branch or multiply the two branch contributions.',
'We have computed sensitivities only. A parameter update would be a separate step using a learning rate.']),
P('Your turn: include a negative input','Use the lecture graph first, then add the branching extension.',[
E(r'a=1,\qquad b=2,\qquad c=-1'),
'1. Calculate u = bc, v = a + u, and J = 3v.',
'2. Calculate the three derivatives of J with respect to a, b and c.',
'3. Add q = b squared and F = J + q. Calculate F and its derivative with respect to b.',
'Show each local derivative and each path contribution, not just the final answers.'], 'INDEPENDENT PRACTICE'),
P('Practice answer: follow values and paths','The negative c makes the J path contribution for b negative.',[
E(r'u=2(-1)=-2,\quad v=1+(-2)=-1,\quad J=3(-1)=-3'),
E(r'\frac{\partial J}{\partial a}=3(1)=3,\quad\frac{\partial J}{\partial b}=3(1)(-1)=-3'),
E(r'\frac{\partial J}{\partial c}=3(1)(2)=6'),
E(r'q=2^2=4,\quad F=-3+4=1'),
E(r'\frac{\partial F}{\partial b}=1(-3)+1(2b)=-3+2(2)=1'),
'The branches partly cancel. Common mistakes: using b instead of c for the derivative of bc with respect to b, or confusing F = 1 with its derivative also being 1 here.'], 'WORKED ANSWER')]
checks=[]
for t in [np.array([5.,3.,2.]),np.array([1.,2.,-1.])]:
 a,b,c=t;checks.append(dict(inputs=t.tolist(),J=3*(a+b*c),F=3*(a+b*c)+b*b,J_gradient=finite_difference(lambda z:3*(z[0]+z[1]*z[2]),t,[3,3*c,3*b]),F_gradient=finite_difference(lambda z:3*(z[0]+z[1]*z[2])+z[1]**2,t,[3,3*c+2*b,3*b])))
(out/'checks.json').write_text(json.dumps(checks,indent=2))
spec=dict(number=7,title='Computation graphs and the chain rule',description='Lecture graph forward and backward, then a branching-path extension.',source_short='Lecture 2 / PDF p.27 / branching extension explicitly labelled',source='Lecture 2 - Logistic Regression + Neural Network.pdf, page 27; branching example is an original extension.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
