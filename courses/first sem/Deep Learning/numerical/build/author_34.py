from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'34-l2-weight-decay';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('Add a cost for large selected weights','The objective balances prediction error and squared weight magnitude.',[
 E(r'J=\frac{1}{N}\sum_{i=1}^{N}\frac{1}{2}(\widehat y_i-t_i)^2+\frac{\lambda}{2}\sum_jw_j^2'),
 'N is the number of examples; lambda is the regularization coefficient. The data term is a mean. The penalty sums every selected weight once, with no extra division by N under this convention.',
 'Lecture 5 page 137 writes the weight penalty using the squared Frobenius norm of each weight matrix: this means add the squares of all its selected entries.',
 'Our exercise penalizes w1 and w2 only. The bias b is explicitly unpenalized. State the selection policy before computing the objective or gradients.']),
P('Set up the main three-parameter example','Chosen data and initial parameters; ordinary gradient descent.',[
 E(r'\widehat y=w_1x_1+w_2x_2+b'),E(r'x=(2,1),\quad t=1,\quad(w_1,w_2,b)=(1,-2,0.5)'),E(r'\lambda=0.2,\quad\eta=0.1'),E(r'J=\frac{1}{2}(\widehat y-t)^2+\frac{0.2}{2}(w_1^2+w_2^2)'),
 'There is one example, so the mean data loss equals its one-example loss. Lambda controls penalty strength; eta controls the parameter update. They are different numbers with different roles.']),
P('Compute prediction and data loss','Keep the residual sign for the gradient, even though the loss squares it.',[
 E(r'\widehat y=1(2)+(-2)(1)+0.5=2-2+0.5=0.5'),E(r'r=\widehat y-t=0.5-1=-0.5'),E(r'L_{data}=\frac{1}{2}(-0.5)^2=\frac{1}{2}(0.25)=0.125'),
 'r is prediction minus target. The negative residual says this prediction is below its target. The squared data loss is nevertheless positive.']),
P('Compute the penalty and total objective','The unpenalized bias does not appear in this sum.',[
 E(r'w_1^2+w_2^2=1^2+(-2)^2=1+4=5'),E(r'R=\frac{\lambda}{2}(w_1^2+w_2^2)=\frac{0.2}{2}(5)=0.5'),E(r'J=L_{data}+R=0.125+0.5=0.625'),
 'R denotes the regularization penalty. The negative weight contributes a positive square, so either sign can incur a large penalty.']),
P('Differentiate each part of the objective','The gradient of a sum is the sum of its gradients.',[
 E(r'\frac{\partial L_{data}}{\partial w_j}=r\frac{\partial\widehat y}{\partial w_j}=rx_j'),E(r'\frac{\partial R}{\partial w_j}=\frac{\lambda}{2}(2w_j)=\lambda w_j'),E(r'\frac{\partial J}{\partial w_j}=rx_j+\lambda w_j'),E(r'\frac{\partial J}{\partial b}=r(1)+0=r'),
 'The factor 2 from differentiating the square cancels the penalty factor 1/2. The penalty bias derivative is zero because b was excluded.']),
P('Substitute every main gradient','All three derivatives use the original parameter state.',[
 E(r'g_{w_1}=(-0.5)(2)+0.2(1)=-1+0.2=-0.8'),E(r'g_{w_2}=(-0.5)(1)+0.2(-2)=-0.5-0.4=-0.9'),E(r'g_b=-0.5'),
 {'table':[['parameter','data gradient','penalty gradient','total'],['w1','-1','+.2','-.8'],['w2','-.5','-.4','-.9'],['b','-.5','0','-.5']],'widths':[135,175,215,130]},
 'The penalty gradient has the weight sign. Subtracting that contribution pulls either positive or negative weights toward zero.']),
P('Update all three parameters simultaneously','Compute every new value from the same original state.',[
 E(r'w_1^{new}=1-0.1(-0.8)=1.08'),E(r'w_2^{new}=-2-0.1(-0.9)=-1.91'),E(r'b^{new}=0.5-0.1(-0.5)=0.55'),
 'Although arithmetic is written one parameter at a time, all gradients came from the original prediction 0.5. Do not recompute the residual halfway through.',
 'w1 increased overall because its data-loss contribution outweighed the penalty contribution. Regularization does not force every total update to reduce every weight magnitude.']),
