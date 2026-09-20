from pathlib import Path
import json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'36-gradient-clipping';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('Clip a gradient before using it in an update','Lecture 5 page 161 gives a ceiling on an individual positive derivative.',[
 E(r'g=(6,-8),\quad c=5,\quad w=(1,1),\quad\eta=0.1'),
 'g is the gradient vector supplied by backpropagation; w is the parameter vector. c is our threshold, called theta on the slide. We compare different clipping rules on the same original g.',
 E(r'w^{new}=w-\eta g_{used}'),
 'First choose and compute the clipped gradient. Then apply the parameter update. Clipping gradients does not mean clipping the values of the weights.',
 'The symmetric coordinate and global-norm rules below are labeled supporting extensions to the slide\'s one-sided ceiling.']),
P('Work the slide one-sided ceiling literally','Only a derivative greater than c is replaced by c.',[
 E(r'g_i>c\Longrightarrow g_i^{used}=c;\quad\mathrm{otherwise}\ g_i^{used}=g_i'),E(r'6>5\Longrightarrow g_1^{used}=5'),E(r'-8>5\ \mathrm{is\ false}\Longrightarrow g_2^{used}=-8'),E(r'g^{used}=(5,-8)'),E(r'w^{new}=(1-0.1(5),\ 1-0.1(-8))=(0.5,1.8)'),
 'A large negative derivative remains untouched. The next extension bounds both positive and negative components.']),
P('Symmetric coordinate clipping','Supporting extension: cap each component between -c and +c.',[
 E(r'g_i^{clip}=\max(-c,\min(g_i,c))'),E(r'g_1^{clip}=\max(-5,\min(6,5))=\max(-5,5)=5'),E(r'g_2^{clip}=\max(-5,\min(-8,5))=\max(-5,-8)=-5'),E(r'g^{clip}=(5,-5)'),E(r'w^{new}=(1-0.1(5),\ 1-0.1(-5))=(0.5,1.5)')]),
P('Global norm clipping: measure the vector length','Supporting extension: cap total Euclidean length instead of individual components.',[
 E(r'\|g\|_2=\sqrt{g_1^2+g_2^2}=\sqrt{6^2+(-8)^2}=\sqrt{100}=10'),
 'The Euclidean norm is the length of the vector, calculated from its squared components. For a nonzero vector, choose one shared scale factor.',
 E(r'a=\min(1,c/\|g\|_2)=\min(1,5/10)=0.5'),E(r'g^{clip}=a g=0.5(6,-8)=(3,-4)'),E(r'\|g^{clip}\|_2=\sqrt{3^2+(-4)^2}=5')]),
P('Use the norm-clipped vector in the update','Both components were scaled by the same factor .5.',[
 E(r'w_1^{new}=1-0.1(3)=0.7'),E(r'w_2^{new}=1-0.1(-4)=1.4'),E(r'w^{new}=(0.7,1.4)'),E(r'\|\Delta w\|_2=\eta\|g^{clip}\|_2=0.1(5)=0.5'),
 'For this plain gradient-descent update, a global clipped-gradient length at most c gives a displacement length at most eta*c. It is not a bound on the parameter vector itself.']),
P('A component cap is not a length cap','The coordinate-clipped vector still has length greater than5.',[
 E(r'\|(5,-5)\|_2=\sqrt{25+25}=\sqrt{50}\approx7.071>5'),E(r'\mathrm{global\ ratios}:\quad3/6=(-4)/(-8)=0.5'),E(r'\mathrm{coordinate\ ratios}:\quad5/6\ne(-5)/(-8)'),
 'Global clipping multiplies a nonzero vector by one positive number, preserving direction. Coordinate clipping can use different effective factors and change direction.',
 'A threshold5 means different things in these two rules: largest allowed component magnitude versus largest allowed total vector length.']),
P('See the directions and allowed regions','Arrows are gradients from the origin, not parameter paths.',[
 {'image':'clipping.png','width':650},
 'The square is the coordinate constraint; the circle is the norm constraint. The norm-clipped arrow lies on the same ray as the original vector.']),
P('Compare the resulting parameter states','Restart from w=(1,1) for each independent comparison.',[
 {'table':[['rule','gradient used','new parameters'],['none','(6,-8)','(.4,1.8)'],['slide positive ceiling','(5,-8)','(.5,1.8)'],['symmetric coordinate','(5,-5)','(.5,1.5)'],['global norm','(3,-4)','(.7,1.4)']],'widths':[250,200,230]},
 'The differences come from different rules, not arithmetic disagreements. Name the rule before computing it.',
 'These supplied gradients illustrate updates; without a declared objective they do not establish which update achieves the lowest loss.']),
P('Handle a small vector, a boundary and zero','A clipping operation should not amplify a vector already within its cap.',[
 E(r'g=(1,-2),\ c=5:\quad\|g\|_2=\sqrt{5}<5\Longrightarrow a=1'),E(r'g=(3,4),\ c=5:\quad\|g\|_2=5\Longrightarrow a=1'),E(r'g=(0,0)\Longrightarrow g^{clip}=(0,0)'),
 'For the zero vector, leave it unchanged directly; do not evaluate c/0. At the exact norm boundary, the shared scale is1. Symmetric coordinate clipping also leaves all these example components unchanged.']),
