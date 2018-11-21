import os
import xml.etree.ElementTree as ET
import pandas as pd


def graph_extracter(all_dir):
    masks_dir = os.path.join(all_dir, 'masks')
    for i, folder in enumerate(os.listdir(masks_dir)):
        print(folder)
        cells = pd.read_excel(os.path.join(masks_dir, folder, folder+'-detections.xlsx'))
        crypt_file_path = (os.path.join(masks_dir, folder, folder+'-crypt.txt'))
        crypt_file = open(crypt_file_path, 'r')
        cryptiness = crypt_file.readlines()[0]


        root = ET.Element("gxl")
        graph = ET.SubElement(root, "graph", id = "graph_{}".format(i), edgeids = "false", edgemode = "undirected")

        #  define the central node
        node = ET.SubElement(graph, "node", id = "_{}".format(0))
        attr = ET.SubElement(node, "attr", name = "x")
        float = ET.SubElement(attr, "float").text = "0"
        attr = ET.SubElement(node, "attr", name="y")
        float = ET.SubElement(attr, "float").text = "{}".format(cryptiness)
        for node_id, nucleus_color in enumerate(cells['Nucleus: Hematoxylin OD mean']):
            node = ET.SubElement(graph, "node", id = "_{}".format(node_id+1))
            attr = ET.SubElement(node, "attr", name = "x")
            float = ET.SubElement(attr, "float").text = "0"
            attr = ET.SubElement(node, "attr", name="y")
            float = ET.SubElement(attr, "float").text = "{}".format(nucleus_color)
            edge = ET.SubElement(graph, "edge", _from="_0", _to="_{}".format(node_id+1))
        tree = ET.ElementTree(root)
        tree.write((os.path.join(masks_dir, folder, "{}-gland.xhtml".format(folder))))
        tree.write((os.path.join(masks_dir, folder,"gland_{}.gxl".format(i))))

