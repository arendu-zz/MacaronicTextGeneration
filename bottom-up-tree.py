# -*- coding: utf-8 -*-
__author__ = 'arenduchintala'
from optparse import OptionParser
import itertools as it
import codecs
import numpy as np
import utils
import pdb
from math import log, exp
import kenlm as lm
from editdistance import edscore, editdistance_prob

global all_nonterminalsm, lex_dict, spans_dict, substring_translations, stopwords, lm_model
hard_prune = 10
stopwords = []
all_nonterminals = {}
lex_dict = {}
spans_dict = {}
substring_translations = {}


class NonTerminal(object):
    def __init__(self, idx, i, k):
        self.idx = idx
        self.span = (i, k)
        self.score = 0.0
        self.phrase = None
        self._children = []
        self.isChildTerminal = False

    def add_terminalChild(self, i, gx):
        self.isChildTerminal = True
        self._children = [(i, i, gx)]

    def get_children(self):
        return self._children

    def add_nonTerminalChild(self, nt_idx):
        self._children.append(nt_idx)
        if len(self._children) > 2:
            raise BaseException("Binary or Unary Nodes only")
        else:
            pass

    def __str__(self):
        return ' '.join([str(self.idx), self.phrase.encode('utf-8'), str(self.score)])

    def __cmp__(self, other):
        if self.score < other.score:
            return -1
        elif self.score == other.score:
            return 0
        else:
            return 1


def read_substring_translations(substring_trans_file, substring_spans_file):
    spans_by_line_num = {}
    for idx, l in enumerate(open(substring_spans_file).readlines()):
        spans_by_line_num[idx] = tuple([int(i) for i in l.split()])

    trans_by_span = {}
    for l in codecs.open(substring_trans_file, 'r', 'utf-8').readlines():
        parts = l.split('|||')
        line_num = int(parts[0])
        trans = ' '.join(parts[1].split()[1:-1])
        score = float(parts[-1])
        span_num = spans_by_line_num[line_num]
        # print span_num, trans, score
        trans_for_line = trans_by_span.get(span_num, [])
        trans_for_line.append((score, trans))
        trans_by_span[span_num] = trans_for_line
    return trans_by_span


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
    global lex_dict
    lex_dict = {}
    for l in lex_file:
        parts = l.split()
        en = parts[0].strip()
        fr = parts[1].strip()
        score = log(float(parts[2]))
        lex_dict[fr] = lex_dict.get(fr, []) + [(score, en)]
    return lex_dict


def get_similarity(t_x, E_y):
    max_ed_score = float('-inf')
    max_e_yt = None
    for e_y in E_y:
        # TODO: do this method how to get a log probability from edit distance? (Currently a hack)
        # ed_score = np.log(edscore(t_x.phrase, e_y.phrase))
        ed_score = editdistance_prob(t_x.phrase, e_y.phrase)
        #
        # pdb.set_trace()
        if ed_score > max_ed_score:
            max_ed_score = ed_score
            max_e_yt = e_y
        else:
            pass
    # TODO: this should not just be a simple log addition
    # TODO: must learn weights for this
    try:
        t_x.score += max_ed_score
    except ValueError:
        pdb.set_trace()
    t_x.add_nonTerminalChild(max_e_yt.idx)
    return t_x


def insert_stopword(e1, e2):
    """
    :param e1: non terminal
    :param e2: non terminal
    :return: score,phrase
    """
    global stopwords, lm_model
    l = []
    e = e1.phrase + ' ' + e2.phrase
    e_score = e1.score + e2.score  # TODO: figure out how to properly combine these scores
    no_sw = e_score + lm_model.score(e)  # TODO: how to combine lm_score with mt_scores
    l.append((no_sw, e))
    for sw in stopwords:
        e_ws = e1.phrase + ' ' + sw + ' ' + e2.phrase
        sw = e_score + lm_model.score(e_ws)  # TODO: how to combine lm_score with mt_scores
        l.append((sw, e_ws))
    return sorted(l, reverse=True)[0]


