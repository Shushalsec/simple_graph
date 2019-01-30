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