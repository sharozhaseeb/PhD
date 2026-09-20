from pathlib import Path
import json, math
import numpy as np
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'32-rmsprop';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
def calc(w,grads):
 w=np.array(w,dtype=float);s=np.zeros(2);rs=[]
 for i,g in enumerate(grads,1):
  g=np.array(g,dtype=float);sn=.5*s+.5*g*g;den=np.sqrt(sn);step=.1*g/den;wn=w-step
  rs.append(dict(t=i,w=w.tolist(),s=s.tolist(),g=g.tolist(),sn=sn.tolist(),den=den.tolist(),step=step.tolist(),wn=wn.tolist()));w,s=wn,sn
 return rs
main=calc([1,1],[[2,4],[2,-4]]);practice=calc([0,0],[[1,2],[-1,2]])
pages=[P('Start with root mean square','RMS means square each value, average the squares, then take the square root.',[
 E(r'\mathrm{RMS}(a_1,\ldots,a_n)=\sqrt{\frac{a_1^2+\cdots+a_n^2}{n}}'),
 'Squaring removes signs, so large negative and positive movements both contribute. Averaging gives a mean square. The final root returns to the units of the original quantity.',
 'Lecture 5 page114 lists coordinate movements. We first compute their ordinary RMS values, then use a different, exponentially weighted calculation for RMSProp optimizer memory.',
 'The optimizer rescales each coordinate using its own recent squared gradients. The base learning rate still controls the overall size of the step.']),
P('RMS of the horizontal coordinate sequence','Use the five X components listed on lecture page114.',[
 E(r'x=(1,1,2,1,1.5)'),E(r'x^2=(1,1,4,1,2.25)'),E(r'\sum x_i^2=1+1+4+1+2.25=9.25'),E(r'\mathrm{mean\ square}=9.25/5=1.85'),E(r'\mathrm{RMS}_x=\sqrt{1.85}\approx1.360147'),
 'This is one root after averaging squares, not an average of square roots or an average of signed components.']),
P('RMS of the vertical coordinate sequence','Negative movements count positively after squaring.',[
 E(r'y=(2.5,-3,2.5,-2,1.5)'),E(r'y^2=(6.25,9,6.25,4,2.25)'),E(r'\sum y_i^2=6.25+9+6.25+4+2.25=27.75'),E(r'\mathrm{mean\ square}=27.75/5=5.55'),E(r'\mathrm{RMS}_y=\sqrt{5.55}\approx2.355844'),
 'The larger vertical RMS suggests more scaling down in that coordinate. This movement illustration motivates the optimizer; it is not its actual recursive state.']),
P('RMS is different from standard deviation','Variance first subtracts the mean; mean square does not.',[
 E(r'a=(2,2),\quad\overline{a}=2'),E(r'\mathrm{RMS}=\sqrt{(2^2+2^2)/2}=2'),E(r'\mathrm{variance}=((2-2)^2+(2-2)^2)/2=0'),E(r'\mathrm{standard\ deviation}=\sqrt{0}=0'),
 'The constant sequence has nonzero magnitude but no variation around its mean. RMS measures the former; standard deviation measures the latter.',
 'A squared gradient is also not a second derivative or a Hessian entry. Square the numerical first derivative already computed by backpropagation.']),
P('The course RMSProp recurrence','Lecture 5 page116 places epsilon inside the square root.',[
 E(r's_{t,j}=\gamma s_{t-1,j}+(1-\gamma)g_{t,j}^2'),E(r'w_{t,j}=w_{t-1,j}-\frac{\eta g_{t,j}}{\sqrt{s_{t,j}+\epsilon}}'),
 't counts updates and j identifies a parameter coordinate. g is the current averaged batch gradient. s stores an exponentially weighted history of its squares. Every multiplication and square is coordinatewise.',
 'Gamma retains old memory; 1-gamma weights the new squared gradient. Eta is the base rate. Epsilon is a positive stabilizer in implementations.',
 'Initialize s once at the start of the training run and retain it across updates. The zero-start estimate is not an unbiased second moment.']),
P('Average the current batch before squaring','Two operations that look similar give different numbers.',[
 E(r'\mathrm{example\ gradients}=(2,-2)'),E(r'g=(2+(-2))/2=0\quad\Longrightarrow\quad g^2=0'),E(r'\mathrm{mean\ of\ squares}=(2^2+(-2)^2)/2=4'),
 'For the lecture mini-batch algorithm, use the first result in the RMSProp recurrence. Its g is the already averaged batch gradient. Do not replace it with the mean of squared example gradients.',
 'Across optimizer updates, keep the squared-gradient memory. Within a batch, clear the temporary sum before averaging new example gradients.']),
P('Set up the two-coordinate optimizer exercise','The gradient vectors are supplied inputs to this state calculation.',[
 E(r'w_0=(1,1),\quad s_0=(0,0),\quad\gamma=0.5,\quad\eta=0.1'),E(r'g_1=(2,4),\qquad g_2=(2,-4)'),E(r'\epsilon=0\quad\mathrm{for\ this\ positive\ denominator\ example\ only}'),
 'These gradients are not claimed to come from a fixed quadratic. Focus on the optimizer calculation after backpropagation has produced them.',
 'Epsilon is zero only to keep these hand calculations simple; every denominator below is positive. d denotes that denominator. Keep full precision between updates; displayed values are rounded. A positive-epsilon calculation follows.'])]
