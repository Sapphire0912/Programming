import cv2
import numpy as np
import time
from my_alg import *


cap = cv2.VideoCapture('./test.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
cnt = 0
print(fps, total_frame)

while True:
    # setting start time
    start_time = time.time()
    # read frame
    ret, frame = cap.read()
    frame_cp = frame.copy()
    cnt += 1

    # handle
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_Gr = colorRange(hsv, 'gray', optrange=None)
    cv2.imshow('mask_Gr', mask_Gr)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # display frame
    cv2.imshow('frame', gray)

    # 30 frame/ 1s
    # 1s - executed time = waiting time
    if cnt % fps == 0:
        cnt = 0
        executed_time = time.time() - start_time
        print(1 - executed_time)
        time.sleep(1.0 - executed_time)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
