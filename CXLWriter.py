import os
import xml.etree.ElementTree as ET
import shutil

all_dir = 'M:/ged-shushan/ged-shushan/data/Letter/t'
masks_dir = os.path.join(all_dir, 'masks')
data_dir = os.path.join(all_dir, 'data')
os.listdir(data_dir)
os.mkdir(data_dir)


def addCXLs(all_dir):
    masks_dir = os.path.join(all_dir, 'masks')

    data_dir = os.path.join(all_dir, 'data')
    os.mkdir(data_dir)
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

addCXLs(all_dir)