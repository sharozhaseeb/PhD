from pathlib import Path
import json, math
import numpy as np
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'37-standardization-initialization';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('Fit preprocessing on training data','Lecture 5 page163 calls for zero mean and unit variance.',[
 E(r'\mathrm{training\ feature}\ x=(2,4,6),\quad N=3'),E(r'\mu=\frac{1}{N}\sum_i x_i,\quad\sigma^2=\frac{1}{N}\sum_i(x_i-\mu)^2'),E(r'\sigma=\sqrt{\sigma^2},\qquad z_i=\frac{x_i-\mu}{\sigma}'),
 'We choose population variance with divisor N for this finite-training-set transformation. It is different from the N-1 estimator used in some statistical estimation exercises.',
 'Fit one mean and standard deviation per feature using training data. Save them and reuse them unchanged on validation, test and future inputs.']),
P('Calculate the training mean and deviations','Centering subtracts the same training mean from each value.',[
 E(r'\mu=(2+4+6)/3=12/3=4'),E(r'x_1-\mu=2-4=-2'),E(r'x_2-\mu=4-4=0'),E(r'x_3-\mu=6-4=2'),E(r'\mathrm{centered\ values}=(-2,0,2)'),
 'The centered values sum to zero. Centering alone does not set their variance to1.']),
P('Calculate variance, then standard deviation','Square each deviation before averaging.',[
 E(r'(-2)^2=4,\quad0^2=0,\quad2^2=4'),E(r'\sigma^2=(4+0+4)/3=8/3\approx2.666667'),E(r'\sigma=\sqrt{8/3}\approx1.632993'),
 'Variance is a squared quantity. Standard deviation has the original feature units; divide by the standard deviation to obtain the dimensionless standardized feature.']),
P('Transform all three training values','Use the same saved denominator for every example.',[
 E(r'z_1=(2-4)/\sqrt{8/3}=-\sqrt{3/2}\approx-1.224745'),E(r'z_2=(4-4)/\sqrt{8/3}=0'),E(r'z_3=(6-4)/\sqrt{8/3}=\sqrt{3/2}\approx1.224745'),
 'Negative z means below the training mean. Positive z means above it. Magnitude measures the distance from that mean in training standard-deviation units.']),
P('Verify zero mean and unit variance exactly','Use exact square roots for the check rather than rounded decimals.',[
 E(r'\overline{z}=(-\sqrt{3/2}+0+\sqrt{3/2})/3=0'),E(r'z_1^2=3/2,\quad z_2^2=0,\quad z_3^2=3/2'),E(r'\mathrm{Var}_{pop}(z)=((z_1-0)^2+(z_2-0)^2+(z_3-0)^2)/3'),E(r'=(1.5+0+1.5)/3=1'),
 'The unit-variance property follows from dividing by the standard deviation computed with the same population convention.']),
P('Transform a new input without refitting','A held-out value is8; the stored training statistics remain mu=4 and sigma=sqrt(8/3).',[
 E(r'z_{new}=\frac{8-4}{\sqrt{8/3}}=\frac{4}{1.632993\ldots}\approx2.449490'),
 'This value is about2.45 training standard deviations above the training mean. It is allowed to lie outside the range of standardized training values.',
 'Do not add this new value to the training set to recompute statistics. Doing so changes the fitted transformation and lets held-out information influence preprocessing.',
 'A validation or test set does not need mean0 and variance1 after this training-fitted transform.']),
P('Check the tempting wrong denominator','Dividing by variance instead of standard deviation does not produce unit variance.',[
 E(r'(-2,0,2)/(8/3)=(-0.75,0,0.75)'),E(r'\mathrm{mean}=0'),E(r'\mathrm{variance}=(0.75^2+0+0.75^2)/3'),E(r'=(0.5625+0.5625)/3=0.375\ne1'),
 'Both transforms center the data, but only division by sigma gives unit variance under the declared convention.']),
P('Choose a safe policy for a constant feature','Training values [5,5,5] have no variation.',[
 E(r'\mu=5,\quad\sigma^2=(0^2+0^2+0^2)/3=0'),E(r'\mathrm{chosen\ denominator}=1\quad\Longrightarrow\quad z=(0,0,0)'),E(r'\mathrm{new\ value}\ 7:\quad z_{new}=(7-5)/1=2'),
 'This explicit policy centers a constant feature without dividing by zero. Its training variance stays zero; no finite scaling can turn a constant sequence into one with unit variance.',
 'Other policies can remove such a feature, but the chosen policy must be applied consistently to new data.']),
