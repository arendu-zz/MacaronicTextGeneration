# -*- coding: latin1 -*-
__author__ = 'arenduchintala'
import numpy as np
from optparse import OptionParser
import pdb


insertion_cost = np.log(0.33)
deletion_cost = np.log(0.33)
substitution_cost = np.log(0.34)


def edscore(a, b):
    ed = editdistance(a, b)
    edr = ed / float(max(len(a), len(b)))
    return 1.0 - edr


def editdistance(a, b):
    table = np.zeros((len(a) + 1, len(b) + 1))
    # table = np.ones((len(a) + 1, len(b) + 1))
    for i in range(len(a) + 1):
        table[i, 0] = i  # i
    for j in range(len(b) + 1):
        table[0, j] = j  # j
    # print 'start'
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                table[i, j] = table[i - 1, j - 1]
            else:
                # print i, j
                diag = table[i - 1, j - 1] + 1  # substitution cost
                # print 'diag', diag
                left = table[i - 1, j] + 1  # deletion cost
                # print 'left', left
                top = table[i, j - 1] + 1  # insertion cost
                # print 'top', top
                best = min(diag, top, left)

                # print 'best so far', best, diag, top, left
                table[i, j] = best
                # print 'current cell', table[i, j]
    # print table
    return table[i, j]


def editdistance_prob(a, b):
    table = np.zeros((len(a) + 1, len(b) + 1))
    # table = np.ones((len(a) + 1, len(b) + 1))
    for i in range(len(a) + 1):
        table[i, 0] = insertion_cost * i  # i
    for j in range(len(b) + 1):
        table[0, j] = deletion_cost * j  # j
    # print 'start'
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                table[i, j] = table[i - 1, j - 1]
            else:
                # print i, j
                diag = table[i - 1, j - 1] + substitution_cost  # substitution cost
                # print 'diag', diag
                left = table[i - 1, j] + deletion_cost  # deletion cost
                # print 'left', left
                top = table[i, j - 1] + insertion_cost  # insertion cost
                # print 'top', top
                # best = min(diag, top, left)
                best = max(diag, top, left)

                # print 'best so far', best, diag, top, left
                table[i, j] = best
                # print 'current cell', table[i, j]
    # print table
    return table[i, j]


if __name__ == "__main__":
    x = "one two three".split()  # "ALTRUISM"
    y = "one bw two three".split()  # "PLASMA"
    ed = editdistance(x, y)
    edp = editdistance_prob(x, y)
    print 'ed', ed, ' ed_prob', np.exp(edp)
    # edr = edscore(x, y)
    # print 'final edr', edr


