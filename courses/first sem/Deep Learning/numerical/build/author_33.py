from pathlib import Path
from fractions import Fraction as F
import json, math
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'33-adam';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
def trace(gs):
 m=v=F(0);w=1.;rs=[]
 for t,g in enumerate(gs,1):
  om,ov=m,v;m=F(9,10)*m+F(1,10)*g;v=F(999,1000)*v+F(1,1000)*g*g
  c1=1-F(9,10)**t;c2=1-F(999,1000)**t;mh=m/c1;vh=v/c2;den=math.sqrt(float(vh));step=.1*float(mh)/den;nw=w-step
  rs.append(dict(t=t,g=g,om=float(om),ov=float(ov),m=float(m),v=float(v),c1=float(c1),c2=float(c2),mh=float(mh),vh=float(vh),den=den,step=step,w=w,nw=nw));w=nw
 return rs
main=trace([2,-1]);practice=trace([-2,-2])
pages=[P('Adam remembers direction and squared magnitude','The same parameter has two memories and one global update counter.',[
 'm is an exponential moving average of signed gradients. v is an exponential moving average of squared gradients. A hat marks a value corrected for zero initialization.',
 'In the momentum lessons, v meant signed parameter displacement. In this Adam lesson, v has a different meaning: squared-gradient memory. Neither m nor Adam v is the actual parameter displacement.',
 E(r'\mathrm{slide}\ \delta\longleftrightarrow\beta_1,\qquad\gamma\longleftrightarrow\beta_2'),
 'Lecture 5 pages 121-122 use delta and gamma for the two decay factors. We use beta1 and beta2 to match the usual Adam notation.',
 'Initialize m, v and the update counter once. Keep all three across batches and epochs.']),
P('Read the raw and corrected moment formulas','First average the current batch gradient, then square that result for v.',[
 E(r'm_t=\beta_1m_{t-1}+(1-\beta_1)g_t'),E(r'v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2'),E(r'\widehat m_t=\frac{m_t}{1-\beta_1^t},\qquad\widehat v_t=\frac{v_t}{1-\beta_2^t}'),
 'The powers use the global update number t, starting at 1. Correction removes the moments\' startup bias toward zero; this is unrelated to a network bias parameter b. The second moment is uncentered, not a variance or a Hessian.',
 E(r'\mathrm{batch}\ (2,-2):\quad g=0,\ g^2=0\ne(2^2+(-2)^2)/2=4')]),
P('Use the course denominator convention','The square-root bar includes epsilon in the lecture equation.',[
 E(r'w_t=w_{t-1}-\eta\frac{\widehat m_t}{\sqrt{\widehat v_t+\epsilon}}'),
 'Eta is still the base learning rate. Epsilon stabilizes the denominator. A common alternative places epsilon outside the root; we compare them numerically later.',
 E(r'w_0=1,\quad m_0=v_0=0,\quad\beta_1=0.9,\quad\beta_2=0.999'),E(r'\eta=0.1,\quad g_1=2,\quad g_2=-1,\quad\epsilon=0'),
 'The gradients are supplied inputs, not claimed to come from a fixed objective. Epsilon 0 is used only for these positive-denominator hand calculations. Keep full precision between steps.'])]
def worked(r,answer=False):
 t=r['t'];g=r['g'];prefix='Practice: ' if answer else '';stage='WORKED ANSWER' if answer else 'WORKED EXAMPLE'
 pages.append(P(f'{prefix}update {t}: raw moments','Retain the previous raw moments, not their corrected versions.',[
 E(rf'g_{t}={g},\qquad g_{t}^2=({g})^2={g*g}'),E(rf'm_{t}=0.9({r["om"]:g})+0.1({g})={r["m"]:g}'),E(rf'v_{t}=0.999({r["ov"]:g})+0.001({g*g})={r["v"]:g}'),
 'The signed gradient can reduce or reverse m. Its square is nonnegative, so opposite signs do not cancel in v.',
 E(rf'\mathrm{{save\ raw}}:\quad(m_{t},v_{t})=({r["m"]:g},{r["v"]:g})')],stage))
 pages.append(P(f'{prefix}update {t}: bias correction','Evaluate each power before subtracting from 1.',[
 E(rf'1-\beta_1^{t}=1-0.9^{t}={r["c1"]:g}'),E(rf'1-\beta_2^{t}=1-0.999^{t}={r["c2"]:g}'),E(rf'\widehat m_{t}=\frac{{{r["m"]:g}}}{{{r["c1"]:g}}}\approx{r["mh"]:.9f}'),E(rf'\widehat v_{t}=\frac{{{r["v"]:g}}}{{{r["c2"]:g}}}\approx{r["vh"]:.9f}'),
 'The two decay factors produce different correction denominators. Use both corrected values in the parameter update. Keep the raw values for the next recurrence.'],stage))
 pages.append(P(f'{prefix}update {t}: denominator and parameter','d denotes the positive denominator; step is the signed quantity subtracted.',[
 E(rf'd=\sqrt{{\widehat v_{t}+0}}\approx\sqrt{{{r["vh"]:.9f}}}\approx{r["den"]:.9f}'),E(rf'\mathrm{{step}}=\frac{{0.1\widehat m_{t}}}{{d}}\approx\frac{{0.1({r["mh"]:.9f})}}{{{r["den"]:.9f}}}'),E(rf'\mathrm{{step}}\approx{r["step"]:.9f}'),E(rf'w_{t}\approx{r["w"]:.9f}-({r["step"]:.9f})={r["nw"]:.9f}'),
 'A negative step increases the parameter because it is subtracted. A positive step decreases it. The sign comes from the corrected first moment, not directly from the latest gradient.'],stage))
