# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import pymongo
import codecs

if __name__ == "__main__":
    dbname = 'EGCDB'
    client = pymongo.MongoClient()
    db = client[dbname]

    filepath_fr = 'online_twitter_lda/input_fr/'
    filepath_en = 'online_twitter_lda/input_en/'

    documents_en = {}
    cursor_en = db.documents.find({'language': 'EN', 'lemmaText': {'$exists': 'true'}}, {'year': 1, 'lemmaText': 1,})
    for elem in cursor_en:
        if documents_en.get(elem['year'], -1) == -1:
            documents_en[elem['year']] = [elem['lemmaText']]
        else:
            documents_en[elem['year']] += [elem['lemmaText']]

    documents_fr = {}
    cursor_fr = db.documents.find({'language': 'FR', 'lemmaText': {'$exists': 'true'}}, {'year': 1, 'lemmaText': 1})
    for elem in cursor_fr:
        if documents_fr.get(elem['year'], -1) == -1:
            documents_fr[elem['year']] = [elem['lemmaText']]
        else:
            documents_fr[elem['year']] += [elem['lemmaText']]

    for key in documents_en:
        timefilename = filepath_en + key + '0000.time'
        textfilename = filepath_en + key + '0000.text'
        f_time = codecs.open(timefilename, 'w', encoding='utf8')
        f_text = codecs.open(textfilename, 'w', encoding='utf8')
        for doc in documents_en[key]:
            f_time.write(key+ '0000\n')
            f_text.write(doc+'\n')
        f_time.close()
        f_text.close()

    for key in documents_fr:
        timefilename = filepath_fr + key + '0000.time'
        textfilename = filepath_fr + key + '0000.text'
        f_time = codecs.open(timefilename, 'w', encoding='utf8')
        f_text = codecs.open(textfilename, 'w', encoding='utf8')
        for doc in documents_fr[key]:
            f_time.write(key+ '0000\n')
            f_text.write(doc+'\n')
        f_time.close()
        f_text.close()


