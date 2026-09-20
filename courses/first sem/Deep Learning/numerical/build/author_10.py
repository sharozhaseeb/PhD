from pathlib import Path
import json,itertools
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'10-truth-table-boolean-network';out.mkdir(exist_ok=True)
def E(s):return {'eq':s}
def P(title,sub,blocks,stage='WORKED EXAMPLE'):return dict(title=title,subtitle=sub,blocks=blocks,stage=stage)
H=lambda s:int(s>=0);rows=list(itertools.product([0,1],repeat=3));truth={(0,0,1),(0,1,1),(1,0,0),(1,0,1)}
table=[['ABC','s001','s011','s100','s101','hidden','output']];checks=[]
for a,b,c in rows:
 ss=[-a-b+c-.5,-a+b+c-1.5,a-b-c-.5,a-b+c-1.5];hs=[H(s) for s in ss];f=H(sum(hs)-.5);assert f==int((a,b,c) in truth)
 table.append([''.join(map(str,(a,b,c))),*ss,''.join(map(str,hs)),f]);checks.append(dict(input=[a,b,c],scores=ss,hidden=hs,F=f))
def kmap(name,values,groups):
 fig,ax=plt.subplots(figsize=(7,2.1),layout='constrained');ax.set(xlim=(-.8,4.2),ylim=(-.3,2.6));ax.axis('off');cols=[(0,0),(0,1),(1,1),(1,0)]
 for j,col in enumerate(cols):ax.text(j+.5,2.3,''.join(map(str,col)),ha='center',fontsize=14)
 ax.text(-.65,2.3,'A / BC',fontsize=12)
 for a in [0,1]:
  ax.text(-.4,1.5-a,str(a),ha='center',fontsize=14)
  for j,(b,c) in enumerate(cols):
   ax.add_patch(Rectangle((j,1-a),1,1,facecolor='#edf3f7' if (a,b,c) in values else 'white',edgecolor='#172B43'));ax.text(j+.5,1.5-a,str(int((a,b,c) in values)),ha='center',va='center',fontsize=18)
 for a,left,color in groups:ax.add_patch(Rectangle((left+.06,1-a+.06),1.88,.88,fill=False,edgecolor=color,lw=3))
 fig.savefig(out/name,dpi=180);plt.close(fig)
kmap('kmap.png',truth,[(0,1,'#006E73'),(1,0,'#A25D24')]);prtruth={(0,1,0),(0,1,1),(1,0,1),(1,1,1)};kmap('practice-map.png',prtruth,[(0,2,'#006E73'),(1,1,'#A25D24')])
pages=[P('Start from a truth table','A small study example applying Lecture 2, pages 61-72; not the slide\'s five-input data.',[
'Inputs A, B and C are Boolean. Output F must be 1 on exactly four input rows.',
{'table':[['ABC','F'],*[[ ''.join(map(str,r)),int(r in truth)] for r in rows]],'widths':[160,160]},
'A literal is one input or its negation. NOT A means 1 - A for a Boolean input.']),
P('Write one AND term per true row','DNF means an OR of AND terms. The bar over a letter means NOT.',[
E(r'001:\quad t_1=\overline{A}\,\overline{B}\,C'),
E(r'011:\quad t_2=\overline{A}\,B\,C'),
E(r'100:\quad t_3=A\,\overline{B}\,\overline{C}'),
E(r'101:\quad t_4=A\,\overline{B}\,C'),
E(r'F=t_1\vee t_2\vee t_3\vee t_4'),
'Juxtaposed literals mean AND, not a new variable. A term tests all three bits; the final OR accepts any matching true row.']),
P('Turn a row detector into a neuron','For row 001, all three matching literal values must be 1.',[
E(r't_1=H((1-A)+(1-B)+C-2.5)'),
E(r'=H(2-A-B+C-2.5)=H(-A-B+C-0.5)'),
'Three matches sum to 3 and give score +0.5. Any mismatch lowers that sum to at most 2, so the score is at most -0.5.',
E(r'(w_A,w_B,w_C)=(-1,-1,1),\quad b=-0.5,\quad T=0.5'),
'Negative weights encode the negated literals directly. No separate NOT neuron is needed.',
'We use H(s) = 1 when s >= 0. Half-integer thresholds avoid ties on Boolean inputs.']),
P('The four hidden row detectors','Expand the complements in each matching-literal test in exactly the same way.',[
E(r't_1=H(-A-B+C-0.5)'),
E(r't_2=H((1-A)+B+C-2.5)=H(-A+B+C-1.5)'),
E(r't_3=H(A+(1-B)+(1-C)-2.5)=H(A-B-C-0.5)'),
E(r't_4=H(A+(1-B)+C-2.5)=H(A-B+C-1.5)'),
E(r'F=H(t_1+t_2+t_3+t_4-0.5)'),
'The output uses weights (1, 1, 1, 1) and threshold 0.5: at least one detector must fire.']),
P('Work one row through every neuron','For input 001, only its own row detector should fire.',[
E(r's_{001}=-0-0+1-0.5=0.5\Rightarrow t_1=1'),
E(r's_{011}=-0+0+1-1.5=-0.5\Rightarrow t_2=0'),
E(r's_{100}=0-0-1-0.5=-1.5\Rightarrow t_3=0'),
E(r's_{101}=0-0+1-1.5=-0.5\Rightarrow t_4=0'),
E(r'F=H(1+0+0+0-0.5)=H(0.5)=1')]),
P('Verify every canonical-network row','Scores are before H; hidden is the four-bit vector after H in detector order.',[
{'table':table,'widths':[70,85,85,85,110,100,70]},
'Detector order: 001, 011, 100, 101. A positive score becomes 1; every negative score becomes 0.',
'In each true row, hidden sums to 1 and output score is +0.5. In every false row, hidden sums to 0 and output score is -0.5.']),
P('Arrange the same table as a K-map','Columns use Gray order: 00, 01, 11, 10. Adjacent columns differ by one bit.',[
{'image':'kmap.png','width':660},
'Top pair 001/011: A = 0 and C = 1 stay fixed; B changes, so remove B.',
'Bottom pair 100/101: A = 1 and B = 0 stay fixed; C changes, so remove C.',
'Groups have power-of-two size. Adjacent edge cells may wrap around; diagonal cells are not adjacent.']),
P('The reduced expression needs two detectors','Grouping removed tests whose input can change without changing the output.',[
E(r'F=(\overline{A}\wedge C)\vee(A\wedge\overline{B})'),
E(r'h_1=H((1-A)+C-1.5)=H(-A+C-0.5)'),
E(r'h_2=H(A+(1-B)-1.5)=H(A-B-0.5)'),
E(r'F=H(h_1+h_2-0.5)'),
'h1 ignores B; h2 ignores C. Each detector now checks two literals rather than three.',
'This reduces the number of hidden neurons from four to two without changing the truth table.'])]
for start in range(0,8,2):
 blocks=[]
 for a,b,c in rows[start:start+2]:
  s1=-a+c-.5;s2=a-b-.5;h1=H(s1);h2=H(s2);fo=H(h1+h2-.5);assert fo==int((a,b,c) in truth)
  blocks.extend([E(rf'{a}{b}{c}:\quad h_1=H(-{a}+{c}-0.5)=H({s1})={h1}'),E(rf'h_2=H({a}-{b}-0.5)=H({s2})={h2}'),E(rf'F=H({h1}+{h2}-0.5)=H({h1+h2-.5})={fo}')])
 pages.append(P('Verify reduced network: rows '+str(start+1)+'-'+str(start+2),'Substitute inputs, threshold both hidden scores, then threshold their sum.',blocks))
