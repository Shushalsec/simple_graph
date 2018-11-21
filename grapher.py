"""

"""
import pandas as pd
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors


patch = cv2.imread('C:/Users/st18l084/Desktop/test_patch.jpg')
plt.imshow(patch)
patch = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB)
plt.imshow(patch)



def one_crypt_extracter(file):
    """
    Function to segment the image into crypt using simple color mask and output the fraction of pixels that are
    classified as crypt out of the total pixels within the annotated region.
    :param subdirectory: subfolder containing only cropped image, its mask and .txt file
    :return: features of crypt - at the moment the fraction of pixels crypt-y (white) enough out of the pixels
    WITHIN the annotated region of the cropped image
    """
    # check if the subdirectory contains the required files
    # read images into numpy arrays
    patch = cv2.imread(os.path.join('C:/Users/st18l084/Desktop', file))
    flower_copy = patch.copy()  # make a copy as the original is read only
    # set the values in the copied image as 0, i.e. black pixel if they are out of the annotation
    # color mask to separate crypts
    min_white = (180, 180, 180)
    max_white = (250, 250, 250)
    crypt_mask = cv2.inRange(flower_copy, min_white, max_white)
    result = cv2.bitwise_and(flower_copy, flower_copy, mask=crypt_mask)
    # split the plot area into 3 columns and take the left pannel
    # plt.subplot(1, 3, 1)
    # plt.axis('off')
    # plt.imshow(patch)  # original image
    # # part 2: middle pannel
    # plt.subplot(1, 3, 2)
    # plt.axis('off')
    # plt.imshow(flower_copy)  # masked image
    # # part 3: right pannel
    # plt.subplot(1, 3, 3)
    # plt.axis('off')
    plt.imshow(result)  # resulting crypt regions identified
    return


one_crypt_extracter('patch2.jpg')