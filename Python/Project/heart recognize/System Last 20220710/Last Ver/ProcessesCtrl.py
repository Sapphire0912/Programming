from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
from MultiThreshold import *
from DCMToAVI import DCMInit
import kalman_test as kt
import Rising_pt as Rs
import pandas as pd
import numpy as np
import math
import time
import cv2
import sys
import os

import FileIO
import DCMToAVI
import Preprocessing
import A4CSegmentation
import IOU_LVEF
import Median as Md
# import A4C_EA_Ratio
import A4CGLS

import time
import cv2

def pixelVal(pix, r1, s1, r2, s2):
    if (0 <= pix and pix <= r1):
        return (s1 / r1)*pix
    elif (r1 < pix and pix <= r2):
        return ((s2 - s1)/(r2 - r1)) * (pix - r1) + s1
    else:
        return ((255 - s2)/(255 - r2)) * (pix - r2) + s2
def linear_LR_APEX(list_1,list_2,img,cen,power1,power2,st,ed):
    x = []
    y = []
    for i in range(0, len(list_1), 1):
        x.append(int(list_1[i][1]))
        y.append(list_1[i][0])


    x_out =x

    x = np.array(x)
    y = np.array(y)
    x = x[:, np.newaxis]

    rx = []
    ry = []

    for i in range(0, len(list_2), 1):
        rx.append(int(list_2[i][1]))
        ry.append(list_2[i][0])


    rx_out = rx

    rx = np.array(rx)
    ry = np.array(ry)
    rx = rx[:, np.newaxis]
    def PolynomialRegression(degree=power1, **kwargs):
        return make_pipeline(PolynomialFeatures(degree),
                             LinearRegression(**kwargs))

    ypred = PolynomialRegression(degree=power1).fit(x, y).predict(x)
    def PolynomialRegression(degree=power2, **kwargs):
        return make_pipeline(PolynomialFeatures(degree),
                             LinearRegression(**kwargs))
    rypred = PolynomialRegression(degree=power2).fit(rx, ry).predict(rx)

    # plt.plot(rx,rypred)
    # plt.plot(rx,ry,'o')
    # plt.plot(x,ypred)
    # plt.plot(x, y, 'o')
    # plt.show()
    return  x_out, ypred, rx_out, rypred

def linear_LR(list_1,list_2,img,cen,power1,power2):
    x = []
    y = []
    for i in range(0, len(list_1), 1):
        x.append(int(list_1[i][1]))
        y.append(list_1[i][0])

    # x.append(int(list_2[len(list_2) - 1][0]))
    # y.append(list_2[len(list_2) - 1][1])
    # x.append(int(list_2[len(list_2)-2][0]))
    # y.append(list_2[len(list_2)-2][1])

    x_out =x

    x = np.array(x)
    y = np.array(y)
    x = x[:, np.newaxis]

    rx = []
    ry = []

    for i in range(0, len(list_2), 1):
        rx.append(int(list_2[i][1]))
        ry.append(list_2[i][0])

    # rx.append(int(list_1[len(list_1) - 1][0]))
    # ry.append(list_1[len(list_1) - 1][1])
    # rx.append(int(list_1[len(list_1)-2][0]))
    # ry.append(list_1[len(list_1)-2][1])

    rx_out = rx

    rx = np.array(rx)
    ry = np.array(ry)
    rx = rx[:, np.newaxis]

    def PolynomialRegression(degree=power1, **kwargs):
        return make_pipeline(PolynomialFeatures(degree),
                             LinearRegression(**kwargs))

    ypred = PolynomialRegression(degree=power1).fit(x, y).predict(x)
    def PolynomialRegression(degree=power2, **kwargs):
        return make_pipeline(PolynomialFeatures(degree),
                             LinearRegression(**kwargs))
    rypred = (PolynomialRegression(degree=power2).fit(rx, ry).predict(rx))

    # plt.plot(rx,rypred)
    # plt.plot(rx,ry,'o')
    # plt.plot(x,ypred)
    # plt.plot(x, y, 'o')
    # plt.show()
    return  x_out, ypred, rx_out, rypred

def linear(list,img,cen,power,st,ed):
    x = []
    y = []
    for i in range(0, len(list), 1):
        x.append(int(list[i][0]))
        y.append(list[i][1])
    x_out =x

    x = np.array(x)
    y = np.array(y)
    x = x[:, np.newaxis]

    def PolynomialRegression(degree=power, **kwargs):
        return make_pipeline(PolynomialFeatures(degree),
                             LinearRegression(**kwargs))

    ypred = PolynomialRegression(degree=power).fit(x, y).predict(x)
    # plt.plot(x,y,'o')
    # plt.plot(x,ypred)
    # plt.show()
    return  x_out, ypred

