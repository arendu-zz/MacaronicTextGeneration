__author__ = 'arenduchintala'

"""
this script generates similar words using nltk wordnet
"""
from nltk.corpus import wordnet as wn
import sys, codecs
from optparse import OptionParser

if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    sys.stdin = codecs.getwriter('utf-8')(sys.stdin)
    optparser = OptionParser()
    optparser.add_option("-e", "--en", dest="english_snt", default="data/training/train.clean.tok.en", help="tags for test set")
    optparser.add_option("-o", "--out", dest="output_sim", default="data/training/en.sim.wn", help="tags for test set")
    (options, _) = optparser.parse_args()
    vocab_en = list(set(open(options.english_snt, 'r').read().split()))

    for v in vocab_en:
        syn_tokens = []
        for s in wn.synsets(v):
            for l in s.lemmas:
                if '_' not in l.name and l.name != v:
                    syn_tokens.append(l.name)
        if len(syn_tokens) > 0:
            out = v + '\t' + ','.join(set(syn_tokens))
            print out.decode('utf-8')

