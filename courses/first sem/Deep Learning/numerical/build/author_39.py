from pathlib import Path
from fractions import Fraction as F
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_lesson import render
out=Path(__file__).resolve().parent.parent/'39-classification-metrics';out.mkdir(exist_ok=True)
def E(s):return {'eq':s,'size':22}
def P(t,s,b,stage='WORKED EXAMPLE'):return dict(title=t,subtitle=s,blocks=b,stage=stage)
def classify(t,p):
 pred=[int(x>=.5) for x in p]
 names=[('TP' if a else 'FP') if b else ('FN' if a else 'TN') for a,b in zip(t,pred)]
 return pred,names,{k:names.count(k) for k in ['TP','FN','FP','TN']}
t=[1,0,1,0,0,1,0,0];p=[.9,.7,.4,.1,.2,.8,.6,.3];digits=[0,7,0,2,8,0,9,4]
pred,names,counts=classify(t,p)
ft=[1,1,1,1,0,0,0,0];fp=[.5,.7,.3,.1,.6,.2,.4,.1];fpr,fn,fc=classify(ft,fp)
pages=[P('Measure whether the model detects digit zero','Assignment 1 PDF page 4: MNIST digit 0 versus every other digit.',[
 'Positive means the class we want to detect: the image contains digit 0. The assignment encodes that class as target t=1. All other digits are encoded as t=0.',
 E(r'\mathrm{digit}\ 0\Longrightarrow t=1;\qquad\mathrm{digits}\ 1\ldots9\Longrightarrow t=0'),
 'Do not confuse the original digit value 0 with the encoded negative label 0. We will evaluate eight supplied study predictions, not actual measured MNIST results.',
 'A confusion matrix counts correct and incorrect decisions. Accuracy, precision, recall and F1 summarize different aspects of those counts.']),
P('Turn each probability into one class decision','Use the explicit study convention: equality at 0.5 predicts positive.',[
 E(r'p=\hat y=\mathrm{predicted\ probability\ of\ class}\ 1'),E(r'p\geq0.5\Longrightarrow\hat t=1;\qquad p<0.5\Longrightarrow\hat t=0'),
 'The assignment specifies a threshold of 0.5. This example explicitly assigns an exact tie to class 1. A probability and a thresholded class are different quantities.',
 E(r'p=0.9\geq0.5\Longrightarrow\hat t=1'),E(r'p=0.4<0.5\Longrightarrow\hat t=0'),
 'Compare the predicted class with the known target only after applying the threshold. Do not round probabilities before thresholding.']),
P('Name the four possible outcomes','True or false describes correctness; positive or negative describes the prediction.',[
 {'table':[['actual t','predicted class','name','meaning'],['1','1','TP','correctly detected zero'],['1','0','FN','missed a zero'],['0','1','FP','false alarm: nonzero called zero'],['0','0','TN','correctly rejected nonzero']],'widths':[90,140,90,370]},
 'TP = true positive; FN = false negative; FP = false positive; TN = true negative. Each example belongs to exactly one category.',
 'A false positive is a positive prediction that is wrong. A false negative is a negative prediction that is wrong.']),
P('Classify all eight examples, one row at a time','The original digit helps keep the positive-class encoding visible.',[
 {'table':[['ID','digit','target t','p','decision','outcome']]+[[str(i+1),str(digits[i]),str(t[i]),str(p[i]),str(pred[i]),names[i]] for i in range(8)],'widths':[65,80,105,90,130,140],'row_height':26},
 'Rows 1 and 6 detect zeros; row 3 misses a zero. Rows 2 and 7 are false alarms. Rows 4, 5 and 8 correctly reject nonzero digits.']),
P('Collect the counts before computing any metric','Actual positives and predicted positives need not be the same examples.',[
 E(r'TP=2,\quad FN=1,\quad FP=2,\quad TN=3'),E(r'N=TP+FN+FP+TN=2+1+2+3=8'),E(r'\mathrm{actual\ positives}=TP+FN=2+1=3'),E(r'\mathrm{predicted\ positives}=TP+FP=2+2=4'),
 'There are 3 actual zeros and 5 actual nonzeros: positive proportion 3/8 and negative proportion 5/8. These are the study sample proportions, not the full MNIST proportions.']),
P('Read the confusion matrix with its axes','Rows are actual classes; columns are predicted classes.',[
 {'image':'matrix.png','width':590},
 'Read across an actual-class row to see what happened to that class. Read down a predicted-class column to see which actual examples received that prediction.']),
P('Accuracy: what fraction of all decisions is correct?','Both correctly detected zeros and correctly rejected nonzeros count.',[
 E(r'\mathrm{accuracy}=\frac{TP+TN}{TP+FN+FP+TN}'),E(r'=\frac{2+3}{2+1+2+3}=\frac{5}{8}=0.625=62.5\%'),
 'Five of the eight predictions are correct. The denominator includes every example; accuracy does not separately show whether either class is neglected.',
 'Check: the correct IDs are 1, 4, 5, 6 and 8. Counting these directly gives the same numerator 5.']),
P('Precision: how reliable are positive predictions?','Restrict attention to the four examples that the model called zero.',[
 E(r'\mathrm{precision}=\frac{TP}{TP+FP}'),E(r'=\frac{2}{2+2}=\frac{2}{4}=0.5=50\%'),
 'Predicted-positive IDs are 1, 2, 6 and 7. Only IDs 1 and 6 are actual zeros. Half the model alarms are correct.',
 'The denominator is the predicted-positive group, not the actual-positive group. False positives reduce precision.']),
P('Recall: what fraction of actual zeros is detected?','Restrict attention to the three examples that really are zero.',[
 E(r'\mathrm{recall}=\frac{TP}{TP+FN}'),E(r'=\frac{2}{2+1}=\frac{2}{3}\approx0.666667=66.6667\%'),
 'Actual-positive IDs are 1, 3 and 6. The model detects IDs 1 and 6 but misses ID 3. It finds two of the three zeros.',
 'The denominator is the actual-positive group. False negatives reduce recall. Precision and recall answer different questions even though both use TP in the numerator.']),
P('F1: combine precision and recall','F1 is their harmonic mean, not their ordinary arithmetic average.',[
 E(r'F_1=\frac{2PR}{P+R},\qquad P=\frac{1}{2},\quad R=\frac{2}{3}'),E(r'2PR=2\left(\frac{1}{2}\right)\left(\frac{2}{3}\right)=\frac{2}{3}'),E(r'P+R=\frac{1}{2}+\frac{2}{3}=\frac{3}{6}+\frac{4}{6}=\frac{7}{6}'),E(r'F_1=\frac{2/3}{7/6}=\frac{2}{3}\times\frac{6}{7}=\frac{4}{7}\approx0.571429'),
 'The ordinary average would be 7/12, a different number. F1 emphasizes having both useful precision and useful recall.']),
P('Compute the same F1 directly from counts','Substituting the precision and recall definitions simplifies the formula.',[
 E(r'F_1=\frac{2TP}{2TP+FP+FN}'),E(r'=\frac{2(2)}{2(2)+2+1}=\frac{4}{7}\approx57.1429\%'),
 'The direct-count form agrees with the harmonic form when both are defined. It is also useful in some edge cases where precision itself is undefined.',
 'TN does not appear in this positive-class F1 formula. Many correctly rejected negatives can raise accuracy without rescuing missed positives.']),
P('The same accuracy can hide a failed detector','Compare with a baseline that predicts negative for every example.',[
 E(r'TP=0,\quad FN=3,\quad FP=0,\quad TN=5'),E(r'\mathrm{accuracy}=\frac{0+5}{8}=62.5\%'),E(r'\mathrm{recall}=\frac{0}{0+3}=0;\qquad F_1=\frac{0}{0+0+3}=0'),
 'This baseline has exactly the same accuracy as our model, yet detects none of the three zeros. Its five correct decisions come entirely from the five nonzero images.',
 'Precision is 0/(0+0), which is undefined mathematically: there are no positive predictions to assess. Do not describe this as a measured precision of zero without declaring a reporting convention.']),
P('Handle empty denominators explicitly','A zero numerator is not the same as a zero denominator.',[
 'If actual positives exist but none are predicted: precision is undefined, recall is zero, and direct-count F1 is zero. The harmonic formula cannot be evaluated using an undefined precision.',
 E(r'TP=FP=FN=0\Longrightarrow F_1=\frac{0}{0}\quad\mathrm{undefined}'),
 'If truth and prediction are both entirely negative, there are no actual or predicted positives. Precision, recall and positive-class F1 are all undefined by their mathematical fractions.',
 'Software may replace undefined scores with zero or another stated convention. Report the convention alongside the counts. Never silently divide by zero.']),
P('Your turn: include the exact threshold tie','Use the same positive class and predict 1 when p is at least 0.5.',[
 {'table':[['ID','target t','p'],['1','1','.5'],['2','1','.7'],['3','1','.3'],['4','1','.1'],['5','0','.6'],['6','0','.2'],['7','0','.4'],['8','0','.1']],'widths':[140,220,220],'row_height':24},
 'Write every predicted class and outcome, build the matrix with labeled axes, then compute accuracy, precision, recall and F1. Keep fractions until the last step.'],'INDEPENDENT PRACTICE'),
P('Answer: threshold, compare, then count','The first probability is exactly 0.5, so its prediction is positive.',[
 {'table':[['ID','target','p','prediction','outcome']]+[[str(i+1),str(ft[i]),str(fp[i]),str(fpr[i]),fn[i]] for i in range(8)],'widths':[90,100,100,160,160],'row_height':25},
 E(r'TP=2,\quad FN=2,\quad FP=1,\quad TN=3')],'WORKED ANSWER'),
P('Answer: matrix and accuracy','The practice set has four actual positives and four actual negatives.',[
 {'table':[['actual / predicted','positive 1','negative 0','row total'],['positive 1','TP = 2','FN = 2','4'],['negative 0','FP = 1','TN = 3','4'],['column total','3','5','8']],'widths':[240,150,150,150]},
 E(r'\mathrm{accuracy}=\frac{TP+TN}{N}=\frac{2+3}{8}=\frac{5}{8}=62.5\%'),
 'There are three positive predictions, of which two are correct. There are four actual positives, of which two are detected.'],'WORKED ANSWER'),
P('Answer: precision, recall and F1','Apply each denominator to the correct group.',[
 E(r'P=\frac{2}{2+1}=\frac{2}{3}\approx66.6667\%'),E(r'R=\frac{2}{2+2}=\frac{1}{2}=50\%'),E(r'F_1=\frac{2(2)}{2(2)+1+2}=\frac{4}{7}\approx57.1429\%'),E(r'\frac{2PR}{P+R}=\frac{2(2/3)(1/2)}{2/3+1/2}=\frac{2/3}{7/6}=\frac{4}{7}'),
 'Compared with the main example, precision and recall trade values, but F1 stays the same. They are symmetric inputs to the harmonic mean.'],'WORKED ANSWER'),
P('A second quiz: start from supplied counts','A different model has TP=6, TN=8, FP=2 and FN=4.',[
 'Compute the total number of examples and all four metrics. State the number of actual positives and the number of predicted positives before substituting.',
 'Explain why swapping FP and FN would exchange precision and recall while leaving accuracy and F1 unchanged.',
 'Do this without reading the next page. These counts are a new independent example, not extra rows appended to either earlier dataset.'],'INDEPENDENT PRACTICE'),
P('Answer: supplied counts to all four metrics','Check every denominator before simplifying.',[
 E(r'N=6+8+2+4=20;\quad TP+FN=10;\quad TP+FP=8'),E(r'\mathrm{accuracy}=\frac{6+8}{20}=\frac{14}{20}=0.7'),E(r'P=\frac{6}{6+2}=\frac{6}{8}=0.75;\qquad R=\frac{6}{6+4}=\frac{6}{10}=0.6'),E(r'F_1=\frac{2(6)}{2(6)+2+4}=\frac{12}{18}=\frac{2}{3}'),E(r'\frac{2PR}{P+R}=\frac{2(0.75)(0.6)}{0.75+0.6}=\frac{0.9}{1.35}=\frac{2}{3}'),
 'Swapping FP and FN exchanges the two denominators for precision and recall. Their sum in F1 and the total in accuracy do not change.'],'WORKED ANSWER'),
P('A reliable exam workflow','Class definition, threshold, counts, denominators, interpretation.',[
 '1. Write which real-world class is positive and its encoded label. For this assignment, digit 0 is positive label 1.',
 '2. State the threshold and exact-tie rule. Convert each probability into a class once, without premature rounding.',
 '3. Compare with truth, count TP/FN/FP/TN, and check that counts sum to the number of examples. Label both confusion-matrix axes.',
 '4. Use all examples for accuracy, predicted positives for precision, actual positives for recall, and the harmonic/direct-count formula for F1.',
 '5. Check zero denominators and explain what the scores mean. Accuracy alone can hide failure on the class of interest.'])]
