from find_roi import FindROI
from find_unit import handle_unit

import glob
import numpy as np
import cv2


def read_file(video_dir):
    all_video_path = glob.glob(video_dir + '*.avi')
    return all_video_path


def pos_info(src, x1points, x2points, theta, ):
    height, width, _ = src.shape
    mask_lv_line = np.zeros(src.shape[:2], np.uint8)
    cv2.line(mask_lv_line, x1points, x2points, (255, 255, 255), 1)

    gray_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    M = cv2.getRotationMatrix2D((width / 2, height / 2), theta, 1)
    rotate = cv2.warpAffine(gray_src, M, (width, height))
    line = cv2.warpAffine(mask_lv_line, M, (width, height))
    cnt_line, _ = cv2.findContours(line, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(cnt_line[0])

    info = rotate[y:y + h, x]
    return info


def show_fig(output_path, array):
    array = np.asarray(array).T
    hei, wid = array.shape
    array = cv2.resize(array, (1024, hei), cv2.INTER_CUBIC)

    cv2.imwrite(output_path, array)


video_path = read_file('../data1_classifier/self_classification/0009/test/')

for path in video_path:
    # 找到 ROI 區域
    video = FindROI(path)
    video.roi_region(path)

    # 找到標準單位
    unit = handle_unit(path)

    # M mode 3個方向
    lv_line_x = int(video.ox - video.radius * np.sin(15 * np.pi / 180))
    lv_line_y = int(video.oy + video.radius * np.sin(75 * np.pi / 180))

    la_line_x = int(video.ox + video.radius * np.sin(15 * np.pi / 180))
    la_line_y = int(video.oy + video.radius * np.sin(75 * np.pi / 180))

    av_line_x = int(video.ox + video.radius * np.sin(30 * np.pi / 180))
    av_line_y = int(video.oy + video.radius * np.sin(60 * np.pi / 180))

    curr_lv = list()
    curr_la = list()
    curr_av = list()

    demo_scale = int(1024 / video.video.get(cv2.CAP_PROP_FRAME_COUNT))

    while video.ret:
        frame = video.get_frame()

        if not video.ret:
            break

        lv_info = pos_info(frame, (video.ox, video.oy), (lv_line_x, lv_line_y), 15)
        la_info = pos_info(frame, (video.ox, video.oy), (la_line_x, la_line_y), -15)
        av_info = pos_info(frame, (video.ox, video.oy), (av_line_x, av_line_y), -30)

        # 剩下展示部分
        for _ in range(demo_scale):
            curr_lv.append(lv_info)
            curr_la.append(la_info)
            curr_av.append(av_info)

        # cv2.circle(frame, (video.ox, video.oy), 5, (255, 255, 0), -1)
        # cv2.line(frame, (video.ox, video.oy), (video.ox, video.oy+video.radius), (0, 255, 255), 2)  # 0
        # cv2.line(frame, (video.ox, video.oy), (lv_line_x, lv_line_y), (255, 0, 0), 2)  # 15
        # cv2.line(frame, (video.ox, video.oy), (la_line_x, la_line_y), (0, 255, 0), 2)  # -15
        # cv2.line(frame, (video.ox, video.oy), (av_line_x, av_line_y), (0, 0, 255), 2)  # -30
        # MM = cv2.getRotationMatrix2D((400, 300), -30, 1)
        # r = cv2.warpAffine(frame, MM, (800, 600))
        # cv2.imshow('f', frame)
        # cv2.waitKey(10000)

    lv_filename = path.split('\\')[-1].replace('.avi', '_lv M mode.png')
    la_filename = path.split('\\')[-1].replace('.avi', '_la M mode.png')
    av_filename = path.split('\\')[-1].replace('.avi', '_av M mode.png')

    show_fig(lv_filename, curr_lv)
    show_fig(la_filename, curr_la)
    show_fig(av_filename, curr_av)

