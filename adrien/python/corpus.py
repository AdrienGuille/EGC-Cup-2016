# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import networkx as nx
import codecs
import pickle
import os
import miscellaneous as misc
import re
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords


def load(limit=None, lexicon=None):
        input_file = codecs.open('../../input/RNTI_articles_export_fixed1347_ids.txt', 'r', encoding='utf-8')
        article_dictionary = {}
        count = 0
        stop_word_list = stopwords.words('french')
        stop_word_list.extend(stopwords.words('english'))
        stop_word_list.extend([u',', u'.', u'\'', u'"', u'(', u')', u'-', u').', u':'])
        for line in input_file:
            line = line.replace('\n', '')
            article = line.split('\t')
            if len(article) == 11 and article[1] == 'EGC':
                article_id = article[8]
                year = article[2]
                title = article[3].lower()
                title = title.replace(u'non supervisé', u'nonsupervisé')
                title = title.replace(u'non-supervisé', u'nonsupervisé')
                title = title.replace(u'partir', u'')
                abstract = article[4].lower()
                authors = article[5].split(',')
                article_path = '../../input/pdfs/1page/'+article_id+'.txt'
                if os.path.isfile(article_path):
                    article_input_file = codecs.open(article_path, 'r', encoding='utf-8')
                    first_page = article_input_file.read()
                else:
                    first_page = ''
                for i in range(0, len(authors)):
                    authors[i] = authors[i].strip()
                authors_affiliations = extract_authors_affiliations(authors, first_page)
                title_lang = article[9]
                abstract_lang = article[10].replace('\n', '')
                lemmatized_title = title
                lemmatized_abstract = abstract
                if lexicon:
                    specific_stop_words = [u'cadrer',u'approcher',u'méthode']
                    lemmatized_title = ''
                    for word in wordpunct_tokenize(title.lower()):
                        if word not in stop_word_list:
                            lemmatized_word = lexicon.get_lem(word)
                            if lemmatized_word is None or lemmatized_word == '=':
                                lemmatized_word = word
                            if lemmatized_word not in specific_stop_words:
                                lemmatized_title += lemmatized_word+' '
                    lemmatized_title = lemmatized_title.replace(u'baser donnée', u'BDD')
                    lemmatized_abstract = ''
                    for word in wordpunct_tokenize(abstract.lower()):
                        if word not in stop_word_list:
                            lemmatized_word = lexicon.get_lem(word)
                            if lemmatized_word is None or lemmatized_word == '=':
                                lemmatized_word = word
                            if lemmatized_word not in specific_stop_words:
                                lemmatized_abstract += lemmatized_word+' '
                    lemmatized_abstract = lemmatized_abstract.replace(u'baser donnée', u'BDD')
                article_dictionary[article_id] = {'year': int(year),
                                                  'title': title,
                                                  'lemmatized_title': lemmatized_title,
                                                  'abstract': abstract,
                                                  'lemmatized_abstract': lemmatized_abstract,
                                                  'authors': authors,
                                                  'authors_affiliation': authors_affiliations,
                                                  'title_lang': title_lang,
                                                  'abstract_lang': abstract_lang,
                                                  'first_page': first_page}
                count += 1
                if limit is not None and count >= limit:
                    break
        return article_dictionary


def extract_authors_affiliations(author_list, text):
    text = unicode(text.replace(u'∗', u'*'))
    references = set()
    authors_affiliations = {}
    email_dictionary = {}
    trim_at = 0
    for author in author_list:
        result = extract_author_affiliation(author, text)
        if result is not None:
            trim_at = result[0]
            authors_affiliations[author] = result[1]
            references = references.union(result[1])
    if trim_at > 0:
        index_end = text.find(u'Résumé.')
        if index_end == -1:
            index_end = text.find(u'Abstract.')
        text0 = text[trim_at:index_end]
        references = list(references)
        for i in range(len(references)-1):
            index_start = text0.find(references[i])
            index_end = text0.find(references[i+1])
            if index_start > -1 and index_end > -1:
                text00 = text0[index_start:index_end]
                domain = re.findall("@[\w\-.]+", text00)
                if len(domain) > 0:
                    email_dictionary[references[i]] = domain[0]
        if len(references) > 0:
            index_start = text0.find(references[len(references)-1])
            if index_start > -1:
                text00 = text0[index_start:]
                domain = re.findall("@[\w\-.]+", text00)
                if len(domain) > 0:
                    email_dictionary[references[len(references)-1]] = domain[0]
        else:
            domain = re.findall("@[\w\-.]+", text0)
            if len(domain) > 0:
                email_dictionary[''] = domain[0]
        affiliation_list = []
        for i in range(len(author_list)):
            author = author_list[i]
            author_affiliation = []
            references = authors_affiliations.get(author)
            if references is not None:
                for reference in references:
                    affiliation = email_dictionary.get(reference)
                    author_affiliation.append(affiliation)
            affiliation_list.append(author_affiliation)
        return affiliation_list


