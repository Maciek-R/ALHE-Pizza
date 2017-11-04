import networkx as nx
import matplotlib.pyplot as plt
import csv
from graph_constants import *

class Graph:
    def __init__(self, path):
        self.edges = self.readEdgesFromFile(path)
        self.labels = None

    def readEdgesFromFile(self, path):
        with open(path, 'rb') as csvfile:
            spamreader = csv.reader(csvfile)
            return [(int(x),int(y)) for x,y in spamreader]

    def draw_graph(self):

        G=nx.Graph()

        for edge in self.edges:
            G.add_edge(edge[0], edge[1])

        #default layout
        graph_pos=nx.shell_layout(G)
        # draw graph
        nx.draw_networkx_nodes(G,graph_pos,node_size=size,
                               alpha=transparency, node_color=color)
        nx.draw_networkx_edges(G,graph_pos,width=tickness,
                               alpha=transparency,edge_color=color)
        nx.draw_networkx_labels(G, graph_pos,font_size=text_size,
                                font_family=text_font)

        if self.labels is None:
            self.labels = range(len(self.edges))

        edge_labels = dict(zip(self.edges, self.labels))
        nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels,
                                     label_pos=edge_text_pos)
        plt.show()

#labels = map(chr, range(65, 65+len(graph)))

g = Graph('graph.csv')
g.draw_graph()
#g.readEdgesFromFile('graph.csv')
