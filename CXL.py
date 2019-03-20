import os
import xml.etree.ElementTree as ET


def addCXLs(all_dir, class_dict):
    """
    Function for creating 3 sets from .gxl files, train : test : validation, with the size ratio of 2 : 1 :1. Files are
    copied to the new folders and .cxl files with the metadata are created to be used later by GED software
    :param all_dir: directory with the masks folder and detections.txt file
    :param class_dict: dictionary defining the class - normal or abnormal, for each gland
    :return: None
    """

    data_dir = './pooled_image_data'
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
        gxl_files = [graph_file for graph_file in os.listdir(data_dir) if graph_file.endswith('.gxl')]
        for gxl in gxl_files:
            # child of fingerprints child with attributes file name and class type
            _print = ET.SubElement(fingerprints, '_print', _file=gxl, _class=gxl.split('_')[-1])
        # save the graph
        tree = ET.ElementTree(root)
        tree.write((os.path.join(data_dir, cxl_to_create)))
        print(cxl_to_create, 'has', len(data_dict[cxl_to_create]), 'graphs!')
        
    # call the function to create the 3 required .cxl files
    createCXL('test.cxl')
    createCXL('train.cxl')
    createCXL('validation.cxl')

