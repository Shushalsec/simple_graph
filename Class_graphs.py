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
        self.source = node1.identifier  # NB the underscore before the attribute name, not a protected member
        self.target = node2.identifier

    def __str__(self):
        return' Edge between nodes {} and {} with attribute set {}'.format(self.source, self.target, self.attr_dict)


class Graph:
    """
    Graph class to generate graphs from input data or based on pre-existing folder files with relevant QuPath data.
    """

    def __init__(self, graph_dir):
        """

        :param graph_dir: individual folder within masks folder with the excel export, txt file for segmentation
        :param attrib_types_list: list of numbers that indicate the key for the selected parameter (value)
        """
        self.parameter_dir = os.path.join(graph_dir, '../../..')
        with open(os.path.join(self.parameter_dir, 'parameters.txt')) as parameter_file:
            self.graph_parameters = json.load(parameter_file)
        self.attrib_types_list = [int(key.strip()) for key in self.graph_parameters['node']['node_attr_list'].split(',')]

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
        if self.graph_parameters['edge']['function'] == 'star':
            crypt_file_path = (os.path.join(self.graph_dir, fold_name+'-crypt.txt'))  # text file path
            crypt_file = pd.read_csv(crypt_file_path, header=None)  # txt file to pandas dataframe
            cryptiness_and_type = {'whiteness': crypt_file.iloc[0][0], 'type': 0}  # percentage that is crypt based on segment.py data
            crypt_x = crypt_file.iloc[1][0]  # crypt centroid
            crypt_y = crypt_file.iloc[2][0]
            central_node = Node(0, cryptiness_and_type, x=crypt_x, y=crypt_y)
            node_list_to_add = [central_node]
        else:
            node_list_to_add = []
        cells = pd.read_excel(os.path.join(self.graph_dir, fold_name+'-detections.xlsx'))
        attrib_options = {k + 1: v for (k, v) in zip(range(len(list(cells)[3:])), list(cells)[3:])}
        attrib_options[len(attrib_options.keys())+1] = 'type'
        for row, cell in cells.iterrows():
            if self.attrib_types_list[0] != 'control':
                node_attribute_dict = {attrib_options[n]: cell[attrib_options[n]] for n in self.attrib_types_list}
                if self.graph_parameters['edge']['function'] == 'star':
                    node_attribute_dict['type'] = 1
            else:
                node_attribute_dict = {'control': '0'}
            current_node = Node(row + 1, node_attribute_dict, x=cell[attrib_options[1]], y=cell[attrib_options[2]])
            node_list_to_add = node_list_to_add + [current_node]
        return node_list_to_add

    def create_edges_given_nodes(self):
        edge_list_to_add = []
        # for node in self.nodes[1:]:
        #     another_edge = Edge(self.nodes[0], node, {})
        #     edge_list_to_add.append(another_edge)
        if self.graph_parameters['edge']['function'] == 'star':
            edge_list_to_add = [Edge(self.nodes[0], node, {}) for node in self.nodes[1:]]
        # TODO: fix the spatial edge function definition bug!
        elif self.graph_parameters['edge']['function'] == 'spatial':
            x = np.asarray([self.nodes[i].x for i in range(len(self.nodes))])
            y = np.asarray([self.nodes[i].y for i in range(len(self.nodes))])
            if self.graph_parameters['edge']['dist_normalize']=='Y':
                x = (x - np.min(x)) / (np.max(x) - np.min(x))
                y = (y - np.min(y)) / (np.max(y) - np.min(y))
            tree = spatial.KDTree(list(zip(x, y)))
            k_nearest = self.graph_parameters['edge']['KDTree_k']
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
            k_nearest = self.graph_parameters['edge']['KDTree_k']
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
            attr_x = ET.SubElement(node, "attr", name='attr_{}'.format(i))
            _float = ET.SubElement(attr_x, "float").text = str(node_to_add.attr_dict[feature])

    def one_edge_writer(self, edge_to_add):
        if self.graph_object.graph_parameters['edge']['function'] == 'star':
            edge = ET.SubElement(self.graph, "edge", source="_0", target="_{}".format(edge_to_add.target))
        else:
            edge = ET.SubElement(self.graph, "edge", source="_{}".format(edge_to_add.source), target="_{}".format(edge_to_add.target))

    def XML_writer(self, file_extension):
        # self.graph.set('id',"graph_{}".format(graph_id))
        for node in self.graph_object.nodes:
            XML.one_node_writer(self, node)
        for edge in self.graph_object.edges:
            XML.one_edge_writer(self, edge)
        tree = ET.ElementTree(self.root)
        tree.write((os.path.join(self.dst_path, "{}-graph.xhtml".format(self.graph_id))))  # for opening in a browser
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

