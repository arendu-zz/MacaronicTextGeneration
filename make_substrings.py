__author__ = 'arenduchintala'
from optparse import OptionParser
import codecs

if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option("--ce", dest="en_corpus", default="data/projectsyndicate/projectsyndicate.clean.en.20",
                   help="english corpus sentences")
    opt.add_option("--cd", dest="de_corpus", default="data/projectsyndicate/projectsyndicate.clean.de.20",
                   help="german corpus sentences")
    (options, _) = opt.parse_args()

    de_sentences = codecs.open(options.de_corpus, 'r', 'utf-8').readlines()

    span_file = codecs.open(options.de_corpus + '.span', 'w', 'utf-8')
    txt_zone_file = codecs.open(options.de_corpus + '.txtspan', 'w', 'utf-8')

    for idx, de_sent in enumerate(de_sentences[:20]):
        de_sent = de_sent.split()
        n = len(de_sent)
        for span in xrange(0, n):
            for i in xrange(0, n - span):
                k = i + span
                span_file.write(str(idx) + ' ' + str(i) + ' ' + str(k) + ' '+ str(n)+'\n')
                s = '$UNK$ <wall/> ' + ' '.join(de_sent[i:k + 1]) + ' <wall/> $UNK$'
                txt_zone_file.write(s + '\n')
