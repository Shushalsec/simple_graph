import pandas as pd
import os
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = 'M:\Cell Graph'
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