__author__ = 'arenduchintala'
import nltk.tokenize as tokenize

if __name__ == '__main__':
    en = open('train.clean.en', 'r').readlines()
    de = open('train.clean.de', 'r').readlines()
    en_clean = open('train.clean.tok.en', 'w')
    de_clean = open('train.clean.tok.de', 'w')
    de_en_clean = open('train.clean.de-en', 'w')
    en_de_clean = open('train.clean.en-de', 'w')
    for e, d in zip(en, de):
        if e.strip() != '' and d.strip() != '':
            e_clean_tok = ' '.join(tokenize.word_tokenize(e.strip())) 
            d_clean_tok = ' '.join(tokenize.word_tokenize(d.strip()))
            en_clean.write(e_clean_tok + '\n')
            de_clean.write(d_clean_tok+ '\n')
            de_en_clean.write(d_clean_tok + ' ||| ' + e_clean_tok + '\n')
            en_de_clean.write(e_clean_tok + ' ||| ' + d_clean_tok + '\n')

    en_de_clean.flush()
    en_de_clean.close()

    de_en_clean.flush()
    de_en_clean.close()

    en_clean.flush()
    en_clean.close()

    de_clean.flush()
    de_clean.close()
