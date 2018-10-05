import pandas as pd
import os
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
#
#
def normalise(df, normalisation_factor_x=1, normalisation_factor_y=1):
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
        x = (row[1] - min_x) / range_x *normalisation_factor_x  # normalise
        y = (row[2] - min_y) / range_y *normalisation_factor_y  # normalise
        if 'Epithelia' in row[0]:
            epi_norm.append([x, y])  # add to epithelia if epithelial
        else:
            other_norm.append([x, y])  # add to other otherwise
    # save as a dictionary with 2 elements
    output_dict = {'Epithelia': np.array(epi_norm), 'Other': np.array(other_norm)}
    return output_dict

#
def normalise_to_img(df, img_patch):
    """
    normalise the dataset ready for extracting a graph to be pasted on an image
    :param df: dataset ex
    :param img_patch:
    :return:
    """
    epi_norm = []  # empty list for the cell centroids that are from epithelium
    other_norm = []  # empty list to add the other type of centroids
    max_x = df.max(axis=0)[1]  # maximum x coordinate value
    max_y = df.max(axis=0)[2]  # maximum y coordinate value
    min_x = df.min(axis=0)[1]  # minimum x coordinate
    min_y = df.min(axis=0)[2]  # minimum y coordinate
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

# def draw_node(arr, ax, radius=0.01, color='red', alpha=0.5):
#     """
#     Function for drawing a separate graph (not on top of an image)
#     :param arr: array or matrix of [0,1] normalised coordinates
#     :param ax: axis on which to add the circle
#     :param radius: size of circles
#     :param color: color of the circles
#     :param alpha: transparency of them circles
#     :return: nothing; just draw them circles
#     """
#     for row in arr:
#         x = row[0]  # the first column number = coordinate x
#         y = 1 - row[1]  # the y coordinate flipped over because the axis starts from the bottom for y instead of top
#         node_circle = Circle((x, y), alpha, radius, color)
#         ax.add_patch(node_circle)


# def add_node_to_img(row, ax, alpha=0.5, radius=0.01, color='red'):
#     """
#     Function for drawing ONE circle or node on top of an image
#     :param row: row of coordinate set x,y that are [0, 1] normalised
#     :param ax: axis on which to draw the image and the circles
#     :param alpha: transparency of them circles
#     :param radius: circle size
#     :param color: circle color
#     :return: nothing, just show the image and the circles on top
#     """
#     ax.imshow(img)  # draw the image
#     x = row[0] * ax.get_xlim()[1]  # first coordinate normalised to the image sizes
#     y = row[1] * ax.get_ylim()[0]  # second one normalised
#     node_circle = Circle((x, y), alpha=alpha, radius=radius, color=color)
#     ax.add_patch(node_circle)


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


# def centroids_to_graph(df, image, cell_type='Epithelia', th=2, alpha=0.5, radius=0.01, color='red'):
#     coordinates = df[cell_type]  # extract the coordinates of the required tissue type
#     print('Centroids selected')
#     fig = plt.figure()  # construct a figure
#     ax = fig.add_subplot(111)  # get the axis
#     ax.imshow(image)  # display the image
#     print('image ready for displaying')
#     # for each coordinate pair or raw of the coordinate array
#     for index, row in enumerate(coordinates):
#         print('adding node number {}'.format(index))
#         # construct a circle on top of an image that is already displayed
#         add_node_to_img(row, ax, alpha, radius, color)
#         neighbors = point_dist(row, coordinates, th)  # get the neighbors of the point (row) which are within the limit
#         print('Found {} neighbors to link to'.format(len(neighbors)))
#         x1, y1 = row[0], row[1]
#         # for each point to be connected
#         for point in neighbors:
#             print(point)
#             # coordinates to be connected
#             x2 = point[0][0]
#             y2 = point[0][1]
#             edge = ConnectionPatch((x1, y1), (x2, y2), coordsA='data')
#             ax.add_patch(edge)