fig,ax=plt.subplots(figsize=(8.5,3.7),layout='constrained');ax.axis('off')
rows=[['actual / predicted','positive 1','negative 0','row total'],['positive 1','TP = 2','FN = 1','3'],['negative 0','FP = 2','TN = 3','5'],['column total','4','4','8']]
tab=ax.table(cellText=rows,loc='center',cellLoc='center',colWidths=[.32,.23,.23,.22]);tab.auto_set_font_size(False);tab.set_fontsize(12);tab.scale(1,2.4)
for (r,c),cell in tab.get_celld().items():
 cell.set_edgecolor('#147d92');cell.set_facecolor('#eaf3f7' if r==0 or c==0 else 'white')
fig.savefig(out/'matrix.png',dpi=180);plt.close(fig)
def metrics(c):
 a,b,d,e=c['TP'],c['FN'],c['FP'],c['TN'];return dict(accuracy=str(F(a+e,a+b+d+e)),precision=str(F(a,a+d)),recall=str(F(a,a+b)),F1=str(F(2*a,2*a+d+b)))
assert counts==dict(TP=2,FN=1,FP=2,TN=3)
assert fc==dict(TP=2,FN=2,FP=1,TN=3)
(out/'checks.json').write_text(json.dumps(dict(main=dict(predictions=pred,outcomes=names,counts=counts,metrics=metrics(counts)),fresh=dict(predictions=fpr,outcomes=fn,counts=fc,metrics=metrics(fc)),challenge=metrics(dict(TP=6,FN=4,FP=2,TN=8))),indent=2))
spec=dict(number=39,title='Classification metrics from every prediction',description='Threshold probabilities, build a labeled confusion matrix, and compute accuracy, precision, recall and F1 with two fully worked practice problems.',source_short='Assignment 1 PDF p.4 / numerical-practice N5.2 / supplied study predictions',source='Assignment 1 PDF page 4: digit 0 is positive target 1, threshold 0.5, report accuracy, precision, recall, F1 and confusion matrix. Exact tie assigned positive as explicit study convention. numerical-practice.md N5.2.',pages=pages)
(out/'lesson.json').write_text(json.dumps(spec,indent=2));render(out/'lesson.json')
