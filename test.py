import numpy as np
import matplotlib.pyplot as plt


x = np.arange(-10, 10, 0.1)
y = np.sin(x)

fig = plt.figure()
ax = fig.add_subplot(111)

#Family y = sinbx
plt.plot(x,y)
y1 = np.sin(2*x)
plt.plot(x,y1)