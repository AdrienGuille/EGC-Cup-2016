# coding: utf-8
from nlp.topic_model import LatentDirichletAllocation, NonNegativeMatrixFactorization
from structure.corpus import Corpus
from structure.author_topic_graph import AuthorTopicGraph
from flask import Flask, render_template
import utils
import itertools
from flask.ext.frozen import Freezer
import shutil
import os

__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

# Flask Web server
app = Flask(__name__)
freeze_browser = True

# Parameters
max_tf = 0.8
min_tf = 4
lemmatizer = None
num_topics = 15
vectorization = 'tfidf'


# Load corpus
'''
corpus = Corpus(source_file_path='../input/egc_lemmatized.csv',
                language='french',
                vectorization=vectorization,
                max_relative_frequency=max_tf,
                min_absolute_frequency=min_tf,
                preprocessor=None)
print 'corpus size:', corpus.size
print 'vocabulary size:', len(corpus.vocabulary)

# Infer topics
topic_model = NonNegativeMatrixFactorization(corpus=corpus)
topic_model.infer_topics(num_topics=num_topics)
utils.save_topic_model(topic_model, '../nmf_15topics_egc.pickle')
topic_model.print_topics(num_words=10)
'''
topic_model = utils.load_topic_model('../nmf_15topics_egc.pickle')

# Clean the data directory
if os.path.exists('static/data'):
    shutil.rmtree('static/data')
os.makedirs('static/data')

# Export topic cloud
utils.save_topic_cloud(topic_model, 'static/data/topic_cloud.json')

# Export details about topics
for topic_id in range(topic_model.nb_topics):
    utils.save_word_distribution(topic_model.top_words(topic_id, 20),
                                 'static/data/word_distribution'+str(topic_id)+'.tsv')
    utils.save_affiliation_repartition(topic_model.affiliation_repartition(topic_id),
                                       'static/data/affiliation_repartition'+str(topic_id)+'.tsv')
    evolution = []
    for i in range(2004, 2016):
        evolution.append((i, topic_model.topic_frequency(topic_id, date=i)))
    utils.save_topic_evolution(evolution, 'static/data/frequency'+str(topic_id)+'.tsv')

# Export details about documents
for doc_id in range(topic_model.corpus.size):
    utils.save_topic_distribution(topic_model.topic_distribution_for_document(doc_id),
                                  'static/data/topic_distribution_d'+str(doc_id)+'.tsv')

# Export details about words
for word_id in range(len(topic_model.corpus.vocabulary)):
    utils.save_topic_distribution(topic_model.topic_distribution_for_word(word_id),
                                  'static/data/topic_distribution_w'+str(word_id)+'.tsv')

# Associate documents with topics
topic_associations = topic_model.documents_per_topic()

# Export per-topic author network
for topic_id in range(topic_model.nb_topics):
    utils.save_json_object(topic_model.corpus.collaboration_network(topic_associations[topic_id]),
                           'static/data/author_network'+str(topic_id)+'.json')

# Export bipartite author-topic graph
author_topic_graph = AuthorTopicGraph(topic_model)
utils.save_json_object(author_topic_graph.json_graph,
                       'static/data/author_topic_graph.json')

print 'Topic/corpus browser ready'


@app.route('/')
def index():
    return render_template('index.html',
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(topic_model.corpus.size),
                           method=type(topic_model).__name__,
                           corpus_size=topic_model.corpus.size,
                           vocabulary_size=len(topic_model.corpus.vocabulary),
                           max_tf=max_tf,
                           min_tf=min_tf,
                           vectorization=vectorization,
                           preprocessor=type(lemmatizer).__name__,
                           num_topics=num_topics)


@app.route('/topic_cloud.html')
def topic_cloud():
    return render_template('topic_cloud.html',
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(topic_model.corpus.size))


