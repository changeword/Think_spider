import numpy as np
from numpy.random import randn
from numpy.linalg import inv, qr
import matplotlib
import matplotlib.pyplot as plt
import math
import random

def nlSamples(n = 100):
    t = np.arange(0, 1.0, 1.0 / n)
    y = [ti + 0.3 * math.sin(2 * math.pi * ti)+random.random()*0.01  for ti in t]
    t = list(t)
    return [t, y]


def bFLR(x, y, rank = 10):
    x = np.matrix(x)
    if x.shape[0] == 1:
        x = x.transpose()
    y = np.matrix(y)
    if y.shape[0] == 1:
        y = y.transpose()
    one = np.ones((x.shape[0], 1))
    tmp = np.zeros((x.shape[0], rank))
    for i in range(rank):
        tmp[:,i] = np.power(x.A, i + 1).transpose()
    xx = np.hstack([one, tmp])
    w = inv((xx.transpose()).dot(xx)).dot(np.transpose(xx)).dot(y)
    return w

def plotBFLR(w, x, y, rank = 10):
    xx = [i for i in np.arange(0.0,1.0,1.0/20)]
    w = w.A.transpose()
    yy = [w.dot(xlist(i, rank))[0,0] for i in xx]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y, 'ro')
    ax.plot(xx,yy)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(str(rank) + ' order regression')
    plt.legend(('training sampes','regression line'))
    plt.show()

def xlist(i, rank):
    l = [np.power(i ,ii) for ii in range(rank+1)]
    l = np.array([l]).transpose()
    return l

plotBFLR(bFLR(nlSamples()[0],nlSamples()[1]),nlSamples()[0],nlSamples()[1])
