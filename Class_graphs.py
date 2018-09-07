import matplotlib.pyplot as plt
import os
from matplotlib.patches import Circle


class Node:
    """Class for building a Node based on the node dictionary extracted from the image
    The first and the second arguments are fro the node coordinates and should be given in normalised image
    units from the QuPath image data. The third argument is a dictionary of further attributes of the node.
    """
    def __init__(self, x_coord, y_coord, feature_dict):

        self.x_coord = x_coord
        self.y_coord = y_coord
        self.features = feature_dict

    def describe(self):
        print('Node is at the point {},{} '
              'with {} features'.format(self.x_coord, self.y_coord, self.features))

class Graph:

    def draw_nodes(self, img):
        print('Initialising node drawing!')
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')
        ax.imshow(img)
        print(max(ax.get_xlim()), max(ax.get_ylim()))
        node_circle = Circle((self.x_coord, self.y_coord), radius = 100, color='red')
        node_circle1 = Circle((self.x_coord+1000, self.y_coord+1000), radius = 100, color='red')
        ax.add_patch(node_circle)
        ax.add_patch(node_circle1)
        # plt.show()
        return (fig, ax)



