from pathlib import Path
import json
from fractions import Fraction as F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'27-momentum-nesterov';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
def trace(a,w,beta,method):
 a=F(str(a));w=F(str(w));b=F(str(beta));eta=F('.1');v=F(0);rows=[]
 for k in range(2):
  q=w+b*v if method=='Nesterov' else w;g=a*q;vn=-eta*g if method=='GD' else b*v-eta*g;wn=w+vn
  rows.append({key:float(val) for key,val in dict(k=k,w=w,v=v,q=q,g=g,vnew=vn,wnew=wn,loss=a*wn*wn/2).items()});w=wn;v=vn
 return rows
A={m:trace(1,2,.9,m) for m in ['GD','Momentum','Nesterov']};B={m:trace(2,1,.5,m) for m in A}
pages=[P('Momentum carries a signed displacement forward','The state is a parameter w plus a stored previous displacement v.',[
 E(r'E(w)=\frac{1}{2}w^2,\quad g(w)=w,\quad w_0=2,\quad v_0=0'),
 E(r'\eta=0.1,\quad\beta=0.9'),
 'Eta scales the current gradient. Beta retains 90 percent of the previous signed displacement, not 90 percent of an averaged gradient.',
 E(r'v_{k+1}=\beta v_k-\eta g(w_k),\qquad w_{k+1}=w_k+v_{k+1}'),
 'A negative v moves the parameter downward when added. This convention matches the lecture signed Delta-W displacement. Do not add an extra (1-beta) factor to the gradient term.']),
 P('Nesterov changes where the gradient is evaluated','The temporary look-ahead anticipates the movement from stored displacement.',[
 E(r'q_k=w_k+\beta v_k'),
 E(r'v_{k+1}=\beta v_k-\eta g(q_k),\qquad w_{k+1}=w_k+v_{k+1}'),
 'q is a temporary gradient-evaluation point. It is not the stored parameter and is not an additional completed training update.',
 'Lecture4 PDF page90 writes the signed displacement as Delta-W. The subscript k on v and w means the displacement and parameter after k updates.',
 E(r'w_{k+1}=q_k-\eta g(q_k)'),
 'This equivalent expression already includes beta times the old displacement through q. Do not add that contribution again.']),
 P('Plain gradient descent gives a useful baseline','Reset to w0=2 and take two updates without stored displacement.',[
 E(r'g_0=2,\qquad w_1=2-0.1(2)=1.8'),
 E(r'g_1=1.8,\qquad w_2=1.8-0.1(1.8)=1.62'),
 E(r'E(w_2)=\frac{1}{2}(1.62)^2=1.3122'),
 'The next pages restart both momentum methods from the same original w0=2,v0=0. Their updates are alternatives to this baseline.'])]
def worked(rows,beta,a,method,practice=False):
 ps=[];stage='WORKED ANSWER' if practice else 'WORKED EXAMPLE'
 for r in rows:
  k=int(r['k']);blocks=[E(rf'w_{k}={r["w"]:g},\quad v_{k}={r["v"]:g}')]
  if method=='Nesterov':blocks.append(E(rf'q_{k}={r["w"]:g}+{beta:g}({r["v"]:g})={r["q"]:g}'))
  blocks.extend([E(rf'g_{k}={a:g}({r["q"]:g})={r["g"]:g}'),
   E(rf'v_{{{k+1}}}={beta:g}({r["v"]:g})-0.1({r["g"]:g})={r["vnew"]:g}'),
   E(rf'w_{{{k+1}}}={r["w"]:g}+({r["vnew"]:g})={r["wnew"]:g}'),
   'The gradient uses the temporary q shown above; the final parameter uses current w plus the new displacement.' if method=='Nesterov' else 'The gradient uses current w. Keep the new displacement as state for the next update.'])
  ps.append(P(('Practice: ' if practice else '')+f'{method}, update {k+1}','Compute the gradient location first, then the new displacement, then the parameter.',blocks,stage))
 return ps
