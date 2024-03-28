import cv2
import numpy as np
import time


def init_camera(cap=0, width=640, high=480):
    camera = cv2.VideoCapture(cap)

    # 判斷影片是否打開
    if camera.isOpened():
        print("WebCamera was opened.")
    else:
        print("WebCamera was closed.")
        raise IOError("Camera is not open.")

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, high)
    return camera


cam = init_camera(0, 800, 600)

# read first image
_, first = cam.read()
blur = cv2.GaussianBlur(first, (21, 21), 0)
old_gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

# corners tracker
p0 = cv2.goodFeaturesToTrack(
    old_gray,
    maxCorners=40,
    qualityLevel=0.1,
    minDistance=0,
    useHarrisDetector=True
)

mask = np.zeros_like(first)
# random colorbar
color = np.random.randint(0, 255, (100, 3))

while True:
    _, frame = cam.read()
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    frame_gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    # optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, winSize=(15, 15), maxLevel=2)

    # 讀取運動角點, st == 1 表示偵測到運動物體, 即 v, u 表示為 0
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    # 繪製軌跡
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
        frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)

    # mask 和 frame 合併
    img = cv2.add(mask, frame)
    # mask = np.zeros_like(frame)
    cv2.imshow('frame', img)

    # 更新前一偵圖片和角點位置
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        cam.release()
        break
