# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"


import pymongo
import codecs
import urllib


dbname = 'EGCDB'
client = pymongo.MongoClient()
db = client[dbname]

cursor = db.documents.find({'booktitle': 'EGC', 'lemmaText': {'$exists': 'true'}})


for elem in cursor:
	urllib.urlretrieve(elem['pdf1page'], 'pdfs/'+str(elem['_id'])+'.pdf')


