import numpy as np
import cv2
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


def corners_key_point():
    """cv2.goodFeaturesToTrack() 角點追蹤參數:
    img: 灰階圖
    maxCorners: 角點數量最大值, 若檢測角點超過此值, 則傳回前 maxCorners 個強角點
    qualityLevel: 角點的品質因子
    minDistance: 如果周圍 minDistance 範圍存在其他更強角點, 則將此角點刪除
    corners: 儲存所有角點
    mask: 指定 ROI(region of interest), 沒指定則是找全圖
    blockSize: 計算協方差矩陣時的視窗大小
    useHarrisDetector: bool, 是否使用 Harris 角點檢測, 若不指定, 則計算 shi-tomasi 角點
    k: Harris 檢測需要的 k 值
    """


cam = init_camera(0, 800, 600)

# 1. 運動檢測
# 創建橢圓
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
kernel = np.ones((5, 5), np.uint8)
bg = None

# help(corners_key_point)
while True:
    ret, frame = cam.read()
    fps = cam.get(cv2.CAP_PROP_FPS)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_blur = cv2.GaussianBlur(frame_gray, (21, 21), 0)

    # 將第一偵設定為輸入的背景
    if bg is None:
        bg = frame_blur
        continue

    # 背景差分, 接著用二值圖做形態學
    # 1. 背景法: 選一張圖當作背景, 接著讓每偵對比(應用在光照穩定的地方)
    # (缺點: 若光照時常變化很容易造成錯誤)
    diff = cv2.absdiff(bg, frame_blur)
    _, thres = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    dilate = cv2.dilate(thres, es, iterations=2)

    # 2. 差偵法: 後偵和前偵對比
    # (缺點: 無法對運動後突然又靜止的景象識別, 優點: 光照不影響)
    # diff = cv2.absdiff(bg, frame_blur)
    # _, thres = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    # dilate = cv2.dilate(thres, es, iterations=2)
    # bg = frame_blur

    # 2. 運動方向預測
    # 2.1 角點追蹤 goodFeaturesToTrack() <- key points
    # 參數說明都在 corners_key_point 函數裡面
    try:
        corners = cv2.goodFeaturesToTrack(
            diff,
            maxCorners=40,
            qualityLevel=0.3,
            minDistance=10,
            blockSize=10,
            useHarrisDetector=True
        )
        # corners = np.int0(corners)
        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)
    except TypeError:
        print("current not moving.")
        continue

    # 顯示矩形, 計算一張圖片目標的輪廓
    contours, hierarchy = cv2.findContours(dilate.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 使用 convex hull
    # try:
    #     for h in contours:
    #         hull = cv2.convexHull(h)
    #         cv2.polylines(frame, [hull], True, (0, 255, 0), 2)
    # except IndexError:
    #     print("not find contours.")
    #     continue

    # 畫輪廓
    max_areas = 0
    max_rect = None
    for c in contours:
        if cv2.contourArea(c) >= max_areas and cv2.contourArea(c) > 20000:
            max_areas = cv2.contourArea(c)
            max_rect = c

    # if cv2.contourArea(c) >= 1500:
    #     (x, y, w, h) = cv2.boundingRect(c)
    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    x, y, w, h = cv2.boundingRect(max_rect)
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(frame, time.ctime(), (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255, 0, 0), 1)
    cv2.putText(frame, "fps: "+str(fps), (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255, 0, 255), 1)
    cv2.putText(frame, "area: "+str(max_areas), (10, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (0, 0, 255), 1)
    cv2.imshow("contours", frame)
    cv2.imshow("different", diff)
    cv2.imshow("dilate", dilate)
    # cv2.imshow("sobel", frame_sobel)

    if cv2.waitKey(1) == ord('q'):
        break


# 2.2 光流法
# 工作原理假設:
# a. 連續兩偵圖像之間, 目標像素亮度不變
# b. 相鄰的像素之間有相似的運動

cam.release()
cv2.destroyAllWindows()
