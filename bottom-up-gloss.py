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
        self._literaltranslations = {}
        self._substringtranslations = {}

    @property
    def substringtranslations(self):
        return [(s, v) for v, s in self._substringtranslations.items()]

    @substringtranslations.setter
    def substringtranslations(self, val):
        self._substringtranslations = {}
        self.append_substringtranslations(val)

    def append_substringtranslations(self, val):
        """
        :param val: a list of tuples of translations, tuples of the form (score,vocab)
        :return:
        """
        for s, v in val:
            if s > self._substringtranslations.get(v, float('-inf')):
                self._substringtranslations[v] = s


    @property
    def literaltranslations(self):
        return [(s, v) for v, s in self._literaltranslations.items()]

    @literaltranslations.setter
    def literaltranslations(self, val):
        self._literaltranslations = {}
        self.append_literaltranslations(val)

    def append_literaltranslations(self, val):
        """
        :param val: a list of tuples of translations, tuples of the form (score,vocab)
        """
        for s, v in val:
            if s > self._literaltranslations.get(v, float('-inf')):
                self._literaltranslations[v] = s


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


def read_lex(lex_file):
    lex_dict = {}
    for l in lex_file:
        parts = l.split()
        en = parts[0].strip()
        fr = parts[1].strip()
        score = log(float(parts[2]))
        lex_dict[fr] = lex_dict.get(fr, []) + [(score, en)]
    return lex_dict


def corpus_spans(nbest):
    span_dict = {}
    for line in open(nbest, 'r').readlines():
        sid, translation = line.split('|||')[:2]
        # print translation
        parts = translation.strip().split('|')
        # print parts
        for part_id in xrange(0, len(parts) - 1, 2):
            # print parts[part_id], '<--', parts[part_id + 1]
            span = tuple(int(s) for s in [sid.strip()] + parts[part_id + 1].split('-'))
            # print span
            s = span_dict.get(span, set([]))
            s.add(parts[part_id])
            span_dict[span] = s
    return span_dict


if __name__ == "__main__":
    opt = OptionParser()
    opt.add_option("-d", dest="data_set", default="data/moses-files/")
    opt.add_option("-l", dest="lex", default="model/lex", help="with extension e2f")
    opt.add_option("--lm", dest="lm", default="train.clean.tok.true.en.arpa", help="english language model file")
    opt.add_option("--nb", dest="nbest", default="en-n-best.txt")
    (options, _) = opt.parse_args()
    data_set = options.data_set
    lex_file = open(data_set + options.lex + '.e2f', 'r').readlines()
    lm_model = lm.LanguageModel(data_set + options.lm)

    lex_dict = read_lex(lex_file)
    span_dict = corpus_spans(options.nbest)

    fr = "San FRANCISCO – Es war noch nie leicht , ein rationales Gespräch über den Wert von Gold zu führen .".split()
    en = "San FRANCISCO – It has never been easy to have a rational conversation about the value of gold .".split()

    # en = "resumption of the session".split()
    # fr = "reanudación del período de sesiones".split()
    n = len(fr)
    chart = {}
    """
    initialize chart with span of 1
    """
    for i in xrange(n):
        gx = ' '.join(fr[i:i + 1])
        Exs = sorted(lex_dict[gx], reverse=True)
        ci = ChartItem(gx)
        ci.literaltranslations = Exs[:5]

        ss = [(0.0, v) for v in span_dict.get((0, i, i), [])]
        print i, ss
        ci.substringtranslations = ss
        chart[i, i + 1] = ci

    """
    initialize chart with substring translations
    """
    for span in xrange(2, n + 1):
        print 'span', span
        for s in xrange(0, n - span + 1):
            e = s + span
            ci = ChartItem(' '.join(fr[s:e]))
            chart[s, e] = ci
            ci.substringtranslations = [(0.0, v) for v in span_dict.get((0, i, i), [])]
            for m in xrange(s + 1, e):
                c1 = chart[s, m].substringtranslations
                c2 = chart[m, e].substringtranslations
                # pdb.set_trace()

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
                ex_trans = get_combinations(chart[s, m].literaltranslations, chart[m, e].literaltranslations, 5)
                ci.append_translations(ex_trans)
                print len(ci.literaltranslations)

    print 'ok'



