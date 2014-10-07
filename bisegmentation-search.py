__author__ = 'arenduchintala'
from collections import defaultdict
import SegmentState
from pprint import pprint

global Q_key2state, Q_score2key
Q_key2state = {}
Q_score2key = []


def sub_array_match(d_span, d_list):
    if d_span[0] in d_list:
        idx = d_list.index(d_span[0])
        # TODO: make this check depend on the current coverage vector
        if ' '.join(d_span) == ' '.join(d_list[idx:idx + len(d_span)]):
            new_c = [False] * idx + [True] * (len(d_span)) + [False] * (len(d_list) - (idx + len(d_span)))
            # final_c = [i | j for i, j in zip(c, new_c)]
            return new_c, (idx, idx + len(d_span))
        else:
            return [False] * len(d_list), None
    else:
        return [False] * len(d_list), None


def find_match_in_source(target_span, cs):
    global en2de
    span_target_str = ' '.join(cs.target[target_span[0]:target_span[1]])
    if span_target_str in en2de:
        source_spans = list(en2de[span_target_str])
        source_spans.sort(reverse=True)
        for score_d, source_span in source_spans:
            cov_source_new, source_matched_span = sub_array_match(source_span.split(), cs.source)
            if source_matched_span is not None:
                cov_target_new = [(target_span[0] <= i < target_span[1]) for i, t in enumerate(cs.target)]
                return cov_source_new, cov_target_new, source_matched_span
    else:
        pass  # target span not in dictionary
    return [False] * len(cs.source), [False] * len(cs.target), None


def pop_from_q():
    Q_score2key.sort()
    (score, cs_key) = Q_score2key.pop()
    cs = Q_key2state.pop(cs_key)
    # print 'popped state', len(Q_key2state)
    return cs


def add_to_q(new_cs):
    global Q_key2state
    if new_cs.state_key() in Q_key2state:
        existing_key = new_cs.state_key()
        old_cs = Q_key2state[existing_key]  # old state obj with same coverage
        if new_cs.score < old_cs.score:  # this is broken TODO: what should really be the score?
            Q_key2state[existing_key] = new_cs
            Q_score2key.remove((old_cs.score, existing_key))
            Q_score2key.append((new_cs.score, existing_key))
            print '******************************replaced state************************', new_cs.state_key()
            print 'len of Q', len(Q_key2state)
        else:
            # print 'ignored state', new_cs.state_key()
            # print 'len of Q', len(Q_key2state)
            pass  # there is a same state with lower score
    else:
        Q_key2state[new_cs.state_key()] = new_cs
        Q_score2key.append((new_cs.score, new_cs.state_key()))
        # print 'adding state', new_cs.state_key()
        # print 'len of Q', len(Q_key2state)


def find_alignments(start_state):
    global Q_key2state
    Q_key2state = {}
    solutions = {}
    add_to_q(start_state)
    while len(Q_key2state) > 0:
        cs = pop_from_q()
        if "0" not in cs.state_key() or False not in cs.cov_target:
            print 'completed result:', cs.state_key(), 'score:', cs.score
            solutions[cs.score] = cs
            print 'found alignment with score:', cs.score
            for a in cs.display_alignment():
                print '\t', a
            print 'ok'
        else:
            s_idx = cs.cov_target.index(False)
            # print 'S_IDX:', s_idx, '/', len(cs.cov_target)
            for k in range(5, 0, -1):
                span_target = (s_idx, s_idx + k)
                new_cov_source, new_cov_target, source_span_match = find_match_in_source(span_target, cs)
                if source_span_match is not None:
                    new_cs = cs.get_copy()  # SegmentState.SegmentState(e_list, d_list, cs.score + 1)
                    new_cs.score += 1
                    new_cs.cov_source = [i | j for i, j in zip(cs.cov_source, new_cov_source)]
                    new_cs.cov_target = [i | j for i, j in zip(cs.cov_target, new_cov_target)]
                    target_span = (s_idx, s_idx + k)
                    new_cs.add_alignment(target_span, source_span_match)
                    # if False not in new_cs.cov_source and False not in new_cs.cov_target:
                    # completed_states.append(new_cs)
                    # print 'added completed state'
                    # else:
                    if new_cs.state_key == cs.state_key:
                        print ' has a match, but the coverage has not changed'
                    add_to_q(new_cs)
                else:
                    pass
    return solutions


if __name__ == "__main__":
    phrase_table_file = open('data/coursera-large/model/phrase-table', 'r').readlines()
    train_en = open('data/coursera-large/train.clean.tok.en', 'r').readlines()
    train_de = open('data/coursera-large/train.clean.tok.es', 'r').readlines()
    en2de = defaultdict(set)
    de2en = defaultdict(set)
    for pt in phrase_table_file:
        parts = pt.split('|||')
        if len(parts[0].split()) < 6 and len(parts[1].split()) < 6:
            en = parts[0].strip()
            de = parts[1].strip()
            scores = [float(sc) for sc in parts[2].split()]
            score = scores[0] * scores[1] + scores[2] * scores[3]
            en2de[en].add((score, de))
            de2en[de].add((score, en))

    lex_file = open('data/coursera-large/model/lex.e2f', 'r').readlines()
    for l in lex_file:
        parts = l.split()
        en = parts[0].strip()
        de = parts[1].strip()
        score = float(parts[2])
        en2de[en].add((score, de))
        de2en[de].add((score, en))

    start_state = SegmentState.SegmentState(train_en[100].split(), train_de[100].split(), 0.0)
    solutions = find_alignments(start_state)
    for s in solutions:
        print 'found alignment with score:', s
        for a in solutions[s].display_alignment():
            print '\t', a





