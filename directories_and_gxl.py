import os
import file_organiser
import Class_graphs

if __name__ == '__main__':

    PROJECT_DIR = r'M:\pT1_selected - exp1'
    # PROJECT_DIR = os.getcwd()
    # pooled_data_dir = os.path.join(PROJECT_DIR, 'pooled_image_data')
    version_name = os.path.basename(os.path.normpath(PROJECT_DIR))

    for folder in os.listdir(PROJECT_DIR):
        if os.path.isdir(os.path.join(PROJECT_DIR, folder)) and folder.endswith(version_name) and len(os.listdir(os.path.join(PROJECT_DIR, folder)))>0:
            print('ORGANISING\t', folder)
            file_organiser.final_organiser(os.path.join(PROJECT_DIR, folder))
            Class_graphs.assemble_data(os.path.join(PROJECT_DIR, folder))












