import pandas as pd
import os
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch
import networkx as nx

def normalise_to_img(df, img_patch):
    """
    normalise the dataset ready for extracting a graph to be pasted on an image
    :param df: dataset ex
    :param img_patch:
    :return:
    """
    epi_norm = []  # empty list for the cell centroids that are from epithelium
    other_norm = []  # empty list to add the other type of centroids
    max_x = 12283.1  # maximum x coordinate value
    max_y = 25592.9  # maximum y coordinate value
    min_x = 10559.1  # minimum x coordinate
    min_y = 24589.2  # minimum y coordinate
    range_x = max_x - min_x  # range of x
    range_y = max_y - min_y  # range of y
    # fig = plt.figure()
    fig = plt.figure(frameon=False)
    ax = fig.add_subplot(111)
    ax.imshow(img_patch)
    ax.axis('equal')
    img_x = ax.get_xlim()[1]
    img_y = ax.get_ylim()[0]
    print(img_x, img_y)
    for i, row in df.iterrows():
        x = (row[1] - min_x) / range_x * img_x  # normalise
        y = (row[2] - min_y) / range_y * img_y  # normalise
        if 'Epithelia' in row[0]:
            epi_norm.append([x, y])  # add to epithelia if epithelial
        else:
            other_norm.append([x, y])  # add to other otherwise
    # save as a dictionary with 2 elements
    output_dict = {'Epithelia': np.array(epi_norm), 'Other': np.array(other_norm)}
    return output_dict, ax

def point_dist(row_number, type_coords, th=0.05):
    """
    for 1 line of the xy coordinate matrix identify other coordinates within threshold Manhattan distance from the
    given point
    :param row_number: index of one row of the coordinate list
    :param type_coords: coordinate array for one type of tisue that is of interest
    :param th: threshold withing which the search for points is done
    :return: coordinates of points close enough to the given row point
    """
    d1 = type_coords[row_number][0]  # separate the x
    d2 = type_coords[row_number][1]  # the y
    # make a mask for filtering the points which are
    # within the threshold (in either direction) for both x and y coordinates
    all_x = type_coords[:, 0]
    all_y = type_coords[:, 1]
    mask = np.argwhere((np.abs(d1 - all_x) < th) & (np.abs(d2 - all_y) < th))
    node_pair = [i[0] for i in mask]
    current_node = [row_number] * len(node_pair)
    result = list(zip(node_pair, current_node))
    return result  # output the actual values of the coordiantes from the original array


def arr_to_dict(arr):
    # write node coordinates to a dictionary
    pos = {k: v for k, v in enumerate(arr)}
    return pos

    # per node compute neighbors
    # per node write neighbors to file

def gi(df, image, threshold):
    """
    Overlay the graph on top of a patch
    :param centroids_file: .txt with centroids and tissue type from QuPath
    :param image: image in numpy array
    :param threshold: limit for connection edges, has to be around 300 to make connections
    :return:
    """
    tissue = 'Other'
    print('***\nInitializing graph from the dataset')
    # dictionary of coordinates by tissue type
    data_dict, ax = normalise_to_img(df, image)
    print('Coordinates imported and normalised')
    # create a dictionary with unique node label and its coordinates as keys and values
    pos = arr_to_dict(data_dict[tissue])
    x = nx.Graph()  # generate an empty graph
    x.add_nodes_from(pos.keys())  # add the nodes from the node dictionary
    print('Nodes added')
    # compute the nodes which are within threshold given the Manhattan distance
    for i in range(len(pos)):
        print('Starting edge calculations...')
        edge = point_dist(i, data_dict[tissue], th=threshold)  # list of edges
        print('**************\n', edge)
        x.add_edges_from(edge)
    nx.draw(x, pos=pos, ax=ax, node_size=7, node_color='lime', alpha=0.8, width=1.2, edge_color='lime')
    # plt.savefig(os.path.join(BASE_DIR, 'Graph and image {}'.format(centroids_file.split('.', 1)[0])), dpi=1000)

BASE_DIR = 'C:/Users/Shushan/Desktop/MSc/Master Thesis/presentation 27.09'

# file with the coordinates of the centroids extracted from QuPath
FILE_NAME = 'f.xlsx'
IMG_FILE = 'supercells.png'
# image file with the patch to be used for overlaying the graph
# IMG_FILE = '06_1.png'
# lonely_graph(FILE_NAME, 0.03)
# image as a numpy array
img = plt.imread(os.path.join(BASE_DIR, IMG_FILE))
# dataset of centroids with the cell types
data = pd.read_excel(os.path.join(BASE_DIR, FILE_NAME))


gi(data, img, 500)