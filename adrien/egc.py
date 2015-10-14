# coding: utf-8
import utils
import networkx as nx
import numpy as np
import csv
import collections

__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

print'\n#EGC 2016 Cup'

print'\n##Data'

print '\n###Data provided by the organizers'
with open('input/RNTI_articles_export_original.txt', 'rb') as csv_file:
    reader = csv.reader(csv_file, delimiter='\t')
    nb_articles_egc = 0
    missing_authors = 0
    missing_abstract = 0
    missing_year = 0
    for row in reader:
        if 'EGC' == row[1]:
            if len(row[5]) < 3:
                missing_authors += 1
            if len(row[4]) < 3:
                missing_abstract += 1
            if len(row[2]) < 3:
                missing_year += 1
            nb_articles_egc += 1
    print 'Number of articles presented at the EGC conference: %i' % nb_articles_egc
    print 'Number of articles without abstract: %i' % missing_abstract

print '\n###Cleaned up data'
with open('input/RNTI_articles_export_prepared.csv', 'rb') as csv_file:
    reader = csv.reader(csv_file, delimiter='\t')
    nb_articles = 0
    lang_abs = []
    lang_title = []
    year = []
    missing_abstract = 0
    next(reader)
    for row in reader:
        if len(row[4]) < 4:
            missing_abstract += 1
        year.append(row[2])
        lang_abs.append(row[10])
        lang_title.append(row[9])
        nb_articles += 1
    print 'Number of well-formatted articles: %i  ' % nb_articles
    print 'Number of articles per year:', collections.Counter(year), '  '
    print 'Number of articles per language detected from the abstract:', collections.Counter(lang_abs), '  '

print'\n#Topical structure of the EGC society'

print '\n##Prepared corpus and topic model'

topic_model = utils.load_topic_model('nmf_15topics_egc.pickle')
print 'corpus size: %i  ' % topic_model.corpus.size
print 'vocabulary size: %i  ' % len(topic_model.corpus.vocabulary)
print 'Topic model: NMF  '
print 'number of topics: %i  ' % topic_model.nb_topics

print '\n##Topics'

print '\n###Most relevant words for each topic -> LaTeX table'
for topic_id in range(topic_model.nb_topics):
    word_list = []
    for weighted_word in topic_model.top_words(topic_id, 8):
        word_list.append(weighted_word[0])
    print 'topic %i & %s\\\\  ' % (topic_id, ', '.join(word_list))

print '\n###Overall frequency of each topic -> Pgfplot table'
frequency = topic_model.topics_frequency()
print 'topic_id\toverall_frequency  '
for topic_id in range(topic_model.nb_topics):
    print '%i\t%f  ' % (topic_id, frequency[topic_id])

topic_associations = topic_model.documents_per_topic()

print '\n##Fading topic: topic #2 (association rule mining)'

print '\n###Frequency vs. year -> Pgfplot table'
print 'year\ttopic_frequency  '
for i in range(2004, 2016):
    print '%i\t%f  ' % (i, topic_model.topic_frequency(2, date=i))

print '\n##Emerging topic: topic #0 (social network analysis and mining)'

print '\n###Frequency vs. year -> Pgfplot table'
print 'year\ttopic_frequency  '
for i in range(2004, 2016):
    print '%i\t%f  ' % (i, topic_model.topic_frequency(0, date=i))

print '\n##Mostly industrial topic: topic #8 (variable and model selection)'

print '\n###Articles per institution -> Pgfplot table'
print 'institution_name\tinstitution_id\tnb_articles  '
id_to_name = []
for institution, nb_articles in topic_model.affiliation_repartition(8):
    print '%s\t%i\t%i  ' % (institution, len(id_to_name), nb_articles)
    id_to_name.append(institution)
print 'labels: %s  ' % ','.join(id_to_name)

print '\n###Titles of the articles related to topic #8 and involving Orange'
count = 0
for doc_id in topic_associations[8]:
    affiliations = topic_model.corpus.affiliations(doc_id)
    if '@orange.com' in affiliations or '@orange-ftgroup.com' in affiliations or '@orange.com' in affiliations:
        print '%i\t%s  ' % (count, topic_model.corpus.short_content(doc_id))
        count += 1

