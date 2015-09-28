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
from unidecode import unidecode
import subprocess
import time


reload(sys)  
sys.setdefaultencoding('utf8')

mypath = 'pdfs/txt'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

def extract_affiliation(text):
	text = text.replace("ﬂ", "fl")
	text = text.replace("ﬁ", "fi")
	for elem in "\)\(><\{\}*|\r\n":
		text = text.replace(elem, '')
	unidecode(text.decode('utf8'))
	
	text = text.replace(',', ' ')
	text = text.replace(';', ' ')
	text = text.split(' ')
	list_affiliations = []
	for elem in text:
		if elem and '@' in elem and '.' in elem[elem.index('@'):]:# and len(elem[elem.index('@'):]) > 3:
			if elem[elem.index('@'):] not in list_affiliations:
				email = elem[elem.index('@'):]
				if email[-1] == '.':
					email = email[:-1]
				list_affiliations.append(email)
	return list_affiliations

def check_organization(text):
	text = text.lower()
	# print text
	ok = False
	keywords = ['ecol', 'centre', 'yliopisto', 'ctre', 'info', 'comp', 'univ', 'inst', 'lab', 'ass']
	for kw in keywords:
		if kw in text:
			ok = True	
			break
	# if ('ecol' in text) or ('centre' in text) or ('yliopisto' in text) or ('ctre' in text) or ('info' in text) or ('comp' in text)or ('univ' in text) or ('inst' in text) or ('lab' in text) or ('ass' in text):
	# 	ok = True
	return ok

def get_affiliations():
	
	keywords = ['contact', 'addre', 'name', 'desc', 'owner', 'registrant']

	affiliations = []
	for f in onlyfiles:
		with codecs.open(mypath + '/' + f) as open_file:
			for line in open_file:
				if '@' in line:
					for affiliation in extract_affiliation(line):
						if affiliation not in affiliations:
							affiliations.append(affiliation)

	idx = 0
	for affiliation in affiliations:

		
		if affiliation.count('.') >= 2:
			aff = affiliation[affiliation.index('.')+1:]
		else:
			aff = affiliation[1:]


		comm = ['whois', aff]
		proc = subprocess.Popen(comm, stdout=subprocess.PIPE)
		tmp = proc.stdout.read()
		lines = tmp.split('\n')

		organization = ""
		ok_org = True
		address = ""
		country = ""
		ok_country = True

		for line in lines:
			# organization
			line = line.strip()
			if line.startswith('contact') and ok_org:
				temp = line[line.index(':')+1:].strip()
				if check_organization(temp):
					organization += temp
					ok_org = False
			if line.startswith('addre') and ok_org:
				temp = line[line.index(':')+1:].strip()
				if check_organization(temp):
					organization += temp
					ok_org = False
			if line.startswith('name:') and ok_org:
				print line, aff
				temp = line[line.index(':')+1:].strip()
				if check_organization(temp):
					organization += temp
					ok_org = False
			if line.startswith('desc') and ok_org:
				temp = line[line.index(':')+1:].strip()
				if check_organization(temp):
					organization += temp
					ok_org = False
			if line.startswith('owner') and ok_org:
				temp = line[line.index(':')+1:].strip()
				if check_organization(temp):
					organization += temp
					ok_org = False
			if line.startswith('registrant') and ok_org:
				temp = line[line.index(':')+1:].strip()
				if check_organization(temp):
					organization += temp
					ok_org = False
			if line.startswith('Organisme') and ok_org:
				temp = line.replace('.', '')
				temp = temp[temp.index('#')+1:] + " "
				if check_organization(temp):
					organization += temp
					ok_org = False
			if line.startswith('g. [Organization]') and ok_org:
				temp = line[line.index(']')+1:].strip()
				if check_organization(temp):
					organization += temp
					ok_org = False
			if line.startswith('Univ') and ok_org:
				temp = line
				if check_organization(temp):
					organization += temp
					ok_org = False

			# country code
			if line.startswith('country') and ok_country:
				country = line[line.index(':')+1:].lstrip()
				ok_country = False
		if ok_country:
			country = aff.split('.')[-1].upper()
		print (affiliation, aff, organization, country)
		# idx += 1
		# if idx == 10:
		# 	break
		# except:
		# 	print "affiliation with problems", affiliation[1:]
		time.sleep(5)

if __name__ == "__main__":
	get_affiliations()
