from pathlib import Path
import json, math, itertools
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'30-sgd-rates-variance';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
pages=[P('Two different questions about SGD','How fast can an objective gap shrink, and how noisy is a sample mean?',[
 'Part A works through the step-size conditions and rate expressions in Lecture5 pages56-58 and86. Part B calculates the variance of sampled losses from pages65-66 and85.',
 'All constants and tiny distributions below are chosen study examples. The rate calculations use stipulated mathematical bounds, not measured predictions for your neural network.',
 'An update changes parameters once. An example-gradient evaluation computes one training example contribution. These counts differ for full batches, SGD and mini-batches.',
 'For the sampling calculations, freeze the parameters first. Otherwise the loss distribution itself changes while you measure it.']),
P('Read the two infinite-sum conditions','Lecture5 page56; index k starts at 1 in this lesson.',[
 E(r'\eta_k=\frac{c}{k^p},\quad c>0,\quad k=1,2,3,\ldots'),
 E(r'\sum_{k=1}^{\infty}\eta_k=\infty,\qquad\sum_{k=1}^{\infty}\eta_k^2<\infty'),
 'An infinite sum is the limiting total of more and more terms. The first condition says accumulated step sizes never reach a finite ceiling; the second says accumulated squared step sizes do.',
 'These are step-size conditions within convergence theorems. Such theorems also require suitable objective regularity, controlled iterates and gradient-noise assumptions, such as unbiased estimates with bounded variance.',
 'A convex objective supports conclusions different from a general nonconvex neural-network loss. These two sums alone do not guarantee a local minimum or global search.']),
P('Apply the p-series test to both sums','The series 1/k raised to exponent a has a finite sum exactly when a>1.',[
 E(r'\sum\eta_k=c\sum\frac{1}{k^p}\quad\Longrightarrow\quad\mathrm{diverges\ if}\ p\leq1'),
 E(r'\sum\eta_k^2=c^2\sum\frac{1}{k^{2p}}\quad\Longrightarrow\quad\mathrm{finite\ if}\ 2p>1'),
 E(r'2p>1\Longrightarrow p>\frac{1}{2};\qquad\frac{1}{2}<p\leq1'),
 'Multiplying a positive series by the finite positive constant c or c squared does not change whether it converges. Both tests must pass at the same time.',
 'The lower endpoint is excluded; the upper endpoint is included.']),
P('Check the endpoints instead of guessing','A smaller rate is not automatically a suitable rate.',[
 {'table':[['p','sum of rates','sum of squared rates','both?'],['0.5','exponent .5: infinite','exponent 1: infinite','no'],['0.75','exponent .75: infinite','exponent 1.5: finite','yes'],['1','exponent 1: infinite','exponent 2: finite','yes'],['2','exponent 2: finite','exponent 4: finite','no']],'widths':[65,230,280,95],'size':13},
 E(r'p=1:\quad \eta_k=c/k,\qquad\eta_k^2=c^2/k^2'),
 'At p=.5 the squared sequence is harmonic, so its sum still diverges. At p=2 the rates shrink so quickly that their total is finite.']),
P('Geometric shrinking fails the first sum','Choose eta_k=c(0.9)^k with k starting at 1.',[
 E(r'\sum_{k=1}^{\infty}c(0.9)^k=\frac{0.9c}{1-0.9}=9c<\infty'),
 E(r'\sum_{k=1}^{\infty}c^2(0.81)^k=\frac{0.81c^2}{1-0.81}=\frac{81}{19}c^2'),
 'Both totals are finite. The square-sum condition passes, but the required divergent sum of rates fails.',
 'This does not say geometric decay is never useful in finite training. It says this schedule does not meet this particular pair of infinite-horizon conditions.']),
P('Turn an inverse gap bound into an update count','Define gap as objective value minus its optimal value.',[
 E(r'\mathrm{gap}_k=J(w_k)-J^*,\qquad\mathrm{gap}_k\leq\frac{2}{k}'),
 E(r'\frac{2}{k}\leq0.01\Longrightarrow2\leq0.01k\Longrightarrow k\geq200'),
 E(r'k=199:\ 2/199\approx0.0100503>0.01'),
 E(r'k=200:\ 2/200=0.01'),
 'J* is the best objective value in the stated optimization problem. The bound guarantees the requested tolerance from update200 onward under its assumptions; actual convergence could be earlier.']),
P('Solve a geometric bound using logarithms','Assume instead gap_k <= 2(0.8)^k.',[
 E(r'2(0.8)^k\leq0.01\Longrightarrow(0.8)^k\leq0.005'),
 E(r'k\ln(0.8)\leq\ln(0.005)'),
 E(r'k\geq\frac{\ln(0.005)}{\ln(0.8)}\approx23.7432\Longrightarrow k_{min}=24'),
 'Taking natural logs preserves the inequality because log increases. Dividing by ln(.8), which is negative, reverses the inequality. Round up to a whole update.',
 E(r'2(0.8)^{23}\approx0.0118059,\qquad2(0.8)^{24}\approx0.00944473')]),
P('Fewer updates can still mean more example work','Illustration: assign the inverse bound to SGD and geometric bound to full gradient.',[
 E(r'T=100\ \mathrm{training\ examples}'),
 E(r'\mathrm{SGD}:\quad200\ \mathrm{updates}\times1=200\ \mathrm{example\ gradients}'),
 E(r'\mathrm{full}:\quad24\ \mathrm{updates}\times100=2400\ \mathrm{example\ gradients}'),
 'T is dataset size. These counts follow the stipulated bounds and cost model; they are not a measured comparison or a claim that one optimizer always wins.',
 'Vectorized and parallel computations change elapsed time. Equal update counts, equal example work and equal runtime are three different comparisons.']),
P('Rewrite the mini-batch expression at equal work','Lecture5 page86 gives O(1/sqrt(bk) + 1/k).',[
 E(r'R(b,k)=\frac{1}{\sqrt{bk}}+\frac{1}{k}'),
 'Big-O describes scale up to constants in a stated regime. For arithmetic only, R sets both hidden coefficients to1; it is not an exact measured gap or a universal numerical bound.',
 E(r'M=bk\Longrightarrow k=M/b'),
 E(r'R=\frac{1}{\sqrt{b(M/b)}}+\frac{1}{M/b}=\frac{1}{\sqrt{M}}+\frac{b}{M}'),
 'b is batch size, k is updates, and M is example-gradient work. The substitution keeps total work fixed when batch size changes.']),
P('Evaluate both terms separately','Hold M=10,000 example-gradient evaluations fixed.',[
 E(r'b=25:\quad k=10000/25=400'),
 E(r'R=1/\sqrt{10000}+25/10000=0.01+0.0025=0.0125'),
 E(r'b=100:\quad k=10000/100=100'),
 E(r'R=1/\sqrt{10000}+100/10000=0.01+0.01=0.02'),
 'The first term is unchanged at equal M; the second grows with b. This expression alone does not establish the slide\'s blanket square-root-of-b degradation in total work, nor a hardware-time prediction.']),
P('A tiny population of losses','Keep parameters fixed and draw a fresh example independently.',[
 E(r'P(D=1)=P(D=3)=\frac{1}{2}'),
 'D is the random loss from one example. Expectation is its probability-weighted mean. Variance is its mean squared distance from that mean.',
 E(r'\mu=\mathbb{E}[D]=\frac{1}{2}(1)+\frac{1}{2}(3)=2'),
 E(r'\sigma^2=\mathrm{Var}(D)=\frac{1}{2}(1-2)^2+\frac{1}{2}(3-2)^2=1'),
 E(r'\sigma=\sqrt{\sigma^2}=1'),
 'Standard deviation is the square root of variance and has the same units as the loss. Variance has squared units.']),
P('Enumerate every two-draw mini-batch','Independent draws allow repeats; each ordered pair has probability 1/4.',[
 {'table':[['D1','D2','mean (D1+D2)/2','squared distance from2'],['1','1','1','1'],['1','3','2','0'],['3','1','2','0'],['3','3','3','1']],'widths':[75,75,245,285]},
 E(r'\mathbb{E}[\overline{D}]=(1+2+2+3)/4=2'),
 E(r'\mathrm{Var}(\overline{D})=(1+0+0+1)/4=0.5'),
 E(r'\mathrm{SD}(\overline{D})=\sqrt{0.5}\approx0.707107'),
 'The mean remains2 but the sample mean varies less. Variance .5 is not standard deviation .5.']),
P('See how averaging concentrates probability','This is a sampling distribution at fixed parameters, not a training curve.',[
 {'image':'sampling.png','width':650},
 'A single draw never equals2. The mean of two draws equals2 half the time. It can still be1 or3, but those outcomes become less likely.']),
P('Why independent batch variance divides by b','Every draw has the same variance sigma squared and is independent of the others.',[
 E(r'\overline{D}=\frac{1}{b}\sum_{i=1}^{b}D_i'),
 E(r'\mathrm{Var}(\overline{D})=\frac{1}{b^2}\mathrm{Var}\left(\sum_{i=1}^bD_i\right)'),
 E(r'=\frac{1}{b^2}\sum_{i=1}^{b}\sigma^2=\frac{b\sigma^2}{b^2}=\frac{\sigma^2}{b}'),
 'Scaling by 1/b scales squared deviations by 1/b squared. Covariance measures how deviations of two draws vary together. Independence makes these cross terms zero, so variances add.',
 E(r'\mathbb{E}[\overline{D}]=\mu,\qquad\mathrm{SD}(\overline{D})=\frac{\sigma}{\sqrt{b}}')]),
P('Calculate variance and standard deviation separately','Suppose a single-example loss has variance9.',[
 E(r'\sigma^2=9\Longrightarrow\sigma=\sqrt{9}=3'),
 E(r'b=9:\quad\mathrm{Var}(\overline{D})=9/9=1,\quad\mathrm{SD}=\sqrt{1}=1'),
 E(r'b=100:\quad\mathrm{Var}(\overline{D})=9/100=0.09'),
 E(r'\mathrm{SD}=\sqrt{0.09}=0.3'),
 'A hundred independent draws reduce variance by100 and standard deviation by10. These are different factors because one measure is squared.']),
P('Without replacement is a different experiment','The complete fixed dataset is [1,3]; select both members.',[
 E(r'\overline{D}=(1+3)/2=2\quad\mathrm{every\ time}'),
 E(r'\mathrm{Var}(\overline{D})=0'),
 'The earlier independent draws allowed (1,1) and (3,3). Selecting both distinct dataset members does not. There is no remaining randomness in the mean.',
 E(r'\sigma_{pop}^2=((1-2)^2+(3-2)^2)/2=1'),
 'The population variance here uses divisor N=2. This is the spread of the fixed dataset, not an estimated sample variance with divisor N-1.']),
P('Optional: finite-population correction','For a uniform subset of b distinct examples from a fixed dataset of size N>1.',[
 E(r'\mathrm{Var}(\overline{D})=\frac{\sigma_{pop}^2}{b}\frac{N-b}{N-1}'),
 E(r'N=2,\ b=2:\quad\frac{1}{2}\frac{2-2}{2-1}=0'),
 E(r'N=2,\ b=1:\quad\frac{1}{1}\frac{2-1}{2-1}=1'),
 'This supporting sampling formula is an extension. The factor (N-b)/(N-1) accounts for dependence caused by sampling without replacement.',
 'Unbiased risk estimation at a fixed parameter does not imply unbiased test performance after choosing parameters using those same data. Training changes parameters and selection uses the observed losses.'],'OPTIONAL EXTENSION'),
P('Your turn: schedules and bound arithmetic','Solve before reading the answer pages.',[
 'For eta_k=c/k^p with k>=1, test p=.4,.6,1,1.1 against both infinite-sum conditions. Show the exponent of each squared sequence.',
 E(r'\mathrm{gap}\leq3/k\quad\mathrm{or}\quad\mathrm{gap}\leq3(0.5)^k'),
 'Under each separate stipulated bound, find the smallest whole update count sufficient for gap<=.03. Check the preceding update.',
 'Evaluate the illustrative R=1/sqrt(M)+b/M with M=1600 and b=16. Show k and each term.'],'INDEPENDENT PRACTICE'),
P('Your turn: a fresh loss distribution','Keep parameters fixed; loss0 and loss4 each have probability1/2.',[
 'Calculate the mean, variance and standard deviation of one draw, and of the mean of four independent draws.',
 'For a direct check, let j be the number of loss4 draws out of four. The 16 equally likely ordered outcomes have counts1,4,6,4,1 for j=0,1,2,3,4. Calculate each sample mean and then its variance.',
 'If the entire fixed dataset [0,4] is selected without replacement, what is the mean and its variance? Explain the difference from independent draws.'],'INDEPENDENT PRACTICE'),
P('Answer: test each exponent twice','The accepted interval is 1/2<p<=1.',[
 {'table':[['p','p<=1?','squared exponent 2p>1?','both'],['.4','yes','.8: no','no'],['.6','yes','1.2: yes','yes'],['1','yes','2: yes','yes'],['1.1','no','2.2: yes','no']],'widths':[80,160,320,100]},
 E(r'p=0.6\ \mathrm{and}\ p=1'),
 'At p=.4 the first sum diverges as required, but the squared sum also diverges. At1.1 the squared sum converges, but the rate sum also converges.'],'WORKED ANSWER'),
P('Answer: inverse and geometric counts','These are sufficient counts under the two supplied bounds.',[
 E(r'3/k\leq0.03\Longrightarrow k\geq3/0.03=100'),
 E(r'3/99\approx0.030303>0.03,\quad3/100=0.03'),
 E(r'3(0.5)^k\leq0.03\Longrightarrow(0.5)^k\leq0.01'),
 E(r'k\geq\ln(0.01)/\ln(0.5)\approx6.64386\Longrightarrow k_{min}=7'),
 E(r'3(0.5)^6=0.046875,\quad3(0.5)^7=0.0234375'),
 'Again, division by a negative logarithm reverses the inequality. The integer ceiling means round up.'],'WORKED ANSWER'),
P('Answer: equal work and one-draw variability','Keep arithmetic for work counts separate from sampling variability.',[
 E(r'k=M/b=1600/16=100'),
 E(r'R=1/\sqrt{1600}+16/1600=1/40+0.01=0.035'),
 E(r'\mu=0.5(0)+0.5(4)=2'),
 E(r'\sigma^2=0.5(0-2)^2+0.5(4-2)^2=4'),
 E(r'\sigma=\sqrt{4}=2'),
 'The loss distribution has the same mean2 as the main example but twice its standard deviation.'],'WORKED ANSWER'),
P('Answer: four independent draws','If j draws have loss4, the mean is (4j)/4=j.',[
 {'table':[['j / sample mean','number of outcomes','probability','(mean-2)^2'],['0','1','1/16','4'],['1','4','4/16','1'],['2','6','6/16','0'],['3','4','4/16','1'],['4','1','1/16','4']],'widths':[160,190,150,170],'row_height':25},
 E(r'\mathbb{E}[\overline{D}]=(0+4+12+12+4)/16=2'),
 E(r'\mathrm{Var}(\overline{D})=(4+4+0+4+4)/16=1'),
 E(r'\mathrm{SD}=1\qquad\mathrm{also}:\quad\sigma^2/b=4/4=1')],'WORKED ANSWER'),
P('Answer: a full dataset has no sampling uncertainty','Without replacement, taking both members of [0,4] fixes its mean.',[
 E(r'\overline{D}=(0+4)/2=2,\qquad\mathrm{Var}(\overline{D})=0'),
 'A fixed full-dataset mean can still differ from the population risk. Zero randomness from selecting this entire dataset is not a promise of zero estimation error relative to the real world.',
 'Exam checklist: identify update versus example count; keep the logarithm inequality direction correct; distinguish a stated bound from big-O scale; name the sampling procedure; freeze parameters; take a square root only when asked for standard deviation.'],'WORKED ANSWER')]