pages += [P('Count what the simplification saved','A stored zero weight still counts as a parameter of a dense layer.',[
E(r'\mathrm{canonical:}\quad3(4)+4+4(1)+1=21'),
'Four hidden neurons each have three input weights and a bias; the output has four weights and one bias.',
E(r'\mathrm{reduced\ dense:}\quad3(2)+2+2(1)+1=11'),
E(r'\mathrm{reduced\ sparse:}\quad2+2+2+3=9'),
'The sparse version omits the unused B-to-h1 and C-to-h2 edges: six present weights plus three biases. Counts depend on how connections are stored.']),
P('Your turn: a different truth table','Set F = 1 for 010, 011, 101 and 111; set F = 0 elsewhere.',[
'1. Place all eight rows into a K-map with columns BC = 00, 01, 11, 10.',
'2. Group adjacent ones and write a reduced OR-of-ANDs expression.',
'3. Convert each term into a hidden neuron, then add an OR output.',
'4. Check all eight rows against the requested truth table.',
'Use the same H convention and half-integer thresholds.'], 'INDEPENDENT PRACTICE'),
P('Practice answer: group and translate','Each group removes the input that changes inside that group.',[
{'image':'practice-map.png','width':500},
'Top pair 010/011 keeps A = 0, B = 1: NOT A AND B. Bottom pair 101/111 keeps A = 1, C = 1: A AND C.',
E(r'F=(\overline{A}\wedge B)\vee(A\wedge C)'),
E(r'h_1=H(-A+B-0.5),\quad h_2=H(A+C-1.5)'),
E(r'F=H(h_1+h_2-0.5)')], 'WORKED ANSWER')]
practice=[['ABC','s1=-A+B-.5','s2=A+C-1.5','h1,h2','F']]
for a,b,c in rows:
 s1=-a+b-.5;s2=a+c-1.5;h1=H(s1);h2=H(s2);f=H(h1+h2-.5);assert f==int((a,b,c) in prtruth);practice.append([f'{a}{b}{c}',s1,s2,f'{h1},{h2}',f])
pages += [P('Practice answer: all eight rows','The output applies H(h1 + h2 - 0.5) to each row.',[
{'table':practice,'widths':[80,170,170,100,70]},
'Example 010: h1 = H(-0 + 1 - 0.5) = 1; h2 = H(0 + 0 - 1.5) = 0; F = H(1 + 0 - 0.5) = 1.',
'Avoid: ordinary binary column order in the map; diagonal grouping; forgetting to adjust the bias when expanding NOT literals.'], 'WORKED ANSWER')]
(out/'checks.json').write_text(json.dumps(dict(canonical=checks,practice_table=practice),indent=2))
spec=dict(number=10,title='Truth tables to Boolean networks',description='Build row detectors, verify all rows, simplify with a Karnaugh map and rebuild.',source_short='Lecture 2 / PDF pp.61-72 / original three-input example',source='Lecture 2 - Logistic Regression + Neural Network.pdf, pages 61-72. The three-input dataset is a study example.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
