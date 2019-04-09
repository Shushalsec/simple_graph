import os
import xml.etree.ElementTree as ET
import json


def create_class_dict(data_dir):
    gxl_classes = [gxl.split('.gxl')[0].split('_')[-1] for gxl in os.listdir(data_dir)]
    class_options = set(gxl_classes)  # unique class names
    file_names = [gxl for gxl in os.listdir(data_dir) if gxl.endswith('.gxl')]  # folder names
    # class_dict_inv = dict(zip(folder_names, folder_classes))
    class_dict = {k: [] for k in class_options}  # set up dict with empty lists for each class key
    for file in file_names:
        # add the folder name to the appropriate list in the dict
        class_dict[file.split('_')[-1].split('.gxl')[0]].append(file)
    return class_dict


def addCXLs(class_dict):
    """
    Function for creating 3 sets from .gxl files, train : test : validation, with the size ratio of 2 : 1 :1. Files are
    copied to the new folders and .cxl files with the metadata are created to be used later by GED software
    :param class_dict: dictionary defining the class - normal or abnormal, for each gland
    :return: None
    """
    data_dir = './data_for_GED'
    data_dict = {'train.cxl': [], 'test.cxl': [], 'validation.cxl': []}
    # set a switch for separating the .gxl files
    test_switch = True
    # TODO: add an option for splitting data taking into account Proben-Nr
    with open(os.path.join('parameters.txt')) as parameter_file:
        parameters = json.load(parameter_file)
    if parameters['split_data'] == 'wsi':

        for i, wsi in enumerate(parameters['pool_images']):
            # move every other into training set
            gxls_from_wsi = [gxl for gxl in os.listdir(data_dir) if gxl.endswith('.gxl') and wsi in gxl]
            if i % 2 == 0:

                data_dict['train.cxl'] = data_dict['train.cxl'] + gxls_from_wsi
            # move every other of the remaining into the test set
            elif test_switch:
                data_dict['test.cxl'] = data_dict['test.cxl'] + gxls_from_wsi
                test_switch = False
            # move the remaining ones into the validation set
            else:
                data_dict['validation.cxl'] = data_dict['validation.cxl'] + gxls_from_wsi
                test_switch = True

    # data_dir = r'M:\pT1_selected - exp1\data_for_GED'
    # dictionary to keep track of the gland titles to be used in 3 .cxl files
        else:
            # for each .gxl graph in data folder
            for graph_class, graph_list in class_dict.items():
                for i, gxl_file in enumerate(graph_list):
                    # move every other into training set
                    if i % 2 == 0:
                        data_dict['train.cxl'].append(gxl_file)
                    # move every other of the remaining into the test set
                    elif test_switch:
                        data_dict['test.cxl'].append(gxl_file)
                        test_switch = False
                    # move the remaining ones into the validation set
                    else:
                        data_dict['validation.cxl'].append(gxl_file)
                        test_switch = True
        # inner function for creating the .cxl files when given the name of the dataset

    def createCXL(cxl_to_create):
        root = ET.Element('GraphCollection')  # xml root
        fingerprints = ET.SubElement(root, 'fingerprints')  # xml child
        # for each .gxl in the list of the graphs saved in the dictionary
        for gxl in data_dict[cxl_to_create]:
            # child of fingerprints child with attributes file name and class type
            _print = ET.SubElement(fingerprints, '_print', _file=gxl, _class=gxl.split('_')[-1].split('.gxl')[0])
        # save the graph
        tree = ET.ElementTree(root)
        tree.write((os.path.join(data_dir, cxl_to_create)))
        print(cxl_to_create, 'has', len(data_dict[cxl_to_create]), 'graphs!')

    # call the function to create the 3 required .cxl files
    createCXL('test.cxl')
    createCXL('train.cxl')
    createCXL('validation.cxl')
    return data_dict


def make_cxls():

    data_directory = './data_for_GED'
    gxl_class_dict = create_class_dict(data_directory)
    addCXLs(gxl_class_dict)

os.chdir(r'M:\pT1_selected - template_annotated - QuPath_export_cell')
make_cxls()