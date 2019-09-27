# file to calculate area inside a polygon
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


line1 = [0, 2, 3, 4]
line2 = [0, 1, 1, 4]
diff = np.subtract(line1, line2)

plt.plot(line1)
plt.plot(line2)
plt.plot(diff)
plt.show()
x1 = diff[:-1]
x2 = diff[1:]

triangle_area = abs(x2 - x1) * .5
square_area = np.amin(zip(x1, x2), axis=1)

area = np.sum([triangle_area, square_area])