def get_combinations(E_y, E_z, g_x):
    """
    :param E_y: weighted set of translations of left child
    :param E_z: weighted set of translations of right child
    :return: weighted set of translations for current node
    """
    """TODO:The weight of each such e_x is given by combining the weights of e_y and e_z
        and then adding the MT system’s score of e_x as a translation of g_x (and adding a
        penalty for the insertion /deletion of function words).

    """
    global all_nonterminals
    nonterminals = []
    ss = {}
    for e1, e2 in it.chain(it.product(E_y, E_z), it.product(E_z, E_y)):
        e_score, e_phrase = insert_stopword(e1, e2)  # returns best (score,phrase) with stop word insertion LM cost
        i = min(e1.span[0], e2.span[0])
        k = max(e2.span[1], e2.span[1])
        # TODO: score e_x also based on how good a translation of g_x is it,how to do this?
        current_score = ss.get(e_phrase, float('-inf'))
        if e_score > current_score:
            ss[e_phrase] = e_score
            nt = NonTerminal(len(all_nonterminals), i, k)
            nt.score = e_score
            nt.phrase = e_phrase
            nt.add_nonTerminalChild(e1.idx)
            nt.add_nonTerminalChild(e2.idx)
            nonterminals.append(nt)
            all_nonterminals[nt.idx] = nt

    return sorted(nonterminals, reverse=True)


def get_single_word_translations(g_x, sent_number, idx):
    global all_nonterminals, lex_dict, hard_prune
    nonterminals = []
    # ss = sorted(lex_dict[g_x], reverse=True)[:hard_prune]
    ss = sorted(substring_translations[sent_number, idx, idx], reverse=True)[:hard_prune]
    for score, phrase in ss:
        nt = NonTerminal(len(all_nonterminals), idx, idx)
        nt.score = score
        nt.phrase = phrase
        nt.add_terminalChild(idx, g_x)
        nonterminals.append(nt)
        all_nonterminals[nt.idx] = nt
    return nonterminals


def get_substring_translations(sent_number, i, k):
    global substring_translations, all_nonterminals, hard_prune
    ss = sorted(substring_translations[sent_number, i, k], reverse=True)[:hard_prune]
    nonterminals = []
    for score, phrase in ss:
        nt = NonTerminal(len(all_nonterminals), i, k)
        nt.score = score
        nt.phrase = phrase
        nonterminals.append(nt)
        all_nonterminals[nt.idx] = nt
    return nonterminals


def display_best_nt(node, i, k):
    """
    :param node: a node is merely a list of non-terminals
    :return:
    """
    print '***************************************************'
    print 'node span', i, k, 'best nonterminal'
    b_score, b_nt = sorted([(nt.score, nt) for nt in node], reverse=True)[0]
    display_tree(b_nt, collapse_same_str=False, show_score=True)
    print '***************************************************'


def display_tree(root_unary, collapse_same_str=True, show_score=False):
    global all_nonterminals
    print_dict = {}
    reached_leaf = []
    children_stack = [(root_unary.span, root_unary)]
    while len(children_stack) > 0:
        print_nodes = []
        next_children_stack = []
        for cs, cn in children_stack:
            if cn.isChildTerminal:
                reached_leaf.append((cs, cn))
            else:
                print_nodes.append((cs, cn))
                next_children_stack += [(all_nonterminals[ccn_idx].span, all_nonterminals[ccn_idx]) for ccn_idx in
                                        cn.get_children()]
        print_nodes.sort()
        all_print_nodes = print_nodes + reached_leaf
        all_print_nodes.sort()
        print_line = ' | '.join([pn.phrase.encode('utf-8') for ps, pn in all_print_nodes])
        print_line_num = print_dict.get(print_line, len(print_dict))
        print_dict[print_line] = print_line_num
        children_stack = next_children_stack
    for l, p in sorted([(l, p) for p, l in print_dict.items()]):
        print p


