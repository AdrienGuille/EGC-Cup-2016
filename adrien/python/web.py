# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from flask import Flask, render_template, request
from lexicon import Lexicon
from corpus import Corpus
import text_mining

# Flask Web server
app = Flask(__name__)
# French lexicon used for lemmatization
lexicon = None
# Default corpus (French article published since EGC 2010)
corpus = None


@app.route('/')
def index():
    titles = corpus.lemmatized_title_list()
    lda_topics = text_mining.train_lda(documents=titles, num_topics=15, num_words=10, remove_singleton=False)
    text_mining.construct_and_save_word_topic_graph(lda_topics, 'static/graph.json')
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index2():
    years = request.form['years']
    print years
    year_array = years.split('_')
    global corpus
    print 'Loading new corpus: French article published between', int(year_array[0]), 'and', int(year_array[1]), '...'
    corpus = Corpus(update_data=True, lexicon=lexicon, title_lang='fr', year_a=int(year_array[0]), year_b=int(year_array[1]))
    titles = corpus.lemmatized_title_list()
    lda_topics = text_mining.train_lda(documents=titles, num_topics=15, num_words=10, remove_singleton=False)
    text_mining.construct_and_save_word_topic_graph(lda_topics, 'static/graph.json')
    return render_template('index.html', year1=int(year_array[0]), year2=int(year_array[1]))


if __name__ == '__main__':
    print 'Loading French lexicon for lemmatization...'
    lexicon = Lexicon(update_data=True)
    print 'Loading default corpus: French article published since EGC 2010 ...'
    corpus = Corpus(update_data=True, lexicon=lexicon, title_lang='fr', year_a=2010, year_b=2016)
    print 'Starting Flask application...'
    app.run(debug=True, host='localhost', port=8080)
