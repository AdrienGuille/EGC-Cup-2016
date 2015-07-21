# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import networkx as nx
import plotting
import community
import drawing

def merge(graph1, graph2):
    graph = nx.Graph(name=graph1.name+'+'+graph2.name)
    graph.add_nodes_from(graph1)
    graph.add_nodes_from(graph2)
    graph.add_edges_from(graph1.edges())
    graph.add_edges_from(graph2.edges())
    return graph

def draw(graph):
    nx.draw_graphviz(graph, name=graph.name)

def connected_components(graph):
    return list(nx.connected_component_subgraphs(graph))

def patterns(graph):
    graphs = connected_components(graph)
    pattern_dict = {}
    pattern_count = {}
    for i in range(0, len(graphs)):
        pattern = str(nx.degree_histogram(graphs[i])).strip('[]')
        if pattern_dict.get(pattern):
            graph_list = pattern_dict.get(pattern)
            count = pattern_count.get(pattern)
            if nx.is_isomorphic(graphs[i], graphs[graph_list[0]]):
                graph_list.append(i)
                pattern_dict[pattern] = graph_list
                pattern_count[pattern] = count + 1
        else:
            pattern_dict[pattern] = [i]
            pattern_count[pattern] = 1
    print sorted(pattern_count.items(), key=lambda x: x[1], reverse=True)
    print pattern_dict

def print_basic_properties(graph):
    print 'Name:', graph.name
    print 'Order:', nx.number_of_nodes(graph)
    print 'Number of edges:', nx.number_of_edges(graph)
    print 'Average degree:', 2*nx.number_of_edges(graph)/nx.number_of_nodes(graph)
    print 'Max degree:', sorted(nx.degree(graph).values(), reverse=True)[0]
    print 'Number of connected components:', len(connected_components(graph))

def degree_analysis(graph, plot=False):
    degree_sequence = sorted(nx.degree(graph).values(), reverse=True)
    if plot:
        plotting.scatter_plot(data_y=degree_sequence,
                              plot_name='Degree distribution ('+graph.name+')',
                              file_path='output/plots/degree_distribution('+graph.name+').png',
                              ymax=100,
                              xmax=1000,
                              loglog=True)
    return nx.density(graph)

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
