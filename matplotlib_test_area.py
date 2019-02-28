class FirstClass:
    def setdata(self, value):
        self.data = value
    def display(self):
        print(self.data)

class SecondClass(FirstClass):
    def display(self):
        print('bla bla bla')

class ThirdClass(SecondClass):
    def __init__(self, value):
        self.data = value
    def __add__(self, other):
        return ThirdClass(self.data + other)
    def __str__(self):
        return('[ThirdClass: {} ]'.format(self.data))
    def mul(self, other):
        self.data *= other


a = ThirdClass('abc')

a.display()

print(a)

b = a + 'def'

a.mul(3)
print(a)
ThirdClass.__bases__

import os
files = [file for file in os.listdir(r'Z:\GRP Dawson\02_Whole slides\2018-189_pT1 Study') if 'HE' in file and '.mrxs' in file]
import pandas as pd
file_df = pd.DataFrame(files)
file_df.to_excel('pt1_he_image_list.xlsx')