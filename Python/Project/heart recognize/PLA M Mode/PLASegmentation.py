from MultiThreshold import *
from sklearn.cluster import KMeans
import numpy as np
import cv2
import os

import FileIO
from MuscleSampling import SplitContour


class Segment(object):
    """
    class name:
        Segment(VideoPath, ROI, OutputSegDir)
        Parasternal Long Axis view 的 腔室語意分析, 以及定義二尖瓣(Mitral Valve)和動脈瓣膜(Aortic Valve)位置

    parameters:
        VideoPath: 輸入影片的路徑, str
        ROI: 輸入要計算的 ROI 範圍 (二值圖)
        OutputSegDir: 輸入影片的路徑, str
    """

    def __init__(self, VideoPath, ROI, OutputSegDir):
        self.VideoPath = VideoPath
        self.roi = ROI
        self.OutputSegDir = OutputSegDir

        # HandleHeartBound 屬性
        self.ChamberCenX, self.ChamberCenY = 0, 0
        self.MaskChamberBound = None

        # Semantic_FindValve 屬性
        self.Centroids = {"LV": (), "LA": (), "RV": (), "Aortic": ()}
        self.HistoryCenters = {"LV": [], "LA": [], "RV": [], "Aortic": []}

        self.MVUpperList = list()
        self.MVLowerList = list()
        self.AVUpperList = list()
        self.AVLowerList = list()

    def HandleHeartBound(self, Skeleton):
        """
        method name:
            HandleHeartBound(Skeleton):
            定義超音波影像中心臟的範圍

        parameters:
            Skeleton: 輸入骨架圖(3通道), ndarray
        """
        print(f'----- 正在處理 {self.VideoPath} Segmentation -----')
        GraySkeleton = cv2.cvtColor(Skeleton, cv2.COLOR_BGR2GRAY)
        GraySkeleton[self.roi[0] != 255] = 0

        try:
            area_ADD = cv2.morphologyEx(GraySkeleton, cv2.MORPH_CLOSE,
                                        cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)))
            t = GraySkeleton.ravel()

            if t.max() > 100:
                cnt, _ = cv2.findContours(area_ADD, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                hull = list()

                for i in range(len(cnt)):
                    for j in range(len(cnt[i])):
                        hull.append(cnt[i][j])

                hull = np.asarray(hull)
                hull = cv2.convexHull(hull)

                bound = np.zeros((600, 800), np.uint8)
                car_bound = np.zeros((600, 800), np.uint8)

                cv2.drawContours(bound, [hull], 0, (255, 255, 255), -1)
                bound = cv2.erode(bound, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)), iterations=1)
                cnt_B, _ = cv2.findContours(bound, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(car_bound, cnt_B, 0, (255, 255, 255), -1)
                cnt_car_bound, _ = cv2.findContours(car_bound, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                M = cv2.moments(cnt_car_bound[0])
                self.ChamberCenX, self.ChamberCenY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
                self.MaskChamberBound = car_bound

        except ValueError:
            raise ValueError(f'當前骨架圖可能為全黑的')

    def _CreateFeatures(self):
        """
        method name:
            _CreateFeatures():
            創建給 Kmeans 訓練的特徵

        return:
            CenterData: Kmeans 的特徵矩陣, ndarray
        """
        video = cv2.VideoCapture(self.VideoPath)

        CenterData = list()
        mask_roi = self.roi[0]
        ChamberCx, ChamberCy = self.ChamberCenX, self.ChamberCenY

        # regPPT = np.zeros((600, 800, 3), np.uint8)

        while True:
            ret, frame = video.read()

            if not ret:
                break

            frame[mask_roi != 255] = [0, 0, 0]
            median = cv2.medianBlur(frame, 19)

            gray_median = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
            gray_median[mask_roi != 255] = 0

            # - distance transform
            thres = cv2.adaptiveThreshold(gray_median, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 221, 7)
            thres[mask_roi != 255] = 0
            _, thres_inv = cv2.threshold(thres, 120, 255, cv2.THRESH_BINARY_INV)
            thres_inv[mask_roi != 255] = 0

            dist_cb = cv2.distanceTransform(thres_inv, cv2.DIST_L1, 3)
            dist_ms = cv2.distanceTransform(thres, cv2.DIST_L1, 3)

            cv2.normalize(dist_cb, dist_cb, 0, 1.0, cv2.NORM_MINMAX)
            cv2.normalize(dist_ms, dist_ms, 0, 1.0, cv2.NORM_MINMAX)

            _, dist = cv2.threshold(dist_cb, 0.35, 255, cv2.THRESH_BINARY)
            dist = np.uint8(dist)
            dist[self.MaskChamberBound != 255] = 0
            # - distance transform End.

            # -- 取出腔室中心點 & 創建特徵
            # - 取出腔室中心點
            cnt_center, _ = cv2.findContours(dist, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in cnt_center:
                area = cv2.contourArea(c)

                if area > 10:
                    HullC = cv2.convexHull(c)
                    x, y, w, h = cv2.boundingRect(HullC)
                    CenterX, CenterY = int(x + w / 2), int(y + h / 2)
                    # - 取出腔室中心點 End.
                    # cv2.circle(regPPT, (CenterX, CenterY), 3, (255, 255, 255), -1)

                    # - 創建特徵
                    diff_w, diff_h = CenterX - ChamberCx, CenterY - ChamberCy

                    # 用角度做 (為了要和 象限 及 角度一致, 因此要先判斷方向)
                    R = np.sqrt((CenterX - ChamberCx) ** 2 + (CenterY - ChamberCy) ** 2)
                    if R == 0:
                        theta = 0
                    else:
                        theta = np.degrees(np.arccos((CenterX - ChamberCx) / R))

                    # 由於 numpy & math 角度亂轉, 要多一點判斷式子
                    # 角度固定從 3 點鐘方向 順時針轉
                    if theta > 90:
                        theta -= 90
                    if abs(diff_h) > abs(diff_w):
                        theta = 90 - theta if theta < 45 else theta
                    if abs(diff_w) > abs(diff_h):
                        theta = 90 - theta if theta > 45 else theta

                    # LA 位置(+, +) 角度小於 90(不影響象限角)
                    if diff_w >= 0 and diff_h <= 0:  # LV 位置 (+, -) 角度 270 ~ 360
                        theta = 360 - theta
                    elif diff_w <= 0 and diff_h >= 0:  # RA 位置 (-, +) 角度 90 ~ 180
                        theta = 180 - theta
                    elif diff_w <= 0 and diff_h <= 0:  # RV 位置 (-, -) 角度 180 ~ 270
                        theta = 180 + theta

                    Feature = [diff_w, diff_h, theta, CenterX, CenterY]
                    CenterData.append(Feature)
                    # - 創建特徵 End.
            # -- 取出腔室中心點 & 創建特徵 End.
        # cv2.imshow('regPPT', regPPT)
        # cv2.waitKey(0)
            # if cv2.waitKey(0) == ord('n'):
            #     continue
            # elif cv2.waitKey(0) == ord('q'):
            #     break

        return CenterData

    def _KmeansCluster(self, ClusterData):
        """
        method name:
            _KmeansCluster(ClusterData):
            利用 Kmeans 分群, 計算出 4 個腔室的質心位置

        parameters:
            ClusterData: 輸入 _CreateFeatures 的回傳值

        return:
            _KmeansAnomalyDetection(*params): 針對 Kmeans 的結果做異常檢測處理
        """

        if len(ClusterData) != 0:
            ClusterData = np.asarray(ClusterData)
            FeatureData, YData = ClusterData[:, :-1], ClusterData[:, -1]
            kmeans = KMeans(n_clusters=4, n_init=10)
            kmeans.fit(FeatureData, YData)
            YPred = kmeans.predict(FeatureData)

            regPPT2 = np.zeros((600, 800, 3), np.uint8)
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
            for regI, regV in enumerate(YPred):
                cv2.circle(regPPT2, (int(ClusterData[regI][3]), int(ClusterData[regI][4])), 3, colors[regV], -1)

            # - 取出 Kmeans 的質心位置
            Cluster_Centers = kmeans.cluster_centers_

            Centroid_pts = list()
            for cluster_index, feature in enumerate(Cluster_Centers):
                dx, dy, angle, Xpoint = feature

                # 改用 dx, dy 去抓質心位置(沒有差太多, 而且相對來說角度較準)
                Xpt = int(self.ChamberCenX + dx)
                Ypt = int(self.ChamberCenY + dy)
                Centroid_pts.append((Xpt, Ypt))
            # - 取出 Kmeans 的質心位置 End.

            for regI, regV in enumerate(Centroid_pts):
                cv2.circle(regPPT2, regV, 10, colors[regI-1], -1)
            print(f'Centroid_pts: {Centroid_pts}')
            cv2.imshow('regPPT2', regPPT2)
            cv2.waitKey(0)

        else:
            raise IndexError()

        return Centroid_pts

    def Semantic_FindValve(self, isOutputSegVideo=False):
        """
        method name:
            Semantic_FindValve(isOutputSegVideo=False):
            Semantic Parasternal Long Axis view 的腔室位置, 以及定義二尖瓣(Mitral Valve)和動脈瓣膜(Aortic Valve)位置

        parameters:
            isOutputSegVideo: 是否輸入 Semantic 的影片, 默認 False
        """

        CenterData = self._CreateFeatures()
        self.Centroids = self._KmeansCluster(CenterData)

        # video = cv2.VideoCapture(self.VideoPath)
        #
        # mask_roi, o, radius = self.roi
        # ChamberCx, ChamberCy = self.ChamberCenX, self.ChamberCenY
        #
        # while True:
        #     ret, frame = video.read()
        #
        #     if not ret:
        #         break
        #
        #     frame[mask_roi != 255] = [0, 0, 0]
        #     median = cv2.medianBlur(frame, 19)
        #
        #     gray_median = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
        #     gray_median[mask_roi != 255] = 0
        #
        #     # - distance transform
        #     thres = cv2.adaptiveThreshold(gray_median, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 221, 7)
        #     thres[mask_roi != 255] = 0
        #     _, thres_inv = cv2.threshold(thres, 120, 255, cv2.THRESH_BINARY_INV)
        #     thres_inv[mask_roi != 255] = 0
        #
        #     dist_cb = cv2.distanceTransform(thres_inv, cv2.DIST_L1, 3)
        #     dist_ms = cv2.distanceTransform(thres, cv2.DIST_L1, 3)
        #
        #     cv2.normalize(dist_cb, dist_cb, 0, 1.0, cv2.NORM_MINMAX)
        #     cv2.normalize(dist_ms, dist_ms, 0, 1.0, cv2.NORM_MINMAX)
        #     # print(np.unique(dist_cb))
        #
        #     _, dist = cv2.threshold(dist_cb, 0.3, 255, cv2.THRESH_BINARY)
        #     dist = np.uint8(dist)
        #     dist[self.MaskChamberBound != 255] = 0
        #     # - distance transform End.
        #
        #     cnt_center, _ = cv2.findContours(dist, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #
        #     for c in cnt_center:
        #         area = cv2.contourArea(c)
        #
        #         if area > 10:
        #             HullC = cv2.convexHull(c)
        #             x, y, w, h = cv2.boundingRect(HullC)
        #             CenterX, CenterY = int(x + w / 2), int(y + h / 2)
        #             # - 取出腔室中心點 End.
        #
        #             # - 創建特徵
        #             diff_w, diff_h = CenterX - ChamberCx, CenterY - ChamberCy
        #
        #             # 用角度做 (為了要和 象限 及 角度一致, 因此要先判斷方向)
        #             R = np.sqrt((CenterX - ChamberCx) ** 2 + (CenterY - ChamberCy) ** 2)
        #             if R == 0:
        #                 theta = 0
        #             else:
        #                 theta = np.degrees(np.arccos((CenterX - ChamberCx) / R))
        #
        #             # 由於 numpy & math 角度亂轉, 要多一點判斷式子
        #             # 角度固定從 3 點鐘方向 順時針轉
        #             if theta > 90:
        #                 theta -= 90
        #             if abs(diff_h) > abs(diff_w):
        #                 theta = 90 - theta if theta < 45 else theta
        #             if abs(diff_w) > abs(diff_h):
        #                 theta = 90 - theta if theta > 45 else theta
        #
        #             # LA 位置(+, +) 角度小於 90(不影響象限角)
        #             if diff_w >= 0 and diff_h <= 0:  # LV 位置 (+, -) 角度 270 ~ 360
        #                 theta = 360 - theta
        #             elif diff_w <= 0 and diff_h >= 0:  # RA 位置 (-, +) 角度 90 ~ 180
        #                 theta = 180 - theta
        #             elif diff_w <= 0 and diff_h <= 0:  # RV 位置 (-, -) 角度 180 ~ 270
        #                 theta = 180 + theta

        pass
