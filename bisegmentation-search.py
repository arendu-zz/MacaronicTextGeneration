# -*- coding: latin1 -*-
__author__ = 'arenduchintala'
from collections import defaultdict
import SegmentState
import PrintCuts
import pdb, sys
import simplejson as json
from pprint import pprint
from optparse import OptionParser
from heapq import heappush, heapify, heappop, nlargest
import codecs
# TODO read pre-ordering rules in collens and koen
# TODO: parse sentences synchronously - get parser from joshua

global Q_key2state, HQ_beam_width, Q_score2key, Q_recursion, HQ, HQ_key2state, fillin, hyp
HQ_beam_width = 100
HQ = []
HQ_key2state = {}
Q_key2state = {}
Q_score2key = []
Q_recursion = []
hyp = "m1"


def sub_array_match(d_span, d_list, d_cov):
    if d_span[0] in d_list:
        match_start_pt = -1
        matched_so_far = 0
        for d_idx, (dl, dc) in enumerate(zip(d_list, d_cov)):
            if matched_so_far < len(d_span) and dl == d_span[matched_so_far] and dc is False:
                if matched_so_far == 0:
                    match_start_pt = d_idx
                matched_so_far += 1
            elif matched_so_far == len(d_span):
                break

        if matched_so_far == len(d_span):
            # print 'good unused match found, start at:', match_start_pt, ' end at', match_start_pt + matched_so_far
            update_cov = [match_start_pt <= u < match_start_pt + matched_so_far for u in range(len(d_list))]
            matched_span = (match_start_pt, match_start_pt + matched_so_far)
            return update_cov, matched_span
        else:
            # print 'no match for', ' '.join(d_span)
            pass
    return [False] * len(d_list), None


def find_match_in_source(target_span, cs, phrase_table):
    span_target_str = ' '.join(cs.target[target_span[0]:target_span[1]])
    if span_target_str in phrase_table:
        source_spans = list(phrase_table[span_target_str])
        source_spans.sort(reverse=True)
        for score_d, source_span in source_spans[:50]:  # TODO: we can speed up here, only loop top K source_spans
            cov_source_new, source_matched_span = sub_array_match(source_span.split(), cs.source, cs.cov_source)
            if source_matched_span is not None:
                cov_target_new = [(target_span[0] <= i < target_span[1]) for i, t in enumerate(cs.target)]
                return cov_source_new, cov_target_new, source_matched_span, score_d
    else:
        pass  # target span not in dictionary
    return [False] * len(cs.source), [False] * len(cs.target), None, 0.0


def pop_from_heap():
    global HQ, HQ_key2state
    (score, state) = heappop(HQ)
    HQ_key2state.pop(state.state_key())
    return state


def remove_from_heap(rm_state):
    global HQ, HQ_key2state
    # print 'removing', str(rm_state.state_key()), rm_state.get_score()
    HQ.remove((rm_state.get_score(), rm_state))
    HQ_key2state.pop(rm_state.state_key())
    heapify(HQ)


def add_to_heap(new_cs):
    global HQ, HQ_key2state
    if new_cs.state_key() in HQ_key2state:
        old_cs = HQ_key2state[new_cs.state_key()]
        if old_cs.get_score() > new_cs.get_score():
            # print '******************* replacing state *****************'
            remove_from_heap(old_cs)
            # print 'replacing with', str(new_cs.state_key()), new_cs.get_score()
            heappush(HQ, (new_cs.get_score(), new_cs))
            HQ_key2state[new_cs.state_key()] = new_cs
        else:
            # print '******************* ignoreing state *****************'
            pass
    else:
        # print '******************* adding state *****************'
        heappush(HQ, (new_cs.get_score(), new_cs))
        HQ_key2state[new_cs.state_key()] = new_cs
        if len(HQ) > HQ_beam_width:
            largest = nlargest(1, HQ)
            (score, state) = largest[0]
            remove_from_heap(state)


