import os
import numpy as np
import cv2


def AllFiles(DirPath, extension_name='avi'):
    result = list()
    for root, dirs, files in os.walk(DirPath):
        for f in files:
            if f[-len(extension_name):] == extension_name:
                result.append(os.path.join(root, f))
    return result


def write_video(FrameList, OutputPath, fps=20):
    if len(FrameList[0].shape) == 2:
        raise IOError('輸出影片要為 3 通道影像 (FileIO.py)')

    outputY, outputX, _ = FrameList[0].shape
    video_writer = cv2.VideoWriter(OutputPath, cv2.VideoWriter_fourcc(*'MJPG'), fps, (outputX, outputY))
    for i in FrameList:
        video_writer.write(i)
    video_writer.release()


# def merge_video(FrameLists, GridArray, OutputPath, fps=20):
#     """curr: f1, f2, hstack"""
#     pass

def merge_video(F1, F2, OutputPath):
    F1Y, F1X, _ = F1[0].shape
    F2Y, F2X, _ = F2[0].shape

    video_writer = cv2.VideoWriter(OutputPath, cv2.VideoWriter_fourcc(*'MJPG'), 20, (F1X + F2X, F1Y))
    for i in range(len(F1)):
        merge = np.hstack([F1[i], F2[i]])
        video_writer.write(merge)
    video_writer.release()
