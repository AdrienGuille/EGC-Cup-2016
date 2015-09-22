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

reload(sys)  
sys.setdefaultencoding('utf8')

mypath = 'pdfs/txt'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

dbname = 'EGCDB'
client = pymongo.MongoClient()
db = client[dbname]

mails_authors = {}

diacritics = {
	u"à": "a",
	u"â": "a",
	u"æ": "ae",
	u"ç": "c",
	u"è": "e",
	u"é": "e",
	u"ê": "e",
	u"ë": "e",
	u"î": "i",
	u"ï": "i",
	u"ô": "o",
	u"œ": "oe",
	u"ù": "u",
	u"û": "u",
	u"ü": "u"
}

def replace_diacritics(text):
	text = text.encode('utf-8')
	# try:
	# 	text = text.decode('utf-8').encode('ascii', 'ignore')
		
	# except:
	# 	text = text.decode('ISO-8859-1').encode('ascii', 'ignore')
	
	for elem in diacritics:
		text.replace(elem, diacritics[elem])
	
	return text

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

for f in onlyfiles:
	d_id = int(f[:-4])
	with codecs.open(mypath + '/' + f) as open_file:
		authors = db.documents.find_one({'_id': d_id}, {'_id': 0, 'authors': 1})
		l_authors = []
		for author in authors['authors']:
			l_authors.append(author['name'].lower())
		l_emails = []
		for line in open_file:
			if '@' in line:
				if '{' in line:
					new_line = line
					new_line.replace('}', ' ')
					new_line.replace('{', ' ')
					new_line.replace('|', ' ')
					new_line.replace(',', ' ')
					new_line = unidecode(new_line.decode('utf8'))
					new_line.split(' ')
					# print new_line
				emails = line.split(' ')
				for email in emails:
					if '@' in email:
						l_emails.append(email.strip().replace('\n', '').lower())
		mails_authors[d_id] = {'authors': l_authors, 'emails': l_emails}

print mails_authors

#extract the authors emails
with codecs.open('emails_authors.csv', 'w', encoding='utf-8') as f_out:
	for elem in mails_authors:
		for author in mails_authors[elem]['authors']:
			u_author = unidecode(author)
			lastname = u_author.split(' ')[-1].split('-')[-1]
			for email in mails_authors[elem]['emails']:
				if lastname in email[:email.index('@')] or 'nom.nom' in email[:email.index('@')]:
					out_str = str(elem) + ';'
					out_str += author + ';'
					# out_str += unidecode(email[email.index('@'):].replace(')', '').replace('>', '').replace('\n', '').replace(',','').replace('}','').replace('{','').replace('*', '').decode('utf8')) + '\n'
					if 'nom.nom' in email[:email.index('@')]:
						author = replace_diacritics(author)
						email = '.'.join(author.split(' ')) + email[email.index('@'):]
					# print email
					#email = replace_specialchars(email)
					# print email, author
					try:
						out_str += unidecode(email.replace(')', '').replace('(', '').replace('>', '').replace('<', '').replace(',','').replace('}','').replace('{','').replace('*', '').replace('\n', '').decode('utf8')) + '\n'
					except:						
						print 'mumu', email, repalce_diacritics(email), author
					f_out.write(out_str)
	f_out.close()

aa = {}

#extract for paper university emails
with codecs.open('id_univs.csv', 'w', encoding='utf-8') as f_out:
	for elem in mails_authors:
		out_str = str(elem) + ';'
		emails_set = set()
		for email in mails_authors[elem]['emails']:
			n_m = unidecode(email[email.index('@'):].replace(')', '').replace('>', '').replace('\n', '').replace(',','').replace('}','').replace('{','').replace('*', '').decode('utf8'))
			if '.' in n_m:
				if aa.get(n_m, -1) == -1:
					aa[n_m] = [elem]
				else:
					aa[n_m] += [elem]
				emails_set.add(n_m)
		if emails_set:
			out_str += ' , '.join(emails_set) + '\n'
		f_out.write(out_str)
	f_out.close()

graph = {}

for elem1 in aa:
	for articles1 in aa[elem1]:
		for elem2 in aa:
			if elem1 != elem2 and articles1 in aa[elem2]:
				if graph.get((elem1, elem2), -1) == -1 and graph.get((elem2, elem1), -1) == -1:
					graph[(elem1, elem2)] = [articles1]
				else:
					if graph.get((elem1, elem2), -1) != -1:
						if articles1 not in graph[(elem1, elem2)]:
							graph[(elem1, elem2)] += [articles1]
					elif graph.get((elem2, elem1), -1) != -1:
						if articles1 not in graph[(elem2, elem1)]:
							graph[(elem2, elem1)] += [articles1]
			# else:
			# 	graph[(elem1, elem2)] = aa[elem1]



for elem in graph:
	print elem[0], elem[1], len(graph[elem]), graph[elem]

