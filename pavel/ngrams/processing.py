#!/usr/bin/env python
# -*- coding: latin-1 -*-
'''
Created on Feb 3, 2014

@author: pavelo
'''
from collections import defaultdict
from math import log

import nltk

from nltk.text import TextCollection

from configuration import config_path, config_stem, config_stopwords, config_bool_stopwords, config_top_k, \
    config_min_tok_len, config_ngram, config_output, config_min_tok_freq
from containers import Document
from utils import import_text_lines, get_texts, \
    update_dict_values
from n_association import AnygramAssocMeasures, AnygramCollocationFinder

from pavel.data_manips import load_data, get_EGC_articles



# GLOBALS for the mesure's names
FREQ = "FREQ"
LIKELIHOOD = "LIKELIHOOD"
PMI = "PMI"
CHI_SQUARE = "CHI_SQUARE"
T_TEST = "T_TEST"
OUR_T_TEST = "OUR_T_TEST"
TFIDF = "TFIDF"
N = "N"
CONCORDANCE = "CONCORDANCE"

# Determine what kind of measure we will use, depending on the config file
measure_dict = {
    FREQ: AnygramAssocMeasures.raw_freq,
    PMI: AnygramAssocMeasures.pmi,
    T_TEST: AnygramAssocMeasures.student_t,
    OUR_T_TEST: AnygramAssocMeasures.our_student_t,
}

if config_bool_stopwords:
    _, stopwords_list = import_text_lines(config_stopwords, encode="utf-8")
    stopwords_list = [w.encode("utf-8") for w in stopwords_list]




def get_any_ngrams(list_documents, ngram=3, min_tok_len=3, min_freq=4,
                   k=50, verbose=False):
    """
    Find trigrams using [Bi][Tri]gramCollocationFinder from the given
    nltk.Document list_documents.
    Returns a dict of dicts with the text name as key and
    its value (a dict) with ngrams as keys and a dict as value, 
    with each measure and its values:
     {"term1": {"FREQ":3000, "PMI":0.343}, "term2": {"FREQ":3000, "PMI":0.3422}, ...} 
        
    """

    tfidf_list = []
    doc_ngrams_scores = {}
    anygram_measures = AnygramAssocMeasures()
    n_texts = float(len(list_documents._texts))

    tfidf_dict = defaultdict(int)
    for d in list_documents._texts:
        ngrams_scores = defaultdict(dict)
        # Find ngrams 


        print "Finding %d-grams for %s..." % (ngram, d.name)
        tcf = AnygramCollocationFinder.from_words(d._tokens, ngram)

        # Filter ngrams according to minimum frequency, length of words in the ngram, 
        # and stopwords in the ngram
        tcf.apply_freq_filter(min_freq)
        # Remove ngrams with points in them, cause those are from different sentences
        tcf.apply_word_filter(lambda w: w in ["."])
        tcf.apply_word_filter(lambda w: len(w) < min_tok_len)
        if config_bool_stopwords:
            tcf.apply_word_filter(lambda w: w in set(stopwords_list))

        for ngr in tcf.ngram_fd.iterkeys():
            tfidf_dict[ngr] += 1

        # Calculate the scores for the ngrams        
        top_k_ttest = tcf.nbest(anygram_measures.our_student_t, k)
        # Create a TextCollection to  found ngrams to then calculate  tfidfs
        ngram_doc = ["_".join(tm) for tm in top_k_ttest]
        tfidf_list.append(nltk.Text(ngram_doc, name=d.name))
        for ng in top_k_ttest:
            print "\t", ng
            for measure, func in measure_dict.items():
                ngrams_scores[ng][measure] = tcf.score_ngram(func, *ng)

        doc_ngrams_scores[d.name] = ngrams_scores

    # Here we add the tf_idf for each ngram in each document
    for _, tscores in doc_ngrams_scores.items():
        for term, scores in tscores.items():
            tfidf_value = scores[FREQ] * log(n_texts / tfidf_dict[term])
            scores.update({TFIDF: tfidf_value, N: ngram})

    return doc_ngrams_scores





