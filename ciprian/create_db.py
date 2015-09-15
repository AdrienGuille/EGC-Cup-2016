# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import pymongo
import utils
from nlplib.lemmatize_text import LemmatizeText
from nlplib.clean_text import CleanText
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
from langdetect import detect

"""
class CreateDB_EGC:
    def __init__(self, dbname='EGCDB'):
        client = pymongo.MongoClient()
        self.db = client[dbname]
        self.ct = CleanText()

    def insert_data(self, corpus):
        documents = []
        no_threads = cpu_count()
        with ProcessPoolExecutor(max_workers=no_threads) as worker:
            for result in worker.map(self.process_element, corpus):
                if result:
                    documents.append(result)
        if documents:
            try:
                self.db.documents.insert(documents, continue_on_error=True)
            except pymongo.errors.DuplicateKeyError:
                pass


    # series,
    # booktitle,
    # year,
    # title,
    # abstract,
    # author,
    # pdf1page,
    # pdfarticle.

    # process one element parallel
    def process_element(self, elem):
        document = dict()
        if len(elem) == 7:
            try:

                lang = detect(elem[4]).upper()
                cleanText = self.ct.cleanTextSimple(elem[4], lang)
                # if clean text exists
                if len(self.ct.removePunctuation(cleanText)) > 0:
                    # extract lemmas and part of speech
                    lemmas = LemmatizeText(rawText=self.ct.removePunctuation(cleanText), language=lang)
                    lemmas.createLemmaText()
                    lemmaText = lemmas.cleanText
                    if lemmaText and lemmaText != " ":
                        lemmas.createLemmas()
                        words = []
                        for w in lemmas.wordList:
                            word = dict()
                            word['word'] = w.word
                            word['tf'] = w.tf
                            word['count'] = w.count
                            word['pos'] = w.wtype
                            words.append(word)

                        # construct the document
                        document['rawText'] = elem[4]#.encode('utf8').encode('string_escape').replace('\r', '').replace('\n', '')
                        document['cleanText'] = cleanText#.encode('utf8').encode('string_escape').replace('\r', '').replace('\n', '')
                        document['lemmaText'] = lemmaText
                        document['series'] = elem[0]
                        document['booktitle'] = elem[1]
                        document['year'] = elem[2]
                        document['title'] = elem[3]

                        #authors
                        authors = []
                        for a in elem[5].split(','):
                            author = dict()
                            names = a.split(' ')
                            author['firstname'] = ' '.join(names[:-1])
                            author['lastname'] = names[-1]
                            authors.append(author)
                        document['authors'] = authors
                        document['source'] = elem[6]
                        document['words'] = words
            except Exception as e:
                print e
        return document
"""
ct = CleanText()
def insert_data(dbname, corpus, remove=False):
    client = pymongo.MongoClient()
    db = client[dbname]
    if remove:
        db.documents.remove({})
    documents = []
    no_threads = cpu_count()
    with ProcessPoolExecutor(max_workers=no_threads) as worker:
        for result in worker.map(process_element, corpus):
            if result:
                documents.append(result)
    if documents:
        print len(documents)
        try:
            db.documents.insert(documents, continue_on_error=True)
        except pymongo.errors.DuplicateKeyError:
            pass

# process one element parallel
def process_element(elem):
    document = dict()
    if len(elem) == 9:
        try:
            # construct the document
            # rawText = elem[4].decode('latin-1').encode('utf-8')#.encode('latin-1').encode('string_escape').replace('\r', '').replace('\n', '')
            document['rawText'] = elem[4].encode('latin-1')#.encode('string_escape').replace('\r', '').replace('\n', '')
            document['series'] = elem[0]
            document['booktitle'] = elem[1]
            document['year'] = elem[2]
            document['title'] = elem[3].encode('latin-1')
            #authors
            authors = elem[5].split(',')
            #document['authors'] = [ {'name': author.strip(' ').decode('latin-1').encode('utf-8'), 'position': authors.index(author)} for author in authors]
            document['authors'] = [ {'name': author.strip(' ').encode('latin-1'), 'position': authors.index(author)} for author in authors]
            document['pdf1page'] = elem[6]
            document['pdfarticle'] = elem[7]
            document['_id'] = elem[8]

            try:
                lang = detect(elem[4].decode('latin-1')).upper()
            except Exception as e1:
                try:
                    lang = detect(elem[3].decode('latin-1')).upper()
                    print e1, 'aici try 2'
                except Exception as e2:
                    lang = 'FR'
                    print e2, 'aici try 3'
            document['language'] = lang

            
            if len(elem[4])>0:
                try:
                    cleanText = ct.cleanTextSimple(elem[4].encode('latin-1'), lang)
                    # if clean text exists
                    # print cleanText
                    if len(ct.removePunctuation(cleanText)) > 0:
                        # extract lemmas and part of speech
                        lemmas = LemmatizeText(rawText=ct.removePunctuation(cleanText), language=lang)
                        lemmas.createLemmaText()
                        lemmaText = lemmas.cleanText
                        if lemmaText and lemmaText != " ":
                            lemmas.createLemmas()
                            words = []
                            for w in lemmas.wordList:
                                word = dict()
                                word['word'] = w.word
                                word['tf'] = w.tf
                                word['count'] = w.count
                                word['pos'] = w.wtype
                                words.append(word)

                            document['cleanText'] = cleanText#.encode('latin-1').encode('string_escape').replace('\r', '').replace('\n', '')
                            document['lemmaText'] = lemmaText
                            document['words'] = words
                except Exception as e:
                    print e, 'sunt in lemmaText'
        except Exception as e:
            print e, 'aici try 1', elem
    else:
        print 'aici in else', elem
    return document

if __name__ == "__main__":
    dbname = 'EGCDB'
    filename = 'RNTI_articles_export.csv'
    header = False
    csv_delimiter = '\t'
    corpus = utils.readCSV(filename)
    # createDB = CreateDB_EGC(dbname=dbname)
    # createDB.insert_data(corpus=corpus)
    print len(corpus)
    insert_data(dbname, corpus)
