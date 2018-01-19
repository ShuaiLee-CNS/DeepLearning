import numpy as np
from numpy import *

a = [[100, 25, 101, 20], [101, 25, 102, 20], [102, 25, 103, 20], [103, 25, 104, 20], [104, 25, 105, 20], [105, 25, 106, 20]]
a1 = mat(a)
point_lon_lat = [102.5, 25.5]
condition1 = (a1[:, 0] <= point_lon_lat[0]) & (a1[:, 1] > point_lon_lat[1]) & (a1[:, 2] > point_lon_lat[0]) & (a1[:, 3] <= point_lon_lat[1])
condition2 = condition1.tolist().index(condition1.max())
if condition2 == 0:
    print("condition2 = %d" % condition2)
else:
    print("bushi0")
# print(condition2)
