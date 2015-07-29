from nltk.probability import FreqDist
from nltk.util import ngrams
from nltk.collocations import AbstractCollocationFinder
from nltk.metrics.association import NgramAssocMeasures

from itertools import permutations
from collections import defaultdict
import math as _math


# ## Indices to marginals arguments:

_log2 = lambda x: _math.log(x, 2.0)
_ln = _math.log

_product = lambda s: reduce(lambda x, y: x * y, s)

_SMALL = 1e-20

NGRAM = 0
"""Marginals index for the ngram count"""

UNIGRAMS = -2
"""Marginals index for a tuple of each unigram count"""

TOTAL = -1
"""Marginals index for the number of words in the data"""


class AnygramAssocMeasures(NgramAssocMeasures):
    """
    I am only interested in student t-test. Which could be usable
    from the parent class 'NgramAssocMeasures' but since we kindof do not
    agree with NLTK t-test formula, and by extension with Manning & Schutze
    t-test calculation. So here we implement our t-test, which uses the 
    population variance instead of the sample variance (as a z-test), which is more correct
    since we already know it as it is a Binomial (Bernoulli) distribution, so
    sigma^2 = p(1-p) and since p is small sigma^2 = p. Manning et al., they use the sample variance
    when there is no need to do so, as, again, we already know the population variance.
    
    No need for _n declaration. It is taken care of in the AnygramCollocationFinder score_ngram method.

    Here the _contingency and _marginals methods should be implemented. This is work pending.
    I do not use them so I did not implemented them yet, although it should 
    follow the way I used for the AnygramCollocation finder: the permutation('iiix') stuff.
    Likelihood measure and others DO need the contingency table and marginals.

    """

    @classmethod
    def our_student_t(cls, *marginals):
        """Scores ngrams using Student's t test with independence hypothesis
        for unigrams, using the population variance, as should be.
        """

        return ((marginals[NGRAM] -
                 _product(marginals[UNIGRAMS]) /
                 float(marginals[TOTAL] ** (cls._n - 1))) /
                (_product(marginals[UNIGRAMS]) /
                 float(marginals[TOTAL] ** (cls._n - 1)) + _SMALL) ** .5)


