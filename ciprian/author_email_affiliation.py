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
	for elem in diacritics:
		text.replace(elem, diacritics[elem])
	return text

def extract_affiliation(text):
	ok = True
	if ("(" in text and ")" in text):
		if ',' in text[text.index("("):text.index(")")]:
			text = text[text.index("("):]
			ok = False
	if ("{" in text and "}" in text):
		text = text[text.index("{"):]
		ok = False
	if ("(" in text and ">" in text):
		text = text[text.index("<"):]
		ok = False

	last_at = text.rfind('@')
	last_space = text.rfind(' ')
	while last_space > last_at:
		text = text[:last_space]
		last_at = text.rfind('@')
		last_space = text.rfind(' ')

	
	are_points = text.rfind('.')
	if are_points < last_at:
		text = ""
	


	
	if ok:
		new_text = text.split(' ')
		emails = ""
		for elem in new_text:
			if '@' in elem:
				emails += elem + ' '
		text = emails
	

	text = text.lower()
	orig_text = text.lower()

	for elem in "\)\(><\{\}*;|\r\n":
		text = text.replace(elem, '')
	text = text.replace("ﬂ", "fl")
	text = text.replace("ﬁ", "fi")
	unidecode(text.decode('utf8'))
	text = replace_diacritics(text)
	text = text.replace(',', ' ')
	text = text.split(' ')
	text = filter(bool, text)
	if len(text) > 1:
		if ("(" in orig_text and ')' in orig_text) or ("{" in orig_text and '}' in orig_text) or ("<" in orig_text and '>' in orig_text):
			mail = text[len(text)-1]
			mail = mail[mail.index('@'):]
			for idx in range(0, len(text)-1):
				text[idx] = text[idx] + mail
		for idx in range(0, len(text)):
			if 'nom' in text[idx] or 'name' in text[idx]:
				text[idx] = 'firstname.lastname' + text[idx][text[idx].index('@'):]
	elif text:
		if 'nom' in text[0] or 'name' in text[0]:
			text[0] = 'firstname.lastname' + text[0][text[0].index('@'):]


	return text

	"""
	list_affiliations = []
	for elem in text:
		if elem and '@' in elem and '.' in elem[elem.index('@'):]:# and len(elem[elem.index('@'):]) > 3:
			if elem[elem.index('@'):] not in list_affiliations:
				list_affiliations.append(elem[elem.index('@'):])
	return list_affiliations
	"""
	

for f in onlyfiles:
	d_id = int(f[:-4])
	with codecs.open(mypath + '/' + f) as open_file:
		authors = db.documents.find_one({'_id': d_id}, {'_id': 0, 'authors': 1})
		l_authors = []
		for author in authors['authors']:
			l_authors.append(author['name'].lower())
		l_emails = []
		for line in open_file:
			if 'abstract' in line.lower() or 'resum' in line.lower():
				break 
			if '@' in line:
				mails_authors[d_id] = {'authors': l_authors, 'emails': extract_affiliation(line)}


author_email = {}

for elem in mails_authors:
	for author in mails_authors[elem]['authors']:
		for email in mails_authors[elem]['emails']:
			new_author = author.replace(" ", ".")
			if "firstname.lastname" in email:
				new_author = replace_diacritics(author.replace(" ", "."))
				if author_email.get(author, -1) == -1:
					author_email[author] = [new_author + email[email.index("@"):]]
				else:
					author_email[author] = list(set(author_email[author] + [new_author + email[email.index("@"):]]))

			else:
				firstname = replace_diacritics(author[:author.rfind(" ")-1])
				lastname = replace_diacritics(author[author.rfind(" ")+1:])
				
				if lastname in email:# or firstname in email:
					if author_email.get(author, -1) == -1:
						author_email[author] = [replace_diacritics(email)]
					else:
						author_email[author] = list(set(author_email[author] + [replace_diacritics(email)]))



#extract emails for authors
for author in author_email:
	emails = ""
	affiliations = ""
	for email in author_email[author]:
		emails += email + ", "
		try:
			affiliations += email[email.index("@"):] + ", "
		except:
			pass
	print author, "; [" , emails[:-2], "] ; [", affiliations[:-2], "]"