def copy_gxl_files(all_dir):
    masks_dir = os.path.join(all_dir, 'masks')  # directory with folders for each gland
    os.mkdir(os.path.join(all_dir, 'data'))  # create a new directory for saving result data
    data_dir = os.path.join(all_dir, 'data')  # directory that will be later accessed by GED
    # for each folder or gland
    for subdir in os.listdir(masks_dir):
        # path to the current directory
        source = os.path.join(masks_dir, subdir)
        # for each file in the gland directory
        for file in os.listdir(source):
            # detect the .gxl file
            if '.gxl' in file:
                # set the path to .gxl as the source
                source_file_path = os.path.join(source, file)
                # copy the file from source to the directory named data
                shutil.copy(source_file_path, data_dir)

def assemble_data(myfolder):

    # myfolder = 'M:/ged-shushan/ged-shushan/data/Letter/results'
    project_dir = os.path.join(myfolder, '..')
    with open(os.path.join(project_dir, 'parameters.txt'), 'r') as parameter_file:
        parameters = json.load(parameter_file)

    masks = os.path.join(myfolder, 'masks')
    fold = os.path.join(myfolder, 'masks', os.listdir(masks)[0]) # fetch the first folder path
    fold_name = os.path.basename(os.path.normpath(fold))

    cells = pd.read_excel(os.path.join(fold, fold_name + '-detections.xlsx'))[:3]
    attrib_options = {k + 1: v for (k, v) in zip(range(len(list(cells)[3:])), list(cells)[3:])}
    print(attrib_options)
    for i, attribute_index in enumerate(parameters['node']['node_attr_list']):
        print(attrib_options[int(attribute_index)])
        parameters['attribute_{}'.format(i)] = attrib_options[int(attribute_index)]
    with open(os.path.join(project_dir, 'parameters.txt'), 'w') as parameter_file:
        json.dump(parameters, parameter_file)
    print('checkpoint 1')
    for subdirectory in os.listdir(masks):
        graph_dir = os.path.join(masks, subdirectory)
        one_graph = Graph(graph_dir)
        one_graph.self_assemble()
        i = subdirectory.split('_')[-2]
        one_XML = XML(one_graph, graph_dir, graph_id=i)
        one_XML.XML_writer('gxl')
        one_graphml = XML(one_graph, graph_dir, graph_id=1, root_tag='graphml')
        one_graphml.XML_writer('graphml')
    copy_gxl_files(myfolder)


if __name__ == '__main__':
    os.chdir(r'M:\pT1_selected - complete_annotation')
    # PROJECT_DIR = r'M:\crypt_to_graph'
    PROJECT_DIR = os.getcwd()
    # pooled_data_dir = os.path.join(PROJECT_DIR, 'pooled_image_data')
    version_name = os.path.basename(os.path.normpath(PROJECT_DIR))
    folder = r'B08.8643_IVE_HE_pT1_selected - complete_annotation'
    assemble_data(os.path.join(PROJECT_DIR, folder))

    #
    # for folder in os.listdir(PROJECT_DIR):
    #     print(folder, os.path.isdir(os.path.join(PROJECT_DIR, folder)), version_name in folder)
    #     if os.path.isdir(os.path.join(PROJECT_DIR, folder)) and folder.endswith(version_name):
    #         if len(os.listdir(os.path.join(PROJECT_DIR, folder)))>0:
    #             if 'data' in os.listdir(os.path.join(PROJECT_DIR, folder)):
    #                 print('Graphs already present, rename the data folder!')
    #                 # Class_graphs.assemble_data(os.path.join(PROJECT_DIR, folder))
    #             else:
    #                 print('CREATING GRAPHS IN\t', folder)
    #                 assemble_data(os.path.join(PROJECT_DIR, folder))
    #
