from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from render_lesson import render
out=Path(__file__).resolve().parent.parent/'21-gradient-hessian-stationary-points';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('A slope tells us which way changes the loss','Use two parameters x and y, collected into the vector w = (x,y).',[
 E(r'E(x,y)=1.5x^2+xy+1.5y^2'),
 'A partial derivative measures change when one parameter moves and the other stays fixed. The gradient collects these slopes into a vector.',
 E(r'\nabla E=\left(\frac{\partial E}{\partial x},\frac{\partial E}{\partial y}\right)'),
 'Curvature means how a slope itself changes as we move. The Hessian collects derivatives of gradient components. Our tuples list those components; the notes write the gradient as a column vector.',
 'This original study example is N4.3. It has the quadratic form on Lecture4 PDF page37 with A equal to its Hessian, and b = 0, c = 0.']),
 P('Differentiate one parameter at a time','Treat the other parameter as a constant.',[
 E(r'\frac{\partial E}{\partial x}=1.5(2x)+y+0=3x+y'),
 'For the xy term, y behaves like a fixed coefficient when x changes. The y-squared term is constant with respect to x.',
 E(r'\frac{\partial E}{\partial y}=0+x+1.5(2y)=x+3y'),
 E(r'\nabla E(2,0)=(3(2)+0,\ 2+3(0))=(6,2)'),
 'At (2,0), increasing x a little increases E about 6 times that increment; increasing y a little increases E about 2 times that increment.']),
 P('Check what those slopes mean numerically','Small changes connect a derivative to something you can calculate.',[
 E(r'E(2,0)=1.5(4)+0+0=6'),
 E(r'E(2.01,0)=1.5(2.01)^2=6.06015'),
 E(r'\Delta E=0.06015\approx 6(0.01)=0.06'),
 E(r'E(2,0.01)=6+2(0.01)+1.5(0.01)^2=6.02015'),
 E(r'\Delta E=0.02015\approx 2(0.01)=0.02'),
 'The slight difference is the quadratic curvature contribution. A derivative is a local rate, not an exact finite-change formula.']),
 P('Differentiate the slopes to form the Hessian','Rows name the gradient component; columns name the parameter being changed.',[
 {'table':[['','differentiate by x','differentiate by y'],['gradient x: 3x+y','Hxx = 3','Hxy = 1'],['gradient y: x+3y','Hyx = 1','Hyy = 3']],'widths':[240,220,220]},
 'Thus H has rows (3,1) and (1,3). The off-diagonal 1 values come from the mixed term xy: moving y changes the x-slope, and moving x changes the y-slope.',
 E(r'\Delta x=0.01\quad\Longrightarrow\quad\Delta(3x+y)=3(0.01)=0.03'),
 E(r'\Delta y=0.01\quad\Longrightarrow\quad\Delta(3x+y)=1(0.01)=0.01'),
 'These slope changes are exact here because the gradient is linear. The Hessian is constant for this quadratic.']),
 P('Find a stationary point before classifying it','Stationary means every first derivative is zero.',[
 E(r'3x+y=0,\qquad x+3y=0'),
 E(r'y=-3x\quad\Longrightarrow\quad x+3(-3x)=-8x=0'),
 E(r'x=0,\qquad y=-3(0)=0'),
 'A zero gradient says the first-order slope vanishes. It does not tell us whether the point is a minimum, maximum or saddle.',
 'To distinguish them, inspect how the function curves in different directions near that point.']),
 P('Eigenvalues describe directional curvature','An eigenvector is a nonzero direction v for which H v = lambda v.',[
 'The matrix changes the length or sign of this direction, without rotating it to another line. Lambda is the corresponding scale factor. For a unit direction, it is the quadratic curvature.',
 'I is the identity matrix: diagonal entries 1 and off-diagonal entries 0. H - lambda I therefore has rows (3-lambda,1) and (1,3-lambda).',
 'For a 2-by-2 matrix with rows (a,b) and (c,d), its determinant is ad-bc. Set this determinant to zero to find the possible eigenvalues.',
 E(r'\det(H-\lambda I)=(3-\lambda)(3-\lambda)-1(1)=0'),
 E(r'(3-\lambda)^2=1\quad\Longrightarrow\quad\lambda=2\ \mathrm{or}\ 4')]),
 P('Verify both eigenvector directions by multiplication','These two independent directions account for the whole two-parameter space.',[
 E(r'H(1,-1)=(3(1)+1(-1),\ 1(1)+3(-1))'),
 E(r'=(2,-2)=2(1,-1)'),
 E(r'H(1,1)=(3(1)+1(1),\ 1(1)+3(1))'),
 E(r'=(4,4)=4(1,1)'),
 'Both eigenvalues are positive. This is called positive definite: every nonzero direction has positive quadratic curvature. At our stationary point, that establishes a strict local minimum. Local compares nearby points; strict means every different nearby point is higher. Global compares the entire domain.']),
 P('Normalize directions before comparing curvature','A unit direction has length 1, so the movement coordinate measures distance.',[
 E(r'u_-=(1,-1)/\sqrt{2},\quad u_+=(1,1)/\sqrt{2}'),
 E(r'E(tu_-)=t^2,\qquad E(tu_+)=2t^2'),
 {'image':'curvature.png','width':590},
 'The second derivatives with respect to distance t are 2 and 4, exactly the eigenvalues. Using unnormalized (1,1) would give E=4t-squared and second derivative 8 because each unit of t moves farther.']),
 P('Maxima curve down; saddles mix directions','Evaluate nearby points to see the distinction directly.',[
 E(r'M(x,y)=-E(x,y),\quad\nabla M(0,0)=0'),
 'Its Hessian is -H with eigenvalues -2 and -4. Both are negative, so (0,0) is a strict maximum of M.',
 E(r'S(x,y)=\frac{x^2-y^2}{2},\quad\nabla S=(x,-y)'),
 'At (0,0), the gradient is zero and the Hessian is diagonal (1,-1). One curvature is positive, the other negative: the Hessian is indefinite.',
 E(r'S(0,0)=0,\quad S(0.1,0)=0.005,\quad S(0,0.1)=-0.005'),
 'Nearby values occur above and below zero, so the origin is a saddle, not a minimum or maximum.']),
 P('A zero Hessian can leave the test inconclusive','Use the original function when second-order information is insufficient.',[
 E(r'T(x,y)=x^4+y^4,\quad\nabla T=(4x^3,4y^3)'),
 'The Hessian has diagonal entries 12x-squared and 12y-squared, with zero off-diagonal entries. At (0,0), every Hessian entry is zero.',
 E(r'\nabla T(0,0)=(0,0),\qquad\lambda_1=\lambda_2=0'),
 'The second-order test is inconclusive. It does not say there is no minimum.',
 E(r'T(x,y)\geq 0=T(0,0)'),
 'Fourth powers are nonnegative and both vanish only at the origin. This direct argument proves a strict global minimum.']),
 P('Your turn: classify two fresh functions','Find gradients, Hessians, stationary points and curvature signs.',[
 E(r'Q(x,y)=2x^2+xy+2y^2,\qquad R(x,y)=-x^2-2y^2'),
 'For Q, also calculate the gradient at (1,-1), solve the two-by-two eigenvalue equation, and verify one eigenvector direction.',
 'For R, explain why the stationary point is a maximum even though its gradient is zero, just like the minimum of Q.',
 'State whether zero Hessian eigenvalues always mean a flat function. Use T from the preceding page to support your answer.'],'INDEPENDENT PRACTICE'),
 P('Practice Q: derivatives and stationary point','Differentiate each term while holding the other variable fixed.',[
 E(r'Q_x=2(2x)+y=4x+y,\qquad Q_y=x+2(2y)=x+4y'),
 E(r'\nabla Q(1,-1)=(4(1)-1,\ 1+4(-1))=(3,-3)'),
 'Differentiate these slopes: H has rows (4,1) and (1,4). The mixed term contributes 1 to each off-diagonal entry.',
 E(r'4x+y=0\Rightarrow y=-4x'),
 E(r'x+4(-4x)=-15x=0\Rightarrow(x,y)=(0,0)')],'WORKED ANSWER'),
 P('Practice Q: eigenvalues and classification','Use the determinant and then check an actual direction.',[
 E(r'\det(H-\lambda I)=(4-\lambda)^2-1=0'),
 E(r'4-\lambda=\pm1\quad\Longrightarrow\quad\lambda=3,5'),
 E(r'H(1,-1)=(4-1,\ 1-4)=(3,-3)=3(1,-1)'),
 'Both eigenvalues are positive. The Hessian is positive definite, so the stationary origin is a strict local minimum.',
 E(r'Q(x,y)=1.5(x^2+y^2)+0.5(x+y)^2\geq0'),
 'The last expression also proves it is the global minimum: all terms are nonnegative and vanish together only at the origin.'] ,'WORKED ANSWER'),
 P('Practice R: downward curvature and common errors','Stationarity and classification are separate questions.',[
 E(r'\nabla R=(-2x,-4y)=(0,0)\Rightarrow(x,y)=(0,0)'),
 'Its Hessian is diagonal (-2,-4), so its eigenvalues are -2 and -4. Both are negative: the origin is a strict maximum.',
 E(r'R(x,y)=-x^2-2y^2\leq0=R(0,0)'),
 'Zero eigenvalues do not imply the function is constant or that no minimum exists. T=x-to-the-fourth+y-to-the-fourth has zero curvature exactly at its minimum but grows away from it.',
 'Common errors: treating the other variable as zero instead of constant, omitting mixed derivatives, calling every zero-gradient point a minimum, or using an unnormalized direction as distance.'],'WORKED ANSWER')]
