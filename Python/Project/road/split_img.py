import numpy as np
import cv2


def video_to_img(path):
    video = cv2.VideoCapture(path)
    cnt = 0

    while True:
        ret, frame = video.read()
        cnt += 1
        if not ret:
            break

        print("正在處理第 %d 幀...", cnt)
        y, x, _ = frame.shape
        size = (640, 480) if x > y else (480, 640)
        frame = cv2.resize(frame, size, cv2.INTER_AREA)

        cv2.imwrite('./img/MOV00271_Trim%d.png' % cnt, frame)


if __name__ == '__main__':
    file = './video/MOV00271_Trim.mp4'
    video_to_img(file)
