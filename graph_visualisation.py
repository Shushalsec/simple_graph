import pandas as pd
import os
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch
import networkx as nx
from scipy import spatial


def draw_networkx_nodes(G, pos,
                        nodelist=None,
                        node_size=300,
                        node_color='#1f78b4',
                        node_shape='o',
                        alpha=1.0,
                        cmap=None,
                        vmin=None,
                        vmax=None,
                        ax=None,
                        linewidths=None,
                        edgecolors=None,
                        label=None,
                        **kwds):
    """Draw the nodes of the graph G.

    This draws only the nodes of the graph G.

    Parameters
    ----------
    G : graph
       A networkx graph

    pos : dictionary
       A dictionary with nodes as keys and positions as values.
       Positions should be sequences of length 2.

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.

    nodelist : list, optional
       Draw only specified nodes (default G.nodes())

    node_size : scalar or array
       Size of nodes (default=300).  If an array is specified it must be the
       same length as nodelist.

    node_color : color string, or array of floats
       Node color. Can be a single color format string (default='#1f78b4'),
       or a  sequence of colors with the same length as nodelist.
       If numeric values are specified they will be mapped to
       colors using the cmap and vmin,vmax parameters.  See
       matplotlib.scatter for more details.

    node_shape :  string
       The shape of the node.  Specification is as matplotlib.scatter
       marker, one of 'so^>v<dph8' (default='o').

    alpha : float or array of floats
       The node transparency.  This can be a single alpha value (default=1.0),
       in which case it will be applied to all the nodes of color. Otherwise,
       if it is an array, the elements of alpha will be applied to the colors
       in order (cycling through alpha multiple times if necessary).

    cmap : Matplotlib colormap
       Colormap for mapping intensities of nodes (default=None)

    vmin,vmax : floats
       Minimum and maximum for node colormap scaling (default=None)

    linewidths : [None | scalar | sequence]
       Line width of symbol border (default =1.0)

    edgecolors : [None | scalar | sequence]
       Colors of node borders (default = node_color)

    label : [None| string]
       Label for legend

    Returns
    -------
    matplotlib.collections.PathCollection
        `PathCollection` of the nodes.

    Examples
    --------
    G = nx.dodecahedral_graph()
    nodes = nx.draw_networkx_nodes(G, pos=nx.spring_layout(G))

    Also see the NetworkX drawing examples at
    https://networkx.github.io/documentation/latest/auto_examples/index.html

    See Also
    --------
    draw()
    draw_networkx()
    draw_networkx_edges()
    draw_networkx_labels()
    draw_networkx_edge_labels()
    """
    import collections
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if ax is None:
        ax = plt.gca()

    if nodelist is None:
        nodelist = list(G)

    if not nodelist or len(nodelist) == 0:  # empty nodelist, no drawing
        return None

    try:
        xy = np.asarray([pos[v] for v in nodelist])
    except KeyError as e:
        raise nx.NetworkXError('Node %s has no position.' % e)
    except ValueError:
        raise nx.NetworkXError('Bad value in node positions.')

    if isinstance(alpha, collections.Iterable):
        node_color = apply_alpha(node_color, alpha, nodelist, cmap, vmin, vmax)
        alpha = None

    node_collection = ax.scatter(xy[:, 0], xy[:, 1],
                                 s=node_size,
                                 c=node_color,
                                 marker=node_shape,
                                 cmap=cmap,
                                 vmin=vmin,
                                 vmax=vmax,
                                 alpha=alpha,
                                 linewidths=linewidths,
                                 edgecolors=edgecolors,
                                 label=label)
    plt.tick_params(
        axis='both',
        which='both',
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False)

    node_collection.set_zorder(2)
    return node_collection





# def visualise_graph(graph_object):
#     one_graphml = XML(graph_object, graphml_folder, graph_id=1, root_tag='graphml')
#     one_graphml.XML_writer('graphml')
#     data = pd.read_excel(os.path.join(graph_object.graph_dir, subdirectory+'-detections.xlsx'))
#     x = data.iloc[:, 3]
#     y = data.iloc[:, 4]
#     g = nx.read_graphml(os.path.join(graphml_folder, os.listdir(graphml_folder)[0]))
#     pos = {n_id: (x[i], y[i]) for i, n_id in enumerate(nx.nodes(g))}
#     nx.draw_networkx(g, pos, node_color = 'lime' , alpha = 1, node_size = 50, with_labels=False, width = 0.1, edge_color = 'lime')
#     plt.show()

