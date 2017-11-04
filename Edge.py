from Node import *
from random import randint

class Edge:
    def __init__(self, nodeFrom, nodeTo, weight=None):
        self.nodeFrom = nodeFrom
        self.nodeTo = nodeTo
        if(weight == None):
            self.weight = self.__getRandomWeight__()
        else:
            self.weight = weight

    def get(self):
        return self.nodeFrom, self.nodeTo

    def __getRandomWeight__(self):
        return 1 + randint() * 4

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.nodeFrom == other.nodeFrom and self.nodeTo == other.nodeTo
        else:
            return False

    def __str__(self):
        return 'Edge('+str(self.nodeFrom)+', '+ str(self.nodeTo)+')'
