import cv2
import numpy as np

path1 = 'D:\\pic\\anime\\angel01.jpg'
path2 = 'D:\\pic\\anime\\angel02.jpg'
output_path = 'D:\\pic\\anime\\merge_angel01_test.png'
pic1 = cv2.imread(path1)
pic2 = cv2.imread(path2)

pic1_2 = np.hstack([pic1, pic2])
# blur = cv2.GaussianBlur(pic1_2, (5, 5), 0)

# cv2.imshow('pic1', pic1)
# cv2.imshow('pic2', pic2)
cv2.imshow('pic1 2', pic1_2)
cv2.imwrite(output_path, pic1_2)
# cv2.imshow('blur', blur)
cv2.waitKey(0)
