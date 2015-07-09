# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import networkx as nx
import plotting

def merge(graph1, graph2):
    return nx.compose(graph1, graph2)

def print_basic_properties(graph):
    print nx.number_of_nodes(graph), 'distinct authors'
    print nx.number_of_edges(graph), 'distinct collaborations'
    print 2*nx.number_of_edges(graph)/nx.number_of_nodes(graph), 'average degree'

def degree_analysis(graph):
    degree_sequence = sorted(nx.degree(graph).values(), reverse=True)
    plotting.scatter_plot(data_y=degree_sequence,
                          plot_name='Degree distribution ('+graph.name+')',
                          file_path='output/degree_distribution('+graph.name+').png',
                          ymax=100,
                          xmax=1000,
                          loglog=True)
    return [degree_sequence, nx.density(graph)]

def average_clustering_coefficient(graph):
    return nx.average_clustering(graph)

def advanced_metrics(graph):
    print ' - Graph: ', graph.name
    if nx.is_connected(graph):
        print 'diameter', nx.diameter(graph)
    else:
        print 'disconnected graph'
    k_core = nx.core_number(graph)
    print 'k-core decomposition: ', sorted(k_core.items(), key=lambda x: x[1], reverse=True)
