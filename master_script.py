import os
import file_organiser
import segment
import Class_graphs
import json

with open('parameters.txt') as parameter_file:
    parameters = json.load(parameter_file)
PROJECT_DIR = os.path.join(parameters['main_dir'], parameters['experiment'])

# myfolder = r'C:\Users\shton\Desktop\QP_output'


for folder in os.listdir(PROJECT_DIR):
    print(folder)
    if os.path.isdir(os.path.join(PROJECT_DIR, folder)) and folder.endswith(parameters['experiment']):
        file_organiser.final_organiser(os.path.join(PROJECT_DIR, folder))
        segment.crypt_percentage_all(os.path.join(PROJECT_DIR, folder))
        Class_graphs.assemble_data(os.path.join(PROJECT_DIR, folder))
