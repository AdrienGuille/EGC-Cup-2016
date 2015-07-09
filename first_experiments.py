# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from gensim import corpora, models
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import defaultdict
from langdetect import detect
import networkx as nx
import codecs


def load_corpus(file_path, year_a=2004, year_b=2014, enforce_language=None):
    input_file = codecs.open(file_path, 'r', encoding='latin-1')
    count = 0
    article_list = []
    for line in input_file:
        article = line.split('\t')
        if len(article) == 8 and article[1] == 'EGC' and int(article[2]) in range(year_a, year_b):
            count += 1
            authors = article[5].split(',')
            language = detect(article[3])
            if enforce_language is None or language == enforce_language:
                for i in range(0, len(authors)):
                    authors[i] = authors[i].strip()
                article_list.append({'title': article[3], 'year': article[2], 'authors': authors, 'abstract': article[4], 'language': language})
    print count, 'articles (', enforce_language, ')'
    return article_list

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

def create_collaboration_graph(corpus):
    graph = nx.Graph()
    graph.add_nodes_from(author_set(corpus))
    for article in corpus:
        authors = article.get('authors')
        for i in range(0, len(authors)):
            for j in range(i+1, len(authors)):
                graph.add_edge(authors[i], authors[j])
    print graph.number_of_edges(), 'distinct collaborations'
    return graph

def export_collaboration_graph(graph, file_path='output/collaboration_graph.gml'):
    nx.write_gml(graph, file_path)

def analyze_collaboration_graph(graph):
    if nx.is_connected(graph):
        print 'diameter', nx.diameter(graph)
    else:
        print 'disconnected graph'
    k_core = nx.core_number(graph)
    print 'k-core decomposition: ', sorted(k_core.items(), key=lambda x: x[1], reverse=True)


def train_lda(abstracts, num_topics=10, stemming=False):
    stop_word_list = stopwords.words('french')
    stop_word_list.extend(stopwords.words('english'))
    stop_word_list.extend([',', '.', '\'', '"', '(', ')', '-', ').'])
    snowball_stemmer = SnowballStemmer('french')
    if stemming:
        formatted_abstracts = [[snowball_stemmer.stem(word) for word in wordpunct_tokenize(abstract.lower()) if word not in stop_word_list] for abstract in abstracts]
    else:
        formatted_abstracts = [[word for word in wordpunct_tokenize(abstract.lower()) if word not in stop_word_list] for abstract in abstracts]
    frequency = defaultdict(int)
    for formatted_abstract in formatted_abstracts:
        for word in formatted_abstract:
            frequency[word] += 1
    formatted_abstracts = [[word for word in formatted_abstract if frequency[word] > 1] for formatted_abstract in formatted_abstracts]
    dictionary = corpora.Dictionary(formatted_abstracts)
    formatted_corpus = [dictionary.doc2bow(formatted_abstract) for formatted_abstract in formatted_abstracts]
    tfidf = models.TfidfModel(formatted_corpus)
    corpus_tfidf = tfidf[formatted_corpus]
    lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, iterations=10000, num_topics=num_topics)
    return lda.show_topics(num_topics=num_topics, num_words=10, formatted=False)

def print_topics(topics):
    count = 0
    for topic in topics:
        word_list = []
        for weighted_word in topic:
            word_list.append(weighted_word[1])
        print 'topic', count, ': ', ' '.join(word_list)
        count += 1

french_article_corpus = load_corpus('input/RNTI_articles_export.txt', 2004, 2015, 'fr')
english_article_corpus = load_corpus('input/RNTI_articles_export.txt', 2004, 2015, 'en')
complete_article_corpus = load_corpus('input/RNTI_articles_export.txt', 2004, 2015)
print len(author_set(french_article_corpus)), 'distinct authors'
collaboration_graph = create_collaboration_graph(complete_article_corpus)
# export_collaboration_graph(collaboration_graph)
analyze_collaboration_graph(collaboration_graph)
print 'degree(Adrien Guille): ', collaboration_graph.degree('Adrien Guille')
latent_topics = train_lda(abstract_list(french_article_corpus), 20)
print_topics(latent_topics)