P('Check the new full regularized objective','Use the new parameters in both the data term and penalty.',[
 E(r'\widehat y^{new}=1.08(2)+(-1.91)(1)+0.55=0.8'),E(r'r^{new}=0.8-1=-0.2,\quad L_{data}^{new}=\frac{1}{2}(0.2)^2=0.02'),E(r'R^{new}=0.1(1.08^2+(-1.91)^2)'),E(r'=0.1(1.1664+3.6481)=0.48145'),E(r'J^{new}=0.02+0.48145=0.50145<0.625'),
 'This chosen step decreases the stated full objective. A different learning rate need not do so.']),
P('Derive the weight-decay form algebraically','For ordinary gradient descent on this declared L2 objective.',[
 E(r'w^{new}=w-\eta(g_{data}+\lambda w)'),E(r'=w-\eta g_{data}-\eta\lambda w'),E(r'=(1-\eta\lambda)w-\eta g_{data}'),E(r'1-\eta\lambda=1-0.1(0.2)=0.98'),
 'The shrink factor acts on the old weight; the data-gradient correction is also computed at the old state. Bias uses its ordinary data update because it is unpenalized.']),
P('Verify both weight updates using the shrink factor','The two algebraic forms must give the same result.',[
 E(r'w_1^{new}=0.98(1)-0.1(-1)=0.98+0.1=1.08'),E(r'w_2^{new}=0.98(-2)-0.1(-0.5)=-1.96+0.05=-1.91'),
 'With only the penalty and zero data gradient, the weights would become .98 and -1.96. Both magnitudes shrink. The real data gradients add the corrections shown above.',
 'Do not use the shrink factor on b in this exercise, and do not apply both the combined gradient and an additional shrink factor: that would count the same penalty twice.']),
P('Read the boxed lecture factor carefully','Lecture page 138 shows both an expanded update and a boxed shorthand.',[
 E(r'\mathrm{objective\ coefficient}:\quad\lambda=0.2'),E(r'\mathrm{per\ step\ decay}:\quad d=\eta\lambda=0.1(0.2)=0.02'),E(r'w^{new}=(1-d)w-\eta g_{data}'),
 'The expanded slide term is -eta*lambda*w. Its boxed factor 1-lambda agrees only if that boxed lambda is redefined as the per-step decay d; otherwise the learning-rate factor is missing.',
 'Keep lambda fixed as the objective coefficient throughout your solution. Here 1-lambda=.8 would be incorrect; the required shrink factor is 1-d=.98.']),
P('Why Adam needs a separate distinction','Ordinary gradient descent applies the same scalar rate to every gradient term.',[
 'With an L2 objective under Adam, the extra lambda*w term enters both moment recurrences before adaptive normalization. A separately applied weight decay instead changes the weight directly.',
 'Those operations are generally different. Do not assume that adding an L2 penalty to an adaptive optimizer is identical to multiplying weights by a decay factor outside it.',
 'For this lesson, the exact equivalence we derived is for ordinary gradient descent with the declared mean-data-loss plus L2 objective.']),
P('Relate a scalar weight to input sensitivity','This derivative is with respect to input x, not a training gradient with respect to w.',[
 E(r'f(x)=\sigma(wx),\quad\frac{df}{dx}=w\sigma(wx)(1-\sigma(wx))'),E(r'x=0:\quad\sigma(0)=\frac{1}{2}\Longrightarrow f^{\prime}(0)=w/4'),E(r'w=0.5:\quad f^{\prime}(0)=0.5/4=0.125'),E(r'w=5:\quad f^{\prime}(0)=5/4=1.25'),
 'This supplies the arithmetic behind the scalar steepness picture on page 133. It is a local illustration, not a general theorem that every deep network with smaller weights is smoother.']),
P('See the two scalar sigmoid responses','Both pass through (0,.5), but their slopes there differ by a factor 10.',[
 {'image':'sigmoid-slopes.png','width':650},
 'The dashed lines are local tangents at x=0. The steeper curve reacts more strongly to small input changes near that point.']),
P('Your turn: fresh data, weights and regularization','Use the same objective convention and leave the bias unpenalized.',[
 E(r'x=(1,2),\quad t=2,\quad(w_1,w_2,b)=(2,1,-1)'),E(r'\lambda=0.1,\quad\eta=0.1'),
 'Compute prediction, residual, data loss, penalty, total objective, all three gradients and one simultaneous update. Show the separate data and penalty gradients.',
 'Verify the weight updates using the shrink factor. Recompute the full objective after the update.'],'INDEPENDENT PRACTICE'),
