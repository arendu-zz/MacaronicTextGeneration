__author__ = 'arenduchintala'
"""
Takes in a tree text file as input. e.g. output/bottom-up-tree.out.pruned.10.txt
"""
import codecs
import pdb
import traceback
import re

if __name__ == '__main__':
    txt_trees = codecs.open('outputs/bottom-up-tree.out.pruned.10.alt.span.txt', 'r', 'utf-8').read().rstrip()
    txt_trees = re.split(r'\n\n+', txt_trees)
    for idx in xrange(0, len(txt_trees), 2):
        a_tree = txt_trees[idx]
        span_tree = txt_trees[idx + 1]
        span_to_str = {}
        try:
            a_tree_lines = a_tree.split('\n')
            if a_tree_lines[0].strip() is '':
                a_tree_lines.pop(0)
            a_span_lines = span_tree.split('\n')
            assert len(a_span_lines) == len(a_tree_lines)

            print 'Sentence', idx + 1
            tl0 = a_tree_lines[0]
            print u'full english:', tl0.encode('utf-8')
            print u'middle cut  :', a_tree_lines[int(len(a_tree_lines) / 2)].encode('utf-8')
            print u'full german :', a_tree_lines[len(a_tree_lines) - 1].encode('utf-8')
            print u'\nEnter an alternative translation for the following:'
            sls = a_span_lines[int(len(a_span_lines) / 2)]
            atl = a_tree_lines[int(len(a_tree_lines) / 2)]
            bb = [tuple([int(p) for p in re.split(r'[\(,\)]', i)[1:-1]]) for i in sls.split('|')]
            xx = [(bb[idx][1] + 1 == n1) for idx, (n1, n2) in enumerate(bb[1:])]
            if False in xx:
                atl = a_tree_lines[int(len(a_tree_lines) / 2) - 1]
                sls = a_span_lines[int(len(a_span_lines) / 2) - 1]
                bb = [tuple([int(p) for p in re.split(r'[\(,\)]', i)[1:-1]]) for i in sls.split('|')]
                xx = [(bb[idx][1] + 1 == n1) for idx, (n1, n2) in enumerate(bb[1:])]
                assert False not in xx
            assert len(sls.split('|')) == len(atl.split('|'))
            gx = [g.strip() for g in a_tree_lines[-1].split('|')]
            for st, tl in zip(sls.split('|'), atl.split('|')):
                st = [int(str(i)) for i in re.split(r'[\(\),]', st) if str(i).strip() is not '']
                print u'\t', tuple(st), ' '.join(gx[st[0]:st[1] + 1]).encode('utf-8'), "|||", tl.strip().encode(
                    'utf-8'), ":"

            print ''
        except BaseException:
            traceback.print_exc()
            raise BaseException()