@app.route('/vocabulary.html')
def vocabulary():
    word_list = []
    for i in range(len(topic_model.corpus.vocabulary)):
        word_list.append((i, topic_model.corpus.word_for_id(i)))
    splitted_vocabulary = []
    words_per_column = int(len(topic_model.corpus.vocabulary)/5)
    for j in range(5):
        sub_vocabulary = []
        for l in range(j*words_per_column, (j+1)*words_per_column):
            sub_vocabulary.append(word_list[l])
        splitted_vocabulary.append(sub_vocabulary)
    return render_template('vocabulary.html',
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(topic_model.corpus.size),
                           splitted_vocabulary=splitted_vocabulary,
                           vocabulary_size=len(word_list))


@app.route('/author_topic_graph.html')
def author_topic_graph():
    return render_template('author_topic_graph.html',
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(topic_model.corpus.size))


@app.route('/topic/<tid>.html')
def topic_details(tid):
    ids = topic_associations[int(tid)]
    documents = []
    for document_id in ids:
        documents.append((topic_model.corpus.short_content(document_id).capitalize(),
                          ', '.join(topic_model.corpus.authors(document_id)),
                          topic_model.corpus.date(document_id), document_id))
    return render_template('topic.html',
                           topic_id=tid,
                           frequency=round(topic_model.topic_frequency(int(tid))*100, 2),
                           documents=documents,
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(topic_model.corpus.size))


@app.route('/document/<did>.html')
def document_details(did):
    vector = topic_model.corpus.vector_for_document(int(did))
    word_list = []
    for a_word_id in range(len(vector)):
        word_list.append((topic_model.corpus.word_for_id(a_word_id), round(vector[a_word_id], 3), a_word_id))
    word_list.sort(key=lambda x: x[1])
    word_list.reverse()
    nb_words = 20
    if [w[1] for w in word_list].index(0.0) < nb_words:
        nb_word = [w[1] for w in word_list].index(0.0)
    documents = []
    for another_doc in topic_model.corpus.similar_documents(int(did), 5):
        documents.append((topic_model.corpus.short_content(another_doc[0]).capitalize(),
                          ', '.join(topic_model.corpus.authors(another_doc[0])),
                          topic_model.corpus.date(another_doc[0]), another_doc[0], round(another_doc[1], 3)))
    return render_template('document.html',
                           doc_id=did,
                           words=word_list[:nb_words],
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(topic_model.corpus.size),
                           documents=documents,
                           authors=', '.join(topic_model.corpus.authors(int(did))),
                           year=topic_model.corpus.date(int(did)),
                           short_content=topic_model.corpus.short_content(int(did)),
                           article_id=topic_model.corpus.data_frame.iloc[int(did)]['url'])


@app.route('/word/<wid>.html')
def word_details(wid):
    documents = []
    for document_id in topic_model.corpus.docs_for_word(int(wid)):
        documents.append((topic_model.corpus.short_content(document_id).capitalize(),
                          ', '.join(topic_model.corpus.authors(document_id)),
                          topic_model.corpus.date(document_id), document_id))
    return render_template('word.html',
                           word_id=wid,
                           word=topic_model.corpus.word_for_id(int(wid)),
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(topic_model.corpus.size),
                           documents=documents)

if __name__ == '__main__':
    if freeze_browser:
        app.config.update(
            FREEZER_BASE_URL='http://mediamining.univ-lyon2.fr/people/guille/egc2016/',
        )
        freezer = Freezer(app)
        @freezer.register_generator
        def topic_details():
            for topic_id in range(topic_model.nb_topics):
                yield {'tid': topic_id}
        @freezer.register_generator
        def document_details():
            for doc_id in range(topic_model.corpus.size):
                yield {'did': doc_id}
        @freezer.register_generator
        def word_details():
            for word_id in range(len(topic_model.corpus.vocabulary)):
                yield {'wid': word_id}
        freezer.freeze()
    else:
        # Load corpus
        app.run(debug=True, host='localhost', port=2016)
