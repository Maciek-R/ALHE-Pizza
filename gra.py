import networkx as nx
import matplotlib.pyplot as plt
from graph_constants import *

def draw_graph(graph, labels=None):

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=size,
                           alpha=transparency, node_color=color)
    nx.draw_networkx_edges(G,graph_pos,width=tickness,
                           alpha=transparency,edge_color=color)
    nx.draw_networkx_labels(G, graph_pos,font_size=text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels,
                                 label_pos=edge_text_pos)

    # show graph
    plt.show()

graph = [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9),
         (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]

# you may name your edge labels
labels = map(chr, range(65, 65+len(graph)))

draw_graph(graph)