def find_alignments(start_state, phrase_table):
    global Q_key2state, Q_score2key
    Q_key2state = {}
    Q_score2key = []
    # solutions = {}
    best_solution = None

    add_to_heap(start_state)
    while len(HQ) > 0:
        # cs = pop_from_q()
        cs = pop_from_heap()
        if False not in cs.cov_target:
            # print 'completed result:', cs.state_key(), 'score:', cs.get_score()
            # solutions[cs.get_score()] = cs
            if best_solution is None:
                # print 'first solution:'
                # cs.display_alignment_strings()
                best_solution = cs
            elif cs.get_score() < best_solution.get_score():
                sys.stdout.write("Best Score: %f   \r" % (cs.get_score()))
                sys.stdout.flush()
                # print 'found new best solution:'
                # cs.display_alignment_strings()
                best_solution = cs
            else:
                # print 'ignoring solution:'
                # cs.display_alignment_strings()
                # pdb.set_trace()
                pass
        else:
            MAX_K = 6 if len(start_state.target) > 6 else len(start_state.target) - 1
            s_idx = cs.cov_target.index(False)
            got_match = False
            for k in range(MAX_K, 0, -1):

                st_idx = s_idx
                end_idx = s_idx + k if s_idx + k < len(cs.target) else len(cs.target)
                span_target = (st_idx, end_idx)
                update_cov_source, update_cov_target, source_span_match, match_score = find_match_in_source(span_target,
                                                                                                            cs,
                                                                                                            phrase_table)
                if source_span_match is not None:
                    new_cs = cs.get_copy()  # SegmentState.SegmentState(e_list, d_list, cs.get_score() + 1)
                    new_cs.cov_source = [i | j for i, j in zip(cs.cov_source, update_cov_source)]
                    new_cs.cov_target = [i | j for i, j in zip(cs.cov_target, update_cov_target)]
                    new_cs.cov_ratio = 1.0
                    st_idx = s_idx
                    end_idx = s_idx + k if s_idx + k < len(new_cs.target) else len(new_cs.target)
                    target_span = (st_idx, end_idx)
                    new_cs.add_alignment(target_span, source_span_match, match_score)

                    add_to_heap(new_cs)
                    got_match = True
                else:
                    pass
            if not got_match or k == 1:
                # print 'force a target ---> NULL alignment'
                new_cs = cs.get_copy()
                update_cov_target = [s_idx <= i < s_idx + 1 for i in range(len(cs.cov_target))]
                new_cs.cov_target = [i | j for i, j in zip(cs.cov_target, update_cov_target)]

                if hyp == "m1":
                    new_cs.cov_ratio = 1.0
                elif hyp == "m2":
                    new_cs.cov_ratio = float(new_cs.cov_source.count(True) + len(new_cs.cov_source)) / float(
                        2 * len(new_cs.cov_source))
                else:
                    new_cs.cov_ratio = float(new_cs.cov_source.count(True) + 1.0) / float(1.0 + len(new_cs.cov_source))

                st_idx = s_idx
                end_idx = s_idx + k if s_idx + k < len(new_cs.target) else len(new_cs.target)
                target_span = (st_idx, end_idx)
                target_token = new_cs.target[s_idx:end_idx][0]
                source_spans = list(fillin[target_token])
                source_spans.sort(reverse=True)
                score_d, source_span = source_spans[0]
                source_span_match = (None, None, '_' + source_span + '_')
                new_cs.add_alignment(target_span, source_span_match, 0.1)
                # add_to_q(new_cs)
                add_to_heap(new_cs)
    # scores = sorted(solutions)
    # best_score = scores[0]
    return best_solution  # solutions[best_score]


