# file to calculate area inside a polygon
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# Step 1. Use 4 points and find intersection

a1 = [0, 5]
a2 = [1, 8]
b1 = [0, 6]
b2 = [1, 2]

da = np.subtract(a2, a1)
db = np.subtract(b2, b1)
dp = np.subtract(a1, b1)

dap = np.array([-da[1], da[0]])

denom = dap.dot(db)
num = dap.dot(dp)
(float(num) / denom)*db + b1
# ------------------------------------------------------------------------------
# Step 2. Use the same 4 points, similar to two points on moving averages that cross


line3 = np.array([5, 8])
line4 = np.array([6, 2])

plt.plot(line3)
plt.plot(line4)
plt.show()

# intersection(line3, line4)
cross_indices = crossover(line3, line4)

# VERSION 1
test = list(map(lambda x: [[line3[x-1], line3[x]], [line4[x-1], line4[x]]], cross_indices))
# VERSION 2
def foo(x):
    return [[line3[x-1], line3[x]], [line4[x-1], line4[x]]]
test = list(map(foo, cross_indices))

matrices = test[0]

da = [1, matrices[0][1] - matrices[0][0]]
db = [1, matrices[1][1] - matrices[1][0]]

































def crossover(x1, x2):
    crossovers = []
    x1_gt_x2 = list(np.array(x1) > np.array(x2))
    current_val = x1_gt_x2[0]
    for index, val in enumerate(x1_gt_x2[1:]):
        if val != current_val:
            crossovers.append(index+1)
        current_val = val
    return crossovers


def intersection(line3, line4):
    da = np.subtract(a2, a1)
    db = np.subtract(b2, b1)
    dp = np.subtract(a1, b1)

    dap = np.array([-da[1], da[0]])

    denom = dap.dot(db)
    num = dap.dot(dp)
    return (float(num) / denom)*db + b1


def area_between(line1, line2):
    ''' Return the area between line1 and line2 '''
    diff = np.subtract(line1, line2)
    x1 = diff[:-1]
    x2 = diff[1:]

    triangle_area = abs(x2 - x1) * .5
    square_area = np.amin(zip(x1, x2), axis=1)

    return np.sum([triangle_area, square_area])
