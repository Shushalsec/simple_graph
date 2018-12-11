import os
import xml.etree.ElementTree as ET

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

    def __init__(self, _id, type, save_type = True, x=0, y=0):
        self._id = _id  # node _id
        # save the node type if needed
        if save_type:
            self.attr_dict['type'] = type  # type of the node - central or peripheral
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

    def one_node_writer(self, node_to_add):
        node = ET.SubElement(self.graph, "node", id="_{}".format(node_to_add._id))
        for feature in node_to_add.attr_dict.keys():
            attr_x = ET.SubElement(node, "attr", name=feature)
            _float = ET.SubElement(attr_x, "float").text = str(node_to_add.attr_dict[feature])

    def one_edge_writer(self, edge_to_add, star_shaped_graph=True):
        if star_shaped_graph:
            edge = ET.SubElement(self.graph, "edge", _from="_0", _to="_{}".format(edge_to_add._to))
        else:
            edge = ET.SubElement(self.graph, "edge", _from="_{}".format(edge_to_add._from), _to="_{}".format(edge_to_add._to))

    def XML_writer(self, dst_path, graph_id=0):
        self.graph.set(id="graph_{}".format(graph_id))
        for node in self.nodes:
            XML.one_node_writer(self, node)
        tree = ET.ElementTree(self.root)
        tree.write((os.path.join(dst_path, "{}-graph.xhtml".format(graph_id))))  # for opening in a browser
        tree.write((os.path.join(dst_path, "graph_{}.gxl".format(graph_id))))  # for using in GED software


mean_od = Attribute('mean OD', 10)
mean_darkness = Attribute('darkness', 2)
nano = Node(1, 0, 0, 0)

