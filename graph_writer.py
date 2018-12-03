import os
import xml.etree.ElementTree as ET
import pandas as pd
import shutil

def graph_extracter(all_dir):
    masks_dir = os.path.join(all_dir, 'masks')
    class_dict = {}
    for i, folder in enumerate(os.listdir(masks_dir)):
        print('Processing gland', folder)
        #  collect the data per folder or gland
        cells = pd.read_excel(os.path.join(masks_dir, folder, folder+'-detections.xlsx'))
        if i==0:
            attrib_options = {k + 1: v for (k, v) in zip(range(len(list(cells)[3:])), list(cells)[3:])}
            for k, v in attrib_options.items():
                print(k, v)
            attrib_num = int(input('Type the number of the attribute to be included in the graph:    '))
            selected_attrib = attrib_options[attrib_num]
            print('You have selected {} as attribute'.format(selected_attrib))
        crypt_file_path = (os.path.join(masks_dir, folder, folder+'-crypt.txt'))
        crypt_file = open(crypt_file_path, 'r')
        cryptiness = crypt_file.readlines()[0]
        #  save the information about the class in a dictionary entry
        class_dict[folder] = folder.split('_')[-1]
        #  create an xml tree
        root = ET.Element("gxl")
        graph = ET.SubElement(root, "graph", id="graph_{}".format(i), edgeids="false", edgemode="undirected")

        #  define the central node
        node = ET.SubElement(graph, "node", id="_{}".format(0))
        attr = ET.SubElement(node, "attr", name="x")
        _float = ET.SubElement(attr, "float").text = "0"
        attr = ET.SubElement(node, "attr", name="y")
        _float = ET.SubElement(attr, "float").text = "{}".format(cryptiness)
        for node_id, nucleus_color in enumerate(cells[selected_attrib]):
            node = ET.SubElement(graph, "node", id="_{}".format(node_id+1))
            attr = ET.SubElement(node, "attr", name="x")
            _float = ET.SubElement(attr, "float").text = "0"
            attr = ET.SubElement(node, "attr", name="y")
            _float = ET.SubElement(attr, "float").text = "{}".format(nucleus_color)
            edge = ET.SubElement(graph, "edge", _from="_0", _to="_{}".format(node_id+1))
        tree = ET.ElementTree(root)
        tree.write((os.path.join(masks_dir, folder, "{}-graph.xhtml".format(folder))))
        tree.write((os.path.join(masks_dir, folder, "graph_{}.gxl".format(i))))
    return class_dict


def addCXLs(all_dir):
    masks_dir = os.path.join(all_dir, 'masks')
    os.mkdir(os.path.join(all_dir, 'data'))
    data_dir = os.path.join(all_dir, 'data')
    for subfolder in os.listdir(masks_dir):
        source = os.path.join(masks_dir, subfolder)
        for file in os.listdir(source):
            if '.gxl' in file:
                source_file_path = os.path.join(source, file)
                shutil.copy(source_file_path, data_dir)



    data_dict ={'train.cxl' : [], 'test.cxl' : [], 'validation.cxl' : []}

    test_switch = True
    for i, file in enumerate(os.listdir(data_dir)):
        if i%2==0:
            data_dict['train.cxl'].append(file)
        elif test_switch:
            data_dict['test.cxl'].append(file)
            test_switch = False
        else:
            data_dict['validation.cxl'].append(file)
            test_switch = True

    def createCXL(cxl_to_create):
        root = ET.Element('GraphColection')
        fingerprints = ET.SubElement(root, 'fingerprints')
        for gxl_file in data_dict[cxl_to_create]:
            _print = ET.SubElement(fingerprints, '_print', _class=gxl_file)
        tree = ET.ElementTree(root)
        tree.write((os.path.join(data_dir, cxl_to_create)))

    createCXL('test.cxl')
    createCXL('train.cxl')
    createCXL('validation.cxl')


myfolder = 'M:/ged-shushan/ged-shushan/data/Letter/results'

class_dictionary = graph_extracter(myfolder)
