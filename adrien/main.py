# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import corpus
import graph_mining
import text_mining

## Load articles from the original .txt file and serialize 3 corpora: (i) French articles, (ii) English articles, (iii) all articles
# french_article_corpus = corpus.load('input/RNTI_articles_export.txt', 2004, 2015, 'fr')
# corpus.serialize(french_article_corpus, 'output/french_articles.pickle')
# english_article_corpus = corpus.load('input/RNTI_articles_export.txt', 2004, 2015, 'en')
# corpus.serialize(english_article_corpus, 'output/english_articles.pickle')
# complete_article_corpus = corpus.load('input/RNTI_articles_export.txt', 2004, 2015)
# corpus.serialize(complete_article_corpus, 'output/all_articles.pickle')

## Deserialize corpora saved on disk
french_article_corpus = corpus.deserialize('output/french_articles.pickle')
english_article_corpus = corpus.deserialize('output/english_articles.pickle')
complete_article_corpus = corpus.deserialize('output/all_articles.pickle')

# Get French abstracts and train LDA for k = 20
latent_topics = text_mining.train_lda(corpus.abstract_list(french_article_corpus), 20)
text_mining.print_topics(latent_topics)

# Extract the collaboration graph for all the articles and compute the k-core decomposition
collaboration_graph = corpus.collaboration_graph(complete_article_corpus)
graph_mining.analyze_collaboration_graph(collaboration_graph)