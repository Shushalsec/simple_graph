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
import sys

def organiser(directory_to_organise):
    """
    The function checks with 2 checkpoints that the files in the directory are intact and complete and moves them to
    separate subdirectories so that each flower data is in a separate folder.
    :param directory_to_organise: the directory containing all the files for every annotation including (1) cropped
    image and (2) annotation mask png per flower/annotation
    :return: None
    """
    files = os.listdir(directory_to_organise)  # list of files
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
            srcname_cropped = os.path.join(directory_to_organise, '{}-cropped.png'.format(identifier)) # source path
            srcname_mask = os.path.join(directory_to_organise, '{}-mask.png'.format(identifier)) # source path
            # srcname_features = os.path.join(directory_to_organise, '{}-features.xlsx'.format(identifier)) # source path
            dstname = os.path.join(directory_to_organise, identifier)  # destination folder
            # move files into directories
            shutil.move(srcname_cropped, dstname)
            shutil.move(srcname_mask, dstname)
            # shutil.move(srcname_features, dstname)
            print('Files moved successfully!')
        except:
            print('Something went wrong with finding files!')



def final_organiser(all_folder):
    masks_folder = os.path.join(all_folder, 'masks')
    organiser(masks_folder)
    detections = pd.read_csv(os.path.join(all_folder, 'detections.txt'), encoding='latin1', sep='\t')

    annotations = ['_'.join(file.split('_')[-2:]) for file in os.listdir(masks_folder)]
    folders = os.listdir(masks_folder)
    for annotation in annotations:
        annotation_detections = detections.loc[detections['Name'] == annotation]
        print(annotation)
        move_to = [s for s in folders if annotation in s][0]
        pd.DataFrame.to_excel(annotation_detections, os.path.join(masks_folder, move_to, '{}-detections.xlsx'.format(move_to)), index=False)

myfolder = 'M:/ged-shushan/ged-shushan/data/Letter/results'

final_organiser(myfolder)