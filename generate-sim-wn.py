__author__ = 'arenduchintala'

"""
this script generates similar words using nltk wordnet
"""
from nltk.corpus import wordnet as wn
import sys, codecs, pdb
from optparse import OptionParser

if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    sys.stdin = codecs.getwriter('utf-8')(sys.stdin)
    optparser = OptionParser()
    optparser.add_option("-e", "--en", dest="english_snt", default="data/training/train.clean.tok.en",
                         help="tags for test set")
    optparser.add_option("-p", "--phrase", dest="allow_phrase", default=False, help="allow phrasal thesaurus entries")
    (options, _) = optparser.parse_args()
    vocab_en = set(open(options.english_snt, 'r').read().lower().split())
    allow_phrase = options.allow_phrase
    for v in vocab_en:
        syn_tokens = []
        for s in wn.synsets(v):
            for l in s.lemmas:
                k = l.name.lower()
                if allow_phrase:
                    if k != v:
                        k = ' '.join(k.split('_')).decode('utf-8')
                        syn_tokens.append(k)
                else:
                    if '_' not in k and k != v:
                        syn_tokens.append(k)
        if len(syn_tokens) > 0:
            out = v + '\t' + ','.join(set(syn_tokens))
            print out.decode('utf-8')

