# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from flask import Flask, render_template, request
from lexicon import Lexicon
from corpus import Corpus
import text_mining
import platform


# Flask Web server
app = Flask(__name__)
# French lexicon used for lemmatization
lexicon = None
# Default corpus (French article published since EGC 2010)
corpus = None
# Topic format
num_topics = 8
num_words = 8


@app.route('/')
def index():
    titles = corpus.lemmatized_title_list()
    lda_topics = text_mining.train_lda(documents=titles, num_topics=num_topics, num_words=num_words, remove_singleton=False)
    text_mining.construct_and_save_word_topic_graph(lda_topics, 'static/graph.json')
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index2():
    years = request.form['years']
    year_array = years.split('_')
    checked_source = request.form.getlist('source')
    source = checked_source[0]
    global corpus
    print 'Loading new corpus: French article published between', int(year_array[0]), 'and', int(year_array[1]), '...'
    corpus = Corpus(update_data=True, lexicon=lexicon, title_lang='fr',
                    year_a=int(year_array[0]), year_b=int(year_array[1])+1)
    if source == 'abstracts':
        print 'Inferring topics from the abstracts with LDA'
        documents = corpus.lemmatized_abstract_list()
    elif source == 'titles':
        print 'Inferring topics from the titles with LDA'
        documents = corpus.lemmatized_title_list()
    lda_topics = text_mining.train_lda(documents=documents, num_topics=num_topics, num_words=num_words, remove_singleton=False)
    text_mining.construct_and_save_word_topic_graph(lda_topics, 'static/graph.json')
    return render_template('index.html', year1=int(year_array[0]), year2=int(year_array[1]))


if __name__ == '__main__':
    print platform.node()
    print 'Loading French lexicon for lemmatization...'
    lexicon = Lexicon(update_data=True)
    print 'Loading default corpus: French article published since EGC 2010 ...'
    corpus = Corpus(update_data=True, lexicon=lexicon, title_lang='fr', year_a=2010, year_b=2016)
    print 'Starting Flask application...'
    host = 'localhost'
    if 'mediamining' in platform.node():
        host = 'mediamining.univ-lyon2.fr'
    app.run(debug=True, host=host, port=2016)
