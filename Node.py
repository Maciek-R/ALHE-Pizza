from math import sqrt

class Node:
    def __init__(self, x, y, ):
        self.x = x
        self.y = y

    def getPosition(self):
        return self.x, self.y

    def getDistanceTo(self, node):
        x,y = node.getPosition()
        return sqrt((x - self.x)**2 + (y-self.y)**2)

    def getLabel(self):
        #return "{},{}".format(str(self.x), str(self.y))
        return (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)
