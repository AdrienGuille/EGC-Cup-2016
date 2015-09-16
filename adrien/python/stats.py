# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from lexicon import Lexicon
from corpus import Corpus
from scipy import stats
import numpy
import math


def compute_linear_correlation_matrix():
    lexicon = Lexicon(update_data=True)
    corpus = Corpus(update_data=True, lexicon=lexicon, title_lang='fr', year_a=2004, year_b=2016)
    corpora = []
    vocabulary = set()
    for i in range(2004, 2016):
        corpus = Corpus(update_data=False, lexicon=lexicon, title_lang='fr', year_a=i, year_b=i+1)
        corpora.append(corpus)
        vocabulary = vocabulary.union(corpus.vocabulary)
    vocabulary_size = len(vocabulary)
    print 'vocabulary size:', vocabulary_size
    correlation_matrix = numpy.eye(vocabulary_size)
    pvalue_matrix = numpy.eye(vocabulary_size)
    word_list = list(vocabulary)
    for i in range(0, vocabulary_size):
        print i
        word_i = word_list[i]
        freq_i = []
        for corpus in corpora:
            freq_i.append(corpus.get_frequency_in_abstracts(word=word_i, lemmatized=True))
        for j in range(i+1, vocabulary_size):
            word_j = word_list[j]
            freq_j = []
            for corpus in corpora:
                freq_j.append(corpus.get_frequency_in_abstracts(word=word_j, lemmatized=True))
            if max(freq_i) > 0.10 and max(freq_j) > 0.10:
                pearson = stats.pearsonr(freq_i, freq_j)
                correlation_matrix[i][j] = pearson[0]
                pvalue_matrix[i][j] = pearson[1]
                if pearson[0] < -0.6 and pearson[1] < 0.05:
                    print word_i, word_j, pearson[0], pearson[1]

if __name__ == '__main__':
    compute_linear_correlation_matrix()
