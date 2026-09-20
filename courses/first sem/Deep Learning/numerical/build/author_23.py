from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'23-saturation-loss-choice';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':21}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
sig=lambda z:1/(1+math.exp(-z))
def calc(p,t):
 z=math.log(p/(1-p));ds=(p-t)*p*(1-p);db=p-t;w=z/2
 ans=dict(p=p,t=t,z=z,w=w,slope=p*(1-p),half=.5*(p-t)**2,bce=-t*math.log(p)-(1-t)*math.log(1-p))
 for name,d in [('half',ds),('bce',db)]:
  wn=w-.1*(2*d);bn=-.1*d;zn=2*wn+bn
  ans[name+'_step']=dict(delta=d,gw=2*d,gb=d,w=wn,b=bn,z=zn,p=sig(zn))
 return ans
A=calc(.01,1);B=calc(.9,0)
pages=[P('The same wrong prediction, two loss functions','A single sigmoid output predicts p=0.01 while the known target is t=1.',[
 E(r'p=\sigma(z)=\frac{1}{1+e^{-z}},\qquad z=wx+b'),
 E(r'x=2,\quad b=0,\quad z=\ln\frac{0.01}{0.99}=-4.59511985'),
 E(r'w=z/2=-2.29755993'),
 'The probability is close to zero, so this target-1 prediction is confidently wrong. Sigmoid saturation means the output changes very little when its input z changes a little.',
 'Lecture4 motivates the saturation problem using squared divergence. This is a separate study example using the handout binary target convention t in {0,1}.']),
 P('State the loss scaling before differentiating','The lecture PDF page12 uses the unhalved square (y-d)-squared.',[
 E(r'L_{half}=\frac{1}{2}(p-t)^2,\qquad L_{BCE}=-[t\ln p+(1-t)\ln(1-p)]'),
 E(r'L_{half}=\frac{1}{2}(0.01-1)^2=0.49005'),
 E(r'L_{BCE}=-\ln(0.01)=4.60517019'),
 'Our half-square convention removes the factor 2 from its derivative. For the lecture unhalved square, double this loss and its gradients: loss 0.9801.',
 'These loss values use different scales and definitions. A smaller numerical loss across two different formulas does not by itself mean a better prediction. Compare their gradient responses at the same prediction.']),
 P('Half-squared error keeps the small sigmoid slope','Use the chain rule through p before reaching z.',[
 E(r'\frac{dL_{half}}{dp}=p-t=0.01-1=-0.99'),
 E(r'\frac{dp}{dz}=p(1-p)=0.01(0.99)=0.0099'),
 E(r'\frac{dL_{half}}{dz}=\frac{dL_{half}}{dp}\frac{dp}{dz}'),
 E(r'=(-0.99)(0.0099)=-0.009801'),
 'The prediction is badly wrong, yet the derivative with respect to z is small because the sigmoid slope is small. For the unhalved square, the derivative is twice this: -0.019602.']),
 P('BCE cancels the sigmoid factor','This simplification is specific to sigmoid output with binary cross-entropy.',[
 E(r'\frac{dL_{BCE}}{dp}=-\frac{t}{p}+\frac{1-t}{1-p}'),
 E(r'\frac{dL_{BCE}}{dz}=\left(-\frac{t}{p}+\frac{1-t}{1-p}\right)p(1-p)'),
 E(r'=-t(1-p)+(1-t)p=p-t'),
 E(r't=1:\quad(-1/0.01)(0.0099)=(-100)(0.0099)=-0.99'),
 'Cancellation assumes 0<p<1, as holds for finite sigmoid logits in exact arithmetic. Do not multiply the simplified p-t by another sigmoid slope.']),
 P('Translate each output derivative into parameters','Let delta = dL/dz. The weight source is x=2; the bias source is 1.',[
 E(r'\frac{dL}{dw}=\frac{dL}{dz}\frac{dz}{dw}=\delta x,\qquad\frac{dL}{db}=\delta'),
 E(r'\mathrm{half:}\quad g_w=(-0.009801)(2)=-0.019602,\quad g_b=-0.009801'),
 E(r'\mathrm{BCE:}\quad g_w=(-0.99)(2)=-1.98,\quad g_b=-0.99'),
 E(r'\frac{|\delta_{BCE}|}{|\delta_{half}|}=\frac{0.99}{0.009801}\approx101.01'),
 'Subtracting either gradient increases z and the target-1 probability. Their magnitudes differ because the two losses weight this error differently.'])]
def steps(a,practice=False):
 ps=[];stage='WORKED ANSWER' if practice else 'WORKED EXAMPLE'
 for name,title in [('half','half-squared error'),('bce','BCE')]:
  s=a[name+'_step']
  ps.append(P(('Practice: ' if practice else '')+f'one step with {title}','Update both w and b from the same original state, using eta=0.1.',[
   E(rf'w_{{new}}={a["w"]:.8f}-0.1({s["gw"]:.8f})={s["w"]:.8f}'),
   E(rf'b_{{new}}=0-0.1({s["gb"]:.8f})={s["b"]:.8f}'),
   E(rf'z_{{new}}=2({s["w"]:.8f})+({s["b"]:.8f})={s["z"]:.8f}'),
   E(rf'p_{{new}}=\frac{{1}}{{1+e^{{-({s["z"]:.8f})}}}}={s["p"]:.8f}'),
   'The updated prediction uses both changed parameters. The comparison starts from the same original weight and bias for each loss; these are alternative steps, not consecutive steps.'],stage))
 return ps
