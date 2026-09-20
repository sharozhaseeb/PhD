from pathlib import Path
from io import BytesIO
import math,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

OUT=Path(__file__).resolve().parent; OUT.mkdir(parents=True,exist_ok=True)
pdf=OUT/'lesson.pdf'
x=np.array([1.,2.,3.]); y=np.array([0.,1.,1.]); p=np.full(3,.5)
dw=float(np.mean((p-y)*x)); db=float(np.mean(p-y)); wn=-.1*dw; bn=-.1*db
znew=wn*x+bn; pnew=1/(1+np.exp(-znew)); lossnew=-y*np.log(pnew)-(1-y)*np.log1p(-pnew)
def cost(w,b):
    z=w*x+b
    return float(np.mean(np.logaddexp(0,z)-y*z))
h=1e-6
assert abs((cost(h,0)-cost(-h,0))/(2*h)-dw)<1e-8
assert abs((cost(0,h)-cost(0,-h))/(2*h)-db)<1e-8
assert cost(wn,bn)<cost(0,0)
(OUT/'verification.json').write_text(json.dumps(dict(dw=dw,db=db,w_new=wn,b_new=bn,z_new=znew.tolist(),p_new=pnew.tolist(),loss_new=lossnew.tolist(),old_cost=cost(0,0),new_cost=cost(wn,bn)),indent=2))

W,H=800,600
c=canvas.Canvas(str(pdf),pagesize=(W,H))
c.setTitle('Logistic regression: three points, one complete training update')
c.setAuthor('Course study support')
INK='#172B43'; TEAL='#006E73'; MUTED='#526477'; BLUE='#EAF3F7'
def text(s,x,y,size=16,color=INK,bold=False):
    c.setFillColor(HexColor(color));c.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
    assert c.stringWidth(s,'Helvetica-Bold' if bold else 'Helvetica',size)<=W-x-35,(s,y)
    c.drawString(x,H-y,s)
def lines(items,y,x=48,size=16,leading=24):
    for s in items:text(s,x,y,size);y+=leading
def eq(s,y,x=52,size=23,maxwidth=700):
    buf=BytesIO();math_to_image('$'+s+'$',buf,dpi=220,format='png',color=INK,prop=FontProperties(size=size))
    buf.seek(0);im=Image.open(buf); iw,ih=im.size
    ww=iw*72/220;hh=ih*72/220
    assert ww<maxwidth,(s,ww)
    c.drawImage(ImageReader(im),x,H-y-hh,width=ww,height=hh,mask='auto')
def start(n,k,title,sub):
    c.setFillColor(HexColor('#FAFCFD'));c.rect(0,0,W,H,fill=1,stroke=0)
    text('LOGISTIC REGRESSION  /  THREE POINTS',48,34,11,TEAL,True)
    text(k.upper(),48,66,12,TEAL,True);text(title,48,106,29,INK,True)
    text(sub,48,137,15,MUTED)
    c.setStrokeColor(HexColor('#D7E3E9'));c.line(48,444,752,444)
    text('One feature | Binary labels | Mean BCE | One full-batch update',48,574,10,MUTED)
    text(f'{n} / 13',714,574,11,TEAL,True)
def callout(title,body,y=489):
    c.setFillColor(HexColor(BLUE));c.roundRect(40,H-y-62,720,70,9,fill=1,stroke=0)
    text(title,54,y+13,15,TEAL,True)
    text(body,54,y+39,14)
def end():c.showPage()

start(1,'Match your notes','Same formulas, simpler symbols','Source: Lecture 2, PDF pages 9 and 22-25 (title slide counts as page 1).')
text('The notes use theta for the parameters and h for the prediction.',48,186,17)
eq(r'h_{\theta}(x)=g(\theta^T x)=p,\qquad g(z)=\sigma(z)=\frac{1}{1+e^{-z}}',211,size=24)
eq(r'\theta_0=b,\quad\theta_1=w,\quad x_0=1',290,size=26)
eq(r'\theta^T(1,x)=\theta_0\times1+\theta_1\times x=b+wx',350,size=23)
lines(['Cost in the notes is L here: one example\'s binary cross-entropy.',
       'J is the mean loss in both. The notes write log; here ln means natural log.',
       'The learning rate alpha and simultaneous-update rule are unchanged.'],416,size=15,leading=23)
callout('Our choices for a small worked example','The three data pairs, starting values, and learning rate are chosen for practice.')
end()

