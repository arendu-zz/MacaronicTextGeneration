__author__ = 'arenduchintala'
import pdb
from optparse import OptionParser


def generate_macaronic(a, d, e):
    a = [(int(g.split('-')[0]), int(g.split('-')[1])) for g in a.split()]
    ds = d.split()
    es = e.split()
    m = [es[x] for (x, y) in a]
    m_filter = [t1 for t1, t2 in zip(m, m[1:]) if t1 != t2]
    m_filter.append(m[-1])
    return ' '.join(m), ' '.join(m_filter)


if __name__ == '__main__':
    optparser = OptionParser()
    optparser.add_option("-a", "--alignment", dest="alignment", default="data/moses-files/model/aligned.grow-diag-final", help="full words for training")

    optparser.add_option("-d", "--de", dest="german_snt", default="data/training/train.clean.de", help="Test lemmas")
    optparser.add_option("-e", "--en", dest="english_snt", default="data/training/train.clean.en", help="tags for test set")
    (opts, _) = optparser.parse_args()

    alignments = open(opts.alignment, 'r').readlines()
    de = open(opts.german_snt, 'r').readlines()
    en = open(opts.english_snt, 'r').readlines()
    for a, d, e in zip(alignments, de, en):
        print a.strip()
        print d.strip()
        m, mf = generate_macaronic(a.strip(), d.strip(), e.strip())
        print mf
        print e.strip()
        print ''

