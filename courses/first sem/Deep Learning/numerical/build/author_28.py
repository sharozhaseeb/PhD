from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'28-curvature-approximations';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='CONCEPTUAL COMPANION'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('Why approximate curvature?','Lecture4 PDF page53 names methods and their central ideas, not full update derivations.',[
 'Newton uses a Hessian to account for curvature. A dense Hessian can be expensive to calculate and store, and unsuitable curvature can make its correction unhelpful.',
 E(r'D\ \mathrm{parameters}\quad\Longrightarrow\quad D\times D\ \mathrm{Hessian\ entries}'),
 E(r'D=1000\quad\Longrightarrow\quad1000^2=1{,}000{,}000\ \mathrm{entries}'),
 'The lecture introduces BFGS, limited-memory BFGS, and Levenberg-Marquardt as approaches that estimate or modify curvature.',
 'This is the roadmap conceptual companion. The small arithmetic illustrations below explain those ideas; they are explicitly not complete BFGS or LM algorithm iterations.']),
 P('BFGS learns from changes between iterates','Compare how far parameters moved with how much their gradients changed.',[
 'BFGS maintains an approximate Hessian or its inverse. Parameter-change and gradient-change information helps update this curvature approximation over successive steps.',
 'Picture moving along a surface: if a small parameter change causes a large gradient change, that direction has substantial curvature. If the gradient changes little, curvature is weaker.',
 {'image':'bfgs.png','width':655},
 'The lecture describes estimating the Hessian from finite differences. The next scalar example illustrates the slope-change idea only; multidimensional BFGS uses a structured matrix update.']),
 P('Optional illustration: curvature from two gradients','This scalar secant calculation is not the full BFGS update rule.',[
 E(r'E(w)=1.5w^2,\qquad g(w)=3w'),
 E(r'w_{old}=1,\quad g_{old}=3(1)=3'),
 E(r'w_{new}=1.2,\quad g_{new}=3(1.2)=3.6'),
 E(r'\Delta w=1.2-1=0.2,\quad\Delta g=3.6-3=0.6'),
 E(r'\mathrm{curvature\ estimate}=\frac{\Delta g}{\Delta w}=\frac{0.6}{0.2}=3'),
 'The exact second derivative is also 3. For this quadratic, any two distinct parameter points give the same slope-change ratio. A general curved function need not have constant curvature.'],'OPTIONAL ARITHMETIC'),
 P('L-BFGS limits the stored history','L means limited memory: retain a small number of recent change pairs.',[
 'Instead of storing a full dense curvature matrix, L-BFGS uses recent parameter-change and gradient-change vectors to construct the needed curvature action.',
 E(r'D=1000,\quad m=5\ \mathrm{recent\ pairs}'),
 E(r'2mD=2(5)(1000)=10{,}000\ \mathrm{scalar\ entries}'),
 E(r'D^2=1{,}000{,}000,\qquad\frac{D^2}{2mD}=100'),
 'Each pair has two vectors of length D. This illustrative history count is 100 times smaller than the dense-matrix entry count. It excludes other state and computational overhead.',
 'Limited memory describes stored information; it does not mean the exact Hessian was computed and then simply discarded.']),
 P('Levenberg-Marquardt starts from residual slopes','The usual context is nonlinear least squares: a sum of squared residuals.',[
 'A residual is prediction minus target. A Jacobian is the table of residual derivatives: rows identify residuals and columns identify parameters.',
 E(r'r(w)=2w-3\quad\Longrightarrow\quad\frac{dr}{dw}=2'),
 'Here the one-entry Jacobian is 2. With many residuals and parameters, the same idea gives a rectangular table of slopes.',
 {'image':'lm.png','width':620},
 'The lecture describes estimating curvature from Jacobians and adding diagonal loading. The damping amount affects the correction. This diagram is a conceptual overview, not a complete LM iteration.']),
 P('Optional illustration: repair zero curvature','Add 0.5 to diagonal entries only; leave off-diagonal entries unchanged.',[
 {'table':[['row','original matrix A','loaded matrix'],['1','(1, 1)','(1.5, 1)'],['2','(1, 1)','(1, 1.5)']],'widths':[80,280,320]},
 E(r'A(1,-1)=(0,0)=0(1,-1)'),
 E(r'(A+0.5I)(1,-1)=(0.5,-0.5)=0.5(1,-1)'),
 E(r'(A+0.5I)(1,1)=(2.5,2.5)=2.5(1,1)'),
 'The original eigenvalues are 0 and 2; after loading they are 0.5 and 2.5. The zero-curvature direction now has positive curvature.',
 'I is the identity matrix. This illustrates diagonal loading only; it does not supply all residual, damping-selection or acceptance steps of LM.'],'OPTIONAL ARITHMETIC'),
 P('Compare the ideas without conflating the methods','Approximate curvature can be represented and used in different ways.',[
 {'table':[['method','information emphasized','central idea'],['BFGS','parameter/gradient changes','update curvature approximation'],['L-BFGS','recent change pairs','limit matrix-history storage'],['LM','residual Jacobian','damp least-squares correction']],'widths':[110,280,290],'size':13},
 'BFGS can store a Hessian approximation or inverse approximation. L-BFGS represents the needed action using recent history rather than a full dense matrix.',
 'LM exploits least-squares residual structure and damping. It is not another name for BFGS, and the diagonal-loading illustration alone is not the full method.',
 'The lecture does not provide full update derivations for these methods. Be able to explain what information they use and what difficulty they address.']),
 P('Your turn: numerical intuition and concept checks','Use the illustrations to explain the mechanisms in your own words.',[
 E(r'g(w)=4w,\quad w_{old}=1,\quad w_{new}=1.25'),
 'Calculate both gradients, their difference, the parameter difference, and the scalar curvature estimate.',
 E(r'D=100,\quad m=3'),
 'Count the entries in a dense Hessian and in three stored change pairs. State what the comparison excludes.',
 'Which method limits change-pair history? What does a Jacobian row describe? Does adding to the diagonal mean adding to every matrix entry? Why is a secant ratio not a complete multidimensional BFGS step?'],'INDEPENDENT PRACTICE'),
 P('Practice: substitute every arithmetic quantity','The scalar estimate uses a ratio of two changes.',[
 E(r'g_{old}=4(1)=4,\quad g_{new}=4(1.25)=5'),
 E(r'\Delta g=5-4=1,\quad\Delta w=1.25-1=0.25'),
 E(r'\mathrm{curvature\ estimate}=1/0.25=4'),
 E(r'\mathrm{dense}=100^2=10{,}000\ \mathrm{entries}'),
 E(r'\mathrm{history}=2(3)(100)=600\ \mathrm{entries}'),
 'This compares only dense-matrix entries with stored history-vector entries. It does not count all auxiliary state, working memory, or runtime cost.'],'WORKED ANSWER'),
 P('Practice: complete the conceptual explanation','Correct names are useful only when you can explain their information flow.',[
 'L-BFGS keeps a limited recent history of parameter-change and gradient-change pairs. BFGS more generally updates a curvature approximation using such changes.',
 'A Jacobian row lists the derivatives of one residual with respect to every parameter. In r(w)=2w-3, the one residual slope is 2.',
 'Diagonal loading changes only diagonal entries. In the worked matrix, the two off-diagonal 1 values stayed 1.',
 'The scalar ratio illustrates one-direction curvature. Full multidimensional BFGS requires a structured matrix update and other algorithm choices, so that ratio is not the complete algorithm.',
 'When studying a supplied formula, work its numbers carefully. When a slide supplies only a conceptual overview, distinguish the stated mechanism from optional deeper formulas.'],'WORKED ANSWER')]
