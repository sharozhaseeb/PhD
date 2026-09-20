from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'06-logistic-decision-boundaries';out.mkdir(exist_ok=True)
def E(s):return {'eq':s}
def P(title,sub,blocks,stage='WORKED EXAMPLE'):return dict(title=title,subtitle=sub,blocks=blocks,stage=stage)
pages=[P('A score from two input features','Use the exact example in Lecture 2, PDF page 13.',[
E(r'z=\theta_0+\theta_1x_1+\theta_2x_2=-3+x_1+x_2'),
E(r'p=h_\theta(x)=g(z)=\frac{1}{1+e^{-z}}'),
'The lecture calls the probability h and the sigmoid g. We write the same probability as p. e is approximately 2.718.',
E(r'(\theta_0,\theta_1,\theta_2)=(-3,1,1),\qquad x_0=1'),
'x0 = 1 supplies the intercept. x1 and x2 are the two measured features.',
'These parameters are fixed for illustration. We are making predictions, not fitting the parameters in this lesson.']),
P('Calculate scores, probabilities and labels','Lecture 2, page 12: predict class 1 when p is at least 0.5.',[
E(r'(1,1):\ z=-3+1+1=-1,\quad p=\frac{1}{1+e^1}\approx0.268941\Rightarrow0'),
E(r'(1,2):\ z=-3+1+2=0,\quad p=\frac{1}{1+e^0}=0.5\Rightarrow1'),
E(r'(2,2):\ z=-3+2+2=1,\quad p=\frac{1}{1+e^{-1}}\approx0.731059\Rightarrow1'),
'The arrow at the end gives the predicted class label. The decimal before it is a probability, not a class label.',
'A score of zero is a tie: our stated convention assigns the boundary to class 1.']),
P('Find the boundary without guessing','The decision boundary is the set of inputs where p = 0.5, equivalently z = 0.',[
E(r'-3+x_1+x_2=0\quad\Longrightarrow\quad x_2=3-x_1'),
E(r'x_1=0\Rightarrow x_2=3,\qquad x_2=0\Rightarrow x_1=3'),
'Plot (0, 3) and (3, 0), then draw the straight line through them.',
E(r'x_1+x_2\geq3\Rightarrow z\geq0\Rightarrow p\geq0.5\Rightarrow\hat y=1'),
E(r'x_1+x_2<3\Rightarrow z<0\Rightarrow p<0.5\Rightarrow\hat y=0'),
'The boundary is a line in the input plane. It is not the S-shaped sigmoid graph.']),
P('Read the two sides of the line','The shaded regions are predicted classes; the dots are our three test inputs.',[
{'image':'line.png','width':640},
'Moving across the line changes the predicted label. Probability varies smoothly even though the thresholded label changes abruptly.']),
P('Compute new features from the same inputs','Lecture 2, page 14 adds squared features. No new measured input is needed.',[
E(r'z=\theta_0+\theta_1x_1+\theta_2x_2+\theta_3x_1^2+\theta_4x_2^2'),
E(r'(\theta_0,\theta_1,\theta_2,\theta_3,\theta_4)=(-1,0,0,1,1)'),
E(r'z=-1+0x_1+0x_2+1x_1^2+1x_2^2=-1+x_1^2+x_2^2'),
'The transformed feature list is (1, x1, x2, x1 squared, x2 squared). Square each measured input before multiplying its coefficient.',
'The score is still linear in its parameters: each theta multiplies a known feature. Its boundary can be curved in the original input plane.']),
P('Predict inside, on and outside the circle','Use the same sigmoid and the same probability threshold.',[
E(r'(0,0):\ z=-1+0^2+0^2=-1,\ p=\frac{1}{1+e^1}\approx0.268941\Rightarrow0'),
E(r'(1,0):\ z=-1+1^2+0^2=0,\ p=\frac{1}{1+e^0}=0.5\Rightarrow1'),
E(r'(1,1):\ z=-1+1^2+1^2=1,\ p=\frac{1}{1+e^{-1}}\approx0.731059\Rightarrow1'),
'Only the score formula changed. A negative score still means p < 0.5; a positive score still means p > 0.5.']),
P('A circular decision boundary','Set z = 0: x1 squared + x2 squared = 1, a circle of radius 1.',[
{'image':'circle.png','width':640},
'Inside: x1 squared + x2 squared < 1 gives class 0. Outside and on the circle: at least 1 gives class 1.']),
P('Your turn: compare the two models','Use the threshold p >= 0.5 for class 1 throughout.',[
E(r'(x_1,x_2)=(0.5,0.5)'),
'1. For z = -3 + x1 + x2, calculate score, probability and class.',
'2. For z = -1 + x1 squared + x2 squared, repeat the calculation.',
'3. In the curved model, change only the intercept from -1 to -4. Derive the new boundary and its radius.',
'4. What class do points exactly on that new boundary receive?',
'Keep probability values when calculating a loss later; do not replace them by 0 or 1.'], 'INDEPENDENT PRACTICE'),
P('Practice answer: scores and geometry','Changing a feature transformation changes the shapes the model can represent.',[
E(r'z_{\mathrm{line}}=-3+0.5+0.5=-2,\quad p=\frac{1}{1+e^2}\approx0.119203\Rightarrow0'),
E(r'z_{\mathrm{circle}}=-1+(0.5)^2+(0.5)^2=-0.5'),
E(r'p=\frac{1}{1+e^{0.5}}\approx0.377541\Rightarrow0'),
E(r'-4+x_1^2+x_2^2=0\Rightarrow x_1^2+x_2^2=4\Rightarrow R=\sqrt{4}=2'),
'On the new circle, z = 0 and p = 0.5, so the label is 1 by our convention.',
'Avoid: forgetting the intercept; adding features before squaring them; confusing a probability with a label.'], 'WORKED ANSWER')]
for kind in ['line','circle']:
 fig,ax=plt.subplots(figsize=(8,3),layout='constrained')
 if kind=='line':
  xx,yy=np.meshgrid(np.linspace(0,3.6,200),np.linspace(0,3.6,200));zz=xx+yy-3
  ax.contourf(xx,yy,zz,levels=[-8,0,8],colors=['#edf1f7','#dcefeb']);ax.plot([0,3],[3,0],color='#006E73',lw=2)
  pts=[(1,1),(1,2),(2,2)];ax.text(.2,.3,'class 0');ax.text(2.5,3,'class 1');ax.set(xlim=(0,3.6),ylim=(0,3.6))
 else:
  xx,yy=np.meshgrid(np.linspace(-1.6,1.6,200),np.linspace(-1.6,1.6,200));zz=xx**2+yy**2-1
  ax.contourf(xx,yy,zz,levels=[-8,0,8],colors=['#edf1f7','#dcefeb']);a=np.linspace(0,2*np.pi,300);ax.plot(np.cos(a),np.sin(a),color='#006E73',lw=2)
  pts=[(0,0),(1,0),(1,1)];ax.text(-.7,-.5,'class 0');ax.text(-1.5,1.25,'class 1');ax.set(xlim=(-1.6,1.6),ylim=(-1.6,1.6));ax.set_aspect('equal')
 for a,b in pts:ax.scatter(a,b,color='#172B43',s=40);ax.annotate(f'({a}, {b})',(a,b),xytext=(5,5),textcoords='offset points')
 ax.set(xlabel='x1: first measured feature',ylabel='x2: second measured feature');fig.savefig(out/f'{kind}.png',dpi=180);plt.close(fig)
checks={str(z):1/(1+math.exp(-z)) for z in [-2,-1,-.5,0,1]};(out/'checks.json').write_text(json.dumps(checks,indent=2))
spec=dict(number=6,title='Logistic regression and decision boundaries',description='Two-feature probabilities, a straight boundary and a transformed circular boundary.',source_short='Lecture 2 / PDF pp.9,12-14 / p >= 0.5 means class 1',source='Lecture 2 - Logistic Regression + Neural Network.pdf, pages 9 and 12-14.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
