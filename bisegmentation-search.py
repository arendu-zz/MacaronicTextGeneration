__author__ = 'arenduchintala'
from collections import defaultdict
import SegmentState

global Q_key2state, Q_score2key
Q_key2state = {}
Q_score2key = []


def sub_array_match(span_list, string_list):
    if span_list[0] in string_list:
        idx = string_list.index(span_list[0])
        # TODO: make this check depend on the current coverage vector
        if ' '.join(span_list) == ' '.join(string_list[idx:idx + len(span_list)]):
            new_c = [False] * idx + [True] * (len(span_list)) + [False] * (len(string_list) - (idx + len(span_list)))
            # final_c = [i | j for i, j in zip(c, new_c)]
            return new_c, ' '.join(span_list)
        else:
            return [False] * len(string_list), None
    else:
        return [False] * len(string_list), None


def find_de_match(span, d_list, e_list):
    de_spans = list(en2de[span])
    if len(span.split()) == 1:
        print 'single word'
    de_spans.sort(reverse=True)
    for score_d, d_span in de_spans:
        coverage_de_new, match_str = sub_array_match(d_span.split(), d_list)
        if match_str is not None:
            print '\tMatch:', span, '--->', match_str
            coverage_en_new = [(s_idx <= i < s_idx + k) for i, t in enumerate(e_list)]
            return coverage_de_new, coverage_en_new, str(span + ' ---> ' + match_str), True
    print '\tNo Match:', span, '--->', 'NULL'
    return [False] * len(d_list), [False] * len(e_list), None, False


def pop_from_q():
    Q_score2key.sort()
    (score, cs_key) = Q_score2key.pop()
    cs = Q_key2state.pop(cs_key)
    print 'popped state', len(Q_key2state)
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
            print 'replaced state', len(Q_key2state)
        else:
            print 'ignored state', len(Q_key2state)
            pass  # there is a same state with lower score
    else:
        Q_key2state[new_cs.state_key()] = new_cs
        Q_score2key.append((new_cs.score, new_cs.state_key()))
        print 'added state', len(Q_key2state)


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
    """
    lex_file = open('data/coursera-large/model/lex.e2f', 'r').readlines()
    for l in lex_file:
        parts = l.split()
        en = parts[0].strip()
        de = parts[1].strip()
        score = float(parts[2])
        en2de[en].add((score, de))
        de2en[de].add((score, en))
    """
    global Q_key2state
    Q_key2state = {}
    e_list = train_en[0]
    d_list = train_de[0]
    e_list = e_list.split()
    d_list = d_list.split()
    init_state = SegmentState.SegmentState(e_list, d_list, 0.0)
    add_to_q(init_state)
    completed_states = []
    while len(Q_key2state) > 0:
        cs = pop_from_q()
        s_idx = cs.cov_target.index(False)
        for k in range(3, 0, -1):
            span_target = ' '.join(cs.target[s_idx:s_idx + k])
            if span_target in en2de:
                new_cov_source, new_cov_target, spans_matched, has_match = find_de_match(span_target, cs.source,
                                                                                         cs.target)
                if has_match:
                    new_cs = cs.get_copy()  # SegmentState.SegmentState(e_list, d_list, cs.score + 1)
                    new_cs.score += 1
                    new_cs.cov_source = [i | j for i, j in zip(cs.cov_source, new_cov_source)]
                    new_cs.cov_target = [i | j for i, j in zip(cs.cov_target, new_cov_target)]
                    new_cs.add_alignment(spans_matched)
                    if False not in new_cs.cov_source and False not in new_cs.cov_target:
                        completed_states.append(new_cs)
                        print 'added completed state'
                    else:
                        add_to_q(new_cs)
    print 'found alignments'




