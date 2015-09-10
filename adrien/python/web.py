# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from flask import Flask, render_template
from lexicon import Lexicon
from corpus import Corpus
import text_mining

# Flask Web server
app = Flask(__name__)
# French lexicon used for lemmatization
lexicon = Lexicon(update_data=True)
# Default corpus (French article published since EGC 2010)
corpus = Corpus(update_data=True, lexicon=lexicon, title_lang='fr', year_a=2010, year_b=2016)


@app.route('/')
def index():
    #titles = corpus.lemmatized_title_list()
    #lda_topics = text_mining.train_lda(documents=titles, num_topics=15, num_words=10, remove_singleton=False)
    return render_template('index.html')

if __name__ == '__main__':
    print 'Loading data...'
    app.run(debug=True, host='localhost', port=8080)
