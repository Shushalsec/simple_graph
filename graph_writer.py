"""
Script 3: writes .gxl and .cxl format graphs
Input should be the directory with organised files, cript data added
"""


import os
import xml.etree.ElementTree as ET
import pandas as pd
import shutil
from decorators import timer

@timer
def graph_extracter(all_dir):
    """

    :param all_dir: directory with the masks and detections.txt file named results at the moment
    :return: dictionary of .gxl graph names and the corresponding class so that this is used when making .cxl files
    """

    masks_dir = os.path.join(all_dir, 'masks') #  subdirectory with the graph folders
    class_dict = {}  # dictionary for saving details about each graph type, i.e. normal or abnormal
    #  for each folder corresponding to a gland annotation
    for i, folder in enumerate(os.listdir(masks_dir)):
        print('Processing gland', folder)
        #  load the data per folder or gland into pandas dataframe
        cells = pd.read_excel(os.path.join(masks_dir, folder, folder+'-detections.xlsx'))
        #  if the first one ask the user about the attribute to be included in the graph
        if i == 0:
            attrib_options = {k + 1: v for (k, v) in zip(range(len(list(cells)[3:])), list(cells)[3:])}  # attributes
            #  print attributes and the corresponding index so that user simply inputs the number not the entire phrase
            for k, v in attrib_options.items():
                print(k, v)
            #  ask for user input and save the number corresponding to an item in the dictionary
            attrib_num = int(input('Type the number of the attribute to be included in the graph:    '))
            #  TODO: by default add x and y coordinates but allow to add 3rd and further attributes
            selected_attrib = attrib_options[attrib_num]  # column title in the detections.txt file that is selected
            print('You have selected {} as attribute'.format(selected_attrib))
        # from each folder get the cript data
        crypt_file_path = (os.path.join(masks_dir, folder, folder+'-crypt.txt'))
        crypt_file = open(crypt_file_path, 'r')
        cryptiness = crypt_file.readlines()[0]

        #  create an xml tree
        root = ET.Element("gxl")
        graph = ET.SubElement(root, "graph", id="graph_{}".format(i), edgeids="false", edgemode="undirected")

        #  define the central node
        node = ET.SubElement(graph, "node", id="_{}".format(0))  # create child of graph - node
        attr = ET.SubElement(node, "attr", name="x")  # define attribute x
        _float = ET.SubElement(attr, "float").text = "0"  # set it to 0 as this is a crypt node
        attr = ET.SubElement(node, "attr", name="y")  # define attribute 2
        # set it using the crypt data extracted earlier
        _float = ET.SubElement(attr, "float").text = "{}".format(cryptiness)
        # for each row of the excel spreadsheet for the given gland
        for node_id, cell_attribute in enumerate(cells[selected_attrib]):
            # define the node with enumeration starting from 1
            node = ET.SubElement(graph, "node", id="_{}".format(node_id+1))
            # define the first attribute
            attr = ET.SubElement(node, "attr", name="x")
            # set it to to 1 as this is a node corresponding to a cell in the gland
            _float = ET.SubElement(attr, "float").text = "1"
            # define the second attribute
            attr = ET.SubElement(node, "attr", name="y")
            # set to the attribute selected by the user
            _float = ET.SubElement(attr, "float").text = "{}".format(cell_attribute)
            # define an edge from the node number 0 i.e. crypt to node it is currently on
            edge = ET.SubElement(graph, "edge", _from="_0", _to="_{}".format(node_id+1))
        # define the xml and save files
        tree = ET.ElementTree(root)
        tree.write((os.path.join(masks_dir, folder, "{}-graph.xhtml".format(folder))))  # for opening in a browser
        tree.write((os.path.join(masks_dir, folder, "graph_{}.gxl".format(i))))  # for using in GED software
        #  save the information about the class in a dictionary entry
        class_dict["graph_{}.gxl".format(i)] = folder.split('_')[-1]  # add an entry to the dictionary about the class
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
    data_dict = {'train.cxl' : [], 'test.cxl' : [], 'validation.cxl' : []}
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
    # call the function to create the 3 required .cxl files
    createCXL('test.cxl')
    createCXL('train.cxl')
    createCXL('validation.cxl')


myfolder = 'M:/ged-shushan/ged-shushan/data/Letter/results'

class_dictionary = graph_extracter(myfolder)
addCXLs(myfolder, class_dictionary)