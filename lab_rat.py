import os
import pandas as pd
from GraphBuilder import *
import CXL
import json
import random
import numpy as np
import sys
import networkx as nx
import matplotlib.pyplot as plt


def create_folder(path):
    if os.path.isdir(path):
        print('CHECK THE DATA ALREADY PRESENT IN {}'.format(exp_folder))
        sys.exit()
    else:
        os.mkdir(path)


def add_sets_to(parameters):
    random.seed(parameters['split_seed'])
    L = parameters['pool_images'].copy()
    parameters['train_set'] = [L.pop(random.randrange(len(L))) for _ in range(round(len(L)/2))]
    parameters['val_set'] = [L.pop(random.randrange(len(L))) for _ in range(round(len(L)/2))]
    parameters['test_set'] = L


def get_stats_for(attribute, parameters):
    train_data_attr = []

    for wsi in parameters['train_set']:
        detections_path = os.path.join(organised_folders, wsi, 'detections.txt')
        detections = pd.read_csv(detections_path, sep='\t', encoding = 'unicode_escape')
        train_data_attr = train_data_attr + list(detections.iloc[:,attribute])
    train_data_np = np.array(train_data_attr)
    mean = train_data_np.mean()
    sd = train_data_np.std()
    return mean, sd, list(detections)[attribute]

def normalise_and_regiter_attributes(parameters):
    parameters['node']['attr_mean'] = []
    parameters['node']['attr_sd'] = []
    parameters['node']['attr_names'] = []
    for i, attribute in enumerate(parameters['node']['node_attr_list']):
        mean, sd, feature = get_stats_for(attribute, parameters)
        parameters['node']['attr_mean'].append(mean)
        parameters['node']['attr_sd'].append(sd)
        parameters['node']['attr_names'].append(feature)


def assemble_data(wsi_folder, parameters):

    masks = os.path.join(wsi_folder, 'masks')
    for subdirectory in os.listdir(masks):
        graph_dir = os.path.join(masks, subdirectory)
        one_graph = Graph(graph_dir, parameters)
        one_graph.self_assemble()
        i = subdirectory.split('_')[-2]
        one_XML = XML(one_graph, gxl_folder, graph_id=i)
        one_XML.XML_writer('gxl')


def collect_gxls_in(set_name, parameters):
    set_gxls = []
    for folder in parameters[set_name]:
        set_gxls = set_gxls + [file+'.gxl' for file in os.listdir(os.path.join(organised_folders, folder, 'masks'))]
    return set_gxls

def createCXL(cxl_to_create, list_of_gxls, data_dir):
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


os.chdir(r'M:\pT1_selected - complete_annotation')

exp_folder = 'experiment_f9'
gxl_folder = os.path.join(exp_folder, 'gxl')

create_folder(gxl_folder)

organised_folders = 'organised_folders'

param_path = os.path.join(exp_folder, 'parameters.txt')
with open(param_path) as parameter_file:
    graph_parameters = json.load(parameter_file)

add_sets_to(graph_parameters)
normalise_and_regiter_attributes(graph_parameters)

for wsi in os.listdir(organised_folders):
    assemble_data(os.path.join(organised_folders, wsi), graph_parameters)

for set_type in ['train_set', 'val_set', 'test_set']:
    set_files = collect_gxls_in(set_type, graph_parameters)
    createCXL(set_type+'.cxl', set_files, gxl_folder)

# with open(os.path.join(project_dir, 'parameters.txt'), 'w') as parameter_file:
#     json.dump(parameters, parameter_file)