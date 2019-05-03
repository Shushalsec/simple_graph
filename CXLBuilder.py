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


def addCXLs(class_dict, data_dir, parameters):
    """
    Function for creating 3 sets from .gxl files, train : test : validation, with the size ratio of 2 : 1 :1. Files are
    copied to the new folders and .cxl files with the metadata are created to be used later by GED software
    :param class_dict: dictionary defining the class - normal or abnormal, for each gland
    :return: None
    """


    def createCXL(cxl_to_create, list_of_gxls):
        root = ET.Element('GraphCollection')  # xml root
        fingerprints = ET.SubElement(root, 'fingerprints')  # xml child
        # for each .gxl in the list of the graphs saved in the dictionary
        for gxl in []:
            # child of fingerprints child with attributes file name and class type
            _print = ET.SubElement(fingerprints, '_print', _file=gxl, _class=gxl.split('_')[-1].split('.gxl')[0])
        # save the graph
        tree = ET.ElementTree(root)
        tree.write((os.path.join(data_dir, cxl_to_create)))
        print(cxl_to_create, 'has', len(list_of_gxls), 'graphs!')

    # call the function to create the 3 required .cxl files
    createCXL('test.cxl')
    createCXL('train.cxl')
    createCXL('validation.cxl')


def make_cxls():

    data_directory = './data_for_GED'
    gxl_class_dict = create_class_dict(data_directory)
    addCXLs(gxl_class_dict)

# os.chdir(r'M:\pT1_selected - template_annotated - QuPath_export_cell')
# make_cxls()