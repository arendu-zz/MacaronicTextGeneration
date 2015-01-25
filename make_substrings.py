__author__ = 'arenduchintala'
from optparse import OptionParser
import codecs

if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option("--ce", dest="en_corpus", default="train.clean.tok.true.en", help="english corpus sentences")
    opt.add_option("--cd", dest="de_corpus", default="train.clean.tok.true.de", help="german corpus sentences")
    opt.add_option("-d", dest="data_set", default="data/moses-files/")
    (options, _) = opt.parse_args()

    data_set = options.data_set
    de_sentences = codecs.open(data_set + options.de_corpus, 'r', 'utf-8').readlines()

    span_file = codecs.open(data_set + options.de_corpus + '.span', 'w', 'utf-8')
    txt_span_file = codecs.open(data_set + options.de_corpus + '.txtspan', 'w', 'utf-8')
    for idx, de_sent in enumerate(de_sentences[:20]):
        de_sent = de_sent.split()
        n = len(de_sent)
        for span in xrange(0, n):
            for i in xrange(0, n - span):
                k = i + span
                span_file.write(str(idx) + ' ' + str(i) + ' ' + str(k) + '\n')
                s = '$UNK$ <wall /> ' + ' '.join(de_sent[i:k + 1]) + ' <wall /> $UNK$'
                txt_span_file.write(s + '\n')