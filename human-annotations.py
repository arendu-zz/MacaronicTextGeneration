__author__ = 'arenduchintala'
"""
Takes in a tree text file as input. e.g. output/bottom-up-tree.out.pruned.1.txt
"""
import codecs, re

if __name__ == '__main__':
    txt_trees = codecs.open('outputs/bottom-up-tree.out.pruned.1.alt.span.txt', 'r', 'utf-8').read().rstrip()
    txt_trees = re.split(r'\n\n+', txt_trees)
    for idx, a_tree in enumerate(txt_trees):
        tree_lines = a_tree.split('\n')[1:]
        span_to_str = {}
        try:
            print 'Sentence', idx + 1
            tl0 = tree_lines[0]
            st = tl0.index('(')
            en = tl0.index(')')
            tl0 = tl0[0:st] + tl0[en + 1:]
            print 'full english:', tl0
            tree_lines_w_span = tree_lines[len(tree_lines) / 2]
            tree_line_no_span = []
            for tl in tree_lines_w_span.split('|'):
                st = tl.index('(')
                en = tl.index(')')
                span = tuple([int(i) for i in tl[st + 1:en].split(',')])
                tl_no_span = tl[0:st] + tl[en + 1:]
                tree_line_no_span.append(tl_no_span)
                span_to_str[span] = tl_no_span
            print 'middle cut  :', '|'.join(tree_line_no_span)
            print 'full german :', tree_lines[len(tree_lines) - 1]
            print '\n Enter translation alternative for the following'
            for span in sorted(span_to_str):
                print '\t', span, span_to_str[span].strip(), ':'
            print ''
        except:
            pass