P('Your turn: a large negative component','Start from zero weights and compare all three rules.',[
 E(r'g=(-12,5),\quad c=6,\quad w=(0,0),\quad\eta=0.1'),
 'Calculate the slide one-sided ceiling, symmetric coordinate clipping and global-norm clipping. Show both components, the norm and shared scale where needed, then each parameter update.',
 'Explain why a component magnitude limit6 does not imply a total gradient length limit6.'],'INDEPENDENT PRACTICE'),
P('Answer: one-sided and symmetric coordinate rules','The slide ceiling only changes components greater than+6.',[
 E(r'-12\leq6,\quad5\leq6\Longrightarrow g_{slide}=(-12,5)'),E(r'w_{slide}^{new}=(0-0.1(-12),\ 0-0.1(5))=(1.2,-0.5)'),E(r'g_1^{coord}=\max(-6,\min(-12,6))=-6'),E(r'g_2^{coord}=\max(-6,\min(5,6))=5'),E(r'w_{coord}^{new}=(0-0.1(-6),\ 0-0.1(5))=(0.6,-0.5)')],'WORKED ANSWER'),
P('Answer: norm, scale and clipped components','One shared factor rescales both coordinates.',[
 E(r'\|g\|_2=\sqrt{(-12)^2+5^2}=\sqrt{144+25}=13'),E(r'a=\min(1,6/13)=6/13'),E(r'g_1^{norm}=(-12)(6/13)=-72/13\approx-5.538462'),E(r'g_2^{norm}=5(6/13)=30/13\approx2.307692'),E(r'\|g^{norm}\|_2=(6/13)(13)=6')],'WORKED ANSWER'),
P('Answer: the final norm-clipped update','Subtracting a negative first component increases the first weight.',[
 E(r'w_1^{new}=0-0.1(-72/13)=36/65\approx0.553846'),E(r'w_2^{new}=0-0.1(30/13)=-3/13\approx-0.230769'),E(r'\|(-6,5)\|_2=\sqrt{36+25}=\sqrt{61}\approx7.81025>6'),
 'The last line checks the symmetric coordinate result: each magnitude is at most6, but total length exceeds6. Global clipping caps the length itself.',
 'Common mistakes: ignoring a large negative component when a symmetric rule was requested, clipping weights instead of gradients, applying a different norm scale to each coordinate, or dividing by a zero norm.'],'WORKED ANSWER')]
fig,ax=plt.subplots(figsize=(9.5,3.6),layout='constrained');ax.add_patch(Circle((0,0),5,fill=False,color='#147d92',ls='--'));ax.add_patch(Rectangle((-5,-5),10,10,fill=False,color='#c86c28',ls=':'))
for g,c,l,pos in [((6,-8),'#777777','original (6,-8)',(1,-8.8)),((5,-5),'#c86c28','coordinate (5,-5)',(-4.8,-7)),((3,-4),'#147d92','norm (3,-4)',(-4.8,-3))]:
 ax.annotate('',xy=g,xytext=(0,0),arrowprops=dict(arrowstyle='->',color=c,lw=2));ax.text(*pos,l,color=c,fontsize=9,bbox=dict(facecolor='white',edgecolor='none',alpha=.9,pad=1))
ax.set(xlim=(-5.8,10),ylim=(-9.5,5.8),xlabel='gradient component 1',ylabel='gradient component 2');ax.set_aspect('equal');ax.axhline(0,color='#cccccc',lw=.7);ax.axvline(0,color='#cccccc',lw=.7);ax.grid(alpha=.15);fig.savefig(out/'clipping.png',dpi=180);plt.close(fig)
checks=[]
for g,c,w in [(np.array([6.,-8.]),5,np.ones(2)),(np.array([-12.,5.]),6,np.zeros(2))]:
 coord=np.clip(g,-c,c);norm=g*min(1,c/np.linalg.norm(g));slide=np.minimum(g,c)
 assert abs(np.linalg.norm(norm)-c)<1e-12 and abs(np.linalg.det(np.array([g,norm])))<1e-12
 checks.append(dict(g=g.tolist(),threshold=c,slide=slide.tolist(),coordinate=coord.tolist(),norm=norm.tolist(),updated={n:(w-.1*v).tolist() for n,v in [('slide',slide),('coordinate',coord),('norm',norm)]}))
(out/'checks.json').write_text(json.dumps(checks,indent=2))
spec=dict(number=36,title='Coordinate and global-norm gradient clipping',description='Work the slide ceiling and two signed-gradient extensions, compare vector directions and updates, handle zero, and solve fresh clipping practice.',source_short='Lecture 5 PDF p.161 / symmetric and norm rules are supporting extensions',source='Lecture 5 PDF page 161 gives the one-sided positive ceiling. Symmetric coordinate and global L2-norm clipping are explicitly labeled supporting extensions; numerical-practice.md N6.9.',pages=pages)
for p in pages:
 for key in ['title','subtitle']:p[key]=p[key].replace('than5','than 5').replace('than+6','than +6')
 for i,b in enumerate(p['blocks']):
  if isinstance(b,str):
   for a,z in [('page 161','page 161'),('threshold5','threshold 5'),('scale is1','scale is 1'),('limit6','limit 6'),('most6','most 6'),('exceeds6','exceeds 6')]:b=b.replace(a,z)
   p['blocks'][i]=b
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
