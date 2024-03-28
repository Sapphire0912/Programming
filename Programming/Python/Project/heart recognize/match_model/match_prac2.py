import os
import glob
import numpy as np
import cv2


class VideoInit(object):
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)
        self.ret = True

        if not self.video:
            raise Exception('影片檔案路徑不存在或格式錯誤')

        else:
            self.y, self.x, self.channel = self.video.read()[1].shape

        # 處理超音波的 ROI
        # 經過 handle_bound_test 測試後, 已找出超音播的扇形圓心位置以及一些圓的參數
        # (假定所有的超音波影像都是這樣, 以及所有的輸入影像大小皆相等)
        self.ox, self.oy = 402, 63
        self.roi_radius = 495
        self.roi_angle = 90
        self.roi_rotate_pos = (-45, 45)

        mask_roi = np.zeros(self.video.read()[1].shape[:2], np.uint8)
        self.roi = cv2.ellipse(
            mask_roi,
            (self.ox, self.oy),
            (self.roi_radius, self.roi_radius),
            self.roi_angle,
            startAngle=self.roi_rotate_pos[0],
            endAngle=self.roi_rotate_pos[1],
            color=(255, 255, 255),
            thickness=-1
        )

    def get_frame(self):
        self.ret, curr_frame = self.video.read()
        return curr_frame

    def release_video(self):
        self.video.release()
        return True

    def get_info(self):
        pass

    def matching(self, model, target, vert, hori, rotate):
        pass


# 嘗試擬合骨架化的模型
video_dir = '.\\1st data class 9\\'
all_video_path = glob.glob(video_dir + '*.avi')

skeletonize_dir = '.\\1st data class 9 skeletonize\\'

