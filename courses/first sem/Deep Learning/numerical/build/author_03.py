from pathlib import Path
import json
import numpy as np
from render_lesson import render
from check_math import half_mse,regression_gradient,finite_difference
out=Path(__file__).resolve().parent.parent/'03-multiple-feature-linear-regression';out.mkdir(exist_ok=True)
def E(s):return {'eq':s}
def P(title,sub,blocks,stage='WORKED EXAMPLE'):return dict(title=title,subtitle=sub,blocks=blocks,stage=stage)
X=np.array([[1,1,0],[1,0,1],[1,1,1.]]);y=np.array([2,1,3.]);t=np.zeros(3);checks=[]
for k in range(3):
 g=regression_gradient(X,y,t);fd=finite_difference(lambda p:half_mse(X,y,p),t,g)
 checks.append(dict(iteration=k,parameters=t.tolist(),predictions=(X@t).tolist(),cost=half_mse(X,y,t),gradient=g.tolist(),finite_difference=fd));t=t-.3*g
np.testing.assert_allclose([r['cost'] for r in checks],[7/3,.51,.1809]);(out/'checks.json').write_text(json.dumps(checks,indent=2))
pages=[P('Two inputs, one prediction','Each example has two measured features. It still has one target.',[
'Our study data are (x1, x2, y) = (1, 0, 2), (0, 1, 1), (1, 1, 3).',
E(r'h_\theta(x)=\theta^Tx=\theta_0x_0+\theta_1x_1+\theta_2x_2'),
'Lecture 1, page 43. The dot product multiplies matching components and adds them. T means transpose.',
E(r'x_0=1,\quad\theta_0=b,\quad\theta_1=w_1,\quad\theta_2=w_2'),
E(r'h(x)=b+w_1x_1+w_2x_2'),
'x0 = 1 is bookkeeping for the bias, not a third measured feature. Parameter order throughout: (b, w1, w2).']),
P('Start with three zero parameters','Feature subscripts choose columns; example superscripts choose rows.',[
E(r'(b,w_1,w_2)=(0,0,0),\qquad \alpha=0.3,\quad m=3'),
E(r'h_1=0+0(1)+0(0)=0,\qquad r_1=0-2=-2'),
E(r'h_2=0+0(0)+0(1)=0,\qquad r_2=0-1=-1'),
E(r'h_3=0+0(1)+0(1)=0,\qquad r_3=0-3=-3'),
E(r'J=\frac{(-2)^2+(-1)^2+(-3)^2}{2(3)}=\frac{14}{6}\approx2.333333'),
'Residual r is prediction minus target. J is half-MSE, matching Lecture 1.']),
P('One gradient for every parameter','Differentiate the same loss with respect to each parameter separately.',[
E(r'\frac{\partial r_i}{\partial b}=1,\quad\frac{\partial r_i}{\partial w_1}=x_1^{(i)},\quad\frac{\partial r_i}{\partial w_2}=x_2^{(i)}'),
E(r'J=\frac{1}{2m}\sum_i r_i^2\quad\Longrightarrow\quad\frac{\partial J}{\partial w_j}=\frac{1}{m}\sum_i r_ix_j^{(i)}'),
'The square derivative contributes 2r; 2 cancels 1/2. Multiply by the relevant input through the chain rule.',
E(r'g_b=\frac{\sum_i r_i}{m},\quad g_1=\frac{\sum_i r_ix_1^{(i)}}{m},\quad g_2=\frac{\sum_i r_ix_2^{(i)}}{m}'),
'Lecture 1, page 44: bias is the same rule with x0 = 1. Average each column once.']),
P('First step: calculate all contributions','Each row contributes (residual, residual times x1, residual times x2).',[
E(r'i=1:\quad(-2,\;(-2)(1),\;(-2)(0))=(-2,-2,0)'),
E(r'i=2:\quad(-1,\;(-1)(0),\;(-1)(1))=(-1,0,-1)'),
E(r'i=3:\quad(-3,\;(-3)(1),\;(-3)(1))=(-3,-3,-3)'),
E(r'g_b=\frac{-2-1-3}{3}=-2'),
E(r'g_1=\frac{-2+0-3}{3}=-\frac53,\qquad g_2=\frac{0-1-3}{3}=-\frac43'),
'A zero input makes that example contribute zero to that weight gradient, even if its prediction is wrong.']),
P('First simultaneous update','Use the same old parameter vector for all three right-hand sides.',[
E(r'b_{\mathrm{new}}=0-0.3(-2)=0.6'),
E(r'w_{1,\mathrm{new}}=0-0.3(-5/3)=0.5'),
E(r'w_{2,\mathrm{new}}=0-0.3(-4/3)=0.4'),
E(r'(b,w_1,w_2)=(0.6,0.5,0.4)'),
'Store the three new values, then replace the old ones together. One pass over all three examples produced one full-batch update.']),
P('Recompute after the first update','The second iteration must start with fresh predictions and residuals.',[
E(r'h_1=0.6+0.5(1)+0.4(0)=1.1,\quad r_1=1.1-2=-0.9'),
E(r'h_2=0.6+0.5(0)+0.4(1)=1.0,\quad r_2=1-1=0'),
E(r'h_3=0.6+0.5(1)+0.4(1)=1.5,\quad r_3=1.5-3=-1.5'),
E(r'J=\frac{(-0.9)^2+0^2+(-1.5)^2}{6}=\frac{0.81+0+2.25}{6}=0.51'),
'The cost fell from 2.333333 to 0.51. Do not reuse the initial residuals.']),
P('Second step: contributions and means','Again, the order in every triple is (bias, weight 1, weight 2).',[
E(r'i=1:\quad(-0.9,\;(-0.9)(1),\;(-0.9)(0))=(-0.9,-0.9,0)'),
E(r'i=2:\quad(0,\;0(0),\;0(1))=(0,0,0)'),
E(r'i=3:\quad(-1.5,\;(-1.5)(1),\;(-1.5)(1))=(-1.5,-1.5,-1.5)'),
E(r'g_b=\frac{-0.9+0-1.5}{3}=-0.8'),
E(r'g_1=\frac{-0.9+0-1.5}{3}=-0.8,\quad g_2=\frac{0+0-1.5}{3}=-0.5'),
'The second example is exactly predicted, so its current contribution is zero.']),
P('Second update and new predictions','Each parameter has its own gradient, but the learning rate is shared.',[
E(r'b=0.6-0.3(-0.8)=0.84'),
E(r'w_1=0.5-0.3(-0.8)=0.74,\quad w_2=0.4-0.3(-0.5)=0.55'),
E(r'h_1=0.84+0.74(1)+0.55(0)=1.58,\quad r_1=1.58-2=-0.42'),
E(r'h_2=0.84+0.74(0)+0.55(1)=1.39,\quad r_2=1.39-1=0.39'),
E(r'h_3=0.84+0.74(1)+0.55(1)=2.13,\quad r_3=2.13-3=-0.87')]),
P('Verify the second cost','The middle example gets worse, but the average fit still improves.',[
E(r'J=\frac{(-0.42)^2+(0.39)^2+(-0.87)^2}{6}'),
E(r'=\frac{0.1764+0.1521+0.7569}{6}=\frac{1.0854}{6}=0.1809'),
E(r'2.333333\quad\longrightarrow\quad0.51\quad\longrightarrow\quad0.1809'),
'These are costs at initialization, after update 1, and after update 2.',
'Shared parameters create tradeoffs across examples. A smaller mean cost does not guarantee improvement for each point.']),
P('Connect this to Homework 1','The homework uses the same rules with six rows and learning rate 0.01.',[
'Homework 1 starts w1 = w2 = b = 0. Its first data row is (x1, x2, y) = (1, 2, 11).',
E(r'h=0+0(1)+0(2)=0,\quad r=0-11=-11'),
E(r'(r,rx_1,rx_2)=(-11,\;(-11)(1),\;(-11)(2))=(-11,-11,-22)'),
'This is only the FIRST ROW contribution, not the full gradient. Repeat for all six rows, sum each column and divide by 6.',
'Then update all three parameters using alpha = 0.01. Our three-row toy data and alpha = 0.3 are study choices, not the homework dataset.',
'Common mistakes: confusing a feature index with an example index; forgetting the bias; mixing parameter order.']),
P('Your turn: a negative feature value','Use one example so you can check every multiplication by hand.',[
E(r'(x_1,x_2,y)=(2,-1,4),\qquad (b,w_1,w_2)=(1,2,3)'),
E(r'm=1,\qquad\alpha=0.1,\qquad J=\frac12(h-y)^2'),
'Calculate the prediction, signed residual, and three gradients.',
'Update all parameters simultaneously. Recompute the prediction and half-MSE.',
'Pay special attention to the sign of the weight 2 gradient.'], 'INDEPENDENT PRACTICE'),
P('Practice answer: one full update','The negative input reverses the sign of its weight contribution.',[
E(r'h=1+2(2)+3(-1)=2,\qquad r=2-4=-2'),
E(r'(g_b,g_1,g_2)=(-2,\;(-2)(2),\;(-2)(-1))=(-2,-4,2)'),
E(r'b=1-0.1(-2)=1.2,\qquad w_1=2-0.1(-4)=2.4'),
E(r'w_2=3-0.1(2)=2.8'),
E(r'h_{\mathrm{new}}=1.2+2.4(2)+2.8(-1)=1.2+4.8-2.8=3.2'),
E(r'J_{\mathrm{new}}=\frac12(3.2-4)^2=\frac12(0.64)=0.32<2=J_{\mathrm{old}}')], 'WORKED ANSWER')]
for p in pages:
 for b in p['blocks']:
  if isinstance(b,dict) and 'eq'in b:b['eq']=b['eq'].replace(r'\frac53',r'\frac{5}{3}').replace(r'\frac43',r'\frac{4}{3}').replace(r'\frac12',r'\frac{1}{2}')
spec=dict(number=3,title='Multiple-feature linear regression',description='Two input features, three parameters and two complete batch updates.',source_short='Lecture 1 / PDF pp.43-44 / Homework 1 connection',source='Lecture 1 - Introduction.pdf, pages 43-44; Home work 1 on Linear Regression.docx.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
