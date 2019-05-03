import os
import xml.etree.ElementTree as ET
import shutil
import pandas as pd
import json
import numpy as np
from scipy import spatial

class Node:
    """Class for building a Node based on the node dictionary extracted from the image
    The first and the second arguments are fro the node coordinates and should be given in normalised image
    units from the QuPath image data. The third argument is a dictionary of further attributes of the node.
    """
    identifier: int

    def __init__(self, identifier, attr_dict, x=0, y=0):
        self.identifier = identifier  # node _id
        # save the node type if needed
        self.attr_dict = attr_dict

        # self.attr_dict['type'] = node_type  # type of the node - central or peripheral
        self.x = x  # node x coordinate of the cell centroid
        self.y = y  # node y coordinate of the cell centroid

    def __str__(self):
        return' Node number {} at {}, {} with attribute set {}'.format(self.identifier, self.x, self.y, self.attr_dict)


class Edge:
    def __init__(self, node1, node2, attr_dict):  # to define an edge it is required to enter the nodes to be linked
        self.attr_dict = attr_dict
        self._from = node1.identifier  # NB the underscore before the attribute name, not a protected member
        self._to = node2.identifier

    def __str__(self):
        return' Edge between nodes {} and {} with attribute set {}'.format(self._from, self._to, self.attr_dict)


class Graph:
    """
    Graph class to generate graphs from input data or based on pre-existing folder files with relevant QuPath data.
    """

    def __init__(self, graph_dir, parameters):
        """

        :param graph_dir: individual folder within masks folder with the excel export, txt file for segmentation
        :param attrib_types_list: list of numbers that indicate the key for the selected parameter (value)
        """
        # self.parameter_dir = os.path.join(graph_dir, '../../..')
        # with open(os.path.join(self.parameter_dir, 'parameters.txt')) as parameter_file:
        #     self.graph_parameters = json.load(parameter_file)
        self.graph_parameters = parameters

        self.nodes = []  # node objects are kept in a list
        self.edges = []  # edge objects are kept in a list
        # self._class = _class  # graph class to be extracted in advance from the folder name
        self.graph_dir = graph_dir  # path to the directory
        # self.attrib_types_list = attrib_types_list  # excel column to take as attribute
        # self.edge_funct = edge_funct


    def add_nodes(self, node_list):
        # add nodes that are given as a list
        self.nodes = self.nodes + node_list

    def add_edges(self, edge_list):
        # add edges given as a list
        self.edges = self.edges + edge_list

    def create_nodes_from_folder(self):
        fold_name = os.path.basename(os.path.normpath(self.graph_dir))  # get the last directory in the path
        node_list_to_add = []
        cells = pd.read_excel(os.path.join(self.graph_dir, fold_name+'-detections.xlsx'))
        col_names = list(cells)

        feature_array = np.array([cells.iloc[:, n] for n in self.graph_parameters['node']['node_attr_list']])

        mean_array = np.expand_dims(np.array(self.graph_parameters['node']['attr_mean']), axis=1)
        sd_array = np.expand_dims(np.array(self.graph_parameters['node']['attr_sd']), axis=1)

        normalised_feature_array = (feature_array - mean_array) / sd_array
        normalised_x = (cells.iloc[:,2] - min(cells.iloc[:,2]))/(max(cells.iloc[:,2]) - min(cells.iloc[:,2]))
        normalised_y = (cells.iloc[:,3] - min(cells.iloc[:,3]))/(max(cells.iloc[:,3]) - min(cells.iloc[:,3]))

        for row, cell in cells.iterrows():

            node_attribute_dict = {col_names[n]: normalised_feature_array[i][row] for i, n in enumerate(self.graph_parameters['node']['node_attr_list'])}
            current_node = Node(row, node_attribute_dict, x=normalised_x[row], y=normalised_y[row])
            node_list_to_add.append(current_node)
        return node_list_to_add

    def create_edges_given_nodes(self):
        edge_list_to_add = []
        # for node in self.nodes[1:]:
        #     another_edge = Edge(self.nodes[0], node, {})
        #     edge_list_to_add.append(another_edge)
        if self.graph_parameters['edge']['function'] == 'star':
            edge_list_to_add = [Edge(self.nodes[0], node, {}) for node in self.nodes[1:]]
        elif self.graph_parameters['edge']['function'] == 'spatial':
            x = np.asarray([self.nodes[i].x for i in range(len(self.nodes))])
            y = np.asarray([self.nodes[i].y for i in range(len(self.nodes))])
            if self.graph_parameters['edge']['dist_normalize']=='Y':
                x = (x - np.min(x)) / (np.max(x) - np.min(x))
                y = (y - np.min(y)) / (np.max(y) - np.min(y))
            tree = spatial.KDTree(list(zip(x, y)))
            k_nearest = self.graph_parameters['edge']['KDTree_k'] + 1
            dist, nn = tree.query(tree.data, k=k_nearest)  # array of distances and k nearest neighbors for each node
            # iterate over the columns of the numpy array with nearest neighbor indices
            for column in range(1, nn.shape[1]):  # omit the first column as this is the node index itself or 0 distance
                for j in range(nn.shape[0]):
                    edge_list_to_add.append(Edge(self.nodes[j], self.nodes[nn[j, column]],
                                                 {'spatial_distance': dist[j, column]}))
        elif self.graph_parameters['edge']['function'] == 'similarity':
            print(list(self.nodes[0].attr_dict.keys()))
            keys = [key for key in list(self.nodes[0].attr_dict.keys())]
            measurements = [tuple(node.attr_dict[k] for k in keys) for node in self.nodes]
            tree = spatial.KDTree(measurements)
            k_nearest = self.graph_parameters['edge']['KDTree_k'] + 1
            dist, nn = tree.query(tree.data, k=k_nearest, p=1)  # array of k nearest neighbors for each node
            for column in range(1, nn.shape[1]):  # omit the first column as this is the node index itself or 0 distance
                for j in range(nn.shape[0]):
                    edge_list_to_add.append(Edge(self.nodes[j], self.nodes[nn[j, column]],
                                                 {'feature_manhattan_distance': dist[j, column]}))
        return edge_list_to_add

    def self_assemble(self):
        node_list_new = self.create_nodes_from_folder()
        self.add_nodes(node_list_new)
        if len(self.nodes) > 1:
            edge_list = self.create_edges_given_nodes()
            self.add_edges(edge_list)



