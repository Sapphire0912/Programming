from VideoInitialization import *
from Multi_Threshold import *
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time


def write_video(frames_list, output_path):
    y, x, _ = frames_list[0].shape
    video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), 30, (x, y))
    for i in frames_list:
        video_writer.write(i)
    video_writer.release()


InputPath = 'E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\Segmentation\\A4C Test Video\\'
# InputPath = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\All Classification_avi" \
#            "\\0002_Apical Four Chamber\\"
VideoPath = AllFiles(InputPath, 'avi')
OutputDir = 'E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\Segmentation\\Multi Test Video\\'

for path in VideoPath[0:1]:
    init = VideoInit(path)
    FileName = path.split('\\')[-1]
    print(f'FileName: {FileName}')

    OutputPath = OutputDir + 'self' + FileName

    curr_time = time.time()
    frame_list = list()
    while True:
        frame_time = time.time()
        ret, frame = init.video.read()

        if not ret:
            break

        frame[init.roi != 255] = [0, 0, 0]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 測試 Multi_Threshold 模組
        multi = MultiThres(gray, init.roi, 40, 255)
        # print(f'L range, M range, H range: {multi.L_range, multi.M_range, multi.H_range}')
        multi.SearchMax()
        result = multi.threshold()
        # cv2.imshow('res', result)
        # cv2.waitKey(1000)

        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        frame_list.append(result)
        frame_time_end = time.time()
        # print(f'處理完當前 frame 時間: {round(frame_time_end - frame_time, 2)} 秒')

    curr_time_end = time.time()
    # print(f'當前影片處理時間: {round(curr_time_end - curr_time, 2)} 秒')
    # print(f'當前影片幀數: {int(init.video.get(cv2.CAP_PROP_FRAME_COUNT))} ')
    # print(f'平均一幀時間: {round((curr_time_end - curr_time) / init.video.get(cv2.CAP_PROP_FRAME_COUNT), 2)} 秒')
    write_video(frame_list, OutputPath)

