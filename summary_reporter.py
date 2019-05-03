import os
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def normalise_with_factor(vector, img_max):
    vec_min = min(vector)
    vec_max = max(vector)
    return (vector - vec_min) / (vec_max - vec_min) * img_max

attr_dict = {'attr_0': "Nucleus: Circularity", 'attr_1':"Nucleus: Hematoxylin OD mean", 'attr_2':"Nucleus: Hematoxylin OD std dev", 'no_attr':"Not Attributed"}

for exp_folder in [r'Z:\Computational_pathology\shushan\80p_7x_spat']:
    prop_n_paths = [os.path.join(exp_folder, folder) for folder in os.listdir(exp_folder) if 'prop_' in folder and '_tt' not in folder and '_test' not in folder]

    result_dict = {'n': [], 'e': [], 'acc': [], 'attr_num': []}
    for prop_path in prop_n_paths:
        print(prop_path)
        prop_file_name = [f for f in os.listdir(prop_path) if f.endswith('.prop')][0]
        knn_file_name = [f for f in os.listdir(prop_path) if f.endswith('knn')][0]
        prop_df = pd.read_csv(os.path.join(prop_path, prop_file_name), header=None)

        with open(os.path.join(prop_path, prop_file_name), 'r') as prop_file:
            prop_content = prop_file.readlines()
        for line in prop_content:
            if '#' not in line and 'node=' in line:
                node = float(line.replace('node=', '').strip('\n'))
            elif '#' not in line and 'edge=' in line:
                edge = float(line.replace('edge=', '').strip('\n'))
            elif '#' not in line and 'nodeAttr1=' in line:
                attr_num = line.replace('nodeAttr1=', '').strip('\n')


        with open(os.path.join(prop_path, knn_file_name), 'r') as prop_file:
            accuracy = prop_file.readline().strip('\n')

        result_dict['n'].append(float(node))
        result_dict['e'].append(float(edge))

        result_dict['attr_num'].append(attr_num)
        result_dict['acc'].append(float(accuracy))
    result_df = pd.DataFrame.from_dict(result_dict)
    result_df.to_excel(os.path.join(exp_folder, 'result_summary.xlsx'), index=None)

    grouped_data = [df for df in result_df.groupby(by=['attr_num'])]
import numpy as np
for attr_num, df in grouped_data:
    plt.scatter(df['n'], df['e'], alpha=0.8,
                s=1000 * df['acc'], c=df['acc'], cmap='Greens')
    plt.title('attr={}'.format(attr_num))
    plt.xlabel('node insertion/deletion cost')
    plt.ylabel('edge insertion/deletion cost')
    plt.xticks(np.arange(min(df['n']), max(df['n']) + 0.4, 0.4))
    plt.yticks(np.arange(min(df['e']), max(df['e'])+0.1, 0.2))
    plt.colorbar()

    for i, txt in enumerate(df['acc']):
        plt.annotate(round(txt*100), (df[['n']].iloc[i,0], df[['e']].iloc[i,0]), rotation=45)

    # plt.savefig(os.path.join(exp_folder, 'attrNum0=attr_1_attrNum1={}_paramVSacc.png'.format(attr_num)))

    plt.show()
#
