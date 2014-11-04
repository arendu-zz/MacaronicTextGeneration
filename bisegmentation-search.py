# -*- coding: utf-8 -*-
__author__ = 'arenduchintala'
from collections import defaultdict
import SegmentState
import PrintCuts

# TODO read pre-ordering rules in collens and koen
# TODO: parse sentences synchronously - get parser from joshua

global Q_key2state, Q_score2key, Q_recursion
Q_key2state = {}
Q_score2key = []
Q_recursion = []


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


def pop_from_q():
    Q_score2key.sort()
    (score, cs_key) = Q_score2key.pop(0)
    cs = Q_key2state.pop(cs_key)
    return cs


def add_to_q(new_cs):
    global Q_key2state
    new_key = new_cs.state_key()
    if new_key in Q_key2state:

        old_cs = Q_key2state[new_key]  # old state obj with same coverage
        if new_cs.get_score() < old_cs.get_score():  # TODO: what should really be the score?
            Q_key2state[new_key] = new_cs
            Q_score2key.remove((old_cs.get_score(), new_key))
            Q_score2key.append((new_cs.get_score(), new_key))
            # print '*************replaced old state*************', new_cs.state_key()
            # print 'len of Q', len(Q_key2state)
        else:
            # print '*************ignored new state*************', new_cs.state_key()
            # print 'new score:', new_cs.get_score(), 'old score', old_cs.get_score()
            # print 'new:'
            # new_cs.display_alignment()
            # print 'old'
            # old_cs.display_alignment()
            # print 'len of Q', len(Q_key2state)
            # there is a same state with lower score
            pass
    else:
        Q_key2state[new_cs.state_key()] = new_cs
        Q_score2key.append((new_cs.get_score(), new_cs.state_key()))
        # print '*************adding state*************', new_cs.state_key()
        # print 'len of Q', len(Q_key2state)


def find_alignments(start_state, phrase_table):
    global Q_key2state, Q_score2key
    Q_key2state = {}
    Q_score2key = []
    # solutions = {}
    best_solution = None
    add_to_q(start_state)
    while len(Q_key2state) > 0:
        cs = pop_from_q()

        if False not in cs.cov_target:
            # print 'completed result:', cs.state_key(), 'score:', cs.get_score()
            # solutions[cs.get_score()] = cs
            if best_solution is None:
                # print 'first solution:'
                # cs.display_alignment_strings()
                best_solution = cs
            elif cs.get_score() < best_solution.get_score():
                # print 'found new best solution:'
                # cs.display_alignment_strings()
                best_solution = cs
            else:
                # print 'ignoring solution:'
                # cs.display_alignment_strings()
                # pdb.set_trace()
                # print 'found alignment with score:', cs.get_score()
                # cs.display_alignment()
                # print 'ok'
                pass
        else:
            MAX_K = 6 if len(start_state.target) > 6 else len(start_state.target) - 1
            s_idx = cs.cov_target.index(False)
            got_match = False
            for k in range(MAX_K, 0, -1):

                st_idx = s_idx
                end_idx = s_idx + k if s_idx + k < len(cs.target) else len(cs.target)
                span_target = (st_idx, end_idx)
                # print 'k', k, span_target
                update_cov_source, update_cov_target, source_span_match, match_score = find_match_in_source(span_target,
                                                                                                            cs,
                                                                                                            phrase_table)
                if source_span_match is not None:
                    new_cs = cs.get_copy()  # SegmentState.SegmentState(e_list, d_list, cs.get_score() + 1)
                    new_cs.cov_source = [i | j for i, j in zip(cs.cov_source, update_cov_source)]
                    new_cs.cov_target = [i | j for i, j in zip(cs.cov_target, update_cov_target)]
                    st_idx = s_idx
                    end_idx = s_idx + k if s_idx + k < len(new_cs.target) else len(new_cs.target)
                    target_span = (st_idx, end_idx)
                    # here we calculate score by how many words in source are covered
                    # new_cs.add_alignment(target_span, source_span_match, source_span_match[1] - source_span_match[0])
                    # here we actually use the match_score provided by the find_match_in_source method
                    new_cs.add_alignment(target_span, source_span_match, match_score)
                    # if False not in new_cs.cov_source and False not in new_cs.cov_target:
                    # completed_states.append(new_cs)
                    # print 'added completed state'
                    # else:
                    add_to_q(new_cs)
                    got_match = True
                else:
                    pass
            if not got_match or k == 1:
                # print 'force a target ---> NULL alignment'
                new_cs = cs.get_copy()
                update_cov_target = [s_idx <= i < s_idx + 1 for i in range(len(cs.cov_target))]
                new_cs.cov_target = [i | j for i, j in zip(cs.cov_target, update_cov_target)]
                st_idx = s_idx
                end_idx = s_idx + k if s_idx + k < len(new_cs.target) else len(new_cs.target)
                target_span = (st_idx, end_idx)
                source_span_match = (None, None)
                new_cs.add_alignment(target_span, source_span_match, 0.0)
                add_to_q(new_cs)
    # scores = sorted(solutions)
    # best_score = scores[0]
    return best_solution  # solutions[best_score]