class XML():
    # create the XML tree
    def __init__(self, graph_object, dst_path, graph_id=0, root_tag = 'gxl', root_child_tag = 'graph'):
        """

        :type graph_object: Graph
        """
        self.graph_object = graph_object
        self.dst_path = dst_path
        self.graph_id = graph_id
        self.root = ET.Element("{}".format(root_tag))
        self.graph = ET.SubElement(self.root, root_child_tag, id=str(graph_id), edgeids="false", edgemode="undirected")

    def one_node_writer(self, node_to_add):
        node = ET.SubElement(self.graph, "node", id="_{}".format(node_to_add.identifier))
        for i, feature in enumerate(node_to_add.attr_dict.keys()):
            attr_i = ET.SubElement(node, "attr", name='attr_{}'.format(i))
            _float = ET.SubElement(attr_i, "float").text = str(node_to_add.attr_dict[feature])
        x = ET.SubElement(node, "attr", name="x")
        x_value = ET.SubElement(x, "float").text = str(node_to_add.x)
        y = ET.SubElement(node, "attr", name="y")
        y_value = ET.SubElement(y, "float").text = str(node_to_add.y)


    def one_edge_writer(self, edge_to_add):
        if self.graph_object.graph_parameters['edge']['function'] == 'star':
            edge = ET.SubElement(self.graph, "edge", _from="_0", _to="_{}".format(edge_to_add._to))
        else:
            edge = ET.SubElement(self.graph, "edge", _from="_{}".format(edge_to_add._from), _to="_{}".format(edge_to_add._to))

    def XML_writer(self, file_extension):
        # self.graph.set('id',"graph_{}".format(graph_id))
        for node in self.graph_object.nodes:
            XML.one_node_writer(self, node)
        for edge in self.graph_object.edges:
            XML.one_edge_writer(self, edge)
        tree = ET.ElementTree(self.root)
        # tree.write((os.path.join(self.dst_path, "{}-graph.xhtml".format(self.graph_id))))  # for opening in a browser
        filename_graph = os.path.basename(os.path.normpath(self.graph_object.graph_dir))
        tree.write((os.path.join(self.dst_path, "{}.{}".format(filename_graph, file_extension))))  # for using in GED software


def create_class_dict(all_dir):
    masks = os.path.join(all_dir, 'masks')
    folder_classes = [folder.split('_')[-1] for folder in os.listdir(masks)]
    class_options = set(folder_classes)  # unique class names
    folder_names = [folder for folder in os.listdir(masks)]  # folder names
    # class_dict_inv = dict(zip(folder_names, folder_classes))
    class_dict = {k:[] for k in class_options}  # set up dict with empty lists for each class key
    for folder in folder_names:
        class_dict[folder.split('_')[-1]].append(folder)  # add the folder name to the appropriate list in the dict
    return class_dict

#
param_path = os.path.join(r'M:\pT1_cell_1\80p_4x_spat', 'parameters.json')
with open(param_path) as parameter_file:
    graph_parameters = json.load(parameter_file)

# g.add_edges(g.create_edges_given_nodes())

# from lab_rat import graph_parameters
# g = Graph(r'M:\pT1_cell_1\organised_folders\B08.8643_IVE_HE\masks\B08.8643_IVE_HE_0_abnormal', graph_parameters)
# g.add_nodes(g.create_nodes_from_folder())
g_23 = Graph(r'M:\pT1_cell_1\organised_folders\B09.15291_D_HE\masks\B09.15291_D_HE_23_normal', graph_parameters)
g_23.self_assemble()
g_31 = Graph(r'M:\pT1_cell_1\organised_folders\B08.13071_G_HE\masks\B08.13071_G_HE_31_normal', graph_parameters)
g_31.self_assemble()

