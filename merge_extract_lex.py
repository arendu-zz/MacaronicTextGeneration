# -*- coding: utf-8 -*-
__author__ = 'arenduchintala'
"""
This is just like merge_tt_lex.py except instead of merging directly in
the phrase table we add phrases into the list of extracted phrases
"""
from optparse import OptionParser
import sys

if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option('--l1', dest='lexe2f', help='lex.e2f file')
    opt.add_option('--l2', dest='lexf2e', help='lex.f2e file')
    opt.add_option('--tt', dest='phrasetable', help='phrase table file')
    opt.add_option('-e', dest='addition2extract', default='addition2extract', help='phrase pairs to add to extracted')
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
    w_inv = open(options.addition2extract+'.inv', 'w')
    w_o = open(options.addition2extract+'.o', 'w')
    w = open(options.addition2extract, 'w')

    for k in lexe2f.viewkeys() & lexf2e.viewkeys():
        de, en = k
        inv_str = en.strip() + ' ||| ' + de.strip() + ' ||| 0-0\n'
        i_str = de.strip() + ' ||| ' + en.strip() + ' ||| 0-0\n'
        o_str1 = de.strip() + ' ||| ' + en.strip() + ' ||| mono mono\n'
        o_str2 = de.strip() + ' ||| ' + en.strip() + ' ||| mono other\n'
        o_str3 = de.strip() + ' ||| ' + en.strip() + ' ||| other mono\n'
        w_inv.write(inv_str)
        w_o.write(o_str1)
        w_o.write(o_str2)
        w_o.write(o_str3)
        w.write(i_str)
    w.flush()
    w_inv.flush()
    w_o.flush()
    w.close()
    w_inv.close()
    w_o.close()
