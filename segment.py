"""
Scripts 2: cryptified

This script allows the user to extract information about the crypts in the given images. It is assumed that the input
is a directory with subdirectories each containing the cropped image region, an image with same magnification for the
mask of annotation from QuPath script output.

This script requires that opencv be installed in the Python environment you are running this script in.

This file should be imported as a module and contains the following function:

    * crypt_data_extracter - returns features of the crypt - fraction that is crypt (at the moment)
"""
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
from decorators import timer
import pandas as pd

def checkpoint(subdir):
    """
    Check if the given subdirectory has all the required documents
    :param subdir: path to the directory
    :return: True or False
    """
    files = os.listdir(subdir)
    if [s for s in os.listdir(subdir) if '-cropped' in s] and [s for s in os.listdir(subdir) if '-mask' in s]:
        print('All images required are present!')
        return True
    else:
        print('Images missing or have been named incorrectly')
        return False


def one_crypt_extracter(subdirectory):
    """
    Function to segment the image into crypt using simple color mask and output the fraction of pixels that are
    classified as crypt out of the total pixels within the annotated region.
    :param subdirectory: subfolder containing only cropped image, its mask and .txt file
    :return: features of crypt - at the moment the fraction of pixels crypt-y (white) enough out of the pixels
    WITHIN the annotated region of the cropped image
    """
    # check if the subdirectory contains the required files
    checkpoint(subdirectory)
    # read images into numpy arrays
    for file in os.listdir(subdirectory):
        if '-cropped' in file:  # get the cropped image from the folder
            flower_file = os.path.join(subdirectory, file)  # get the path to the cropped image file
            flower = cv2.imread(flower_file)  # get the numpy array of the cropped image
        elif '-mask' in file:  # get the annotation mask in the folder
            flower_mask_file = os.path.join(subdirectory, file)  # get the path to the annotation mask image
            annotation_mask = plt.imread(flower_mask_file)  # get the mask as a numpy array

    bool_mask = annotation_mask.astype(bool)  # convert to boolean array from float array
    flower_copy = flower.copy()  # make a copy as the original is read only
    # set the values in the copied image as 0, i.e. black pixel if they are out of the annotation
    flower_copy[bool_mask == False] = 0.0
    # color mask to separate crypts
    flower_hsv = cv2.cvtColor(flower_copy, cv2.COLOR_BGR2HSV)

    min_white = (120, 0, 200)
    max_white = (170, 60, 250)
    mask = cv2.inRange(flower_hsv, min_white, max_white)
    result = cv2.bitwise_and(flower_hsv, flower_hsv, mask=mask)
    #  TODO: try Otsu binarization for segmentation instead of simple thresholding
    # split the plot area into 3 columns and take the left pannel
    plt.subplot(1, 3, 1)
    plt.axis('off')
    plt.imshow(flower)  # original image
    # part 2: middle pannel
    plt.subplot(1, 3, 2)
    plt.axis('off')
    plt.imshow(flower_copy)  # masked image
    # part 3: right pannel
    plt.subplot(1, 3, 3)
    plt.axis('off')
    plt.imshow(result)  # resulting crypt regions identified
    plt.savefig(os.path.join(subdirectory, 'test-segmentation.jpg'))
    fraction_crypty = np.sum(result != 0)/np.sum(flower_copy != 0)
    print('..and is ~{}% crypt!'.format(int(round(fraction_crypty*100))))
    return fraction_crypty

@timer
def crypt_percentage_all(all_dir):
    masks_dir = (os.path.join(all_dir, 'masks'))
    ann_data = pd.read_csv(os.path.join(all_dir, 'annotations.txt'), encoding='latin1', sep='\t')
    ann_data.set_index('Name', inplace = True)
    for col in list(ann_data):
        if 'Centroid X' in col:
            x = col
        elif 'Centroid Y' in col:
            y = col
    for folder in os.listdir(masks_dir):
        folder_path = os.path.join(masks_dir, folder)
        if os.path.isdir(folder_path):
            annotation = '_'.join(folder.split('_')[-2:])
            crypt_x = ann_data.loc[annotation][x]
            crypt_y = ann_data.loc[annotation][y]
            print('This flower is centered at: ', crypt_x, crypt_y)
            crypt_percentage = one_crypt_extracter(folder_path)
            file_object = open(os.path.join(folder_path, '{}-crypt.txt'.format(folder)), 'w')
            file_object.write('{}\n'.format(str(crypt_percentage)))
            file_object.write('{}\n'.format(str(crypt_x)))
            file_object.write('{}\n'.format(str(crypt_y)))
            file_object.close()

#myfolder = 'M:/ged-shushan/ged-shushan/data/Letter/results'
