import cv2
import numpy as np
import matplotlib.pyplot as plt

from read_file import Allfiles
from find_roi import FindROI


class HeartROI(object):
    def __init__(self, mask_roi, img_size='default'):
        # init parameter
        self.mask_roi = mask_roi
        if isinstance(img_size, str) and img_size == 'default':
            self.height, self.width = self.mask_roi.shape

        elif isinstance(img_size, tuple):
            self.height, self.width = img_size

        # adaptive threshold init and result parameters
        self.kernel = np.ones((5, 5), np.uint8)
        self.ori_dtC, self.ori_dtM = None, None
        self.adapt_C, self.adapt_M = None, None
        self.dtC = None
        self.dtM = None
        self.cnt_C = None
        self.cnt_M = None

        # heart bound result parameters
        self.mask_C = None
        self.mask_M = None

        # hist result parameters
        self.gray_scale = None
        self.count = None

    def adapt_thres(self, img, maxVal=255, thres_alg=cv2.ADAPTIVE_THRESH_MEAN_C, block_size=131, C=9,
                    dis_alg=cv2.DIST_L1, dis_mask_size=5):

        # chamber
        chamber_thres = cv2.adaptiveThreshold(img, maxVal, thres_alg, cv2.THRESH_BINARY_INV, block_size, C)

        # morphology opening
        opening_C = cv2.morphologyEx(chamber_thres, cv2.MORPH_OPEN, self.kernel)

        # distance transform
        DT_C = cv2.distanceTransform(opening_C, dis_alg, dis_mask_size).astype(np.float32)
        scale = 255 / np.max(DT_C)
        DT_C *= scale
        DT_C = cv2.convertScaleAbs(DT_C)
        DT_C[self.mask_roi != 255] = 0

        # muscle
        muscle_thres = cv2.adaptiveThreshold(img, maxVal, thres_alg, cv2.THRESH_BINARY, block_size, C)

        # morphology opening
        opening_M = cv2.morphologyEx(muscle_thres, cv2.MORPH_OPEN, self.kernel)

        # distance transform
        DT_M = cv2.distanceTransform(opening_M, dis_alg, dis_mask_size).astype(np.float32)
        DT_M = cv2.convertScaleAbs(DT_M)
        DT_M[self.mask_roi != 255] = 0
        scale = 255 / np.max(DT_M)
        DT_M = (DT_M * scale).astype(np.float32)
        DT_M = cv2.convertScaleAbs(DT_M)

        self.adapt_C = chamber_thres
        self.adapt_M = muscle_thres
        self.ori_dtC = DT_C
        self.ori_dtM = DT_M
        self.dtC = cv2.resize(DT_C, (self.width, self.height), cv2.INTER_CUBIC)
        self.dtM = cv2.resize(DT_M, (self.width, self.height), cv2.INTER_CUBIC)

    def heart_bound(self):
        mask_C = np.zeros((self.height, self.width), np.uint8)
        mask_M = np.zeros((self.height, self.width), np.uint8)

        # chamber mask
        pts_C = list()
        for h in range(self.height):
            cx, cy = 0, 0
            max_dis = 0
            for w in range(self.width):
                d = self.dtC[h, w]

                if d > max_dis:
                    max_dis = d
                    cx, cy = w, h

            if cx != 0 and cy != 0:
                pts_C.append([cx, cy])

        for w in range(self.width):
            cx, cy = 0, 0
            max_dis = 0
            for h in range(self.height):
                d = self.dtC[h, w]

                if d > max_dis:
                    max_dis = d
                    cx, cy = w, h

            if cx != 0 and cy != 0:
                pts_C.append([cx, cy])

        pts_C = np.asarray(pts_C)
        pts_C_hull = cv2.convexHull(pts_C)
        cv2.drawContours(mask_C, [pts_C_hull], 0, (255, 255, 255), -1)
        cnt_C, _ = cv2.findContours(mask_C, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # muscle
        pts_M = list()
        for h in range(self.height):
            cx, cy = 0, 0
            max_dis = 0
            for w in range(self.width):
                d = self.dtM[h, w]
                if d > max_dis:
                    cx, cy = w, h
                    is_region = cv2.pointPolygonTest(cnt_C[0], (cx, cy), False)

                    if is_region != -1:
                        max_dis = d
                    else:
                        continue

            if cx != 0 and cy != 0:
                is_region = cv2.pointPolygonTest(cnt_C[0], (cx, cy), False)
                if is_region != -1:
                    pts_M.append([cx, cy])

        for w in range(self.width):
            cx, cy = 0, 0
            max_dis = 0
            for h in range(self.height):
                d = self.dtM[h, w]
                if d > max_dis:
                    cx, cy = w, h
                    is_region = cv2.pointPolygonTest(cnt_C[0], (cx, cy), False)

                    if is_region != -1:
                        max_dis = d
                    else:
                        continue

            if cx != 0 and cy != 0:
                is_region = cv2.pointPolygonTest(cnt_C[0], (cx, cy), False)
                if is_region != -1:
                    pts_M.append([cx, cy])

        pts_M = np.asarray(pts_M)
        pts_M_hull = cv2.convexHull(pts_M)
        cv2.drawContours(mask_M, [pts_M_hull], 0, (255, 255, 255), -1)
        cnt_M, _ = cv2.findContours(mask_M, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        self.mask_C = mask_C
        self.mask_M = mask_M

    def hist(self, frame):
        if len(frame.shape) > 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ori_y, ori_x = frame.shape
        self.mask_M = cv2.resize(self.mask_M, (ori_x, ori_y), cv2.INTER_LINEAR)
        self.mask_C = cv2.resize(self.mask_C, (ori_x, ori_y), cv2.INTER_LINEAR)
        cnt_C, _ = cv2.findContours(self.mask_C, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt_M, _ = cv2.findContours(self.mask_M, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cnt_C = cv2.convexHull(np.asarray(cnt_C[0]))
        self.cnt_M = cv2.convexHull(np.asarray(cnt_M[0]))
        self.mask_M = cv2.drawContours(self.mask_M, [self.cnt_M], 0, (255, 255, 255), -1)
        self.mask_C = cv2.drawContours(self.mask_C, [self.cnt_C], 0, (255, 255, 255), -1)

        frame[self.mask_M != 255] = 0
        mask_zero_area = np.unique(self.mask_M, return_counts=True)[1][0]

        valve, count = np.unique(frame, return_counts=True)
        count[0] -= mask_zero_area

        self.gray_scale = valve
        self.count = count

    def draw_hist(self, display=False):
        if display:
            plt.title('curr frame histogram')
            plt.xlabel('x scale')
            plt.ylabel('count')
            plt.scatter(self.gray_scale, self.count, color='red')
            plt.plot(self.gray_scale, self.count, color='blue')
            plt.show()


# return all avi files in the specified dir.
# video_path = Allfiles('E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\All Classification_avi\\0009_Parasternal Long Axis\\', 'avi')
# output_dir = 'E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\match_model\\match_all(muscle)\\alpha_video\\'
#
# for path in video_path:
#     file_name = path.split('\\')[-1]
#
#     # 1. find roi
#     video = FindROI(path)
#     video.roi_region(path)
#     mask_roi = video.roi
#     # 1. find roi end.
#
#     # 2. open video
#     while video.ret:
#         # get frame
#         frame = video.get_frame()
#
#         if not video.ret:
#             break
#
#         # gray & median blur
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         med_blur = cv2.medianBlur(gray, 9)
#
#         # heart range
#         handle_heart = HeartROI(mask_roi, (150, 200))  # init parameters
#         handle_heart.adapt_thres(med_blur)  # adaptive threshold
#         handle_heart.heart_bound()  # distance transform
#         handle_heart.hist(med_blur)  # calculate histogram
#         handle_heart.draw_hist()  # display a histogram with a graph
#
#         cv2.drawContours(frame, [handle_heart.cnt_M], 0, (255, 0, 0), 2)
#         cv2.imshow('dtM', handle_heart.dtM)
#         cv2.imshow('dtC', handle_heart.dtC)
#         cv2.imshow('frame', frame)
#
#         handle_heart.draw_hist()
#
#         cv2.waitKey(10)
