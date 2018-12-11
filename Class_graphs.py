import os
from matplotlib.patches import Circle
import xml.etree.ElementTree as ET
import shutil

class Attribute:
    """
    Class for node or edge attribute description
    """
    def __init__(self, label, value):
        self.label = label  # the excel column header to include as node attribute
        self.value = value  # numerical value of the attribute

    def __str__(self):
        return 'attribute type: {} \nvalue: {}'.format(self.label, self.value)

    def add_attr(self, node_object):
        # add attribute as a dictionary entry in the attr_dict attribute of a node object
        node_object.attr_dict[self.label] = self.value

class Node:
    """Class for building a Node based on the node dictionary extracted from the image
    The first and the second arguments are fro the node coordinates and should be given in normalised image
    units from the QuPath image data. The third argument is a dictionary of further attributes of the node.
    """

    attr_dict = {}  # dictionary with attribute type as the unique key and the value as the well.. the value of it

    def __init__(self, _id, type, x=0, y=0):
        self._id = _id  # node _id
        self.type = type  # type of the node - central or peripheral
        self.x = x  # node x coordinate of the cell centroid
        self.y = y  # node y coordinate of the cell centroid


    def __str__(self):
        return(' Node number {} with attribute set {}'.format(self._id, self.attr_dict))


class Edge:
    attr_dict = {}
    def __init__(self, node1, node2): #  to define an edge it is required to enter the nodes to be linked
        self._from = node1._id  # NB the underscore before the attribute name
        self._to = node2._id

    def __str__(self):
        return(' Edge between nodes {} and {} with attribute set {}'.format(self._from, self._to, self.attr_dict))

class Graph():

    def __init__(self, _id, _class):
        self._id = _id
        self.nodes = []
        self.edges = []
        self._class = _class
    def add_a_node(self, node_list):
        self.nodes = self.nodes + node_list
    def add_nodes(self, node):
        self.nodes.append(node)
    def add_edge(self, edge):
        self.edges = self.edges + edge
    def add_edges(self, edge_list):
        self.edges.append(edge_list)

class XML(Graph):
    # create the XML tree
    def __init__(self, root_tag = 'gxl', root_child_tag = 'graph'):
        self.root = ET.Element("{}".format(root_tag))
        self.graph = ET.SubElement(self.root, root_child_tag, edgeids="false", edgemode="undirected")

    def one_node_writer(self, save_coords=True, save_node_type=True):
        pass
    def XML_writer(self, graph_id):
        self.graph.set(id="graph_{}".format(graph_id))









