from numpy import *
import random

# random_number = random.sample(range(100), 10)
# print(random_number)
a = [[1,2,3],[2,3,4],[3,4,5],[4,5,6],[5,6,7],[6,7,8],[7,8,9],[8,9,0]]
b = random.sample(range(len(a)), 3)
print(b)
c = [a[n] for n in b]
print(c)

name = ['/static/C101217.jpg', '/static/C101218.jpg']
print(name)
name = name[1:]
print(name)