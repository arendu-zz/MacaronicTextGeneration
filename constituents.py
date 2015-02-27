__author__ = 'arenduchintala'
from nltk.tree import Tree


if __name__ == '__main__':
    parses = open('data/moses-files/train.clean.tok.true.20.de.parse', 'r').readlines()
    for p_idx, p in enumerate(parses):
        t = Tree.fromstring(p, remove_empty_top_bracketing=True)
        t.collapse_unary(collapsePOS=True, collapseRoot=True, joinChar=' | ')
        l = t.leaves()
        n = len(l)
        for i in xrange(0, n - 1):
            for k in xrange(i + 1, n):
                span = k - i
                nid = t.treeposition_spanning_leaves(i, k)
                if isinstance(t[nid], Tree):
                    if len(t[nid].leaves()) == span:
                        labels = ','.join(t[nid].label().split(' | '))
                        ps = ' '.join([str(p_idx), str(i), str(k - 1), '|||', labels, '|||', ' '.join(l[i:k])])
                        print ps

                if isinstance(t[nid], str):
                    nid = nid[:-1]
                    labels = ','.join(t[nid].label().split(' | '))
                    ps = ' '.join([str(p_idx), str(i), str(k - 1), '|||', labels, '|||', ' '.join(l[i:k])])
                    print ps
