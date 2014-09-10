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
    optparser.add_option("-e", "--en", dest="english_snt", default="data/training/train.clean.tok.en",
                         help="tags for test set")
    optparser.add_option("-o", "--out", dest="output_sim", default="data/training/en.similarity",
                         help="tags for test set")
    (options, _) = optparser.parse_args()
    vocab_en = list(set(open(options.english_snt, 'r').read().split()))
    google_model = gensim.models.word2vec.Word2Vec.load_word2vec_format('data/GoogleNews-vectors-negative300.bin.gz',
                                                                        binary=True)

    for v in vocab_en:
        similar_v = [(-1, '')] * 20
        for k in vocab_en:
            if k != v:
                try:
                    cosine_dist = google_model.similarity(v, k)
                    cosine_dist = float(cosine_dist)
                    current_min, current_token = min(similar_v)
                    if cosine_dist > current_min:
                        similar_v[similar_v.index((current_min, current_token))] = (cosine_dist, k)
                    else:
                        pass
                except KeyError:
                    pass
                except:
                    print 'error_in', v, k
        if (-1, '') not in similar_v:
            s = ' '.join(["{0:.4f}".format(s[0]) + "," + s[1] for s in similar_v if s[0] > 0.0 and s[1] != ''])
            o = v + '\t' + ','.join([s[1] for s in similar_v])
            print o.decode('utf-8')




