# -*- coding: utf8 -*-
__author__ = 'arenduchintala'
import numpy as np
from optparse import OptionParser
import pdb
import traceback
from pprint import pprint


class EditDistance(object):
    def __init__(self, word2vec_file):

        self.word2vec = {}
        self.a = []
        self.b = []
        if word2vec_file is not None:
            self.loadw2v(word2vec_file)


    def edscore(self, a, b):
        ed = self.editdistance(a, b)
        edr = ed / float(max(len(a), len(b)))
        return 1.0 - edr

    def alignmentdistance(self, a, b):
        self.a = a
        self.b = b
        null_threshold = 5e-1
        alignments = {}
        for tb in b:
            align = (tb, '<eps>')
            align_max = null_threshold
            for ta in a:
                cs = self.cosine_sim(self.word2vec[tb.lower()], self.word2vec[ta.lower()])
                if cs > align_max:
                    align = (tb, ta)
                    align_max = cs
                else:
                    pass
            alignments[align] = align_max
        return alignments.keys()


    def editdistance(self, a, b):
        self.a = a
        self.b = b
        substitution_penalty = 5e-1
        inset_penalty = 5e-1
        delete_penalty = 5e-1
        table = np.zeros((len(a) + 1, len(b) + 1), dtype=float)
        came_from = {}
        # table = np.ones((len(a) + 1, len(b) + 1))
        for i in range(len(a) + 1):
            table[i, 0] = delete_penalty ** i  # i
            came_from[i, 0] = (i - 1, 0), (a[i - 1], '<eps>')

        for j in range(len(b) + 1):
            table[0, j] = inset_penalty ** j  # j
            came_from[0, j] = (0, j - 1), ('<eps>', b[j - 1])

        # print 'start'
        for i in range(1, len(a) + 1):
            for j in range(1, len(b) + 1):
                if a[i - 1] == b[j - 1]:
                    diag = table[i - 1, j - 1] * 1.0
                else:
                    if a[i - 1].lower() in self.word2vec and b[j - 1].lower() in self.word2vec:
                        cs = self.cosine_sim(self.word2vec[a[i - 1].lower()], self.word2vec[b[j - 1].lower()])
                        # print cs, a[i - 1], b[j - 1]
                    else:
                        cs = substitution_penalty
                    diag = table[i - 1, j - 1] * cs  # substitution cost
                top = table[i, j - 1] * inset_penalty  # insertion cost
                left = table[i - 1, j] * delete_penalty  # deletion cost

                best, prev, tok = max((diag, (i - 1, j - 1), (a[i - 1], b[j - 1])),
                                      (top, (i, j - 1), ('<eps>', b[j - 1])),
                                      (left, (i - 1, j), (a[i - 1], '<eps>')))

                table[i, j] = best
                came_from[i, j] = (prev, tok)
                # print 'current cell', table[i, j]
        # print table

        alignments = self.bt(came_from)
        return table[i, j], alignments

    def bt(self, cf):
        i = len(self.a)
        j = len(self.b)
        alignments = []
        while not (i == 0 and j == 0):
            prev, tok = cf[i, j]
            alignments.append((tok[0], tok[1]))  # this is an alignment
            i = prev[0]
            j = prev[1]
        alignments.reverse()
        return alignments


    def editdistance_prob(self, a, b):
        insertion_cost = np.log(0.33)
        deletion_cost = np.log(0.33)
        substitution_cost = np.log(0.34)
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

    def cosine_sim(self, v1, v2):
        dot = 0.0
        v1_sq = 0.0
        v2_sq = 0.0
        for i in xrange(len(v1)):
            dot += v1[i] * v2[i]
            v1_sq += v1[i] ** 2.0
            v2_sq += v2[i] ** 2.0
        denom = (np.sqrt(v1_sq) * np.sqrt(v2_sq))
        i = dot / denom
        i = i if i <= 1 else 1.0
        i = i if i >= 0.0 else 0.0
        return i


    def loadw2v(self, word2vec_file):
        try:
            open(word2vec_file, 'r')
        except IOError, err:
            print Exception, err
            return False
        print 'loading word vecs...'
        with open(word2vec_file) as infile:
            for line in infile:
                terms = line.split()
                word = terms.pop(0)
                vec = np.array(terms, dtype='|S')
                vec = vec.astype(np.float32)
                self.word2vec[word] = vec
        print 'done.'
        return True


if __name__ == "__main__":
    opt = OptionParser()
    opt.add_option("-x", dest="x", default="this is a test",
                   help="1st string")
    opt.add_option("-y", dest="y", default="this is a test",
                   help="2st string)")
    opt.add_option("-d", dest="word2vecfile", default="data/glove.6B.50d.txt",
                   help="txt file with word2vec")
    (options, _) = opt.parse_args()
    x = options.x.split()  # ", account flows down".split()  #
    # x = "A L T R U I S M".split()
    y = options.y.split()  # "it rain rains down".split()  #
    # y = "P L A S M A".split()
    E = EditDistance(options.word2vecfile)
    ed, alignments = E.editdistance(x, y)
    print ed
    print alignments
    edp = E.editdistance_prob(x, y)
    print 'ed', ed, ' ed_prob', np.exp(edp)
    # edr = edscore(x, y)
    # print 'final edr', edr


