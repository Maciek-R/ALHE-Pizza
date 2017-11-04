from Node import *
from random import random

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

    def getAll(self):
        return self.nodeFrom, self.nodeTo, self.weight

    def __getRandomWeight__(self):
        return 1 + random() * 4

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.nodeFrom == other.nodeFrom and self.nodeTo == other.nodeTo
        else:
            return False

    def __hash__(self):
        return hash(self.nodeFrom) ^ hash(self.nodeTo) ^ hash(self.weight)
