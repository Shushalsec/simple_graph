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
            flower = plt.imread(flower_file)  # get the numpy array of the cropped image
        elif '-mask' in file:  # get the annotation mask in the folder
            flower_mask_file = os.path.join(subdirectory, file)  # get the path to the annotation mask image
            annotation_mask = plt.imread(flower_mask_file)  # get the mask as a numpy array
    bool_mask = annotation_mask.astype(bool)  # convert to boolean array from float array
    flower_copy = flower.copy()  # make a copy as the original is read only
    # set the values in the copied image as 0, i.e. black pixel if they are out of the annotation
    flower_copy[bool_mask == False] = 0.0
    # color mask to separate crypts
    min_white = (180, 180, 180)
    max_white = (250, 250, 250)
    crypt_mask = cv2.inRange(flower_copy, min_white, max_white)
    result = cv2.bitwise_and(flower_copy, flower_copy, mask=crypt_mask)
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
    print(subdirectory)
    plt.savefig(os.path.join(subdirectory, '{}-segmentation.png'.format(subdirectory)))
    print(os.path.join(subdirectory, '{}-segmentation.png'.format(subdirectory)))
    fraction_crypty = np.sum(result != 0)/np.sum(flower_copy != 0)
    print('This flower is ~{}% crypt!'.format(int(round(fraction_crypty*100))))
    return fraction_crypty



def crypt_percentage_all(all_dir):
    os.chdir(os.path.join(all_dir, 'masks'))
    for folder in os.listdir():
        if os.path.isdir(folder):
            print('Processing folder {}'.format(folder))
            crypt_percentage = one_crypt_extracter(folder)
            file_object = open(os.path.join(folder, '{}-crypt.txt'.format(folder)), 'w')
            file_object.write(str(crypt_percentage))
            file_object.close()



myfolder = 'M:/ged-shushan/ged-shushan/data/Letter/results'
crypt_percentage_all(myfolder)
one_crypt_extracter(os.path.join(myfolder, 'masks', '287c_B2004.12899_III-B_HE_0_abnormal'))