pages+=worked(A['Momentum'],.9,1,'Momentum')+worked(A['Nesterov'],.9,1,'Nesterov')
pages+=[P('Trace Nesterov second-step dependencies','This picture is a calculation flow; q is temporary.',[
 {'image':'lookahead.png','width':655},
 E(r'w_2=q_1-0.1g(q_1)=1.62-0.1(1.62)=1.458'),
 E(r'v_2=w_2-w_1=1.458-1.8=-0.342'),
 'Using q1 plus the entire new v2 would count the old momentum contribution twice. Use either w1+v2 or q1 minus the fresh gradient correction.']),
 P('Compare all second-step states','With zero initial displacement, both momentum methods share the first step.',[
 {'table':[['method','gradient point','second gradient','new v','new w'],['GD','1.8','1.8','not stored','1.62'],['Momentum','1.8','1.8','-0.36','1.44'],['Nesterov','1.62','1.62','-0.342','1.458']],'widths':[145,145,155,125,110]},
 E(r'E_{GD}=1.3122,\quad E_M=\frac{1.44^2}{2}=1.0368'),
 E(r'E_N=\frac{1.458^2}{2}=1.062882'),
 'This particular two-step example gives these losses. It does not establish that one method always wins. Changing curvature, rate, momentum coefficient or initial state can change the comparison.']),
 P('Your turn: new curvature and momentum coefficient','Reset all three methods before comparing them.',[
 E(r'E(w)=w^2,\quad w_0=1,\quad v_0=0,\quad\eta=0.1,\quad\beta=0.5'),
 'Calculate two updates of plain gradient descent, momentum and Nesterov. Record every gradient-evaluation point and both momentum displacements.',
 'Explain why the derivative is now 2w instead of w. In the Nesterov second step, distinguish temporary q from stored w.',
 'Try the calculation before reading the next complete answer pages.'],'INDEPENDENT PRACTICE'),
 P('Practice: derivative and gradient-descent baseline','The missing factor 1/2 changes the derivative.',[
 E(r'g(w)=\frac{d(w^2)}{dw}=2w'),
 E(r'g_0=2(1)=2,\quad w_1=1-0.1(2)=0.8'),
 E(r'g_1=2(0.8)=1.6,\quad w_2=0.8-0.1(1.6)=0.64'),
 E(r'E(w_2)=0.64^2=0.4096'),
 'Both momentum methods also start at w0=1,v0=0. Their first update will match this first step because the old displacement is zero.'],'WORKED ANSWER')]
pages+=worked(B['Momentum'],.5,2,'Momentum',True)+worked(B['Nesterov'],.5,2,'Nesterov',True)
pages.append(P('Practice checkpoint and common mistakes','The state you carry changes the next update.',[
 {'table':[['method','second gradient point','second gradient','final w'],['GD','0.8','1.6','0.64'],['Momentum','0.8','1.6','0.54'],['Nesterov','0.7','1.4','0.56']],'widths':[145,245,170,120]},
 E(r'E_M=0.54^2=0.2916,\qquad E_N=0.56^2=0.3136'),
 'Do not reset velocity after every step, use current-w gradient for Nesterov, add the old momentum twice, or mix this displacement convention with a gradient-average formula containing (1-beta).',
 'Changing the definition of stored state can give an equivalent algorithm only with the corresponding sign and learning-rate conversion. Match the stated convention before substituting numbers.'],'WORKED ANSWER'))
fig,ax=plt.subplots(figsize=(10,2.2),layout='constrained');ax.axis('off');ax.set(xlim=(-.3,2.3),ylim=(-.6,.65))
for x,txt in [(0,'current stored w1\n1.8'),(1,'temporary q1\n1.62'),(2,'new stored w2\n1.458')]:ax.text(x,0,txt,ha='center',va='center',fontsize=12,bbox=dict(boxstyle='round',facecolor='#e6f1f2',edgecolor='#006E73'))
for x,label in [(0,'add beta*v1 = -0.18'),(1,'subtract eta*g(q1) = 0.162')]:ax.annotate('',xy=(x+.76,0),xytext=(x+.25,0),arrowprops=dict(arrowstyle='->',lw=2,color='#006E73'));ax.text(x+.5,.42,label,ha='center',fontsize=10)
fig.savefig(out/'lookahead.png',dpi=180);plt.close(fig)
assert [A[m][-1]['wnew'] for m in A]==[1.62,1.44,1.458]
assert [B[m][-1]['wnew'] for m in B]==[.64,.54,.56]
(out/'checks.json').write_text(json.dumps(dict(main=A,practice=B,arithmetic='exact fractions before display'),indent=2))
spec=dict(number=27,title='Momentum and Nesterov, step by step',description='Track signed displacement and the exact gradient location through two updates, compare plain GD, and solve a fresh changed-curvature practice.',source_short='Lecture4 PDF p.75-93; Nesterov formula p.90 / N4.6',source='Lecture4 PDF pages75-93, especially page90 signed Delta-W Nesterov equation. v denotes signed parameter displacement. numerical-practice.md N4.6.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
