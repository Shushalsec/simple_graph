#    Copyright (C) 2004-2019 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
#
# Author: Aric Hagberg (hagberg@lanl.gov)
"""
**********
Matplotlib
**********

Draw networks with matplotlib.

See Also
--------

matplotlib:     http://matplotlib.org/

pygraphviz:     http://pygraphviz.github.io/

"""
from numbers import Number
import networkx as nx
from networkx.utils import is_string_like
from networkx.drawing.layout import shell_layout, \
    circular_layout, kamada_kawai_layout, spectral_layout, \
    spring_layout, random_layout

__all__ = ['draw_networkx',
           'draw_networkx_nodes',
           'draw_networkx_edges']



def draw_networkx(G, pos=None, arrows=True, with_labels=True, **kwds):
    """Draw the graph G using Matplotlib.

    Draw the graph with Matplotlib with options for node positions,
    labeling, titles, and many other drawing features.
    See draw() for simple drawing without labels or axes.

    Parameters
    ----------
    G : graph
       A networkx graph

    pos : dictionary, optional
       A dictionary with nodes as keys and positions as values.
       If not specified a spring layout positioning will be computed.
       See :py:mod:`networkx.drawing.layout` for functions that
       compute node positions.

    arrows : bool, optional (default=True)
       For directed graphs, if True draw arrowheads.
       Note: Arrows will be the same color as edges.

    arrowstyle : str, optional (default='-|>')
        For directed graphs, choose the style of the arrowsheads.
        See :py:class: `matplotlib.patches.ArrowStyle` for more
        options.

    arrowsize : int, optional (default=10)
       For directed graphs, choose the size of the arrow head head's length and
       width. See :py:class: `matplotlib.patches.FancyArrowPatch` for attribute
       `mutation_scale` for more info.

    with_labels :  bool, optional (default=True)
       Set to True to draw labels on the nodes.

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.

    nodelist : list, optional (default G.nodes())
       Draw only specified nodes

    edgelist : list, optional (default=G.edges())
       Draw only specified edges

    node_size : scalar or array, optional (default=300)
       Size of nodes.  If an array is specified it must be the
       same length as nodelist.

    node_color : color string, or array of floats, (default='#1f78b4')
       Node color. Can be a single color format string,
       or a  sequence of colors with the same length as nodelist.
       If numeric values are specified they will be mapped to
       colors using the cmap and vmin,vmax parameters.  See
       matplotlib.scatter for more details.

    node_shape :  string, optional (default='o')
       The shape of the node.  Specification is as matplotlib.scatter
       marker, one of 'so^>v<dph8'.

    alpha : float, optional (default=1.0)
       The node and edge transparency

    cmap : Matplotlib colormap, optional (default=None)
       Colormap for mapping intensities of nodes

    vmin,vmax : float, optional (default=None)
       Minimum and maximum for node colormap scaling

    linewidths : [None | scalar | sequence]
       Line width of symbol border (default =1.0)

    width : float, optional (default=1.0)
       Line width of edges

    edge_color : color string, or array of floats (default='r')
       Edge color. Can be a single color format string,
       or a sequence of colors with the same length as edgelist.
       If numeric values are specified they will be mapped to
       colors using the edge_cmap and edge_vmin,edge_vmax parameters.

    edge_cmap : Matplotlib colormap, optional (default=None)
       Colormap for mapping intensities of edges

    edge_vmin,edge_vmax : floats, optional (default=None)
       Minimum and maximum for edge colormap scaling

    style : string, optional (default='solid')
       Edge line style (solid|dashed|dotted,dashdot)

    labels : dictionary, optional (default=None)
       Node labels in a dictionary keyed by node of text labels

    font_size : int, optional (default=12)
       Font size for text labels

    font_color : string, optional (default='k' black)
       Font color string

    font_weight : string, optional (default='normal')
       Font weight

    font_family : string, optional (default='sans-serif')
       Font family

    label : string, optional
        Label for graph legend

    Notes
    -----
    For directed graphs, arrows  are drawn at the head end.  Arrows can be
    turned off with keyword arrows=False.

    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if pos is None:
        pos = nx.drawing.spring_layout(G)  # default to spring layout

    node_collection = draw_networkx_nodes(G, pos, **kwds)
    edge_collection = draw_networkx_edges(G, pos, arrows=arrows, **kwds)

    plt.draw_if_interactive()

import collections
import numpy as np
import matplotlib.pyplot as plt


def draw_networkx_nodes(graph_object, image_file_path,
                        node_size=30,
                        node_color='#1f78b4',
                        node_shape='o',
                        alpha=1.0,
                        cmap=None,
                        vmin=None,
                        vmax=None,
                        linewidths=None,
                        edgecolors=None,
                        label=None,
                        **kwds):

    def normalise_to_img(vector, img_max):
        vec_min = min(vector)
        vec_max = max(vector)
        return (vector - vec_min) / (vec_max - vec_min) * img_max

    fig = plt.figure(frameon=False)
    ax = fig.add_subplot(111)
    image_np = plt.imread(image_file_path)
    ax.imshow(image_np)


    image_max_x = ax.get_xlim()[1]
    image_max_y = ax.get_ylim()[0]

    xy = np.asarray([[node.x, node.y] for node in graph_object.nodes])

    xy[:, 0] = normalise_to_img(xy[:, 0], image_max_x)
    xy[:, 1] = normalise_to_img(xy[:, 1], image_max_y)


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
    plt.show()
    return ax


from itertools import islice, cycle





def apply_alpha(colors, alpha, elem_list, cmap=None, vmin=None, vmax=None):
    """Apply an alpha (or list of alphas) to the colors provided.

    Parameters
    ----------

    colors : color string, or array of floats
       Color of element. Can be a single color format string (default='r'),
       or a  sequence of colors with the same length as nodelist.
       If numeric values are specified they will be mapped to
       colors using the cmap and vmin,vmax parameters.  See
       matplotlib.scatter for more details.

    alpha : float or array of floats
       Alpha values for elements. This can be a single alpha value, in
       which case it will be applied to all the elements of color. Otherwise,
       if it is an array, the elements of alpha will be applied to the colors
       in order (cycling through alpha multiple times if necessary).

    elem_list : array of networkx objects
       The list of elements which are being colored. These could be nodes,
       edges or labels.

    cmap : matplotlib colormap
       Color map for use if colors is a list of floats corresponding to points
       on a color mapping.

    vmin, vmax : float
       Minimum and maximum values for normalizing colors if a color mapping is
       used.

    Returns
    -------

    rgba_colors : numpy ndarray
        Array containing RGBA format values for each of the node colours.

    """
    from itertools import islice, cycle

    try:
        import numpy as np
        from matplotlib.colors import colorConverter
        import matplotlib.cm as cm
    except ImportError:
        raise ImportError("Matplotlib required for draw()")

    # If we have been provided with a list of numbers as long as elem_list,
    # apply the color mapping.
    # assert len(colors) == len(elem_list) and isinstance(colors[0], Number)
    mapper = cm.ScalarMappable(cmap=cmap)
    mapper.set_clim(vmin, vmax)
    rgba_colors = mapper.to_rgba(colors)

    # Set the final column of the rgba_colors to have the relevant alpha values
    try:
        # If alpha is longer than the number of colors, resize to the number of
        # elements.  Also, if rgba_colors.size (the number of elements of
        # rgba_colors) is the same as the number of elements, resize the array,
        # to avoid it being interpreted as a colormap by scatter()
        if len(alpha) > len(rgba_colors) or rgba_colors.size == len(elem_list):
            rgba_colors = np.resize(rgba_colors, (len(elem_list), 4))
            rgba_colors[1:, 0] = rgba_colors[0, 0]
            rgba_colors[1:, 1] = rgba_colors[0, 1]
            rgba_colors[1:, 2] = rgba_colors[0, 2]
        rgba_colors[:, 3] = list(islice(cycle(alpha), len(rgba_colors)))
    except TypeError:
        rgba_colors[:, -1] = alpha
    return rgba_colors


import matplotlib.cm as cm
mapper = cm.ScalarMappable('r')
mapper.set_clim(None, None)
rgba_colors = mapper.to_rgba('#1f78b4')





def draw_networkx_edges(edge_pos, ax,
                        edgelist=None,
                        width=1.0,
                        edge_color='k',
                        style='solid',
                        alpha=1.0,
                        arrowstyle='-|>',
                        arrowsize=10,
                        edge_cmap=None,
                        edge_vmin=None,
                        edge_vmax=None,

                        arrows=True,
                        label=None,
                        node_size=300,
                        nodelist=None,
                        node_shape="o",
                        connectionstyle=None,
                        **kwds):

    try:
        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.cbook as cb
        from matplotlib.colors import colorConverter, Colormap, Normalize
        from matplotlib.collections import LineCollection
        from matplotlib.patches import FancyArrowPatch
        import numpy as np
    except ImportError:
        raise ImportError("Matplotlib required for draw()")
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise





    edge_collection = LineCollection(edge_pos,
                                     colors='r',
                                     linewidth = width,
                                     antialiaseds=(1,),
                                     linestyle=style,
                                     transOffset=ax.transData,
                                     )
    edge_collection.set_array(edge_positions)
    edge_collection.set_zorder(1)  # edges go behind nodes
    # edge_collection.set_label(label)
    ax.add_collection(edge_collection)

    # Note: there was a bug in mpl regarding the handling of alpha values
    # for each line in a LineCollection. It was fixed in matplotlib by
    # r7184 and r7189 (June 6 2009). We should then not set the alpha
    # value globally, since the user can instead provide per-edge alphas
    # now.  Only set it globally if provided as a scalar.
    plt.show()

    return ax, edge_collection

import GraphBuilder
import numpy as np
image = r'M:\pT1_selected - complete_annotation - organised\B08.8643_IVE_HE_pT1_selected - complete_annotation\masks\B08.8643_IVE_HE_0_abnormal\B08.8643_IVE_HE_0_abnormal-cropped.jpg'

ax = draw_networkx_nodes(GraphBuilder.g, image, alpha=0.5)


edge_positions = [np.asarray([[GraphBuilder.g.nodes[e._from].x, GraphBuilder.g.nodes[e._from].y], [GraphBuilder.g.nodes[e._to].x, GraphBuilder.g.nodes[e._to].y]]) for e in GraphBuilder.g.edges]

edge_positions

new_ax, edges = draw_networkx_edges(edge_positions, ax)
plt.show()
from matplotlib import colors as mcolors
colors = [mcolors.to_rgba(c) for c in plt.rcParams['axes.prop_cycle'].by_key()['color']]


import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

segments = [ [(1,2),(3,4)],
                                [(5,6),(7,8)] ]
lc = mc.LineCollection(segments, linestyles='solid', pickradius=5, zorder=2)
fig, ax = pl.subplots()

ax.add_collection(lc)
ax.autoscale()