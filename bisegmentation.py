__author__ = 'arenduchintala'
from collections import defaultdict
import re
import pdb


def disp_binary_list(lst):
    bl = [int(l) for l in lst]
    print '\t', bl


def sub_array_match(span_list, string_list, c):
    if span_list[0] in string_list:
        idx = string_list.index(span_list[0])
        # TODO: make this check depend on the current coverage vector
        if ' '.join(span_list) == ' '.join(string_list[idx:idx + len(span_list)]):
            new_c = [False] * idx + [True] * (len(span_list)) + [False] * (len(string_list) - (idx + len(span_list)))
            final_c = [i | j for i, j in zip(c, new_c)]
            return final_c, ' '.join(span_list)
        else:
            return c, None
    else:
        return c, None


def find_de_match(span, d_list, coverage_de):
    de_spans = list(en2de[span])
    if len(span.split()) == 1:
        print 'single word'
    de_spans.sort(reverse=True)
    for score_d, d_span in de_spans:
        coverage_de, match_str = sub_array_match(d_span.split(), d_list, coverage_de)
        if match_str is not None:
            print '\tMatch:', span, '--->', match_str
            return coverage_de, True
    print '\tNo Match:', span, '--->', 'NULL'
    return coverage_de, False


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

    print len(en2de), len(de2en)
    for e_list, d_list in zip(train_en, train_de)[1:2]:
        e_list = e_list.split()
        d_list = d_list.split()
        coverage_de = [False] * len(d_list)
        coverage_en = [False] * len(e_list)
        s_idx = 0
        while s_idx < len(e_list):
            k = 5
            has_de_match = False
            while k > 0:
                span_en = ' '.join(e_list[s_idx:s_idx + k])
                if span_en in en2de:
                    print "span:", s_idx, s_idx + k, span_en, ':is present in phrase table'
                    coverage_de, has_de_match = find_de_match(span_en, d_list, coverage_de)
                    if has_de_match:
                        coverage_en = [(s_idx <= i < s_idx + k) | t for i, t in enumerate(coverage_en)]
                        disp_binary_list(coverage_en)
                        disp_binary_list(coverage_de)
                        s_idx += k
                        k = 5
                        break
                    else:
                        print "span:", s_idx, s_idx + k, span_en, ':could not find match in de side'
                        k -= 1
                else:
                    print "span:", s_idx, s_idx + k, span_en, ':is not present phrase table'
                    k -= 1
            if not has_de_match:
                s_idx += 1

