# do all for separate graph
def lonely_graph(centroids_file, g_threshold, g_node_size=10, g_edge_width=0.5):
    """
    Grpah without the image
    :param centroids_file: QuPath output file for centorid detection
    :param g_threshold: threshold for connecting nodes
    :param g_node_size: node size
    :param g_edge_width: width of the edges
    :return: nothing. just shows the image and saves .gml for the graph and .png for the image
    """
    tissue = 'Epithelia'
    print('***\nInitializing graph from the dataset')
    centroid_dataset = pd.read_csv(os.path.join(BASE_DIR, centroids_file), sep='\t')
    # dictionary of coordinates by tissue type
    data_dict = normalise(centroid_dataset)
    # flip over the y coordinate
    data_dict[tissue][:, 1] = 1 - data_dict[tissue][:, 1]
    print('Coordinates imported and normalised')
    # create a dictionary with unique node label and its coordinates as keys and values
    pos = arr_to_dict(data_dict[tissue])
    x = nx.Graph()  # generate an empty graph
    x.add_nodes_from(pos.keys())  # add the nodes from the node dictionary
    print('Nodes added')
    # compute the nodes which are within threshold given the Manhattan distance
    for i in range(len(pos)):
        edge = point_dist(i, data_dict[tissue], th=g_threshold)  # list of edges
        x.add_edges_from(edge)  # edges added to the graph
    print('Edges added')
    fig = plt.figure()
    ax = fig.add_subplot(111)  # plot axes to be passed to the graph drawing function
    ax.set_xlim(0, 1)  # normalise the x coordinate to [0, 1]
    ax.set_ylim(0, 1)  # normalise the y coordinate to [0, 1]
    nx.draw(x, pos=pos, ax=ax, node_size=g_node_size, width=g_edge_width)
    nx.write_gml(x, os.path.join(BASE_DIR, '{}.gml'.format(centroids_file.split('.', 1)[0])))
    plt.savefig(os.path.join(BASE_DIR, 'Graph {}'.format(centroids_file.split('.', 1)[0])), dpi=1000)
    print('Done!\n***')


def standardise_path(file_name):
    return file_name.replace('\\', '/')


def graph_and_image(centroids_file, image, threshold, show_centrality, tissue = 'Epithelia'):
    """
    Overlay the graph on top of a patch
    :param show_centrality: True if want to add centrality to the plot
    :param centroids_file: .txt with centroids and tissue type from QuPath
    :param image: image in numpy array
    :param threshold: limit for connection edges, has to be around 300 to make connections
    :return:
    """
    print('***\nInitializing graph from the dataset')
    centroid_dataset = pd.read_csv(os.path.join(BASE_DIR, centroids_file), sep='\t')
    # dictionary of coordinates by tissue type
    data_dict, ax = normalise_to_img(centroid_dataset, image)
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
    nx.draw(x, pos=pos, ax=ax, node_size=7, node_color='lime', alpha=0.8, width=0.8, edge_color='lime')
    if show_centrality:
        centrality_values = nx.algorithms.centrality.degree_centrality(x)
        values = [centrality_values.get(node, 0.25) for node in x.nodes()]
        nx.draw(x, pos=pos, ax=ax, node_size=100, cmap=plt.get_cmap('Purples'), node_color=values)
    plt.savefig(os.path.join(BASE_DIR, 'Graph and image {}'.format(centroids_file.split('.', 1)[0])), dpi=1000)
    return (x, pos)

# def hierarchical_graph(centoid_df_file, circle_radius, edge_width, grid_size=0.1, min_cluster_size=3, edge_threshold=0.1, circle_alpha=0.5):
#     tissue = 'Epithelia'
#     dataframe_of_centroids = pd.read_csv(os.path.join(BASE_DIR, centoid_df_file), sep='\t')
#     data_dictionary = normalise(dataframe_of_centroids)
#     data_dictionary[tissue][:, 1] = 1 - data_dictionary[tissue][:, 1]
#     centroids = data_dictionary['Epithelia']
#     super_centroids = []
#     x_centroids = centroids[:, 0]
#     y_centroids = centroids[:, 1]
#     x_min = np.min(x_centroids)
#     x_max = np.max(x_centroids)
#     y_min = np.min(y_centroids)
#     y_max = np.max(y_centroids)
#     print(x_min, x_max, y_min, y_max)
#     x_grid = np.arange(x_min, x_max, grid_size)
#     y_grid = np.arange(y_min, y_max, grid_size)
#     print('x grid is: ', x_grid)
#     print('y grid is: ', y_grid)
#     counter = 0
#     for x in x_grid:
#         for y in y_grid:
#             n = np.where(
#                 (x < centroids[:, 0]) &
#                 (centroids[:, 0] < (x+grid_size)) &
#                 (y < centroids[:, 1]) &
#                 (centroids[:, 1] < (y + grid_size)))
#             if len(n[0]) > min_cluster_size:
#                 super_centroids.append((np.average(centroids[n[0]], axis=0)))
#             counter+=len(n)
#             print(counter)
#     n_s_centr = np.array(super_centroids)
#     super_dict = arr_to_dict(super_centroids)
#     x = nx.Graph()
#     x.add_nodes_from(super_dict.keys())
#     print('Hierarchical graph has ', x.number_of_nodes(), 'nodes')
#     for i in range(len(super_dict)):
#         edge = point_dist(i, n_s_centr, th=edge_threshold)  # list of edges
#         x.add_edges_from(edge)  #
#     fig = plt.figure()
#     ax = fig.add_subplot(111)  # plot axes to be passed to the graph drawing function
#     ax.set_xlim(0, 1)  # normalise the x coordinate to [0, 1]
#     ax.set_ylim(0, 1)  # normalise the y coordinate to [0, 1]
#     nx.draw(x, pos=super_dict, ax=ax, width = edge_width, alpha=circle_alpha, node_size=circle_radius)
#     nx.write_gml(x, os.path.join(BASE_DIR, 'test.gml'))
#     plt.savefig(os.path.join(BASE_DIR, 'Hierarchical graph of {} file with {} nodes.svg'.format(centoid_df_file.split('.', 1)[0], x.number_of_nodes())), dpi=1000)

