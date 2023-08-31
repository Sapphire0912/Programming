import cv2
import numpy as np
from scipy import signal

__all__ = ['colorRange', 'sobel', 'adjust_threshold',
           'adjust_canny', 'adjust_HoughLineSP', 'lbp',
           'compare']


def nothing(no):
    pass


def colorRange(img, target, optrange=None):
    color_dict = {
        "black": (np.array([0, 0, 0]), np.array([120, 255, 46])),
        "gray": (np.array([0, 0, 46]), np.array([180, 43, 220])),
        "white": (np.array([0, 0, 221]), np.array([180, 30, 255])),
        "red_1": (np.array([0, 43, 46]), np.array([10, 255, 255])),
        "red_2": (np.array([156, 43, 46]), np.array([180, 255, 255])),
        "orange": (np.array([11, 43, 46]), np.array([25, 255, 255])),
        "yellow": (np.array([26, 43, 46]), np.array([34, 255, 255])),
        "green": (np.array([35, 43, 46]), np.array([77, 255, 255])),
        "cyan_blue": (np.array([78, 43, 46]), np.array([99, 255, 255])),
        "blue": (np.array([100, 43, 46]), np.array([124, 255, 255])),
        "purple": (np.array([125, 43, 46]), np.array([155, 255, 255]))
    }

    if target in color_dict.keys():
        if isinstance(optrange, tuple) and optrange is not None:
            return cv2.inRange(img, optrange[0], optrange[1])
        elif optrange is None:
            minT, maxT = color_dict[target]
            return cv2.inRange(img, minT, maxT)
        else:
            raise TypeError("optrange 參數值錯誤: 傳入一個元組(min, max)")
    else:
        s = "target 參數內容 black, gray, white, red_1, red_2, orange, yellow, green, cyan_blue, blue, purple"
        raise TypeError(s)


def sobel(img, dx=0, dy=0, method="sqrt"):
    kx = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    ky = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])

    iy, ix = img.shape
    reg = np.zeros((iy + 2, ix + 2), np.int32)
    reg[1:iy + 1, 1:ix + 1] = img

    gx = np.zeros(img.shape, np.int32)
    gy = np.zeros(img.shape, np.int32)

    while dx > 0:
        gx = signal.convolve(reg, kx, mode='valid')
        dx -= 1
        if dx != 0:
            reg[1:iy + 1, 1:ix + 1] = gx

    while dy > 0:
        gy = signal.convolve(reg, ky, mode='valid')
        dy -= 1
        if dy != 0:
            reg[1:iy + 1, 1:ix + 1] = gy

    if method == "sqrt":
        return np.sqrt(gx * gx + gy * gy).astype(np.uint8)
    elif method == "abs":
        return (np.abs(gx) + np.abs(gy)).astype(np.uint8)
    else:
        raise TypeError("Parameter method is only sqrt and abs.")


def adjust_threshold(img, name, param1, param2, param1_lim=(0, 255), param2_lim=(0, 255), method=None):
    """
    img: gray image, ndarray
    name: windows name, str
    param1: threshold1 parameter name, str
    param2: threshold2 parameter name, str
    param1_lim: parameter1 min and max value, tuple(min, max)
    param2_lim: parameter2 min and max value, tuple(min, max)
    method: handle method, cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, cv2.THRESH_OTSU, cv2.THRESH_TOZERO, etc.
    """
    wins = name
    name1 = param1
    name2 = param2
    min1, max1 = param1_lim
    min2, max2 = param2_lim
    val1 = 0
    val2 = 0
    cv2.namedWindow(wins, cv2.WINDOW_NORMAL)
    cv2.createTrackbar(name1, wins, min1, max1, nothing)
    cv2.createTrackbar(name2, wins, min2, max2, nothing)

    while cv2.waitKey(1) != ord('q'):
        thres1 = cv2.getTrackbarPos(name1, wins)
        thres2 = cv2.getTrackbarPos(name2, wins)
        _, thres = cv2.threshold(img, thres1, thres2, method)
        val1 = thres1
        val2 = thres2
        cv2.imshow(wins, thres)
    cv2.destroyWindow(wins)
    return val1, val2, method


