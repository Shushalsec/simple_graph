from skimage import data, segmentation
from skimage.future import graph
from matplotlib import pyplot as plt


img = plt.imread('C:/Users/Shushan/Desktop/MSc/Master Thesis/RAG/rag1.png')
labels = segmentation.slic(img, compactness=30, n_segments=400)
g = graph.rag_mean_color(img, labels)

fig, ax = plt.subplots(nrows=2, sharex=True, sharey=True, figsize=(6, 8))

ax[0].set_title('RAG drawn with default settings')
lc = graph.show_rag(labels, g, img, ax=ax[0])
# specify the fraction of the plot area that will be used to draw the colorbar
fig.colorbar(lc, fraction=0.03, ax=ax[0])

ax[1].set_title('RAG drawn with grayscale image and viridis colormap')
lc = graph.show_rag(labels, g, img,
                    img_cmap='gray', edge_cmap='viridis', ax=ax[1])
fig.colorbar(lc, fraction=0.03, ax=ax[1])

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()
import cv2
import numpy as np

img = cv2.imread(os.path.join(BASE_DIR, IMG_FILE),0)

thresholded = img<100
thresholded = thresholded.astype(int)
im = np.array(thresholded * 255, dtype = np.uint8)
threshed = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 0)
cv2.imshow('threshed', im)

kernel = np.ones((5,5),np.uint8)
closing = cv2.morphologyEx(im, cv2.MORPH_CLOSE, kernel)
# gradient = cv2.morphologyEx(threshed, cv2.MORPH_GRADIENT, kernel)
# cv2.imshow('threshed', gradient)
opening = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
cv2.imshow('opening', opening)
closing = cv2.morphologyEx(im, cv2.MORPH_CLOSE, kernel)
cv2.imshow('closing', closing)
cv2.imwrite('closed_circles2', closing)
ret, thresh = cv2.threshold(closing, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(im2, contours, -1, (0,255,0), 3)
plt.imshow(opening<90)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

import json
import os

with open('parameters.txt') as parameter_file:
    parameters = json.load(parameter_file)
parameters['main_dir']

with open('parameters.txt', 'w') as parameter_file:
    json.dump(parameters, parameter_file)