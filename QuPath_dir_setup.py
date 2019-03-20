import os

# QUPATH_DIR = 'M:\pT1_selected - Copy'
QUPATH_DIR = os.getcwd()
project_name = os.path.basename(os.path.normpath(QUPATH_DIR))


for image_file in os.listdir(os.path.join(QUPATH_DIR, 'data')):
    image_folder = image_file.split('.qpdata')[0] + '_' + project_name
    if not os.path.exists(os.path.join(QUPATH_DIR, image_folder)):
        os.makedirs(os.path.join(QUPATH_DIR, image_folder))
        print('CREATED DIRECTORY CALLED:\t', image_folder)
