import pandas as pd
import os
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch
import networkx as nx


def normalise(df):
    """
    :param df: pandas df with the centroid coordinates in columns 1 and 2 and the cell type in column 0
    :return: a dictionary with tissue types as keys and normalised list of coordinates as values
    """

    epi_norm = []  # empty list for the cell centroids that are from epithelium
    other_norm = []  # empty list to add the other type of centroids
    max_x = df.max(axis=0)[1]  # maximum x coordinate value
    max_y = df.max(axis=0)[2]  # maximum y coordinate value
    min_x = df.min(axis=0)[1]  # minimum x coordinate
    min_y = df.min(axis=0)[2]  # minimum y coordinate
    range_x = max_x - min_x  # range of x
    range_y = max_y - min_y  # range of y
    for i, row in df.iterrows():
        x = (row[1] - min_x) / range_x  # normalise
        y = (row[2] - min_y) / range_y  # normalise
        if 'Epithelia' in row[0]:
            epi_norm.append([x, y])  # add to epithelia if epithelial
        else:
            other_norm.append([x, y])  # add to other otherwise
    # save as a dictionary with 2 elements
    output_dict = {'Epithelia': np.array(epi_norm), 'Other': np.array(other_norm)}
    return output_dict


def draw_node(arr, ax, radius=0.01, color='red', alpha=0.5):
    """
    Function for drawing a separate graph (not on top of an image)
    :param arr: array or matrix of [0,1] normalised coordinates
    :param ax: axis on which to add the circle
    :param radius: size of circles
    :param color: color of the circles
    :param alpha: transparency of them circles
    :return: nothing; just draw them circles
    """
    for row in arr:
        x = row[0]  # the first column number = coordinate x
        y = 1 - row[1]  # the y coordinate flipped over because the axis starts from the bottom for y instead of top
        node_circle = Circle((x, y), alpha, radius, color)
        ax.add_patch(node_circle)


def add_node_to_img(row, ax, alpha=0.5, radius=0.01, color='red'):
    """
    Function for drawing ONE circle or node on top of an image
    :param row: row of coordinate set x,y that are [0, 1] normalised
    :param ax: axis on which to draw the image and the circles
    :param alpha: transparency of them circles
    :param radius: circle size
    :param color: circle color
    :return: nothing, just show the image and the circles on top
    """
    ax.imshow(img)  # draw the image
    x = row[0] * ax.get_xlim()[1]  # first coordinate normalised to the image sizes
    y = row[1] * ax.get_ylim()[0]  # second one normalised
    node_circle = Circle((x, y), alpha=alpha, radius=radius, color=color)
    ax.add_patch(node_circle)


def point_dist(row_number, type_coords, th=0.05):
    """
    for 1 line of the xy coordinate matrix identify other coordinates within threshold Manhattan distance from the
    given point
    :param row: one row of the coordinate list
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


def centroids_to_graph(df, image, cell_type='Epithelia', th=2, alpha=0.5, radius=0.01, color='red'):
    coordinates = df[cell_type]  # extract the coordinates of the required tissue type
    print('Centroids selected')
    fig = plt.figure()  # construct a figure
    ax = fig.add_subplot(111)  # get the axis
    ax.imshow(image)  # display the image
    print('image ready for displaying')
    # for each coordinate pair or raw of the coordinate array
    for index, row in enumerate(coordinates):
        print('adding node number {}'.format(index))
        # construct a circle on top of an image that is already displayed
        add_node_to_img(row, ax, alpha, radius, color)
        neighbors = point_dist(row, coordinates, th)  # get the neighbors of the point (row) which are within the limit
        print('Found {} neighbors to link to'.format(len(neighbors)))
        x1, y1 = row[0], row[1]
        # for each point to be connected
        for point in neighbors:
            print(point)
            # coordinates to be connected
            x2 = point[0][0]
            y2 = point[0][1]
            edge = ConnectionPatch((x1, y1), (x2, y2), coordsA='data')
            ax.add_patch(edge)


# directry with the relevant files
# BASE_DIR = 'C:/Users/Shushan/Desktop/MSc/Master Thesis/Cell_graph'
BASE_DIR = 'M:/Cell Graph'
# file with the coordinates of the centroids extracted from QuPath
FILE_NAME = 'polygons_patch.txt'

# pandas dataframe with the coordinates9
data = pd.read_csv(os.path.join(BASE_DIR, FILE_NAME), sep='\t')
# dictionary of coordinates by tissue type
data_dict = normalise(data)
# image file into numpy
image_file: str = 'B14.22816_J_HE.png'
img = plt.imread(os.path.join(BASE_DIR, image_file))


# do all for separate graph
def lonely_graph(centroids_file, threshold, node_size=10, edge_width=0.5):
    tissue = 'Epithelia'
    print('***\nInitializing graph from the dataset')
    data = pd.read_csv(os.path.join(BASE_DIR, centroids_file), sep='\t')
    # dictionary of coordinates by tissue type
    data_dict = normalise(data)
    # flip over the y coordinate
    data_dict[tissue][:, 1] = 1 - data_dict[tissue][:, 1]
    print('Coordinates imported and normalised')
    # create a dictionary with unique node label and its coordinates as keys and values
    pos = arr_to_dict(data_dict[tissue])
    X = nx.Graph()  # generate an empty graph
    X.add_nodes_from(pos.keys())  # add the nodes from the node dictionary
    print('Nodes added')
    # compute the nodes which are within threshold given the Manhattan distance
    for i in range(len(pos)):
        edge = point_dist(i, data_dict[tissue], th=threshold)  # list of edges
        X.add_edges_from(edge)  # edges added to the graph
    print('Edges added')
    fig = plt.figure()
    ax = fig.add_subplot(111)  # plot axes to be passed to the graph drawing function
    ax.set_xlim(0, 1)  # normalise the coordinate system to [0, 1]
    ax.set_ylim(0, 1)
    nx.draw(X, pos=pos, ax=ax, node_size=10, width=edge_width)
    print('Done!\n***')

lonely_graph(FILE_NAME, 0.03)
