import numpy as np
import cv2


img1 = 'C:/Users/user/Desktop/unknown.png'
img2 = 'C:/Users/user/Desktop/unknown2.png'

ori1 = cv2.imread(img1)
ori2 = cv2.imread(img2)


diff = cv2.subtract(ori1, ori2)
cv2.imshow('diff', diff)
cv2.waitKey(0)
cv2.destroyAllWindows()
