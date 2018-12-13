import numpy as np
from numpy.random import randn
from numpy.linalg import inv, qr
import matplotlib
import matplotlib.pyplot as plt
import math
import random


def linearSamples(n = 20):
    a = 0.5
    b = 1.0
    r = [i + 2.0*random.random() for i in range(n)]
    return [range(0, len(r)), r]

def lR(x, y):
    x = np.matrix(x)
    if x.shape[0] == 1:
        x = x.transpose()
    y = np.matrix(y)
    if y.shape[0] == 1:
        y = y.transpose()
    one = np.ones((x.shape[0], 1))
    x = np.hstack([one, x])
    w = inv((x.transpose()).dot(x)).dot(np.transpose(x)).dot(y)
    return w

def plotLM(w, x,y):
    xx = [i for i in np.arange(0.0,20.0,0.5)]
    yy = [w[0,0] + w[1,0] * i for i in xx]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y, '.')
    ax.plot(xx,yy)
    s = 'y = %s + %s * x' %(str(w[0,0])[0:7], str(w[1, 0])[0:7])
    ax.annotate(s, xy=(12.5, 13.3),  xycoords='data',
                xytext=(-180, 30), textcoords='offset points',
                bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=90,rad=10"))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(('training sampes','regression line'))
    plt.show()



plotLM(lR(linearSamples()[0],linearSamples()[1]),linearSamples()[0],linearSamples()[1])