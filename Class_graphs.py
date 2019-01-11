import os
import xml.etree.ElementTree as ET
import shutil
import pandas as pd


class Node:
    """Class for building a Node based on the node dictionary extracted from the image
    The first and the second arguments are fro the node coordinates and should be given in normalised image
    units from the QuPath image data. The third argument is a dictionary of further attributes of the node.
    """


    def __init__(self, _id, type, attr_dict, x=0, y=0):
        self._id = _id  # node _id
        # save the node type if needed
        self.attr_dict = attr_dict
        self.attr_dict['type'] = type  # type of the node - central or peripheral
        self.x = x  # node x coordinate of the cell centroid
        self.y = y  # node y coordinate of the cell centroid


    def __str__(self):
        return(' Node number {} at {}, {} with attribute set {}'.format(self._id, self.x, self.y, self.attr_dict))


class Edge:
    def __init__(self, node1, node2, attr_dict={}): #  to define an edge it is required to enter the nodes to be linked
        self.attr_dict = attr_dict
        self._from = node1._id  # NB the underscore before the attribute name
        self._to = node2._id

    def __str__(self):
        return(' Edge between nodes {} and {} with attribute set {}'.format(self._from, self._to, self.attr_dict))

class Graph():

    def __init__(self, _class, graph_dir, attrib_types_list):
        self.nodes = []
        self.edges = []
        self._class = _class
        self.graph_dir = graph_dir
        self.attrib_types_list = attrib_types_list

    def add_nodes(self, node_list):
        self.nodes = self.nodes + node_list

    def add_edges(self, edge_list):
        self.edges = self.edges + edge_list

    def create_nodes_from_folder(self):
        crypt_file_path = (os.path.join(self.graph_dir, self.graph_dir.split('/')[-1]+'-crypt.txt'))
        crypt_file = pd.read_csv(crypt_file_path, header = None)
        cryptiness_attr = {'whiteness' : crypt_file.iloc[0][0]}
        crypt_x = crypt_file.iloc[1][0]
        crypt_y = crypt_file.iloc[2][0]
        central_node = Node(0, 0, cryptiness_attr, x=crypt_x, y=crypt_y)
        node_list_to_add = [central_node]
        cells = pd.read_excel(os.path.join(self.graph_dir, self.graph_dir.split('/')[-1]+'-detections.xlsx'))[:3]
        attrib_options = {k + 1: v for (k, v) in zip(range(len(list(cells)[3:])), list(cells)[3:])}
        for row, cell in cells.iterrows():
            node_attribute_dict = {attrib_options[n]: cell[attrib_options[n]] for n in self.attrib_types_list}
            current_node = Node(row + 1, 1, node_attribute_dict, x=cell[attrib_options[1]], y=cell[attrib_options[2]])
            node_list_to_add = node_list_to_add + [current_node]
        # get the crypt data

        # central_node_attr.add_to(central_node)
        # node_list_to_add.append(central_node)
        return node_list_to_add

    def create_edges_given_nodes(self, node_list):
        edge_list_to_add = []
        for node in node_list[1:]:
            another_edge = Edge(node_list[0], node)
            edge_list_to_add.append(another_edge)
        return edge_list_to_add

    def self_assemble(self):
        node_list_new = self.create_nodes_from_folder()
        edge_list = self.create_edges_given_nodes(node_list_new)
        self.add_nodes(node_list_new)
        self.add_edges(edge_list)
        print('Graph successfuly self-assembled!')

if __name__ == '__main__':
    fold = 'M:/ged-shushan/ged-shushan/data/Letter/results/masks/287c_B2004.12899_III-B_HE_0_normal'

    a = Graph('norm', fold, [3, 4])
    a.self_assemble()
    print(a.nodes[0])
    print(a.nodes[1])
    print(a.nodes[2])
    print(a.edges[0])



class XML(Graph):
    # create the XML tree
    def __init__(self, dst_path, root_tag = 'gxl', root_child_tag = 'graph'):
        self.dst_path = dst_path
        self.root = ET.Element("{}".format(root_tag))
        self.graph = ET.SubElement(self.root, root_child_tag, id='***', edgeids="false", edgemode="undirected")

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

    def XML_writer(self, graph_id=0):
        self.graph.set('id',"graph_{}".format(graph_id))
        for node in self.Graph.nodes:
            XML.one_node_writer(self, node)
        graph_shape = input('Should I get a star shaped graph? True/False')
        for edge in self.Graph.edges:
            XML.one_edge_writer(self, edge, star_shaped_graph=graph_shape)
        tree = ET.ElementTree(self.root)
        tree.write((os.path.join(self.dst_path, "{}-graph.xhtml".format(graph_id))))  # for opening in a browser
        tree.write((os.path.join(self.dst_path, "graph_{}.gxl".format(graph_id))))  # for using in GED software



def addCXLs(all_dir, class_dict):
    """
    Function for creating 3 sets from .gxl files, train : test : validation, with the size ratio of 2 : 1 :1. Files are
    copied to the new folders and .cxl files with the metadata are created to be used later by GED software
    :param all_dir: directory with the masks folder and detections.txt file
    :param class_dict: dictionary defining the class - normal or abnormal, for each gland
    :return: None
    """
    masks_dir = os.path.join(all_dir, 'masks')  # directory with folders for each gland
    os.mkdir(os.path.join(all_dir, 'data'))  # create a new directory for saving result data
    data_dir = os.path.join(all_dir, 'data')  # directory that will be later accessed by GED
    # for each folder or gland
    for subfolder in os.listdir(masks_dir):
        # path to the current directory
        source = os.path.join(masks_dir, subfolder)
        # for each file in the gland directory
        for file in os.listdir(source):
            # detect the .gxl file
            if '.gxl' in file:
                # set the path to .gxl as the source
                source_file_path = os.path.join(source, file)
                # copy the file from source to the directory named data
                shutil.copy(source_file_path, data_dir)
    # dictionary to keep track of the gland titles to be used in 3 .cxl files
    data_dict = {'train.cxl': [], 'test.cxl': [], 'validation.cxl': []}
    # set a switch for separating the .gxl files
    test_switch = True
    # for each .gxl graph in data folder
    for i, file in enumerate(os.listdir(data_dir)):
        # move every other into training set
        if i % 2 == 0:
            data_dict['train.cxl'].append(file)
        # move every other of the remaining into the test set
        elif test_switch:
            data_dict['test.cxl'].append(file)
            test_switch = False
        # move the remaining ones into the validation set
        else:
            data_dict['validation.cxl'].append(file)
            test_switch = True
    # inner function for creating the .cxl files when given the name of the dataset
    def createCXL(cxl_to_create):
        root = ET.Element('GraphCollection')  # xml root
        fingerprints = ET.SubElement(root, 'fingerprints')  # xml child
        # for each .gxl in the list of the graphs saved in the dictionary
        for gxl_file in data_dict[cxl_to_create]:
            # child of fingerprints child with attributes file name and class type
            _print = ET.SubElement(fingerprints, '_print', _file=gxl_file, _class=class_dict[gxl_file])
        # save the graph
        tree = ET.ElementTree(root)
        tree.write((os.path.join(data_dir, cxl_to_create)))
        print(cxl_to_create, 'has', len(data_dict[cxl_to_create]), 'graphs!')
    # call the function to create the 3 required .cxl files
    createCXL('test.cxl')
    createCXL('train.cxl')
    createCXL('validation.cxl')

