from scipy import signal
from scipy import fftpack
from ctypes import *
import Cconv

import cv2
import numpy as np
import time
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


class MultiThres(object):
    def __init__(self, src, ROI, MinThres=0, MaxThres=255):
        """
        parameters:
            src: 輸入原始圖像
            ROI: ROI 區域
            MinThres: 最小門檻值
            MaxThres: 最大門檻值
        """

        self.roi = ROI
        self.interpolate = self._interpolate(src, ROI, MinThres, MaxThres)

        # SearchMax 的屬性
        self.L, self.M, self.H = 41, 92, 160
        self.LM, self.MH = 80, 143
        self.MinThres = MinThres
        self.MaxThres = MaxThres

    def _interpolate(self, src, roi, MinThres, MaxThres):
        hist_time = time.time()
        # --- 處理影像是否灰階
        if len(src.shape) > 2:
            self.src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        else:
            self.src = src
        # --- 處理影像是否灰階 End.

        # --- 統計影像灰階直方圖, 去除非 ROI 區域
        unique = np.unique(self.src, return_counts=True)
        not_roi_effect = np.unique(roi, return_counts=True)[1][0]
        unique[1][0] = unique[1][0] - not_roi_effect
        # --- 統計影像灰階直方圖, 去除非 ROI 區域 End.
        hist_time_end = time.time()
        # print(f'計算 histogram 時間: {round(hist_time_end - hist_time, 2)} 秒')

        # --- 一階內插
        interpolate_time = time.time()
        # 1. 處理直方圖對應灰階值索引
        hist = np.zeros(256, np.int)
        for index, scale in enumerate(unique[0]):
            hist[scale] = unique[1][index]
        # 1. 處理直方圖對應灰階值索引 End.

        # 2. 線性內插
        for index, scale in enumerate(unique[0]):
            if index == len(unique[0]) - 1:
                break

            if MinThres <= scale <= MaxThres:
                # 代表灰階間有缺值
                if unique[0][index + 1] - unique[0][index] > 1:
                    x_interval = unique[0][index + 1] - unique[0][index]
                    y_interval = unique[1][index + 1] - unique[1][index]
                    slope = y_interval / x_interval

                    for med in range(unique[0][index] + 1, unique[0][index + 1], 1):
                        y_insert = int(np.round(slope * (med - unique[0][index]) + unique[1][index], 0))
                        hist[med] = y_insert

        # 2. 線性內插 End.
        # --- 一階內插 End.
        # interpolate_time_end = time.time()
        # print(f'計算一階內插時間: {round(interpolate_time_end - interpolate_time, 2)} 秒')

        return hist

    def SearchMax(self):
        hist = self.interpolate
        min_t, max_t = self.MinThres, self.MaxThres

        split_range = (max_t - min_t) // 3
        L_range = [min_t, min_t + split_range + 1]
        M_range = [min_t + split_range + 1, max_t - split_range]
        H_range = [max_t - split_range, max_t + 1]

        # --- 定義出三個三角形的位置, 以及個別的最高值
        L = int(np.argmax(hist[L_range[0]:L_range[1]]) + min_t)
        M = int(np.argmax(hist[M_range[0]:M_range[1]]) + M_range[0])
        H = int(np.argmax(hist[H_range[0]:H_range[1]]) + H_range[0])

        LM = int(np.argmin(hist[L:M]) + L)
        MH = int(np.argmin(hist[M:H]) + M)

        self.L, self.M, self.H = L, M, H
        self.LM, self.MH = LM, MH

        # plt.title(f'L, LM, M, MH, H: {L, LM, M, MH, H}')
        # plt.xlabel('Gray Scale')
        # plt.ylabel('Amount')
        #
        # # 1st version data
        # xcale = np.arange(0, max_t+1)
        # hist[:min_t] = 0
        # plt.bar(xcale, hist, alpha=0.6)
        # plt.scatter(L, hist[L], s=60, label='L')
        # plt.scatter(M, hist[M], s=60, label='M')
        # plt.scatter(H, hist[H], s=60, label='H')
        # plt.scatter(LM, hist[LM], s=60, label='LM')
        # plt.scatter(MH, hist[MH], s=60, label='MH')
        # plt.plot([0, L, LM], [0, hist[L], 0], color='red')
        # plt.plot([LM, M, MH], [0, hist[M], 0], color='orange')
        # plt.plot([MH, H, max_t], [0, hist[H], 0], color='green')
        # plt.show()
        # plt.legend()
        # plt.clf()
        # --- 定義出三個三角形的位置, 以及個別的最高值 End.

        # -- self method
        # - L, M, H 取平均
        # L_hist = hist[L_range[0]:L_range[1]]
        # M_hist = hist[M_range[0]:M_range[1]]
        # H_hist = hist[H_range[0]:H_range[1]]
        #
        # L_weight = np.arange(L_range[0], L_range[1])
        # M_weight = np.arange(M_range[0], M_range[1])
        # H_weight = np.arange(H_range[0], H_range[1])
        #
        # L_avg = int(np.sum(L_hist * L_weight) / np.sum(L_hist))
        # M_avg = int(np.sum(M_hist * M_weight) / np.sum(M_hist))
        # H_avg = int(np.sum(H_hist * H_weight) / np.sum(H_hist))
        #
        # # - LM, MH 取最小值
        # LM_hist = hist[L_avg + 1: M_avg]
        # LM_weight = np.arange(L_avg + 1, M_avg)
        #
        # MH_hist = hist[M_avg + 1: H_avg]
        # MH_weight = np.arange(M_avg + 1, H_avg)
        #
        # LM_avg = int(np.sum(LM_hist * LM_weight) / np.sum(LM_hist))
        # MH_avg = int(np.sum(MH_hist * MH_weight) / np.sum(MH_hist))
        #
        # print(f'L, LM, M, MH, H: {L_avg, LM_avg, M_avg, MH_avg, H_avg}')

        # plt.title(f'L, LM, M, MH, H: {L_avg, LM_avg, M_avg, MH_avg, H_avg}')
        # plt.xlabel('Gray Scale')
        # plt.ylabel('Amount')
        #
        # xcale = np.arange(0, max_t+1)
        # hist[:min_t] = 0
        # plt.bar(xcale, hist, alpha=0.6)
        # plt.scatter(L_avg, hist[L_avg], s=60, label='L')
        # plt.scatter(M_avg, hist[M_avg], s=60, label='M')
        # plt.scatter(H_avg, hist[H_avg], s=60, label='H')
        # plt.scatter(LM_avg, hist[LM_avg], s=60, label='LM')
        # plt.scatter(MH_avg, hist[MH_avg], s=60, label='MH')
        # plt.plot([0, L_avg, LM_avg], [0, hist[L_avg], 0], color='red')
        # plt.plot([LM_avg, M_avg, MH_avg], [0, hist[M_avg], 0], color='orange')
        # plt.plot([MH_avg, H_avg, max_t], [0, hist[H_avg], 0], color='green')
        # plt.show()
        # plt.legend()
        # plt.clf()
        # self.L, self.M, self.H = L_avg, M_avg, H_avg
        # self.LM, self.MH = LM_avg, MH_avg
        # -- self method End.

    def threshold(self):
        # create u & ux map
        st = time.time()
        Cconv.U(self.L, self.LM, self.M, self.MH, self.H)

        # show u & ux map
        # u = Cconv.cvar.u
        # addr_u = c_double * 256
        # u = np.array(addr_u.from_address((int(u))))
        #
        # ux = Cconv.cvar.ux
        # addr_ux = c_double * 256
        # ux = np.array(addr_ux.from_address((int(u))))

        # C multi-threshold
        height, width = self.src.shape
        Cconv.thresconv(self.src.astype(np.int32))
        result = Cconv.cvar.result

        addr_x = c_int * width
        addr_xy = addr_x * height
        result = np.array(addr_xy.from_address(int(result))).astype(np.uint8)
        end = time.time()
        # print('C 計算 Multi-threshold 花費時間: ', round(end - st, 2), '秒')
        return result