start(2,'Start here','What are we trying to learn?','A number x goes in. We estimate the probability that its label y is 1.')
text('Our three training examples',48,187,20,bold=True)
for i,(a,b) in enumerate(zip(x,y)):
    xx=55+i*240
    text(f'Example {i+1}',xx,223,15,TEAL,True)
    eq(rf'(x_{i+1},y_{i+1})=({int(a)},{int(b)})',244,x=xx,size=22,maxwidth=230)
lines(['x = one input value.   y = the known label, either 0 or 1.',
       'w = weight: how strongly x affects the score.   b = bias: a shared offset.',
       'p = the predicted probability of label 1. It is not the known label y.',
       'One shared w and b serve all 3 examples; i identifies the example.'],320,size=16)
eq(r'w=0,\qquad b=0,\qquad \alpha=0.1,\qquad m=3',410)
text('Zero is our starting guess; alpha controls step size; m counts examples.',52,465,15,MUTED)
callout('Our plan','Predict each p, measure the loss, calculate gradients, then update w and b.')
end()

start(3,'Step 1 / Forward pass','Turn each x into a probability','Use the same starting w = 0 and b = 0 for all three examples.')
eq(r'z_i=wx_i+b\qquad\longrightarrow\qquad p_i=\sigma(z_i)=\frac{1}{1+e^{-z_i}}',180,size=24)
text('Sigmoid maps any score to a probability between 0 and 1.',52,244,16)
text('The symbol sigma names sigmoid: negative z gives p < 0.5; positive z gives p > 0.5.',52,265,14)
text('e is approximately 2.718; e to the power 0 equals 1.',52,286,14,MUTED)
for i,a in enumerate(x):
    yy=300+i*59
    eq(rf'z_{i+1}=0\times {int(a)}+0=0\qquad p_{i+1}=\frac{{1}}{{1+e^0}}=\frac{{1}}{{2}}=0.5',yy,size=22)
callout('What does 0.5 mean?','Before learning, the model assigns a 50% chance of label 1 to every point.')
end()

start(4,'Step 2 / Loss','How wrong are these probabilities?','Binary cross-entropy (BCE) penalizes low probability for the correct label.')
eq(r'L_i=-\left[y_i\ln(p_i)+(1-y_i)\ln(1-p_i)\right]',175,size=24)
text('ln means natural logarithm. Use ln on your calculator, not log base 10.',52,231,15,MUTED)
eq(r'L_1=-[0\ln(0.5)+1\ln(1-0.5)]=-\ln(0.5)=0.693147',258,size=20)
eq(r'L_2=-[1\ln(0.5)+0\ln(1-0.5)]=-\ln(0.5)=0.693147',311,size=20)
eq(r'L_3=-[1\ln(0.5)+0\ln(1-0.5)]=-\ln(0.5)=0.693147',364,size=20)
eq(r'J=\frac{L_1+L_2+L_3}{3}=\frac{0.693147+0.693147+0.693147}{3}=0.693147',425,size=19)
callout('Two useful shortcuts','If y = 1, use -ln(p). If y = 0, use -ln(1-p). J is the mean of all losses.')
end()

start(5,'Before the gradients','Read a derivative as sensitivity','We want to know which small changes would make the loss smaller.')
eq(r'\frac{\partial L}{\partial z}',177,size=30)
lines(['Read this as: how much does loss L change per small increase in score z?',
       'The curly symbol means a partial derivative: hold other inputs fixed.'],234,size=16)
eq(r'\mathrm{score}\ z\quad\longrightarrow\quad\mathrm{probability}\ p\quad\longrightarrow\quad\mathrm{loss}\ L',298,size=23)
lines(['For example 1 (y = 0), at p = 0.5:',
       'A small +0.01 change in z gives about +0.25 x 0.01 = +0.0025 in p.',
       'That gives about +2 x 0.0025 = +0.005 in L: the loss increases.',
       'The chain rule multiplies the two sensitivities: 2 x 0.25 = 0.5.'],360,size=16,leading=27)
callout('Next: where do 0.25 and 2 come from?', 'Use the supplied derivative rules on the next page. These changes are local estimates.')
end()

