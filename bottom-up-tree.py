# -*- coding: utf-8 -*-
__author__ = 'arenduchintala'
from optparse import OptionParser
import itertools as it
import codecs
import utils
import pdb
from math import log, exp
import kenlm as lm


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
            s.add(parts[part_id].strip())
            span_dict[span] = s
    return span_dict


def read_lex(lex_file):
    lex_dict = {}
    for l in lex_file:
        parts = l.split()
        en = parts[0].strip()
        fr = parts[1].strip()
        score = log(float(parts[2]))
        lex_dict[fr] = lex_dict.get(fr, []) + [(score, en)]
    return lex_dict


def get_similarity(t_x_string, g_ik):
    # TODO: do this method
    pass


def get_combinations(E_y, E_z, g_x):
    """
    :param E_y: weighted set of translations of left child
    :param E_z: weighted set of translations of right child
    :return: weighted set of translations for current node
    """
    ss = []
    for e1, e2 in it.chain(it.product(E_y, E_z), it.product(E_z, E_y)):
        e_x = (utils.logadd(e1[0], e2[0]), ' '.join([e1[1].strip(), e2[1].strip()]))
        # TODO: score e_x also based on how good a translation of g_x is it
        # how to do this?
        ss.append(e_x)
    return sorted(ss, reverse=True)[:10]


def get_translations(gr_sent, i, j, spans_dict, sent_number, lex_dict):
    if i == j:
        # single word span
        s = ' '.join(gr_sent[i:j + 1])
        ss = sorted(lex_dict[s], reverse=True)[:10]
    else:
        ss = [(0.0, v) for v in set(spans_dict.get((sent_number, i, j), []))]
        # TODO: replace this part with the trick Phillip gave
        # %#$#$% <wall /> bla bla bla <wall /> @#$T#$
    return ss


if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option("--ce", dest="en_corpus", default="train.clean.tok.true.en", help="english corpus sentences")
    opt.add_option("--cd", dest="de_corpus", default="train.clean.tok.true.de", help="german corpus sentences")
    opt.add_option("-d", dest="data_set", default="data/moses-files/")
    opt.add_option("-l", dest="lex", default="model/lex", help="with extension e2f")
    opt.add_option("--lm", dest="lm", default="train.clean.tok.true.en.arpa", help="english language model file")
    opt.add_option("--nb", dest="nbest", default="en-n-best.txt")
    (options, _) = opt.parse_args()
    data_set = options.data_set
    lex_data = codecs.open(data_set + options.lex + '.e2f', 'r', 'utf-8').readlines()
    en_sentences = codecs.open(data_set + options.en_corpus, 'r', 'utf-8').readlines()
    de_sentences = codecs.open(data_set + options.de_corpus, 'r', 'utf-8').readlines()

    lex_dict = read_lex(lex_data)
    spans_dict = corpus_spans(options.nbest)
    lm_model = lm.LanguageModel(data_set + options.lm)

    en = en_sentences[5].split()
    de = de_sentences[5].split()

    binary_nodes = {}
    unary_nodes = {}

    # initialize unary nodes
    n = len(de)
    for i in xrange(0, n):
        E_x = get_translations(de, i, i, spans_dict, 5, lex_dict)
        print de[i:i + 1], E_x
        unary_nodes[i, i] = E_x

    # for larger spans
    for span in xrange(1, n):
        for i in xrange(0, n - span):
            k = i + span
            for j in xrange(i, k):
                print de
                print 'span size', span, 'start', i, 'mid', j, 'mid', j + 1, 'end', k
                print 'span gr', de[i:k], 'child1', de[i:j + 1], 'child2', de[j + 1:k + 1]
                E_y = unary_nodes[i, j]
                E_z = unary_nodes[j + 1, k]
                E_x = get_combinations(E_y, E_z, de[i:k + 1])
                binary_nodes[i, k] = E_x

                T_x = get_translations(de, i, k, spans_dict, 5, lex_dict)
                for t_x in T_x:
                    t_x[0] += get_similarity(t_x[1], binary_nodes[i, k])
                unary_nodes[i, k] = T_x


