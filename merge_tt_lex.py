# -*- coding: utf-8 -*-
__author__ = 'arenduchintala'
from optparse import OptionParser
import sys

if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option('--l1', dest='lexe2f', help='lex.e2f file')
    opt.add_option('--l2', dest='lexf2e', help='lex.f2e file')
    opt.add_option('--tt', dest='phrasetable', help='phrase table file')
    (options, _) = opt.parse_args()
    seen_pairs = {}
    with open(options.phrasetable) as f:
        for line in f:
            args = line.split('|||')
            de = args[0].strip()
            en = args[1].strip()
            if len(de.split()) == 1 and len(en.split()) == 1:
                seen_pairs[(de, en)] = 1

    lexe2f = {}
    with open(options.lexe2f) as f:
        for line in f:
            args = line.split()
            # line =[de, en, score]
            de, en = args[0].strip(), args[1].strip()
            if (de, en) not in seen_pairs:
                lexe2f[de, en] = float(args[2].strip())

    lexf2e = {}
    with open(options.lexf2e) as f:
        for line in f:
            args = line.split()
            # line =[en, de, score]
            en, de = args[0].strip(), args[1].strip()
            if (de, en) not in seen_pairs:
                lexf2e[de, en] = float(args[2].strip())

    for k in lexe2f.viewkeys() & lexf2e.viewkeys():
        t_e2f, l_e2f, t_f2e, l_f2e = lexe2f[k], lexe2f[k], lexf2e[k], lexf2e[k]
        l = [k[0]], k[1], ' '.join([t_e2f, l_e2f, t_f2e, l_f2e], '0-0', '1 1 1', '')
        sys.stdout.write(' ||| '.join(l) + '\n')