start(6,'Step 3 / Why the gradient simplifies','Where does p minus y come from?','These derivative rules are supplied; combine them using the chain rule.')
eq(r'\frac{\partial L}{\partial p}=-\frac{y}{p}+\frac{1-y}{1-p},\qquad\frac{\partial p}{\partial z}=p(1-p)',176,size=24)
eq(r'\frac{\partial L}{\partial z}=\frac{\partial L}{\partial p}\frac{\partial p}{\partial z}',244,size=25)
eq(r'=\left(-\frac{y}{p}+\frac{1-y}{1-p}\right)p(1-p)',305,size=25)
eq(r'=-y(1-p)+(1-y)p=p-y',365,size=25)
eq(r'p=0.5,\ y=0:\quad\frac{\partial L}{\partial p}=2,\quad\frac{\partial p}{\partial z}=0.25\quad\Rightarrow\quad 2(0.25)=0.5',413,size=19)
eq(r'p=0.5,\ y=1:\quad\frac{\partial L}{\partial p}=-2,\quad\frac{\partial p}{\partial z}=0.25\quad\Rightarrow\quad -2(0.25)=-0.5',449,size=19)
callout('This shortcut combines sigmoid AND BCE','The sigmoid derivative is already included. Do not multiply by p(1-p) again.')
end()

start(7,'Step 4 / Parameter gradients','How should w and b change?','J is a mean loss, so its gradient is the mean of the contributions.')
eq(r'z=wx+b\quad\Rightarrow\quad\frac{\partial z}{\partial w}=x,\quad\frac{\partial z}{\partial b}=1',174,size=22)
eq(r'\frac{\partial L_i}{\partial w}=(p_i-y_i)x_i,\qquad\frac{\partial L_i}{\partial b}=p_i-y_i',226,size=24)
text('Example',52,302,14,TEAL,True);text('Error: p - y',190,302,14,TEAL,True)
text('Weight contribution: error times input',352,302,14,TEAL,True)
for j,(err,contrib) in enumerate(zip(p-y,(p-y)*x)):
    yy=329+31*j
    text(str(j+1),70,yy,16);text(f'0.5 - {int(y[j])} = {err:+.1f}',188,yy,16)
    text(f'({err:+.1f}) x {int(x[j])} = {contrib:+.1f}',395,yy,16)
eq(r'\frac{\partial J}{\partial w}=\frac{0.5-1.0-1.5}{3}=-\frac{2}{3}',417,size=23)
eq(r'\frac{\partial J}{\partial b}=\frac{0.5-0.5-0.5}{3}=-\frac{1}{6}',480,size=23)
text('The bias contribution is the error itself because its multiplier is 1.',52,548,14,MUTED)
end()

start(8,'Step 5 / One learning update','Subtract learning rate times gradient','Both new values use gradients calculated at the OLD w and b.')
eq(r'w_{\mathrm{new}}=w-\alpha\frac{\partial J}{\partial w}',181,size=27)
eq(r'=0-0.1\left(-\frac{2}{3}\right)=\frac{1}{15}\approx 0.066667',241,size=25)
eq(r'b_{\mathrm{new}}=b-\alpha\frac{\partial J}{\partial b}',320,size=27)
eq(r'=0-0.1\left(-\frac{1}{6}\right)=\frac{1}{60}\approx 0.016667',379,size=25)
lines(['A negative gradient means a small increase in that parameter lowers mean loss.',
       'Subtracting moves in that direction; alpha controls how far we move.'],448,size=15,leading=22)
callout('One batch, one update','We used all 3 points before updating. Do not update after each row here.')
end()

start(9,'Step 6 / Check the result','Predict again with the new parameters','Keep exact fractions internally; the displayed results are rounded.')
eq(r'z_i=\frac{1}{15}x_i+\frac{1}{60},\qquad p_i=\frac{1}{1+e^{-z_i}}',174,size=24)
for j in range(3):
    yy=247+73*j
    text(f'x = {j+1}, y = {int(y[j])}',575,yy+54,14,TEAL,True)
    eq(rf'z_{j+1}=\frac{{{j+1}}}{{15}}+\frac{{1}}{{60}}\approx {znew[j]:.6f}\quad\Rightarrow\quad p_{j+1}=\frac{{1}}{{1+e^{{-{znew[j]:.6f}}}}}\approx {pnew[j]:.6f}',yy,size=20)
    loss_expr=rf'-\ln(1-{pnew[j]:.6f})' if y[j]==0 else rf'-\ln({pnew[j]:.6f})'
    eq(rf'L_{j+1}={loss_expr}\approx {lossnew[j]:.6f}',yy+36,size=19)
eq(rf'J_{{\mathrm{{new}}}}=\frac{{{lossnew[0]:.6f}+{lossnew[1]:.6f}+{lossnew[2]:.6f}}}{{3}}\approx {cost(wn,bn):.6f}',470,size=21)
text('The mean loss fell from 0.693147. Lower mean BCE is the training objective.',52,544,15,TEAL,True)
end()

