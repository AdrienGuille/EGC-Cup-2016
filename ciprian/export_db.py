# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"


import pymongo
import codecs


dbname = 'EGCDB'
client = pymongo.MongoClient()
db = client[dbname]

cursor=db.documents.find({'booktitle': 'EGC', 'lemmaText': {'$exists': 'true'}})
#series;booktitle;year;title;abstract;authors;pdf1page;pdfarticle;id;lang\n
with codecs.open('EGC_articles.csv', 'w', encoding='utf-8') as file_out:
	file_out.write('series;booktitle;year;title;abstract;authors;pdf1page;pdfarticle;id;lang\n')
	for elem in cursor:
		str_print = elem['series'] + ';'
		str_print += elem['booktitle'] + ';'
		str_print += elem['year'] + ';'
		str_print += elem['title'].replace('\"', ' ').replace(';', ' ') + ';'
		str_print += elem['rawText'].replace('\"', ' ').replace(';', ' ') + ';'
		x = [0]*len(elem['authors'])
		for author in elem['authors']:
			x[author['position']] = author['name']
		str_print += ','.join(x) +';'
		str_print += elem['pdf1page'] + ';'
		str_print += elem['pdfarticle'].replace('\n', '') + ';'
		str_print += str(elem['_id']) +';'
		str_print += elem['language'] +'\n'
		file_out.write(str_print)
	file_out.close()