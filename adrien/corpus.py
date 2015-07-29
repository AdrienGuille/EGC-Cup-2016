# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import networkx as nx
import codecs
import pickle
import os


def load():
        input_file = codecs.open('input/RNTI_articles_export_fixed1347_ids.txt', 'r', encoding='utf-8')
        article_dictionary = {}
        for line in input_file:
            line = line.replace('\n', '')
            article = line.split('\t')
            if len(article) == 11 and article[1] == 'EGC':
                article_id = article[8]
                year = article[2]
                title = article[3]
                abstract = article[4]
                authors = article[5].split(',')
                for i in range(0, len(authors)):
                    authors[i] = authors[i].strip()
                title_lang = article[9]
                abstract_lang = article[10].replace('\n','')
                article_path = 'input/pdfs/1page/'+article_id+'.txt'
                if os.path.isfile(article_path):
                    article_input_file = codecs.open(article_path, 'r', encoding='utf-8')
                    first_page = article_input_file.read()
                else:
                    first_page = ''
                article_dictionary[article_id] = {'year': int(year), 'title': title, 'abstract': abstract,
                                                  'authors': authors,'title_lang': title_lang,
                                                  'abstract_lang': abstract_lang,
                                                  'first_page': first_page}
        return article_dictionary


class Corpus:

    def __init__(self, update_data=False, title_lang=None, abstract_lang=None, year_a=None, year_b=None):
        if update_data:
            self.articles = load()
            pickle.dump(self.articles, open('output/corpus.pickle', 'wb'))
        else:
            self.articles = pickle.load(open('output/corpus.pickle', 'rb'))
        ids = []
        for article_id, article in self.articles.iteritems():
            test_title_lang = title_lang is None or title_lang == article.get('title_lang')
            test_abstract_lang = abstract_lang is None or abstract_lang == article.get('abstract_lang')
            test_year = (year_a is None) or (year_b is not None and article.get('year') in range(year_a, year_b))
            if not (test_title_lang and test_abstract_lang and test_year):
                ids.append(article_id)
        for article_id in ids:
            del self.articles[article_id]

    def title_list(self):
        titles = []
        for article in self.articles.values():
            titles.append(article.get('title'))
        return titles

    def abstract_list(self):
        abstracts = []
        for article in self.articles.values():
            abstracts.append(article.get('title'))
        return abstracts

    def author_set(self):
        authors = set()
        for article in self.articles.values():
            for author in article.get('authors'):
                authors.add(author)
        return authors

    def pretty_print(self):
        print len(self.articles), 'articles'
        print len(self.author_set()), 'authors'

    def collaboration_graph(self, name=''):
        graph = nx.Graph(name=name)
        graph.add_nodes_from(self.author_set())
        for article in self.articles.values():
            authors = article.get('authors')
            for i in range(0, len(authors)):
                for j in range(i+1, len(authors)):
                    graph.add_edge(authors[i], authors[j])
        return graph