start(10,'What to remember','One training step, in plain language','Use this order whenever you solve a one-feature logistic-regression question.')
steps=[('1. Score','Multiply input by weight; add bias: z = wx + b.'),
('2. Probability','Apply sigmoid: p = 1 / (1 + exp(-z)).'),
('3. Loss','Use the true label: -ln(p) for 1; -ln(1-p) for 0.'),
('4. Contributions','Calculate p - y; multiply by x for the weight gradient.'),
('5. Average','Add the 3 contributions for each parameter; divide each sum by 3.'),
('6. Update','Subtract learning rate times each mean gradient, simultaneously.')]
for j,(a,b) in enumerate(steps):
    yy=188+42*j;text(a,48,yy,16,TEAL,True);text(b,190,yy,15)
lines(['The first point\'s loss went UP, but the average loss went DOWN.',
       'One update need not improve every example or change classification accuracy.',
       'For another step, start from the NEW w and b and recompute every probability.'],459,size=15,leading=24)
text('Convention: predict label 1 when p >= 0.5. Here accuracy stays 2/3.',48,544,14,MUTED)
end()
start(11,'Try it yourself','A fresh three-point problem','Cover the next two pages and calculate one full-batch update.')
eq(r'(x_1,y_1)=(0,0),\quad(x_2,y_2)=(1,0),\quad(x_3,y_3)=(2,1)',180,size=23)
eq(r'w=0,\qquad b=0,\qquad\alpha=0.1,\qquad m=3',243,size=25)
lines(['1. Calculate every score, probability, and binary cross-entropy loss.',
       '2. Find each p - y and each (p - y)x contribution.',
       '3. Average the contributions separately for w and b.',
       '4. Update both parameters using the old gradients.',
       '5. Recompute all three probabilities and the mean loss.'],323,size=17,leading=30)
callout('Explain the signs','Do w and b move in the same direction? Explain using the two gradients.')
end()
start(12,'Worked answer / 1','Predictions, gradients, and update','At w = b = 0 every score is 0, so every probability is 0.5.')
eq(r'L_1=L_2=-\ln(1-0.5),\quad L_3=-\ln(0.5),\quad J\approx0.693147',176,size=21)
for i,(a,label) in enumerate([(0,0),(1,0),(2,1)]):
    e=.5-label
    eq(rf'p_{i+1}-y_{i+1}=0.5-{label}={e:+.1f}',233+42*i,size=20)
    eq(rf'(p_{i+1}-y_{i+1})x_{i+1}=({e:+.1f})({a})={e*a:+.1f}',233+42*i,x=405,size=20)
eq(r'\frac{\partial J}{\partial w}=\frac{0+0.5-1}{3}=-\frac{1}{6},\qquad\frac{\partial J}{\partial b}=\frac{0.5+0.5-0.5}{3}=\frac{1}{6}',368,size=23)
eq(r'w_{new}=0-0.1(-1/6)=1/60',416,size=20)
eq(r'b_{new}=0-0.1(1/6)=-1/60',448,size=20)
callout('Opposite signs, opposite moves','The negative weight gradient increases w; the positive bias gradient decreases b.')
end()
start(13,'Worked answer / 2','Check the fresh model','Use w = 1/60 and b = -1/60. Recompute; do not reuse the old probabilities.')
px=np.array([0.,1.,2.]); py=np.array([0.,0.,1.])
pz=(px-1)/60; pp=1/(1+np.exp(-pz)); pl=np.logaddexp(0,pz)-py*pz
assert abs(float(np.mean((.5-py)*px))+1/6)<1e-12
assert abs(float(np.mean(.5-py))-1/6)<1e-12
for i in range(3):
    yy=175+90*i
    eq(rf'z_{i+1}=({int(px[i])}-1)/60\approx{pz[i]:.6f},\quad p_{i+1}=1/(1+e^{{-z_{i+1}}})\approx{pp[i]:.6f}',yy,size=21)
    formula=rf'-\ln(1-{pp[i]:.6f})' if py[i]==0 else rf'-\ln({pp[i]:.6f})'
    eq(rf'y_{i+1}={int(py[i])}:\quad L_{i+1}={formula}\approx{pl[i]:.6f}',yy+39,size=21)
eq(rf'J_{{new}}=({pl[0]:.6f}+{pl[1]:.6f}+{pl[2]:.6f})/3\approx{pl.mean():.6f}',453,size=20)
callout('Common mistakes','Use probabilities in BCE; average once; update together; keep full precision until display.')
end();c.save()
print(str(pdf.resolve()))
print(json.dumps(dict(old_cost=cost(0,0),new_cost=cost(wn,bn),gradient=[dw,db])))