def linear_apex(list,img,cen,power):
    x = []
    y = []
    for i in range(0, len(list), 1):
        x.append(int(list[i][1]))
        y.append(list[i][0])
    x_out =x

    x = np.array(x)
    y = np.array(y)
    x = x[:, np.newaxis]

    def PolynomialRegression(degree=power, **kwargs):
        return make_pipeline(PolynomialFeatures(degree),
                             LinearRegression(**kwargs))

    ypred = PolynomialRegression(degree=power).fit(x, y).predict(x)
    # plt.plot(x,y,'o')
    # plt.plot(x,ypred)
    # plt.show()
    # plt.clf()

    return  x_out, ypred

def dist_pt(a,b):
    x = np.array((int(a[0]), int(a[1])))
    y = np.array((int(b[0]), int(b[1])))
    dist = np.sqrt(np.sum(np.square(x - y)))
    return dist

def Process(
        InputDCMDir,
        InputGTDir,
        OutputAVIDir,
        OutputSkeletonizeDir,
        OutputSegmentDir,
        OutputGLSDir
):

    """
    function:
        process(
            InputDCMDir,
            OutputAVIDir,
            OutputSkeletonizeDir,
            OutputSegmentDir,
            OutputGLSDir
        ):
        控制系統的流程

    parameters:
        InputDCMDir: DCM 檔案的資料夾路徑, str
        OutputAVIDir: 輸出存放 avi 檔案的資料夾路徑, str
        OutputSkeletonizeDir: 輸出存放骨架圖檔案的資料夾路徑, str
        OutputSegmentDir: 輸出存放定義完瓣膜和腔室的影片資料夾路徑, str
        OutputGLSDir: 輸出存放 DLS 的影片資料夾路徑, str
    """

    # 1. DCMToAVI
    ProcessTime = time.time()
    DCMFiles = FileIO.AllFiles(InputDCMDir, 'dcm')
    if len(DCMFiles) == 0:
        raise ValueError(f"{InputDCMDir} 該路徑底下找不到有 DCM 的檔案.")

    FileCount = 0
    for DCMPath in DCMFiles[:3]:
        FileCount += 1
        print(f'FileCount: {FileCount}')
        print(f'----- 正在進行 {DCMPath} DCM 轉檔 -----')
        DCMStartTime = time.time()

        ConvertAVI = DCMToAVI.DCMInit(
            FilePath=DCMPath,
            OutputDir=OutputAVIDir
        )

        # 讀取 DCM 裡面的 cine rate & bpm
        CineRate, HeartRate = ConvertAVI.fps, ConvertAVI.bpm
        print(f'CineRate {CineRate}, HeartRate: {HeartRate}')

        if not CineRate:
            print(f'{DCMPath}, DCM 資訊裡沒有 Cine Rate 數值\n')
        if not HeartRate:
            print(f'{DCMPath}, DCM 資訊裡沒有 Heart Rate 數值\n')

        DCMEndTime = time.time()
        print(f'===== DCM 轉檔花費時間: {round(DCMEndTime - DCMStartTime, 2)} 秒 =====\n')

        # 2. AVI 影片的預處理 (ROI & Skeletonize)
        PreStartTime = time.time()
        VideoPath = ConvertAVI.AVIPath
        FileName = str(VideoPath.split('\\')[-1]).replace('DCM', 'avi')
        CaseName = FileName[:-4]
        # GTDir = os.path.join(InputGTDir, CaseName)

        print(f'----- 正在進行 {VideoPath} AVI 影像的預處理 -----')

        ROI = Preprocessing.ROI(VideoPath)  # return: roi, (ox, oy), radius
        Preprocessing.Skeletonize(VideoPath, OutputSkeletonizeDir)

        PreEndTime = time.time()
        print(f'===== 完成 {VideoPath} Preprocessing 所需時間: {round(PreEndTime - PreStartTime, 2)} 秒 =====\n')
        # 2. AVI 影片的預處理 (ROI & Skeletonize) End.

        # 3. A4C Segmentation
        SegmentStartTime = time.time()
        SkeletonPath = OutputSkeletonizeDir + FileName + '.png'
        try:
            skeleton = cv2.imread(SkeletonPath)

        except cv2.error:
            print(f'{SkeletonPath}, 沒有找到該檔案的骨架圖')
            continue

        try:
            Segment = A4CSegmentation.Segment(
                VideoPath=VideoPath,
                ROI=ROI,
                OutputSegDir=OutputSegmentDir
            )
            Segment.HandleHeartBound(skeleton)

        except ValueError:
            print(f'{SkeletonPath}, 該骨架圖可能為全黑的')
            continue

        try:
            Segment.Semantic_FindValve(isOutputSegVideo=False)

        except (IndexError, ValueError):
            print(f'{VideoPath}, 統計腔室中心點有問題, 檢查該影片 distance transform 的過程')
            continue

        SegmentEndTime = time.time()
        print(f'===== 完成 {FileName} Segment 所需時間: {round(SegmentEndTime - SegmentStartTime, 2)} 秒 =====\n')
        # 3. A4C Segmentation End.

        # 4. E/A Ratio
        # EAValve = A4C_EA_Ratio.EARatio(
        #     VideoPath=VideoPath,
        #     ROI=ROI,
        #     LeftValvePos=Segment.LeftPivotList,
        #     RightValvePos=Segment.RightPivotList
        # )
        # EAValve.EAWave()

        # 4. Global Longitudinal Strain
        # MatchingStartTime = time.time()
        # print(f'----- 正在進行 {VideoPath} Global Longitudinal Strain 的 Muscle Semantic 處理 -----')
        #
        # try:
        #     MatchLV = A4CGLS.MatchModel(
        #         Path=VideoPath,
        #         ROI=ROI,
        #         OutputMatchingDir=OutputGLSDir
        #     )
        #     LeftValve, RightValve = Segment.LeftPivotList, Segment.RightPivotList
        #     MatchLV.MuscleMatching(LeftValve, RightValve, isOutputVideo=True)
        #
        # except:  # 通常是 fitting 會有狀況
        #     print(f'{VideoPath} Matching 到 Fitting 過程有狀況 (未處理)')
        #     # continue
        #
        # MatchingEndTime = time.time()
        # print(f'===== 完成 {FileName} Muscle Semantic 所需時間: {round(MatchingEndTime - MatchingStartTime, 2)} 秒 =====\n')

        # 4. 計算 LVEF
        print(f'----- 正在計算 {FileName} LVEF -----')
        val = np.zeros([600, 800, 3], dtype=np.uint8)

        pt_L = Md.Median_pt(Segment.LeftPivotList)
        LV_pt = pt_L.calculate()

        pt_R = Md.Median_pt(Segment.RightPivotList)
        RV_pt = pt_R.calculate()

        pt_cen = Md.Median_pt(Segment.HistoryCenters["LV"])
        LV_cn  = pt_cen.calculate()

        write_path = VideoPath.split("\\")[-1]
        write_path = write_path.split(".")[0]

        cap = cv2.VideoCapture(VideoPath)
        # out = cv2.VideoWriter("D:\\System_combine\\compare\\" + FileName, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (800, 600))
        fm_count = 0
        ROi = ROI[0]
        # ecg_region------------------------------------------------------------------------------------------------------------
        ROi = cv2.erode(ROi, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)), iterations=2)
        last_L = []
        last_R = []
        while (cap.isOpened()):

            fm_count    = fm_count + 1
            ret, frame  = cap.read()

            if ret == False:
                break

            text = "Frame_count: " + str(fm_count)
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1, (255, 255, 255), 1, cv2.LINE_AA)
# median_filter------------------------------------------------------------------------------------------------------------
            median      = cv2.medianBlur(frame, 19)
            median_gr   = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
            frame_gr    = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            try:
                # whole_MT------------------------------------------------------------------------------------------------------------
                multi = MultiThres(frame_gr, ROi, 4, 40, 255)
                multi.SearchMax()
                mt_img = multi.threshold()
                mtimg_tmp = mt_img.copy()
                closing = cv2.morphologyEx(mt_img, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),iterations=1)
                cnt, hierarchy = cv2.findContours(mt_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                for c in cnt:
                    area = cv2.contourArea(c)
                    if area < 100:
                        cv2.drawContours(mtimg_tmp, [c], 0, (0, 0, 0), -1)
                # closing = cv2.morphologyEx(mtimg_tmp, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),iterations=1)


                # cnt, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                # for c in cnt:
                #     area = cv2.contourArea(c)
                #     if area < 200:
                #         cv2.drawContours(closing, [c], 0, (0, 0, 0), -1)

    # LV_center------------------------------------------------------------------------------------------------------------
                LV_cen = LV_cn[fm_count - 1]

    # L&R_valve------------------------------------------------------------------------------------------------------------
                Lf = LV_pt[fm_count - 1]
                Rt = RV_pt[fm_count - 1]

                tes = frame.copy()

                # scan_searching------------------------------------------------------------------------------------------------------------
                pt = Rs.Rising_pt(LV_cen, mtimg_tmp, 180, 8, 10, 5, 2)
                result = pt.search_pt()
                test_fr = frame.copy()
                apx = []
                hor = []
                point = []
                apx_pt_x = []
                apx_pt_y = []
                for i in range(1, len(result) - 1, 1):

                    y = int(result[i][0][0])
                    x = int(result[i][0][1])

                    dist_L = dist_pt(Lf, (x, y))
                    dist_R = dist_pt(Rt, (x, y))
                    distant = 20 - int(result[i][1])
                    point.append((x, y))
                    hor.append(distant)
                    apx.append(y)

                    # if i >= 10 and i <= 25:
                    #     apx_pt_x.append(x)
                    #     apx_pt_y.append(y)
                    cv2.circle(closing, (x, y), 3, (int(192), int(240), int(150)), -1)
                    # cv2.circle(frame, (x, y), 3, (int(192), int(240), int(150)), -1)
                cv2.circle(test_fr, (LV_cen[0], LV_cen[1]), 3, (int(20), int(140), int(240)), -1)
                LV_scan = np.zeros([600, 800, 3], dtype=np.uint8)
                for i in range(0, len(point), 1):

                    if i + 1 == len(point):
                        cv2.line(LV_scan, (point[i][0], point[i][1]),
                                 (point[0][0], point[0][1]), (255, 255, 255), 1)

                    else:
                        cv2.line(LV_scan, (point[i][0], point[i][1]),
                                 (point[i + 1][0], point[i + 1][1]), (255, 255, 255), 1)
                LV_scan_gr = cv2.cvtColor(LV_scan, cv2.COLOR_BGR2GRAY)
                cnt, hierarchy = cv2.findContours(LV_scan_gr, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
                c = max(cnt, key=cv2.contourArea)
                cv2.drawContours(LV_scan_gr, [c], -1, (255, 255, 255), -1)

                # cv2.imshow("closing", closing)
                AP = apx.index(min(apx))
                # cv2.circle(frame, (point[AP][0], point[AP][1]), 3, (255, 130, 255), -1)

    # LV_size------------------------------------------------------------------------------------------------------------
                pt = Rs.Rising_pt(LV_cen, mtimg_tmp, 180, 8, 10, 5, 1)
                result = pt.search_pt()



                hor = []
                point_size = []
                for i in range(1, len(result) - 1, 1):
                    y = int(result[i][0][0])
                    x = int(result[i][0][1])
                    dist_L = dist_pt(Lf, (x, y))
                    dist_R = dist_pt(Rt, (x, y))
                    distant = 20 - int(result[i][1])
                    point_size.append((x, y))
                    # pass
                    hor.append(distant)



                    # cv2.circle(frame, (x, y), 3, (int(192 * distant / 20), int(240 * distant / 20), int(150 * distant / 20)), -1)

                LV_area = np.zeros([600, 800, 3], dtype=np.uint8)
                for i in range(0, len(point_size), 1):

                    if i + 1 == len(point_size):
                        cv2.line(LV_area, (point_size[i][0], point_size[i][1]),
                                 (point_size[0][0], point_size[0][1]), (255, 255, 255), 1)

                    else:
                        cv2.line(LV_area, (point_size[i][0], point_size[i][1]),
                                 (point_size[i + 1][0], point_size[i + 1][1]), (255, 255, 255), 1)
                LV_area_gr = cv2.cvtColor(LV_area, cv2.COLOR_BGR2GRAY)

    # L&R_valve_function------------------------------------------------------------------------------------------------------------
                x = [int(Lf[0]), int(Rt[0])]
                y = [int(Lf[1]), int(Rt[1])]

                coefficients = np.polyfit(x, y, 1)
                a = coefficients[0]
                b = coefficients[1]
                y1 = int(a * 0 + b)
                y2 = int(a * 800 + b)
                mid_base = ((int(Lf[0]) + int(Rt[0])) / 2, (int(Lf[1]) + int(Rt[1])) / 2)

                temp = frame.copy()
                cnt, hierarchy = cv2.findContours(LV_area_gr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for c in cnt:
                    area = cv2.contourArea(c)
                    hull = cv2.convexHull(c)
                    cv2.drawContours(LV_area, [hull], 0, (255, 255, 255), -1)
                    cv2.drawContours(LV_area_gr, [hull], 0, (255, 255, 255), -1)
                    cv2.drawContours(temp, [hull], 0, (255, 255, 255), 4)
                    cv2.line(LV_area, (0, y1 + 100),
                             (800, y2 + 100), (0, 0, 0), 100)
                    cv2.line(LV_area_gr, (0, y1 + 100),
                             (800, y2 + 100), (0, 0, 0), 100)
    # -----------------------------------------------------------------------------------------------------------

                Cavity_L = []
                Cavity_R = []
                VL = []
                VR = []
                for i in range(0, len(point), 1):
                    # cv2.circle(frame, (c[i][0][0], c[i][0][1]), 3, (255,255,255), -1)
                    y = int(point[i][1])
                    x = int(point[i][0])
                    dist_L = dist_pt(Lf, (x, y))
                    dist_R = dist_pt(Rt, (x, y))
                    VL.append(dist_L)
                    VR.append(dist_R)

                LI = VL.index(min(VL))
                RI = VR.index(min(VR))
                # cv2.circle(frame, (point[LI][0], point[LI][1]), 3, (255, 255, 255), -1)
                # cv2.circle(frame, (point[RI][0], point[RI][1]), 3, (0, 153, 216), -1)

                for i in range(0, len(point), 1):

                    y = int(point[i][1])
                    x = int(point[i][0])

                    dx = x
                    dy = y

                    if i >= LI and i < AP:
                        # if dx > top_seg_L[0][0]:
                        Cavity_L.append((dx, dy))
                    elif RI >= i and i >= AP:
                        # if dx > top_seg_R[len(top_seg_R)-1][0]:
                        Cavity_R.append((dx, dy))
                Cavity_L.append((point[AP][0], point[AP][1]))
                reg = np.zeros([600, 800,3], dtype=np.uint8)
                # Cavity_L.sort(key=lambda s: s[1])
                # Cavity_R.sort(key=lambda s: s[1])
                LRy_L, LRx_L, LRy_R, LRx_R = linear_LR(Cavity_L, Cavity_R, reg, LV_cen, 4, 3)

                clockwise_pt_x = []
                clockwise_pt_y = []

                for elem in range(len(LRx_L)-1, -1, -1):
                    clockwise_pt_x.append(int(LRx_L[elem]))
                # clockwise_pt_x.append(apex_med[0])
                for elem in range(len(LRx_R) - 1, -1, -1):
                    clockwise_pt_x.append(int(LRx_R[elem]))

                for elem in range(len(LRy_L)-1, -1, -1):
                    clockwise_pt_y.append(LRy_L[elem])
                # clockwise_pt_y.append(apex_med[1] - add)
                for elem in range(len(LRy_R) - 1, -1, -1):
                    clockwise_pt_y.append(LRy_R[elem])

                LV_LR = np.zeros([600, 800, 3], dtype=np.uint8)
                for i in range(0, len(clockwise_pt_x), 1):

                    if i+1 == len(clockwise_pt_x):
                        cv2.line(LV_LR, (clockwise_pt_x[i], clockwise_pt_y[i]),
                            (clockwise_pt_x[0], clockwise_pt_y[0]), (255, 255, 255), 1)

                    else:
                        cv2.line(LV_LR, (clockwise_pt_x[i], clockwise_pt_y[i]),
                            (clockwise_pt_x[i+1], clockwise_pt_y[i+1]), (255, 255, 255), 1)

                LV_LR = cv2.cvtColor(LV_LR, cv2.COLOR_BGR2GRAY)
                cnt, hierarchy = cv2.findContours(LV_LR, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
                c = max(cnt, key=cv2.contourArea)
                cv2.drawContours(LV_LR, [c], -1, (255, 255, 255), -1)
                test = cv2.bitwise_and(frame, LV_area)

                test_gr = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)
                val, count = np.unique(test_gr, return_counts=True);
                avg = np.sum(val * count / np.sum(count[1:]))
                ret_S, thres = cv2.threshold(test_gr, avg * 1.5, 255, cv2.THRESH_BINARY_INV)
                thres = cv2.bitwise_and(thres, LV_area_gr)
                thres = cv2.morphologyEx(thres, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)),
                                         iterations=4)
                thres = cv2.erode(thres, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
                lst = cv2.bitwise_and(thres, LV_area_gr)
                lst = cv2.erode(lst, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
                cnt, hierarchy = cv2.findContours(lst, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
                c = max(cnt, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(c)

                # draw the biggest contour (c) in green
                LV_mor = np.zeros([600, 800, 3], dtype=np.uint8)
                cv2.drawContours(LV_mor, [c], -1, (255, 255, 255), -1)
                LV_mor_gr = cv2.cvtColor(LV_mor, cv2.COLOR_BGR2GRAY)
                LV_LR = cv2.dilate(LV_LR, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
                LV_mor = cv2.bitwise_and(LV_mor_gr, LV_LR)

                cnt, hierarchy = cv2.findContours(LV_mor, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
                c = max(cnt, key=cv2.contourArea)
                # print(c)
                VL = []
                VR = []
                temp_y = []
                for i in range(0, len(c), 1):
                    # cv2.circle(frame, (c[i][0][0], c[i][0][1]), 3, (255,255,255), -1)
                    y = int(c[i][0][1])
                    x = int(c[i][0][0])
                    dist_L = dist_pt(Lf, (x, y))
                    dist_R = dist_pt(Rt, (x, y))
                    VL.append(dist_L)
                    VR.append(dist_R)
                    temp_y.append(y)
                LI = VL.index(min(VL))
                RI = VR.index(min(VR))
                # print(Lf,Rt)

                ap = temp_y.index(min(temp_y))

                # print((c[LI][0][0],c[LI][0][1]),(c[RI][0][0],c[RI][0][1]))
                Cavity_L = []
                Cavity_R = []
                Cavity = []

                for i in range(0, len(c), 1):

                    y = int(c[i][0][0])
                    x = int(c[i][0][1])

                    dx = y
                    dy = x

                    if RI <= i and i <= len(c):
                        # if dx > top_seg_L[0][0]:
                        Cavity_L.append((dx, dy))
                    elif i <= LI and i >= ap:
                        # if dx > top_seg_R[len(top_seg_R)-1][0]:
                        Cavity_R.append((dx, dy))
                Cavity_L.sort(key=lambda s: s[1])
                Cavity_R.sort(key=lambda s: s[1])
                top_seg = []
                top_seg_L = []
                top_seg_R = []
                for i in range(0, len(c), 1):
                    y = int(c[i][0][0])
                    x = int(c[i][0][1])
                    if i < 25:
                        top_seg_L.append((x, y))
                    elif i > (len(c) - 25):
                        top_seg_R.append((x, y))

                top_seg_R.sort(key=lambda s: s[1])
                top_seg_L.sort(key=lambda s: s[1])
                # top_seg_L.reverse()
                top_seg_L.extend(top_seg_R)

                LV_x, LV_y = linear_apex(top_seg_L, reg, LV_cen, 2)
                LRy_L, LRx_L, LRy_R, LRx_R = linear_LR(Cavity_L, Cavity_R, reg, LV_cen, 4, 3)

                res_pt_L = []
                res_pt_R = []
                div_L = len(LRy_L)/20
                div_R = len(LRx_R)/20
                for i in range(20,0,-1):
                    k = int(i*div_R)-1
                    cv2.circle(frame, (int(LRx_R[k]), int(LRy_R[k])), 3, (240, 153, 216), -1)
                    res_pt_R.append((int(LRx_R[k]), int(LRy_R[k])))
                # for i in range(len(LRx_R) - 1, 0, -div_R):
                #     res_pt_R.append((int(LRx_R[i]), int(LRy_R[i])))

                for i in range(20,0,-1):
                    k = int(i*div_L)-1
                    cv2.circle(frame, (int(LRx_L[k]), int(LRy_L[k])), 3, (240, 153, 216), -1)
                    res_pt_L.append((int(LRx_L[k]), int(LRy_L[k])))



                last_L.append(res_pt_L)
                last_R.append(res_pt_R)

            except:
                L_emt = np.zeros(shape=(20, 2))
                R_emt = np.zeros(shape=(20, 2))
                last_L.append(L_emt)
                last_R.append(R_emt)
            # cv2.imshow("frame", frame)
            # cv2.imshow("con", con)
            # out.write(frame)
        #     key = cv2.waitKey(1)
        #     if key == ord('q') or key == 27:
        #         break
        #     elif key == ord(' '):
        #         while cv2.waitKey(1) != ord(' '):
        #             pass
        #
        # cv2.destroyAllWindows()

        fm_count = len(last_L)
        rows, cols = (fm_count, 2)
        result_L = np.zeros(shape=(rows, 20, cols))
        result_R = np.zeros(shape=(rows, 20, cols))
        for i in range(0, 20, 1):
            tmp_L = []
            tmp_R = []
            for k in range(0, fm_count, 1):
                # print(k)
                tmp_L.append((int(last_L[k][i][0]), int(last_L[k][i][1])))
                tmp_R.append((int(last_R[k][i][0]), int(last_R[k][i][1])))

            pt_l = Md.Median_pt(tmp_L)
            tmp_L_med = pt_l.calculate()

            pt_r = Md.Median_pt(tmp_R)
            tmp_R_med = pt_r.calculate()

            for q in range(0, fm_count, 1):
                # print(q)
                result_L[q][i][0] = tmp_L_med[q][0]
                result_L[q][i][1] = tmp_L_med[q][1]
                result_R[q][i][0] = tmp_R_med[q][0]
                result_R[q][i][1] = tmp_R_med[q][1]


        cap = cv2.VideoCapture(VideoPath)

        width                = 800
        height               = 600
        # out = cv2.VideoWriter("D:\\Last_System\\IOU_score\\" + FileName, cv2.VideoWriter_fourcc(*'XVID'), 20.0,
        #                       (800, 600))

        # write_path = VideoPath.split("\\")[-1]
        # write_path = write_path.split(".")[0]
        # print(write_path)
        all_frames = []
        frame_count = 0
        result_dict = dict()

        while(cap.isOpened()):

            ret, frame        = cap.read()


            if ret == False:
                break

            fin_LR = []

            # print(result_L)

            for i in range(0, 20, 1):
                fin_LR.append((int(result_R[frame_count][i][0]), int(result_R[frame_count][i][1])))
                cv2.circle(frame, (int(result_R[frame_count][i][0]), int(result_R[frame_count][i][1])), 3, (240, 153, 216), -1)
            for i in range(19, -1, -1):
                fin_LR.append((int(result_L[frame_count][i][0]), int(result_L[frame_count][i][1])))
                cv2.circle(frame, (int(result_L[frame_count][i][0]), int(result_L[frame_count][i][1])), 3, (240, 153, 216), -1)

            result_area = np.zeros([600, 800], dtype=np.uint8)
            for i in range(0, len(fin_LR), 1):
                if i + 1 == len(fin_LR):
                    cv2.line(result_area, (fin_LR[i][0], fin_LR[i][1]),
                             (fin_LR[0][0], fin_LR[0][1]), (255, 255, 255), 1)

                else:
                    cv2.line(result_area, (fin_LR[i][0], fin_LR[i][1]),
                             (fin_LR[i + 1][0], fin_LR[i + 1][1]), (255, 255, 255), 1)

            cnt, hierarchy = cv2.findContours(result_area, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            c = max(cnt, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)

            # draw the biggest contour (c) in green
            # LV_mor = np.zeros([600, 800, 3], dtype=np.uint8)
            cv2.drawContours(result_area, [c], -1, (255, 255, 255), -1)
            result_dict[frame_count + 1] = result_area

            # GTDir = "D:\\\Last_System\\Ground Truth\\"+write_path+"\\"
            # score, frame = IOUScore.HandleIOU(
            #     src=frame,
            #     FrameCount=frame_count+1,
            #     mask=result_area,
            #     GroundTruthDir=GTDir )
            # con = cv2.addWeighted(reg_gr, 0.5, LV_LR, 0.5, 1)
            # result_area = cv2.cvtColor(result_area, cv2.COLOR_GRAY2RGB)
            # frame = cv2.addWeighted(frame, 1, result_area, 0.3, 1)

            # cv2.imshow("result_area", result_area)
            # cv2.imshow("frame", frame)
            # out.write(frame)
            frame_count += 1

            # key = cv2.waitKey(1)
            # if key == ord('q') or key == 27:
            #     break
            # elif key == ord(' '):
            #     while(cv2.waitKey(1)!=ord(' ')):
            #         pass

        # cv2.destroyAllWindows()

        # create UnitCM List
        # UnitList = [
        #     17, 17, 17, 16, 15, 15, 15,
        #     13, 15, 15, 15, 15, 15, 15,
        #     15, 15, 17, 15, 17, 13, 13
        # ]

        # call IOU_LVEF
        # 1. compare two LVEF result
        # GTDir = InputGTDir + CaseName + '\\'
        # lvef = IOU_LVEF.LVEFInfo(
        #     UnitCM=UnitList[FileCount - 1],
        #     Radius=ROI[2]
        # )
        # lvef.FindCycle(result_dict, CineRate, HeartRate)
        # print(lvef.ESVFrame, lvef.EDVFrame)
        # draw Dice value

        # try:
        #     EDV, ESV, LVEF, Degree = lvef.calLVEF(mode='self')  # self lvef
        #     GT_EDV, GT_ESV, GT_LVEF, GT_Degree = lvef.calLVEF(mode='GT', GTDir=GTDir)
        #     print(f'Self -> EDV: {EDV}cm\u00b3, ESV: {ESV}cm\u00b3, LVEF: {LVEF}%, Degree: {Degree}')
        #     print(f'GT -> EDV: {GT_EDV}cm\u00b3, ESV: {GT_ESV}cm\u00b3, LVEF: {GT_LVEF}%, Degree: {GT_Degree}')
        #
        # except IndexError:
        #     print("!!!!! 需要計算 LVEF !!!!!")
        #     EDVTime, ESVTime = lvef.EDVFrame, lvef.ESVFrame
        #     EDVFrame = [result_dict[i] for i in EDVTime]
        #     ESVFrame = [result_dict[i] for i in ESVTime]
        #
        #     GTFiles = FileIO.AllFiles(GTDir, 'png')
        #     GTDict = dict()
        #     for files in GTFiles:
        #         fc = int(files.split('_')[-1].split('.')[0])  # fc -> frame_count
        #         GTDict[fc] = files
        #
        #     EDVArea, ESVArea = list(), list()
        #     for i, _mask in enumerate(EDVFrame):
        #         cnt, _ = cv2.findContours(_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #         _area = cv2.contourArea(cnt[0])
        #         EDVArea.append(_area)
        #
        #     for i, _mask in enumerate(ESVFrame):
        #         cnt, _ = cv2.findContours(_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #         _area = cv2.contourArea(cnt[0])
        #         ESVArea.append(_area)
        #
        #     Text = ["Hyper Dynamic", "Normal", "Mild", "Moderate", "Severe"]
        #     Degree = np.array([70, 49, 39, 29, 0])
        #     EDV, ESV = max(EDVArea), min(ESVArea)
        #     EDV = round(EDV / (UnitList[FileCount - 1] ** 3), 1)
        #     ESV = round(ESV / (UnitList[FileCount - 1] ** 3), 1)
        #
        #     LVEF = round(100 * (EDV - ESV) / EDV, 1)
        #     degree = Text[len(Degree[Degree > LVEF])]
        #
        #     # GT LVEF
        #     GT_EDVList, GT_ESVList = list(), list()
        #     for i in EDVTime:
        #         _mask = cv2.imread(GTDict[i], 0)
        #         cnt, _ = cv2.findContours(_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #         _area = cv2.contourArea(cnt[0])
        #         GT_EDVList.append(_area)
        #
        #     for i in ESVTime:
        #         _mask = cv2.imread(GTDict[i], 0)
        #         cnt, _ = cv2.findContours(_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #         _area = cv2.contourArea(cnt[0])
        #         GT_ESVList.append(_area)
        #
        #     GT_EDV, GT_ESV = max(GT_EDVList), min(GT_ESVList)
        #     GT_EDV = round(GT_EDV / (UnitList[FileCount - 1] ** 3), 1)
        #     GT_ESV = round(GT_ESV / (UnitList[FileCount - 1] ** 3), 1)
        #     GT_LVEF = round(100 * (GT_EDV - GT_ESV) / GT_EDV, 1)
        #     GT_degree = Text[len(Degree[Degree > GT_LVEF])]
        #
        #     print(f'Self -> EDV: {EDV}cm\u00b3, ESV: {ESV}cm\u00b3, LVEF: {LVEF}%, Degree: {degree}')
        #     print(f'GT -> EDV: {GT_EDV}cm\u00b3, ESV: {GT_ESV}cm\u00b3, LVEF: {GT_LVEF}%, Degree: {GT_degree}')

        # write img
        # target = cv2.VideoCapture(VideoPath)
        # _counts = 0
        # _writeDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System Last 20220710\\Last Ver" \
        #             "\\TargetDir\\"
        # while True:
        #     ret, frame = target.read()
        #
        #     if not ret:
        #         break
        #
        #     _counts += 1
        #     # if (_counts in lvef.ESVFrame) or (_counts in lvef.EDVFrame):
        #     _casePath = os.path.join(_writeDir, CaseName)
        #     if not os.path.exists(_casePath):
        #         os.makedirs(_casePath)
        #
        #     _framestr = str(_counts) if _counts > 9 else "0%s" % _counts
        #     _filename = FileName.split('.')[0]
        #     _concat = _filename + '_' + _framestr + '.png'
        #     cv2.imwrite(_casePath + "\\" + _concat, result_dict[_counts])
        #     pass

