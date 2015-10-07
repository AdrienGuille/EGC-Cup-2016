from sklearn.decomposition import NMF
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from ngrams.utils import load_stopword_list
from utils import french_tokenizer
from sklearn.linear_model import LogisticRegression
from sklearn import linear_model
from sklearn.svm import SVC

__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'

from sklearn.pipeline import Pipeline

from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.feature_extraction.text import TfidfVectorizer


def build_sup_base_model():
    # clasif = linear_model.LinearRegression()
    # clasif = SVC(kernel="linear")
    clasif = RandomForestClassifier(n_estimators=15)
    pipeline = Pipeline([("clasif", clasif)])
    return pipeline

