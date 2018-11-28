import os
import file_organiser
import segment
import graph_writer
import CXLWriter

myfolder = 'M:/ged-shushan/ged-shushan/data/Letter/results'

file_organiser.final_organiser(myfolder)
segment.crypt_percentage_all(myfolder)
graph_writer.graph_extracter(myfolder)
