# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"

import sys
from os import listdir
from os.path import isfile, join
import codecs
import pymongo
from unidecode import unidecode
from mllib.train_lda import LDA

reload(sys)  
sys.setdefaultencoding('utf8')

dbname = 'EGCDB'
client = pymongo.MongoClient()
db = client[dbname]


#Extract for each author the articles written and construct topics with LDA

article_authors = db.documents.find({'booktitle': 'EGC', 'lemmaText': {'$exists': 'true'}, 'language': 'FR'}, {'_id': 1, 'authors': 1})

articles_by_author = {}

for article in article_authors:
	for author in article['authors']:
		if articles_by_author.get(author['name'], -1) == -1:
			articles_by_author[author['name']] = [article['_id']]
		else:
			articles_by_author[author['name']] += [article['_id']]

for author in articles_by_author:
	no_articles = len(articles_by_author[author])
	print author, 'topics for:', len(articles_by_author[author]), 'articles:'
	lda = LDA(dbname=dbname, host='localhost', port=27017, language='FR')
	query = {'_id': {'$in': articles_by_author[author]}}
	for topic in lda.apply(query=query, num_topics=no_articles, num_words=10, iterations=1500)[0]:
		t = ""
		idx = 0
		for elem in topic:
			t += elem[1] + " "
		print idx, t
		idx += 1




