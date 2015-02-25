__author__ = 'arenduchintala'
from math import exp, log, pi, sqrt
import copy
import numpy as np
import pdb

global punc
punc = set(", . ? ! : ' \" ".split())


def normpdf(x, mean, sd):
    var = float(sd) ** 2
    denom = (2 * pi * var) ** .5
    num = exp(-(float(x) - float(mean)) ** 2 / (2 * var))
    return num / denom


def flatten_backpointers(bt):
    reverse_bt = []
    while len(bt) > 0:
        x = bt.pop()
        reverse_bt.append(x)
        if len(bt) > 0:
            bt = bt.pop()
    reverse_bt.reverse()
    return reverse_bt


def logadd(x, y):
    """
    trick to add probabilities in logspace
    without underflow
    """
    if x == 0.0 and y == 0.0:
        return log(exp(x) + exp(y))  # log(2)
    elif x >= y:
        return x + log(1 + exp(y - x))
    else:
        return y + log(1 + exp(x - y))


def logadd_of_list(a_list):
    logsum = a_list[0]
    for i in a_list[1:]:
        logsum = logadd(logsum, i)
    return logsum


def sign_difference(v1, v2):
    assert len(v1) == len(v2)
    assert isinstance(v1, np.ndarray)
    assert isinstance(v2, np.ndarray)
    diff = 0.0
    for k in xrange(len(v1)):
        if v1[k] > 0 and v2[k] > 0:
            pass
        elif v1[k] < 0 and v2[k] < 0:
            pass
        else:
            diff += 1.0
    return diff, len(v1)


def cosine_sim(v1, v2):
    assert len(v1) == len(v2)
    assert isinstance(v1, np.ndarray)
    assert isinstance(v2, np.ndarray)
    dot = 0.0
    v1_sq = 0.0
    v2_sq = 0.0
    for i in xrange(len(v1)):
        dot += v1[i] * v2[i]
        v1_sq += v1[i] ** 2.0
        v2_sq += v2[i] ** 2.0
    denom = (sqrt(v1_sq) * sqrt(v2_sq))
    if denom > 0.0:
        return dot / denom
    else:
        return float('inf')


def gradient_checking(theta, eps, val):
    f_approx = np.zeros(np.shape(theta))
    for i, t in enumerate(theta):
        theta_plus = copy.deepcopy(theta)
        theta_minus = copy.deepcopy(theta)
        theta_plus[i] = theta[i] + eps
        theta_minus[i] = theta[i] - eps
        f_approx[i] = (val(theta_plus) - val(theta_minus)) / (2 * eps)
    return f_approx


def R(h, ref):
    hnr = len(h.intersection(ref))
    r = len(ref)
    if r == 0.0:
        return 0.0
    return float(hnr) / r


def P(h, ref):
    hnr = len(h.intersection(ref))
    h = len(h)
    if h == 0.0:
        return 0.0
    return float(hnr) / h


def get_meteor_score(h, ref, alpha=0.5):
    global punc
    h = set(h.split()) - punc
    ref = set(ref.split()) - punc
    prec = P(h, ref)
    recall = R(h, ref)
    if recall == 0 and prec == 0:
        return 0.0
    return prec * recall / (((1 - alpha) * recall) + (alpha * prec))


if __name__ == '__main__':
    v1 = np.array([float(l.split()[-1]) for l in open('v1', 'r').readlines() if l[0] != '#'])
    v2 = np.array([float(l.split()[-1]) for l in open('v2', 'r').readlines() if l[0] != '#'])
    print 'difference v1-v2'
    print 'cosine sim', cosine_sim(v1, v2)
    print 'sign diff ', sign_difference(v1, v2)