for path in all_video_path:
    # 檔案名稱
    file_name = path.split('\\')[-1]

    # 用 class 方式建立 影片屬性和方法
    video = VideoInit(path)
    roi = video.roi

    # 讀取骨架圖片
    skeletonize_file_path = skeletonize_dir + file_name + '.png'
    skeletonize_file = cv2.imread(skeletonize_file_path)

    skeletonize_file[roi != 255] = [0, 0, 0]
    gray_skeletonize = cv2.cvtColor(skeletonize_file, cv2.COLOR_BGR2GRAY)

    # ----- 找出骨架的邊界(調整模型比例用的)
    # roi 最小矩形的範圍
    contour_roi, hierarchy = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contour_roi[0])
    roi = roi[y:y+h, x:x+w]
    gray_skeletonize = gray_skeletonize[y:y+h, x:x+w]

    x_bound = list()
    y_bound = list()

    contour_skeletonize, hierarchy = cv2.findContours(gray_skeletonize, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contour_skeletonize)):
        for j in range(len(contour_skeletonize[i])):
            x_bound.append(contour_skeletonize[i][j][0][0])
            y_bound.append((contour_skeletonize[i][j][0][1]))

    try:
        ske_x, ske_y = min(x_bound), min(y_bound)
        ske_height, ske_width = max(y_bound) - min(y_bound), max(x_bound) - min(x_bound)

    except ValueError:
        print('%s 骨架圖片可能是全黑的' % path)
        continue
    # ----- End

    # ----- 調整模型的大小比例
    # matching 模型時 從較明顯的區域開始擬合(A -> C -> B)
    model_all = cv2.imread('./model_anchor/0009_Parasternal long axis.png')
    model_A = cv2.imread('./model_anchor/0009_Parasternal long axis_1.png')
    model_B = cv2.imread('./model_anchor/0009_Parasternal long axis_2.png')
    model_C = cv2.imread('./model_anchor/0009_Parasternal long axis_3.png')

    model_all_gray = cv2.cvtColor(model_all, cv2.COLOR_BGR2GRAY)
    _, model_all_thres = cv2.threshold(model_all_gray, 180, 255, cv2.THRESH_BINARY)
    contour_model, hierarchy = cv2.findContours(model_all_thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 原始二尖瓣位置(未找到瓣膜前, 暫時寫死)
    valve_pos = np.zeros(model_all.shape, np.uint8)
    top_valve = (691, 384)
    bottom_valve = (649, 445)
    cv2.line(valve_pos, top_valve, bottom_valve, (255, 255, 255), 20)

    # 找出模型的最小擬合矩形後, 裁減原始圖像
    # 最小擬合矩形(無角度)
    x, y, w, h = cv2.boundingRect(contour_model[0])

    # 裁減原始圖像
    model_all = model_all[y:y+h, x:x+w]
    model_A = model_A[y:y+h, x:x+w]
    model_B = model_B[y:y+h, x:x+w]
    model_C = model_C[y:y+h, x:x+w]
    valve_pos = valve_pos[y:y+h, x:x+w]

    # 調整比例
    model_height, model_width = model_all.shape[:2]
    height_scale = ske_height / model_height
    width_scale = ske_width / model_width

    # ===== 這部分暫時沒有用到
    # 裁減圖像後的 二尖瓣位置(左上角座標)
    top_valve_x, top_valve_y = top_valve[0] - x, top_valve[1] - y
    bottom_valve_x, bottom_valve_y = bottom_valve[0] - x, bottom_valve[1] - y

    top_valve_pos = (top_valve_x * width_scale, top_valve_y * height_scale)
    bottom_valve_pos = (bottom_valve_x * width_scale, bottom_valve_x * height_scale)
    # =====

    re_width = np.round(model_width * width_scale).astype(np.int)
    re_height = np.round(model_height * height_scale).astype(np.int)

    re_model_all = cv2.resize(model_all, (re_width, re_height))
    re_model_A = cv2.resize(model_A, (re_width, re_height))
    re_model_B = cv2.resize(model_B, (re_width, re_height))
    re_model_C = cv2.resize(model_C, (re_width, re_height))
    output_value_pos = cv2.resize(valve_pos, (re_width, re_height))

    # 把模型分別放在和扇形區域相對應的位置
    roi_x, roi_y = roi.shape
    output_model_A = np.zeros((roi_x, roi_y, 3), np.uint8)
    output_model_B = np.zeros((roi_x, roi_y, 3), np.uint8)
    output_model_C = np.zeros((roi_x, roi_y, 3), np.uint8)

    output_model_A[ske_y:ske_y+ske_height, ske_x:ske_x+ske_width] = re_model_A
    output_model_B[ske_y:ske_y+ske_height, ske_x:ske_x+ske_width] = re_model_B
    output_model_C[ske_y:ske_y+ske_height, ske_x:ske_x+ske_width] = re_model_C
    # ----- End

    # ----- 找到肌肉相對應位置
    # 將原始灰階圖片轉成 BGR 後, 做形態學
    bgr_skeletonize = cv2.cvtColor(gray_skeletonize, cv2.COLOR_GRAY2BGR)

    k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    closing = cv2.morphologyEx(bgr_skeletonize, cv2.MORPH_CLOSE, k, iterations=1)
    dilation = cv2.dilate(closing, k, iterations=4)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, k, iterations=1)

    # cv2.imshow('bgr sk', bgr_skeletonize)
    # cv2.imshow('closing', closing)
    y, x, color = bgr_skeletonize.shape
    # matching 寫在 class 裡面(之後思考一下)
    # 根據每幀調整在這裡寫 while(沒有必要全部的東西都重新跑過)

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

            for theta in range(-10, 30, 5):
                rotate_mat = cv2.getRotationMatrix2D((x / 2, y / 2), theta, 1)
                rotate_A = cv2.warpAffine(affine_A, rotate_mat, (x, y))

                # cv2.imshow('rotate_A', rotate_A)
                fitting_A = cv2.bitwise_and(rotate_A, closing)
                # cv2.imshow('fitting_A', fitting_A)
                # cv2.waitKey(10)
                fitting_area = np.sum(fitting_A)

                if fitting_area > max_fitting_area_A:
                    max_fitting_area_A = fitting_area
                    best_theta_A = theta
                    best_vertical_A = vertical
                    best_horizontal_A = horizontal

                    model_best_A = rotate_A
                    best_fitting_A = cv2.bitwise_and(rotate_A, bgr_skeletonize)

    check_A = cv2.addWeighted(bgr_skeletonize, 1, model_best_A, 0.3, 1)
    # 把超出扇形的部分去除掉
    check_A[roi != 255] = [0, 0, 0]
    # cv2.imshow('filter_check_A', check_A)

    # cv2.imshow('best_fitting_A', best_fitting_A)
    # --- matching A End

    # 處理 二尖瓣位置
    trans_mat = np.array([[1, 0, best_horizontal_A], [0, 1, best_vertical_A]], np.float32)
    affine_valve = cv2.warpAffine(output_value_pos, trans_mat, (x, y))

    rotate_mat = cv2.getRotationMatrix2D((x/2, y/2), best_theta_A, 1)
    rotate_valve = cv2.warpAffine(affine_valve, rotate_mat, (x, y))

    # --- matching C
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

                fitting_C = cv2.bitwise_and(rotate_C, closing)
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

    check_C = cv2.addWeighted(bgr_skeletonize, 1, model_best_C, 0.3, 1)
    # 把超出扇形的部分去除掉
    check_C[roi != 255] = [0, 0, 0]
    # cv2.imshow('filter_check_C', check_C)
    # --- matching C End

    # --- matching B
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

                fitting_B = cv2.bitwise_and(rotate_B, closing)
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

    check_B = cv2.addWeighted(bgr_skeletonize, 1, model_best_B, 0.3, 1)
    # 把超出扇形的部分去除掉
    check_B[roi != 255] = [0, 0, 0]
    # cv2.imshow('filter_check_A', check_A)
    # --- matching B End

    # 將 A, B, C 的結果合併
    result_A = cv2.addWeighted(best_fitting_A, 0.7, model_best_A, 0.3, 1)
    result_B = cv2.addWeighted(best_fitting_B, 0.7, model_best_B, 0.3, 1)
    result_C = cv2.addWeighted(best_fitting_C, 0.7, model_best_C, 0.3, 1)

    # Q. 使用 numpy 掩模加法白色部分會變黑; 使用 cv2.add() 圖像疊加的方式
    marker = cv2.add(cv2.add(result_A, result_B), result_C)
    muscle_marker = best_fitting_A + best_fitting_B + best_fitting_C

    print(path)
    marker = cv2.cvtColor(marker, cv2.COLOR_BGR2GRAY)
    relative_pos = cv2.bitwise_xor(roi, marker)
    cv2.imshow('relative_pos', relative_pos)
    cv2.imshow('result', marker)
    cv2.imshow('muscle_marker', muscle_marker)
    cv2.waitKey(5000)
    # write_path = './1st que result/'
    # cv2.imwrite(write_path + file_name + '.png', marker)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('p'):
        while cv2.waitKey(1) != ord(' '):
            pass

cv2.destroyAllWindows()
