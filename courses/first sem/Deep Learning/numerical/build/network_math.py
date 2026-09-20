"""Independent scalar and matrix checks for the shared study network."""
from pathlib import Path
import json, math
import numpy as np

def original():
    return json.loads((Path(__file__).parent/'shared-network.json').read_text())

def forward_scalar(x, target, net=None):
    net=original() if net is None else net
    ys=[list(map(float,x))];zs=[]
    for W,b in zip(net['weights'],net['biases']):
        z=[sum(W[i][j]*ys[-1][i] for i in range(len(W)))+b[j] for j in range(len(b))]
        zs.append(z);ys.append([1/(1+math.exp(-a)) for a in z])
    p=ys[-1][0];loss=-target*math.log(p)-(1-target)*math.log(1-p)
    return dict(x=list(x),target=target,z=zs,y=ys,loss=loss)

def check_forward(x,target,net=None):
    net=original() if net is None else net
    s=forward_scalar(x,target,net);a=np.array(x,dtype=float)
    for l,(W,b) in enumerate(zip(net['weights'],net['biases'])):
        z=a@np.array(W)+np.array(b);a=1/(1+np.exp(-z))
        np.testing.assert_allclose(z,s['z'][l],atol=1e-13)
        np.testing.assert_allclose(a,s['y'][l+1],atol=1e-13)
    return s

def backward_scalar(x,target,net=None):
    net=original() if net is None else net
    c=check_forward(x,target,net);ds=[None]*len(net['weights']);ds[-1]=[c['y'][-1][0]-target]
    paths=[None]*len(ds)
    for l in range(len(ds)-2,-1,-1):
        paths[l]=[[net['weights'][l+1][j][k]*ds[l+1][k] for k in range(len(ds[l+1]))] for j in range(len(c['y'][l+1]))]
        ds[l]=[sum(paths[l][j])*a*(1-a) for j,a in enumerate(c['y'][l+1])]
    gw=[[[src*d for d in ds[l]] for src in c['y'][l]] for l in range(len(ds))]
    return dict(cache=c,deltas=ds,paths=paths,weights=gw,biases=ds)

def check_backward(x,target,net=None):
    import copy
    net=original() if net is None else net
    result=backward_scalar(x,target,net);a=result['cache']['y'];md=np.array(result['deltas'][-1])
    for l in range(len(net['weights'])-1,-1,-1):
        np.testing.assert_allclose(md,result['deltas'][l],atol=1e-13)
        np.testing.assert_allclose(np.outer(a[l],md),result['weights'][l],atol=1e-13)
        if l>0:
            aa=np.array(a[l]);md=(np.array(net['weights'][l])@md)*aa*(1-aa)
    checks=[]
    for l,(W,b) in enumerate(zip(net['weights'],net['biases'])):
        indices=[('weights',i,j) for i in range(len(W)) for j in range(len(b))]+[('biases',None,j) for j in range(len(b))]
        for kind,i,j in indices:
            plus=copy.deepcopy(net);minus=copy.deepcopy(net);h=1e-6
            if kind=='weights':
                plus[kind][l][i][j]+=h;minus[kind][l][i][j]-=h;g=result[kind][l][i][j]
            else:
                plus[kind][l][j]+=h;minus[kind][l][j]-=h;g=result[kind][l][j]
            fd=(forward_scalar(x,target,plus)['loss']-forward_scalar(x,target,minus)['loss'])/(2*h)
            assert abs(fd-g)<1e-8,(kind,l,i,j,g,fd)
            checks.append(dict(kind=kind,layer=l+1,source=i,destination=j,analytic=g,finite_difference=fd))
    result['finite_differences']=checks
    return result