fig,axs=plt.subplots(1,2,figsize=(9.5,3),layout='constrained')
for ax,probs,title in zip(axs,[[.5,0,.5],[.25,.5,.25]],['Single draw D','Two-draw mean']):
 ax.bar([1,2,3],probs,color='#147d92',width=.5);ax.set(xticks=[1,2,3],ylim=(0,.6),xlabel='loss or mean loss',ylabel='probability',title=title);ax.grid(axis='y',alpha=.2)
fig.savefig(out/'sampling.png',dpi=180);plt.close(fig)
pairs=list(itertools.product([1,3],repeat=2));means=[sum(x)/2 for x in pairs]
fresh=[sum(x)/4 for x in itertools.product([0,4],repeat=4)]
assert sum((x-2)**2 for x in means)/4==.5
assert sum((x-2)**2 for x in fresh)/16==1
assert math.ceil(math.log(.005)/math.log(.8))==24
assert math.ceil(math.log(.01)/math.log(.5))==7
(out/'checks.json').write_text(json.dumps(dict(main_pairs=pairs,means=means,fresh_means=fresh,main_geometric_count=24,practice_geometric_count=7),indent=2))
spec=dict(number=30,title='SGD rates, work and variance',description='Step-size sums, bound arithmetic, equal-work comparisons and fully enumerated loss distributions with fresh practice.',source_short='Lecture5 PDF p.56-58,65-66,85-86 / explicit theoretical assumptions',source='Lecture5 PDF pages40-59,60-74,85-86. Chosen examples follow numerical-practice.md N6.2/N6.3; finite-population correction is a labeled supporting extension.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
