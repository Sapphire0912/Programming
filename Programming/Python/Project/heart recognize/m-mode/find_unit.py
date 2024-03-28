import cv2
import numpy as np
import time


def handle_unit(path):
    video = cv2.VideoCapture(path)
    _, first = video.read()

    m = first[75:93, 19:29]
    m = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY)
    m = cv2.resize(m, (40, 72), cv2.INTER_CUBIC)
    m[m > 128] = 255
    m[m <= 128] = 0

    cnt, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rect = cv2.boundingRect(cnt[0])

    x1, y1, width, height = rect

    # 分成 6 等分
    h = height // 3
    w = width // 2

    cx, ucy, dcy = x1 + w, y1 + h, y1 + height - h

    ul_score = np.unique(m[y1:ucy, x1:cx], return_counts=True)[1][1]
    cl_score = np.unique(m[ucy:dcy, x1:cx], return_counts=True)[1][1]
    dl_score = np.unique(m[dcy:y1+height, x1:cx], return_counts=True)[1][1]

    ur_score = np.unique(m[y1:ucy, cx:x1+width], return_counts=True)[1][1]
    cr_score = np.unique(m[ucy:dcy, cx:x1+width], return_counts=True)[1][1]
    dr_score = np.unique(m[dcy:y1+height, cx:x1+width], return_counts=True)[1][1]

    score_list = [ul_score, ur_score, cl_score, cr_score, dl_score, dr_score]

    # 對應的 key-value
    d = {
        (2, 3): 3,
        (2, 5): 3,
        (1, 0): 5,
        (1, 2): 6,
        (5, 1): 7,
        (2, 4): 2,
        (0, 5): 4
    }

    max_index = score_list.index(max(score_list))
    min_index = score_list.index(min(score_list))
    f = (min_index, max_index)
    # cv2.imshow('digit%d' % i, m)
    return d[f] + 10

