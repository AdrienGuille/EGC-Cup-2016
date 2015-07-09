# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import corpus
import graph_mining
import text_mining
import plotting

# Load articles from the original .txt file and serialize 3 corpora:
# (i) French articles, (ii) English articles, (iii) all articles
#
# french_article_corpus = corpus.load('input/RNTI_articles_export.txt', 2004, 2015, 'fr')
# corpus.serialize(french_article_corpus, 'output/french_articles.pickle')
# english_article_corpus = corpus.load('input/RNTI_articles_export.txt', 2004, 2015, 'en')
# corpus.serialize(english_article_corpus, 'output/english_articles.pickle')
# complete_article_corpus = corpus.load('input/RNTI_articles_export.txt', 2004, 2015)
# corpus.serialize(complete_article_corpus, 'output/all_articles.pickle')

# Deserialize corpora saved on disk
french_article_corpus = corpus.deserialize('output/french_articles.pickle')
english_article_corpus = corpus.deserialize('output/english_articles.pickle')
complete_article_corpus = corpus.deserialize('output/all_articles.pickle')

# Get French abstracts and train LDA for k = 20
print '## Text Mining'
print ' - French article corpus'
latent_topics = text_mining.train_lda(corpus.abstract_list(french_article_corpus), 20)
text_mining.print_topics(latent_topics)
print ' - English article corpus'
latent_topics = text_mining.train_lda(corpus.abstract_list(english_article_corpus), 20)
text_mining.print_topics(latent_topics)

# Extract the collaboration graph for all the articles and compute the k-core decomposition
print '## Graph Mining'
global_collaboration_graph = corpus.collaboration_graph(complete_article_corpus, 'global_collaboration_graph')
graph_mining.analyze_collaboration_graph(global_collaboration_graph)
french_collaboration_graph = corpus.collaboration_graph(french_article_corpus, 'french_collaboration_graph')
graph_mining.analyze_collaboration_graph(french_collaboration_graph)


# Compute basic metrics on the collaboration graph for each year from 2004 until 2014
average_clustering_x = []
average_clustering_y = []
for i in range(2004, 2015):
    article_corpus = corpus.load('input/RNTI_articles_export.txt', i, i+1)
    collaboration_graph = corpus.collaboration_graph(article_corpus, 'collaboration_graph ('+str(i)+')')
    graph_mining.degree_analysis(collaboration_graph)
    average_clustering_x.append(i)
    average_clustering_y.append(graph_mining.average_clustering_coefficient(collaboration_graph))
plotting.scatter_plot(data_x=average_clustering_x,
                      data_y=average_clustering_y,
                      plot_name='Clustering coefficient vs. time',
                      file_path='output/clustering_coefficient_vs_time.png')