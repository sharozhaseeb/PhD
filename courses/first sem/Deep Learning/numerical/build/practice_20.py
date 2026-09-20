import copy
from network_math import original,check_backward,check_forward,forward_scalar

def build_practice(E,P):
 net=original();data={'C':([0,1],1),'D':([1,-1],0)}
 R={name:check_backward(*xy) for name,xy in data.items()};pages=[]
 def add(t,b):pages.append(P(t,'Fresh practice answer: original parameters, C and D batch, learning rate 0.1.',b,'WORKED ANSWER'))
 pages.append(P('Your turn: a fresh complete training step','Reset the original fifteen parameters; these are new input examples.',[
  E(r'C:\ x=(0,1),\ t=1;\qquad D:\ x=(1,-1),\ t=0'),
  E(r'J=(\ell_C+\ell_D)/2,\qquad\eta=0.1'),
  'Calculate both complete forward passes, losses, all five deltas per example, and all fifteen parameter gradients per example. Average each gradient once, update every parameter, then recompute both complete forwards and the new mean loss.',
  'Explain which C gradients must be zero and why. Explain how D negative second input affects its first-layer weight gradients. Do not reuse A/B gradients: the inputs have changed.',
  'Stop here and attempt the problem before reading the following full worked answers.'],'INDEPENDENT PRACTICE'))
 def forwards(name,c,n,new=False):
  for l,W in enumerate(n['weights']):
   blocks=[]
   for j in range(len(W[0])):
    terms='+'.join(rf'({W[i][j]:.6f})({c["y"][l][i]:.6f})' for i in range(len(W)))
    z=c['z'][l][j];a=c['y'][l+1][j]
    blocks.extend([E(rf'z_{{{j+1}}}^{{({l+1})}}={terms}+({n["biases"][l][j]:.6f})'),E(rf'={z:.10f},\quad y_{{{j+1}}}^{{({l+1})}}=\frac{{1}}{{1+e^{{-({z:.10f})}}}}={a:.10f}')])
   if l==2:
    p=c['y'][-1][0];expr=rf'-\ln({p:.10f})' if c['target']==1 else rf'-\ln(1-{p:.10f})'
    blocks.append(E(rf'\ell_{{{name}}}={expr}={c["loss"]:.10f}'))
   blocks.append('Use this newly computed activation in the next layer; keep all digits in a calculator until the final answer.' if l<2 else 'The target enters the loss here. Keep the probability for BCE; do not replace it with a thresholded class.')
   add(f'{name}: '+('updated' if new else 'original')+f' forward, layer {l+1}',blocks)
   if new:pages[-1]['subtitle']='Fresh practice answer: updated parameters after the C/D batch step.'
 for name,r in R.items():
  forwards(name,r['cache'],net)
  d=r['deltas'][-1][0];p=r['cache']['y'][-1][0];t=data[name][1]
  add(f'{name}: output delta',[E(rf'\delta_1^{{(3)}}=y-t={p:.10f}-{t}={d:.10f}'),
   'This derivative is for one example loss. The mean factor 1/2 enters later, after each parameter gradient has been calculated.'])
  for l in [1,0]:
   for j in [0,1]:
    paths=r['paths'][l][j];a=r['cache']['y'][l+1][j];up=sum(paths)
    terms='+'.join(rf'({net["weights"][l+1][j][k]:g})({r["deltas"][l+1][k]:.10f})' for k in range(len(paths)))
    add(f'{name}: hidden layer {l+1}, neuron {j+1} delta',[
     E(rf'u={terms}'),E(rf'={"+".join(f"({p:.10f})" for p in paths)}={up:.10f}'),
     E(rf'y(1-y)={a:.10f}(1-{a:.10f})={a*(1-a):.10f}'),
     E(rf'\delta_{{{j+1}}}^{{({l+1})}}=({up:.10f})({a*(1-a):.10f})={r["deltas"][l][j]:.10f}'),
     'Here u is the incoming backward derivative: add all downstream weighted deltas, then multiply by this neuron local sigmoid slope.'])
  for l,W in enumerate(net['weights']):
   for j in range(len(W[0])):
    d=r['deltas'][l][j];blocks=[E(r'g_{w_{i,j}^{(l)}}=y_i^{(l-1)}\delta_j^{(l)}')]
    for i in range(len(W)):
     a=r['cache']['y'][l][i]
     blocks.append(E(rf'g_{{w_{{{i+1},{j+1}}}^{{({l+1})}}}}=({a:.10f})({d:.10f})={r["weights"][l][i][j]:.10f}'))
    blocks.append(E(rf'g_{{b_{{{j+1}}}^{{({l+1})}}}}=1({d:.10f})={d:.10f}'))
    blocks.append('C first input is zero, so both first-input weight gradients are zero, even though the destination deltas are nonzero.' if name=='C' and l==0 else 'D second input is -1, so its second-input gradients have the opposite sign from the destination delta.' if name=='D' and l==0 else 'Each weight uses its own source activation; the bias uses the constant source 1.')
    add(f'{name}: layer {l+1}, neuron {j+1} gradients',blocks)
 def risk(n):return sum(forward_scalar(*xy,n)['loss'] for xy in data.values())/2
 old=risk(net);add('Practice: initial mean loss',[
  E(rf'J_{{old}}=\frac{{{R["C"]["cache"]["loss"]:.10f}+{R["D"]["cache"]["loss"]:.10f}}}{{2}}={old:.10f}'),
  'We now have both example gradients at one common parameter state. Average C and D for each corresponding parameter, then subtract learning rate times that mean.'])
 new=copy.deepcopy(net);checks=[]
 for l,W in enumerate(net['weights']):
  for j in range(len(W[0])):
   blocks=[]
   for i in list(range(len(W)))+[None]:
    k='biases' if i is None else 'weights'
    def get(n):return n[k][l][j] if i is None else n[k][l][i][j]
    def put(n,v):
     if i is None:n[k][l][j]=v
     else:n[k][l][i][j]=v
    a=get(R['C']);b=get(R['D']);g=(a+b)/2;v=get(net);vn=v-.1*g;put(new,vn)
    q=rf'b_{{{j+1}}}^{{({l+1})}}' if i is None else rf'w_{{{i+1},{j+1}}}^{{({l+1})}}'
    blocks.extend([E(rf'g_{{{q}}}=\frac{{({a:.8f})+({b:.8f})}}{{2}}={g:.8f}'),E(rf'({q})_{{new}}={v:g}-0.1({g:.8f})={vn:.8f}')])
    plus=copy.deepcopy(net);minus=copy.deepcopy(net);put(plus,v+1e-6);put(minus,v-1e-6);fd=(risk(plus)-risk(minus))/2e-6;assert abs(fd-g)<1e-8
    checks.append(dict(kind=k,layer=l,source=i,destination=j,C=a,D=b,mean=g,old=v,new=vn,fd=fd))
   blocks.append('Average matching gradients; every update starts from the original state.')
   add(f'Practice: update layer {l+1}, neuron {j+1}',blocks)
 refreshed={name:check_forward(*xy,new) for name,xy in data.items()}
 for name,c in refreshed.items():forwards(name,c,new,True)
 J=risk(new)
 add('Practice: refreshed mean and readiness check',[
  E(rf'J_{{new}}=\frac{{{refreshed["C"]["loss"]:.10f}+{refreshed["D"]["loss"]:.10f}}}{{2}}={J:.10f}'),
  E(rf'\Delta J={J:.10f}-{old:.10f}={J-old:.10f}'),
  'Both examples were evaluated with all fifteen new parameters. Compare your intermediate values to locate the first mismatch, rather than changing later numbers to match the final mean.',
  'Readiness: explain every source activation, every destination delta, every branch sum, the single averaging factor, and why the second forward pass cannot reuse the old cache.'])
 pages[-1]['subtitle']='Fresh practice answer: compare the original and updated C/D batch means.'
 return pages,dict(original=R,parameters=checks,updated_parameters=new,refreshed=refreshed,old_J=old,new_J=J)