if __name__ == "__main__":
    opt = OptionParser()

    opt.add_option("-d", dest="data_set", default="data/moses-files/")
    opt.add_option("--pt", dest="phrase_table", default="model/phrase-table")
    opt.add_option("--en", dest="train_en", default="train.clean.tok.true.en")
    opt.add_option("--de", dest="train_de", default="train.clean.tok.true.de")
    opt.add_option("-l", dest="lex", default="model/lex", help="with extension e2f")
    opt.add_option("--hp", dest="hyp", default="m1", help="hyperparameter 'm1' 'm2' or 'm3'")

    (options, _) = opt.parse_args()
    hyp = options.hyp
    data_set = options.data_set
    phrase_table_file = open(data_set + options.phrase_table, 'r').readlines()
    train_en = open(data_set + options.train_en, 'r').readlines()
    train_de = open(data_set + options.train_de, 'r').readlines()
    print train_de[0]
    print [(str(i), str(s)) for i, s in enumerate(train_de[0].split())]
    print ' '.join(['("' + str(i) + ' ' + str(s) + '")' for i, s in enumerate(train_de[0].split())])
    # en2de = defaultdict(set)
    de2en = defaultdict(set)
    fillin = defaultdict(set)
    for pt in phrase_table_file:
        parts = pt.split('|||')
        if len(parts[0].split()) < 6 and len(parts[1].split()) < 6:
            en = parts[0].strip()
            de = parts[1].strip()
            scores = [float(sc) for sc in parts[2].split()]
            # score = scores[0] * scores[1] + scores[2] * scores[3]
            score = scores[0]  # * 0.5 + scores[2] * 0.5
            # en2de[en].add((score, de))
            de2en[de].add((score, en))

    lex_file = open(data_set + options.lex + '.e2f', 'r').readlines()
    lex_dict = {}
    for l in lex_file:
        parts = l.split()
        en = parts[0].strip()
        de = parts[1].strip()
        score = float(parts[2])
        lex_dict[en, de] = score
    """
    lex_file_inv = open(data_set + options.lex + '.f2e', 'r').readlines()
    lex_dict_inv = {}
    for l in lex_file_inv:
        parts = l.split()
        de = parts[0].strip()
        en = parts[1].strip()
        score = float(parts[2])
        lex_dict_inv[en, de] = score
    """
    for e, d in lex_dict:
        score_e2f = lex_dict[e, d]
        # score_f2e = lex_dict_inv[e, d]
        score = score_e2f  # * 0.5 + score_f2e * 0.5
        # en2de[e].add((score, d))
        de2en[d].add((score, e))
        fillin[d].add((score, e))
    snippet = "#" + str(opt.values) + "\n"
    print snippet
    print 'read data completed...'
    for idx in range(45)[:]:

        # recursive solution
        source_l = train_en[idx].split()  # English
        target_l = train_de[idx].split()  # German
        # target_l = "Prozent angestiegen".split()
        # source_l = "% over".split()
        # target_l = ['allerdings', 'ist']
        # source_l = [',', 'is']
        # = ['minute']
        # = ['un', 'minuto']  # .split()

        phrase_table = de2en
        if len(target_l) < 23 and len(source_l) < 23:
            print '****************', 'SOLUTION FOR', idx, '****************'
        start_state = SegmentState.SegmentState((0, len(target_l)), (0, len(source_l)), target_l, source_l)

        Q_recursion.append(start_state)
        # print 'pushed', start_state.target, start_state.source
        while len(Q_recursion) > 0:
            current_solution = Q_recursion.pop()
            # print(current_solution)
            best_solution = find_alignments(current_solution, phrase_table)
            # print 'best: ', best_solution.get_score()
            # pdb.set_trace()
            alignment_strings = best_solution.get_alignment_strings()
            to_add = []
            for a in sorted(alignment_strings):
                new_recursion_state = SegmentState.SegmentState(a[0], a[1],
                                                                alignment_strings[a][0],
                                                                alignment_strings[a][1])
                # print new_recursion_state
                current_solution.add_to_children(new_recursion_state)
                if len(alignment_strings[a][0]) > 1:
                    to_add.append(new_recursion_state)
                else:
                    pass  # don't recurse on single word phrases
                    # print 'pushed', new_recursion_state.target, new_recursion_state.source
            for ta in reversed(to_add):
                Q_recursion.append(ta)
        print'\n********TREE LEVELS********'

        rep = start_state.get_recursive_rep()
        print json.dumps(rep)
        # PrintCuts.print_levels(start_state)
        # print '\n********TREE CUTS********'
        # start_state.display = True
        # PrintCuts.print_cuts(start_state)




