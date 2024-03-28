from VideoInitialization import *
from multi_thres import *
import cv2
import numpy as np
import time

InputPath = 'E:/MyProgramming/Python/Project/implement/heart recognize/All Classification_avi/0002_Apical Four Chamber/'
VideoPath = AllFiles(InputPath, 'avi')


def write_video(frames_list, output_path):
    y, x, _ = frames_list[0].shape
    video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), 30, (x, y))
    for i in frames_list:
        video_writer.write(i)
    video_writer.release()


for path in VideoPath[0:1]:
    curr_total_st = time.time()

    init = VideoInit(path)
    total_frame = int(init.video.get(cv2.CAP_PROP_FRAME_COUNT))

    FileName = path.split('/')[-1]
    # print(f'File Name: {FileName}')
    frame_list = list()
    OutputPath = 'E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\Segmentation\\Multi Test Video\\'
    OutputPath = OutputPath + FileName
    print(OutputPath)

    while True:
        ret, frame = init.video.read()

        if not ret:
            break

        hist_time = time.time()
        frame[init.roi != 255] = [0, 0, 0]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # med_blur = cv2.medianBlur(gray, 9)

        hst = np.zeros(256)
        for x in range(0, 800):
            for y in range(0, 600):
                # if 30 < med_blur[y, x] < 255:
                hst[int(gray[y, x])] += 1
        end_hist_time = time.time()
        # print(f'計算 histogram 時間: {round(end_hist_time - hist_time, 2)} 秒')

        multi_time_st = time.time()
        multi = MultiThres(hst, 9, 25, 255)

        search_time_st = time.time()
        L, M, H, ZL, LM, MH, HX = multi.search_max()
        print(f'L, M, H: {L, M, H}')
        print(f'ZL, LM, MH, HX: {ZL, LM, MH, HX}')

        end_search_time = time.time()
        # print(f'計算 L, M, H 時間: {round(end_search_time - search_time_st, 2)} 秒')

        thres_time_st = time.time()
        # result = multi.threshold(med_blur, L, LM, M, MH, H)
        end_thres_time = time.time()
        # print(f'計算 Multi-threshold 時間: {round(end_thres_time - thres_time_st, 4)} 秒')

        end_multi_time = time.time()
        # print(f'處理 Multi-threshold 時間: {round(end_multi_time - multi_time_st, 2)} 秒')
        # result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

        # print(f'debug: {np.unique(result, return_counts=True)}')
        # print(f'hist: {hst}')
        # print(f'L: {L}, M: {M}, H: {H}')
        # print(f'ZL: {ZL}, LM: {LM}, MH: {MH}, HX: {HX}')

        # cv2.imshow('mb', med_blur)
        # cv2.imshow('result', result)
        # frame_list.append(result)
        # print('finished frame count: ', len(frame_list), '\n')
        # cv2.waitKey(1)

    curr_total_end = time.time()
    print(f'當前影片處理時間: {round(curr_total_end - curr_total_st, 2)} 秒')
    print(f'當前影片總幀數: {int(total_frame)}')
    print(f'平均一幀時間: {round(round(curr_total_end - curr_total_st, 2) / int(total_frame), 2)} 秒')
    # write_video(frame_list, OutputPath)
