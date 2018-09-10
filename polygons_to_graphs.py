import pandas as pd
import os
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance
from matplotlib.patches import ConnectionPatch
from scipy import stats

BASE_DIR = 'M:\Cell Graph'
FILE_NAME = 'polygons.txt'




def normalise(df):
    normalised_e = []
    normlised_o = []
    max_x = data.max(axis=0)[1]
    max_y = data.max(axis=0)[2]
    min_x = data.min(axis=0)[1]
    min_y = data.min(axis=0)[2]
    range_x = max_x - min_x
    range_y = max_y - min_y
    for i, row in data.iterrows():
        x = (row[1] - min_x) / (range_x)
        y = (row[2] - min_y) / (range_y)
        if 'Epithelia' in row[0]:
            normalised_e.append([x, y])
        else:
            normlised_o.append([x, y])
    data_dict = {'Epithelia': np.array(normalised_e),
                 'Other': np.array(normlised_o)}
    return data_dict

def add_node(arr, ax):
    for row in arr:
        node_circle = Circle((row[0], 1-row[1]), radius=50, color='red')
        ax.add_patch(node_circle)

def add_node_to_img(arr, ax):
    for row in arr:
        node_circle = Circle((row[0]*ax.get_xlim()[1], (row[1])*ax.get_ylim()[0]), radius=30, color='red')
        ax.add_patch(node_circle)


data = pd.read_csv(os.path.join(BASE_DIR, FILE_NAME), sep = '\t')
data_dict = normalise(data)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal')
add_node(data_dict['Epithelia'], ax)

x = data_dict['Epithelia'][:,0]
y = data_dict['Epithelia'][:,1]

H, xedges, yedges = np.histogram2d(x,y, bins=100)
H=H.T
plt.imshow(H)
np.histogram(H)
np.max(H)
r = stats.binned_statistic_2d(x, y, None, 'mean')


img_file = 'B14.22816_J_HE.png'
img = plt.imread(os.path.join(BASE_DIR, img_file))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal')
ax.imshow(img)
ax.set_aspect('equal')
add_node_to_img(data_dict['Epithelia'], ax)
