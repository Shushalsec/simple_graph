import os
import json
import pandas as pd
import sys

# project_dir = r'M:\pT1_selected - exp1'
project_dir = os.getcwd()


with open(os.path.join(project_dir, 'parameters.txt'), 'r') as parameter_file:
    parameters = json.load(parameter_file)


experiment_name = os.path.basename(os.path.normpath(project_dir))
exp_folders = [folder for folder in os.listdir(project_dir) if folder.endswith(experiment_name) and
               len(os.listdir(os.path.join(project_dir, folder))) > 0]
if len(exp_folders) == 0:
    print('NONE OF THE FOLDERS CONTAIN RESULT FILES!')
    sys.exit()
else:
    path_to_detections = os.path.join(project_dir, exp_folders[0], 'detections.txt')
    cells = pd.read_csv(path_to_detections, encoding="ISO-8859-1", delimiter='\t')
    attrib_options = {k + 1: v for (k, v) in zip(range(len(list(cells)[3:])), list(cells)[3:])}

    for i, attribute_index in enumerate(parameters['node_attr_list']):
        print(attrib_options[int(attribute_index)])
        parameters['attribute_{}'.format(i)] = attrib_options[int(attribute_index)]
    with open(os.path.join(project_dir, 'parameters.txt'), 'w') as parameter_file:
        json.dump(parameters, parameter_file)