if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option("--ce", dest="en_corpus", default="train.clean.tok.true.20.en", help="english corpus sentences")
    opt.add_option("--cd", dest="de_corpus", default="train.clean.tok.true.20.de", help="german corpus sentences")
    opt.add_option("--st", dest="substr_trans", default="substring_trans.20.de", help="german corpus sentences")
    opt.add_option("--ss", dest="substr_spans", default="train.clean.tok.true.20.de.span",
                   help="each line has a span and sent num")
    opt.add_option("-d", dest="data_set", default="data/moses-files/")
    opt.add_option("--sw", dest="stopwords", default="small_stopwords.txt")
    opt.add_option("-l", dest="lex", default="model/lex", help="with extension e2f")
    opt.add_option("--lm", dest="lm", default="train.clean.tok.true.en.arpa", help="english language model file")
    opt.add_option("--nb", dest="nbest", default="en-n-best.txt")
    (options, _) = opt.parse_args()
    data_set = options.data_set
    lex_data = codecs.open(data_set + options.lex + '.e2f', 'r', 'utf-8').readlines()
    en_sentences = codecs.open(data_set + options.en_corpus, 'r', 'utf-8').readlines()
    de_sentences = codecs.open(data_set + options.de_corpus, 'r', 'utf-8').readlines()
    substring_translations = read_substring_translations(data_set + options.substr_trans,
                                                         data_set + options.substr_spans)
    lex_dict = read_lex(lex_data)
    spans_dict = corpus_spans(options.nbest)
    stopwords = codecs.open(data_set + options.stopwords, 'r').read().split()
    lm_model = lm.LanguageModel(data_set + options.lm)
    for sent_num in xrange(0, 10):
        en = en_sentences[sent_num].split()
        de = de_sentences[sent_num].split()
        if len(en) < 25:
            binary_nodes = {}
            unary_nodes = {}
            all_nonterminals = {}

            # initialize unary nodes
            n = len(de)
            for i in xrange(0, n):
                E_x = get_single_word_translations(' '.join(de[i:i + 1]), sent_num, i)  # using lex table
                # E_x = get_substring_translations(sent_num, i, i)  # using substring translations
                unary_nodes[i, i] = E_x

            # for larger spans
            for span in xrange(1, n):
                for i in xrange(0, n - span):
                    k = i + span
                    for j in xrange(i, k):
                        # print 'span size', span, 'start', i, 'mid', j, 'mid', j + 1, 'end', k
                        # print 'span gr', de[i:k], 'child1', de[i:j + 1], 'child2', de[j + 1:k + 1]
                        E_y = unary_nodes[i, j]
                        E_z = unary_nodes[j + 1, k]
                        E_x = get_combinations(E_y, E_z, de[i:k + 1])
                        bl = binary_nodes.get((i, k), [])
                        E_x += bl
                        binary_nodes[i, k] = E_x

                    T_x = get_substring_translations(sent_num, i, k)
                    E_x = []
                    for t_x in T_x:
                        t_x = get_similarity(t_x, sorted(binary_nodes[i, k], reverse=True)[:hard_prune])
                        E_x.append(t_x)
                    ul = unary_nodes.get((i, k), [])
                    E_x += ul
                    unary_nodes[i, k] = E_x

                    # display_best_nt(unary_nodes[i, k], i, k)
                    # pdb.set_trace()

            """
            if we have human translation, we find the root unary node that is closest to the human translation
            """
            closest_unary = None
            best_edscore_from_human = float('-inf')
            for idx, root_unary in enumerate(unary_nodes[0, len(de) - 1]):
                eds = edscore(root_unary.phrase, en)
            if eds > best_edscore_from_human:
                closest_unary = root_unary
            best_edscore_from_human = eds

            print 'closest unary'
            print en_sentences[sent_num].strip()
            display_tree(closest_unary)
            print ' | '.join(de)
            print ''




