# coding: utf-8
__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

import networkx as nx
import matplotlib.pyplot as plt

def draw_graph_with_communities(graph, communities):
    plt.clf()
    size = float(len(set(communities.values())))
    pos = nx.graphviz_layout(graph)
    count = 0.
    for com in set(communities.values()):
        count += 1.
        list_nodes = [nodes for nodes in communities.keys() if communities[nodes] == com]
        nx.draw_networkx_nodes(graph, pos, list_nodes, node_size=20, node_color=str(count/size))
    nx.draw_networkx_edges(graph,pos, alpha=0.5)
    plt.show()
