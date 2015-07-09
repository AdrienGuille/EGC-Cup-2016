# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import networkx as nx
import matplotlib.pyplot as plt


def analyze_collaboration_graph(graph):
    if nx.is_connected(graph):
        print 'diameter', nx.diameter(graph)
    else:
        print 'disconnected graph'
    degree_sequence = sorted(nx.degree(graph).values(), reverse=True)
    print 'max degree:', max(degree_sequence)
    plt.loglog(degree_sequence,'b-',marker='o')
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")
    plt.savefig('output/degree_histogram('+graph.name+').png')
    print 'Degree distribution plot saved in: output/degree_distribution(', graph.name, ').png'
    k_core = nx.core_number(graph)
    print 'k-core decomposition: ', sorted(k_core.items(), key=lambda x: x[1], reverse=True)
    print 'estimated average clustering coefficient: ', nx.average_clustering(graph)