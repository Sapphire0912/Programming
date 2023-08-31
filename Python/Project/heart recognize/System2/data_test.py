
from   skimage.feature import local_binary_pattern
from   skimage.morphology import skeletonize
from   skimage import measure,data,color
import matplotlib.pyplot as plt
from   PIL import Image
import numpy as np
import glob as gb
import skimage
import Median as Md
import time
import cv2 
import os


# def timeMedBlur(lst):
#     afterBlur = list()
#     length = len(lst)
#
#     for i in range(length):
#         if i == 0 or i == length - 1:
#             afterBlur.append(lst[i])
#
#         else:
#             # pts = np.asarray(lst[i-1:i+2])
#             pts = lst[i-1:i+2]
#             medPt = np.sort(pts, axis=0)[1]
#             afterBlur.append(medPt)
#
#     return afterBlur


# last_L = [[(489, 372), (496, 304), (480, 276), (478, 273), (475, 268), (473, 266), (469, 259), (458, 245), (456, 242), (454, 239), (453, 238), (451, 235), (449, 233), (445, 228), (443, 226), (429, 210), (421, 203), (417, 199), (410, 193), (404, 188)], [(510, 382), (521, 336), (508, 301), (499, 283), (497, 280), (495, 277), (494, 275), (493, 274), (492, 273), (486, 264), (483, 259), (459, 231), (450, 222), (435, 210), (435, 210), (433, 208), (424, 202), (420, 199), (413, 195), (403, 189)], [(503, 375), (506, 370), (509, 365), (511, 359), (513, 342), (508, 320), (501, 304), (492, 284), (488, 277), (486, 272), (482, 265), (477, 256), (460, 232), (445, 216), (441, 213), (436, 209), (434, 207), (429, 204), (421, 199), (415, 195)], [(509, 380), (510, 374), (511, 362), (512, 345), (509, 322), (504, 305), (497, 288), (491, 279), (487, 272), (484, 268), (478, 261), (473, 255), (461, 241), (459, 239), (452, 232), (448, 228), (440, 220), (430, 210), (424, 205), (415, 196)]]
# last_R = [[(350, 385), (355, 366), (356, 360), (357, 357), (360, 338), (360, 331), (361, 325), (361, 323), (361, 321), (361, 318), (361, 314), (362, 285), (363, 271), (363, 266), (364, 234), (365, 228), (367, 213), (369, 202), (371, 193), (372, 187)], [(353, 380), (354, 379), (356, 371), (358, 362), (358, 360), (359, 357), (364, 320), (364, 319), (364, 316), (364, 310), (365, 268), (366, 264), (366, 244), (368, 226), (368, 221), (370, 209), (371, 203), (371, 201), (372, 194), (374, 189)], [(349, 383), (353, 377), (360, 362), (361, 359), (363, 354), (366, 337), (368, 319), (368, 313), (368, 305), (367, 270), (367, 265), (367, 262), (366, 254), (366, 251), (367, 242), (367, 235), (371, 212), (375, 200), (377, 195), (381, 187)], [(358, 378), (360, 372), (362, 367), (364, 359), (365, 352), (366, 349), (369, 325), (370, 320), (370, 311), (371, 303), (372, 284), (372, 277), (372, 266), (373, 262), (374, 241), (377, 209), (379, 199), (379, 196), (380, 194), (381, 188)]]
#
#
# last_L = np.asarray(last_L).T
#
# resultL = list()
# for k in range(20):
#     lastLx = timeMedBlur(last_L[0][k])
#     lastLy = timeMedBlur(last_L[1][k])
#     lastL = np.vstack([lastLx, lastLy]).T
#     resultL.append(lastL.tolist())
# resultL = np.asarray(last_L).T
# print(resultL)

# fm_count = len(last_L)
# rows, cols = (fm_count, 2)

# result_L = [[[0] * cols] * 20] * rows
# result_R = [[[0] * cols] * 20] * rows
#
# for i in range(0, 20, 1):
#     tmp_L = []
#     tmp_R = []
#     for k in range(0, fm_count - 1, 1):
#         tmp_L.append((int(last_L[k][i][0]), int(last_L[k][i][1])))
#         tmp_R.append((int(last_R[k][i][0]), int(last_R[k][i][1])))
#
#     pt_l = Md.Median_pt(tmp_L)
#     tmp_L_med = pt_l.calculate()
#
#     pt_r = Md.Median_pt(tmp_R)
#     tmp_R_med = pt_r.calculate()

    # print(tmp_L_med)
    # print(tmp_R_med)
    # for q in range(0, fm_count - 1, 1):
        # print(q,i)
        # print(tmp_L_med[q],tmp_R_med[q])

        # result_L[q][i][0] = tmp_L_med[q][0]
        # result_L[q][i][1] = tmp_L_med[q][1]
        # result_R[q][i][0] = tmp_R_med[q][0]
        # result_R[q][i][1] = tmp_R_med[q][1]
        # print(result_L)
        # print(result_R)
# print("result_L:", result_L[0])
# print(last_R)
