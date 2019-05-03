import os
import json
import shutil
import sys
import CXL
import pandas as pd

def copy_gxl_files_from(src_dir, dst_dir):
    print('COPYING GRAPHS FROM\t', src_dir)
    data_dir = os.path.join(src_dir, 'data')
    for gxl in os.listdir(data_dir):
        shutil.copy(os.path.join(data_dir, gxl), dst_dir)

def copy_results():
    src_dir = 'data_for_GED'
    assert os.listdir(src_dir)
    HIST_DIR = r'M:\ged-shushan\ged-shushan\data\Histology'
    dst_dir = os.path.join(HIST_DIR, 'data_for_GED')
    shutil.copytree(src_dir, dst_dir)

def update_parameters(project_dir, experiment_name):
    exp_folders = [folder for folder in os.listdir(project_dir) if folder.endswith(experiment_name) and
                   len(os.listdir(os.path.join(project_dir, folder))) > 0]
    if len(exp_folders) == 0:
        print('NONE OF THE FOLDERS CONTAIN RESULT FILES!')
        sys.exit()
    else:
        path_to_detections = os.path.join(project_dir, exp_folders[0], 'detections.txt')
        cells = pd.read_csv(path_to_detections, encoding="ISO-8859-1", delimiter='\t')
        attrib_options = {k + 1: v for (k, v) in zip(range(len(list(cells)[3:])), list(cells)[3:])}

        for i, attribute_index in enumerate(parameters['node']['node_attr_list']):
            print(attrib_options[int(attribute_index)])
            parameters['attribute_{}'.format(i)] = attrib_options[int(attribute_index)]
        with open(os.path.join(project_dir, 'parameters.txt'), 'w') as parameter_file:
            json.dump(parameters, parameter_file)


if __name__ == '__main__':

    # PROJECT_DIR = r'M:\pT1_selected - exp1'
    # PROJECT_DIR = r'M:\crypt_to_graph'
    os.chdir(r'M:\pT1_selected - template_annotated - QuPath_export_cell')
    PROJECT_DIR = os.getcwd()
    pooled_data_dir = os.path.join(PROJECT_DIR, 'data_for_GED')
    if len(os.listdir(pooled_data_dir))>0:
        print('CLEAN THE FOLDER data_for_GED!')
        sys.exit()
    version_name = os.path.basename(os.path.normpath(PROJECT_DIR))
    #
    with open(os.path.join(PROJECT_DIR, 'parameters.txt')) as parameter_file:
        parameters = json.load(parameter_file)
    #
    #
    # # if ALL means all the images should be pulled together
    # if parameters['pool_images'] == 'ALL':
    #     for folder in os.listdir(PROJECT_DIR):
    #         if os.path.isdir(os.path.join(PROJECT_DIR, folder)) and folder.endswith(version_name) and len(os.listdir(os.path.join(PROJECT_DIR, folder)))>0:
    #             copy_gxl_files_from(os.path.join(PROJECT_DIR, folder), pooled_data_dir)
    #     CXL.make_cxls()
    #     copy_results()
    #     update_parameters(PROJECT_DIR, version_name)
    if isinstance(parameters['pool_images'], list):
        for folder in parameters['pool_images']:
            copy_gxl_files_from(os.path.join(PROJECT_DIR, folder+'_'+version_name), pooled_data_dir)
        CXL.make_cxls()
        copy_results()
        update_parameters(PROJECT_DIR, version_name)
    else:
        print('ERROR IN PARAMETERS')
        sys.exit()



