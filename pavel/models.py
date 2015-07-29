__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline


from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.feature_extraction.text import TfidfVectorizer

1


def build_unsup_base_model(level="word", ngrams=(1, 3)):
    select = SelectPercentile(score_func=chi2, percentile=15)

    clust = KMeans(n_clusters=10, random_state=42)
    countvect_word = TfidfVectorizer(ngram_range=ngrams, analyzer=level)
    pipeline = Pipeline([("datamatrix", countvect_word), ("select", select), ("clust", clust)])
    return pipeline
