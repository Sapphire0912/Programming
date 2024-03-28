import os
import glob
import numpy as np
import cv2


class VideoInit(object):
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)
        self.ret = True
        self.roi = None

        if not self.video:
            raise Exception('影片檔案路徑不存在或格式錯誤')

        else:
            self.y, self.x, self.channel = self.video.read()[1].shape

    def get_frame(self):
        self.ret, curr_frame = self.video.read()
        return curr_frame

    def release_video(self):
        self.video.release()
        return True

    def roi_region(self, input_path, mask_threshold=10, kernel_size=(3, 3), morph_iter=3):
        handle_video = cv2.VideoCapture(input_path)
        _, first = handle_video.read()
        mask_diff_all = np.zeros(first.shape[:2], np.uint8)

        while True:
            _ret, f = handle_video.read()

            if not _ret:
                break

            gray_first = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(gray_frame, gray_first)

            mask_diff = np.zeros(diff.shape, np.uint8)
            mask_diff[diff > mask_threshold] = 255
            mask_diff_all += mask_diff
            np.clip(mask_diff_all, 0, 255, out=mask_diff_all)

        mask_last = np.zeros(first.shape[:2], np.uint8)
        contours, hier = cv2.findContours(mask_diff_all, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(mask_last, contours, -1, (255, 255, 255), -1)

        kernel = np.ones(kernel_size, np.uint8)
        mask_erode = cv2.erode(mask_last, kernel, iterations=morph_iter)
        mask_dilate = cv2.dilate(mask_erode, kernel, iterations=morph_iter - 1)

        mask_last_bound = np.zeros(first.shape[:2], np.uint8)
        contours, hier = cv2.findContours(mask_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(mask_last_bound, contours, -1, (255, 255, 255), 2)

        # 已知扇形角度為 90, 直線斜率為 1, -1
        # 霍夫轉換找出直線後, 找交點求圓心
        roi_pos = np.zeros(mask_dilate.shape, np.uint8)

        lines = cv2.HoughLinesP(mask_last_bound, 1, np.pi / 180, threshold=200, minLineLength=60, maxLineGap=130)
        x1_y1 = list()
        x2_y2 = list()
        lm_error, rm_error = 1, 1
        l_index = None
        r_index = None

        try:
            # 找出線的斜率後判斷為左邊或右邊
            for line_index in range(len(lines)):
                x1, y1, x2, y2 = lines[line_index][0]
                m = (y2 - y1) / ((x2 - x1) + 1e-08)

                if m < 0:
                    if abs(m + 1) < lm_error:
                        lm_error = abs(m + 1)
                        l_index = line_index
                else:
                    if abs(m - 1) < rm_error:
                        rm_error = abs(m - 1)
                        r_index = line_index

                x1_y1.append((x1, y1))
                x2_y2.append((x2, y2))

            # 找到最接近斜率 = -1, 1 的線段, 並找出圓心座標
            a1, b1 = x1_y1[l_index]
            a2, b2 = x2_y2[l_index]
            m1 = (b2 - b1) / (a2 - a1)

            A1, B1 = x1_y1[r_index]
            A2, B2 = x2_y2[r_index]
            m2 = (B2 - B1) / (A2 - A1)
            c0, c1 = m1 * a1 - b1, m2 * A1 - B1

            ox = np.round((c0 - c1) / (m1 - m2)).astype(np.int)
            oy = np.round(((m1 + m2) * ox - c0 - c1) / 2).astype(np.int)

            rad = 0
            for ii in range(len(contours)):
                for jj in range(len(contours[ii])):
                    if rad < contours[ii][jj][0][1]:
                        rad = contours[ii][jj][0][1]
            rad = rad - oy
            cv2.ellipse(roi_pos, (ox, oy), (rad, rad), 90, -45, 45, (255, 255, 255), -1)
            self.roi = roi_pos

        except TypeError:
            # 假如找不到直線就以最低點當成圓心, 畫出 90 度的扇形, 半徑為 y 軸的最高減圓心
            rad = 0
            ox, oy = 0, 600

            for i in range(len(contours)):
                for j in range(len(contours[i])):
                    if rad < contours[i][j][0][1]:
                        rad = contours[i][j][0][1]

                    if oy > contours[i][j][0][1]:
                        oy = contours[i][j][0][1]
                        ox = contours[i][j][0][0]
            rad = rad - oy
            cv2.ellipse(roi_pos, (ox, oy), (rad, rad), 90, -45, 45, (255, 255, 255), -1)
            self.roi = roi_pos


def write_video(frames_list, output_path):
    y, x, _ = frames_list[0].shape
    video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), 30, (x, y))
    for i in frames_list:
        video_writer.write(i)
    video_writer.release()