pages.insert(7,P('Derive the two directional curves','Substitute the coordinates of each unit direction into the original function.',[
 E(r'x=t/\sqrt{2},\quad y=-t/\sqrt{2}'),
 E(r'E=1.5(t^2/2)-t^2/2+1.5(t^2/2)=t^2'),
 E(r'x=t/\sqrt{2},\quad y=t/\sqrt{2}'),
 E(r'E=1.5(t^2/2)+t^2/2+1.5(t^2/2)=2t^2'),
 E(r'\frac{d^2(t^2)}{dt^2}=2,\qquad\frac{d^2(2t^2)}{dt^2}=4'),
 'The sign of xy changes between the directions; the two square terms stay the same. This is why the same surface has different curvature along different directions.']))
fig,ax=plt.subplots(figsize=(9,2.5),layout='constrained');t=np.linspace(-1.5,1.5,300);ax.plot(t,t*t,label='unit direction (1,-1) / sqrt(2): curvature 2',color='#006E73');ax.plot(t,2*t*t,label='unit direction (1,1) / sqrt(2): curvature 4',color='#BD6A24');ax.set(xlabel='signed distance t from stationary origin',ylabel='E along direction');ax.legend(fontsize=9);ax.grid(alpha=.2);fig.savefig(out/'curvature.png',dpi=170);plt.close(fig)
H=np.array([[3.,1.],[1.,3.]])
assert np.allclose(np.linalg.eigvalsh(H),[2,4])
assert np.allclose(np.linalg.eigvalsh([[4,1],[1,4]]),[3,5])
f=lambda w:1.5*w[0]**2+w[0]*w[1]+1.5*w[1]**2
g=lambda w:np.array([3*w[0]+w[1],w[0]+3*w[1]])
fd=[]
for w in [np.array([2.,0.]),np.array([.3,-.7])]:
 for j in range(2):
  d=np.eye(2)[j]*1e-5
  numerical=(f(w+d)-f(w-d))/(2e-5)
  assert abs(numerical-g(w)[j])<1e-8
  assert np.allclose((g(w+d)-g(w-d))/(2e-5),H[:,j])
  fd.append(float(numerical))
checks=dict(gradient=['3*x+y','x+3*y'],hessian=H.tolist(),eigenvalues=[2,4],practice_eigenvalues=[3,5],stationary=[0,0],finite_differences=fd)
(out/'checks.json').write_text(json.dumps(checks,indent=2))
spec=dict(number=21,title='Gradient, Hessian and stationary points',description='Differentiate a two-parameter function, compute curvature directions, and classify minima, maxima and saddles with full practice answers.',source_short='L3 PDF p.115-132 / L4 PDF p.37-49 / N4.3',source='Lecture3 PDF pages115-121: derivatives/Hessian, pages122-132: stationary points; Lecture4 PDF pages37-49: multivariate quadratics; numerical-practice.md N4.3. Original numerical examples.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
