# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from gensim import corpora, models
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
from collections import defaultdict
import networkx as nx


def load_corpus(file_path):
    input_file = open(file_path, 'r')
    count = 0
    article_list = []
    for line in input_file:
        article = line.split('\t')
        if len(article) == 8 and article[1] == 'EGC':
            count += 1
            authors = article[5].split(',')
            for i in range(0,len(authors)):
                authors[i] = authors[i].strip()
            article_list.append({'title': article[3], 'year': article[2], 'authors': authors, 'abstract': article[4]})
    print count, 'articles'
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

def export_collaboration_graph(graph):
    graph.write_gml(graph, 'collaboration.gml')

def analyze_collaboration_graph(graph):
    if nx.is_connected(graph):
        print 'diameter', nx.diameter(graph)
    else:
        print 'disconnected graph'
    k_core = nx.core_number(graph)
    print 'k-core decomposition: ', sorted(k_core.items(), key=lambda x: x[1], reverse=True)


def train_lda(abstracts, num_topics):
    stopword_list = stopwords.words('french')
    formatted_abstracts = [[word for word in wordpunct_tokenize(abstract.lower()) if word not in stopword_list] for abstract in abstracts]
    frequency = defaultdict(int)
    for formatted_abstract in formatted_abstracts:
        for word in formatted_abstract:
            frequency[word] += 1
    formatted_abstracts = [[word for word in formatted_abstract if frequency[word] > 1] for formatted_abstract in formatted_abstracts]
    dictionary = corpora.Dictionary(formatted_abstracts)
    formatted_corpus = [dictionary.doc2bow(formatted_abstract) for formatted_abstract in formatted_abstracts]
    tfidf = models.TfidfModel(formatted_corpus)
    corpus_tfidf = tfidf[formatted_corpus]
    lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, iterations=3000, num_topics=num_topics)
    return lda.show_topics(num_topics=num_topics, num_words=10, formatted=False)

def print_topics(topics):
    count = 0
    for topic in topics:
        word_list = []
        for weighted_word in topic:
            word_list.append(weighted_word[1])
        print('topic',count,': ',' '.join(word_list))
        count += 1

article_corpus = load_corpus('RNTI_articles_export_utf-8.txt')
collaboration_graph = create_collaboration_graph(article_corpus)
# export_collaboration_graph(collaboration_graph)
analyze_collaboration_graph(collaboration_graph)
print 'degree(Adrien Guille): ', collaboration_graph.degree('Adrien Guille')
# latent_topics = train_lda(abstract_list(article_corpus), 20)
# print_topics(latent_topics)
