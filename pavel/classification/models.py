from sklearn.decomposition import NMF
from sklearn.tree import DecisionTreeClassifier
from ngrams.utils import load_stopword_list
from utils import french_tokenizer

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

from sklearn.pipeline import Pipeline

from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.feature_extraction.text import TfidfVectorizer


def build_sup_base_model():
    clasif = DecisionTreeClassifier()
    pipeline = Pipeline([("clasif", clasif)])
    return pipeline

