import os
import file_organiser
import segment
import Class_graphs
import json


with open('parameters.txt') as parameter_file:
    parameters = json.load(parameter_file)
myfolder = parameters['qupath_output_path']
# myfolder = r'C:\Users\shton\Desktop\QP_output'

# file_organiser.final_organiser(myfolder)
# segment.crypt_percentage_all(myfolder)
Class_graphs.assemble_data(myfolder)
