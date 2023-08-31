import FileIO
from MultiThreshold import MultiThres

import numpy as np
import cv2
from skimage.morphology import skeletonize


ImgDir = "E:\\MyProgramming\\Python\\Project\\implement\\zebra fish\\test img\\"
OutputImgDir = "E:\\MyProgramming\\Python\\Project\\implement\\zebra fish\\test img\\test sobel2\\"
ImgPathList = FileIO.AllFiles(ImgDir, 'bmp')

for imgPath in ImgPathList:
    FIleName = imgPath.split('\\')[-1]
    print(f'FileName: {FIleName}')

    img = cv2.imread(imgPath)
    ROI = np.ones(img.shape[:2], np.uint8) * 255

    # gray (test sobel dir)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    med_blur = cv2.medianBlur(gray, 5)
    # sobel = cv2.Sobel(gray, ddepth=-1, dx=1, dy=1, ksize=5)
    # gray (test sobel dir) End.

    # 1st Multi-Threshold
    Multi = MultiThres(gray, ROI, 4, 1, 255)
    Multi.SearchMax()
    print('1st:', Multi.ValueList)
    threshold = Multi.threshold()
    # End.

    # -- 找出最大階區塊的輪廓
    level = np.unique(threshold)
    maxLevelImg = threshold.copy()
    maxLevelImg[maxLevelImg != level[-1]] = 0

    Cnt_maxLevel, _ = cv2.findContours(maxLevelImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 1. 以最大面積(通常為身體)當基準
    maxArea, maxIndex = 0, 0
    for i, cnt in enumerate(Cnt_maxLevel):
        area = cv2.contourArea(cnt)
        if area > maxArea:
            maxArea, maxIndex = area, i

    targetCnt = Cnt_maxLevel[maxIndex]

    # 2. waiting, 若真的要做 需要調整對比度試試看
    ROI2 = np.zeros(img.shape[:2], np.uint8)
    cv2.drawContours(ROI2, [targetCnt], 0, (255, 255, 255), -1)
    ROI2 = cv2.bitwise_not(ROI2)
    # med_blur[ROI2 != 255] = 0
    # med_blur[med_blur > 31] = 0
    # med_blur = cv2.resize(med_blur, (960, 480), cv2.LINE_AA)
    # threshold = cv2.resize(threshold, (960, 480), cv2.LINE_AA)

    # cv2.imshow('med_blur', med_blur)
    # cv2.imshow('threshold', threshold)
    # cv2.waitKey(0)

    # 2nd Multi-Threshold
    gray[ROI2 != 255] = 0
    max_value = np.max(gray)
    Multi = MultiThres(gray, ROI2, 4, 1, max_value)
    Multi.SearchMax()
    print('2nd:', Multi.ValueList, 'Max Value: ', max_value)
    threshold = Multi.threshold()
    # End.

    ROI2 = cv2.resize(ROI2, (960, 480), cv2.LINE_AA)
    threshold = cv2.resize(threshold, (960, 480), cv2.LINE_AA)
    cv2.imshow('threshold', threshold)
    cv2.waitKey(0)

    # -- draw bounding box
    # minRect = cv2.minAreaRect(targetCnt)
    # points = cv2.boxPoints(minRect).astype(np.int0)
    # cv2.drawContours(img, [points], 0, (0, 0, 255), 5)
    # -- draw bounding box

    # cv2.imwrite(OutputImgDir + FIleName.replace('.bmp', '.png'), sobel)
    # cv2.waitKey(0)
