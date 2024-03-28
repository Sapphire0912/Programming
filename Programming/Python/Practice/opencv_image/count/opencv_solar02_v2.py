import numpy as np
import cv2


path = './count/DJI_0002.JPG'
ori = cv2.imread(path)
# print(ori.shape)  # (2160, 3840, 3)

ori = cv2.resize(ori, (1280, 720), interpolation=cv2.INTER_AREA)
