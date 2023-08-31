import cv2
import numpy as np
import time
import scipy.signal as signal
from scipy import interpolate
import matplotlib.pyplot as plt


class MultiThres(object):
    def __init__(self, List, division, min, max):
        linear_time_st = time.time()

        # 一階內插
        Lst = []
        ori_Lst = []
        for index in range(len(List)):
            # 取灰階值範圍
            if min < index < max:
                LeftVal, RightVal = 0, 0
                LeftPos, RightPos = 0, 0
                ori_Lst.append(List[index])

                if List[index] == 0:
                    # 若 當前 grayscale = 0, 則左右取值做內插
                    # Left
                    for left in range(index - 1, 0, -1):
                        if List[left] != 0:
                            LeftVal = List[left]
                            LeftPos = left
                            break

                    # Right
                    for right in range(index + 1, max, 1):
                        if List[right] != 0:
                            RightVal = List[right]
                            RightPos = right
                            break

                    # 間距
                    x_interval = RightPos - LeftPos  # x distance
                    y_interval = RightVal - LeftVal  # y distance
                    m = y_interval / x_interval  # slope
                    # y = m(x - x1) + y1
                    y = np.round(m * (index - LeftPos) + LeftVal, 1)
                    Lst.append(y)

                else:
                    Lst.append(List[index])
        linear_time_end = time.time()
        # print(f'一階內插時間: {round(linear_time_end - linear_time_st, 3)} 秒')

        Length = len(Lst)

        self.L = (0, int(Length / 3))
        self.M = (int(Length / 3), int(Length * 2 / 3))
        self.H = (int(Length * 2 / 3), Length)
        self.min = min
        self.max = max
        self.list = Lst
        self.List = List

    def search_max(self):
        global H_value, M_value, L_value, ZL_value, LM_value, MH_value, HX_value, MV, LV, HV
        # print(len(list))
        for k in range(0, 3, 1):
            if k == 0:
                temp = []
                for i in range(self.L[0], self.L[1], 1):
                    temp.append(self.list[i])
                L_value = temp.index(max(temp))+self.L[0]+self.min
                LV = temp.index(max(temp))+self.L[0]
                # if LV == 0:
                #     LV += 1

            elif k == 1:
                temp = []
                for i in range(self.M[0], self.M[1], 1):
                    temp.append(self.list[i])
                M_value = temp.index(max(temp))+self.M[0]+self.min
                MV = temp.index(max(temp))+self.M[0]

            elif k == 2:
                temp = []
                for i in range(self.H[0], self.H[1], 1):
                    temp.append(self.list[i])
                H_value = temp.index(max(temp))+self.H[0]+self.min
                HV = temp.index(max(temp))+self.H[0]
        # print(len(self.list))

        for i in range(0, 4, 1):
            if i == 0:
                temp = []
                for p in range(0, LV, 1):
                    temp.append(self.list[p])
                ZL_value = temp.index(min(temp))+self.min
                # print(temp.index(min(temp)),min(temp),temp)

            elif i == 1:
                temp = []
                for p in range(LV, MV, 1):
                    temp.append(self.list[p])
                LM_value = temp.index(min(temp)) + LV+self.min
                # print(temp.index(min(temp)),min(temp),temp)
            elif i == 2:
                temp = []
                for p in range(MV, HV, 1):
                    temp.append(self.list[p])
                # print(temp.index(min(temp)),min(temp),temp)

                MH_value = temp.index(min(temp)) + MV+self.min
            elif i == 3:
                temp = []
                for p in range(HV, len(self.list)-1, 1):
                    temp.append(self.list[p])
                HX_value = temp.index(min(temp)) + HV + self.min
                # print(temp.index(min(temp)),min(temp),temp)
                # if HX_value == 0:
                #     HX_value += 1
        return L_value, M_value, H_value, ZL_value, LM_value, MH_value, HX_value

    def _s(self, mat, L, LM, M, MH, H):
        # variable
        alpha_L, beta_L = L, LM - L
        alpha_M, beta_M = M - LM, MH - M
        alpha_H, beta_H = H - MH, 255 - H
        tot_uL, tot_uM, tot_uH = 0, 0, 0
        tot_uLX, tot_uMX, tot_uHX = 0, 0, 0

        # u_i(x_i): LR[rectified(m, x_i) / alpha + rectified(x_i, m) / beta]
        # s = sigma(u_i(x_i)x_i) / sigma(u_i(x_i))

        for i in range(3):
            for j in range(3):
                # handle L
                rlb = L - mat[i, j] if mat[i, j] <= L else 0
                rla = mat[i, j] - L if mat[i, j] >= L else 0

                cLi = rla / alpha_L + rlb / beta_L
                uLi = 1 - cLi if cLi <= 1 else 0
                tot_uL += uLi
                tot_uLX += uLi * mat[i, j]

                # handle M
                rmb = M - mat[i, j] if mat[i, j] <= M else 0
                rma = mat[i, j] - M if mat[i, j] >= M else 0

                cMi = rma / alpha_M + rmb / beta_M
                uMi = 1 - cMi if cMi <= 1 else 0
                tot_uM += uMi
                tot_uMX += uMi * mat[i, j]

                # handle H
                rhb = H - mat[i, j] if mat[i, j] <= H else 0
                rha = mat[i, j] - H if mat[i, j] >= H else 0

                cHi = rha / alpha_H + rhb / beta_H
                uHi = 1 - cHi if cHi <= 1 else 0
                tot_uH += uHi
                tot_uHX += uHi * mat[i, j]

        ML = tot_uLX / (tot_uL + 1e-8)
        MM = tot_uMX / (tot_uM + 1e-8)
        MH = tot_uHX / (tot_uH + 1e-8)
        return np.array([ML, MM, MH])

    def threshold(self, src, L, LM, M, MH, H):
        height, width = src.shape
        result = np.zeros((height-2, width-2), np.uint8)
        for h in range(1, height-1):
            for w in range(1, width-1):
                matrix = src[h-1:h+2, w-1:w+2]
                avg = np.mean(matrix)
                M_array = self._s(matrix, L, LM, M, MH, H)
                # print(f'ML, MM, MH: {M_array[0], M_array[1], M_array[2]}')
                val_index = np.argmin(np.abs(avg - M_array))
                # print(f'val index: {val_index}')

                if val_index == 0:
                    result[h-1, w-1] = 0
                elif val_index == 1:
                    result[h-1, w-1] = 128
                else:
                    result[h-1, w-1] = 255

        return result
