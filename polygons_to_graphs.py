import pandas as pd
import os
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance
from matplotlib.patches import ConnectionPatch

BASE_DIR = 'C:/Users/Shushan/Downloads'
FILE_NAME = 'polygons_2.txt'




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

def add_node(row, ax):
    node_circle = Circle((row[0], row[1]), radius=0.01, color='red')
    ax.add_patch(node_circle)


data = pd.read_csv(os.path.join(BASE_DIR, FILE_NAME), sep = '\t')
data_dict = normalise(data)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal')
add_node(data.iloc[0], ax)
add_node(data_dict['Epithelia'][0], ax)
r = data_dict['Epithelia'][0]
node_circle = Circle((r[0], r[1]), radius=0.01, color='red')
ax.add_patch(node_circle)
plt.imshow()

d = np.array([[1, 1], [2,3], [4, 3], [1, 6], [1,1]])
# def sliding_box(np_xy, step_x, step_y, overlap):
d
d_tuple = tuple(map(tuple, d))
x_min, y_min = d.min(axis=0)
x_max, y_max = d.max(axis=0)
x = d[:,0]
y = d[:,1]
th = 2
d_matrix = d
#for 1 line of the xy coordinate matrix identify other coordinates within threshold Manhattan distance from the given point
def point_dist(row):
    d1 = row[0] #separate the x
    d2 = row[1] # the y
    # print('x range is ', d1-th, ":", d1+th)
    # print('y range is ', d2-th, ":", d2+th)
    #make a mask for filtering the points which are within the threshold (in either direction) for both x and y coordinates
    mask = np.argwhere(((d1+th>=d_matrix[:,0]) & (d1-th<=d_matrix[:,0])) &
                       ((d2+th>=d_matrix[:,1]) & (d1-th<=d_matrix[:,1])))
    return (d_matrix[mask]) # output the indices and the actual values of the coordiantes


for row in d:
    connect_to = point_dist(row)
    for point in connect_to:
        edge = ConnectionPatch((point[0], point[1]), coordsA='data')
        ax.add_patch(edge)


# step = 1
# box_size = 2
# for i in range(x_min, x_max, step):
#     for j in range(y_min, y_max, step):
#         mask = np.argwhere((i<=x) & ((i+box_size)>x) & (j<=y) & ((j+box_size)>=y))
#         patch = d[mask]
#         dist = scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(patch))
#         closest
        # print(i, ':', i+box_size, j, ':', j+box_size, 'found this  ', mask)




x_edges = list(range(x_min, x_max))
scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(d))
H, xedges, yedges = np.histogram2d(d[:,0], d[:,1], bins=(1, 1))