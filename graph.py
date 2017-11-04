import networkx as nx
import matplotlib.pyplot as plt
import csv
from graph_constants import *
from GraphGenerator import *
from Node import *
from Edge import *

class Graph:
    def __init__(self):
        self.edges = []
        self.nodes = []

    def generate(self, nodesNo, edgesNo):
        self.nodesNo = nodesNo
        self.edgesNo = edgesNo
        graphGenerator = GraphGenerator(nodesNo, edgesNo)
        self.edges = graphGenerator.edges
        self.nodes = graphGenerator.nodes
        self.labels = self.__createLabels__()

    def createFromFile(self, pathNodes, pathEdges):
        self.__readFromFile__(pathNodes, pathEdges)
        self.labels = self.__createLabels__()

    def __createLabels__(self):
        return map(Node.getLabel, self.nodes)


    def draw_graph(self):

        G=nx.Graph()

        for edge in self.edges:
            nodeFrom, nodeTo = edge.get()
            G.add_edge(nodeFrom.getLabel(), nodeTo.getLabel())

        #default layout
        graph_pos=nx.shell_layout(G)
        # draw graph
        nx.draw_networkx_nodes(G,graph_pos,node_size=size,
                               alpha=transparency, node_color=color)
        nx.draw_networkx_edges(G,graph_pos,width=tickness,
                               alpha=transparency,edge_color=color)
        nx.draw_networkx_labels(G, graph_pos,font_size=text_size,
                                font_family=text_font)

        #if self.labels is None:
            #self.labels = range(len(self.edges))

        print self.edges
        print self.labels
        edge_labels = dict(zip(self.edges, self.labels))
        print edge_labels
    #    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels,
        #                             label_pos=edge_text_pos)
        plt.show()

    def writeToFile(self, pathNode, pathEdges):
        self.__writeNodes__(pathNode)
        self.__writeEdges__(pathEdges)

    def __writeNodes__(self, pathNode):
        with open(pathNode, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
            for x,y in map(Node.getPosition, self.nodes):
                writer.writerow([x,y])

    def __writeEdges__(self, pathEdges):
        with open(pathEdges, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',', quotechar = ' ', quoting=csv.QUOTE_MINIMAL)
            for x,y,w in map(Edge.getAll, self.edges):
                xPos = x.getPosition()
                yPos = y.getPosition()
                writer.writerow([xPos[0], xPos[1], yPos[0], yPos[1],w])

    def __readFromFile__(self, pathNode, pathEdges):
        self.__readNodes__(pathNode)
        self.__readEdges__(pathEdges)

    def __readNodes__(self, pathNode):
        with open(pathNode, 'rb') as csvfile:
            spamreader = csv.reader(csvfile)
            self.nodes = [Node(int(x),int(y)) for x,y in spamreader]

    def __readEdges__(self, pathEdges):
        with open(pathEdges, 'rb') as csvfile:
            spamreader = csv.reader(csvfile)
            self.edges = [Edge(Node(int(n1x),int(n1y)), Node(int(n2x), int(n2y)), float(w)) for n1x,n1y,n2x,n2y,w in spamreader]

#labels = map(chr, range(65, 65+len(graph)))

g = Graph()
g.createFromFile('nodes.csv', 'edges.csv')
#for x in g.nodes:
#    print x.x,  x.y
#for x in g.edges:
#    print x.nodeFrom.x, x.nodeFrom.y, x.nodeTo.x, x.nodeTo.y, x.weight

g.draw_graph()

#g.generate(10, 20)
#g.writeToFile('nodes.csv', 'edges.csv')
#g.draw_graph()
#g.readEdgesFromFile('graph.csv')
