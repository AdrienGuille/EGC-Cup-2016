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
    config_min_tok_len
from containers import Document
from utils import import_text_lines, get_texts, \
    update_dict_values
from n_association import AnygramAssocMeasures, AnygramCollocationFinder




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
    _, fr_stopwords = import_text_lines(config_stopwords, encode="utf8")
    fr_stopwords = [w.encode("utf-8") for w in fr_stopwords]


def fix_ZZ_labels(text):
    def remove_zz_labels(text):
        import re
        # Replace all ZZtheme01 for text markers to separate interviews
        text = re.sub(ur"ZZtheme01", "_texte_", text)
        # Remove all ZZtheme0X tags from the text
        text = re.sub(ur"ZZtheme[0-9]+", "", text)
        # Remove the rest of ZZ tags
        text = re.sub(ur"ZZ.*", "", text).strip("\n")
        # Replace crazy apostrophe for normal one.
        text = text.replace(u"\x92", "'")
        return text

    text = remove_zz_labels(text)
    return text.lower()


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
    ngrams_scores = defaultdict(dict)
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
        tcf.apply_word_filter(lambda w: len(w) < min_tok_len)
        if config_bool_stopwords:
            tcf.apply_word_filter(lambda w: w in set(fr_stopwords))

        for ngr in tcf.ngram_fd.iterkeys():
            tfidf_dict[ngr] += 1

        # Calculate the scores for the ngrams        
        top_k_ttest = tcf.nbest(anygram_measures.our_student_t, k)
        # Create a TextCollection to  found ngrams to then calculate  tfidfs
        ngram_doc = ["_".join(tm) for tm in top_k_ttest]
        tfidf_list.append(nltk.Text(ngram_doc, name=d.name))
        for ng in top_k_ttest:
            print "--", ng
            for measure, func in measure_dict.items():
                ngrams_scores[ng][measure] = tcf.score_ngram(func, *ng)

        doc_ngrams_scores[d.name] = ngrams_scores

    # tfidf_collection = TextCollection(tfidf_list)
    # Here we add the tf_idf for each ngram in each document    
    for _, tscores in doc_ngrams_scores.items():
        for term, scores in tscores.items():
            tfidf_value = scores[FREQ] * log(n_texts / tfidf_dict[term])
            scores.update({TFIDF: tfidf_value, N: ngram})

    return doc_ngrams_scores


