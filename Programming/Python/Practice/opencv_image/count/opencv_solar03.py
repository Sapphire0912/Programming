import cv2
import numpy as np


path = "./count/DJI_0010.JPG"
ori = cv2.imread(path)
# print(ori.shape)  # (3078, 5472, 3)

re_ori = cv2.resize(ori, (1368, 770), interpolation=cv2.INTER_AREA)

# HSV
hsv = cv2.cvtColor(re_ori, cv2.COLOR_BGR2HSV)
hsv_f = cv2.cvtColor(re_ori, cv2.COLOR_BGR2HSV_FULL)

cv2.imshow("hsv", hsv)
cv2.imshow("hsv_f", hsv_f)

cv2.waitKey(0)
cv2.destroyAllWindows()
