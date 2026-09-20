from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'24-newton-method';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('Newton uses slope and curvature together','Start with one parameter, where the Hessian is just a second derivative.',[
 E(r'E(w)=2(w-1)^2,\quad g=4(w-1),\quad H=4'),
 E(r'w_0=3:\quad g_0=8,\qquad w_{new}=3-\frac{8}{4}=1'),
 E(r'E(3)=8,\qquad E(1)=0'),
 'The full Newton correction divides slope by curvature. In this exact positive-curvature quadratic, it lands at the minimum in one step.',
 E(r'\mathrm{GD\ at}\ \eta_G=0.1:\quad w_{new}=3-0.1(8)=2.2'),
 'Gradient descent uses a chosen rate times the slope. Newton adjusts the correction using curvature.']),
 P('Map the lecture formula to a linear system','Evaluate the gradient and Hessian at the same original parameter vector.',[
 E(r'w_{new}=w-\eta_NH^{-1}g'),
 'Lecture4 PDF page50 includes a rate eta. Here eta_N=1 means a full Newton step. We use g as a column gradient; tuples below list its components.',
 E(r'Hs=g,\qquad w_{new}=w-s\quad(\eta_N=1)'),
 'The correction s equals H-inverse times g. The actual displacement is -s. Some notes instead name the signed displacement Delta and solve H Delta = -g.',
 E(r'H\Delta=-g,\quad\Delta=-s,\quad w_{new}=w+\Delta'),
 'Both conventions give the same update. Solving the system avoids explicitly forming the inverse.']),
 P('Compute the mixed-quadratic ingredients','Reuse the Lesson21 function and the same start for both methods.',[
 E(r'E(x,y)=1.5x^2+xy+1.5y^2,\quad w_0=(2,0)'),
 E(r'g=(3x+y,\ x+3y),\quad g_0=(6,2)'),
 {'table':[['Hessian row','column x','column y'],['differentiate 3x+y','3','1'],['differentiate x+3y','1','3']],'widths':[330,175,175]},
 E(r'E(2,0)=1.5(2)^2+2(0)+1.5(0)^2=6'),
 'Thus H has rows (3,1) and (1,3). Its positive eigenvalues 2 and 4 were derived in Lesson21.']),
 P('Solve for the Newton correction by elimination','The matrix equation Hs=g becomes two ordinary equations.',[
 E(r'3s_x+s_y=6,\qquad s_x+3s_y=2'),
 E(r's_y=6-3s_x'),
 E(r's_x+3(6-3s_x)=2\Rightarrow -8s_x=-16\Rightarrow s_x=2'),
 E(r's_y=6-3(2)=0'),
 E(r'w_{new}=(2,0)-(2,0)=(0,0),\quad E_{new}=0'),
 'Check the solution: 3(2)+0=6 and 2+3(0)=2. The correction is (2,0), while the displacement is (-2,0).']),
 P('Optional check: the two-by-two inverse','The linear solve is sufficient; this shows why the inverse formula agrees.',[
 'For rows (a,b) and (c,d), the inverse has rows (d,-b) and (-c,a), all divided by ad-bc. This requires a nonzero determinant.',
 E(r'\det H=3(3)-1(1)=8'),
 'Therefore H inverse has rows (3,-1)/8 and (-1,3)/8.',
 E(r's_x=\frac{3(6)-1(2)}{8}=\frac{16}{8}=2'),
 E(r's_y=\frac{-1(6)+3(2)}{8}=\frac{0}{8}=0'),
 'These are exactly the correction components found by elimination. Do not invert each matrix entry separately.']),
 P('Compare gradient descent from the same start','Use eta_G=0.1; this is an alternative update, not an extra Newton step.',[
 E(r'w_{GD}=(2,0)-0.1(6,2)=(1.4,-0.2)'),
 E(r'E(1.4,-0.2)=1.5(1.4)^2+(1.4)(-0.2)+1.5(-0.2)^2'),
 E(r'=2.94-0.28+0.06=2.72'),
 {'table':[['method','starting loss','new point','new loss'],['GD rate0.1','6','(1.4, -0.2)','2.72'],['full Newton','6','(0, 0)','0']],'widths':[180,160,190,150]},
 'Both lower this quadratic. Their directions differ because Newton accounts for the mixed curvature rather than multiplying every gradient coordinate by the same scalar.']),
 P('Two alternative arrows from one starting point','Contours connect points with equal loss.',[
 {'image':'paths.png','width':610},
 'The arrows share the original point (2,0). The gradient-descent point is not an intermediate stage of the Newton calculation.']),
 P('Why the exact quadratic finishes in one full step','The local quadratic model is the entire function in this special case.',[
 'For an exact positive-definite quadratic and an exact solve, a full Newton step reaches the unique minimum from any starting point. General neural-network losses do not have this guarantee.',
 E(r'\eta_N=0.5:\quad w_{new}=(2,0)-0.5(2,0)=(1,0)'),
 E(r'E(1,0)=1.5(1)^2=1.5'),
 'A damped Newton step keeps the lecture rate below one here. It moves only partway along the correction, so the one-step result no longer applies.',
 'The Hessian can also be expensive, singular or indefinite. These issues are separate from the arithmetic of a successful small quadratic example.']),
 P('An invertible Hessian can lead to a saddle','Newton seeks a stationary point; that point need not be a minimum.',[
 E(r'S(x,y)=\frac{x^2-y^2}{2},\quad w_0=(0,1),\quad g_0=(0,-1)'),
 'H is diagonal (1,-1), which is invertible but indefinite. Solve Hs=g: sx=0 and -sy=-1, so s=(0,1).',
 E(r'w_{new}=(0,1)-(0,1)=(0,0)'),
 E(r'S_{old}=-0.5,\qquad S_{new}=0'),
 'The loss increases and the origin is a saddle. Reaching the exact stationary point in one step is not the same as reaching a minimum.']),
 P('A singular Hessian makes the raw formula undefined','Even a true minimum may have zero curvature at that point.',[
 E(r'T(w)=w^4,\quad g(w)=4w^3,\quad H(w)=12w^2'),
 E(r'w=0:\quad g=0,\quad H=0,\quad g/H=0/0\ \mathrm{undefined}'),
 'The origin is a minimum because w-to-the-fourth is nonnegative. But the raw Newton division cannot be evaluated there. Do not call 0/0 a zero correction.',
 'A practical method needs an appropriate stopping test or a modified step when the curvature system cannot be solved.']),
 P('Your turn: a fresh mixed quadratic','Reset to the stated starting point for each alternative method.',[
 E(r'Q(x,y)=2x^2+xy+2y^2,\quad w_0=(1,-1)'),
 'Calculate the gradient and Hessian. Find the initial loss. Solve Hs=g by elimination and calculate a full Newton step and its loss.',
 'Separately take one gradient-descent step with rate 0.1 from the original start and calculate its loss. Explain correction s versus signed displacement -s.'],'INDEPENDENT PRACTICE'),
 P('Practice: ingredients and elimination','Differentiate, substitute the start, then solve the two equations.',[
 E(r'g=(4x+y,x+4y)\Rightarrow g_0=(3,-3)'),
 'H has rows (4,1) and (1,4), from differentiating those gradient components.',
 E(r'Q(1,-1)=2-1+2=3'),
 E(r'4s_x+s_y=3,\quad s_x+4s_y=-3'),
 E(r's_y=3-4s_x\Rightarrow s_x+4(3-4s_x)=-3'),
 E(r'-15s_x=-15\Rightarrow s_x=1,\quad s_y=3-4=-1')],'WORKED ANSWER'),
 P('Practice: both updates and both losses','The full Newton correction is s=(1,-1); its displacement is (-1,1).',[
 E(r'w_N=(1,-1)-(1,-1)=(0,0),\quad Q_N=0'),
 E(r'w_G=(1,-1)-0.1(3,-3)=(0.7,-0.7)'),
 E(r'Q_G=2(0.7)^2+(0.7)(-0.7)+2(-0.7)^2'),
 E(r'=0.98-0.49+0.98=1.47'),
 'Common errors: using H inverse entry-by-entry, evaluating H and g at different points, adding s when it was defined by Hs=g, dropping the lecture rate without declaring a full step, or assuming invertible means positive definite.'],'WORKED ANSWER')]