def get_references_length(references):
    length = 0
    for i in range(len(references)):
        length += (i+1)
    return length


def extract_author_affiliation(author_name, text):
    index_start = text.find(author_name)
    if index_start > -1:
        author_in_text = text[index_start: index_start+len(author_name)+6]
        author_asterisk = author_in_text[len(author_name):]
        references = set(misc.references(author_asterisk))
        pos = index_start+len(author_name)+get_references_length(references)+len(references)-1
        return [pos, references]


class Corpus:

    def __init__(self, limit=None, update_data=False, lexicon=None, title_lang=None, abstract_lang=None, year_a=None, year_b=None):
        if update_data:
            self.articles = load(limit=limit, lexicon=lexicon)
            pickle.dump(self.articles, open('../../output/corpus.pickle', 'wb'))
        else:
            self.articles = pickle.load(open('../../output/corpus.pickle', 'rb'))
        ids = []
        for article_id, article in self.articles.iteritems():
            test_title_lang = title_lang is None or title_lang == article.get('title_lang')
            test_abstract_lang = abstract_lang is None or abstract_lang == article.get('abstract_lang')
            test_year = (year_a is None) or (year_b is not None and article.get('year') in range(year_a, year_b))
            if not (test_title_lang and test_abstract_lang and test_year):
                ids.append(article_id)
        for article_id in ids:
            del self.articles[article_id]

    def print_article(self, article_id, lemmatized_title_only=False):
        article = self.articles.get(article_id)
        if article is not None:
            if lemmatized_title_only:
                print article.get()

    def get_frequency_in_abstracts(self, word):
        frequency = 0
        count = 0
        for article in self.articles.values():
            count += 1
            if word in article.get('lemmatized_abstract'):
                frequency += 1
        return float(frequency)/float(count)

    def print_articles(self, article_ids):
        for article_id in article_ids:
            self.print_article(article_id)

    def title_list(self):
        titles = []
        for article in self.articles.values():
            titles.append(article.get('title'))
        return titles

    def lemmatized_title_list(self):
        titles = []
        for article in self.articles.values():
            titles.append(article.get('lemmatized_title'))
        return titles

    def articles_authored_by(self, author_name):
        article_ids = []
        for article_id, article in self.articles.iteritems():
            if author_name in article.get('authors'):
                article_ids.append(article_id)
        return article_ids

    def abstract_list(self):
        abstracts = []
        for article in self.articles.values():
            abstracts.append(article.get('abstract'))
        return abstracts

    def lemmatized_abstract_list(self):
        abstracts = []
        for article in self.articles.values():
            abstracts.append(article.get('lemmatized_abstract'))
        return abstracts

    def author_set(self):
        authors = set()
        for article in self.articles.values():
            for author in article.get('authors'):
                authors.add(unicode(author))
        return authors

    def earliest_paper(self):
        min_year = 3000
        for article in self.articles.values():
            year = int(article.get('year'))
            if year < min_year:
                min_year = year
        return min_year

    def latest_paper(self):
        max_year = 0
        for article in self.articles.values():
            year = int(article.get('year'))
            if year > max_year:
                max_year = year
        return max_year

    def pretty_print(self):
        print len(self.articles), 'articles published between', self.earliest_paper(), 'and', self.latest_paper()
        print len(self.author_set()), 'authors'

    def collaboration_graph(self, name=''):
        graph = nx.Graph(name=name)
        graph.add_nodes_from(self.author_set())
        for article in self.articles.values():
            authors = article.get('authors')
            for i in range(0, len(authors)):
                for j in range(i+1, len(authors)):
                    graph.add_edge(unicode(authors[i]), unicode(authors[j]))
        return graph
