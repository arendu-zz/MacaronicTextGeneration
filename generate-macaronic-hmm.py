__author__ = 'arenduchintala'
"""
Generates a macaronic string in "english" using a hmm model.
Observations of the model are aligned tokens (G,E)
G = german token
E = english token

The possible states of each observation is M.
M is the set of Synonyms(E) intersected BestLexTranslations(G)

Probability of emission is P( (G,E) | M)
Probability of transition is P(M_t+1 | M_t) which is computed using the Es associated to the Ms
"""

import sys, codecs, pdb, operator, kenlm
from optparse import OptionParser
from math import log, exp

global BOUNDRY_STATE
BOUNDRY_STATE = '<s>'
global language_model


def flatten_backpointers(bt):
    reverse_bt = []
    while len(bt) > 0:
        x = bt.pop()
        reverse_bt.append(x)
        if len(bt) > 0:
            bt = bt.pop()
    reverse_bt.reverse()
    return reverse_bt


def get_transition_prob(mj, mj_1, original_src_sentence):
    mod_src_sentence = [s for s in original_src_sentence]
    if isinstance(mj, tuple):
        mj_token = mj[0]
        mj_id = mj[1]
        mod_src_sentence[mj_id] = mj_token
    else:
        mj_token = mj

    if isinstance(mj_1, tuple):
        mj_1_token = mj_1[0]
        mj_1_id = mj_1[1]
        mod_src_sentence[mj_1_id] = mj_1_token
    else:
        mj_1_token = mj_1

    global language_model
    full_score = language_model.score(' '.join(mod_src_sentence))
    return full_score
    # if mj_1_token == BOUNDRY_STATE:
    # return language_model.score(mj_token)
    #elif mj_token == BOUNDRY_STATE:
    #    return language_model.score(mj_1_token)
    #else:
    #    return language_model.score(mj_1_token + ' ' + mj_token)


def get_emission(o, s):
    pass


def get_viterbi(obs_sequence, states, original_src_sentence):
    states.append([BOUNDRY_STATE])
    pi = {(0, BOUNDRY_STATE): 0.0}
    arg_pi = {(0, BOUNDRY_STATE): []}
    for k in range(1, len(obs_sequence) + 2):  # the words are numbered from 1 to n, 0 is special start character
        for v in states[k]:  # [1]:
            max_prob_to_bt = {}
            for u in states[k - 1]:  # [1]:
                aj = v
                aj_1 = u
                q = get_transition_prob(aj, aj_1, original_src_sentence)
                e = log(1.0 / len(states[k]))  # get_emission(target_token, source_token)
                # print k
                # print v, '|', u
                # print aj, '|', aj_1, '=', q
                # print target_token, '|', source_token, '=', e
                p = pi[(k - 1, u)] + q + e
                # print 'alpha_p', alpha_p
                if len(arg_pi[(k - 1, u)]) == 0:
                    bt = [u]
                else:
                    bt = [arg_pi[(k - 1, u)], u]
                max_prob_to_bt[p] = bt
            max_bt = max_prob_to_bt[max(max_prob_to_bt)]
            new_pi_key = (k, v)
            pi[new_pi_key] = max(max_prob_to_bt)
            arg_pi[new_pi_key] = max_bt
    max_bt = max_prob_to_bt[max(max_prob_to_bt)]
    max_p = max(max_prob_to_bt)
    max_bt = flatten_backpointers(max_bt)
    max_bt.pop(0)
    return max_bt, max_p  # returns the best back trace, best path probability, sum of path probabilites


def logadd(x, y):
    """
    trick to add probabilities in logspace
    without underflow
    """
    # Todo: handle special case when x,y=0
    if x == 0.0 and y == 0.0:
        return log(exp(x) + exp(y))
    elif x >= y:
        return x + log(1 + exp(y - x))
    else:
        return y + log(1 + exp(x - y))


def get_states(observation, synsets, translations):
    states = []
    for g, e, e_id in observation:
        e_from_g = set([eg[1] for eg in sorted(translations[g])])
        if e not in synsets:
            e_from_syn = [e]
        else:
            e_from_syn = set([s[1] for s in synsets[e]])
        m = list(e_from_g.intersection(e_from_syn))
        mt = [(ms, e_id) for ms in m]
        states.append(mt)
    return states


