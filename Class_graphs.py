import os
import xml.etree.ElementTree as ET
import shutil
import pandas as pd


class Node:
    """Class for building a Node based on the node dictionary extracted from the image
    The first and the second arguments are fro the node coordinates and should be given in normalised image
    units from the QuPath image data. The third argument is a dictionary of further attributes of the node.
    """

    def __init__(self, _id, node_type, attr_dict, x=0, y=0):
        self._id = _id  # node _id
        # save the node type if needed
        self.attr_dict = attr_dict
        self.attr_dict['type'] = node_type  # type of the node - central or peripheral
        self.x = x  # node x coordinate of the cell centroid
        self.y = y  # node y coordinate of the cell centroid

    def __str__(self):
        return' Node number {} at {}, {} with attribute set {}'.format(self._id, self.x, self.y, self.attr_dict)


class Edge:
    def __init__(self, node1, node2, attr_dict={}):  # to define an edge it is required to enter the nodes to be linked
        self.attr_dict = attr_dict
        self._from = node1._id  # NB the underscore before the attribute name
        self._to = node2._id

    def __str__(self):
        return' Edge between nodes {} and {} with attribute set {}'.format(self._from, self._to, self.attr_dict)


class Graph():
    '''
    Graph class to generate graphs from input data or based on pre-existing folder files with relevant QuPath data.
    '''

    def __init__(self, graph_dir, attrib_types_list):
        '''
        :param _class: graph class - normal or abnormal
        :param graph_dir: individual folder within masks folder with the excel export, txt file for segmentation
        :param attrib_types_list: list of numbers that indicate the key for the selected parameter (value)
        '''
        self.nodes = []  # node objects are kept in a list
        self.edges = []  # edge objects are kept in a list
        # self._class = _class  # graph class to be extracted in advance from the folder name
        self.graph_dir = graph_dir  # path to the directory
        self.attrib_types_list = attrib_types_list  # excel column to take as attribute

    def add_nodes(self, node_list):
        # add nodes that are given as a list
        self.nodes = self.nodes + node_list

    def add_edges(self, edge_list):
        # add edges given as a list
        self.edges = self.edges + edge_list

    def create_nodes_from_folder(self):
        fold_name = os.path.basename(os.path.normpath(self.graph_dir))  # get the last directory in the path
        crypt_file_path = (os.path.join(self.graph_dir, fold_name+'-crypt.txt'))  # text file path
        crypt_file = pd.read_csv(crypt_file_path, header=None)  # txt file to pandas dataframe
        cryptiness_attr = {'whiteness': crypt_file.iloc[0][0]}  # percentage that is crypt based on segment.py data
        crypt_x = crypt_file.iloc[1][0]  # crypt centroid
        crypt_y = crypt_file.iloc[2][0]
        central_node = Node(0, 0, cryptiness_attr, x=crypt_x, y=crypt_y)
        node_list_to_add = [central_node]
        cells = pd.read_excel(os.path.join(self.graph_dir, fold_name+'-detections.xlsx'))[:3]
        attrib_options = {k + 1: v for (k, v) in zip(range(len(list(cells)[3:])), list(cells)[3:])}

        for row, cell in cells.iterrows():
            node_attribute_dict = {attrib_options[n]: cell[attrib_options[n]] for n in self.attrib_types_list}
            current_node = Node(row + 1, 1, node_attribute_dict, x=cell[attrib_options[1]], y=cell[attrib_options[2]])
            node_list_to_add = node_list_to_add + [current_node]
        return node_list_to_add

    def create_edges_given_nodes(self):
        edge_list_to_add = []
        for node in self.nodes[1:]:
            another_edge = Edge(self.nodes[0], node)
            edge_list_to_add.append(another_edge)
        return edge_list_to_add

    def self_assemble(self):
        node_list_new = self.create_nodes_from_folder()
        self.add_nodes(node_list_new)
        edge_list = self.create_edges_given_nodes()
        self.add_edges(edge_list)
        print('Graph successfuly self-assembled!')


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
        node = ET.SubElement(self.graph, "node", id="_{}".format(node_to_add._id))
        for feature in node_to_add.attr_dict.keys():
            attr_x = ET.SubElement(node, "attr", name=feature)
            _float = ET.SubElement(attr_x, "float").text = str(node_to_add.attr_dict[feature])

    def one_edge_writer(self, edge_to_add, star_shaped_graph=True):
        if star_shaped_graph:
            edge = ET.SubElement(self.graph, "edge", _from="_0", _to="_{}".format(edge_to_add._to))
        else:
            edge = ET.SubElement(self.graph, "edge", _from="_{}".format(edge_to_add._from), _to="_{}".format(edge_to_add._to))

    def XML_writer(self):
        # self.graph.set('id',"graph_{}".format(graph_id))
        for node in self.graph_object.nodes:
            XML.one_node_writer(self, node)
        for edge in self.graph_object.edges:
            XML.one_edge_writer(self, edge, star_shaped_graph=True)
        tree = ET.ElementTree(self.root)
        tree.write((os.path.join(self.dst_path, "{}-graph.xhtml".format(self.graph_id))))  # for opening in a browser
        tree.write((os.path.join(self.dst_path, "graph_{}.gxl".format(self.graph_id))))  # for using in GED software




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
    # dictionary to keep track of the gland titles to be used in 3 .cxl files
    data_dict = {'train.cxl': [], 'test.cxl': [], 'validation.cxl': []}
    # set a switch for separating the .gxl files
    test_switch = True
    # for each .gxl graph in data folder
    for graph_class, graph_list in class_dict.items():
        for i, folder in enumerate(graph_list):
            # move every other into training set
            if i % 2 == 0:
                data_dict['train.cxl'].append(folder)
            # move every other of the remaining into the test set
            elif test_switch:
                data_dict['test.cxl'].append(folder)
                test_switch = False
            # move the remaining ones into the validation set
            else:
                data_dict['validation.cxl'].append(folder)
                test_switch = True
        # inner function for creating the .cxl files when given the name of the dataset

    def createCXL(cxl_to_create):
        root = ET.Element('GraphCollection')  # xml root
        fingerprints = ET.SubElement(root, 'fingerprints')  # xml child
        # for each .gxl in the list of the graphs saved in the dictionary
        for folder in data_dict[cxl_to_create]:
            gxl_file = [graph_file for graph_file in os.listdir(os.path.join(all_dir, 'masks', folder)) if '.gxl' in graph_file][0]
            # child of fingerprints child with attributes file name and class type
            _print = ET.SubElement(fingerprints, '_print', _file=gxl_file, _class=folder.split('_')[-1])
        # save the graph
        tree = ET.ElementTree(root)
        tree.write((os.path.join(data_dir, cxl_to_create)))
        print(cxl_to_create, 'has', len(data_dict[cxl_to_create]), 'graphs!')
    # call the function to create the 3 required .cxl files
    createCXL('test.cxl')
    createCXL('train.cxl')
    createCXL('validation.cxl')