# 嘗試擬合骨架化的模型
video_dir = '.\\1st data class 9\\'
all_video_path = glob.glob(video_dir + '*.avi')

skeletonize_dir = '.\\1st data class 9 skeletonize\\'

for path in all_video_path:
    # 檔案名稱
    file_name = path.split('\\')[-1]

    video = VideoInit(path)
    video.roi_region(path, 10, (3, 3), 3)
    mask_roi = video.roi   # 到時候要修正演算法(抓到其中一條邊和扇形的中心點)
    # cv2.imshow('mask_roi', mask_roi)
    # cv2.waitKey(2000)

    # 讀取骨架圖片
    skeletonize_file_path = skeletonize_dir + file_name + '.png'
    skeletonize_file = cv2.imread(skeletonize_file_path)

    skeletonize_file[mask_roi != 255] = [0, 0, 0]
    gray_skeletonize = cv2.cvtColor(skeletonize_file, cv2.COLOR_BGR2GRAY)

    # ----- 以下四行可以用 ROI 區域取代(ROI 區域演算法要修改準確點, 目前 class9 沒有特別的情況)
    # info_mask = np.zeros((video.y, video.x), np.uint8)
    # info_mask[100:550, 100:700] = 255
    # gray_model = cv2.cvtColor(skeletonize_file, cv2.COLOR_BGR2GRAY)
    # image = cv2.add(gray_model, np.zeros(gray_model.shape, np.uint8), mask=info_mask)
    # -----

    # ----- 找到骨架的邊界
    x_bound = list()
    y_bound = list()

    contour_skeletonize, hierarchy = cv2.findContours(gray_skeletonize, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contour_skeletonize)):
        for j in range(len(contour_skeletonize[i])):
            x_bound.append(contour_skeletonize[i][j][0][0])
            y_bound.append((contour_skeletonize[i][j][0][1]))

    try:
        x = int((max(x_bound) + min(x_bound)) / 2)
        y = int((max(y_bound) + min(y_bound)) / 2)
        rad_x = (max(x_bound) - min(x_bound)) / 2
        rad_y = (max(y_bound) - min(y_bound)) / 2

        radius = int(min(rad_x, rad_y) + abs(rad_x - rad_y) // 2)
        left, right = x - radius, x + radius
        top, bottom = y - radius, y + radius

        gray_skeletonize = gray_skeletonize[top:bottom, left:right]
        mask_roi = mask_roi[top:bottom, left:right]

    except ValueError:
        print('%s 骨架圖片可能是全黑的' % path)
        continue
    # ----- End

    # ----- 調整模型的大小比例
    model_all = cv2.imread('./model_anchor/0009_Parasternal long axis.png')
    model_A = cv2.imread('./model_anchor/0009_Parasternal long axis_1.png')
    model_B = cv2.imread('./model_anchor/0009_Parasternal long axis_2.png')
    model_C = cv2.imread('./model_anchor/0009_Parasternal long axis_3.png')

    model_all_gray = cv2.cvtColor(model_all, cv2.COLOR_BGR2GRAY)
    _, model_all_thres = cv2.threshold(model_all_gray, 180, 255, cv2.THRESH_BINARY)
    contour_model, hierarchy = cv2.findContours(model_all_thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 原始二尖瓣位置(未找到瓣膜前, 暫時寫死)(Mitral Valve)
    mv_pos = np.zeros(model_all.shape, np.uint8)
    mv_top = (677, 378)
    mv_bottom = (640, 477)
    cv2.line(mv_pos, mv_top, mv_bottom, (255, 255, 255), 20)

    # 動脈瓣膜位置(Aortic Value)
    av_pos = np.zeros(model_all.shape, np.uint8)
    av_top = (703, 339)
    av_bottom = (726, 391)
    cv2.line(av_pos, av_top, av_bottom, (255, 255, 255), 20)
    # cv2.imshow('mv_pos', mv_pos)
    # cv2.imshow('av_pos', av_pos)

    # 找出模型的最小擬合圓形後, 裁減原始圖像
    # 最小封閉圓形
    (x, y), radius_model = cv2.minEnclosingCircle(contour_model[0])
    x, y, radius_model = int(x), int(y), int(radius_model)  # 圓形中心點和半徑

    m_left, m_right = x - radius_model, x + radius_model
    m_top, m_bottom = y - radius_model, y + radius_model

    # 裁減原始圖像
    model_all = model_all[m_top:m_bottom, m_left:m_right]
    model_A = model_A[m_top:m_bottom, m_left:m_right]
    model_B = model_B[m_top:m_bottom, m_left:m_right]
    model_C = model_C[m_top:m_bottom, m_left:m_right]

    mv_pos = mv_pos[m_top:m_bottom, m_left:m_right]
    av_pos = av_pos[m_top:m_bottom, m_left:m_right]

    # 裁減圖像後的 二尖瓣、動脈瓣膜位置(左上角座標)
    mv_top_x, mv_top_y = mv_top[0] - m_left, mv_top[1] - m_top
    mv_bottom_x, mv_bottom_y = mv_bottom[0] - m_left, mv_bottom[1] - m_top

    av_top_x, av_top_y = av_top[0] - m_left, av_top[1] - m_top
    av_bottom_x, av_bottom_y = av_bottom[0] - m_left, av_bottom[1] - m_top

    # 調整比例
    scale = radius / radius_model
    top_mv_pos = (int(mv_top_x * scale), int(mv_top_y * scale))
    bottom_mv_pos = (int(mv_bottom_x * scale), int(mv_bottom_y * scale))
    top_av_pos = (int(av_top_x * scale), int(av_top_y * scale))
    bottom_av_pos = (int(av_bottom_x * scale), int(av_bottom_y * scale))

    ori_height, ori_width = model_all.shape[:2]
    width, height = int(ori_width * scale), int(ori_height * scale)

    output_model_all = cv2.resize(model_all, (width, height))
    output_model_A = cv2.resize(model_A, (width, height))
    output_model_B = cv2.resize(model_B, (width, height))
    output_model_C = cv2.resize(model_C, (width, height))

    output_mv_pos = cv2.resize(mv_pos, (width, height))
    output_av_pos = cv2.resize(av_pos, (width, height))
    # ----- End

    # ----- 找到肌肉相對應位置
    # 將原始灰階圖片轉成 BGR 後, 做形態學
    bgr_skeletonize = cv2.cvtColor(gray_skeletonize, cv2.COLOR_GRAY2BGR)

    k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    closing = cv2.morphologyEx(bgr_skeletonize, cv2.MORPH_CLOSE, k, iterations=1)
    dilation = cv2.dilate(closing, k, iterations=4)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, k, iterations=1)

    y, x, color = bgr_skeletonize.shape

    # --- matching A (LV, LA)
    max_fitting_area_A = 0
    best_theta_A = 0
    best_horizontal_A, best_vertical_A = 0, 0
    model_best_A = None
    best_fitting_A = np.zeros(output_model_A.shape, np.uint8)

    for vertical in range(15, 80, 5):
        for horizontal in range(-30, 30, 6):
            trans_mat = np.array([[1, 0, horizontal], [0, 1, vertical]], np.float32)
            affine_A = cv2.warpAffine(output_model_A, trans_mat, (x, y))

            for theta in range(-10, 20, 5):
                rotate_mat = cv2.getRotationMatrix2D((x / 2, y / 2), theta, 1)
                rotate_A = cv2.warpAffine(affine_A, rotate_mat, (x, y))

                fitting_A = cv2.bitwise_and(rotate_A, closing)
                fitting_area = np.sum(fitting_A)

                if fitting_area > max_fitting_area_A:
                    max_fitting_area_A = fitting_area
                    best_theta_A = theta
                    best_vertical_A = vertical
                    best_horizontal_A = horizontal

                    model_best_A = rotate_A
                    best_fitting_A = cv2.bitwise_and(rotate_A, bgr_skeletonize)
    # --- matching A End

    # --- matching C
    # 將 A 區塊消除
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    Area_A = cv2.dilate(best_fitting_A, k, iterations=15)

    match_seg_C = closing.copy()
    match_seg_C[Area_A == 255] = 0

    max_fitting_area_C = 0
    best_theta_C = 0
    best_horizontal_C, best_vertical_C = 0, 0
    model_best_C = None
    best_fitting_C = None

    for vertical in range(-20, 4, 4):
        for horizontal in range(-10, 6, 4):
            trans_mat = np.array([[1, 0, horizontal], [0, 1, vertical]], np.float32)
            affine_C = cv2.warpAffine(output_model_C, trans_mat, (x, y))

            for theta in range(-6, 10, 2):
                rotate_mat = cv2.getRotationMatrix2D((x / 2, y / 2), theta, 1)
                rotate_C = cv2.warpAffine(affine_C, rotate_mat, (x, y))

                fitting_C = cv2.bitwise_and(rotate_C, match_seg_C)
                fitting_area = np.sum(fitting_C)

                if fitting_area > max_fitting_area_C:
                    max_fitting_area_C = fitting_area
                    best_theta_C = theta
                    best_vertical_C = vertical
                    best_horizontal_C = horizontal

                    model_best_C = rotate_C
                    best_fitting_C = cv2.bitwise_and(rotate_C, bgr_skeletonize)

    # 避免該片段模型無法擬合
    if model_best_C is None:
        trans_mat = np.array([[1, 0, best_horizontal_A], [0, 1, best_vertical_A]], np.float32)
        affine_C = cv2.warpAffine(output_model_C, trans_mat, (x, y))

        rotate_mat = cv2.getRotationMatrix2D((x / 2, y / 2), best_theta_A, 1)
        model_best_C = cv2.warpAffine(affine_C, rotate_mat, (x, y))
        best_fitting_C = model_best_C
        best_fitting_C = cv2.erode(best_fitting_C, k, iterations=1)
    # --- matching C End

    # --- matching B
    # 將 A, C 區塊消除
    Area_C = cv2.dilate(best_fitting_C, k, iterations=10)

    match_seg_B = closing.copy()
    match_seg_B[Area_A == 255] = 0
    match_seg_B[Area_C == 255] = 0

    max_fitting_area_B = 0
    best_theta_B = 0
    best_horizontal_B, best_vertical_B = 0, 0
    model_best_B = None
    best_fitting_B = None

    for vertical in range(-10, 10, 5):
        for horizontal in range(-20, 20, 5):
            trans_mat = np.array([[1, 0, horizontal], [0, 1, vertical]], np.float32)
            affine_B = cv2.warpAffine(output_model_B, trans_mat, (x, y))

            for theta in range(-6, 6, 2):
                rotate_mat = cv2.getRotationMatrix2D((x / 2, y / 2), theta, 1)
                rotate_B = cv2.warpAffine(affine_B, rotate_mat, (x, y))

                fitting_B = cv2.bitwise_and(rotate_B, match_seg_B)
                fitting_area = np.sum(fitting_B)

                if fitting_area > max_fitting_area_B:
                    max_fitting_area_B = fitting_area
                    best_theta_B = theta
                    best_vertical_B = vertical
                    best_horizontal_B = horizontal

                    model_best_B = rotate_B
                    best_fitting_B = cv2.bitwise_and(rotate_B, bgr_skeletonize)

    # 避免該片段模型無法擬合
    if model_best_B is None:
        trans_mat = np.array([[1, 0, best_horizontal_A], [0, 1, best_vertical_A]], np.float32)
        affine_B = cv2.warpAffine(output_model_B, trans_mat, (x, y))

        rotate_mat = cv2.getRotationMatrix2D((x/2, y/2), best_theta_A, 1)
        model_best_B = cv2.warpAffine(affine_B, rotate_mat, (x, y))
        best_fitting_B = model_best_B
        best_fitting_B = cv2.erode(best_fitting_B, k, iterations=1)
    # --- matching B End

    # 處理 二尖瓣、動脈瓣膜位置
    hori = (best_horizontal_A + best_horizontal_B) / 2
    vert = (best_vertical_A + best_vertical_B) / 2
    theta = (best_theta_A + best_theta_B) / 2

    trans_mat = np.array([[1, 0, hori], [0, 1, vert]], np.float32)
    affine_mv = cv2.warpAffine(output_mv_pos, trans_mat, (x, y))

    rotate_mat = cv2.getRotationMatrix2D((x/2, y/2), theta, 1)
    mv_pos = cv2.warpAffine(affine_mv, rotate_mat, (x, y))

    hori = (best_horizontal_C + best_horizontal_B) / 2
    vert = (best_vertical_C + best_vertical_B) / 2
    theta = (best_theta_C + best_theta_B) / 2

    trans_mat = np.array([[1, 0, hori], [0, 1, vert]], np.float32)
    affine_av = cv2.warpAffine(output_av_pos, trans_mat, (x, y))

    rotate_mat = cv2.getRotationMatrix2D((x/2, y/2), theta, 1)
    av_pos = cv2.warpAffine(affine_av, rotate_mat, (x, y))

    # 將 A, B, C 的結果合併
    result_A = cv2.addWeighted(best_fitting_A, 0.7, model_best_A, 0.3, 1)
    result_B = cv2.addWeighted(best_fitting_B, 0.7, model_best_B, 0.3, 1)
    result_C = cv2.addWeighted(best_fitting_C, 0.7, model_best_C, 0.3, 1)

    # Q. 使用 numpy 掩模加法白色部分會變黑; 使用 cv2.add() 圖像疊加的方式
    marker = cv2.add(cv2.add(result_A, result_B), result_C)
    muscle_marker = best_fitting_A + best_fitting_B + best_fitting_C

    # cv2.imshow('marker', marker)
    # cv2.imshow('muscle ori', muscle_marker)

    # write_path = './1st data class 9 match/'
    # cv2.imwrite(write_path + file_name + '.png', marker)
    # ----- matching End

    # --- Area bound
    ret_L, locate = cv2.threshold(marker, 50, 255, cv2.THRESH_BINARY)
    ret_S, sk_mark = cv2.threshold(marker, 200, 255, cv2.THRESH_BINARY)

    locate = cv2.cvtColor(locate, cv2.COLOR_BGR2GRAY)

    t = gray_skeletonize.ravel()

    if max(t) < 100:
        continue

    else:
        cnt, hierarchy = cv2.findContours(locate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        hull = list()

        for i in range(len(cnt)):
            for j in range(len(cnt[i])):
                hull.append(cnt[i][j])

        my_array = np.asarray(hull)
        hull = cv2.convexHull(my_array)

        bound = np.zeros(locate.shape, np.uint8)
        cv2.drawContours(bound, [hull], 0, (255, 255, 255), -1)

        k = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        bound = cv2.erode(bound, k, iterations=1)
        cnt_B, hierarchy = cv2.findContours(bound, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        area_BD = np.zeros(locate.shape, np.uint8)
        area_FB = np.zeros(locate.shape, np.uint8)
        cv2.drawContours(area_BD, cnt_B, 0, (255, 255, 255), 2)
        cv2.drawContours(area_FB, cnt_B, 0, (255, 255, 255), -1)

        area_FB = cv2.erode(area_FB, k, iterations=6)

    area_BD = cv2.cvtColor(area_BD, cv2.COLOR_GRAY2BGR)
    area_FB = cv2.cvtColor(area_FB, cv2.COLOR_GRAY2BGR)
    marker = cv2.add(marker, area_BD)
    marker[marker >= 20] = 255
    cv2.imshow('marker', marker)
    cv2.imshow('area_FB', area_FB)
    cv2.imshow('area_BD', area_BD)
    # ----- Area bound End

    # ----- heart center
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    heart_center = cv2.add(model_best_B, best_fitting_B)
    heart_center = cv2.erode(heart_center, k, iterations=8)
    heart_center = cv2.cvtColor(heart_center, cv2.COLOR_BGR2GRAY)

    cnt_center, hierarchy = cv2.findContours(heart_center, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cx, cy, cw, ch = cv2.boundingRect(cnt_center[0])

    # matching B (最右邊的部分, 避免 LA 和 Aortic 連在一起)
    cx, cy = cx + cw, cy + int(ch / 2)
    # print(cx, cy)
    # ----- heart center End

    # ----- LV position
    lv_bound = cv2.add(best_fitting_A, best_fitting_B)
    gray_lv_bound = cv2.cvtColor(lv_bound, cv2.COLOR_BGR2GRAY)

    cnt_lv, hierarchy = cv2.findContours(gray_lv_bound, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hull = list()

    for i in range(len(cnt_lv)):
        for j in range(len(cnt_lv[i])):
            hull.append(cnt_lv[i][j])

    my_array = np.asarray(hull)
    hull = cv2.convexHull(my_array)

    lch_bd = np.zeros(locate.shape, np.uint8)
    cv2.drawContours(lch_bd, [hull], 0, (255, 255, 255), -1)

    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    lch_bd = cv2.erode(lch_bd, k, iterations=1)
    cnt_lv, _ = cv2.findContours(lch_bd, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lch_bd = cv2.cvtColor(lch_bd, cv2.COLOR_GRAY2BGR)
    # ----- LV position End

    count = 0
    lv_size = list()
    curr_list = list()
    # ----- watershed
    while video.ret:
        frame = video.get_frame()

        if not video.ret:
            break

        area_B = area_FB.copy()
        marker_p = marker.copy()
        count += 1

        frame[video.roi != 255] = [0, 0, 0]
        frame = frame[top:bottom, left:right]

        t = frame.ravel()
        t = [tt for tt in t if 256 > tt > 30]
        avg = sum(t) // len(t)
        # print('avg:', avg)

        # --- chamber marker
        marker_all = cv2.add(marker, cv2.add(mv_pos, av_pos))
        # marker_all = cv2.cvtColor(marker_all, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('marker_all', marker_all)

        ret2, th2 = cv2.threshold(frame, avg+25, 255, cv2.THRESH_BINARY_INV)
        in_mark = cv2.bitwise_and(th2, area_B)
        cv2.imshow('th2 in_mark', in_mark)

        in_mark = cv2.subtract(in_mark, marker_p)
        cv2.imshow('th3 in_mark', in_mark)

        retM, thM = cv2.threshold(frame, avg-5, 255, cv2.THRESH_BINARY)
        # cv2.imshow('thM', thM)
        thM = cv2.bitwise_and(thM, marker_p)
        thM = cv2.bitwise_and(thM, area_B)
        # cv2.imshow('thM', thM)

        k = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        in_mark = cv2.erode(in_mark, k, iterations=3)

        cv2.line(in_mark, (cx, cy), (800, cy), (0, 0, 0), 20)
        in_mark[mask_roi != 255] = 0
        in_mark[mv_pos == 255] = 0
        in_mark[av_pos == 255] = 0
        in_mark = cv2.erode(in_mark, k, iterations=3)

        result_marker = cv2.add(thM, in_mark)
        result_frame = cv2.add(frame, result_marker)
        cv2.imshow('result_marker', result_marker)

        lv_locate = cv2.cvtColor(in_mark, cv2.COLOR_BGR2GRAY)
        cnt_lc, _ = cv2.findContours(lv_locate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        size = 0
        lv_lc = list()

        for c in cnt_lc:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)

            if area > size:
                lv_lc.append([(x+w/2), (y+h/2)])
                size = area

        # --- chamber marker End

        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        bg = cv2.dilate(area_B, k, iterations=1)
        unknown = cv2.subtract(bg, result_marker)

        gray_fg = cv2.cvtColor(result_marker, cv2.COLOR_BGR2GRAY)
        unknown = cv2.cvtColor(unknown, cv2.COLOR_BGR2GRAY)

        _, markers = cv2.connectedComponents(gray_fg)
        markers = markers + 1
        markers[unknown == 255] = 0

        markers = cv2.watershed(frame, markers)
        uni_mark, count = np.unique(markers, return_counts=True)
        # 先計算 marker 數量, 若 count 小於 一個值 就給它=0
        # print('marker amount:', len(uni_mark))

        # watershed -1 是邊界
        # color_info = np.zeros(frame.shape, np.uint8)
        # reg_color = list()
        #
        # for m in range(len(uni_mark)):
        #     if uni_mark[m] > 1 and count[m] > 300:
        #         b = np.random.randint(50, 200)
        #         g = np.random.randint(50, 200)
        #         r = np.random.randint(50, 200)
        #         color_info[markers == uni_mark[m]] = [b, g, r]
        #
        #         if [b, g, r] in reg_color:
        #             color_info[markers == uni_mark[m]] = [0, g-43, r-18]
        #
        #         reg_color.append([b, g, r])
        #
        # color_info[markers == -1] = [0, 0, 0]
        # curr_result = cv2.addWeighted(color_info, 0.3, frame, 1, 1)
        # cv2.circle(curr_result, (cx, cy), 1, (0, 255, 0), 20)
        # curr_list.append(curr_result)

        cv2.imshow('bg', bg)
        # cv2.imshow('gray_fg', gray_fg)
        cv2.imshow('unknown', unknown)
        cv2.imshow('in_mark', in_mark)
        # cv2.imshow('curr_result', curr_result)
        # cv2.imshow('frame', frame)
        # cv2.waitKey(1)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('p'):
            while cv2.waitKey(1) != ord(' '):
                pass

    # write_path = './1st data class 9 muscle/'
    # print(file_name)
    # write_video(curr_list, write_path + file_name)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('p'):
        while cv2.waitKey(1) != ord(' '):
            pass

cv2.destroyAllWindows()
