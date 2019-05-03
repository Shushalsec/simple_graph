import os
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.manifold import MDS
import numpy as np


result_path = r'Z:\Computational_pathology\shushan\80p_7x_spat\1_attr_stage'
tt_folders = [folder for folder in os.listdir(result_path) if '_tt' in folder and '04_04' in folder]

for one_tt in tt_folders:
    example_tt = os.path.join(result_path, one_tt)

    prop_file = [f for f in os.listdir(example_tt) if f.endswith('.prop')][0]
    file_prefix = prop_file.split('.')[0]

    raw_file = os.path.join(example_tt, file_prefix+'.raw')
    raw_df = pd.read_csv(raw_file, sep=' ', header=None, dtype=float)

    # raw_79=pd.read_csv(r'Z:\Computational_pathology\shushan\80p_4x_spat\prop_79\prop_79.raw', sep=' ', header=None, dtype=float)
    # raw_79.drop(columns=[raw_79.shape[1]-1], inplace=True)
    # a=np.asarray(raw_79)
    # ind = np.unravel_index(np.argmin(a, axis=None), a.shape)
    # a[44,51]

    raw_df.drop(columns=[raw_df.shape[1]-1], inplace=True)
    raw_np = np.asarray(raw_df)

    ged_file = os.path.join(example_tt, file_prefix+'.ged')
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



    plt.imshow(raw_df, zorder=2, cmap='Blues', interpolation='nearest')
    plt.show()



    model = MDS(n_components=2, dissimilarity='precomputed', random_state=1, metric=False)
    out = model.fit_transform(raw_df)

    fig, ax = plt.subplots()
    ax.scatter(out[:, 0], out[:, 1], color = typemap)

    # for i, txt in enumerate(point_names_list):
    #     ax.annotate(txt, (out[:, 0], out[:, 1]))
    plt.axis('tight')
    plt.savefig(os.path.join(example_tt, 'mds.png'))
    plt.show()
    from matplotlib.ticker import NullFormatter

    from sklearn import manifold, datasets

    tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
    Y = tsne.fit_transform(raw_df)

    ax = fig.add_subplot(2, 5, 10)
    plt.scatter(Y[:, 0], Y[:, 1], c=typemap, cmap=plt.cm.Spectral)

    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')
    plt.savefig(os.path.join(example_tt, 'tsne.png'))
    plt.show()