if __name__ == '__main__':

    myfolder = 'M:/ged-shushan/ged-shushan/data/Letter/results'

    masks = os.path.join(myfolder, 'masks')
    fold = os.path.join(myfolder, 'masks', os.listdir(masks)[0]) # fetch the first folder path
    fold_name = os.path.basename(os.path.normpath(fold))
    cells = pd.read_excel(os.path.join(fold, fold_name + '-detections.xlsx'))[:3]
    attrib_options = {k + 1: v for (k, v) in zip(range(len(list(cells)[3:])), list(cells)[3:])}
    print(attrib_options)
    key_list=[]
    str_list = input(
       'Time to choose the node attributes. Enter comma separated number keys of the attributes to be included\n')
    try:
        key_list = [int(l) for l in str_list.replace(' ', '').split(',')]
    except:
        print('Something went wrong with your input!')
        for subdirectory in os.listdir(masks):
            graph_dir = os.path.join(masks, subdirectory)
            one_graph = Graph(graph_dir, key_list)
            one_graph.self_assemble()
            i = subdirectory.split('_')[-2]
            one_XML = XML(one_graph, graph_dir, graph_id=i)
            one_XML.XML_writer()

    myclassdict = create_class_dict(myfolder)
    addCXLs(myfolder, myclassdict)