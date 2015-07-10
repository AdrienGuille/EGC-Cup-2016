# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import networkx as nx
import plotting
import community

def merge(graph1, graph2):
    graph = nx.Graph(name=graph1.name+'+'+graph2.name)
    graph.add_nodes_from(graph1)
    graph.add_nodes_from(graph2)
    graph.add_edges_from(graph1.edges())
    graph.add_edges_from(graph2.edges())
    return graph

def draw(graph):
    nx.draw_graphviz(graph, name=graph.name)

def print_basic_properties(graph):
    print nx.number_of_nodes(graph), 'distinct authors'
    print nx.number_of_edges(graph), 'distinct collaborations'
    print 2*nx.number_of_edges(graph)/nx.number_of_nodes(graph), 'average degree'

def degree_analysis(graph):
    degree_sequence = sorted(nx.degree(graph).values(), reverse=True)
    plotting.scatter_plot(data_y=degree_sequence,
                          plot_name='Degree distribution ('+graph.name+')',
                          file_path='output/plots/degree_distribution('+graph.name+').png',
                          ymax=100,
                          xmax=1000,
                          loglog=True)
    return [degree_sequence, nx.density(graph)]

def average_clustering_coefficient(graph):
    return nx.average_clustering(graph)

def page_rank(graph):
    node_dictionary = nx.pagerank(graph, alpha=0.85, max_iter=300)
    return sorted(node_dictionary.items(), key=lambda x: x[1], reverse=True)

def k_core_decomposition(graph):
    k_core = nx.core_number(graph)
    return sorted(k_core.items(), key=lambda x: x[1], reverse=True)

def louvain_modularity(graph):
    return community.best_partition(graph)
