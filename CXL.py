import os
import xml.etree.ElementTree as ET


def create_class_dict(data_dir):
    gxl_classes = [gxl.split('.gxl')[0].split('_')[-1] for gxl in os.listdir(data_dir)]
    class_options = set(gxl_classes)  # unique class names
    file_names = [gxl.split('.gxl')[0] for gxl in os.listdir(data_dir)]  # folder names
    # class_dict_inv = dict(zip(folder_names, folder_classes))
    class_dict = {k: [] for k in class_options}  # set up dict with empty lists for each class key
    for file in file_names:
        class_dict[file.split('_')[-1]].append(file)  # add the folder name to the appropriate list in the dict
    return class_dict


def addCXLs(class_dict):
    """
    Function for creating 3 sets from .gxl files, train : test : validation, with the size ratio of 2 : 1 :1. Files are
    copied to the new folders and .cxl files with the metadata are created to be used later by GED software
    :param class_dict: dictionary defining the class - normal or abnormal, for each gland
    :return: None
    """

    # data_dir = './data_for_GED'
    data_dir = r'M:\pT1_selected - exp1\data_for_GED'
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


if __name__ == '__main__':
    # data_directory = r'M:\pT1_selected - exp1\data_for_GED'
    data_directory = './data_for_GED'
    gxl_class_dict = create_class_dict(data_directory)
    addCXLs(gxl_class_dict)
