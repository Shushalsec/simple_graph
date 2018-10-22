import pandas as pd
import os
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance
from matplotlib.patches import ConnectionPatch
from scipy import stats
import networkx as nx

BASE_DIR = 'C:/Users/st18l084/Dropbox'
FILE_NAME = '366b.xlsx'
IMG = '366a_ann.jpg'






def normalise(df, img_patch):
    normalised = []
    max_x = 20964.2
    max_y = 33671.8
    min_x = 720.66
    min_y = 3267.5
    range_x = max_x - min_x
    range_y = max_y - min_y
    fig = plt.figure(frameon=False)
    ax = fig.add_subplot(111)
    ax.imshow(img_patch)
    ax.axis('equal')
    img_x = ax.get_xlim()[1]
    img_y = ax.get_ylim()[0]
    for i, row in df.iterrows():
        x = (row[1] - min_x) / range_x * img_x  # normalise
        y = (row[2] - min_y) / range_y * img_y  # normalise
        normalised.append([x,y])
    # save as a dictionary with 2 elements
    print('Data normalisation completed')
    return normalised, ax

def add_node(arr, ax):
    for row in arr:
        node_circle = Circle((row[0], 1-row[1]), radius=50, color='red')
        ax.add_patch(node_circle)

def add_node_to_img(arr, ax):
    for row in arr:
        node_circle = Circle((row[0]*ax.get_xlim()[1], (row[1])*ax.get_ylim()[0]), radius=30, color='red')
        ax.add_patch(node_circle)


img = plt.imread(os.path.join(BASE_DIR, IMG))
data = pd.read_excel(os.path.join(BASE_DIR, FILE_NAME))

centr, ax = normalise(data, img)
G = nx.Graph()
G.add_nodes_from([i for i in range(4)])
d = scipy.spatial.distance.pdist(centr)
D = scipy.spatial.distance.squareform(d)
D[D==0.] = np.nan
D
edges = [(a, b) for a, b  in enumerate(np.nanargmin(D, axis = 1))]
pos = {}
for i in range(4):
    pos[i] = centr[i]
pos
G.add_edges_from(edges)
nx.draw(G, pos = pos, node_size = 100)
G.nodes
plt.savefig(os.path.join(BASE_DIR, 'graph'), bbox_inches = 'tight')