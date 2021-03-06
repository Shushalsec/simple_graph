import matplotlib.pyplot as plt
import pylab as plt
from matplotlib import collections  as mc
import numpy as np
# import GraphBuilder
import matplotlib.colors as clrs
import os
import re
import sys

def normalise_with_factor(vector, img_max):
    vec_min = min(vector)
    vec_max = max(vector)
    return (vector - vec_min) / (vec_max - vec_min) * img_max


def draw_graph(graph_object, image_file_path, image_save_path, ax=None,
               width=2, background = True,
               node_size=30,
               graph_color='lime',
               node_shape='o',
               style='solid'):
    if not ax:
        fig = plt.figure(frameon=False)
        ax = fig.add_subplot(111)

    image_np = plt.imread(image_file_path)

    if background:
        ax.imshow(image_np)
        image_max_x = np.abs(ax.get_xlim()[0]) + np.abs(ax.get_xlim()[1])
        image_max_y = np.abs(ax.get_ylim()[0]) + np.abs(ax.get_ylim()[1])
    else:
        image_max_x = image_np.shape[0]
        image_max_y = image_np.shape[1]

    xy = np.asarray([[node.x, node.y] for node in graph_object.nodes])

    xy[:, 0] = normalise_with_factor(xy[:, 0], image_max_x)
    xy[:, 1] = normalise_with_factor(xy[:, 1], image_max_y)


    node_collection = ax.scatter(xy[:, 0], xy[:, 1],
                                 s=node_size,
                                 c=graph_color,
                                 marker=node_shape)
    ax.set_zorder(2)

    edge_positions = [ [[ xy[e._from,0], xy[e._from,1] ],
                              [ xy[e._to,0], xy[e._to,1] ]] for e in
                  graph_object.edges]



    edge_collection = mc.LineCollection(edge_positions,
                                        colors=graph_color,
                                        linewidths=width,
                                        linestyles=style)
    ax.add_collection(edge_collection)
    ax.autoscale()
    # ax.margins(0.1)
    ax.set_zorder(1)
    plt.axis('off')
    plt.savefig(image_save_path, bbox_inches='tight')
    plt.show()
    return ax, edge_positions



def apply_alpha(color, graph_object, attribute_name):
    print('Graph node alphas based on {} values'.format(attribute_name))
    alphas = normalise_with_factor(np.asarray([node.attr_dict[attribute_name] for node in graph_object.nodes]), 1)
    all_colors = [list(clrs.to_rgba(color, a)) for a in alphas]
    return all_colors

#
# def draw_fancy_graph(graph_object, image_path=None, graph_color='lime', alpha = None, attribute_to_highlight=None):
#     assert len(graph_object.nodes)>0
#
#     IMAGE_DB_PATH = r'M:\pT1_selected - complete_annotation - not_organised\not_organised_folders'
#
#     if not image_path:
#         try:
#
#             graph_folder = os.path.basename(graph_object.graph_dir)
#             pattern = '(.+)_[0-9]+_[normal|abnormal]'
#             wsi_name = re.search(pattern, os.path.basename(GraphBuilder.g.graph_dir)).group(1)
#
#             image_path = os.path.join(IMAGE_DB_PATH, wsi_name, 'masks', graph_folder+'-cropped.jpg')
#         except:
#             print('Image dataset not found. Please specify the image path manually')
#     if attribute_to_highlight:
#         colors = apply_alpha(graph_color, graph_object, attribute_to_highlight)
#     else:
#         colors = clrs.to_rgba(graph_color, alpha)
#     draw_graph(graph_object, image_path, graph_color=colors)
#


def draw_while_building(graph_object, exp_folder, c=None, ax=None, background=True, alpha = None, attribute_to_highlight=None):

    assert len(graph_object.nodes) > 0

    wsi_n_class = graph_object.graph_dir.rsplit('\\')[-1]

    pattern = '(.+)_[0-9]+_[normal|abnormal]'
    wsi_name = re.search(pattern, wsi_n_class).group(1)
    img_path = os.path.join('organised_folders', wsi_name, 'masks', wsi_n_class, wsi_n_class+'-cropped.jpg')
    if not os.path.isdir(os.path.join(exp_folder, 'graphviz')):
        os.mkdir(os.path.join(exp_folder, 'graphviz'))
    img_save_path = os.path.join(exp_folder, 'graphviz', wsi_n_class+'.jpg')
    graph_save_path = os.path.join(exp_folder, 'graphviz', 'graph_'+wsi_n_class+'.jpg')
    print(wsi_n_class)
    if not c:
        if 'abnormal' in wsi_n_class:
            c = 'r'
        else:
            c = 'lime'

    if attribute_to_highlight:
        colors = apply_alpha(c, graph_object, attribute_to_highlight)
    else:
        colors = clrs.to_rgba(c, alpha)
    if background:
        draw_graph(graph_object, image_file_path=img_path, image_save_path=img_save_path, background=True, graph_color=colors, ax=ax)
    else:
        draw_graph(graph_object, image_file_path=img_path, image_save_path=graph_save_path, background=False, graph_color=colors, ax=ax)


#
# os.chdir(r'M:\pT1_cell_1')
# draw_while_building(g_23, r'M:\pT1_cell_1\80p_4x_spat')
#
# draw_while_building(g_31, r'M:\pT1_cell_1\80p_4x_spat', c='r')
