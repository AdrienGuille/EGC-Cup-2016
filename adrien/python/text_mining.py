# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from gensim import corpora, models
from nltk import wordpunct_tokenize
from nltk.stem import SnowballStemmer
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import codecs
import json
import networkx as nx
import miscellaneous as misc
import math


def compute_vector_space(documents, remove_singleton=True):
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


def perform_lsa(documents, num_topics=10, num_words=10, remove_singleton=True):
    vector_space_model = compute_vector_space(documents=documents, remove_singleton=remove_singleton)
    corpus_tfidf = vector_space_model[0]
    dictionary = vector_space_model[1]
    lsi = models.LsiModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_topics)
    return lsi.show_topics(num_topics=num_topics, num_words=num_words, formatted=False)


def train_lda(documents, num_topics=10, num_words=None, remove_singleton=True):
    vector_space_model = compute_vector_space(documents=documents, remove_singleton=remove_singleton)
    corpus_tfidf = vector_space_model[0]
    dictionary = vector_space_model[1]
    if num_words is None:
        num_words = len(dictionary)
    lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, iterations=30000, num_topics=num_topics)
    return lda.show_topics(num_topics=num_topics, num_words=num_words, formatted=False)


def perform_nmf(documents, num_topics=10, num_words=10):
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=2000)
    tfidf = vectorizer.fit_transform(documents)
    nmf = NMF(n_components=num_topics, random_state=1).fit(tfidf)
    feature_names = vectorizer.get_feature_names()
    topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        word_list = [feature_names[i] for i in topic.argsort()[:-num_words - 1:-1]]
        weighted_word_list = []
        for word in word_list:
            weighted_word_list.append(('0.0', word))
        topics.append(weighted_word_list)
    return topics


def compare_models(model0, model1):
    divergence_matrix = []
    vocabulary = set()
    for probability, word in model0[0]:
        vocabulary.add(word)
    for probability, word in model1[0]:
        vocabulary.add(word)
    for topic0 in model0:
        dict0 = {}
        for probability, word in topic0:
            dict0[word] = probability
        distribution0 = []
        for word in vocabulary:
            probability = dict0.get(word)
            if probability is None:
                probability = 0.000001
            distribution0.append(probability)
        row = []
        for topic1 in model1:
            dict1 = {}
            for probability, word in topic1:
                dict1[word] = probability
            distribution1 = []
            for word in vocabulary:
                probability = dict1.get(word)
                if probability is None:
                    probability = 0.000001
                distribution1.append(probability)
            jsd = misc.jensen_shannon_divergence(distribution0, distribution1)
            distance = math.sqrt(jsd)
            row.append(distance)
        divergence_matrix.append(row)
    return divergence_matrix


def print_topics(topics, num_words=10):
    count = 0
    for topic in topics:
        word_list = []
        for weighted_word in topic:
            word_list.append(weighted_word[1])
            if len(word_list) == num_words:
                break
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
        for j in range(0, len(topic)):
            main_word = topic[j][1]
            main_word_id = nodes_array.index(main_word)
            for i in range(j+1, len(topic)):
                this_word_id = nodes_array.index(topic[i][1])
                json_links.append({'source': main_word_id, 'target': this_word_id, 'value':int(len(topic)-i)})
                nx_graph.add_edge(unicode(main_word), unicode(topic[i][1]))
    nodes_array = []
    group = 0
    page_rank = nx.pagerank(nx_graph, alpha=0.85, max_iter=300)
    for topic in topics:
        for weighted_word in topic:
            if weighted_word[1] not in nodes_array:
                nodes_array.append(weighted_word[1])
                if word_is_unique(weighted_word[1], topics):
                    json_nodes.append({'name': weighted_word[1],
                                       'weight': page_rank.get(weighted_word[1])*10,
                                       'group': group})
                else:
                    json_nodes.append({'name': weighted_word[1],
                                       'weight': page_rank.get(weighted_word[1])*10,
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
    return count == 1
