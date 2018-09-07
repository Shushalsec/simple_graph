import Class_graphs
import Image_dictionary
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import matplotlib.pyplot as plt


points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]])

vor = Voronoi(points)
voronoi_plot_2d(vor, ax=ax)
plt.show()


#extract excel file data with coordinates and other features
data_file = 'd.xlsx'
data_dir = 'C:/Users/Shushan/Desktop'
data = pd.read_excel(os.path.join(data_dir, data_file))

#import the image
img_file = 'B14.22816PCK.png'
img = plt.imread(os.path.join(data_dir, img_file))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal')
ax.imshow(img)

#save the excel data with normalised coordinates, area and perimeter data for each node
graph_data = Image_dictionary.extract_dictionary(data, img)
n_d = graph_data[0]
n = Class_graphs.Node(n_d[0],n_d[1],[3])
n.draw_nodes(img)
