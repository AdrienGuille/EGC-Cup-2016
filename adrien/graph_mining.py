# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import networkx as nx


def analyze_collaboration_graph(graph):
    if nx.is_connected(graph):
        print 'diameter', nx.diameter(graph)
    else:
        print 'disconnected graph'
    k_core = nx.core_number(graph)
    print 'k-core decomposition: ', sorted(k_core.items(), key=lambda x: x[1], reverse=True)