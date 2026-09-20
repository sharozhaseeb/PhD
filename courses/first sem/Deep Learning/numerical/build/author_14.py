from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'14-activations-derivatives';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('An activation and its slope are different','Lecture 3, PDF page 156 lists the four functions and their derivatives.',[
E(r'z=b+\sum_i w_ix_i,\quad a=f(z),\quad f^{\prime}(z)=\frac{da}{dz}'),
'z is the weighted input before activation. We write a for the activation; the notes often write y. Here a is not a known target label.',
'The derivative is the local slope: how much the activation changes for a tiny increase in z.',
E(r'\Delta a\approx f^{\prime}(z)\Delta z'),
'Our main input is z = ln(3). Natural logarithm ln(3) means the number whose exponential is 3. This choice makes hand arithmetic simple.',
E(r'e^{\ln3}=3,\quad e^{-\ln3}=1/3,\quad\ln3\approx1.098612')]),
P('Sigmoid: calculate the activation first','The output is between zero and one; its derivative is a different number.',[
E(r'a=\sigma(z)=\frac{1}{1+e^{-z}}'),
E(r'z=\ln3:\quad a=\frac{1}{1+1/3}=\frac{1}{4/3}=\frac{3}{4}=0.75'),
E(r'\sigma^{\prime}(z)=a(1-a)'),
E(r'\sigma^{\prime}(\ln3)=\frac{3}{4}\left(1-\frac{3}{4}\right)=\frac{3}{4}\frac{1}{4}=\frac{3}{16}=0.1875'),
E(r'\Delta z=0.01\Rightarrow\Delta a\approx0.1875(0.01)=0.001875'),
'A small increase of 0.01 in input changes this activation by about 0.001875. This is a local approximation, not an exact finite difference.']),
P('Tanh: use the two exponential values','The assignment gives this exponential form; the lecture gives the derivative.',[
E(r'a=\tanh z=\frac{e^z-e^{-z}}{e^z+e^{-z}}'),
E(r'a=\frac{3-1/3}{3+1/3}=\frac{8/3}{10/3}=\frac{8}{10}=\frac{4}{5}=0.8'),
E(r'\tanh^{\prime}(z)=1-a^2'),
E(r'\tanh^{\prime}(\ln3)=1-(4/5)^2=1-16/25=9/25=0.36'),
'Square the activation before subtracting it from 1. The formula is not (1 - a) squared. Unlike sigmoid, tanh may output negative values.']),
P('ReLU: choose the correct branch','ReLU means rectified linear unit: keep positive input, otherwise output zero.',[
E(r'a=\max(0,z)'),
E(r'z=\ln3>0\Rightarrow a=\ln3\approx1.098612'),
E(r'f^{\prime}(z)=1\quad\mathrm{for}\ z>0'),
E(r'f^{\prime}(\ln3)=1'),
'At a positive input, increasing z by 0.01 increases the activation by exactly 0.01 as long as both inputs remain positive.',
'Zero is a special point where the classical derivative does not exist. We will compare the source conventions explicitly.']),
P('Softplus: a smooth positive activation','Use the natural logarithm, not a base-10 calculator logarithm.',[
E(r'a=\ln(1+e^z)'),
E(r'a=\ln(1+3)=\ln4\approx1.386294'),
E(r'f^{\prime}(z)=\frac{1}{1+e^{-z}}=\sigma(z)'),
E(r'f^{\prime}(\ln3)=\frac{1}{1+1/3}=\frac{3}{4}=0.75'),
'Softplus and sigmoid have different outputs. Softplus has sigmoid as its derivative; do not replace its activation by sigmoid.']),
P('Negative input: sigmoid and tanh','Now z = -ln(3), so exp(z) = 1/3 and exp(-z) = 3.',[
E(r'\sigma(-\ln3)=\frac{1}{1+3}=\frac{1}{4}=0.25'),
E(r'\sigma^{\prime}(-\ln3)=\frac{1}{4}(1-1/4)=\frac{3}{16}=0.1875'),
E(r'\tanh(-\ln3)=\frac{1/3-3}{1/3+3}=\frac{-8/3}{10/3}=-\frac{4}{5}'),
E(r'\tanh^{\prime}(-\ln3)=1-(-4/5)^2=1-16/25=9/25'),
'The activation of tanh is negative, but its slope here is positive. A negative activation does not imply a negative derivative.']),
P('Negative input: ReLU and softplus','The two functions behave differently on the negative side.',[
E(r'\mathrm{ReLU}(-\ln3)=\max(0,-\ln3)=0'),
E(r'\mathrm{ReLU}^{\prime}(-\ln3)=0'),
E(r'\mathrm{softplus}(-\ln3)=\ln(1+1/3)=\ln(4/3)\approx0.287682'),
E(r'\mathrm{softplus}^{\prime}(-\ln3)=\frac{1}{1+3}=\frac{1}{4}'),
'ReLU is flat for strictly negative input. Softplus is smooth and still has a small positive output and slope.']),
P('At zero: three smooth functions','Substitute exp(0) = 1 before calculating the derivatives.',[
E(r'\sigma(0)=\frac{1}{1+1}=\frac{1}{2},\quad\sigma^{\prime}(0)=\frac{1}{2}(1-1/2)=\frac{1}{4}'),
E(r'\tanh(0)=\frac{1-1}{1+1}=0,\quad\tanh^{\prime}(0)=1-0^2=1'),
E(r'\mathrm{softplus}(0)=\ln(1+1)=\ln2\approx0.693147'),
E(r'\mathrm{softplus}^{\prime}(0)=\frac{1}{1+1}=\frac{1}{2}'),
'Zero activation and zero derivative are different claims. Tanh has activation 0 at the origin but slope 1.']),
P('ReLU at zero: reconcile the two sources','The left and right slopes disagree, so there is no classical derivative.',[
E(r'\mathrm{ReLU}(0)=0'),
E(r'\mathrm{left\ slope}=\frac{f(0)-f(-0.01)}{0.01}=\frac{0-0}{0.01}=0'),
E(r'\mathrm{right\ slope}=\frac{f(0.01)-f(0)}{0.01}=\frac{0.01-0}{0.01}=1'),
'Lecture 3, PDF page 156 assigns slope 1 when z >= 0. Assignment 1, PDF page 2 assigns slope 1 only when z > 0, otherwise 0.',
'These are chosen backpropagation conventions at the kink, not classical derivatives. For assignment-aligned work, use 0 at zero and state that convention.']),
P('Compare the activation curves','Same input z, different outputs and local slopes.',[
{'image':'activations.png','width':660},
'Sigmoid and tanh flatten near their upper and lower limits. ReLU has a corner at zero. Softplus smoothly bends from a near-flat negative side to a near-linear positive side.']),
P('Saturation means a small local slope','At z = 4 the smooth bounded activations change slowly; their slopes are not zero.',[
E(r'\sigma(4)=\frac{1}{1+e^{-4}}\approx0.982014'),
E(r'\sigma^{\prime}(4)=0.982014(1-0.982014)\approx0.017663'),
E(r'\tanh(4)\approx0.999329,\quad\tanh^{\prime}(4)=1-0.999329^2\approx0.001341'),
E(r'\Delta z=0.01:\quad\Delta\sigma\approx0.00017663,\quad\Delta\tanh\approx0.00001341'),
'At zero the same small input change gives about 0.0025 for sigmoid and 0.01 for tanh. Repeated small slope factors can shrink gradients in a deep network.']),
P('Use the local slope in the chain rule','Suppose the incoming loss derivative is dL/da = 2 at z = ln(3).',[
E(r'\frac{dL}{dz}=\frac{dL}{da}\frac{da}{dz}=2f^{\prime}(z)'),
E(r'\mathrm{sigmoid}:\quad2(3/16)=3/8=0.375'),
E(r'\mathrm{tanh}:\quad2(9/25)=18/25=0.72'),
E(r'\mathrm{ReLU}:\quad2(1)=2'),
E(r'\mathrm{softplus}:\quad2(3/4)=3/2=1.5'),
'The incoming derivative depends on the rest of the network and loss. Here it is a supplied value, used to isolate the role of the activation derivative.']),
P('Your turn: an input with simple exponentials','Use z = ln(2), so exp(z) = 2 and exp(-z) = 1/2.',[
'For sigmoid, tanh, ReLU and softplus, calculate both the activation and its local derivative. Show the substitutions before simplifying.',
'Then suppose dL/da = -3. Calculate dL/dz for each activation using the chain rule.',
'Finally, state the derivative convention you would use for ReLU at zero in Assignment 1, and why it is a convention.'],'INDEPENDENT PRACTICE'),
P('Practice answer: sigmoid and tanh','Keep exact fractions until the final result.',[
E(r'\sigma(\ln2)=\frac{1}{1+1/2}=\frac{2}{3}'),
E(r'\sigma^{\prime}(\ln2)=\frac{2}{3}(1-2/3)=\frac{2}{9}'),
E(r'\frac{dL}{dz}=(-3)(2/9)=-2/3'),
E(r'\tanh(\ln2)=\frac{2-1/2}{2+1/2}=\frac{3/2}{5/2}=\frac{3}{5}'),
E(r'\tanh^{\prime}(\ln2)=1-(3/5)^2=16/25'),
E(r'\frac{dL}{dz}=(-3)(16/25)=-48/25=-1.92')],'WORKED ANSWER'),
P('Practice answer: ReLU and softplus','The sign of the loss derivative comes from the incoming value -3.',[
E(r'\mathrm{ReLU}(\ln2)=\ln2\approx0.693147,\quad f^{\prime}=1'),
E(r'\frac{dL}{dz}=(-3)(1)=-3'),
E(r'\mathrm{softplus}(\ln2)=\ln(1+2)=\ln3\approx1.098612'),
E(r'f^{\prime}=\frac{1}{1+1/2}=\frac{2}{3},\quad\frac{dL}{dz}=(-3)(2/3)=-2'),
'Assignment 1 uses ReLU slope 0 at zero. Its left and right slopes are 0 and 1, so the usual derivative does not exist there.',
'Checklist: do not confuse activation with slope, tanh derivative with (1-a)^2, or softplus output with sigmoid output.'],'WORKED ANSWER')]
z=np.linspace(-4,4,500);fig,axs=plt.subplots(1,2,figsize=(10,3.4),layout='constrained')
fs=[('sigmoid',lambda z:1/(1+np.exp(-z))),('tanh',np.tanh),('ReLU',lambda z:np.maximum(0,z)),('softplus',lambda z:np.logaddexp(0,z))]
for name,f in fs:axs[0].plot(z,f(z),label=name)
for name,v in [('sigmoid',fs[0][1](z)*(1-fs[0][1](z))),('tanh',1-np.tanh(z)**2),('softplus',fs[0][1](z))]:axs[1].plot(z,v,label=name,color={'sigmoid':'tab:blue','tanh':'tab:orange','softplus':'tab:red'}[name])
axs[1].plot([-4,0],[0,0],color='green',label='ReLU');axs[1].plot([0,4],[1,1],color='green');axs[1].scatter([0],[0],color='green',s=24,zorder=4);axs[1].scatter([0],[1],facecolor='white',edgecolor='green',s=24,zorder=4)
for ax in axs:ax.set_xlabel('z');ax.grid(alpha=.2);ax.legend(fontsize=8)
axs[0].set_ylabel('activation a');axs[1].set_ylabel('local slope');axs[1].set_title('ReLU at zero: chosen convention');fig.savefig(out/'activations.png',dpi=180);plt.close(fig)
checks=[]
for z in [-math.log(3),math.log(3),math.log(2),4]:
 for name,f in fs:
  val=float(f(z));h=1e-6;fd=float((f(z+h)-f(z-h))/(2*h));s=1/(1+math.exp(-z))
  analytic={'sigmoid':s*(1-s),'tanh':1-math.tanh(z)**2,'ReLU':float(z>0),'softplus':s}[name]
  assert abs(fd-analytic)<1e-7
  checks.append(dict(z=z,activation=name,value=val,analytic=analytic,finite_difference=fd))
(out/'checks.json').write_text(json.dumps(checks,indent=2))
spec=dict(number=14,title='Activations and derivatives',description='Substitute into all four lecture activation formulas, understand slopes, and practise the chain rule.',source_short='Lecture 3 / PDF p.156; Assignment 1 / PDF p.2 / zero convention stated',source='Lecture 3 - Learning Neural Network.pdf, page 156; Assignment 1.pdf, page 2. Original numerical inputs.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
