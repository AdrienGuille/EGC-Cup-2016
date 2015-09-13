from sklearn.decomposition import NMF
from ngrams.utils import load_stopword_list
from utils import french_tokenizer

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline

from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.feature_extraction.text import TfidfVectorizer


def build_unsup_base_model(level="word", ngrams=(1, 11)):
    select = SelectPercentile(score_func=chi2, percentile=15)

    clust = KMeans(n_clusters=15, random_state=42)
    countvect_word = TfidfVectorizer(ngram_range=ngrams, analyzer=level, strip_accents="unicode")
    pipeline = Pipeline([("datamatrix", countvect_word), ("select", select), ("clust", clust)])
    return pipeline


def build_unsup_nmf(level="word", ngrams=(1, 3)):
    n_features = 1000
    n_topics = 14
    vectorizer = TfidfVectorizer(ngram_range=ngrams, analyzer=level, max_df=0.85, min_df=5, max_features=n_features,
                                 use_idf=True, stop_words=load_stopword_list("../ngrams/stopwords.txt"),
                                 tokenizer=french_tokenizer)
    nmf = NMF(n_components=n_topics, random_state=1000)
    pipeline = Pipeline([("vectorize", vectorizer), ("clust", nmf)])

    return pipeline
