# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"


import pymongo
import sys
import codecs

query_fr = {0: {'booktitle': 'EGC', 'language': 'FR', 'lemmaText': {'$exists': 'true'}},
            1: {'language': 'FR', 'lemmaText': {'$exists': 'true'}}}

query_en = {0: {'booktitle': 'EGC', 'language': 'EN', 'lemmaText': {'$exists': 'true'}},
            1: {'language': 'EN', 'lemmaText': {'$exists': 'true'}}}

words_fr = {}
words_en = {}

if __name__ == "__main__":
    dbname = sys.argv[1] #
    mode = int(sys.argv[2]) # 0 EGC corpus, 1 all corpus

    client = pymongo.MongoClient()
    db = client[dbname]

    authors_en = db.documents.find(query_en[mode], {'authors': 1, 'year': 1, 'words': 1}, sort=[("year", pymongo.ASCENDING)])
    print "English articles"
    for author in authors_en:
        for name in author['authors']:
            print author['year'], name.strip(' ')
        for word in author['words']:
            if words_en.get(author['year'], -1) == -1:
                words_en[author['year']] = {word['word']: word['count']}
            else:
                if words_en[author['year']].get(word['word'], -1) == -1:
                    words_en[author['year']][word['word']] = word['count']
                else:
                    words_en[author['year']][word['word']] += word['count']


    authors_fr = db.documents.find(query_fr[mode], {'authors': 1, 'year': 1, 'words': 1}, sort=[("year", pymongo.ASCENDING)])
    print "French articles"
    for author in authors_fr:
        for name in author['authors']:
            print author['year'], name.strip(' ')
        for word in author['words']:
            if words_fr.get(author['year'], -1) == -1:
                words_fr[author['year']] = {word['word']: word['count']}
            else:
                if words_fr[author['year']].get(word['word'], -1) == -1:
                    words_fr[author['year']][word['word']] = word['count']
                else:
                    words_fr[author['year']][word['word']] += word['count']

    for year in sorted(words_en, key=words_en.get, reverse=True):
        with codecs.open('word_frequency/frequency_en_'+year, mode='w', encoding='utf-8') as fout:
            for word in sorted(words_en[year], key=words_en[year].get, reverse=True):
                fout.write(word + ';' + str(words_en[year][word]) +'\n')
        fout.close()

    for year in sorted(words_fr, key=words_fr.get, reverse=True):
        with codecs.open('word_frequency/frequency_fr_'+year, mode='w', encoding='utf-8') as fout:
            for word in sorted(words_fr[year], key=words_fr[year].get, reverse=True):
                fout.write(word + ';' + str(words_fr[year][word]) +'\n')
        fout.close()