pages+=steps(A)
pages+=[P('Why the logit change contains x-squared','Combine the updates only after you understand both parameter contributions.',[
 E(r'z_{new}=(w-\eta\delta x)x+(b-\eta\delta)'),
 E(r'=wx+b-\eta\delta(x^2+1)=z-\eta\delta(x^2+1)'),
 E(r'x=2:\quad x^2+1=5'),
 E(r'\mathrm{half:}\quad\Delta z=-0.1(-0.009801)(5)=0.0049005'),
 E(r'\mathrm{BCE:}\quad\Delta z=-0.1(-0.99)(5)=0.495'),
 'This is a same-example logit change after updating both its weight and bias. A bias-only update would omit the x-squared term.']),
 P('Where sigmoid becomes insensitive','The same sigmoid is used with either loss.',[
 {'image':'sigmoid.png','width':650},
 'The slope is 0.0099 at p=0.01 or 0.99, versus 0.25 at p=0.5. BCE removes this output factor from the logit derivative; it does not remove every hidden-layer sigmoid factor or guarantee easy optimization.']),
 P('Your turn: a wrong target-zero prediction','Use a new probability and recompute all quantities.',[
 E(r'p=0.9,\quad t=0,\quad x=2,\quad b=0'),
 E(r'z=\ln(9),\quad w=\ln(9)/2,\quad\eta=0.1'),
 'Find both losses, the sigmoid slope, both derivatives with respect to p and z, and the weight/bias gradients. Then make one simultaneous w,b update for each loss and recompute the probability.',
 'Explain why the new logit decreases. State what would change if the squared loss had no factor 1/2.'],'INDEPENDENT PRACTICE'),
 P('Practice: losses and full chain-rule arithmetic','The target is zero, so BCE uses the logarithm of 1-p.',[
 E(r'L_{half}=\frac{1}{2}(0.9-0)^2=0.405,\quad L_{BCE}=-\ln(0.1)=2.30258509'),
 E(r'\frac{dp}{dz}=0.9(1-0.9)=0.09'),
 E(r'\mathrm{half:}\quad\frac{dL}{dp}=0.9,\quad\delta=0.9(0.09)=0.081'),
 E(r'\mathrm{BCE:}\quad\frac{dL}{dp}=1/(1-0.9)=10,\quad\delta=10(0.09)=0.9'),
 E(r'\mathrm{half:}\ (g_w,g_b)=(0.162,0.081);\quad\mathrm{BCE:}\ (1.8,0.9)'),
 'Positive parameter gradients are subtracted, reducing w and b. For this positive input, both changes reduce z and therefore reduce the wrong high probability.'],'WORKED ANSWER')]
pages+=steps(B,True)
pages.append(P('Practice checks and the scope of the conclusion','Same prediction and architecture; different loss derivatives.',[
 E(r'\mathrm{half:}\quad z_{new}=\ln9-0.1(0.081)(5)=\ln9-0.0405'),
 E(r'\mathrm{BCE:}\quad z_{new}=\ln9-0.1(0.9)(5)=\ln9-0.45'),
 'Using an unhalved square doubles its loss and gradients. Keeping the same learning rate would therefore double that parameter displacement.',
 'Do not threshold the probability before the loss, add an extra sigmoid derivative to p-t, confuse a loss derivative with a weight derivative, or infer that BCE eliminates hidden-layer vanishing gradients.'],'WORKED ANSWER'))
fig,ax=plt.subplots(figsize=(9.5,3),layout='constrained');zs=np.linspace(-6,6,300);ax.plot(zs,1/(1+np.exp(-zs)),color='#006E73')
for p,offset in [(.01,(15,18)),(.5,(12,-25)),(.99,(-130,-35))]:
 z=math.log(p/(1-p));ax.scatter([z],[p],color='#BD6A24');ax.annotate(f'p={p:g}; slope={p*(1-p):g}',(z,p),xytext=offset,textcoords='offset points',fontsize=10)
ax.set(xlabel='logit z',ylabel='sigmoid probability p');ax.grid(alpha=.2);fig.savefig(out/'sigmoid.png',dpi=170);plt.close(fig)
fd=[]
for a in [A,B]:
 for name in ['half','bce']:
  def loss(w,b):
   p=sig(2*w+b);t=a['t'];return .5*(p-t)**2 if name=='half' else -t*math.log(p)-(1-t)*math.log(1-p)
  h=1e-5;w=a['w'];gw=(loss(w+h,0)-loss(w-h,0))/(2*h);gb=(loss(w,h)-loss(w,-h))/(2*h)
  assert abs(gw-a[name+'_step']['gw'])<1e-8;assert abs(gb-a[name+'_step']['gb'])<1e-8
  fd.append(dict(p=a['p'],loss=name,weight_fd=gw,bias_fd=gb))
(out/'checks.json').write_text(json.dumps(dict(main=A,practice=B,finite_differences=fd),indent=2))
spec=dict(number=23,title='Sigmoid saturation and loss choice',description='Compare half-squared error and BCE on the same wrong prediction, derive every gradient, and work both parameter updates with a fresh practice.',source_short='Lecture4 PDF p.8-26 (unhalved square p.12) / BCE handout p.2',source='Lecture4 PDF pages8-26: saturation/squared divergence, unhalved formula page12; Backpropagation_Derivation.pdf page2: sigmoid+BCE; numerical-practice.md N4.1. Half-square study convention explicitly labeled.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
