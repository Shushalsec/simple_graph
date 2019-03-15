import os
import shutil
import datetime
import json

with open('parameters.txt') as parameter_file:
    parameters = json.load(parameter_file)
SOURCE_DIR = os.path.join(parameters['main_dir'], parameters['experiment'])

# if __name__ == '__main__':
HIST_DIR = r'M:\ged-shushan\ged-shushan\data\Histology'
SINK_DIR =

currentDT = datetime.datetime.now()
# to save the version information create a folder with the image folder name + datetime stamp
os.mkdir(os.path.join(HIST_DIR, 'EXPERIMENT_'+str(currentDT)))

#copy the data folders from each project result folder in pT1_DIR to HIST_DIR

#copy annotations and detections files to HIST_DIR
shutil.copy(os.path.join(source_dir, 'detections.txt'), os.path.join(destination_dir))

# copy the script to save the parameters of the detection

#copy the