from find_roi import FindROI
from find_unit import handle_unit
from read_file import Allfiles
from heart_bound import HeartROI
from Rising_pt import Rising_pt

import matplotlib.pyplot as plt
import numpy as np
import cv2


def write_video(frames_list, output_path):
    y, x, _ = frames_list[0].shape
    video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), 20, (x, y))
    for i in frames_list:
        video_writer.write(i)
    video_writer.release()


video_path = Allfiles('E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\All Classification_avi\\0009_Parasternal Long Axis\\', 'avi')
output_dir = 'E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\match_model\\match_all(muscle)\\alpha_video\\'

for path in video_path:
    # ----- Pre. 處理基本資訊
    file_name = path.split('\\')[-1]
    # --- ROI
    video = FindROI(path)
    video.roi_region(path)
    mask_roi = video.roi
    ox, oy = video.ox, video.oy
    # ---  ROI End.

    # --- Unit
    unit = handle_unit(path)
    # --- Unit End.
    # ----- Pre. 處理基本資訊 End.

    # 1. 找到每幀腔室的中心點
    frame_list = list()
    while video.ret:
        frame = video.get_frame()

        if not video.ret:
            break

        frame[mask_roi != 255] = [0, 0, 0]

        # 中值濾波
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        med_blur = cv2.medianBlur(gray, 9)

        # heart range
        handle_heart = HeartROI(mask_roi, (180, 240))  # init parameters
        handle_heart.adapt_thres(med_blur)  # adaptive threshold, distance transform
        handle_heart.heart_bound()  # find bound
        handle_heart.hist(med_blur)  # calculate histogram

        # find chamber center
        # mask_chamber = handle_heart.ori_dtC.copy()
        # mask_chamber[mask_chamber != 0] = 255
        # mask_fg = np.zeros(mask_roi.shape, np.uint8)

        DT_Chamber = handle_heart.ori_dtC.copy()
        DT_Chamber[handle_heart.mask_M != 255] = 0
        DT_Chamber[DT_Chamber >= 0.45 * np.max(DT_Chamber)] = 255
        DT_Chamber[DT_Chamber < 0.45 * np.max(DT_Chamber)] = 0

        cnt_DTC, _ = cv2.findContours(DT_Chamber, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        DTC_center = list()
        for index in range(len(cnt_DTC)):
            area = cv2.contourArea(cnt_DTC[index])
            if area > 150:
                M = cv2.moments(cnt_DTC[index])
                # cv2.drawContours(mask_fg, [cnt_DTC[index]], -1, (255, 255, 255), -1)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                DTC_center.append((cx, cy))

        # unknown = cv2.subtract(mask_chamber, mask_fg)
        # _, marker = cv2.connectedComponents(mask_fg)
        # marker = marker + 1
        # marker[unknown == 255] = 0
        # markers = cv2.watershed(frame, marker)
        # print(np.unique(markers))

        # uni, count = np.unique(markers, return_counts=True)
        # for index in range(len(uni)):
        #     if uni[index] == -1:
        #         frame[marker == uni[index]] = [0, 0, 255]
        #
        #     if uni[index] != -1 and count[index] < 30000:
        #         b = np.random.randint(50, 255)
        #         g = np.random.randint(50, 255)
        #         r = np.random.randint(50, 255)
        #
        #         frame[marker == uni[index]] = [b, g, r]

        # for center in DTC_center:
        #     cv2.circle(frame, center, 2, (0, 255, 0), 2)

        # cv2.drawContours(frame, [handle_heart.cnt_M], 0, (255, 0, 0), 2)
        # cv2.imshow('dtC', handle_heart.ori_dtC)
        # cv2.imshow('dtM', handle_heart.ori_dtM)
        cv2.imshow('frame', frame)
        # cv2.imshow('mask_chamber', mask_chamber)
        # cv2.imshow('fg', mask_fg)
        # cv2.imshow('unknown', unknown)
        cv2.waitKey(10)

        # frame_list.append(frame)
    # print(file_name)
    # write_video(frame_list, output_path=output_dir + file_name)
