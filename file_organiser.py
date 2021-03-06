"""
Script 1: Add on to the QuPath script to be that exports crops .jpg, annotation masks .png and feature .txt files all in one
directory. This script takes such a directory and sorts files from the same annotation into separate subdirectories
to make things neat and tidy.
This file should be imported as a module and contains the following function:

        *
"""
import shutil
import os
import re
import pandas as pd

def organiser(directory_to_organise):
    """
    The function checks with 2 checkpoints that the files in the directory are intact and complete and moves them to
    separate subdirectories so that each flower data is in a separate folder.
    :param directory_to_organise: the directory containing all the files for every annotation including (1) cropped
    image and (2) annotation mask png per flower/annotation
    :return: None
    """
    files = [file_img for file_img in os.listdir(directory_to_organise) if ('.jpg' in file_img) or ('.png' in file_img)]  # list of image files
    delimiters = '-cropped|-features|-mask'  # file name suffixes to look for
    directory_names = [re.split(delimiters, file)[0] for file in files]  # list of file names with suffixes removed
    # double check that there are 3 of each corresponding to the (1) (2) and (3) files required
    if 2*len(set(directory_names)) == len(directory_names):
        directory_names = list(set(directory_names))
    else:
        print('Check files for missing data!')
    # create the new folders for each annotation
    for directory in directory_names:
        os.mkdir(os.path.join(directory_to_organise, directory))
    # collect all files with same prefix and move them to the corresponding folder
    for identifier in directory_names:
        # just in case one of the file types is missing
        print(identifier)
        try:
            srcname_cropped = os.path.join(directory_to_organise, '{}-cropped.jpg'.format(identifier)) # source path
            srcname_mask = os.path.join(directory_to_organise, '{}-mask.png'.format(identifier)) # source path
            # srcname_features = os.path.join(directory_to_organise, '{}-features.xlsx'.format(identifier)) # source path
            dstname = os.path.join(directory_to_organise, identifier)  # destination folder
            # move files into directories
            shutil.move(srcname_cropped, dstname)
            shutil.move(srcname_mask, dstname)
            # shutil.move(srcname_features, dstname)
            # print('Files moved successfully!')
        except:
            print('Something went wrong with finding files!')


def final_organiser(all_folder):
    masks_folder = os.path.join(all_folder, 'masks')
    organiser(masks_folder)
    detections = pd.read_csv(os.path.join(all_folder, 'detections.txt'), encoding='latin1', sep='\t').drop(columns=['Class'])
    detections.dropna(axis=0, inplace=True, how='any')

    annotations = ['_'.join(file.split('_')[-2:]) for file in os.listdir(masks_folder)]

    folders = os.listdir(masks_folder)
    for annotation in annotations:
        annotation_detections = detections.loc[detections['Name'] == annotation]
        move_to = [s for s in folders if annotation == '_'.join(s.split('_')[-2:])][0]
        pd.DataFrame.to_excel(annotation_detections, os.path.join(masks_folder, move_to, '{}-detections.xlsx'.format(move_to)), index=False)
        if len(annotation_detections)<5:
            shutil.rmtree(os.path.join(masks_folder, move_to))
            print(all_folder, annotation, 'DELETED')

if __name__ == '__main__':
    os.chdir(r'M:\pT1_cell_4')
    PROJECT_DIR = os.getcwd()
    version_name = os.path.basename(os.path.normpath(PROJECT_DIR))
    org_folders = os.path.join(PROJECT_DIR, 'organised_folders')
    for folder in os.listdir(org_folders):
        # if os.path.isdir(os.path.join(PROJECT_DIR, folder)) and folder.endswith(version_name):
        #     if len(os.listdir(os.path.join(PROJECT_DIR, folder)))>0:
        if os.path.isdir(os.listdir(os.path.join(org_folders, folder, 'masks'))[0]):
            print('Skipped folder {}'.format(folder))
        else:
            print('ORGANISING\t', folder)
            final_organiser(os.path.join(org_folders, folder))
# import os
# import pandas as pd
# for folder in os.listdir(r'M:\pT1_cell_1\organised_folders\B16.6031_B_HE\masks'):
#     excel = [f for f in os.listdir(os.path.join(r'M:\pT1_cell_1\organised_folders\B16.6031_B_HE\masks', folder)) if f.endswith('xlsx')][0]
#     excel_path = os.path.join(r'M:\pT1_cell_1\organised_folders\B16.6031_B_HE\masks', folder, excel)
#     print(excel)
#     if not len(pd.read_excel(excel_path)) >0:
#         print('*********', excel, '*********')
# folder_path = r'M:\pT1_cell_3\organised_folders'
# len_dict = {}
# for wsi in os.listdir(folder_path):
#
#     len_dict[wsi]=[len(pd.read_csv(os.path.join(folder_path, wsi, 'detections.txt'), encoding='latin1')), len(os.listdir(os.path.join(folder_path, wsi, 'masks')))]
#
# pd.DataFrame.from_dict(len_dict, orient='index').to_csv(os.path.join(folder_path, 'graph_sizes.csv'))
#
# res={}
# for folder in os.listdir(r'M:\pT1_cell_4\organised_folders'):
#     res[folder]=0
#     df_path = os.path.join(r'M:\pT1_cell_4\organised_folders', folder, 'detections.txt')
#     det = pd.read_csv(df_path, encoding='latin1', sep='\t')
#     groups = det.groupby('Name')
#     for g in groups:
#         res[folder]+=len(g[1])
#     pd.DataFrame(res).to_csv(r'M:\pT1_cell_4\organised_folders\{}\cell_counts.csv'.format(folder))
#
# pd.DataFrame.from_dict(res, orient='index').to_csv(r'M:\pT1_cell_4\cell_counts.csv')
