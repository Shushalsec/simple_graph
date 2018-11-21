import os
import file_organiser
import segment
import graph_writer

myfolder = 'C:/Users/st18l084/Dropbox/colon crypt/results2'

file_organiser.final_organiser(myfolder)
segment.crypt_percentage_all(myfolder)
graph_writer.graph_extracter(myfolder)