def coord(r,j,answer=False):
 k=r['t'];g=r['g'][j];s=r['s'][j];sn=r['sn'][j];den=r['den'][j];step=r['step'][j];w=r['w'][j];wn=r['wn'][j]
 pages.append(P(f'{"Practice: " if answer else ""}update {k}, coordinate {j+1}','Square, update memory, take the root, then subtract the signed normalized gradient.',[
 E(rf'g={g:g},\quad g^2=({g:g})^2={g*g:g}'),E(rf's_{{new}}=0.5({s:g})+0.5({g*g:g})={sn:g}'),E(rf'd=\sqrt{{{sn:g}+0}}\approx{den:.6f}'),E(rf'\mathrm{{step}}=\frac{{0.1({g:g})}}{{\sqrt{{{sn:g}}}}}\approx{step:.6f}'),E(rf'w_{{new}}\approx{w:.6f}-({step:.6f})={wn:.6f}'),
 'The squared state stays nonnegative. The numerator keeps the gradient sign; subtracting a negative step increases the parameter.'],'WORKED ANSWER' if answer else 'WORKED EXAMPLE'))
for r in main:
 for j in range(2):coord(r,j)
pages.append(P('Read the vector states together','Each parameter retains its own squared-gradient history.',[
 {'table':[['update','g','new s','new w'],['1','(2,4)','(2,8)','(.858579,.858579)'],['2','(2,-4)','(3,12)','(.743109,.974049)']],'widths':[90,150,160,280]},
 E(r'\eta/\sqrt{s_1}=(0.1/\sqrt{2},\ 0.1/\sqrt{8})'),E(r'\approx(0.070711,\ 0.035355)'),
 'Coordinate2 has twice the first gradient magnitude but half the effective rate, so the first normalized steps are equal. This is a property of these numbers, not a universal equality.']))
pages.append(P('Expand the memory to see its weights','For gamma=.5 and a zero initial state.',[
 E(r's_1=0.5g_1^2'),E(r's_2=0.5s_1+0.5g_2^2=0.25g_1^2+0.5g_2^2'),E(r'\mathrm{coordinate\ 2}:\quad0.25(4^2)+0.5((-4)^2)=4+8=12'),
 'The latest squared gradient has weight .5; the preceding one has .25. Their weights sum to .75 because the remaining .25 multiplies the initial zero state.',
 'This is an exponential moving average, not the uniform mean of the two squares. Opposite signs do not cancel inside this squared memory. RMSProp here has no Adam-style bias correction.']))
pages.append(P('Positive epsilon changes the denominator','Use a supplied new state s=4, gradient g=2, eta=.1, and epsilon=1.',[
 E(r'\mathrm{course}:\quad d=\sqrt{4+1}=\sqrt{5}\approx2.236068'),E(r'\mathrm{step}=0.1(2)/\sqrt{5}\approx0.089443'),E(r'\mathrm{outside\ variant}:\quad d=\sqrt{4}+1=3'),E(r'\mathrm{step}=0.1(2)/3\approx0.066667'),
 'For a current parameter1, the course update gives about .910557; the outside-root variant gives .933333. These are different formulas, so declare the convention before substituting.']))
pages += [P('Why a stabilizer matters at zero','A zero new state and zero gradient should not create a division by zero.',[
 E(r's=0,\ g=0,\ \epsilon=1:\quad\mathrm{step}=0.1(0)/\sqrt{0+1}=0'),E(r'\epsilon=0:\quad0/\sqrt{0}=0/0\quad\mathrm{undefined}'),
 'The value1 is deliberately large to make the comparison visible. It is an illustration of placement and stabilization, not a recommended practical default.',
 'The main example safely omitted epsilon only because all its computed denominators were positive.']),
P('Your turn: a fresh sign-changing coordinate','Reset both parameter and memory for this separate practice run.',[
 E(r'w_0=(0,0),\quad s_0=(0,0),\quad g_1=(1,2),\quad g_2=(-1,2)'),E(r'\gamma=0.5,\quad\eta=0.1,\quad\epsilon=0'),
 'For each update and coordinate, calculate the gradient square, new memory, denominator, signed step and new parameter. Keep the first state when processing update2.',
 'Separately, compare the course and outside-root denominator for s=4, epsilon=1, and explain why RMS and standard deviation differ on [2,2].'],'INDEPENDENT PRACTICE')]
for r in practice:
 for j in range(2):coord(r,j,True)
pages.append(P('Practice checkpoint and common mistakes','All new parameters use the state computed in the same update.',[
 E(r's_1=(0.5,2),\quad w_1\approx(-0.141421,-0.141421)'),E(r's_2=(0.75,3),\quad w_2\approx(-0.025951,-0.256891)'),E(r'\sqrt{4+1}=\sqrt{5}\approx2.236068,\quad\sqrt{4}+1=3'),
 'For [2,2], RMS is 2 while standard deviation is 0: magnitude is different from spread around the mean.',
 'Avoid squaring before averaging the batch, retaining a negative sign after squaring, dropping the gradient sign in the update, using the previous s in the denominator, or resetting memory between batches.'],'WORKED ANSWER'))
assert np.allclose(main[-1]['wn'],[.743108589925,-0+ .974048697601],atol=1e-10)
assert np.allclose(practice[-1]['wn'],[-.025951302399,-.256891410075],atol=1e-10)
(out/'checks.json').write_text(json.dumps(dict(main=main,practice=practice,rms=[math.sqrt(1.85),math.sqrt(5.55)],positive_epsilon_steps=[.2/math.sqrt(5),.2/3]),indent=2))
spec=dict(number=32,title='RMSProp, one coordinate at a time',description='Calculate ordinary RMS, distinguish second moments from variance, and trace two complete two-parameter RMSProp updates with fresh practice.',source_short='Lecture 5 PDF p.114,116,118 / epsilon inside square root',source='Lecture 5 PDF pages110-118, coordinate sequence114, recurrence116 and mini-batch algorithm118. numerical-practice.md N6.5 supplied-gradient examples; arithmetic-only epsilon0 plus a positive-epsilon comparison.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
