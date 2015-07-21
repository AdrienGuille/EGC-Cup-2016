# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from langdetect import detect
import networkx as nx
import codecs
import pickle
import os

def load(file_path, year_a=2004, year_b=2014, enforce_language=None):
    input_file = codecs.open(file_path, 'r', encoding='utf-8')
    article_list = []
    for line in input_file:
        article = line.split('\t')
        if len(article) == 10 and 'EGC' in article[1] and int(article[2]) in range(year_a, year_b):
            authors = article[5].split(',')
            if len(article[4]) > 10:
                language = detect(article[4])
            else:
                language = detect(article[3])
            if enforce_language is None or language == enforce_language:
                for i in range(0, len(authors)):
                    authors[i] = authors[i].strip()
                article_list.append({'id': article[9].strip(), 'title': article[3], 'year': article[2], 'authors': authors, 'abstract': article[4], 'language': language})
    return article_list

def language_precision(corpus):
    total = 0.
    test_articles = 0.
    language_matches = 0.
    miss_matches = []
    for article in corpus:
        total += 1
        language = article.get('language')
        article_id = str(article.get('id'))
        file_path = 'input/pdfs/1page/'+article_id+'.txt'
        if os.path.isfile(file_path):
            test_articles += 1
            text_file = codecs.open(file_path, 'r', encoding='utf-8')
            first_page = text_file.read()
            french_keyword = 'Résumé.'
            english_keyword = 'Abstract.'
            if (french_keyword.decode('utf-8') in first_page and language == 'fr' and english_keyword not in first_page) or (english_keyword.decode('utf-8') in first_page and language == 'en' and french_keyword not in first_page):
                language_matches += 1
            else:
                miss_matches.append(article_id)
    return [test_articles, language_matches, total, miss_matches]

def serialize(corpus, file_path):
    pickle.dump(corpus, open(file_path, 'wb'))

def deserialize(file_path):
    return pickle.load(open(file_path, 'rb'))

def title_list(corpus):
    titles = []
    for article in corpus:
        titles.append(article.get('title'))
    return titles

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
    return authors

def pretty_print(corpus):
    print len(corpus), 'articles'
    print len(author_set(corpus)), 'authors'

def collaboration_graph(corpus, name=''):
    graph = nx.Graph(name=name)
    graph.add_nodes_from(author_set(corpus))
    for article in corpus:
        authors = article.get('authors')
        for i in range(0, len(authors)):
            for j in range(i+1, len(authors)):
                graph.add_edge(authors[i], authors[j])
    return graph