class AnygramCollocationFinder(AbstractCollocationFinder):
    """A tool for the finding and ranking of ngram collocations or other
    association measures. It is often useful to use from_words() rather than
    constructing an instance directly.
    """

    def __init__(self, n, word_fd, otherngram_fd, wildcard_fd, ngram_fd):
        """Construct a NramCollocationFinder, given FreqDists for
        appearances of words, bigrams, two words with any word between them,
        and trigrams.
        """
        AbstractCollocationFinder.__init__(self, word_fd, ngram_fd)
        self.wildcard_fd = wildcard_fd
        self.otherngram_fd = otherngram_fd
        self.n = n

    @staticmethod
    def convert_indices(string_indices):
        wildcard_indices = []
        for s in string_indices:
            temp = []
            for idx_i, c in enumerate(s):
                if c == 'i':
                    temp.append(idx_i)
            wildcard_indices.append(temp)
        pass
        return wildcard_indices

    @classmethod
    def from_words(cls, words, n):
        """Construct a AnygramCollocationFinder for all trigrams in the given
        sequence.
        """

        wildfd = FreqDist()
        #         nfd = {}
        nfd = defaultdict(FreqDist)
        #         for i in range(1, n + 1):
        #             nfd['n' * i] = FreqDist()

        for ngram in ngrams(words, n, pad_right=True):
            nfd['n'].inc(ngram[0])
            for idx in range(1, n):
                if ngram[idx] is None:
                    continue
                # We add the true ngrams (f.ex, iii for a trigram, or iiii for a fourgram)
                off_idx = idx + 1

                nfd['n' * off_idx][(tuple(ngram[:off_idx]))] += 1

                """
                
                We add the wildcards for each ngram (f.ex, ixii for a trigram)
                But  first we need to know the possible permutations of a 
                ngram and keep only the distincts and then keep only those
                that are wildcards, meaning that they are not proper ngrams
                in the sense that not all words of interest i are together
                
                Here we create a ngram string which has the shape
                iiix or whatever the case. For example:
                To find trigram wildcards in a fourgram sequence we have
                iiix, so three i's  and one x.
                We are (in the trigram case) interested in ixii, xixi, ixix,
                which are the wildcard patterns 
                """
                wildcard_string = "%s%s" % ('i' * off_idx, 'x' * (n - off_idx))

                # We permutate the letters of this string and it will
                # give us the words (w1,w2,w3,...) that make up the wildcard
                # TODO: Check if combination is not the same without filtering -_-
                wildcard_permut = list(set(permutations(wildcard_string, n)))

                # Now remove the true ngrams (iiix or iiiix)

                wildcard_permut = [w for w in wildcard_permut if 'i' * off_idx not in ''.join(w)]
                if not wildcard_permut:
                    continue
                # Now we transform this i's into indices to add the words to our wildcard FD
                # Such that ixii is converted into 0,2,3 (the positions on the string of the 'i's), so I know
                # that I need w0, w2 and w3 (or w1, w3 and w4 in a one-based counting...)

                wildcard_indices = cls.convert_indices(wildcard_permut)

                # So now we have the indices! So lets just add them to the wildcardfd
                for w in wildcard_indices:
                    wildcard_words = tuple([ngram[i] for i in w])
                    # Check that the ngrams with these indices actually exist
                    if all(wildcard_words):
                        wildfd[wildcard_words] += 1

        # Here we return the values to actually initialize the class. It should be noted that there
        # is an important detail with the "inside"ngrams of a given ngram (bigrams,trigrams inside
        # a quadgram). I return them as a dict of FreqDists. 
        return cls(n, nfd['n'], dict([('n' * f, nfd['n' * f]) for f in range(2, n)]), wildfd, nfd['n' * n])

    def score_ngram(self, score_fn, *words):
        """Returns the score for a given fourgram using the given scoring
        function.
        """

        if len(words) != self.n:
            print "You should ask specifically for a %d words ngram" % self.n
            return

        words = tuple(words)
        n_all = self.word_fd.N()
        n_ngram = self.ngram_fd[words]

        if not n_ngram:
            return
        n_unigrams = tuple([self.word_fd[w] for w in words])
        values = defaultdict(list)

        for idx in range(2, self.n):
            # We need the n-2-grams, n-1-grams, etc., found inside the ngram, either the
            # wildcards, like the wildcard trigram 'ixii', and real ngrams, like 'iiix'
            # We begin building the strings that must be permuted to find the correct sequence
            # We get the real and wildcards ngrams:
            ngram_string = "%s%s" % ('i' * idx, 'x' * (self.n - idx))
            ngram_permut = list(set(permutations(ngram_string, self.n)))
            wildcards = [w for w in ngram_permut if 'i' * idx not in ''.join(w)]
            true_ngrams = [w for w in ngram_permut if 'i' * idx in ''.join(w)]

            # TODO TOP PRIORITY TODO: Actually look for words, not iiix or whatever... This doesnot work! 
            # See from_words method
            for w in wildcards:
                values['n' * idx].append(self.wildcard_fd[w])
            for t in true_ngrams:
                values['n' * idx].append(self.otherngram_fd['n' * idx][t])

        # Add the _n value that is added in AssocMeasures, but we cannot add it there since n is not fixed
        if hasattr(score_fn, "im_self"):
            score_fn.im_self._n = self.n

        # This part I don't know how it should be solved. I want to return 
        # n-2 tuples as single parameters, but I can't imagine how to do it...
        # so I send a list..
        n_all_ngrams = [tuple(values['n' * i]) for i in range(2, self.n)]
        # We add the first element to be the n_ngram
        n_all_ngrams = [n_ngram] + n_all_ngrams
        n_all_ngrams.append(n_unigrams)
        n_all_ngrams.append(n_all)

        return score_fn(*n_all_ngrams)


if __name__ == '__main__':
    import nltk

    anygram_measures = AnygramAssocMeasures()
    bigram_measures = nltk.association.BigramAssocMeasures()

    #     finder = BigramCollocationFinder.from_words(nltk.corpus.genesis.words('english-web.txt'))
    #     print finder.nbest(bigram_measures.pmi, 10)
    mi_finder = AnygramCollocationFinder.from_words(nltk.corpus.genesis.words('english-web.txt')[:], 3)
    print mi_finder.nbest(anygram_measures.student_t, 10)
    print mi_finder.nbest(anygram_measures.our_student_t, 10)
    pass