P('Separate standardization from other preprocessing','The assignment and lecture describe different transformations.',[
 E(r'\mathrm{8\ bit\ pixel\ scale}:\quad x_{scaled}=x/255'),E(r'128/255\approx0.501961,\quad0/255=0,\quad255/255=1'),
 'Assignment 1 page4 requests pixels in[0,1]. Dividing 8-bit values by255 is a range transformation; it does not promise zero mean and unit variance.',
 'Fixed input standardization also does not include all of batch normalization: batch-dependent statistics, learned scale/offset and its train/inference behavior are separate machinery.']),
P('Optional: calculate named initializer scales','The slide names Xavier, Kaiming and SVD; it does not derive their numerical algorithms.',[
 'For a dense layer, fan_in is the number of incoming inputs to each unit; fan_out is the number of output units. Bias constants are not counted in these fan values here.',
 E(r'\mathrm{fan}_{in}=8,\quad\mathrm{fan}_{out}=4'),E(r'\mathrm{Xavier\ normal}:\quad V_X=\frac{2}{\mathrm{fan}_{in}+\mathrm{fan}_{out}}'),E(r'\mathrm{He\ normal}:\quad V_H=\frac{2}{\mathrm{fan}_{in}}'),
 'These are stated zero-mean normal variants: Xavier is associated with linear/tanh-style variance balance, while He/Kaiming accounts for ReLU. Gains and variants differ; these are not universal guarantees.'],'OPTIONAL EXTENSION'),
P('Take roots before scaling a normal draw','Initializer variance and initializer standard deviation are different.',[
 E(r'V_X=2/(8+4)=1/6,\quad\sigma_X=\sqrt{1/6}\approx0.408248'),E(r'V_H=2/8=1/4,\quad\sigma_H=\sqrt{1/4}=0.5'),E(r'Z\sim\mathcal{N}(0,1),\quad w=\sigma Z'),E(r'Z=-1.2:\quad w_X\approx0.408248(-1.2)=-0.489898'),E(r'w_H=0.5(-1.2)=-0.6'),
 'Z~N(0,1) means a draw from a normal distribution with mean 0 and variance 1; ~ means drawn from. The target variance belongs to that distribution, not necessarily to a finite set of drawn weights.'],'OPTIONAL EXTENSION'),
P('Why identical hidden units can stay identical','A small deterministic symmetry example, with only w1 and w2 trainable.',[
 E(r'h_j=\mathrm{ReLU}(w_jx),\quad\widehat y=h_1+h_2,\quad L=\frac{1}{2}(\widehat y-t)^2'),E(r'x=1,\quad t=0,\quad w_1=w_2=1'),E(r'h_1=h_2=1,\quad\widehat y=2,\quad r=\widehat y-t=2,\quad L=2'),E(r'g_{w_1}=2(1)(1)=2,\quad g_{w_2}=2(1)(1)=2'),E(r'\eta=0.1:\quad w_1^{new}=w_2^{new}=1-0.1(2)=0.8'),
 'With outgoing weights fixed at 1 and biases at 0, each gradient is residual times ReLU slope times input: 2*1*1. Identical deterministic paths receive identical updates.']),
P('Initialization scope and symmetry','Breaking symmetry lets otherwise interchangeable units begin differently.',[
 'Different initial weights can produce different activations and gradients. Independent draws are one way to avoid the exact symmetry in the preceding example.',
 'The identical-update argument assumes identical paths and deterministic conditions; asymmetric noise or different dropout masks can break those conditions.',
 'SVD means singular value decomposition, a matrix factorization that can provide orthogonal directions for certain initialization schemes. The lecture names it without specifying a numerical scheme; a full SVD initializer is outside this source\'s worked formula coverage.',
 'Zero initialization of every interchangeable hidden unit is therefore different from initializing a network bias to zero. The symmetry issue concerns matching trainable paths.']),
