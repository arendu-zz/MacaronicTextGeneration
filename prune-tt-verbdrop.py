__author__ = 'arenduchintala'
from optparse import OptionParser
import codecs

if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option("-t", dest="ttable", default="~/MachineTranslation/MyExperiments/WMT2013/model/phrase.table.4")
    opt.add_option("-s", dest="word2unipos", default="data/projectsyndicate/de.pos")
    (options, _) = opt.parse_args()
    f = codecs.open(options.ttable, 'r', 'utf-8')
    verbs = set([])
    word2unipos = codecs.open(options.word2unipos, 'r', 'utf-8')
    for line in word2unipos.readlines():
        token = line.split()[0]
        pos = line.split()[1].split(',')
        if 'VERB' in pos:
            verbs.add(token)
    word2unipos.close()
    i = 0
    with f:
        for line in f:
            #! – auch ||| – also ||| 0.00217246 1.23546e-05 0.00814672 0.164632 ||| 1-0 2-1 ||| 15 4 1 ||| |||
            parms = line.split('|||')
            de = parms[0].split()
            en = parms[1].split()
            alignments = parms[3].split()
            de_aglined = set([int(p.split('-')[0]) for p in alignments])
            de_aligned_to_null = set([token for idx, token in enumerate(de) if idx not in de_aglined])
            verbs_aligned_to_null = de_aligned_to_null.intersection(verbs)
            if len(verbs_aligned_to_null) == 0:
                print "OK  ", line
            else:
                print "SKIP", line
                print verbs_aligned_to_null

            i += 1
            if i > 200:
                break;