def get_concordances(list_documents, scored_ngrams):
    print
    print "Calculate concordances"
    for doc in list_documents._texts:
        dict_ngrams = scored_ngrams[doc.name]
        print "Finding concordances for %s\n" % doc.name
        # TODO: Get concordances for only the k-top ngrams
        for t, scores in dict_ngrams.items():
            concordance = doc.concordance_ngrams(t, 3)
            if concordance:
                concordances_found = list(set([" ".join(c) for c in concordance]))
                concordances_found = '"%s"' % u" | ".join(concordances_found)
                scores.update({CONCORDANCE: concordances_found})
                #                 for c in concordance:
                #                     print(" ".join(c))
                #
                #             print "*"*100

    return scored_ngrams


def get_unigrams(tc):
    """
    Get the unigrams from the documents in the list
    Return a list of dictionaries (one for each text) with the unique terms as keys
    and a dictionary with the frequency as value:
    {"term1": {"FREQ":3000}, "term2": {"FREQ":3000}, ...} 
    """
    dict_unigrams = {}
    text_unigrams = {}
    for t in tc._texts:
        fdist = t.vocab()
        print "\t...for %s" % t.name
        ordered_fdist = zip(fdist.keys(), fdist.values())
        for term, val in ordered_fdist[:config_top_k]:
            dict_unigrams[term] = {FREQ: float(val) / len(t.tokens), TFIDF: tc.tf_idf(term, t), N: 1}
        text_unigrams[t.name] = dict_unigrams

    # print ordered_fdist[:config_top_k]
    return text_unigrams


def make_tables(scored_ngrams, results_folder="./", encoding="utf-8"):
    sep = u","
    #     scores = scored_ngrams.values()[0].values()[0].keys()
    scores = [N, FREQ, TFIDF, PMI, OUR_T_TEST, T_TEST, CONCORDANCE]
    column_headers = u"TERM" + sep + sep.join(scores) + "\n"
    for text, tscores in scored_ngrams.items():

        path = results_folder + u"RESULT_" + text[:-4] + u".csv"
        fileo = open(path, "w")
        fileo.write(column_headers)

        for term, scores_dic in tscores.items():
            line_string = [" ".join(term)]
            for col in scores:
                if scores_dic.has_key(col):
                    line_string.append(scores_dic[col])
                else:
                    line_string.append(u'NA')
            line_string = sep.join([unicode(v) for v in line_string])
            fileo.write(line_string.encode(encoding) + "\n")
        fileo.close()
        pass

    pass


def main2():
    df = load_data("../input/RNTI_articles_export_fixed1347_ids.txt")
    df = get_EGC_articles(df)

def main():
    # Get text from folder or file
    # TODO Change the folder corpus to the upper level!
    texts = get_texts(config_path)
    if not texts:
        print "No texts found"
        return
    # Dictionary that will hold all the ngrams and their values, for each measure (dict of dicts)
    scored_ngrams = {}
    # Create a list of Document objects with the texts. Pretreat them also.
    list_documents = []

    for label, text in texts.iteritems():
        list_documents.append(Document(text, stem=config_stem, name=label))

    # list_documents = TextCollection([Document(text, stem=config_stem, name=label)
    #                                  for label, text in texts.items()][:])
    list_documents = TextCollection(list_documents)
    global config_ngram
    if config_ngram == 0:
        config_ngram = 1

    #########################################N GRAM EXTRACTION #################################################

    # Now do the ngram extraction

    for ng in range(2, config_ngram + 1):
        ngrams = get_any_ngrams(list_documents, ngram=ng, k=config_top_k,
                                min_tok_len=config_min_tok_len, min_freq=config_min_tok_freq)

        scored_ngrams = update_dict_values(scored_ngrams, ngrams)

    scored_ngrams = update_dict_values(scored_ngrams, get_concordances(list_documents, scored_ngrams))
    make_tables(scored_ngrams, results_folder=config_output)
    return


if __name__ == '__main__':
    from datetime import datetime

    start_time = datetime.now()
    #     cProfile.run('main()')
    main()
    print(datetime.now() - start_time)
