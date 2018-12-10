import matplotlib.pyplot as plt
import os
from matplotlib.patches import Circle


class Attribute:
    """
    Class for node or edge attribute description
    """
    def __init__(self, label, value):
        self.label = label
        self.value = value

    def __str__(self):
        return 'attribute type: {} \nvalue: {}'.format(self.label, self.value)

    def add_attr(self, node_object):
        node_object.attr_dict[self.label] = self.value

class Node:
    """Class for building a Node based on the node dictionary extracted from the image
    The first and the second arguments are fro the node coordinates and should be given in normalised image
    units from the QuPath image data. The third argument is a dictionary of further attributes of the node.
    """

    attr_dict = {}

    def __init__(self, _id, x=0, y=0):
        self._id = _id
        self.x = x
        self.y = y


    def __str__(self):
        return(' Node number {} with attribute set {}'.format(self._id, self.attr_dict))


class Edge:
    attr_dict = {}
    def __init__(self, node1, node2):
        self._from = node1._id
        self._to = node2._id

    def __str__(self):
        return(' Edge between nodes {} and {} with attribute set {}'.format(self._from, self._to, self.attr_dict))

class Graph():

    def __init__(self, _id, _class):
        self._id = _id
        self.nodes = []
        self.edge = []
        self._class = _class
    def add_nodes(self):
        pass
    def add_edges(self):
        pass
