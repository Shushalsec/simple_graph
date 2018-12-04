import os
import file_organiser
import segment
import graph_writer

myfolder = 'M:/ged-shushan/ged-shushan/data/Letter/results'

file_organiser.final_organiser(myfolder)
segment.crypt_percentage_all(myfolder)
mydict = graph_writer.graph_extracter(myfolder)
graph_writer.addCXLs(myfolder, mydict)