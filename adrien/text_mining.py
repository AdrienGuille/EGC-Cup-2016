# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from gensim import corpora, models
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import defaultdict

def compute_vector_space(abstracts, stemming=False):
    stop_word_list = stopwords.words('french')
    stop_word_list.extend(stopwords.words('english'))
    stop_word_list.extend([',', '.', '\'', '"', '(', ')', '-', ').', ':'])
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
    return [corpus_tfidf, dictionary]

def perform_lsi(abstracts, num_topics=10, stemming=False):
    vector_space_model = compute_vector_space(abstracts=abstracts, stemming=stemming)
    corpus_tfidf = vector_space_model[0]
    dictionary = vector_space_model[1]
    lsi = models.LsiModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=num_topics)
    return lsi.show_topics(num_topics=num_topics, num_words=10, formatted=False)

def train_lda(abstracts, num_topics=10, stemming=False):
    vector_space_model = compute_vector_space(abstracts=abstracts, stemming=stemming)
    corpus_tfidf = vector_space_model[0]
    dictionary = vector_space_model[1]
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
