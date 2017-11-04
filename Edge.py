class Edge:
    def __init__(self, nodeFrom, nodeTo, weight=1, isOneWay=False):
        self.nodeFrom = nodeFrom
        self.nodeTo = nodeTo
        self.weight = weight
        self.isOneWay = isOneWay

    def get(self):
        return self.nodeFrom, self.nodeTo
