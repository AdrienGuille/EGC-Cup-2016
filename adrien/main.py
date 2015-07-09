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
# french_article_corpus = corpus.deserialize('output/french_articles.pickle')
# english_article_corpus = corpus.deserialize('output/english_articles.pickle')
# complete_article_corpus = corpus.deserialize('output/all_articles.pickle')

# Get French abstracts and train LDA for k = 20
# print '## Text Mining'
# print ' - French article corpus'
# latent_topics = text_mining.train_lda(corpus.abstract_list(french_article_corpus), 20)
# text_mining.print_topics(latent_topics)
# print ' - English article corpus'
# latent_topics = text_mining.train_lda(corpus.abstract_list(english_article_corpus), 20)
# text_mining.print_topics(latent_topics)

# Compute basic metrics on the collaboration graph for each year from 2004 until 2014
print '## Graph Mining'
print ' - Collaborations by year'
year = []
density = []
average_clustering = []
graphs = []
for i in range(2004, 2015):
    print i
    article_corpus = corpus.load('input/RNTI_articles_export.txt', i, i+1)
    collaboration_graph = corpus.collaboration_graph(article_corpus, 'collaboration_graph ('+str(i)+')')
    graph_mining.print_basic_properties(collaboration_graph)
    graphs.append(collaboration_graph)
    degree_analysis = graph_mining.degree_analysis(collaboration_graph)
    print 'max degree:', max(degree_analysis[0])
    density.append(degree_analysis[1])
    average_clustering.append(graph_mining.average_clustering_coefficient(collaboration_graph))
    year.append(i)
    print ''
plotting.scatter_plot(data_x=year,
                      data_y=average_clustering,
                      plot_name='Clustering coefficient vs. time',
                      file_path='output/clustering_coefficient_vs_time.png')
plotting.scatter_plot(data_x=year,
                      data_y=density,
                      plot_name='Density vs. time',
                      file_path='output/density_vs_time.png')
print ' - Accumulating collaborations through years'
cumulative_graph = graphs[0]
density = []
average_clustering = []
for i in range(1,len(graphs)):
    cumulative_graph = graph_mining.merge(cumulative_graph, graphs[i])
    graph_mining.print_basic_properties(cumulative_graph)
    degree_analysis = graph_mining.degree_analysis(cumulative_graph)
    print 'max degree:', max(degree_analysis[0])
    density.append(degree_analysis[1])
    average_clustering.append(graph_mining.average_clustering_coefficient(cumulative_graph))
    print ''
plotting.scatter_plot(data_y=average_clustering,
                      plot_name='Clustering coefficient vs. time (cumulative graph)',
                      file_path='output/cumulative_clustering_coefficient_vs_time.png')
plotting.scatter_plot(data_y=density,
                      plot_name='Density vs. time (cumulative graph)',
                      file_path='output/cumulative_density_vs_time.png')