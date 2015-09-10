# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from gensim import corpora, models
from nltk import wordpunct_tokenize
from nltk.stem import SnowballStemmer
from collections import defaultdict
import codecs
import json
import networkx as nx


def compute_vector_space(documents, stemming=False, remove_singleton=True):
    snowball_stemmer = SnowballStemmer('french')
    if stemming:
        formatted_documents = [[snowball_stemmer.stem(word) for word in wordpunct_tokenize(document.lower())] for document in documents]
    else:
        formatted_documents = [[word for word in wordpunct_tokenize(document.lower())] for document in documents]
    frequency = defaultdict(int)
    if remove_singleton:
        for formatted_document in formatted_documents:
            for word in formatted_document:
                frequency[word] += 1
        formatted_documents = [[word for word in formatted_document if frequency[word] > 1] for formatted_document in formatted_documents]
    dictionary = corpora.Dictionary(formatted_documents)
    formatted_corpus = [dictionary.doc2bow(formatted_document) for formatted_document in formatted_documents]
    tfidf = models.TfidfModel(formatted_corpus)
    corpus_tfidf = tfidf[formatted_corpus]
    return [corpus_tfidf, dictionary]


def perform_lsa(documents, num_topics=10, num_words=10, stemming=False, remove_singleton=True):
    vector_space_model = compute_vector_space(documents=documents, stemming=stemming, remove_singleton=remove_singleton)
    corpus_tfidf = vector_space_model[0]
    dictionary = vector_space_model[1]
    lsi = models.LsiModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_topics)
    return lsi.show_topics(num_topics=num_topics, num_words=num_words, formatted=False)


def train_lda(documents, num_topics=10, num_words=10, stemming=False, remove_singleton=True):
    vector_space_model = compute_vector_space(documents=documents, stemming=stemming, remove_singleton=remove_singleton)
    corpus_tfidf = vector_space_model[0]
    dictionary = vector_space_model[1]
    lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, iterations=30000, num_topics=num_topics)
    return lda.show_topics(num_topics=num_topics, num_words=num_words, formatted=False)


def print_topics(topics):
    count = 0
    for topic in topics:
        word_list = []
        for weighted_word in topic:
            word_list.append(weighted_word[1])
        print 'topic', count, ': ', ' '.join(word_list)
        count += 1


def construct_and_save_word_topic_graph(topics, file_path):
    nx_graph = nx.Graph(name='')
    json_graph = {}
    json_nodes = []
    nodes_array = []
    json_links = []
    for topic in topics:
        for weighted_word in topic:
            if weighted_word[1] not in nodes_array:
                nodes_array.append(weighted_word[1])
    nx_graph.add_nodes_from(nodes_array)
    for topic in topics:
        main_word = topic[0][1]
        main_word_id = nodes_array.index(main_word)
        for i in range(1, len(topic)):
            this_word_id = nodes_array.index(topic[i][1])
            json_links.append({'source': main_word_id, 'target': this_word_id})
            nx_graph.add_edge(unicode(main_word), unicode(topic[i][1]))
    nodes_array = []
    group = 0
    for topic in topics:
        for weighted_word in topic:
            if weighted_word[1] not in nodes_array:
                nodes_array.append(weighted_word[1])
                if word_is_unique(weighted_word[1], topics):
                    json_nodes.append({'name': weighted_word[1],
                                       'weight': nx_graph.degree(weighted_word[1]),
                                       'group': group})
                else:
                    json_nodes.append({'name': weighted_word[1],
                                       'weight': nx_graph.degree(weighted_word[1]),
                                       'group': -1})
        group += 1
    json_graph['nodes'] = json_nodes
    json_graph['links'] = json_links
    with codecs.open(file_path, 'w', encoding='utf-8') as fp:
        json.dump(json_graph, fp, indent=4, separators=(',', ': '))


def save_topics(topics, file_path):
    output = codecs.open(file_path, 'w', encoding='utf-8')
    for topic in topics:
        word_list = []
        for weighted_word in topic:
            word_list.append(weighted_word[1])
            word_list.append(str(weighted_word[0]))
        output.write(' '.join(word_list)+'\n')


def word_is_unique(word, topics):
    count = 0
    for topic in topics:
        for weighted_word in topic:
            if weighted_word[1] == word:
                count += 1
    return word == 1
