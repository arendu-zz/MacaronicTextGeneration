__author__ = 'arenduchintala'
"""
this script uses gensim's word2vec to take in the english corpus, and come up with most similar 20 words
for each word in the english vocab.
"""
from optparse import OptionParser
import gensim
import codecs, sys

if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    sys.stdin = codecs.getwriter('utf-8')(sys.stdin)
    optparser = OptionParser()
    optparser.add_option("-e", "--en", dest="english_snt", default="data/training/train.clean.tok.en", help="tags for test set")
    optparser.add_option("-o", "--out", dest="output_sim", default="data/training/en.similarity", help="tags for test set")
    (options, _) = optparser.parse_args()
    vocab_en = list(set(open(options.english_snt, 'r').read().split()))
    google_model = gensim.models.word2vec.Word2Vec.load_word2vec_format('data/GoogleNews-vectors-negative300.bin.gz', binary=True)

    for v in vocab_en:
        similar_v = []
        for k in vocab_en:
            try:
                cosine_dist = google_model.similarity(v, k)
                current_min = min(similar_v)[0]
                if len(similar_v) <= 20:
                    similar_v.append((cosine_dist, k))
                elif cosine_dist > current_min:
                    similar_v[similar_v.index(current_min)] = (cosine_dist, k)
                else:
                    pass
            except KeyError:
                pass
        if len(similar_v) == 20:
            s = ' '.join(["{0:.4f}".format(s[1]) + "," + s[0] for s in similar_v])
            o = v + '\t' + ','.join([s[1] for s in similar_v])
            print o.decode('utf-8')




