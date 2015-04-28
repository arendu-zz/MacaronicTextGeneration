__author__ = 'arenduchintala'
from optparse import OptionParser

if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option("-t", dest="ttable", default="~/MachineTranslation/MyExperiments/WMT2013/model/phrase.table.4")
    opt.add_option("-s", dest="word2unipos", default="data/projectsyndicate/de.pos")
    (options, _) = opt.parse_args()

