import pandas as pd
import os
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch


image_file: str = 'fml.png'
img = plt.imread(os.path.join(BASE_DIR, image_file))

fig = plt.figure()  # construct a figure
ax = fig.add_subplot(111)  # get the axis
ax.imshow(img)
edge = ConnectionPatch((0.1, 0.1), (ax.get_xlim()[1], ax.get_ylim()[0]), coordsA='data', color='red')
ax.add_patch(edge)
