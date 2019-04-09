import os
import file_organiser
import Class_graphs

if __name__ == '__main__':
    os.chdir(r'M:\pT1_selected - template_annotated - QuPath_export_cell')
    # PROJECT_DIR = r'M:\crypt_to_graph'
    PROJECT_DIR = os.getcwd()
    # pooled_data_dir = os.path.join(PROJECT_DIR, 'pooled_image_data')
    version_name = os.path.basename(os.path.normpath(PROJECT_DIR))

    for folder in os.listdir(PROJECT_DIR):
        print(folder, os.path.isdir(os.path.join(PROJECT_DIR, folder)), version_name in folder)
        if os.path.isdir(os.path.join(PROJECT_DIR, folder)) and folder.endswith(version_name):
            if len(os.listdir(os.path.join(PROJECT_DIR, folder)))>0:
                if 'data' in os.listdir(os.path.join(PROJECT_DIR, folder)):
                    print('Graphs already present, rename the data folder!')
                    # Class_graphs.assemble_data(os.path.join(PROJECT_DIR, folder))
                else:
                    print('ORGANISING\t', folder)
                    Class_graphs.assemble_data(os.path.join(PROJECT_DIR, folder))


