import os
import json
import shutil
import sys

def copy_gxl_files_from(src_dir, dst_dir):
    print('COPYING GRAPHS FROM\t', src_dir)
    data_dir = os.path.join(src_dir, 'data')
    for gxl in os.listdir(data_dir):
        shutil.copy(os.path.join(data_dir, gxl), dst_dir)


if __name__ == '__main__':

    # PROJECT_DIR = r'M:\pT1_selected - exp1'
    PROJECT_DIR = os.getcwd()
    pooled_data_dir = os.path.join(PROJECT_DIR, 'pooled_image_data')
    version_name = os.path.basename(os.path.normpath(PROJECT_DIR))

    with open(os.path.join(PROJECT_DIR, 'parameters.txt')) as parameter_file:
        parameters = json.load(parameter_file)


    # if ALL means all the images should be pulled together
    if parameters['pool_images'] == 'ALL':
        for folder in os.listdir(PROJECT_DIR):
            if os.path.isdir(os.path.join(PROJECT_DIR, folder)) and folder.endswith(version_name) and len(os.listdir(os.path.join(PROJECT_DIR, folder)))>0:
                copy_gxl_files_from(os.path.join(PROJECT_DIR, folder), pooled_data_dir)
    elif isinstance(parameters['pool_images'], list):
        for folder in parameters['pool_images']:
            copy_gxl_files_from(os.path.join(PROJECT_DIR, folder), pooled_data_dir)
    else:
        print('ERROR IN PARAMETERS')
        sys.exit()



