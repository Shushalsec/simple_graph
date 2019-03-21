import os
import shutil

if __name__ == '__main__':
    # source_dir = r'M:\pT1_selected - exp1\data_for_GED'
    source_dir = './data_for_GED'
    hist_dir = r'M:\ged-shushan\ged-shushan\data\Histology'
    current_experiment = os.path.basename(os.path.normpath(source_dir))
    destination_dir = os.path.join(hist_dir, current_experiment)

    shutil.copytree(source_dir, destination_dir)