def adjust_canny(img, name, param1, param2, param1_lim=(0, 255), param2_lim=(0, 255)):
    wins = name
    name1 = param1
    name2 = param2
    min1, max1 = param1_lim
    min2, max2 = param2_lim
    val1 = 0
    val2 = 0
    cv2.namedWindow(wins, cv2.WINDOW_NORMAL)
    cv2.createTrackbar(name1, wins, min1, max1, nothing)
    cv2.createTrackbar(name2, wins, min2, max2, nothing)

    while cv2.waitKey(1) != ord('q'):
        thres1 = cv2.getTrackbarPos(name1, wins)
        thres2 = cv2.getTrackbarPos(name2, wins)
        canny = cv2.Canny(img, thres1, thres2)
        val1 = thres1
        val2 = thres2
        cv2.imshow(wins, canny)
    cv2.destroyWindow(wins)
    return val1, val2


def adjust_HoughLineSP(ori, img, name, rho, theta, line_thres, minLineLength, maxLineGap):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.createTrackbar("line_thres", name, line_thres[0], line_thres[1], nothing)
    cv2.createTrackbar("min_line", name, minLineLength[0], minLineLength[1], nothing)
    cv2.createTrackbar("max_gap", name, maxLineGap[0], maxLineGap[1], nothing)

    while True:
        line_thres = cv2.getTrackbarPos("line_thres", name)
        min_line = cv2.getTrackbarPos("min_line", name)
        max_gap = cv2.getTrackbarPos("max_gap", name)

        linesP = cv2.HoughLinesP(
            image=img,
            rho=rho,
            theta=theta,
            threshold=line_thres,
            minLineLength=min_line,
            maxLineGap=max_gap
        )

        try:
            ori_cp = ori.copy()
            for line in linesP:
                for x1, y1, x2, y2 in line:
                    cv2.line(ori_cp, (x1, y1), (x2, y2), (255, 0, 0), 3)

            cv2.imshow(name, ori_cp)
            cv2.imshow("handle img", img)
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyWindow(name)
                return linesP

        except TypeError:
            cv2.setTrackbarPos("line_thres", name, 0)
            cv2.setTrackbarPos("min_line", name, 0)
            cv2.setTrackbarPos("max_gap", name, 1)
            continue


def compare(img, sample, high=32, width=8, condi=0.5):
    # 儲存指定區塊的sample
    y, x = sample
    s = img[y:y + high, x:x + width]

    # 使用 calcHist() 取得直方圖數據
    s_hist = cv2.calcHist([s], [0], None, [256], [0, 255])

    # 和圖片的每個 high*width 做比較(採用 相關性比較)
    # 將相似度符合的條件畫成同個 color

    # 存放 color 資訊的 陣列
    color = np.zeros(img.shape, dtype=np.uint8)
    # 0 為不塗色, 255 為塗色

    img_y, img_x = img.shape
    for j in range(0, img_y // high):
        for i in range(0, img_x // width):
            y1 = j * high
            y2 = y1 + high
            x1 = i * width
            x2 = x1 + width
            c_hist = cv2.calcHist([img[y1:y2, x1:x2]], [0], None, [256], [0, 255])
            sim = cv2.compareHist(s_hist, c_hist, cv2.HISTCMP_CORREL)

            if sim >= condi:
                color[y1:y2, x1:x2] = 255
    return color


def bit_to_int(matrix):
    # 傳入 3x3  將二進制值轉成十進制, 傳回十進制值
    pos = np.array([[3, 4, 5], [2, 0, 6], [1, 0, 7]])
    weight = np.power(2, pos)
    lbp_value = np.sum(weight * matrix) - 1
    return lbp_value


def lbp(img):
    # 邊緣填充 0
    y, x = img.shape
    con_img = np.zeros((y + 2, x + 2), dtype=np.uint16)
    con_img[1:y + 1, 1:x + 1] = img

    # 儲存 lbp image
    lbp_img = np.zeros(img.shape, dtype=np.uint8)

    # 取值
    for j in range(0, y):
        for i in range(0, x):
            # 取 3x3 區塊
            target = con_img[j:j + 3, i:i + 3]
            bits = np.where(target >= target[1, 1], 1, 0)
            lbp_img[j, i] = bit_to_int(bits)
    return lbp_img