#
#
# G = nx.Graph()
# nodes = nx.nodes(G)
#
# data = pd.read_excel(r'C:\Users\st18l084\Desktop\2.xlsx')
#
# G.add_nodes_from([i for i in range(data.shape[0])])
#
# max_x = 18504.1   # maximum x coordinate value
# max_y = 22867   # maximum y coordinate value
# min_x = 17511.2   # minimum x coordinate
# min_y = 22456.2   # minimum y coordinate
# range_x = max_x - min_x  # range of x
# range_y = max_y - min_y  # range of y
# # fig = plt.figure()
# fig = plt.figure(frameon=False)
# ax = fig.add_subplot(111)
# image_file = r'C:\Users\st18l084\Desktop\2.png'
# image = plt.imread(image_file)
# ax.imshow(image)
# ax.axis('equal')
# image_max_x = ax.get_xlim()[1]
# image_max_y = ax.get_ylim()[0]
#
# # image_max_x = (18504.1 - 17511.2)
# # image_max_y = (22867 - 22456.2)
#
#
#
# x = np.asarray(data.iloc[:,3])
# y = np.asarray(data.iloc[:,4])
# x = (x - np.min(x)) / (np.max(x) - np.min(x))*image_max_x
# y = (y - np.min(y)) / (np.max(y) - np.min(y)) * image_max_y
# d = {i:(x,y) for i, (x, y) in enumerate(zip(x, y))}
#
#
# tree = spatial.KDTree(list(zip(x, y)))
# k_nearest = 4
# dist, nn = tree.query(tree.data, k=k_nearest)  # array of distances and k nearest neighbors for each node
# # iterate over the columns of the numpy array with nearest neighbor indices
# for column in range(1, nn.shape[1]):  # omit the first column as this is the node index itself or 0 distance
#     for j in range(nn.shape[0]):
#         G.add_edge(j, nn[j, column])
#
# # G = nx.Graph()
# # G.add_node(1)
# # nx.draw_networkx(G, pos={1:(3,3)})
#
#
# fig = plt.figure(frameon=False)
# ax = fig.add_subplot(111)
# ax.imshow(image)
# ax.axis('off')
# nx.draw_networkx(G, ax = ax, pos=d, node_color = 'lime' , alpha = 1, node_size = 50, with_labels=False, width = 3, edge_color = 'lime')
# plt.savefig(r'C:\Users\st18l084\Desktop\lime', dpi=1000)
#
#
# ##############################################################################################################3
#
#
# G = nx.read_graphml(r'M:\pT1_selected - complete_annotation\experiment_f9\graphml\B08.8643_IVE_HE_0_abnormal.graphml')
# nx.nodes(G)
# nx.edges(G)
#
# nx.draw_networkx(G)
# plt.show()
# # G = nx.Graph()
# # G.add_node(1)
# # nx.draw_networkx(G, pos={1:(3,3)})
# image_file = r'C:\Users\st18l084\Desktop\1.jpg'
# image = plt.imread(image_file)
#
# fig = plt.figure(frameon=False)
# ax = fig.add_subplot(111)
# ax.imshow(image)
# ax.axis('equal')
#
# image_max_x = ax.get_xlim()[1]
# image_max_y = ax.get_ylim()[0]
#
# def normalise_x(cell, min, max):
#     return (cell - min)/(max - min) *image_max_x
#
# def normalise_y(cell, min, max):
#     return (cell - min)/(max - min) * image_max_y
#
#
# data = pd.read_excel(r'C:\Users\st18l084\Desktop\1.xlsx')
# x_min = data.iloc[:,3].min()
# x_max = data.iloc[:,3].max()
# y_min = data.iloc[:,4].min()
# y_max = data.iloc[:,4].max()
#
#
# x_normalised = np.vectorize(normalise_x)(data.iloc[:,3], x_min,x_max)
# y_normalised = np.vectorize(normalise_y)(data.iloc[:,4], y_min, y_max)
#
# d = {'_{}'.format(i+1):(x,y) for i, (x, y) in enumerate(zip(x_normalised, y_normalised))}
#
# nx.draw_networkx(G, ax = ax, pos=d, node_color = 'green' , alpha = 0.5, node_size = 10, font_size = 1, edge_color = 'lime')
# plt.show()
#
# def normalise_to_img(df, img_patch):
#     """
#     normalise the dataset ready for extracting a graph to be pasted on an image
#     :param df: dataset ex
#     :param img_patch:
#     :return:
#     """
#     epi_norm = []  # empty list for the cell centroids that are from epithelium
#     other_norm = []  # empty list to add the other type of centroids
#     max_x = 17511.2018/0.2428  # maximum x coordinate value
#     max_y = 22456.2181/0.2428  # maximum y coordinate value
#     min_x = 18504/0.2428  # minimum x coordinate
#     min_y = 22866/0.2428  # minimum y coordinate
#     range_x = max_x - min_x  # range of x
#     range_y = max_y - min_y  # range of y
#     # fig = plt.figure()
#     fig = plt.figure(frameon=False)
#     ax = fig.add_subplot(111)
#     ax.imshow(img_patch)
#     ax.axis('equal')
#     img_x = ax.get_xlim()[1]
#     img_y = ax.get_ylim()[0]
#     print(img_x, img_y)
#     for i, row in df.iterrows():
#         x = (row[1] - min_x) / range_x * img_x  # normalise
#         y = (row[2] - min_y) / range_y * img_y  # normalise
#         if 'normal' in row[0]:
#             epi_norm.append([x, y])  # add to epithelia if epithelial
#         else:
#             other_norm.append([x, y])  # add to other otherwise
#     # save as a dictionary with 2 elements
#     output_dict = {'normal': np.array(epi_norm), 'Other': np.array(other_norm)}
#     return output_dict, ax
#
# normalise_to_img()
#
# def point_dist(row_number, type_coords, th=0.05):
#     """
#     for 1 line of the xy coordinate matrix identify other coordinates within threshold Manhattan distance from the
#     given point
#     :param row_number: index of one row of the coordinate list
#     :param type_coords: coordinate array for one type of tisue that is of interest
#     :param th: threshold withing which the search for points is done
#     :return: coordinates of points close enough to the given row point
#     """
#     d1 = type_coords[row_number][0]  # separate the x
#     d2 = type_coords[row_number][1]  # the y
#     # make a mask for filtering the points which are
#     # within the threshold (in either direction) for both x and y coordinates
#     all_x = type_coords[:, 0]
#     all_y = type_coords[:, 1]
#     mask = np.argwhere((np.abs(d1 - all_x) < th) & (np.abs(d2 - all_y) < th))
#     node_pair = [i[0] for i in mask]
#     current_node = [row_number] * len(node_pair)
#     result = list(zip(node_pair, current_node))
#     return result  # output the actual values of the coordiantes from the original array
#
#
# def arr_to_dict(arr):
#     # write node coordinates to a dictionary
#     pos = {k: v for k, v in enumerate(arr)}
#     return pos
#
#     # per node compute neighbors
#     # per node write neighbors to file
#
# def gi(df, image, threshold):
#     """
#     Overlay the graph on top of a patch
#     :param centroids_file: .txt with centroids and tissue type from QuPath
#     :param image: image in numpy array
#     :param threshold: limit for connection edges, has to be around 300 to make connections
#     :return:
#     """
#     tissue = 'Other'
#     print('***\nInitializing graph from the dataset')
#     # dictionary of coordinates by tissue type
#     data_dict, ax = normalise_to_img(df, image)
#     print('Coordinates imported and normalised')
#     # create a dictionary with unique node label and its coordinates as keys and values
#     pos = arr_to_dict(data_dict[tissue])
#     x = nx.Graph()  # generate an empty graph
#     x.add_nodes_from(pos.keys())  # add the nodes from the node dictionary
#     print('Nodes added')
#     # compute the nodes which are within threshold given the Manhattan distance
#     for i in range(len(pos)):
#         print('Starting edge calculations...')
#         edge = point_dist(i, data_dict[tissue], th=threshold)  # list of edges
#         print('**************\n', edge)
#         x.add_edges_from(edge)
#     nx.draw(x, pos=pos, ax=ax, node_size=7, node_color='#7fbf7b', alpha=0.8, width=1.2, edge_color='lime')
#     # plt.savefig(os.path.join(BASE_DIR, 'Graph and image {}'.format(centroids_file.split('.', 1)[0])), dpi=1000)
#
# BASE_DIR = r'M:\EXPERIMENT_ARCHIVE\pT1_selected -porcadasht'
#
# # file with the coordinates of the centroids extracted from QuPath
# FILE_NAME = 'f.xlsx'
# IMG_FILE = 'daone.png'
# # image file with the patch to be used for overlaying the graph
# # IMG_FILE = '06_1.png'
# # lonely_graph(FILE_NAME, 0.03)
# # image as a numpy array
# img = plt.imread(os.path.join(BASE_DIR, IMG_FILE))
# # dataset of centroids with the cell types
# data = pd.read_excel(os.path.join(BASE_DIR, FILE_NAME))
#
#
# gi(data, img, 500)