def flow(name,labels):
 fig,ax=plt.subplots(figsize=(10,1.65),layout='constrained');ax.axis('off');ax.set(xlim=(-.4,len(labels)-.6),ylim=(-.5,.5))
 for i,lab in enumerate(labels):
  ax.text(i,0,lab,ha='center',va='center',fontsize=11,bbox=dict(boxstyle='round',facecolor='#e6f1f2',edgecolor='#006E73'))
  if i<len(labels)-1:ax.annotate('',xy=(i+.72,0),xytext=(i+.28,0),arrowprops=dict(arrowstyle='->',color='#006E73',lw=2))
 fig.savefig(out/name,dpi=180);plt.close(fig)
flow('bfgs.png',['parameter\nchange','gradient\nchange','curvature\napproximation'])
flow('lm.png',['residual\nslopes','Jacobian-based\ncurvature','diagonal\nloading','solve\ncorrection'])
assert np.allclose(np.linalg.eigvalsh([[1,1],[1,1]]),[0,2]);assert np.allclose(np.linalg.eigvalsh([[1.5,1],[1,1.5]]),[.5,2.5])
(out/'checks.json').write_text(json.dumps(dict(secant_main=3,secant_practice=4,dense_main=1000000,history_main=10000,dense_practice=10000,history_practice=600,loaded_eigenvalues=[.5,2.5]),indent=2))
spec=dict(number=28,title='Curvature approximations: conceptual companion',description='Understand BFGS, L-BFGS and Levenberg-Marquardt using diagrams and clearly labeled small arithmetic illustrations, with practice answers.',source_short='Lecture4 PDF p.50-53 / conceptual overview; optional arithmetic labeled',source='Lecture4 PDF pages50-53, especially page53 overview of BFGS/L-BFGS and Levenberg-Marquardt. Secant, memory-count and loading arithmetic are explanatory extensions, not full update algorithms.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