fig,ax=plt.subplots(figsize=(8.7,3.5),layout='constrained');xx,yy=np.meshgrid(np.linspace(-.6,2.5,200),np.linspace(-1.1,1,200));zz=1.5*xx*xx+xx*yy+1.5*yy*yy
ax.contour(xx,yy,zz,levels=[.2,.5,1,2,3,4,6],colors='#bacbd2');ax.scatter([2,1.4,0],[0,-.2,0],c=['black','#BD6A24','#006E73'])
for end,color in [((1.4,-.2),'#BD6A24'),((0,0),'#006E73')]:ax.annotate('',xy=end,xytext=(2,0),arrowprops=dict(arrowstyle='->',lw=2,color=color))
ax.text(2,.13,'shared start (2,0)',ha='right',fontsize=10);ax.text(1.2,-.42,'GD (1.4,-0.2)',color='#BD6A24',fontsize=10);ax.text(-.4,.15,'Newton (0,0)',color='#006E73',fontsize=10);ax.set(xlabel='parameter x',ylabel='parameter y');fig.savefig(out/'paths.png',dpi=180);plt.close(fig)
checks=[]
for H,w in [(np.array([[3.,1.],[1.,3.]]),np.array([2.,0.])),(np.array([[4.,1.],[1.,4.]]),np.array([1.,-1.]))]:
 g=H@w;s=np.linalg.solve(H,g);n=w-s;gd=w-.1*g
 assert np.allclose(n,[0,0]);assert np.allclose(H@s,g)
 checks.append(dict(H=H.tolist(),g=g.tolist(),correction=s.tolist(),old_loss=float(w@H@w/2),newton_loss=float(n@H@n/2),gd_loss=float(gd@H@gd/2)))
(out/'checks.json').write_text(json.dumps(checks,indent=2))
spec=dict(number=24,title='Newton method and curvature correction',description='Solve a full Newton correction, compare gradient descent from the same point, and work a fresh practice with saddle/singular counterexamples.',source_short='Lecture4 PDF p.33-36,47-52 / full Newton eta=1 / N4.3',source='Lecture4 PDF pages33-36: scalar curvature; pages47-52: normalized multivariate update and Hessian issues, eta included on page50. numerical-practice.md N4.3.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