for r in main:worked(r)
pages += [P('The latest gradient changed sign, but m did not','At update 2, old positive history outweighs the new negative contribution.',[
 E(r'm_2=0.9(0.2)+0.1(-1)=0.18-0.1=0.08>0'),E(r'\widehat m_2=0.08/0.19>0'),E(r'w_2\approx0.9-0.026633704=0.873366296'),
 'The new gradient is negative, but the retained first moment is positive. Adam still subtracts a positive step in this update.',
 'A supplied gradient sequence is enough to trace optimizer state. Without a declared objective, it does not establish that each parameter update lowers the loss.']),
P('Why dividing by 1 minus beta to the t helps','For this illustration, suppose the same scalar gradient g is repeated.',[
 E(r'm_0=0,\quad m_1=(1-\beta)g'),E(r'm_2=\beta(1-\beta)g+(1-\beta)g=(1-\beta^2)g'),E(r'm_t=(1-\beta^t)g\quad\Longrightarrow\quad m_t/(1-\beta^t)=g'),
 'The initial zero leaves the exponential weights summing to less than 1. Dividing by their total removes that zero-start attenuation. The same calculation applies to repeated g squared for the second moment.',
 'For random gradients with a stationary expectation, the correction removes this initialization bias in expectation. It does not make an arbitrary changing sequence equal to its latest gradient.']),
P('Two common correction errors','Use the power of beta, not the power of its complement.',[
 E(r'1-0.9^2=1-0.81=0.19'),E(r'(1-0.9)^2=0.1^2=0.01\quad\mathrm{different}'),E(r'\mathrm{uncorrected\ first\ step}=0.1(0.2)/\sqrt{0.004}\approx0.316228'),E(r'\mathrm{corrected\ first\ step}=0.1(2)/\sqrt{4}=0.1'),
 'Omitting both corrections does not make them cancel: the first and second decay factors differ, and the second moment is under a square root.',
 'Do not restart t at an epoch boundary. In a new training run, reset t and both moment states together.']),
P('Positive epsilon: the placement is visible','Use corrected moments m-hat=2 and v-hat=4, eta=.1, epsilon=1.',[
 E(r'\mathrm{course\ step}=\frac{0.1(2)}{\sqrt{4+1}}\approx0.089443'),E(r'\mathrm{alternative\ step}=\frac{0.1(2)}{\sqrt{4}+1}\approx0.066667'),E(r'w_{old}=1:\quad w_{course}\approx0.910557,\quad w_{alternative}\approx0.933333'),
 'The course puts epsilon inside the root. The comparison uses a deliberately visible epsilon value, not a recommended default.',
 'With both corrected moments zero, positive epsilon yields a zero step; epsilon 0 would make the ratio 0/0 undefined.']),
P('Your turn: repeat a negative gradient','Start a separate run from the original initial state.',[
 E(r'w_0=1,\quad m_0=v_0=0,\quad(g_1,g_2)=(-2,-2)'),E(r'\beta_1=0.9,\quad\beta_2=0.999,\quad\eta=0.1,\quad\epsilon=0'),
 'For both updates, calculate raw moments, correction denominators, corrected moments, final denominator, signed step and new parameter. Work the second update using retained raw states.',
 'Explain why the corrected second moment can equal 4 while the variance of the constant sequence [-2,-2] is 0. Then identify where to add a positive epsilon under the lecture convention.'],'INDEPENDENT PRACTICE')]
for r in practice:worked(r,True)
pages.append(P('Practice checkpoint: magnitude is not variability','The two repeated negative gradients are a useful bias-correction check.',[
 E(r'm_1=-0.2,\quad v_1=0.004,\quad m_2=-0.38,\quad v_2=0.007996'),E(r'\widehat m_1=\widehat m_2=-2,\quad\widehat v_1=\widehat v_2=4'),E(r'w_1=1-(-0.1)=1.1,\quad w_2=1.1-(-0.1)=1.2'),E(r'\mathrm{variance}=((-2-(-2))^2+(-2-(-2))^2)/2=0'),
 'The squared-gradient level is 4, but deviation around its constant mean is 0. Adam uses the former. With positive epsilon, its course denominator is sqrt(v-hat + epsilon).'],'WORKED ANSWER'))
assert abs(main[-1]['nw']-.873366296477)<1e-8
assert abs(practice[-1]['nw']-1.2)<1e-12
(out/'checks.json').write_text(json.dumps(dict(main=main,practice=practice,arithmetic='Exact Fraction raw moments and corrections; floating square roots',positive_epsilon_steps=[.2/math.sqrt(5),.2/3]),indent=2))
spec=dict(number=33,title='Adam moments and bias correction',description='Calculate raw moments, correction powers, denominator and parameter updates through a gradient sign change; solve a fresh complete two-step practice.',source_short='Lecture 5 PDF p.121-122 / epsilon inside root; global update count',source='Lecture 5 PDF pages119-124, equations121-122. Slide delta maps to beta1 and gamma to beta2. numerical-practice.md N6.6 supplied-gradient examples, with positive-epsilon convention comparison.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
