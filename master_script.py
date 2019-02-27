import os
import file_organiser
import segment
import Class_graphs

#myfolder = 'M:/ged-shushan/ged-shushan/data/Letter/results'
myfolder = r'C:\Users\shton\Desktop\QP_output'

file_organiser.final_organiser(myfolder)
segment.crypt_percentage_all(myfolder)
Class_graphs.assemble_data(myfolder)