"""
def get_states(observation, synsets, translations):
    states = []
    for g, e in observation:
        e_from_g = [eg for eg in sorted(translations[g])]
        if e not in synsets:
            e_from_syn = [(0.0, e)]
        else:
            e_from_syn = synsets[e]

        m_tokens = {}
        for logp, e_token in e_from_syn + e_from_g:  # we can direcl
            if e_token in e_from_syn and e_token in e_from_g:  # this if does the intersection
                # e_token = e_token.lower()
                e_score = m_tokens.get(e_token, float('-inf'))
                e_score = logadd(e_score, logp)
                m_tokens[e_token] = e_score
        sorted_m = sorted(m_tokens.iteritems(), key=operator.itemgetter(1), reverse=True)
        m = sorted_m[:5]
        # print g, e, m
        pdb.set_trace()
"""


def get_observations(target2source, src_tokens, target_tokens):
    observations = []
    for k in sorted(target2source):
        max_align_prob, max_src_id = max(target2source[k])
        observations.append((target_tokens[k], src_tokens[max_src_id], max_src_id))
    return observations


def get_target2src(alignment_str, src_tokens, target_tokens, lexp):
    target2src = {}
    for a in alignment_str.split():
        i, j = a.split('-')  # src-tar
        i = int(i)
        j = int(j)
        src_is = target2src.get(j, [])
        prob_alignment = lexp[target_tokens[j], src_tokens[i]]
        src_is.append((prob_alignment, i))
        target2src[j] = src_is
    return target2src


if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    sys.stdin = codecs.getwriter('utf-8')(sys.stdin)
    optparser = OptionParser()
    optparser.add_option("-a", "--align", dest="word_alignment",
                         default="data/moses-files-tok/model/aligned.grow-diag-final",
                         help="alignment file between src-target de-en")

    optparser.add_option("-e", "--en", dest="sentences_en",
                         default="data/training/train.clean.tok.en",
                         help="english sentences")
    optparser.add_option("-d", "--de", dest="sentences_de",
                         default="data/training/train.clean.tok.de",
                         help="german sentences")
    optparser.add_option("-s", "--syn", dest="synsets", default="data/training/en.sim.wn",
                         help="synset file (from wordnet)")
    optparser.add_option("-l", "--lex", dest="lex_probs",
                         default="data/moses-files-tok/model/lex.f2e")
    optparser.add_option("-m", "--lm", dest="lang_model", default="data/training/train.clean.lm.en",
                         help="arpa formatted language models")
    (options, _) = optparser.parse_args()

    lexf2e = {}
    translations = {}
    for line in open(options.lex_probs, 'r').readlines():
        g, e, lp = line.split()
        logp = log(float(lp))
        lexf2e[g, e] = logp
        es = translations.get(g, [])
        es.append((logp, e))
        translations[g] = es

    synsets = {}
    for line in open(options.synsets, 'r').readlines():
        v, syns = line.split('\t')
        syns = syns.strip().split(',')
        try:
            probs = log(float(1.0 / len(syns) + 1))
        except ValueError:
            pdb.set_trace()
        synsets[v] = [(probs, s) for s in syns] + [(probs, v)]
    alignments = open(options.word_alignment, 'r').readlines()
    src_sentences = [snt.split() for snt in open(options.sentences_en, 'r').readlines()]
    target_sentences = [snt.split() for snt in open(options.sentences_de, 'r').readlines()]

    language_model = kenlm.LanguageModel(options.lang_model)

    for alignment, src, tar in zip(alignments, src_sentences, target_sentences)[:200]:
        t = get_target2src(alignment, src, tar, lexf2e)
        o = get_observations(t, src, tar)
        print alignment.decode('utf-8').strip()

        print ' '.join(tar).decode('utf-8').strip()
        # print 'obs       :', o
        states = get_states(o, synsets, translations)
        # print 'trelis    :', states
        viterbi_states, viterbi_p = get_viterbi(o, [[BOUNDRY_STATE]] + states, src)
        v = [vf[0] for vf in viterbi_states]
        print ' '.join(v).decode('utf-8')
        v_filter = [t1 for t1, t2 in zip(v, v[1:]) if t1 != t2]
        v_filter.append(v_filter[-1])
        print ' '.join(v_filter).decode('utf-8')
        print ' '.join(src).decode('utf-8').strip()
        print ''
        # pdb.set_trace()


