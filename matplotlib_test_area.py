import numpy as np
points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]])
from scipy.spatial import Voronoi, voronoi_plot_2d
vor = Voronoi(points)
import matplotlib.pyplot as plt
voronoi_plot_2d(vor)
plt.show()

import pandas as pd
data_file = 'd.xlsx'
data_dir = 'C:/Users/Shushan/Desktop'
data = pd.read_excel(os.path.join(data_dir, data_file))


#import the image
import os
img_file = 'B14.22816PCK.png'
img = plt.imread(os.path.join(data_dir, img_file))
