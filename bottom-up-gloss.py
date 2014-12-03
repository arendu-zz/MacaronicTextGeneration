# -*- coding: latin1 -*-
__author__ = 'arenduchintala'
from optparse import OptionParser
import itertools as it
import pdb
from math import log, exp
import kenlm as lm

global lm_model


class ChartItem(object):
    def __str__(self):
        return self.gx

    def __init__(self, gx):
        self.gx = gx
        self._translations = {}


    @property
    def translations(self):
        return [(s, v) for v, s in self._translations.items()]

    @translations.setter
    def translations(self, val):
        self._translations = {}
        self.append_translations(val)

    def append_translations(self, val):
        for s, v in val:
            if s > self._translations.get(v, float('-inf')):
                self._translations[v] = s


def get_lm_score(fragment):
    global lm_model
    score = lm_model.score(fragment)
    return score


def get_combinations(ey_trans, ez_trans, top=None):
    """
    Here we take the translations for 2 adjacent nodes
    and recombine them (also here we can add insertions and deletions)
    :param ey_trans:
    :param ez_trans:
    :return:
    """
    trans = []
    for e1, e2 in it.chain(it.product(ey_trans, ez_trans), it.product(ez_trans, ey_trans)):
        score_1, trans_1 = e1
        score_2, trans_2 = e2
        e_trans = trans_1 + " " + trans_2
        lm_score = get_lm_score(e_trans)
        ezy = (score_1 + score_2 + lm_score, e_trans)
        trans.append(ezy)
    trans = sorted(trans, reverse=True)
    if top is not None:
        return trans[:top]
    else:
        return trans


def get_translation(de_span):
    """
    Here we will look up the possible translations for the german span 'de_span'
    :param de_span:
    :return:
    """
    return None


if __name__ == "__main__":

    opt = OptionParser()
    opt.add_option("-d", dest="data_set", default="data/coursera-large/")
    opt.add_option("-l", dest="lex", default="model/lex", help="with extension e2f")
    opt.add_option("--lm", dest="lm", default="en.arpa", help="english language model file")
    (options, _) = opt.parse_args()
    data_set = options.data_set
    lex_file = open(data_set + options.lex + '.e2f', 'r').readlines()
    lm_model = lm.LanguageModel(data_set + options.lm)
    lex_dict = {}
    for l in lex_file:
        parts = l.split()
        en = parts[0].strip()
        fr = parts[1].strip()
        score = log(float(parts[2]))
        lex_dict[fr] = lex_dict.get(fr, []) + [(score, en)]

    # fr = "San FRANCISCO – Es war noch nie leicht , ein rationales Gespräch über den Wert von Gold zu führen .".split()
    # en = "San FRANCISCO – It has never been easy to have a rational conversation about the value of gold .".split()

    en = "resumption of the session".split()
    fr = "reanudación del período de sesiones".split()
    n = len(fr)
    chart = {}
    """
    initialize chart with span of 1
    """
    for i in xrange(n):
        gx = ' '.join(fr[i:i + 1])
        Exs = sorted(lex_dict[gx], reverse=True)
        ci = ChartItem(gx)
        ci.translations = Exs[:5]
        chart[i, i + 1] = ci
    """
    do larger spans 2 to n
    """
    for span in xrange(2, n + 1):
        print 'span', span
        for s in xrange(0, n - span + 1):
            e = s + span
            ci = ChartItem(' '.join(fr[s:e]))
            chart[s, e] = ci
            for m in xrange(s + 1, e):
                print 's,m,e', s, m, e
                # print ' '.join(fr[s:e]), '=', fr[s:m], '+', fr[m:e]
                # print ' '.join(fr[s:e]), '=', chart[s, m], '+', chart[m, e]
                ex_trans = get_combinations(chart[s, m].translations, chart[m, e].translations, 5)
                ci.append_translations(ex_trans)
                print len(ci.translations)
    pdb.set_trace()
    print 'ok'



