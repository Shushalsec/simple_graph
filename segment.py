import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors



BASE_DIR = 'C:/Users/st18l084/Dropbox/'
FILE = 'nemo0.jpg'
WSI = '366b_2.jpg'
flags = [i for i in dir(cv2) if i.startswith('COLOR_BGR')]
flags
nemo = cv2.imread(os.path.join(BASE_DIR, WSI))
nemo = cv2.cvtColor(nemo, cv2.COLOR_BGRA2RGB)
plt.imshow(nemo)

r, g, b = cv2.split(nemo)
fig = plt.figure()
axis = fig.add_subplot(1, 1, 1, projection="3d")

pixel_colors = nemo.reshape((np.shape(nemo)[0]*np.shape(nemo)[1], 3))
norm = colors.Normalize(vmin=-1.,vmax=1.)
norm.autoscale(pixel_colors)
pixel_colors = norm(pixel_colors).tolist()
axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")

hsv_nemo = cv2.cvtColor(nemo, cv2.COLOR_RGB2HSV)
h, s, v = cv2.split(hsv_nemo)
fig = plt.figure()
axis = fig.add_subplot(1, 1, 1, projection="3d")

axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
axis.set_xlabel("Hue")
axis.set_ylabel("Saturation")
axis.set_zlabel("Value")
plt.show()
from matplotlib.colors import hsv_to_rgb
center[:,0]
x = center[:,0]
x
square = np.full((10, 10, 3), x, dtype=np.uint8) / 255.0
plt.imshow(hsv_to_rgb(square))
plt.show()







light_orange = (1, 190, 200)
dark_orange = (18, 255, 255)
mask = cv2.inRange(hsv_nemo, light_orange, dark_orange)
result = cv2.bitwise_and(nemo, nemo, mask)
plt.subplot(1, 2, 1)
plt.imshow(mask, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()
from matplotlib.colors import hsv_to_rgb
light_white = (0,0,200)
dark_white = (145, 60, 255)
mask_white = cv2.inRange(hsv_nemo, light_white, dark_white)
results_white = cv2.bitwise_and(nemo, nemo, mask=mask_white)
plt.subplot(1,2,1)
plt.imshow(mask_white, cmap='gray')
plt.subplot(1,2,2)
plt.imshow(results_white, cmap='gray')
final_mask = mask+mask_white
final_result = cv2.bitwise_and(nemo, nemo, mask=final_mask)
plt.subplot(1,2,1)
plt.imshow(final_mask, cmap='Purples')
plt.subplot(1,2,2)
plt.imshow(final_result)
plt.show()

blur = cv2.GaussianBlur(final_result, (7,7), 0)
plt.imshow(blur)

#################################################################################
# img = cv2.imread(os.path.join(BASE_DIR, WSI))
img = nemo
plt.imshow(img)
Z = img.reshape((-1,3))

# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3
ret,label,center=cv2.kmeans(Z,K,None,criteria,20,cv2.KMEANS_RANDOM_CENTERS)

# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))
plt.imshow(label.reshape((img.shape[:2]))==1, cmap='gray')
cv2.imshow('res2',res2)
cv2.waitKey(0)
cv2.destroyAllWindows()
plt.subplot(1,3,1)
plt.imshow()
plt.subplot(1,3,2)
plt.imshow(res2)
plt.subplot(1,3,3)
plt.imshow(res2)
plt.subplot(1,3,4)
plt.imshow(res2)