if __name__ == "__main__":
    data_set = 'moses-files-tok'  # 'coursera-large'
    phrase_table_file = open('data/' + data_set + '/model/phrase-table', 'r').readlines()
    train_en = open('data/' + data_set + '/train.clean.tok.en', 'r').readlines()
    train_de = open('data/' + data_set + '/train.clean.tok.de', 'r').readlines()
    en2de = defaultdict(set)
    de2en = defaultdict(set)
    for pt in phrase_table_file:
        parts = pt.split('|||')
        if len(parts[0].split()) < 6 and len(parts[1].split()) < 6:
            en = parts[0].strip()
            de = parts[1].strip()
            scores = [float(sc) for sc in parts[2].split()]
            # score = scores[0] * scores[1] + scores[2] * scores[3]
            score = scores[0] * 0.5 + scores[2] * 0.5
            en2de[en].add((score, de))
            de2en[de].add((score, en))

    lex_file = open('data/' + data_set + '/model/lex.e2f', 'r').readlines()
    lex_dict = {}
    for l in lex_file:
        parts = l.split()
        en = parts[0].strip()
        de = parts[1].strip()
        score = float(parts[2])
        lex_dict[en, de] = score

    lex_file_inv = open('data/' + data_set + '/model/lex.f2e', 'r').readlines()
    lex_dict_inv = {}
    for l in lex_file_inv:
        parts = l.split()
        de = parts[0].strip()
        en = parts[1].strip()
        score = float(parts[2])
        lex_dict_inv[en, de] = score

    for e, d in lex_dict:
        score_e2f = lex_dict[e, d]
        score_f2e = lex_dict_inv[e, d]
        score = score_e2f * 0.5 + score_f2e * 0.5
        en2de[e].add((score, d))
        de2en[d].add((score, e))

    print 'read data completed...'

    for idx in range(20)[:]:

        # recursive solution
        source_l = train_en[idx].split()
        target_l = train_de[idx].split()
        # target_l = "señora presidenta , una cuestión de procedimiento .".split()
        # source_l = "madam president , on a point of order .".split()
        # = ['minute']
        # = ['un', 'minuto']  # .split()

        phrase_table = de2en
        if len(target_l) < 20 and len(source_l) < 20:
            print '****************', 'SOLUTION FOR', idx, '****************'
            start_state = SegmentState.SegmentState((0, len(target_l)), (0, len(source_l)), target_l, source_l)

            Q_recursion.append(start_state)
            # print 'pushed', start_state.target, start_state.source
            while len(Q_recursion) > 0:
                current_solution = Q_recursion.pop()
                # print(current_solution)
                best_solution = find_alignments(current_solution, phrase_table)
                # print 'best: ', best_solution.get_score()
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
            PrintCuts.print_levels(start_state)

            # print '\n********TREE CUTS********'
            # start_state.display = True
            # PrintCuts.print_cuts(start_state)




