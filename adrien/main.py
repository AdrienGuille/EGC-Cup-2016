# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import corpus
import graph_mining
import text_mining

french_article_corpus = corpus.load_corpus('input/RNTI_articles_export.txt', 2004, 2015, 'fr')
english_article_corpus = corpus.load_corpus('input/RNTI_articles_export.txt', 2004, 2015, 'en')
complete_article_corpus = corpus.load_corpus('input/RNTI_articles_export.txt', 2004, 2015)
collaboration_graph = corpus.collaboration_graph(complete_article_corpus)
graph_mining.analyze_collaboration_graph(collaboration_graph)
print 'degree(Adrien Guille): ', collaboration_graph.degree('Adrien Guille')
latent_topics = text_mining.train_lda(corpus.abstract_list(french_article_corpus), 20)
text_mining.print_topics(latent_topics)