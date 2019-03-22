import os
import shutil
import datetime
import json

if __name__ == '__main__':

    # src_dir = r'M:\pT1_selected - exp1\data_for_GED'
    src_dir = 'data_for_GED'
    HIST_DIR = r'M:\ged-shushan\ged-shushan\data\Histology'
    dst_dir = os.path.join(HIST_DIR, 'data_for_GED')
    shutil.copytree(src_dir, dst_dir)

