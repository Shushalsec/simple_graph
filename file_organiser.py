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


def organiser(directory_to_organise):
    files = os.listdir(directory_to_organise)

    delimiters = '-cropped|-features|-mask'
    directory_names = [re.split(delimiters, file)[0] for file in files]
    if 3*len(set(directory_names)) == len(directory_names):
        directory_names = list(set(directory_names))
    else:
        print('Check files for missing data!')

    for dir in directory_names:
        os.mkdir(os.path.join(directory_to_organise, dir))

    for identifier in directory_names:
        try:
            srcname_cropped = os.path.join(directory_to_organise, '{}-cropped.jpg'.format(identifier))
            srcname_mask = os.path.join(directory_to_organise, '{}-mask.png'.format(identifier))
            srcname_features = os.path.join(directory_to_organise, '{}-features.xlsx'.format(identifier))
            dstname = os.path.join(directory_to_organise, identifier)
            shutil.move(srcname_cropped, dstname)
            shutil.move(srcname_mask, dstname)
            shutil.move(srcname_features, dstname)
        except:
            print('Something went wrong with finding files!')
