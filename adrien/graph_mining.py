# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import networkx as nx
import plotting
import community
import drawing


class GraphMining:

    def __init__(self, source_graph):
        self.graph = source_graph

    def merge(self, graph2):
        self.graph.name = self.graph.name+'+'+graph2.graph.name
        self.graph.add_nodes_from(graph2.graph)
        self.graph.add_edges_from(graph2.graph.edges())

    def draw(self):
        nx.draw_graphviz(self.graph, name=self.graph.name)

    def connected_components(self):
        return list(nx.connected_component_subgraphs(self.graph))

    def patterns(self):
        graphs = self.connected_components()
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

    def number_of_nodes(self):
        return self.graph.number_of_nodes()

    def print_basic_properties(self):
        print 'Name:', self.graph.name
        print 'Order:', nx.number_of_nodes(self.graph)
        print 'Number of edges:', nx.number_of_edges(self.graph)
        print 'Average degree:', 2*nx.number_of_edges(self.graph)/nx.number_of_nodes(self.graph)
        print 'Max degree:', sorted(nx.degree(self.graph).values(), reverse=True)[0]
        print 'Density:', nx.density(self.graph)
        print 'Number of connected components:', len(self.connected_components())

    def degree_analysis(self, plot=False):
        degree_sequence = sorted(nx.degree(self.graph).values(), reverse=True)
        if plot:
            plotting.scatter_plot(data_y=degree_sequence,
                                  plot_name='Degree distribution ('+self.graph.name+')',
                                  file_path='output/plots/degree_distribution('+self.graph.name+').png',
                                  ymax=100,
                                  xmax=1000,
                                  loglog=True)
        return nx.density(self.graph)

    def average_clustering_coefficient(self):
        return nx.average_clustering(self.graph)

    def page_rank(self):
        node_dictionary = nx.pagerank(self.graph, alpha=0.85, max_iter=300)
        return sorted(node_dictionary.items(), key=lambda x: x[1], reverse=True)

    def k_core_decomposition(self):
        k_core = nx.core_number(self.graph)
        return sorted(k_core.items(), key=lambda x: x[1], reverse=True)

    def louvain_modularity(self):
        return community.best_partition(self.graph)