P('Answer: prediction and both loss terms','All starting values belong to the fresh practice problem.',[
 E(r'\widehat y=2(1)+1(2)-1=3,\quad r=3-2=1'),E(r'L_{data}=\frac{1}{2}(1)^2=0.5'),E(r'R=\frac{0.1}{2}(2^2+1^2)=0.05(5)=0.25'),E(r'J=0.5+0.25=0.75')],'WORKED ANSWER'),
P('Answer: every practice gradient and update','Use the same residual 1 in all three data derivatives.',[
 E(r'g_{w_1}=1(1)+0.1(2)=1+0.2=1.2'),E(r'g_{w_2}=1(2)+0.1(1)=2+0.1=2.1,\quad g_b=1'),E(r'w_1^{new}=2-0.1(1.2)=1.88'),E(r'w_2^{new}=1-0.1(2.1)=0.79'),E(r'b^{new}=-1-0.1(1)=-1.1')],'WORKED ANSWER'),
P('Answer: verify the factor and recompute prediction','The factor is .99 because it includes the learning rate.',[
 E(r'1-\eta\lambda=1-0.1(0.1)=0.99'),E(r'w_1^{new}=0.99(2)-0.1(1)=1.88'),E(r'w_2^{new}=0.99(1)-0.1(2)=0.79'),E(r'\widehat y^{new}=1.88(1)+0.79(2)-1.1=2.36'),E(r'r^{new}=2.36-2=0.36')],'WORKED ANSWER'),
P('Answer: the new full objective','The penalty is evaluated at the updated weights too.',[
 E(r'L_{data}^{new}=\frac{1}{2}(0.36)^2=0.0648'),E(r'R^{new}=0.05(1.88^2+0.79^2)'),E(r'=0.05(3.5344+0.6241)=0.207925'),E(r'J^{new}=0.0648+0.207925=0.272725'),
 'Common errors: penalizing an excluded bias, dividing the regularizer by batch size again, losing the negative-weight sign in its derivative, using 1-lambda instead of 1-eta*lambda, or shrinking a second time after already including the penalty gradient.'],'WORKED ANSWER')]
fig,ax=plt.subplots(figsize=(9.5,3),layout='constrained');xx=np.linspace(-4,4,400)
for w,c in [(.5,'#147d92'),(5,'#c86c28')]:
 ax.plot(xx,1/(1+np.exp(-w*xx)),color=c,label=f'w={w}, slope at 0 = {w/4:g}')
 tx=np.linspace(-.25,.25,40);ax.plot(tx,.5+w/4*tx,'--',color=c)
ax.set(xlabel='input x',ylabel='sigmoid output',ylim=(-.03,1.03));ax.grid(alpha=.2);ax.legend(fontsize=9);fig.savefig(out/'sigmoid-slopes.png',dpi=180);plt.close(fig)
checks=[]
for theta,x,t,lam in [(np.array([1.,-2.,.5]),np.array([2.,1.]),1,.2),(np.array([2.,1.,-1.]),np.array([1.,2.]),2,.1)]:
 def obj(p):return .5*(p[:2]@x+p[2]-t)**2+lam/2*(p[:2]@p[:2])
 r=theta[:2]@x+theta[2]-t;g=np.r_[r*x+lam*theta[:2],r];h=1e-6;fd=np.array([(obj(theta+np.eye(3)[j]*h)-obj(theta-np.eye(3)[j]*h))/(2*h) for j in range(3)])
 assert max(abs(g-fd))<1e-9
 new=theta-.1*g;checks.append(dict(old=theta.tolist(),gradient=g.tolist(),finite_difference=fd.tolist(),new=new.tolist(),J_old=obj(theta),J_new=obj(new)))
(out/'checks.json').write_text(json.dumps(checks,indent=2))
spec=dict(number=34,title='L2 regularization and weight decay',description='Compute every loss and gradient term, update all parameters, check the full new objective, and reconcile the lecture shrink-factor notation.',source_short='Lecture 5 PDF p.133,137-138 / unpenalized bias; objective lambda fixed',source='Lecture 5 pages125-143; objective137, update138, sigmoid steepness133. numerical-practice.md N6.7. Bias exclusion is an explicitly chosen exercise convention.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
