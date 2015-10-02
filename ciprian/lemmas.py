# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"


# extracting lemmas


import sys
from os import listdir
from os.path import isfile, join
import codecs
import pymongo
from unidecode import unidecode
import subprocess
import time
from nlplib.lemmatize_text import LemmatizeText

reload(sys)  
sys.setdefaultencoding('utf8')

dbname = 'EGCDB'
client = pymongo.MongoClient()
db = client[dbname]

pos_mapping = {
	"VIMP": "v", 
	"VINF": "v", 
	"VPP": "v", 
	"VPR": "v", 
	"VS": "v",
	"DETWH": "det",
	"ADVWH": "adv",
	"NPP": "np"
}

def extractPOS(filename):
	comm = ['./pos.sh', filename]
	proc = subprocess.Popen(comm, stdout=subprocess.PIPE)
	tmp = proc.stdout.read()
	return tmp

def writeFile(filename, text):
	with open(filename, 'w') as m_file:
		m_file.write(text)
        m_file.close()

def readCSV(filename, encoding='utf8', header=True):
    corpus = []
    with codecs.open(filename, 'r', encoding=encoding) as csvfile:
        for line in csvfile:
            corpus.append(line.replace('\n', '').split('\t'))
    if header:
    	return corpus[0], corpus[1:]
    else:
    	return corpus

def readLefff(filename, encoding='utf8'):
    corpus = []
    with codecs.open(filename, 'r', encoding=encoding) as csvfile:
        for line in csvfile:
            corpus.append(line.replace('\n', '').split('\t'))
            if 'adv' in line[1].lower():
            	line[1] = 'adv'
            if 'adj' in line[1].lower():
            	line[1] = 'adj'
    return corpus

# documents = db.documents.find({'booktitle': 'EGC'}, {'_id': 1, 'rawText': 1, 'title': 1, 'year': 1, 'booktitle': 1, 'language': 1})

# for document in documents:
# 	filename = 'texts/'+str(document["_id"])
# 	text = document["title"] + "." + document["rawText"]
# 	writeFile(filename, text)
# 	pos = extractPOS(filename)
# 	if pos:
# 		print document["_id"], document["year"], document["booktitle"], pos

lefff = readCSV('lefff-3.4.mlex', header=False)


def splitPos(text):
	text = text.split(' ')
	lemmas = ""
	for elem in text:
		word = elem.split('/')[0]
		pos = elem.split('/')[1]
		if pos_mapping.get(pos, -1) != -1:
			pos = pos_mapping[pos]
		ok = True
		if pos != 'PONCT':
			for elem in lefff:
				if elem[0] == word.lower() and pos.lower() == elem[1]:
					lemmas += elem[2] + ' '
					ok = False
					break
		if ok:
			lemmas += word + ' '
	return lemmas

header, corpus = readCSV('RNTI_articles_export_fixed1347_ids.txt')

print header
idx = 0
for line in  corpus:
	# language title
	if line[9] == 'fr':
		filename = 'texts/'+str(line[8]) + 'title'
		writeFile(filename, line[3])
		pos_title = extractPOS(filename)
		lemma_title = splitPos(pos_title)
	elif line[9] == 'en':
		lt = LemmatizeText(line[3])
		lt.createLemmaText()
		lemma_title = lt.cleanText
	# language abstract
	if line[10] == 'fr':
		filename = 'texts/'+str(line[8]) + 'abstract'
		writeFile(filename, line[4])
		pos_abstract = extractPOS(filename)
		lemma_abstract = splitPos(pos_abstract)
	elif line[10] == 'en':
		lt = LemmatizeText(line[4])
		lt.createLemmaText()
		lemma_abstract = lt.cleanText
	if line[9] == 'fr' and line[10] == 'fr':
		line[12] = lemma_title + ' ' + lemma_abstract
	if line[9] == 'en' and line[10] == 'en':
		line[12] = lemma_title + ' ' + lemma_abstract
	if line[9] == 'en' and line[10] == 'fr':
		line[12] = lemma_abstract
	if line[9] == 'fr' and line[10] == 'en':
		line[12] = lemma_title
	line[13] = line[3]

	print line[0] + '\t' + line[1] + '\t' + line[2] + '\t' + line[3] + '\t' +line[4] + '\t' + line[5] + '\t' + line[6] + '\t' + line[7] + '\t' + line[8] + '\t' + line[9] + '\t' + line[10] + '\t' + line[11] + '\t' + line[12] + '\t' + line[13] + '\t' + line[14] + '\n'
	