# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import pymongo
import codecs
import sys

query_fr = {0: {'booktitle': 'EGC', 'language': 'FR', 'lemmaText': {'$exists': 'true'}},
            1: {'language': 'FR', 'lemmaText': {'$exists': 'true'}}}

query_en = {0: {'booktitle': 'EGC', 'language': 'EN', 'lemmaText': {'$exists': 'true'}},
            1: {'language': 'EN', 'lemmaText': {'$exists': 'true'}}}

filepath_fr = {0: 'online_twitter_lda/EGC_corpus/input_fr/', 1: 'online_twitter_lda/all_corpus/input_fr/'}
filepath_en = {0: 'online_twitter_lda/EGC_corpus/input_en/', 1: 'online_twitter_lda/all_corpus/input_en/'}

filepath = {0: 'online_twitter_lda/EGC_corpus/', 1: 'all_corpus/'}

if __name__ == "__main__":
    dbname = sys.argv[1] #
    mode = int(sys.argv[2]) # 0 EGC corpus, 1 all corpus
    no_topics = sys.argv[3] # number of topics

    client = pymongo.MongoClient()
    db = client[dbname]

    documents_en = {}
    cursor_en = db.documents.find(query_en[mode], {'year': 1, 'lemmaText': 1,})
    for elem in cursor_en:
        if documents_en.get(elem['year'], -1) == -1:
            documents_en[elem['year']] = [elem['lemmaText']]
        else:
            documents_en[elem['year']] += [elem['lemmaText']]

    for key in documents_en:
        timefilename = filepath_en[mode] + key + '0000.time'
        textfilename = filepath_en[mode] + key + '0000.text'
        f_time = codecs.open(timefilename, 'w', encoding='utf8')
        f_text = codecs.open(textfilename, 'w', encoding='utf8')
        for doc in documents_en[key]:
            f_time.write(key+ '0000\n')
            f_text.write(doc+'\n')
        f_time.close()
        f_text.close()

    documents_fr = {}
    cursor_fr = db.documents.find(query_fr[mode], {'year': 1, 'lemmaText': 1})
    for elem in cursor_fr:
        if documents_fr.get(elem['year'], -1) == -1:
            documents_fr[elem['year']] = [elem['lemmaText']]
        else:
            documents_fr[elem['year']] += [elem['lemmaText']]

    for key in documents_fr:
        timefilename = filepath_fr[mode] + key + '0000.time'
        textfilename = filepath_fr[mode] + key + '0000.text'
        f_time = codecs.open(timefilename, 'w', encoding='utf8')
        f_text = codecs.open(textfilename, 'w', encoding='utf8')
        for doc in documents_fr[key]:
            f_time.write(key+ '0000\n')
            f_text.write(doc+'\n')
        f_time.close()
        f_text.close()


