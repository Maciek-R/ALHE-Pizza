import sys
from plotly.graph_objs import *
import networkx as nx

class Employee:
    """Employee class"""
    def __init__(self, first, last):
        self.first = first
        self.last = last

    def test_method(self):
        pass



    def fullName(self):
        return '{}{}'.format(self.first, self.last)



emp = Employee('John', 'Smith')
emp.test_method()
print(emp.fullName())
print('asd')

emp.zmienna = 15

print(emp.zmienna+13)
