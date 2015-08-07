# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

from corpus import Corpus
from graph_mining import GraphMining
import text_mining
import plotting
import drawing
import miscellaneous as misc

text_analytics = False
graph_analytics = False

# Update data and load the complete corpus
corpus = Corpus(False)
corpus.print_article('18')

if text_analytics:
    print 'Complete corpus'
    corpus.pretty_print()
    # Extract latent topics
    num_topics = 8
    for i in range(2004, 2016):
        # Load sub-corpus
        current_corpus = Corpus(False, title_lang='fr', year_a=i, year_b=i+1)
        print i, 'corpus'
        current_corpus.pretty_print()
        # Latent Dirichlet Allocation
        titles = current_corpus.title_list()
        lda_topics = text_mining.train_lda(titles, num_topics)
        print 'LDA'
        text_mining.print_topics(lda_topics)
        # Latent Semantic Analysis
        lsi_topics = text_mining.perform_lsi(titles, num_topics)
        print 'LSI'
        text_mining.print_topics(lsi_topics)
        print ''

if graph_analytics:
    generate_plots = True
    if generate_plots:
        mode = ''
        graphs = []
        while mode != 'stop':
            year = []
            authors = []
            density = []
            average_clustering = []
            connected_components = []
            for i in range(2004, 2016):
                year.append(i)
                if mode == '(cumulative)':
                    if i == 2004:
                        graph = graphs[0]
                    else:
                        graph.merge(graphs[i-2004])
                else:
                    current_corpus = Corpus(False, title_lang='fr', year_a=i, year_b=i+1)
                    graph = GraphMining(current_corpus.collaboration_graph(str(i)+mode))
                    graphs.append(graph)
                graph.print_basic_properties()
                authors.append(graph.number_of_nodes())
                density.append(graph.degree_analysis(plot=True))
                average_clustering.append(graph.average_clustering_coefficient())
                connected_components.append(len(graph.connected_components()))
                page_rank = graph.page_rank()
                print 'Top 10 collaborative people (Page Rank)', misc.to_simple_ranking(page_rank[:10])
                k_core = graph.k_core_decomposition()
                print 'Top 10 collaborative people (K-core)', misc.to_simple_ranking(k_core[:10])
                print ''
            plotting.scatter_plot(data_x=year,
                                  data_y=authors,
                                  plot_name='Number of distinct authors vs. time '+mode,
                                  file_path='output/plots/number_authors_vs_time'+mode+'.png')
            plotting.scatter_plot(data_x=year,
                                  data_y=average_clustering,
                                  plot_name='Clustering coefficient vs. time '+mode,
                                  file_path='output/plots/clustering_coefficient_vs_time'+mode+'.png')
            plotting.scatter_plot(data_x=year,
                                  data_y=density,
                                  plot_name='Density vs. time '+mode,
                                  file_path='output/plots/density_vs_time'+mode+'.png')
            plotting.scatter_plot(data_x=year,
                                  data_y=connected_components,
                                  plot_name='Number of connected components vs. time '+mode,
                                  file_path='output/plots/connected_components_vs_time'+mode+'.png')
            if mode == '':
                mode = '(cumulative)'
            else:
                mode = 'stop'