# def hierarchical_graph_and_img(centoid_df_file, img, circle_radius, edge_width, grid_size=0.1, min_cluster_size=3, edge_threshold=0.1, circle_alpha=0.5):
#     tissue = 'Epithelia'
#     dataframe_of_centroids = pd.read_csv(os.path.join(BASE_DIR, centoid_df_file), sep='\t')
#     data_dictionary, ax = normalise_to_img(dataframe_of_centroids, img)
#     data_dictionary[tissue][:, 1] = 1 - data_dictionary[tissue][:, 1]
#     centroids = data_dictionary['Epithelia']
#     super_centroids = []
#     x_centroids = centroids[:, 0]
#     y_centroids = centroids[:, 1]
#     x_min = np.min(x_centroids)
#     x_max = np.max(x_centroids)
#     y_min = np.min(y_centroids)
#     y_max = np.max(y_centroids)
#     print(x_min, x_max, y_min, y_max)
#     x_grid = np.arange(x_min, x_max, grid_size)
#     y_grid = np.arange(y_min, y_max, grid_size)
#     print('x grid is: ', x_grid)
#     print('y grid is: ', y_grid)
#     for x in x_grid:
#         for y in y_grid:
#             n = np.where(
#                 (x < centroids[:, 0]) &
#                 (centroids[:, 0] < (x+grid_size)) &
#                 (y < centroids[:, 1]) &
#                 (centroids[:, 1] < (y + grid_size)))
#             if len(n[0]) > min_cluster_size:
#                 super_centroids.append((np.average(centroids[n[0]], axis=0)))
#             print(n[0])
#     n_s_centr = np.array(super_centroids)
#     super_dict = arr_to_dict(super_centroids)
#     x = nx.Graph()
#     x.add_nodes_from(super_dict.keys())
#     print('Hierarchical graph has ', x.number_of_nodes(), 'nodes')
#     for i in range(len(super_dict)):
#         edge = point_dist(i, n_s_centr, th=edge_threshold)  # list of edges
#         x.add_edges_from(edge)  #
#     nx.draw(x, pos=super_dict, ax=ax, width = edge_width, alpha=circle_alpha, node_size=circle_radius)
#     nx.write_gml(x, os.path.join(BASE_DIR, 'test.gml'))
#     plt.savefig(os.path.join(BASE_DIR, 'Hierarchical graph of {} file with {} nodes.svg'.format(centoid_df_file.split('.', 1)[0], x.number_of_nodes())), dpi=1000)


# directory with the relevant files
# BASE_DIR = 'C:/Users/Shushan/Desktop/MSc/Master Thesis/Cell_graph/pres images/patch'
# BASE_DIR = 'M:/Cell Graph/large_patch02'
BASE_DIR = 'C:/Users/Shushan/Desktop/MSc/Master Thesis/Cell_graph/05'

# file with the coordinates of the centroids extracted from QuPath
FILE_NAME = 'polygons_small_patch05.txt'
# IMG_FILE = 'supercells.png'
# image file with the patch to be used for overlaying the graph
IMG_FILE = 'patch_05.png'
# lonely_graph(FILE_NAME, 0.03)
# image as a numpy array
img = plt.imread(os.path.join(BASE_DIR, IMG_FILE))
# dataset of centroids with the cell types
data = pd.read_excel(os.path.join(BASE_DIR, FILE_NAME))

# graph_and_image(FILE_NAME, img, 300)
# hierarchical_graph(FILE_NAME, circle_radius=10, edge_width=0.2, grid_size=0.1, min_cluster_size=100, edge_threshold = 0.1, circle_alpha=0.9)
# hierarchical_graph_and_img(FILE_NAME, img, circle_radius=10, edge_width=0.2, grid_size=100, min_cluster_size=1000, edge_threshold = 0.1, circle_alpha=0.9)
x1, pos1 = graph_and_image(FILE_NAME, img, 80, True, 'Epithelia')
# x2, pos2 = graph_and_image(FILE_NAME, img, 80, 'Other')
fig = plt.figure()
ax = fig.add_subplot(111)

centrality_values = nx.algorithms.centrality.degree_centrality(x1)
values = [centrality_values.get(node, 0.25) for node in x1.nodes()]
# nx.draw(x1, pos=pos1, ax=ax, node_size=7, alpha=0.8, width=0.8, edge_color='lime', cmap=plt.get_cmap('jet'), node_color=centrality_values.values())
nx.draw(x1, pos=pos1, ax=ax, node_size=20, cmap=plt.get_cmap('Purples'), node_color=values)


