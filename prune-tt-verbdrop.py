__author__ = 'arenduchintala'
from optparse import OptionParser
import codecs

if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option("-t", dest="ttable", default="~/MachineTranslation/MyExperiments/WMT2013/model/phrase.table.4")
    opt.add_option("-s", dest="word2unipos", default="data/projectsyndicate/de.pos")
    (options, _) = opt.parse_args()
    f = codecs.open(options.ttable, 'r', 'utf-8')
    i = 0
    with f:
        for line in f:
            #! – auch ||| – also ||| 0.00217246 1.23546e-05 0.00814672 0.164632 ||| 1-0 2-1 ||| 15 4 1 ||| |||
            parms = line.split('|||')


            i+=1
            if i > 200:
                break;


