from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
import cv2

path = './background.jpg'
img = cv2.imread(path)
img = cv2.resize(img, (384, 216), cv2.INTER_AREA)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
y, x, _ = img.shape

feature_img = np.reshape(img, [-1, 3])
eps = 1
minPts = 6

dbscan = DBSCAN(eps=eps, min_samples=minPts)
dbscan.fit(feature_img)
labels = dbscan.fit_predict(feature_img)

pred = np.reshape(labels, [y, x])


fig, ax = plt.subplots(1, 2)
ax[0].imshow(img)
ax[1].imshow(pred)

plt.show()