# def get_nltk_ngrams(list_documents, ngram=3, min_tok_len=3, min_freq=4,
#                               k=50, verbose=False):
#     """
#     Find trigrams using [Bi][Tri]gramCollocationFinder from the given
#     document tokens list_documents.
#     Returns a dict of dicts with the text name as key and
#     its value (a dict) with ngrams as keys and a dict as value, 
#     with each measure and its values:
#      {"term1": {"FREQ":3000, "PMI":0.343}, "term2": {"FREQ":3000, "PMI":0.3422}, ...} 
#         
#     """
#     
#     
#     from nltk import TrigramAssocMeasures, TrigramCollocationFinder, \
#                      BigramAssocMeasures, BigramCollocationFinder
#     
#     from collections import defaultdict
#     
#     
#     tfidf_list = []
#     ngrams_scores = defaultdict(dict)
#     doc_ngrams_scores = {}
#     # Determine if we use tri or bi grams
#     assoc_measures = {2: BigramAssocMeasures, 3: TrigramAssocMeasures}
#     collocation_finder = {2: BigramCollocationFinder, 3:TrigramCollocationFinder}
#     
#     # Determine what kind of measure we will use, depending on the config file
#     measure_dict = {LIKELIHOOD: assoc_measures[ngram].likelihood_ratio,
#                FREQ: assoc_measures[ngram].raw_freq,
#                PMI:assoc_measures[ngram].pmi,
#                CHI_SQUARE: assoc_measures[ngram].chi_sq,
#                }
#     
#     
#     for d in list_documents._texts:
#         ngrams_scores = defaultdict(dict)
#         # Find ngrams 
#         print "Finding %d-grams for %s..." % (ngram, d.name)
#         tcf = collocation_finder[ngram].from_words(d._tokens)  
#         
#         # Create a TextCollection to  found ngrams to then calculate  tfidfs
#         
#         ngram_doc = ["_".join(tm) for tm in tcf.ngram_fd.keys()]   
#         tfidf_list.append(nltk.Text(ngram_doc, name=d.name))
#         
#         # Filter ngrams according to minimum frequency, length of words in the ngram, 
#         # and stopwords in the ngram
#         tcf.apply_freq_filter(min_freq)
#         tcf.apply_word_filter(lambda w: len(w) < min_tok_len) 
#         if config_bool_stopwords:
#             tcf.apply_word_filter(lambda w: w in set(fr_stopwords))
#         
#         # Calculate tscores for the ngrams        
#         for measure, func in measure_dict.items():
#             scored_ngrams = list(tcf._score_ngrams(func))[:k]
#             for ng, value in scored_ngrams:
#                 ngrams_scores[ng][measure] = value
#     #         print_ngrams(best_k, measure)   
#         
#         doc_ngrams_scores[d.name] = ngrams_scores
#     tfidf_collection = TextCollection(tfidf_list)
#     # Here we add the tf_idf for each ngram in each document    
#     for doc, tscores in doc_ngrams_scores.items():        
#         for term, scores in tscores.items():
#             tfidf_value = scores[FREQ] * tfidf_collection.idf("_".join(term))
#             scores.update({TFIDF:tfidf_value, N:ngram})
#             
#       
#     return  doc_ngrams_scores


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


# def get_big_ngrams(list_documents, ngram=4, k=40, min_freq=2, min_tok_len=2):
#     from collections import defaultdict
#     
#     doc_ngrams_scores = defaultdict(dict)
#     list_doc_tokens = [d._tokens for d in list_documents._texts ]
#     texts_tokens = dict(zip([tx.name for tx in list_documents._texts], list_doc_tokens))
#     tfidf_texts = []
#     for doc in list_documents._texts:
#         text = doc.name
#         tokens = doc._tokens
#     
#         print "Finding %d-grams for %s..." % (ngram, text)
#         ngrams = nltk.util.ngrams(tokens, ngram, pad_right=True)
#         dict_sorted = dict(Counter(ngrams))
#         sorted_ngrams = sort_dict(dict_sorted, by_key=False)
#         tfidf_texts.append(nltk.Text(["_".join(tm) for tm in dict_sorted.keys() if not None in tm]))
#         
#         # 1st filter remove not so frequent ngrams
#         filtered_ngrams = [(term, float(freq) / len(ngrams)) 
#                            for term, freq in sorted_ngrams if freq > min_freq]
#         
#         # 2nd and 3rd filter Remove ngrams with certain words and with tokens smaller than  min_tok_len
#         filtered_ngrams2 = []
#         for n in filtered_ngrams:
#             if config_bool_stopwords:
#                 long_words = [1 for w in n[0] if len(w) >= min_tok_len
#                                 and w not in fr_stopwords ]
#     
#             else:
#                 long_words = [1 for w in n[0] if len(w) >= min_tok_len  ]
#             
#             if len(long_words) == len(n[0]):          
#                 filtered_ngrams2.append(n)
#         
#         # We keep only the top-k and save the results in a dictionary
#         best_k = filtered_ngrams2[:k]
#         for ngrs, vals in best_k:
#             temp_dict = {ngrs:{FREQ:vals, N:ngram}}
#         doc_ngrams_scores[text] = temp_dict
#     
#     # We calculate tfidf after we get the info
#     tfidf_collection = nltk.TextCollection(tfidf_texts)
#     for doc, tscores in doc_ngrams_scores.items():        
#         for term, scores in tscores.items():
#             tfidf_value = scores[FREQ] * tfidf_collection.idf("_".join(term))
#             scores.update({TFIDF:tfidf_value})
# 
# 
#         
#     
# #         print_ngrams(best_k, "frequence") 
#     return doc_ngrams_scores



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


