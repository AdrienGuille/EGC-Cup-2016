# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from gensim import corpora, models
from nltk.corpus import stopwords
from collections import defaultdict


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

def train_lda(abstracts, num_topics):
    stopword_list = stopwords.words('french')
    formatted_abstracts = [[word for word in abstract.lower().split() if word not in stopword_list] for abstract in abstracts]
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

def create_collaboration_graph(corpus):
    collaborations = set()
    for article in corpus:
        authors = article.get('authors')
        year = article.get('year')
        for i in range(0, len(authors)):
            for j in range(i+1, len(authors)):
                collaboration = authors[i]+'\t'+authors[j]
                collaborations.add(collaboration)
    print len(collaborations), 'collaborations'
    return collaborations

def export_collaboration_graph(file_path, edge_set):
    output_file = open(file_path, 'w')
    output_file.write("\n".join(edge_set))

article_corpus = load_corpus('RNTI_articles_export_utf-8.txt')
collaboration_graph = create_collaboration_graph(article_corpus)
export_collaboration_graph('all_collaborations.csv', collaboration_graph)
latent_topics = train_lda(abstract_list(article_corpus), 20)
print_topics(latent_topics)
