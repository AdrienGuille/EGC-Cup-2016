# -*- coding: latin-1 -*-
'''
Created on Feb 3, 2014

@author: pavelo
'''

import nltk

tok_fr = nltk.RegexpTokenizer(r'''(?x)
                      \d+(\.\d+)?\s*%   # les pourcentages
                | \w'               # les contractions d', l', ...
                | \w+               # les mots pleins
                | [^\w\s]           # les ponctuations
                ''')


class Document(nltk.Text):
    def find_point(self, idx, direction="fwd"):
        if direction == "fwd":
            value = 1
        else:
            value = -1

        while (self._tokens[idx] != "."):
            idx += value
            if idx < 0:
                return 0
            if idx >= len(self._tokens):
                return len(self._tokens) - 1
        return idx + 1

    def concordance_ngrams(self, ngram, concordances_max=3):
        """
        This function finds a concordance (words sourrounding the given trigram)
        for the given trigram (w1,w2,w3).
        
        The sentence where the trigram was found will be returned
        """
        concordances_found = 0
        if not self.__getattribute__("_tokens"):
            return "No _tokens yet"

        self.list_concordance = []
        w1 = ngram[0]
        offset_w1 = self._concordance_index.offsets(w1)
        # If we found the first word of the trigram (w1) in the current text
        if offset_w1:
            # For each occurrence of w1:
            for idx in offset_w1:
                if concordances_found >= concordances_max:
                    break
                # We check that the following words are part of the ngram
                is_ngram = 0
                for idx_p, w_idx in enumerate(range(idx + 1, idx + len(ngram))):

                    if w_idx < len(self.tokens) and self.tokens[w_idx] == ngram[idx_p + 1]:
                        is_ngram += 1
                    else:
                        break
                        # If the number of matched words are the same number of words of the ngram, then we have
                # our ngram.
                if len(ngram) == is_ngram + 1:
                    # Then we build the concordance 
                    concordances_found += 1
                    concordance_tokens = [t for t in
                                          self._tokens[self.find_point(idx, "bwd"):self.find_point(idx)]]
                    self.list_concordance.append([t.decode("latin-1") for t in concordance_tokens])
        return self.list_concordance

    def preprocess(self, text=None, stem=False, stopwords=False):

        if text is None:
            text = self.text

        def tokenizer_fr(text):
            # Courtesy of http://www.fabienpoulard.info/post/2008/03/05/Tokenisation-en-mots-avec-NLTK

            return tok_fr.tokenize(text)

        # Tokenization
        self._original_tokens = tokenizer_fr(text)
        self._tokens = self._original_tokens

        #         self._tokens = [t for t in self._tokens if len(t) > 1]

        if stem:
            from nltk.stem.snowball import FrenchStemmer
            fr_stemmer = FrenchStemmer()

            self._tokens = [fr_stemmer.stem(t) for t in self._tokens]
        self._concordance_index = nltk.ConcordanceIndex(self._tokens, key=lambda s: s)

    def __init__(self, text=None, stem=False, stopwords=False, name=None):
        self.text = text.encode("latin-1")
        self.preprocess(self.text, stem=stem,
                        stopwords=stopwords)  # en lieu de map(lambda t: t.preprocess(stem=True, stopwords=True), list_documents)
        super(Document, self).__init__(self._tokens, name)
        pass
