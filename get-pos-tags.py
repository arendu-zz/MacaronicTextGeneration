# -*- coding: utf-8 -*-
__author__ = 'arenduchintala'
from optparse import OptionParser
from nltk import ParentedTree
import codecs

if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option("-p",
                   dest="parse",
                   default="data/projectsyndicate/projectsyndicate.truecased.de.20.parse",
                   help="german parses parse persentence")
    opt.add_option("-m", dest="map", default="data/projectsyndicate/de-negra.map")
    opt.add_option("-s", dest="word2unipos", default="data/projectsyndicate/de.pos")
    (options, _) = opt.parse_args()
    word2pos = {}
    f = codecs.open(options.parse, 'r', 'utf-8')
    posmap = {}
    for line in codecs.open(options.map, 'r', 'utf-8').readlines():
        de_pos, uni_pos = line.split()
        posmap[de_pos] = uni_pos

    with f:
        for line in f:
            t = ParentedTree.fromstring(line.strip())
            for pos_token in t.subtrees(lambda t: t.height() == 2):
                pos_token = str(pos_token)[1:-1]
                (pos, token) = pos_token.split()
                token = token.encode('utf-8')
                s = word2pos.get(token, set())
                s.add(posmap[pos])
                word2pos[token] = s
    f.close()
    w = codecs.open(options.word2unipos, 'w', 'utf-8')
    for token, set_pos in word2pos.items():
        print token, ':', ','.join(set_pos)
        w.write(token.encode('utf-8') + '\t' + ','.join(set_pos) + '\n')
    w.flush()
    w.close()



