import os
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.manifold import MDS
import numpy as np


result_path = r'Z:\Computational_pathology\shushan\80p_4x_spat\prop_97'

prop_file = [f for f in os.listdir(result_path) if f.endswith('.prop')][0]
file_prefix = prop_file.split('.')[0]


raw_file = os.path.join(result_path, file_prefix+'.raw')
raw_df = pd.read_csv(raw_file, sep=' ', header=None, dtype=float)

raw_df.drop(columns=[raw_df.shape[1]-1], inplace=True)
raw_np = np.asarray(raw_df)
k=3
nearest_indeces = np.argpartition(raw_np, k, axis=1)[:,:k]

ged_file = os.path.join(result_path, file_prefix+'.ged')
ged_df = pd.read_csv(ged_file, sep=' ', header=None)
ged_df.drop(columns=[ged_df.shape[1]-1], inplace=True)
typemap = []
point_names_list = []
val_classes = []
with open(ged_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        data_point_class = line.split('|')[0]
        data_point_name = line.split('|')[2].split('.gxl')[0]
        point_names_list.append(data_point_name)
        if data_point_class == 'abnormal':
            typemap.append('red')
            val_classes.append(1)
        else:
            typemap.append('green')
            val_classes.append(0)
val_classes = np.asarray(val_classes)

train_labels = [0 if 'abnormal' in cell else 1 for cell in ged_df.iloc[0,1:]]

from scipy import stats
nearest_point_classes = np.asarray(train_labels)[nearest_indeces]

pred_classes = stats.mode(nearest_point_classes, axis=1)[0]
pred_classes.shape
val_classes.shape
correct_preds = sum(pred_classes.flatten()==val_classes)
total_preds = len(pred_classes)
accuracy = correct_preds/total_preds


