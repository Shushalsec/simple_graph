import pandas as pd
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from numpy import unravel_index
import shutil


DIR = 'C:/Users/st18l084/Dropbox/Ki67 Project/Results'
data_file = [file for file in os.listdir(DIR) if 'Detections' in file][0]
bb_file = [file for file in os.listdir(DIR) if 'bounding' in file][0]

if len(data_file)>1 or len(bb_file)>1:
    print('There are more than one text files to analyse!')
else:
    print('Text files found!')

bb_data  = pd.read_csv(os.path.join(DIR, bb_file), encoding='latin1', sep='\t')
core_name = data_file.split(' Detectionstxt')[0]
new_folder = '{}'.format(core_name)
os.mkdir(os.path.join(DIR, new_folder))
data = pd.read_csv(os.path.join(DIR, data_file), encoding='latin1', sep='\t')

col = data.columns.values
name, x, y = col[0], col[3], col[4]

subdata = data[[name, x, y]].copy()

subdata.dropna(inplace=True)
grouped = subdata.groupby(col[0])
neg, pos = [ x for _, x in grouped]
range_x = max(subdata[x]) - min(subdata[x])
range_y = max(subdata[y]) - min(subdata[y])




# histogram for all the cells
bin_factor = 200  # the larger this number the smaller the number of bins (and smaller the resolution)
bins = [round(range_x/bin_factor), round(range_y/bin_factor)]
print('x bins = ', bins[0], '\n', 'y_bins = ', bins[1])
H_all, xedges, yedges = np.histogram2d(subdata[x], subdata[y], bins)  # all cell detections
H_all = H_all.T
plt.imshow(H_all, cmap = 'Purples')
plt.colorbar()
plt.title('Number of Cells per Tile')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig(os.path.join(DIR, new_folder, '{}_H_all.jpg'.format(core_name)))
plt.close()

# histogram for positive cells
H_pos, height, width = np.histogram2d(pos[x], pos[y], bins)  # positive cells
H_pos = H_pos.T
fig = plt.figure()
plt.imshow(H_pos, cmap='Reds')
plt.colorbar()
plt.title('Number of Positive Cells per Tile')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig(os.path.join(DIR, new_folder, '{}_H_pos.jpg'.format(core_name)))
plt.close()

# histogram for Ki67 scores across the image
thr_H_pos =  H_pos[H_all>20]  # threshold to get at least 2000 as the overall number of cells
result = np.nan_to_num(H_pos/H_all*100)  # get percentage of Ki67 positive cells
below_100_indeces = H_pos/H_all*100<100  # mask array with only scores
ki67_scores = H_pos/H_all*100
zeros = np.zeros_like(ki67_scores)
filtered_ki67 = np.where(below_100_indeces, ki67_scores, zeros)
plt.imshow(filtered_ki67, cmap='RdPu')
plt.colorbar()
plt.title('Ki67%')
plt.xlabel('X')
plt.ylabel('Y')

plt.savefig(os.path.join(DIR, new_folder, '{}_res.jpg'.format(core_name)))
plt.close()

res_bins = range(5, 100, 5)
result = result[result<100]

plt.hist(result, rwidth = 0.95, bins = res_bins)
plt.savefig(os.path.join(DIR, new_folder, '{}_hist.jpg'.format(core_name)))
plt.close()


# coordinates of the top hot spots
bb_x = bb_data['x'][0]
bb_y = bb_data['y'][0]
bb_width = bb_data['Width'][0]
bb_height = bb_data['Height'][0]
w = bb_width / bins[0]  # width of one grid cell
h = bb_height / bins[1]  # height of one grid cell
with open(os.path.join(DIR, 'spot_size.txt'), 'w') as f:
    f.write('{}\n{}'.format(w,h))

top_n = 10
indices =  np.argpartition(H_pos.flatten(), -2)[-top_n:]
hot_spot_coords = np.vstack(np.unravel_index(indices, H_pos.shape)).T
hot_xes = []
hot_ys = []
for hot_spot in hot_spot_coords:

    x_coord = bb_x + (hot_spot[1]) * w  # from upper left shift 10 grid cells
    y_coord = bb_y + (hot_spot[0]) * h  # from upper left go down 4 grid cells

    hot_xes.append(float(x_coord))
    hot_ys.append(float(y_coord))

with open(os.path.join(DIR, 'x.txt'), 'w') as f:
    for item in hot_xes:
        print(item)
        f.write("{}\n".format(item))

with open(os.path.join(DIR, 'y.txt'), 'w') as f:
    for item in hot_ys:
        print(item)
        f.write("{}\n".format(item))


# dest = os.path.join(DIR, core_name)
#
#
# files = os.listdir(DIR)
#
# for f in files:
#     if os.path.isfile(os.path.join(DIR, f)):
#         shutil.move(DIR+'/'+f, dest)

# import os
# os.chdir('Z:/04_DIA/10_Ki67/Ki67 Visiopharm/thumbnails')
#
# file_names_th = [[file.split('.jpg')[0]] for file in os.listdir()]
#
#
# df = pd.DataFrame.from_records(file_names_th)
# pd.DataFrame.to_excel(df, 'T:/res/Ki67_Scores_new.xlsx', index=False, header=['Slide'])
#
os.listdir('C:/Users/st18l084/Desktop/Ki67 presentation')