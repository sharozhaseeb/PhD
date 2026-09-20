"""Reusable independent numerical checks for authored lessons."""
import numpy as np

def finite_difference(cost, parameters, gradient, step=1e-6, atol=1e-7):
    parameters=np.asarray(parameters,dtype=float)
    actual=[]
    for i in range(parameters.size):
        plus=parameters.copy();minus=parameters.copy()
        plus.flat[i]+=step;minus.flat[i]-=step
        actual.append((cost(plus)-cost(minus))/(2*step))
    actual=np.array(actual).reshape(parameters.shape)
    np.testing.assert_allclose(actual,gradient,atol=atol,rtol=1e-6)
    return actual.tolist()

def half_mse(design, targets, parameters):
    residual=np.asarray(design)@np.asarray(parameters)-np.asarray(targets)
    return float(np.mean(residual**2)/2)

def regression_gradient(design,targets,parameters):
    design=np.asarray(design);targets=np.asarray(targets)
    return design.T@(design@parameters-targets)/len(targets)
