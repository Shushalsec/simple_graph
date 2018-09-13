from skimage import data, segmentation
from skimage.future import graph
from matplotlib import pyplot as plt
import os
import cv2

BASE_DIR = 'M:/Cell Graph'
# file with the coordinates of the centroids extracted from QuPath
FILE_NAME = 'polygons_patch.txt'

# pandas dataframe with the coordinates9
# dictionary of coordinates by tissue type
# image file into numpy
image_file: str = 'smaller_patch.png'
img = plt.imread(os.path.join(BASE_DIR, image_file))
blur = cv2.bilateralFilter(img,10,200,200)

labels = segmentation.slic(blur, compactness=30, n_segments=400)
g = graph.rag_mean_color(blur, labels)

fig = plt.figure()  # construct a figure
ax = fig.add_subplot(111)
lc = graph.show_rag(labels, g, blur, ax=ax)
# specify the fraction of the plot area that will be used to draw the colorbar
fig.colorbar(lc, fraction=0.03, ax=ax)



ax.axis('off')

plt.tight_layout()
plt.show()

from skimage.future import graph
from skimage import segmentation, color, filters, io
from matplotlib import pyplot as plt

img = plt.imread(os.path.join(BASE_DIR, image_file))

gimg = color.rgb2gray(img)

labels = segmentation.slic(img, compactness=30, n_segments=400)
edges = filters.sobel(gimg)
edges_rgb = color.gray2rgb(edges)

g = graph.rag_boundary(labels, edges)
lc = graph.show_rag(labels, g, edges_rgb, img_cmap=None, edge_cmap='viridis',
                    edge_width=1.2)

plt.colorbar(lc, fraction=0.03)
io.show()