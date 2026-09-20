from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
ROOT=Path(__file__).resolve().parent.parent
out=ROOT/'01-single-feature-linear-regression';out.mkdir(exist_ok=True)
def E(s):return {'eq':s}
def P(title,sub,blocks,stage='WORKED EXAMPLE'):return dict(title=title,subtitle=sub,blocks=blocks,stage=stage)
pages=[
P('A line makes a numerical prediction','Our goal: measure how well one chosen line fits three observed points.',[
'Data: (x, y) = (1, 2), (2, 3), (3, 5). x is an input; y is its known target.',
E(r'h_\theta(x)=\theta_0+\theta_1x\qquad\mathrm{(Lecture\ 1,\ p.33)}'),
'h is the prediction. Theta names the model parameters: theta 0 is the intercept (bias); theta 1 is the slope (weight).',
E(r'\theta_0=0,\quad\theta_1=1,\quad m=3\quad\Longrightarrow\quad h_\theta(x)=x'),
'm counts examples. One shared line predicts all three points. These starting parameters are chosen for this study example.']),
P('Predict all three targets','Substitute each input into the same line. Do not change the parameters.',[
E(r'h_\theta(x^{(i)})=\theta_0+\theta_1x^{(i)}'),
'The superscript (i) identifies an example; it is not an exponent.',
E(r'h_\theta(x^{(1)})=0+1\times1=1\qquad y^{(1)}=2'),
E(r'h_\theta(x^{(2)})=0+1\times2=2\qquad y^{(2)}=3'),
E(r'h_\theta(x^{(3)})=0+1\times3=3\qquad y^{(3)}=5'),
'Predictions (1, 2, 3) differ from targets (2, 3, 5). Now measure the gaps.']),
P('Keep the sign, then square','Residual means prediction minus target. A negative residual is an underprediction.',[
E(r'r_i=h_\theta(x^{(i)})-y^{(i)}'),
E(r'r_1=1-2=-1\qquad r_1^2=(-1)^2=1'),
E(r'r_2=2-3=-1\qquad r_2^2=(-1)^2=1'),
E(r'r_3=3-5=-2\qquad r_3^2=(-2)^2=4'),
'Squaring makes every contribution nonnegative. A gap twice as large contributes four times as much squared error.',
'Keep the signed residuals too: the next lesson needs them for gradients.']),
P('Combine errors into one cost','The lecture uses half the mean squared error: be careful with the factor 2.',[
E(r'J(\theta_0,\theta_1)=\frac{1}{2m}\sum_{i=1}^{m}(h_\theta(x^{(i)})-y^{(i)})^2'),
'Lecture 1, PDF page 36. The summation sign means add all example contributions.',
E(r'J=\frac{1}{2\times3}(1+1+4)=\frac{6}{6}=1'),
E(r'\mathrm{MSE}=\frac{1+1+4}{3}=2\qquad J=\frac{1}{2}\mathrm{MSE}=1'),
'The factor 1/2 keeps the best-fit line the same and simplifies derivatives later. It is a convention, not part of every definition of MSE.',
'A smaller J means a closer fit under this squared-error measure.']),
P('Picture what the cost measures','The vertical gaps are target minus prediction; our signed residual is the reverse.',[
{'image':'fit.png','width':660},
'All three predictions lie below their targets. Squaring the gaps loses their direction; cost alone does not tell us how to move the line.']),
P('Your turn: shift the line upward','Stop here and calculate before looking at the answer page.',[
'Use the same three pairs: (1, 2), (2, 3), (3, 5). Change only the intercept.',
E(r'\theta_0=1,\qquad\theta_1=1,\qquad h_\theta(x)=1+x'),
'1. Calculate all three predictions.',
'2. Calculate each residual: prediction minus target.',
'3. Square the residuals and add them.',
'4. Divide by 2m. Is this cost lower than the original J = 1?',
'This is a new candidate line, not a gradient-descent update yet.'], 'INDEPENDENT PRACTICE'),
P('Practice answer and common mistakes','Compare each intermediate result with your working.',[
E(r'h_1=1+1(1)=2,\quad h_2=1+1(2)=3,\quad h_3=1+1(3)=4'),
E(r'r_1=2-2=0,\quad r_2=3-3=0,\quad r_3=4-5=-1'),
E(r'J=\frac{0^2+0^2+(-1)^2}{2\times3}=\frac{1}{6}\approx0.166667<1'),
'This candidate fits better overall. It predicts the first two targets exactly and underpredicts the third by 1.',
'Common mistakes: dividing by 3 instead of 6; treating (-1)^2 as -1; using a target as the model prediction.',
'Next: calculate gradients to choose a useful parameter change automatically.'], 'WORKED ANSWER')]
fig,ax=plt.subplots(figsize=(8,2.5),layout='constrained');ax.plot([0,3.5],[0,3.5],color='#006E73',label='prediction h(x) = x');ax.scatter([1,2,3],[2,3,5],color='#172B43',label='observed target y',s=60)
for x,y in zip([1,2,3],[2,3,5]):ax.plot([x,x],[x,y],'--',color='#A25D24');ax.text(x+.07,(x+y)/2,f'gap {y-x}',fontsize=10)
ax.set(xlabel='x: input',ylabel='y: target / prediction',xlim=(0,3.6),ylim=(0,5.5));ax.legend(loc='upper left');ax.grid(alpha=.15);fig.savefig(out/'fit.png',dpi=180);plt.close(fig)
spec=dict(number=1,title='Single-feature linear regression',description='Three points, signed residuals and the lecture\'s half-MSE cost.',source_short='Lecture 1 / PDF pp.33,36 / half-MSE convention',source='Lecture 1 - Introduction.pdf, pages 33 and 36 (PDF page numbers).',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2),encoding='utf-8');render(out/'lesson.json')