def make_tables(scored_ngrams, results_folder="sorties/"):
    sep = ","
    #     scores = scored_ngrams.values()[0].values()[0].keys()
    scores = [N, FREQ, TFIDF, PMI, OUR_T_TEST, T_TEST, CONCORDANCE]
    column_headers = "TERM" + sep + sep.join(scores) + "\n"
    for text, tscores in scored_ngrams.items():

        path = results_folder + "RESULT_" + text.encode("latin-1")[:-4] + ".csv"
        fileo = open(path, "w")
        fileo.write(column_headers)

        for term, scores_dic in tscores.items():
            line_string = []
            line_string.append(" ".join(term).decode("latin-1"))
            for col in scores:
                if scores_dic.has_key(col):
                    line_string.append(scores_dic[col])
                else:
                    line_string.append('NA')
            line_string = sep.join([unicode(v) for v in line_string])
            fileo.write(line_string.encode("latin-1") + "\n")
        fileo.close()
        pass

    pass


def main():
    # Get text from folder or file
    # TODO Change the folder corpus to the upper level!
    import sys
    sys.path.insert("../")
    texts = get_texts(config_path)
    if not texts:
        print "No texts found"
        return
    # Dictionary that will hold all the ngrams and their values, for each measure (dict of dicts)
    scored_ngrams = {}
    # Create a list of Document objects with the texts. Pretreat them also.
    list_documents = TextCollection([Document(text, stem=config_stem, name=label)
                                     for label, text in texts.items()][:])

    global config_ngram
    if config_ngram == 0:
        config_ngram = 1

    #########################################N GRAM EXTRACTION #################################################

    # Now do the ngram extraction
    """
    We have here two possibilities. If n <= 3, we can use NLTK methods and measures (frequency, PMI, likelihood, etc.).
    If n > 3, we find the ngrams and then count them, giving the frequency as the only "quality" measure for the ngrams found.
    """


    #     unigrams = get_unigrams(list_documents)
    #     scored_ngrams = unigrams

    for ng in range(2, config_ngram + 1):
        ngrams = get_any_ngrams(list_documents, ngram=ng, k=config_top_k,
                                min_tok_len=config_min_tok_len)
        scored_ngrams = update_dict_values(scored_ngrams, ngrams)

    scored_ngrams = update_dict_values(scored_ngrams, get_concordances(list_documents, scored_ngrams))
    make_tables(scored_ngrams)
    return


#     if config_ngram > 1:
#         temp_ngram = 3 if config_ngram >= 3 else 2
#         for n in range(2, temp_ngram + 1):
#             ngrams = get_nltk_ngrams(list_documents, ngram=n, k=config_top_k,
#                                      min_tok_len=config_min_tok_len)
#             # we add the found ngrams to the main dict with ngrams for each text
#             scored_ngrams = update_dict_values(scored_ngrams, ngrams)
# #          
#     if config_ngram > 3:
#         for n in range(4, config_ngram + 1):
#             ngrams = get_big_ngrams(list_documents, ngram=n, k=config_top_k,
#                                     min_tok_len=config_min_tok_len)
#             scored_ngrams = update_dict_values(scored_ngrams, ngrams)
#     
#     scored_ngrams = update_dict_values(scored_ngrams, get_concordances(list_documents, scored_ngrams))
#     
#     ############################### ALL INFORMATION IS CALCULATED, LET's PRINT IT IN TABLES (CSV) files ###################
#     
#     make_tables(scored_ngrams)
#     pass

if __name__ == '__main__':
    from datetime import datetime

    start_time = datetime.now()
    #     cProfile.run('main()')
    main()
    print(datetime.now() - start_time)
