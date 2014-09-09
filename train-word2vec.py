__author__ = 'arenduchintala'
"""
trains a word2vec model using the training data
"""
from optparse import OptionParser
import gensim, codecs, sys

if __name__ == '__main__':
    optparser = OptionParser()
    optparser.add_option("-e", "--en", dest="english_snt", default="data/training/train.clean.tok.en", help="tags for test set")
    optparser.add_option("-o", "--out", dest="output_model", default="data/training/word2vec.bin", help="tags for test set")
    (options, _) = optparser.parse_args()

    sentences = codecs.open(options.english_snt, 'r', encoding='UTF-8').readlines()
    model = gensim.models.word2vec.Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    model.save_word2vec_format(options.output_model, binary=True)