P('Your turn: fit a fresh training transform','Do not reuse the main example variance just because its mean looks familiar.',[
 E(r'\mathrm{training}=(1,4,7),\quad\mathrm{held\ out}=10'),
 'Compute the training mean, centered values, population variance, standard deviation and every standardized training value. Verify their mean/variance and transform10 using only saved training statistics.',
 'Optional: for fan_in=4 and fan_out=4, calculate the two stated normal initializer variances and standard deviations. If a standard-normal draw equals2, what weight does each produce?'],'INDEPENDENT PRACTICE'),
P('Answer: fresh training mean and spread','Use divisor N=3 for this transformation.',[
 E(r'\mu=(1+4+7)/3=4'),E(r'\mathrm{deviations}=(1-4,4-4,7-4)=(-3,0,3)'),E(r'\sigma^2=(9+0+9)/3=6'),E(r'\sigma=\sqrt{6}\approx2.449490'),
 'The mean matches the original example but the variance does not: the fresh training values are farther apart.'],'WORKED ANSWER'),
P('Answer: every transformed value and held-out input','Save the fresh mean4 and standard deviation sqrt(6).',[
 E(r'z_1=-3/\sqrt{6}=-\sqrt{3/2}\approx-1.224745'),E(r'z_2=0,\quad z_3=3/\sqrt{6}=\sqrt{3/2}\approx1.224745'),E(r'\overline{z}=0,\quad\mathrm{Var}_{pop}(z)=(1.5+0+1.5)/3=1'),E(r'z_{new}=(10-4)/\sqrt{6}=6/\sqrt{6}\approx2.449490'),
 'The normalized pattern matches because both training sequences are equally spaced rescalings, not because we reused the earlier standard deviation.'],'WORKED ANSWER'),
P('Answer: optional initializer arithmetic','Both fan values are4 in this fresh layer.',[
 E(r'V_X=2/(4+4)=0.25,\quad\sigma_X=\sqrt{0.25}=0.5'),E(r'V_H=2/4=0.5,\quad\sigma_H=\sqrt{0.5}\approx0.707107'),E(r'Z=2:\quad w_X=0.5(2)=1'),E(r'w_H=\sqrt{0.5}(2)\approx1.414214'),
 'Common errors: dividing by variance, fitting statistics on held-out data, expecting a constant feature to gain variance, or using an initializer variance directly as the normal draw multiplier.'],'WORKED ANSWER')]
checks=[]
for xs,xnew in [([2,4,6],8),([1,4,7],10)]:
 a=np.array(xs,dtype=float);mu=a.mean();v=((a-mu)**2).mean();sd=math.sqrt(v);z=(a-mu)/sd
 assert abs(z.mean())<1e-14 and abs((z*z).mean()-1)<1e-14
 checks.append(dict(training=xs,mean=mu,variance=v,sd=sd,z=z.tolist(),heldout=xnew,transformed=(xnew-mu)/sd))
(out/'checks.json').write_text(json.dumps(dict(standardization=checks,wrong_variance=.375,initializer_main_variances=[1/6,1/4],initializer_practice_variances=[.25,.5]),indent=2))
spec=dict(number=37,title='Standardization and initialization scales',description='Fit and verify training statistics, transform held-out data, handle constants, distinguish pixel scaling, and calculate explicitly optional initializer scales.',source_short='Lecture 5 PDF p.163 / Assignment 1 p.4 / initializer formulas labeled optional',source='Lecture 5 PDF page163 normalization and named initialization methods; Assignment 1 page4 pixel range. numerical-practice.md N6.10. Population-variance convention and optional normal initializer variants explicitly declared.',pages=pages)
for p in pages:
 for key in ['title','subtitle']:
  for a,b in [('page163','page 163'),('value is8','value is 8'),('mean4','mean 4'),('are4','are 4')]:p[key]=p[key].replace(a,b)
 for i,b in enumerate(p['blocks']):
  if isinstance(b,str):
   for a,z in [('to1','to 1'),('about2.45','about 2.45'),('mean0','mean 0'),('variance1','variance 1'),('values[','values ['),('page4','page 4'),('in[0,1]','in [0,1]'),('by255','by 255'),('at1','at 1'),('at0','at 0'),('transform10','transform 10'),('equals2','equals 2')]:b=b.replace(a,z)
   p['blocks'][i]=b
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
