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
types ={
	1: { 'booktitle': 'EGC', 'lemmaText': {'$exists': 'true'}, 'language': 'FR'}, 
	2: { 'booktitle': 'EGC', 'lemmaText': {'$exists': 'true'}, 'language': 'EN'}, 
	3: { 'lemmaText': {'$exists': 'true'}, 'language': 'FR'}, 
	4: { 'lemmaText': {'$exists': 'true'}, 'language': 'EN'}

}

def number_topics(n):
	if n == 1:
		return 1
	elif n>1 and n<19:
		return int(round(n/2.0))
	else:
		return 10

def create_topics(choise):
	articles_by_author = {}
	article_authors = db.documents.find(types[choise], {'_id': 1, 'authors': 1})
	for article in article_authors:
		for author in article['authors']:
			if articles_by_author.get(author['name'], -1) == -1:
				articles_by_author[author['name']] = [article['_id']]
			else:
				articles_by_author[author['name']] += [article['_id']]

	for author in articles_by_author:
		no_articles = len(articles_by_author[author])
		lda = LDA(dbname=dbname, host='localhost', port=27017, language='FR')
		query = {'_id': {'$in': articles_by_author[author]}}
		idx = 0
		no_topics = number_topics(no_articles)
		print author, 'topics for:', len(articles_by_author[author]), 'articles, no topics', no_topics
		for topic in lda.apply(query=query, num_topics=no_topics, num_words=10, iterations=1500)[0]:
			t = ""
			for elem in topic:
				t += elem[1] + " "
			print idx, t
			idx += 1

if __name__ == "__main__":
	choise = int(sys.argv[1]) # 1 EGC corpus FR, 2 EGC corpus EN, 3 all corpus FR, 4 all corpus EN
	create_topics(choise)



