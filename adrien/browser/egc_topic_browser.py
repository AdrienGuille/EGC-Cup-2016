# coding: utf-8
from nlp.topic_model import LatentDirichletAllocation, NonNegativeMatrixFactorization
from structure.corpus import Corpus
from structure.author_topic_graph import AuthorTopicGraph
import numpy as np
from scipy import stats as st
from flask import Flask, render_template
import utils
from flask.ext.frozen import Freezer
import shutil
import os

__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

# Flask Web server
app = Flask(__name__)
freeze_browser = True

# Parameters
update_data = False
max_tf = 0.8
min_tf = 4
lemmatizer = None
num_topics = 15
vectorization = 'tfidf'

# Fit a new topic model
'''
# Load corpus
corpus = Corpus(source_file_path='../input/input_for_topic_modeling.csv',
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

# Load an existing topic model
topic_model = utils.load_topic_model('../nmf_15topics_egc.pickle')
topic_model.print_topics()

# Associate documents with topics
topic_associations = topic_model.documents_per_topic()
# Extract the list of authors
author_list = topic_model.corpus.all_authors()

if update_data:
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
    # Export details about authors
    for author_id in range(len(author_list)):
        utils.save_topic_distribution(topic_model.topic_distribution_for_author(author_list[author_id]),
                                      'static/data/topic_distribution_a'+str(author_id)+'.tsv')
    # Export per-topic author network
    for topic_id in range(topic_model.nb_topics):
        utils.save_json_object(topic_model.corpus.collaboration_network(topic_associations[topic_id]),
                               'static/data/author_network'+str(topic_id)+'.json')

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


@app.route('/author_index.html')
def authors():
    splitted_author_list = []
    authors_per_column = int(len(author_list)/5)
    for j in range(5):
        sub_list = []
        for l in range(j*authors_per_column, (j+1)*authors_per_column):
            sub_list.append((l, author_list[l]))
        splitted_author_list.append(sub_list)
    return render_template('all_authors.html',
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(topic_model.corpus.size),
                           splitted_author_list=splitted_author_list,
                           number_of_authors=len(author_list))


@app.route('/topic/<tid>.html')
def topic_details(tid):
    ids = topic_associations[int(tid)]
    documents = []
    for document_id in ids:
        document_author_id = []
        for author_name in topic_model.corpus.authors(document_id):
            document_author_id.append((author_list.index(author_name), author_name))
        documents.append((topic_model.corpus.short_content(document_id).capitalize(),
                          document_author_id,
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
    documents = []
    for another_doc in topic_model.corpus.similar_documents(int(did), 5):
        document_author_id = []
        for author_name in topic_model.corpus.authors(another_doc[0]):
            document_author_id.append((author_list.index(author_name), author_name))
        documents.append((topic_model.corpus.short_content(another_doc[0]).capitalize(),
                          document_author_id,
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
        document_author_id = []
        for author_name in topic_model.corpus.authors(document_id):
            document_author_id.append((author_list.index(author_name), author_name))
        documents.append((topic_model.corpus.short_content(document_id).capitalize(),
                          document_author_id,
                          topic_model.corpus.date(document_id), document_id))
    return render_template('word.html',
                           word_id=wid,
                           word=topic_model.corpus.word_for_id(int(wid)),
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(topic_model.corpus.size),
                           documents=documents)


@app.route('/author/<aid>.html')
def author_details(aid):
    documents = []
    for document_id in topic_model.corpus.documents_by_author(author_list[int(aid)]):
        document_author_id = []
        for author_name in topic_model.corpus.authors(document_id):
            document_author_id.append((author_list.index(author_name), author_name))
        documents.append((topic_model.corpus.short_content(document_id).capitalize(),
                          document_author_id,
                          topic_model.corpus.date(document_id), document_id))
    repartition = np.array(topic_model.topic_distribution_for_author(author_list[int(aid)]))
    skewness = float(st.skew(repartition, axis=0))
    return render_template('author.html',
                           author_name=author_list[int(aid)],
                           author_id=str(int(aid)),
                           affiliations='',
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(topic_model.corpus.size),
                           documents=documents,
                           skewness=round(skewness, 3))

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
        @freezer.register_generator
        def author_details():
            for author_id in range(len(author_list)):
                yield {'aid': author_id}
        freezer.freeze()
    else:
        # Load corpus
        app.run(debug=True, host='localhost', port=2016)