print '\n##Highly collaborative topic: topic #4 (pattern mining)'

print '\n###Order of the collaboration network and size of the largest component per topic -> Pgfplot table'
print 'topic_id\tnetwork_order\tlargest_cc_size\taverage_cc_size  '
for topic_id in range(topic_model.nb_topics):
    graph = topic_model.corpus.collaboration_network(topic_associations[topic_id], nx_format=True)
    graph_order = len(nx.nodes(graph))
    connected_components = sorted(nx.connected_component_subgraphs(graph), key=len, reverse=True)
    largest_connected_component = connected_components[0]
    largest_connected_component_size = len(nx.nodes(largest_connected_component))
    size = []
    for i in range(len(connected_components)):
        size.append(len(nx.nodes(connected_components[i])))
    mean_size = np.array(size).mean(axis=0)
    print '%i\t%i\t%i\t%f  ' % (topic_id, graph_order, largest_connected_component_size, mean_size)

size = []
normalized_size = []
cc_density = []
print '\n###Normalized size of the largest component in the collaboration network per topic -> Pgfplot table'
print 'topic_id\tnormalized_size\tcc_density  '
for topic_id in range(topic_model.nb_topics):
    graph = topic_model.corpus.collaboration_network(topic_associations[topic_id], nx_format=True)
    graph_order = len(nx.nodes(graph))
    connected_components = sorted(nx.connected_component_subgraphs(graph), key=len, reverse=True)
    largest_connected_component = connected_components[0]
    size.append(len(nx.nodes(largest_connected_component)))
    largest_connected_component_norm_size = float(len(nx.nodes(largest_connected_component)))/float(graph_order)
    nx.write_gexf(graph, 'gexf/'+str(topic_id)+'.gexf')
    normalized_size.append(largest_connected_component_norm_size)
    cc_density.append(nx.density(largest_connected_component))
    print '%i\t%f\t%f  ' % (topic_id, largest_connected_component_norm_size, nx.density(largest_connected_component))

mean_size = np.array(size).mean(axis=0)
mean_norm_size = np.array(normalized_size).mean(axis=0)
mean_density = np.array(cc_density).mean(axis=0)
print '\nMean largest c.c. size: %f, mean normalized size: %f, mean largest c.c. density: %f' % (mean_size, mean_norm_size, mean_density)

print '\n###Global collaboration graph'
global_graph = topic_model.corpus.collaboration_network(range(topic_model.corpus.size), nx_format=True)
global_graph_order = len(nx.nodes(global_graph))
connected_components = sorted(nx.connected_component_subgraphs(global_graph), key=len, reverse=True)
largest_connected_component = connected_components[0]
largest_connected_component_size = len(nx.nodes(largest_connected_component))
print 'order: %i, largest connected component: %i  ' % (global_graph_order, largest_connected_component_size)

print'\n#Collaborative structure of the EGC society'

print'\n##Evolution of the density of the collaboration network'

cumulative_graph = nx.Graph()
print 'year\tyear_density\tcumulative_density  '
for year in range(2004, 2016):
    year_graph = topic_model.corpus.collaboration_network(topic_model.corpus.doc_ids(year), nx_format=True)
    cumulative_graph.add_nodes_from(nx.nodes(year_graph))
    cumulative_graph.add_edges_from(nx.edges(year_graph))
    year_density = nx.density(year_graph)
    cumulative_density = nx.density(cumulative_graph)
    print '%i\t%f\t%f  ' % (year, year_density, cumulative_density)

print'\n##Evolution of the average clustering coefficient of the collaboration network'

cumulative_graph = nx.Graph()
print 'year\tyear_clust_coeff\tcumulative_clust_coeff  '
for year in range(2004, 2016):
    year_graph = topic_model.corpus.collaboration_network(topic_model.corpus.doc_ids(year), nx_format=True)
    cumulative_graph.add_nodes_from(nx.nodes(year_graph))
    cumulative_graph.add_edges_from(nx.edges(year_graph))
    year_clust_coeff = nx.average_clustering(year_graph)
    cumulative_clust_coeff = nx.average_clustering(cumulative_graph)
    print '%i\t%f\t%f  ' % (year, year_clust_coeff, cumulative_clust_coeff)
