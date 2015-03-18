__author__ = 'arenduchintala'

from optparse import OptionParser
from nltk.tree import Tree
import pdb


if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option("-p", dest="parse", default="data/projectsyndicate/projectsyndicate.clean.de.20.parse")
    (options, _) = opt.parse_args()
    parses = open(options.parse, 'r').readlines()
    parsespans = open(options.parse + '.spans', 'w')
    for p_idx, p in enumerate(parses):
        t = Tree.fromstring(p, remove_empty_top_bracketing=True)
        t.collapse_unary(collapsePOS=True, collapseRoot=True, joinChar=' | ')
        l = t.leaves()
        n = len(l)
        for i in xrange(0, n):
            for k in xrange(i + 1, n + 1):
                span = k - i
                nid = t.treeposition_spanning_leaves(i, k)
                if isinstance(t[nid], Tree):
                    if len(t[nid].leaves()) == span:
                        labels = ','.join(t[nid].label().split(' | '))
                        ps = ' '.join([str(p_idx), str(i), str(k - 1), '|||', labels, '|||', ' '.join(l[i:k])])
                        # print ps
                        parsespans.write(ps + '\n')

                if isinstance(t[nid], str):
                    nid = nid[:-1]
                    labels = ','.join(t[nid].label().split(' | '))
                    ps = ' '.join([str(p_idx), str(i), str(k - 1), '|||', labels, '|||', ' '.join(l[i:k])])
                    # print ps
                    parsespans.write(ps + '\n')
                    # t.draw()
                    # pdb.set_trace()
