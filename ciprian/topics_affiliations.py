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

mypath = 'pdfs/txt'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

dbname = 'EGCDB'
client = pymongo.MongoClient()
db = client[dbname]

def extract_affiliation(text):
	for elem in "\)\(><\{\}*|\r\n":
		text = text.replace(elem, '')
	unidecode(text.decode('utf8'))
	
	text = text.replace(',', ' ')
	text = text.split(' ')
	list_affiliations = []
	for elem in text:
		if elem and '@' in elem and '.' in elem[elem.index('@'):]:# and len(elem[elem.index('@'):]) > 3:
			if elem[elem.index('@'):] not in list_affiliations:
				list_affiliations.append(elem[elem.index('@'):])
	return list_affiliations

affiliation_articles = {}
idx = 0
for f in onlyfiles:
	d_id = int(f[:-4])
	isEGCFR = db.documents.find_one({'_id': d_id, 'booktitle': 'EGC', 'language': 'FR'})
	if isEGCFR:
		with codecs.open(mypath + '/' + f) as open_file:
			l_emails = []
			for line in open_file:
				if '@' in line:
					for affiliation in extract_affiliation(line):
						if affiliation_articles.get(affiliation, -1) == -1:
							affiliation_articles[affiliation] = [d_id]
						else:
							affiliation_articles[affiliation] = list(set(affiliation_articles[affiliation] + [d_id]))


for affiliation in affiliation_articles:
	no_articles = len(affiliation_articles[affiliation])
	print affiliation, 'topics for:', len(affiliation_articles[affiliation]), 'articles:'
	lda = LDA(dbname=dbname, host='localhost', port=27017, language='FR')
	query = {'_id': {'$in': affiliation_articles[affiliation]}}
	for topic in lda.apply(query=query, num_topics=no_articles, num_words=10, iterations=1500)[0]:
		t = ""
		idx = 0
		for elem in topic:
			t += elem[1] + " "
		print idx, t
		idx += 1

# for affiliation in affiliation_articles:
# 	print affiliation, affiliation_articles[affiliation]

