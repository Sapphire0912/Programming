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
    mask_roi = video.roi

    # 讀取骨架圖片
    skeletonize_file_path = skeletonize_dir + file_name + '.png'
    skeletonize_file = cv2.imread(skeletonize_file_path)

    skeletonize_file[mask_roi != 255] = [0, 0, 0]
    gray_skeletonize = cv2.cvtColor(skeletonize_file, cv2.COLOR_BGR2GRAY)

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

    # 調整比例
    scale = radius / radius_model
    ori_height, ori_width = model_all.shape[:2]
    width, height = int(ori_width * scale), int(ori_height * scale)

    output_model_all = cv2.resize(model_all, (width, height))
    output_model_A = cv2.resize(model_A, (width, height))
    output_model_B = cv2.resize(model_B, (width, height))
    output_model_C = cv2.resize(model_C, (width, height))
    # ----- End

    # ----- 找到肌肉相對應位置(根據每幀做 matching)
    # 抓出每一幀
    curr_res = list()
    frame_count = 0
    while video.ret:
        frame = video.get_frame()
        frame_count += 1
        if not video.ret:
            break

        frame[video.roi != 255] = [0, 0, 0]
        frame = frame[top:bottom, left:right]
        frame_cp = frame.copy()

        y, x, _ = frame.shape
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

                    fitting_A = cv2.bitwise_and(rotate_A, frame)
                    fitting_area = np.sum(fitting_A)

                    if fitting_area > max_fitting_area_A:
                        max_fitting_area_A = fitting_area
                        best_theta_A = theta
                        best_vertical_A = vertical
                        best_horizontal_A = horizontal

                        model_best_A = rotate_A
                        best_fitting_A = cv2.bitwise_and(rotate_A, frame)
        # --- matching A End

        # --- matching C
        # 將 A 區塊消除
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        Area_A = cv2.dilate(best_fitting_A, k, iterations=15)

        match_seg_C = frame.copy()
        match_seg_C[Area_A == 255] = 0

        max_fitting_area_C = 0
        best_theta_C = 0
        best_horizontal_C, best_vertical_C = 0, 0
        model_best_C = None
        best_fitting_C = None

        for vertical in range(-32, 0, 4):
            for horizontal in range(-20, 6, 4):
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
                        best_fitting_C = cv2.bitwise_and(rotate_C, frame)

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

        match_seg_B = frame.copy()
        match_seg_B[Area_A == 255] = 0
        match_seg_B[Area_C == 255] = 0

        max_fitting_area_B = 0
        best_theta_B = 0
        best_horizontal_B, best_vertical_B = 0, 0
        model_best_B = None
        best_fitting_B = None

        for vertical in range(-10, 10, 5):
            for horizontal in range(-50, 10, 5):
                trans_mat = np.array([[1, 0, horizontal], [0, 1, vertical]], np.float32)
                affine_B = cv2.warpAffine(output_model_B, trans_mat, (x, y))

                for theta in range(-10, 10, 2):
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
                        best_fitting_B = cv2.bitwise_and(rotate_B, frame)

        # 避免該片段模型無法擬合
        if model_best_B is None:
            trans_mat = np.array([[1, 0, best_horizontal_A], [0, 1, best_vertical_A]], np.float32)
            affine_B = cv2.warpAffine(output_model_B, trans_mat, (x, y))

            rotate_mat = cv2.getRotationMatrix2D((x/2, y/2), best_theta_A, 1)
            model_best_B = cv2.warpAffine(affine_B, rotate_mat, (x, y))
            best_fitting_B = model_best_B
            best_fitting_B = cv2.erode(best_fitting_B, k, iterations=1)
        # --- matching B End

        # 將 A, B, C 的結果合併
        result_A = cv2.addWeighted(best_fitting_A, 0.7, model_best_A, 0.3, 1)
        result_B = cv2.addWeighted(best_fitting_B, 0.7, model_best_B, 0.3, 1)
        result_C = cv2.addWeighted(best_fitting_C, 0.7, model_best_C, 0.3, 1)

        muscle_all = cv2.add(cv2.add(result_A, result_B), result_C)
        muscle_marker = best_fitting_A + best_fitting_B + best_fitting_C

        # cv2.imshow('muscle_marker', muscle_marker)
        # cv2.imshow('muscle_all', muscle_all)
        # ----- matching End.

        # ----- Muscle bound
        _, muscle_thres = cv2.threshold(muscle_all, 50, 255, cv2.THRESH_BINARY)
        gray_muscle = cv2.cvtColor(muscle_thres, cv2.COLOR_BGR2GRAY)
        cnt_muscle, _ = cv2.findContours(gray_muscle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hull_muscle = list()
        for i in range(len(cnt_muscle)):
            for j in range(len(cnt_muscle[i])):
                hull_muscle.append(cnt_muscle[i][j])

        hull_muscle = np.asarray(hull_muscle)
        hull_muscle = cv2.convexHull(hull_muscle)

        bound_region = np.zeros(muscle_all.shape, np.uint8)
        bound_line = np.zeros(muscle_all.shape, np.uint8)
        cv2.drawContours(bound_region, [hull_muscle], 0, (255, 255, 255), -1)
        cv2.drawContours(bound_line, [hull_muscle], 0, (255, 255, 255), 2)

        bound_all = cv2.bitwise_or(bound_line, muscle_thres)
        gray_bound_region = cv2.cvtColor(bound_region, cv2.COLOR_BGR2GRAY)
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        erode_bound_region = cv2.erode(gray_bound_region, k, iterations=10)
        # cv2.imshow('bound_region', bound_region)
        # ----- Muscle bound End

        # ----- chamber & muscle marker
        # 分成 A, B, C 三個區段來處理
        mask_muscle = np.zeros(muscle_marker.shape[:2], np.uint8)

        gray_muscle_A = cv2.cvtColor(best_fitting_A, cv2.COLOR_BGR2GRAY)
        gray_muscle_B = cv2.cvtColor(best_fitting_B, cv2.COLOR_BGR2GRAY)
        gray_muscle_C = cv2.cvtColor(best_fitting_C, cv2.COLOR_BGR2GRAY)

        _, thres_muscle_A = cv2.threshold(gray_muscle_A, 50, 255, cv2.THRESH_BINARY)
        _, thres_muscle_B = cv2.threshold(gray_muscle_B, 50, 255, cv2.THRESH_BINARY)
        _, thres_muscle_C = cv2.threshold(gray_muscle_C, 50, 255, cv2.THRESH_BINARY)

        # 處理瓣膜 mitral, aortic valve
        cnt_muscle_A, _ = cv2.findContours(thres_muscle_A, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt_muscle_B, _ = cv2.findContours(thres_muscle_B, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt_muscle_C, _ = cv2.findContours(thres_muscle_C, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 限制瓣膜抓取的範圍(用已知的資訊來處理)
        # 找出 Mitral valve 位置
        all_bx, all_by = list(), list()
        max_cnt_area_B = 20
        center_muscle_bx, center_muscle_by = 0, 0
        for cnt_B_index in range(len(cnt_muscle_B)):
            # 找出輪廓面積最大區塊的中心點, 用來定位用
            area = cv2.contourArea(cnt_muscle_B[cnt_B_index])
            if area > max_cnt_area_B:
                M = cv2.moments(cnt_muscle_B[cnt_B_index])
                center_muscle_bx = int(M["m10"] / M["m00"])
                center_muscle_by = int(M["m01"] / M["m00"])
                max_cnt_area_B = area

            for B_point_index in range(len(cnt_muscle_B[cnt_B_index])):
                bx, by = cnt_muscle_B[cnt_B_index][B_point_index][0]
                all_bx.append(bx)
                all_by.append(by)

        all_A_point = list()
        max_cnt_area_A = 20
        center_muscle_ax, center_muscle_ay = 0, 0
        for cnt_A_index in range(len(cnt_muscle_A)):
            # 找出輪廓面積最大區塊的中心點, 用來定位用
            area = cv2.contourArea(cnt_muscle_A[cnt_A_index])
            if area > max_cnt_area_A:
                M = cv2.moments(cnt_muscle_A[cnt_A_index])
                center_muscle_ax = int(M["m10"] / M["m00"])
                center_muscle_ay = int(M["m01"] / M["m00"])
                max_cnt_area_A = area

            for A_point_index in range(len(cnt_muscle_A[cnt_A_index])):
                ax, ay = cnt_muscle_A[cnt_A_index][A_point_index][0]
                all_A_point.append([ax, ay])

        # 找出 contour 的全距, 取一個距離去限制瓣膜搜尋的範圍(mitral)
        search_range = (max(all_bx) - min(all_bx)) * 0.2 + min(all_bx)
        mv_range = list()
        for f in range(len(all_bx)):
            if all_bx[f] <= search_range:
                mv_range.append([all_bx[f], all_by[f]])

        min_dis = 600
        last_ax, last_ay = 0, 0
        last_bx, last_by = 0, 0
        for a_index in range(len(all_A_point)):
            ax, ay = all_A_point[a_index]
            for b_index in range(len(mv_range)):
                bx, by = mv_range[b_index]
                distance = np.sqrt((bx - ax) ** 2 + (by - ay) ** 2)

                if distance < min_dis:
                    last_ax, last_ay = ax, ay
                    last_bx, last_by = bx, by
                    min_dis = distance

        # 找出 aortic valve 位置
        all_C_point = list()
        max_cnt_area_C = 20
        center_muscle_cx, center_muscle_cy = 0, 0
        for cnt_C_index in range(len(cnt_muscle_C)):
            # 找出輪廓面積最大區塊的中心點, 用來定位用
            area = cv2.contourArea(cnt_muscle_C[cnt_C_index])
            if area > max_cnt_area_C:
                M = cv2.moments(cnt_muscle_C[cnt_C_index])
                center_muscle_cx = int(M["m10"] / M["m00"])
                center_muscle_cy = int(M["m01"] / M["m00"])
                max_cnt_area_C = area

            for C_point_index in range(len(cnt_muscle_C[cnt_C_index])):
                cx, cy = cnt_muscle_C[cnt_C_index][C_point_index][0]
                all_C_point.append([cx, cy])

        # 限制搜尋範圍(aortic)
        max_search_range = (max(all_bx) - min(all_bx)) * 0.6 + min(all_bx)
        min_search_range = (max(all_bx) - min(all_bx)) * 0.3 + min(all_bx)
        av_range = list()
        for f in range(len(all_bx)):
            if max_search_range > all_bx[f] >= min_search_range:
                av_range.append([all_bx[f], all_by[f]])

        min_dis = 600
        last_cx, last_cy = 0, 0
        last_bx2, last_by2 = 0, 0
        for c_index in range(len(all_C_point)):
            cx, cy = all_C_point[c_index]
            for b_index in range(len(av_range)):
                bx, by = av_range[b_index]
                distance = np.sqrt((bx - cx) ** 2 + (by - cy) ** 2)

                if distance < min_dis:
                    last_cx, last_cy = cx, cy
                    last_bx2, last_by2 = bx, by
                    min_dis = distance

        gray_muscle_marker = cv2.cvtColor(muscle_marker, cv2.COLOR_BGR2GRAY)
        _, thres_muscle_marker = cv2.threshold(gray_muscle_marker, 50, 255, cv2.THRESH_BINARY)
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        erode_muscle_marker = cv2.erode(thres_muscle_marker, k, iterations=1)
        mask_muscle = cv2.bitwise_or(mask_muscle, erode_muscle_marker)

        k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask_muscle = cv2.erode(mask_muscle, k, iterations=3)

        center_list = list()
        center_list.append([center_muscle_ax, center_muscle_ay])
        center_list.append([center_muscle_bx, center_muscle_by])
        center_list.append([center_muscle_cx, center_muscle_cy])
        # print('muscle center info: ', muscle_center_info)

        # cv2.imshow('muscle marker', muscle_marker)
        # cv2.imshow('mask_muscle', mask_muscle)
        # cv2.imshow('erode_muscle_marker', erode_muscle_marker)

        # 處理腔室的 marker
        # 根據每一幀去找出腔室的區域(瓣膜暫時用寫死的方式)
        frame_cp[erode_bound_region != 255] = [0, 0, 0]

        gray_frame = cv2.cvtColor(frame_cp, cv2.COLOR_BGR2GRAY)
        cv2.line(gray_frame, (last_ax-30, last_ay-6), (last_bx-30, last_by+6), (255, 255, 255), 20)
        cv2.line(gray_frame, (last_cx-25, last_cy-10), (last_bx2-25, last_by2+10), (255, 255, 255), 20)
        # cv2.imshow('gray_frame', gray_frame)

        frame_inv = cv2.bitwise_not(gray_frame, mask=gray_frame)
        _, thres = cv2.threshold(frame_inv, 195, 255, cv2.THRESH_BINARY)

        k = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closing = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, k, iterations=2)
        cnt_closing, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        filter_marker = np.zeros(frame_cp.shape, np.uint8)
        mask_filter = np.zeros(frame_cp.shape[:2], np.uint8)
        for c in cnt_closing:
            # 過濾小區域
            if cv2.contourArea(c) > 3000:
                cv2.drawContours(filter_marker, [c], -1, (255, 255, 255), -1)
        filter_marker = cv2.erode(filter_marker, k, iterations=2)
        filter_marker = cv2.cvtColor(filter_marker, cv2.COLOR_BGR2GRAY)

        cnt_filter, _ = cv2.findContours(filter_marker, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnt_filter:
            if cv2.contourArea(c) > 2000:
                cv2.drawContours(mask_filter, [c], -1, (255, 255, 255), -1)
        mask_filter = cv2.erode(mask_filter, k, iterations=2)
        mask_filter[erode_bound_region != 255] = 0
        # cv2.imshow('mask_filter1', mask_filter)

        # 找出不同腔室的定位點(順便過濾 erode 後的雜點)
        reg_x, reg_y = list(), list()
        cnt_mask, _ = cv2.findContours(mask_filter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt_m_index in range(len(cnt_mask)):
            area = cv2.contourArea(cnt_mask[cnt_m_index])
            if area > 200:
                M = cv2.moments(cnt_mask[cnt_m_index])
                center_chamber_x = int(M["m10"] / M["m00"])
                center_chamber_y = int(M["m01"] / M["m00"])
                reg_x.append(center_chamber_x)
                reg_y.append(center_chamber_y)
            else:
                cv2.drawContours(mask_filter, [cnt_mask[cnt_m_index]], -1, (0, 0, 0), -1)

        # 先用 x 軸抓出 LV 位置後, 再用 y 軸分出 LA 和 Aortic 位置(如果存在的情況)
        # LV 一定在最左邊, 並且小於 整張圖片正中心的位置
        img_center_x, img_center_y = mask_filter.shape
        img_center_x = img_center_x // 2
        img_center_y = img_center_y // 2

        reg_sort_x = sorted(reg_x)

        lv_center = list()
        for i in range(len(reg_sort_x)):
            if reg_sort_x[i] < img_center_x:
                lv_pos = reg_x.index(reg_sort_x[i])
                lv_center.append([reg_x[lv_pos], reg_y[lv_pos]])
                del reg_x[lv_pos], reg_y[lv_pos]

        if len(lv_center) > 1:
            for cen_lv_index in range(0, len(lv_center) - 1):
                p1x, p1y = lv_center[cen_lv_index]
                p2x, p2y = lv_center[cen_lv_index + 1]
                cv2.line(mask_filter, (p1x, p1y), (p2x, p2y), (255, 255, 255), 1)
                lv_cx, lv_cy = int((p1x + p2x) / 2), int((p1y + p2y) / 2)
                center_list.append([[lv_cx, lv_cy]])
        else:
            center_list.append(lv_center)

        # 拿 muscle B 的 y 軸當成區分 LA 和 Aortic 的標準
        Bx, By = center_list[1]
        la_center = list()
        aortic_center = list()
        for j in range(len(reg_y)):
            if reg_y[j] < By:
                aortic_center.append([reg_x[j], reg_y[j]])
            else:
                la_center.append([reg_x[j], reg_y[j]])
        if la_center != list():
            center_list.append(la_center)
        if aortic_center != list():
            center_list.append(aortic_center)
        # print('center_list:', center_list)

        mask_filter[mask_muscle == 255] = 255
        # cv2.imshow('frame', frame)
        # cv2.imshow('closing', closing)
        # cv2.imshow('filter_marker', filter_marker)
        cv2.imshow('mask_filter_res', mask_filter)
        # ----- chamber & muscle End

        # ----- watershed
        bg = cv2.dilate(gray_bound_region, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)), iterations=1)
        unknown = cv2.subtract(bg, mask_filter)
        # cv2.imshow('unknown', unknown)

        _, markers = cv2.connectedComponents(mask_filter)
        markers = markers + 1
        markers[unknown == 255] = 0
        markers = cv2.watershed(frame, markers)
        uni_mark, count = np.unique(markers, return_counts=True)
        # print('original:', uni_mark, count)

        # 找出 watershed 的結果具體位於心臟的哪個位置
        # -1 是邊界, 1 是背景
        color_info = np.zeros(frame.shape, np.uint8)
        # print('center_info:', center_info)

        colors = [
            [255, 0, 0],
            [0, 255, 0],
            [0, 0, 255],
            [255, 255, 0],
            [0, 255, 255],
            [255, 0, 255]
        ]

        reg_pos = np.zeros(frame.shape[:2], np.uint8)
        bound_info = np.zeros(frame.shape, np.uint8)

        for m in range(len(uni_mark)):
            index, min_dis = 0, 600

            # 過濾太小區域
            if uni_mark[m] > 1 and count[m] > 500:
                reg_pos[markers == uni_mark[m]] = 255

                cnt_reg, _ = cv2.findContours(reg_pos, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                M = cv2.moments(cnt_reg[0])
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])

                # 計算 center_x, center_y 和 肌肉 & 腔室位置的最短距離
                for d in range(len(center_list)):
                    if isinstance(center_list[d][0], list):
                        for i in range(len(center_list[d])):
                            xx, yy = center_list[d][i]
                            distance = np.sqrt((center_x - xx) ** 2 + (center_y - yy) ** 2)
                            if min_dis > distance:
                                min_dis = distance
                                index = d
                    else:
                        xx, yy = center_list[d]
                        distance = np.sqrt((center_x - xx) ** 2 + (center_y - yy) ** 2)
                        if min_dis > distance:
                            min_dis = distance
                            index = d

                color_info[markers == uni_mark[m]] = colors[index]
                b, g, r = colors[index]
                cv2.drawContours(bound_info, cnt_reg, -1, (b, g, r), 2)
                reg_pos[markers == uni_mark[m]] = 0
                cv2.waitKey(50)

        curr_result = cv2.addWeighted(frame, 1, color_info, 0.1, 1)
        curr_result = cv2.addWeighted(curr_result, 1, bound_info, 1, 1)
        curr_res.append(curr_result)
        cv2.imshow('curr_result', curr_result)
        cv2.waitKey(1)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        elif key == ord('p'):
            while cv2.waitKey(1) != ord(' '):
                pass
        # ----- watershed end

    write_path = './1st data class 9 muscle/' + file_name
    print(write_path)
    write_video(curr_res, write_path)
    # ----- matching End

cv2.destroyAllWindows()
