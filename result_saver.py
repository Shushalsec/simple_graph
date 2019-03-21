import os
import shutil
import datetime
import json

# if __name__ == '__main__':

SOURCE_DIR = r'M:\pT1_selected - exp1'
# SOURCE_DIR = os.getcwd()
HIST_DIR = r'M:\ged-shushan\ged-shushan\data\Histology'
current_experiment = os.path.basename(os.path.normpath(SOURCE_DIR))
dst_dir = os.path.join(HIST_DIR, current_experiment)


currentDT = datetime.datetime.now()
# to save the version information create a folder with the image folder name + datetime stamp
os.mkdir(os.path.join(HIST_DIR, 'EXPERIMENT_'+str(currentDT)))

#copy the data folders from each project result folder in pT1_DIR to HIST_DIR

#copy annotations and detections files to HIST_DIR
shutil.copy(os.path.join(source_dir, 'detections.txt'), os.path.join(destination_dir))

# copy the script to save the parameters of the detection

#copy the