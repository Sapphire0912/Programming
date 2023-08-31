from find_roi import FindROI
from find_unit import handle_unit
from read_file import Allfiles
from sklearn.cluster import OPTICS
import matplotlib.pyplot as plt
import numpy as np
import cv2

# 讀取指定副檔名的檔案
input_dir = '.\\video\\'
avi_files = Allfiles(input_dir, '.avi')
skeleton_files = Allfiles('.\\ske_png\\', '.png')

for path in avi_files:
    # ----- Pre. 處理基礎資訊
    # 抓出 ROI
    video = FindROI(path)
    video.roi_region(path)
    mask_roi = video.roi

    # 抓出標準單位
    unit = handle_unit(path)

    # 找出 skeletonize 的有效矩形區域
    file_name = path.split('\\')[-1]
    skeleton = cv2.imread('.\\ske_png\\' + file_name + '.png')
    skeleton[mask_roi != 255] = [0, 0, 0]
    gray_skeleton = cv2.cvtColor(skeleton, cv2.COLOR_BGR2GRAY)
    cnt_ske, _ = cv2.findContours(gray_skeleton, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x_bound, y_bound = list(), list()
    for i in range(len(cnt_ske)):
        for j in range(len(cnt_ske[i])):
            x_bound.append(cnt_ske[i][j][0][0])
            y_bound.append(cnt_ske[i][j][0][1])

    x1, x2, y1, y2 = min(x_bound), max(x_bound), min(y_bound), max(y_bound)
    w, h = x2 - x1, y2 - y1
    mask_roi_effect = mask_roi[y1:y2, x1:x2]

    # 嘗試用分群來區分肌肉區塊(聚類演算法) 取出 key points
    # wait
    # ----- Pre. OK

    # Target: 找出瓣膜位置
    while video.ret:
        frame = video.get_frame()

        if not video.ret:
            break

        frame[mask_roi != 255] = [0, 0, 0]
        frame_effect = frame[y1:y2, x1:x2]

        # 中值濾波取平均當門檻值做二值化
        gray = cv2.cvtColor(frame_effect, cv2.COLOR_BGR2GRAY)
        med_blur = cv2.medianBlur(gray, 15)
        avg = int(np.sum(med_blur) / np.unique(mask_roi_effect, return_counts=True)[1][-1])

        mask_cnt_thres = np.zeros(gray.shape, np.uint8)
        _, thres = cv2.threshold(med_blur, avg-5, 255, cv2.THRESH_BINARY)
        cnt_thres, _ = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        print('avg:', avg)
        frame_effect[thres == 255] = [255, 0, 0]
        cv2.imshow('med_blur', med_blur)
        cv2.imshow('thres', thres)
        cv2.imshow('frame_effect', frame_effect)
        cv2.waitKey(100)





