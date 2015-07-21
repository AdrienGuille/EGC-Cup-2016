# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import corpus
import graph_mining
import text_mining
import plotting
import drawing


# Load articles from the original .txt file and serialize corpora:

"""
for i in range(2004, 2015):
    article_corpus = corpus.load('input/RNTI_articles_export_fixed1347_ids.txt', i, i+1, 'fr')
    corpus.serialize(article_corpus, 'output/corpora/french_articles_'+str(i)+'.pickle')
    print i
    corpus.pretty_print(article_corpus)
    print ''
french_article_corpus = corpus.load('input/RNTI_articles_export_fixed1347_ids.txt', 2004, 2015, 'fr')
corpus.serialize(french_article_corpus, 'output/corpora/french_articles.pickle')
english_article_corpus = corpus.load('input/RNTI_articles_export_fixed1347_ids.txt', 2004, 2015, 'en')
corpus.serialize(english_article_corpus, 'output/corpora/english_articles.pickle')
complete_article_corpus = corpus.load('input/RNTI_articles_export_fixed1347_ids.txt', 2004, 2015)
corpus.serialize(complete_article_corpus, 'output/corpora/all_articles.pickle')

# Deserialize corpora saved on disk
french_article_corpus = corpus.deserialize('output/corpora/french_articles.pickle')
english_article_corpus = corpus.deserialize('output/corpora/english_articles.pickle')
complete_article_corpus = corpus.deserialize('output/corpora/all_articles.pickle')

# Extract latent topics from the 2014 articles
print '## Text Mining'
print ' - French article corpus'
french_articles_2014 = corpus.deserialize('output/corpora/french_articles_2014.pickle')
lda_topics = text_mining.train_lda(corpus.title_list(french_articles_2014), 6)
print 'LDA'
text_mining.print_topics(lda_topics)
lsi_topics = text_mining.perform_lsi(corpus.title_list(french_articles_2014), 6)
print 'LSI'
text_mining.print_topics(lsi_topics)

# Analyze the evolution of collaborations from 2004 until 2014
print '## Graph Mining'
print ' - Collaborations by year'
year = []
authors = []
density = []
average_clustering = []
graphs = []
for i in range(2004, 2015):
    print i
    article_corpus = corpus.deserialize('output/corpora/french_articles_'+str(i)+'.pickle')
    collaboration_graph = corpus.collaboration_graph(article_corpus, str(i))
    authors.append(collaboration_graph.number_of_nodes())
    graph_mining.print_basic_properties(collaboration_graph)
    graphs.append(collaboration_graph)
    graph_mining.draw(collaboration_graph)
    degree_analysis = graph_mining.degree_analysis(collaboration_graph)
    print 'max degree:', max(degree_analysis[0])
    density.append(degree_analysis[1])
    average_clustering.append(graph_mining.average_clustering_coefficient(collaboration_graph))
    page_rank = graph_mining.page_rank(collaboration_graph)
    print page_rank[:10]
    k_core = graph_mining.k_core_decomposition(collaboration_graph)
    print k_core[:10]
    year.append(i)
    print ''
plotting.scatter_plot(data_x=year,
                      data_y=authors,
                      plot_name='Number of distinct authors vs. time',
                      file_path='output/plots/number_authors_vs_time.png')
plotting.scatter_plot(data_x=year,
                      data_y=average_clustering,
                      plot_name='Clustering coefficient vs. time',
                      file_path='output/plots/clustering_coefficient_vs_time.png',
                      linear_regression=True)
plotting.scatter_plot(data_x=year,
                      data_y=density,
                      plot_name='Density vs. time',
                      file_path='output/plots/density_vs_time.png',
                      linear_regression=True)
print ' - Accumulating collaborations through years'

cumulative_graph = graphs[0]
authors = []
density = []
average_clustering = []
connected_components = []
for i in range(0, len(graphs)):
    cumulative_graph = graph_mining.merge(cumulative_graph, graphs[i])
    authors.append(cumulative_graph.number_of_nodes())
    connected_components.append(len(graph_mining.connected_components(cumulative_graph)))
    graph_mining.print_basic_properties(cumulative_graph)
    degree_analysis = graph_mining.degree_analysis(cumulative_graph)
    print 'max degree:', max(degree_analysis[0])
    density.append(degree_analysis[1])
    average_clustering.append(graph_mining.average_clustering_coefficient(cumulative_graph))
    page_rank = graph_mining.page_rank(cumulative_graph)
    print page_rank[:10]
    k_core = graph_mining.k_core_decomposition(cumulative_graph)
    print k_core[:10]
    # communities = graph_mining.louvain_modularity(collaboration_graph)
    # drawing.draw_graph_with_communities(collaboration_graph, communities)
    print ''
plotting.scatter_plot(data_x=year,
                      data_y=authors,
                      plot_name='Number of connected components vs. time (cumulative graph)',
                      file_path='output/plots/cumulative_connected_components_vs_time.png')
plotting.scatter_plot(data_x=year,
                      data_y=authors,
                      plot_name='Number of distinct authors vs. time (cumulative graph)',
                      file_path='output/plots/cumulative_number_authors_vs_time.png',
                      linear_regression=True)
plotting.scatter_plot(data_x=year,
                      data_y=average_clustering,
                      plot_name='Clustering coefficient vs. time (cumulative graph)',
                      file_path='output/plots/cumulative_clustering_coefficient_vs_time.png')
plotting.scatter_plot(data_x=year,
                      data_y=density,
                      plot_name='Density vs. time (cumulative graph)',
                      file_path='output/plots/cumulative_density_vs_time.png')

french_article_corpus = corpus.deserialize('output/corpora/english_articles.pickle')
corpus.pretty_print(french_article_corpus)
"""

french_2012_article_corpus = corpus.deserialize('output/corpora/french_articles_2012.pickle')
collaboration_graph = corpus.collaboration_graph(french_2012_article_corpus, 2012)
graph_mining.patterns(collaboration_graph)
