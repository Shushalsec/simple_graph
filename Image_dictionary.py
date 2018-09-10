import matplotlib.pyplot as plt
import os
import pandas as pd
from matplotlib.patches import Circle
import numpy as np
import scipy.spatial.distance
from matplotlib.patches import ConnectionPatch

def zeros(df):
    '''
    :param df: all the initial data as a pandas dataframe
    :return: upper left and botom right point coordinates
    '''
    #get the column names for coordinates
    x_coords = df.columns.values[3]
    y_coords = df.columns.values[4]
    #extract the row with vertex point data
    zeros_df = df.loc[df['ROI'] == 'Points']
    zeros_df.sort_values(by=[x_coords], inplace=True)
    #extract x and y coordinate values
    x0 = zeros_df[x_coords]
    y0 = zeros_df[y_coords]
    x_min = x0.iloc[0]
    x_max = x0.iloc[1]
    y_min = y0.iloc[0]
    y_max = y0.iloc[1]
    return x_min, y_min, x_max, y_max

def extract_list(df):
    data_list = []
    x_coords = df.columns.values[3]
    y_coords = df.columns.values[4]
    area = df.columns.values[5]
    perimeter = df.columns.values[6]
    polygon_data = df.loc[df['ROI'] == 'Polygon']
    x_min, y_min, x_max, y_max = zeros(df)
    x_range = x_max - x_min
    y_range = y_max - y_min
    for i, row in polygon_data.iterrows():
        polygon_x = (row.loc[x_coords] - x_min)/(x_range)
        polygon_y = (row.loc[y_coords] - y_min)/(y_range)
        data_list.append([polygon_x, polygon_y, row.loc[area], row.loc[perimeter]])
    return data_list

data_file = 'd.xlsx'
data_dir = 'C:/Users/Shushan/Desktop'
data = pd.read_excel(os.path.join(data_dir, data_file))
#import the image
img_file = 'B14.22816PCK.png'
img = plt.imread(os.path.join(data_dir, img_file))

node_list = extract_list(data)
node_array = np.array(node_list)
node_coordinates = node_array[:,:2]
distances = scipy.spatial.distance.pdist(node_coordinates)
from matplotlib.patches import ConnectionPatch

d = scipy.spatial.distance.squareform(distances)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal')
ax.imshow(img)
x_max = max(ax.get_xlim())
y_max = max(ax.get_ylim())
for row, node in enumerate(node_list):
    node_circle = Circle((node[0]*x_max, node[1]*y_max), radius=80, color='red')
    ax.add_patch(node_circle)
    pair = np.nanargmin(d[row])
    edge = ConnectionPatch((node[0]*x_max, node[1]*y_max), (node_list[pair][0]*x_max, node_list[pair][1]*y_max), coordsA='data')
    ax.add_patch(edge)

















































