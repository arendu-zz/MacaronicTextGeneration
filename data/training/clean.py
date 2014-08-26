__author__ = 'arenduchintala'
import nltk.tokenize as tokenize

if __name__ == '__main__':
    en = open('train.clean.en', 'r').readlines()
    de = open('train.clean.de', 'r').readlines()
    # en_clean = open('train.clean.en', 'w')
    # de_clean = open('train.clean.de', 'w')
    de_en_clean = open('train.clean.de-en', 'w')
    en_de_clean = open('train.clean.en-de', 'w')
    for e, d in zip(en, de):
        if e.strip() != '' and d.strip() != '':
            # en_clean.write(e.strip() + '\n')
            # de_clean.write(d.strip() + '\n')
            de_en_clean.write(' '.join(tokenize.word_tokenize(d.strip())) + ' ||| ' + ' '.join(tokenize.word_tokenize(e.strip())) + '\n')
            en_de_clean.write(' '.join(tokenize.word_tokenize(e.strip())) + ' ||| ' + ' '.join(tokenize.word_tokenize(d.strip())) + '\n')

    en_de_clean.flush()
    en_de_clean.close()

    de_en_clean.flush()
    de_en_clean.close()

    # en_clean.flush()
    # en_clean.close()

    # de_clean.flush()
    # de_clean.close()
