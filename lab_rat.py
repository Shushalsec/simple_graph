from GraphBuilder import *
import random
import numpy as np
import sys


def replace_slashes(path):
    return path.replace('\\', '/')

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




def normalise_and_regiter_attributes(parameters, wsi_collection_dir):
    parameters['node']['attr_mean'] = []
    parameters['node']['attr_sd'] = []
    parameters['node']['attr_names'] = []

    def get_stats_for(attribute):
        train_data_attr = []

        for wsi in parameters['train_set']:
            detections_path = os.path.join(wsi_collection_dir, wsi, 'detections.txt')
            detections = pd.read_csv(detections_path, sep='\t', encoding='unicode_escape')
            train_data_attr = train_data_attr + list(detections.iloc[:, attribute])
        train_data_np = np.array(train_data_attr)
        mean = train_data_np.mean()
        sd = train_data_np.std()
        return mean, sd, list(detections)[attribute]

    for i, attribute in enumerate(parameters['node']['node_attr_list']):
        mean, sd, feature = get_stats_for(attribute)
        parameters['node']['attr_mean'].append(mean)
        parameters['node']['attr_sd'].append(sd)
        parameters['node']['attr_names'].append(feature)


def assemble_data(wsi_folder, parameters, gxl_folder_path):

    masks = os.path.join(wsi_folder, 'masks')
    random.seed(parameters['sampling_seed'])
    folders_normal = [folder for folder in os.listdir(masks) if 'abnormal' not in folder]
    folders_abnormal = [folder for folder in os.listdir(masks) if 'abnormal' in folder]
    folders_sampled_normal = random.sample(folders_normal, round(parameters['included_data_fraction']*len(folders_normal)))
    folders_sampled_abnormal = random.sample(folders_abnormal, round(parameters['included_data_fraction']*len(folders_abnormal)))
    for subdirectory in folders_sampled_abnormal + folders_sampled_normal:
        print('Creating graph from', subdirectory)
        graph_dir = os.path.join(masks, subdirectory)
        one_graph = Graph(graph_dir, parameters)
        one_graph.self_assemble()
        i = subdirectory.split('_')[-2]
        one_XML = XML(one_graph, gxl_folder_path, graph_id=i)
        one_XML.XML_writer('gxl')

def collect_gxls_in(set_name, parameters, gxl_folder_path):
    set_gxls = []
    for wsi in parameters[set_name]:
        set_gxls = set_gxls + [file for file in os.listdir(gxl_folder_path) if wsi in file]
    return set_gxls

def createCXL(cxl_to_create, list_of_gxls, data_dir, parameters):
    root = ET.Element('GraphCollection')  # xml root
    fingerprints = ET.SubElement(root, 'fingerprints')  # xml child
    # for each .gxl in the list of the graphs saved in the dictionary
    for gxl in list_of_gxls:
        # child of fingerprints child with attributes file name and class type
        _print = ET.SubElement(fingerprints, '_print', _file=gxl, _class=gxl.split('_')[-1].split('.gxl')[0])
    # save the graph
    tree = ET.ElementTree(root)
    tree.write((os.path.join(data_dir, cxl_to_create+'.cxl')))
    print(cxl_to_create, 'has', len(list_of_gxls), 'graphs!')


os.chdir(r'M:\pT1_selected-complete_annotation')  # directory with most recent QuPath outputs

exp_folder = 'experiment_100'  # one example folder TODO: loop through all the experiment folders

# reset the paths in the GED software .prop file

source_path = replace_slashes(os.path.join(os.getcwd(), exp_folder, 'gxl', 'val_set.cxl'))
target_path = replace_slashes(os.path.join(os.getcwd(), exp_folder, 'gxl', 'val_set.cxl'))
path_path = replace_slashes(os.path.join(os.getcwd(), exp_folder, 'gxl'))
result_path = replace_slashes(os.path.join(os.getcwd(), exp_folder, 'results'))

prop_path = os.path.join(exp_folder, 'letters-hed.prop')
with open(prop_path, 'r') as file:
    file_lines = file.readlines()

for i, line in enumerate(file_lines):
    if 'source' in line:
        file_lines[i] = 'source={}'.format(source_path) + '\n'
    if 'target' in line:
        file_lines[i] = 'target={}'.format(target_path) + '\n'
    if line[:4]=='path':
        file_lines[i] = 'path={}'.format(path_path) + '/' + '\n'
    if 'result' in line:
        file_lines[i] = 'result={}'.format(result_path) + '/' + '\n'

with open(prop_path, 'w') as file_to_write:
    for item in file_lines:

        file_to_write.write(str(item))

gxl_folder = os.path.join(exp_folder, 'gxl')
#
create_folder(gxl_folder)
#
organised_folders = 'organised_folders'
#
param_path = os.path.join(exp_folder, 'parameters.txt')
with open(param_path) as parameter_file:
    graph_parameters = json.load(parameter_file)

add_sets_to(graph_parameters)
normalise_and_regiter_attributes(graph_parameters, organised_folders)

for wsi in os.listdir(organised_folders):
    assemble_data(os.path.join(organised_folders, wsi), graph_parameters, gxl_folder)

for set_type in ['train_set', 'val_set', 'test_set']:
    set_files = collect_gxls_in(set_type, graph_parameters, gxl_folder)
    createCXL(set_type, set_files, gxl_folder, graph_parameters)


random.seed(graph_parameters['sampling_seed'])


# with open(param_path, 'w') as parameter_file:
#     json.dump(graph_parameters, parameter_file)