from random import randint
from Edge import *
from Node import *
WIDTH = 100
HEIGHT = 100

class GraphGenerator:

    def __init__(self, nodesNo, edgesNo):
        self.edges = []
        self.nodes = []
        self.nodesNo = nodesNo
        self.edgesNo = edgesNo

    def generate(self):
        self.__generateNodes__()
        self.__generateEdges__()


    def __generateNodes__(self):
        for x in range(self.nodesNo):
            self.nodes.append(self.__createUniqueNode__())

    def __generateEdges__(self):
        for x in range(self.edgesNo):
            self.edges.append(self.__createUniqueEdge__())

    def __takeRandomNode__(self):
        return self.nodes[randint(0, self.nodesNo-1)]

    def __createUniqueEdge__(self):
            nodeFrom = self.__takeRandomNode__()
            nodeTo = self.__takeRandomNode__()
            newEdge = Edge(nodeFrom, nodeTo)
            if nodeFrom is nodeTo or newEdge in self.edges:
                return self.__createUniqueEdge__()
            else:
                return newEdge

    def __createUniqueNode__(self):
        x = randint(0, WIDTH)
        y = randint(0, HEIGHT)
        node = Node(x, y)
        if(node in self.nodes):
            return self.__createUniqueNode__()
        else:
            return node

    def saveToFile(self, path):
        with open(path, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter = ' ', quotechar = '|', quoting=csv.QUOTE_MINIMAL)


a = GraphGenerator(10, 4)
a.generate()
