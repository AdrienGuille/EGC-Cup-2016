# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import corpus
import graph_mining
import text_mining
import plotting
import drawing
import miscellaneous

update_data = False
text_analytics = False
graph_analytics = True

if update_data:
    # Load data from the text file and serialize various corpora w.r.t language and year
    all_articles = corpus.load('input/RNTI_articles_export_fixed1347_ids.txt', 2004, 2016)
    corpus.serialize(all_articles, 'output/corpora/all_articles.pickle')
    french_articles = corpus.load('input/RNTI_articles_export_fixed1347_ids.txt', 2004, 2016, 'fr')
    corpus.serialize(french_articles, 'output/corpora/all_french_articles.pickle')
    english_articles = corpus.load('input/RNTI_articles_export_fixed1347_ids.txt', 2004, 2016, 'en')
    corpus.serialize(english_articles, 'output/corpora/all_english_articles.pickle')
    for i in range(2004, 2016):
        french_article_corpus = corpus.load('input/RNTI_articles_export_fixed1347_ids.txt', i, i+1, 'fr')
        corpus.serialize(french_article_corpus, 'output/corpora/french_articles_'+str(i)+'.pickle')
        english_article_corpus = corpus.load('input/RNTI_articles_export_fixed1347_ids.txt', i, i+1, 'en')
        corpus.serialize(english_article_corpus, 'output/corpora/english_articles_'+str(i)+'.pickle')
        french_english_article_corpus = corpus.load('input/RNTI_articles_export_fixed1347_ids.txt', i, i+1)
        corpus.serialize(french_english_article_corpus, 'output/corpora/all_articles_'+str(i)+'.pickle')

# Deserialize corpora
all_articles = corpus.deserialize('output/corpora/all_articles.pickle')
french_articles = corpus.deserialize('output/corpora/all_french_articles.pickle')
english_articles = corpus.deserialize('output/corpora/all_english_articles.pickle')
article_dict = {}
for i in range(2004, 2016):
    article_dict[str(i)] = corpus.deserialize('output/corpora/all_articles_'+str(i)+'.pickle')
french_article_dict = {}
for i in range(2004, 2016):
    french_article_dict[str(i)] = corpus.deserialize('output/corpora/french_articles_'+str(i)+'.pickle')
english_article_dict = {}
for i in range(2004, 2016):
    english_article_dict[str(i)] = corpus.deserialize('output/corpora/english_articles_'+str(i)+'.pickle')

if text_analytics:
    # Extract latent topics using LDA and LSI
    num_topics = 8
    for i in range(2004, 2016):
        lda_topics = text_mining.train_lda(corpus.title_list(french_article_dict.get(str(i))), num_topics)
        print 'LDA'
        text_mining.print_topics(lda_topics)
        lsi_topics = text_mining.perform_lsi(corpus.title_list(french_article_dict.get(str(i))), 6)
        print 'LSI'
        text_mining.print_topics(lsi_topics)

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
                        graph = graph_mining.merge(graph, graphs[i-2004])
                else:
                    graph = corpus.collaboration_graph(article_dict.get(str(i)))
                    graphs.append(graph)
                graph.name = str(i)+mode
                graph_mining.print_basic_properties(graph)
                authors.append(graph.number_of_nodes())
                density.append(graph_mining.degree_analysis(graph, plot=True))
                average_clustering.append(graph_mining.average_clustering_coefficient(graph))
                connected_components.append(len(graph_mining.connected_components(graph)))
                page_rank = graph_mining.page_rank(graph)
                print page_rank[:10]
                k_core = graph_mining.k_core_decomposition(graph)
                print k_core[:10]
                print ''
            plotting.scatter_plot(data_x=year,
                                  data_y=authors,
                                  plot_name='Number of distinct authors vs. time '+mode,
                                  file_path='output/plots/number_authors_vs_time.png'+mode+'.png')
            plotting.scatter_plot(data_x=year,
                                  data_y=average_clustering,
                                  plot_name='Clustering coefficient vs. time '+mode,
                                  file_path='output/plots/clustering_coefficient_vs_time'+mode+'.png')
            plotting.scatter_plot(data_x=year,
                                  data_y=density,
                                  plot_name='Density vs. time '+mode,
                                  file_path='output/plots/density_vs_time.png'+mode+'.png')
            plotting.scatter_plot(data_x=year,
                                  data_y=connected_components,
                                  plot_name='Number of connected components vs. time '+mode,
                                  file_path='output/plots/connected_components_vs_time.png'+mode+'.png')
            if mode == '':
                mode = '(cumulative)'
            else:
                mode = 'stop'
