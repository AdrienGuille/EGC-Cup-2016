import networkx as nx
import matplotlib.pyplot as plt
import codecs

def draw_graph(graph, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3, node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1, edge_text_pos=0.3,
               text_font='sans-serif', save=True, filename=None):

    edge_labels=dict([((u,v,),d['weight']) for u,v,d in graph.edges(data=True)])
    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(graph)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(graph)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(graph)
    elif graph_layout == 'circular':
        graph_pos=nx.circular_layout(graph)
    else:
        graph_pos=nx.shell_layout(graph)

    # draw graph
    nx.draw_networkx_nodes(graph, graph_pos, node_size=node_size, alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(graph, graph_pos, width=edge_tickness, alpha=edge_alpha, edge_color=edge_color)
    nx.draw_networkx_labels(graph, graph_pos, font_size=node_text_size, font_family=text_font)
    nx.draw_networkx_edge_labels(graph, graph_pos, edge_labels=edge_labels, label_pos=edge_text_pos)

    # show graph
    if save == True:
        plt.savefig(filename, dpi=1000)
    plt.show()

univ_map = {}
def readCSV(filename, encoding='latin-1'):
    graph = nx.Graph()
    idx = 0
    with codecs.open(filename, 'r', encoding=encoding) as csvfile:
        for line in csvfile:
            weight = int(line.split(' ')[2])
            affiliation1 = line.split(' ')[0].replace('@', '')
            affiliation2 = line.split(' ')[1].replace('@', '')
            if univ_map.get(affiliation1, -1) == -1:
                univ_map[affiliation1] = idx
                idx += 1
            if univ_map.get(affiliation2, -1) == -1:
                univ_map[affiliation2] = idx
                idx += 1
            graph.add_edges_from([(univ_map[affiliation1], univ_map[affiliation2])], weight=weight)
    return graph


# graph, labels = readCSV('graph.txt', encoding='utf-8', k=3)
# print graph
# G = nx.Graph()
# G.add_edges_from(graph)
# nx.draw(G)
# plt.show()
# draw_graph(graph, labels, graph_layout = 'spectral')


graph = readCSV('colab_graf.txt', encoding='utf-8')
#remove nodes with 1 edge
outdeg = graph.degree()
# to_remove = [n for n in outdeg if outdeg[n] <= 1]
to_keep = [n for n in outdeg if outdeg[n] >= 13]
g = graph.subgraph(to_keep)
# for n in outdeg:
#     print outdeg[n]
# graph.remove_nodes_from(to_remove)
for elem in univ_map:
    print univ_map[elem], elem
draw_graph(g, node_size=1600, graph_layout='shell', save=True, filename='graph1.png')
draw_graph(graph, node_size=1600, graph_layout='random', save=True, filename='graph2.png')