# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from langdetect import detect
import networkx as nx
import codecs
import pickle


def load(file_path, year_a=2004, year_b=2014, enforce_language=None):
    input_file = codecs.open(file_path, 'r', encoding='latin-1')
    count = 0
    article_list = []
    for line in input_file:
        article = line.split('\t')
        if len(article) == 8 and article[1] == 'EGC' and int(article[2]) in range(year_a, year_b):
            authors = article[5].split(',')
            language = detect(article[3])
            if enforce_language is None or language == enforce_language:
                count += 1
                for i in range(0, len(authors)):
                    authors[i] = authors[i].strip()
                article_list.append({'title': article[3], 'year': article[2], 'authors': authors, 'abstract': article[4], 'language': language})
    print count, 'articles (', enforce_language, ')'
    return article_list

def serialize(corpus, file_path):
    pickle.dump(corpus, open(file_path, 'wb'))

def deserialize(file_path):
    return pickle.load(open(file_path, 'rb'))

def abstract_list(corpus):
    abstracts = []
    for article in corpus:
        abstracts.append(article.get('abstract'))
    return abstracts

def author_set(corpus):
    authors = set()
    for article in corpus:
        for author in article.get('authors'):
            authors.add(author)
    print len(authors), 'distinct authors'
    return authors

def collaboration_graph(corpus, name=''):
    graph = nx.Graph(name=name)
    graph.add_nodes_from(author_set(corpus))
    for article in corpus:
        authors = article.get('authors')
        for i in range(0, len(authors)):
            for j in range(i+1, len(authors)):
                graph.add_edge(authors[i], authors[j])
    print graph.number_of_edges(), 'distinct collaborations'
    return graph