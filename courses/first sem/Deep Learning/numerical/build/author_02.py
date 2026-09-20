from pathlib import Path
import json
import numpy as np
from render_lesson import render
from check_math import half_mse,regression_gradient,finite_difference
out=Path(__file__).resolve().parent.parent/'02-linear-regression-gradient-descent';out.mkdir(exist_ok=True)
def E(s):return {'eq':s}
def P(title,sub,blocks,stage='WORKED EXAMPLE'):return dict(title=title,subtitle=sub,blocks=blocks,stage=stage)
X=np.array([[1,1],[1,2],[1,3]],float);y=np.array([2,3,5.]);theta=np.array([0.,1.]);grad=regression_gradient(X,y,theta);new=theta-.1*grad
check=finite_difference(lambda t:half_mse(X,y,t),theta,grad)
np.testing.assert_allclose(grad,[-4/3,-3]);np.testing.assert_allclose(half_mse(X,y,new),199/900)
pr=np.array([1.,1.]);pg=regression_gradient(X,y,pr);pn=pr-.1*pg;finite_difference(lambda t:half_mse(X,y,t),pr,pg);np.testing.assert_allclose(half_mse(X,y,pn),31/360)
(out/'checks.json').write_text(json.dumps(dict(gradient=grad.tolist(),finite_difference=check,new_parameters=new.tolist(),new_cost=half_mse(X,y,new),practice_new_cost=half_mse(X,y,pn)),indent=2))
pages=[P('Use error to choose a better line','Continue Lesson01. A gradient tells us how cost changes when a parameter changes.',[
'Data: (1, 2), (2, 3), (3, 5). Initial intercept theta 0 = 0; slope theta 1 = 1.',
E(r'h_\theta(x)=\theta_0+\theta_1x,\quad r_i=h_\theta(x^{(i)})-y^{(i)}'),
E(r'(r_1,r_2,r_3)=(-1,-1,-2),\qquad J=1'),
'A partial derivative holds the other parameter fixed. Read dJ/dtheta as the sensitivity of cost to a small parameter increase.',
E(r'\frac{\partial J}{\partial\theta_0},\quad\frac{\partial J}{\partial\theta_1},\qquad\alpha=0.1'),
'Alpha is the learning rate: it scales the size of our parameter step.']),
P('Derive the intercept gradient','Every prediction increases by 1 when the intercept increases by 1.',[
E(r'J=\frac{1}{2m}\sum_i r_i^2,\qquad r_i=\theta_0+\theta_1x^{(i)}-y^{(i)}'),
E(r'\frac{\partial r_i}{\partial\theta_0}=1'),
E(r'\frac{\partial J}{\partial\theta_0}=\frac{1}{2m}\sum_i 2r_i\frac{\partial r_i}{\partial\theta_0}'),
E(r'=\frac{1}{2m}\sum_i 2r_i(1)=\frac{1}{m}\sum_i r_i'),
'The derivative of a square gives 2r. That 2 cancels the 1/2 in the cost. The remaining gradient is the mean signed residual.']),
P('Derive the slope gradient','A slope change affects a prediction in proportion to that example\'s input.',[
E(r'\frac{\partial r_i}{\partial\theta_1}=x^{(i)}'),
'For x = 3, increasing the slope by 0.01 increases the prediction by 0.03.',
E(r'\frac{\partial J}{\partial\theta_1}=\frac{1}{2m}\sum_i2r_i x^{(i)}=\frac{1}{m}\sum_i r_ix^{(i)}'),
'Same residuals, different influence: multiply each residual by its own input before averaging.',
'These are the two gradients in Lecture 1, PDF page 44. Do not square residuals again when calculating them.']),
P('Substitute all three examples','Both gradients use the same old parameters, before any update.',[
E(r'g_0=\frac{\partial J}{\partial\theta_0}=\frac{-1+(-1)+(-2)}{3}=-\frac{4}{3}'),
E(r'r_1x^{(1)}=(-1)(1)=-1'),
E(r'r_2x^{(2)}=(-1)(2)=-2'),
E(r'r_3x^{(3)}=(-2)(3)=-6'),
E(r'g_1=\frac{\partial J}{\partial\theta_1}=\frac{-1-2-6}{3}=-3'),
'g is a short name for the gradient value. A negative gradient suggests a small increase in that parameter will lower cost.']),
P('Update both parameters together','Lecture 1, page 41: calculate temporary values, then replace both parameters.',[
E(r'\theta_j^{\mathrm{new}}=\theta_j^{\mathrm{old}}-\alpha g_j\qquad(j=0,1)'),
E(r'\theta_0^{\mathrm{new}}=0-0.1(-4/3)=\frac{2}{15}\approx0.133333'),
E(r'\theta_1^{\mathrm{new}}=1-0.1(-3)=1+0.3=1.3'),
'Subtracting a negative number increases the parameter. Both the intercept and the slope rise in this example.',
'Do not replace the intercept and then recalculate the slope gradient. That would mix old and new states.']),
P('Predict again with the new line','Keep exact fractions until the final decimal to avoid rounding drift.',[
E(r'h_1=\frac{2}{15}+1.3(1)=\frac{43}{30},\quad r_1=\frac{43}{30}-2=-\frac{17}{30}'),
E(r'h_2=\frac{2}{15}+1.3(2)=\frac{41}{15},\quad r_2=\frac{41}{15}-3=-\frac{4}{15}'),
E(r'h_3=\frac{2}{15}+1.3(3)=\frac{121}{30},\quad r_3=\frac{121}{30}-5=-\frac{29}{30}'),
'The predictions are approximately 1.433333, 2.733333 and 4.033333. They are all closer to their targets than before.']),
P('Check that the cost really decreased','A useful update must be checked using new predictions, not old residuals.',[
E(r'J_{\mathrm{new}}=\frac{(-17/30)^2+(-4/15)^2+(-29/30)^2}{6}'),
E(r'=\frac{289/900+64/900+841/900}{6}=\frac{1194}{5400}'),
E(r'J_{\mathrm{new}}=\frac{199}{900}\approx0.221111<1=J_{\mathrm{old}}'),
'One full-batch step uses all 3 examples and makes one simultaneous update.',
'A negative gradient is a local direction clue. An excessively large learning rate can still overshoot and increase cost.']),
P('Your turn: one step from another line','Use the same data, but begin at intercept 1 and slope 1.',[
E(r'\theta_0=1,\quad\theta_1=1,\quad\alpha=0.1,\quad m=3'),
'1. Predict all three targets and calculate signed residuals.',
'2. Calculate both mean gradients.',
'3. Update the intercept and slope simultaneously.',
'4. Recompute the predictions and half-MSE. Did the cost decrease?',
'Write the old and new parameter values in separate columns.'], 'INDEPENDENT PRACTICE'),
P('Practice answer: gradients and update','First finish all old-state calculations; then change the parameters.',[
E(r'h=(2,3,4),\qquad r=(2-2,3-3,4-5)=(0,0,-1)'),
E(r'g_0=\frac{0+0-1}{3}=-\frac{1}{3}'),
E(r'g_1=\frac{0(1)+0(2)+(-1)(3)}{3}=-1'),
E(r'\theta_0^{\mathrm{new}}=1-0.1(-1/3)=\frac{31}{30}'),
E(r'\theta_1^{\mathrm{new}}=1-0.1(-1)=1.1'),
'Initial practice cost: (0 + 0 + 1) / 6 = 1/6.'], 'WORKED ANSWER'),
P('Practice answer: verify the new cost','Two predictions now overshoot, but the overall fit improves.',[
E(r'h_1=31/30+1.1(1)=32/15,\quad r_1=32/15-2=2/15'),
E(r'h_2=31/30+1.1(2)=97/30,\quad r_2=97/30-3=7/30'),
E(r'h_3=31/30+1.1(3)=13/3,\quad r_3=13/3-5=-2/3'),
E(r'J=\frac{(2/15)^2+(7/30)^2+(-2/3)^2}{6}=\frac{31}{360}\approx0.086111'),
'This is below 1/6. Improving average loss does not require every example to improve.',
'Avoid: reversed residual signs; averaging twice; updating one parameter before computing the other gradient.'], 'WORKED ANSWER')]
spec=dict(number=2,title='Linear-regression gradient descent',description='Derive, calculate and verify one simultaneous training step.',source_short='Lecture 1 / PDF pp.36,41,44 / simultaneous updates',source='Lecture 1 - Introduction.pdf, pages 36, 41 and 44.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
