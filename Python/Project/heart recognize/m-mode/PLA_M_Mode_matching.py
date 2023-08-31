from find_roi import FindROI
from find_unit import handle_unit
from read_file import Allfiles
from skeletonize_bound import skeleton_bound
from model_scale import adjust_scale
from matching import match_muscleA, match_muscleB, match_muscleC

from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import cv2


def find_keypoint(fitting, n_poly=4, keypoint_step=10):
    fitting = cv2.cvtColor(fitting, cv2.COLOR_BGR2GRAY)
    cnt_fit, _ = cv2.findContours(fitting, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x_points, y_points = list(), list()

    for i in range(len(cnt_fit)):
        for j in range(len(cnt_fit[i])):
            x_points.append(cnt_fit[i][j][0][0])
            y_points.append(cnt_fit[i][j][0][1])

    x_points = np.asarray(x_points)
    y_points = np.asarray(y_points)

    # curve fitting
    linear_model = np.polyfit(x_points, y_points, n_poly)
    linear_model = np.poly1d(linear_model)
    x_key_points = np.arange(min(x_points), max(x_points), keypoint_step)
    y_key_points = linear_model(x_key_points)

    return (x_points, y_points), (x_key_points, y_key_points)


def new_fitting(points, n_poly=4, keypoint_step=10):
    x_points, y_points = points[:, 0], points[:, 1]

    # curve fitting
    linear_model = np.polyfit(x_points, y_points, n_poly)
    linear_model = np.poly1d(linear_model)
    x_key_points = np.arange(min(x_points), max(x_points), keypoint_step)
    y_key_points = linear_model(x_key_points)

    return (x_points, y_points), (x_key_points, y_key_points)


def write_video(frames_list, output_path):
    y, x, _ = frames_list[0].shape
    video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), 30, (x, y))
    for i in frames_list:
        video_writer.write(i)
    video_writer.release()


video_path = Allfiles('.\\video\\', 'avi')
skeletonize_path = Allfiles('.\\ske_png\\', '.png')

model_all = cv2.imread('./model_anchor/0009_Parasternal long axis.png')
model_A = cv2.imread('./model_anchor/0009_Parasternal long axis_1.png')
model_B = cv2.imread('./model_anchor/0009_Parasternal long axis_2.png')
model_C = cv2.imread('./model_anchor/0009_Parasternal long axis_3.png')

for path in video_path:
    file_name = path.split('\\')[-1]

    # ----- Pre. 處理基本資訊
    # ROI 區域
    video = FindROI(path)
    video.roi_region(path)
    mask_roi = video.roi
    ox, oy = video.ox, video.oy

    # 標準單位
    unit = handle_unit(path)
    # ----- Pre. OK

    # ----- 1. 找出骨架邊界並調整標準模型的比例
    skeleton = '.\\ske_png\\' + file_name + '.png'
    skeleton_info = skeleton_bound(skeleton, mask_roi)

    if skeleton_info is None:
        continue

    skeleton = cv2.imread(skeleton)
    skeleton[mask_roi != 255] = [0, 0, 0]

    top, bottom, left, right, radius = skeleton_info
    mask_roi_effect = mask_roi[top:bottom, left:right]
    skeleton_effect = skeleton[top:bottom, left:right]

    output_model_A, output_model_B, output_model_C = adjust_scale(model_all, model_A, model_B, model_C, radius)
    # ----- 1. OK

    # ------ 2. matching 骨架圖找出 key points
    # Current method
    model_best_A, best_fitting_A = match_muscleA(skeleton_effect, output_model_A)
    model_best_C, best_fitting_C = match_muscleC(skeleton_effect, output_model_C)
    model_best_B, best_fitting_B = match_muscleB(skeleton_effect, output_model_B)

    cnt_pointA, fit_pointA = find_keypoint(best_fitting_A, n_poly=4, keypoint_step=20)
    cnt_pointB, fit_pointB = find_keypoint(best_fitting_B, n_poly=3, keypoint_step=15)
    cnt_pointC, fit_pointC = find_keypoint(best_fitting_C, n_poly=4, keypoint_step=20)

    A_points = np.vstack([fit_pointA[0], fit_pointA[1]]).T.astype(np.int)
    B_points = np.vstack([fit_pointB[0], fit_pointB[1]]).T.astype(np.int)
    C_points = np.vstack([fit_pointC[0], fit_pointC[1]]).T.astype(np.int)

    # ori_model = cv2.add(cv2.add(output_model_A, output_model_B), output_model_C)
    # cv2.imshow('mb', model_best)
    # cv2.imshow('ori', ori_model)
    # cv2.waitKey(0)

    # curr = cv2.add(cv2.add(best_fitting_A, best_fitting_B), best_fitting_C)
    # cv2.imshow('curr', curr)
    # cv2.waitKey(0)

    # visible
    # for i in range(len(fit_pointA[0])):
    #     cv2.circle(skeleton_effect, (int(fit_pointA[0][i]), int(fit_pointA[1][i])), 5, (0, 128, 255), -1)
    #     cv2.circle(skeleton_effect, (int(fit_pointA[0][i]), int(fit_pointA[1][i])), 5, (255, 255, 0), 2)
    #
    # for i in range(len(fit_pointB[0])):
    #     cv2.circle(skeleton_effect, (int(fit_pointB[0][i]), int(fit_pointB[1][i])), 5, (0, 128, 255), -1)
    #     cv2.circle(skeleton_effect, (int(fit_pointB[0][i]), int(fit_pointB[1][i])), 5, (255, 255, 0), 2)
    #
    # for i in range(len(fit_pointC[0])):
    #     cv2.circle(skeleton_effect, (int(fit_pointC[0][i]), int(fit_pointC[1][i])), 5, (0, 128, 255), -1)
    #     cv2.circle(skeleton_effect, (int(fit_pointC[0][i]), int(fit_pointC[1][i])), 5, (255, 255, 0), 2)
    #
    # cv2.polylines(skeleton_effect, [A_points], False, (0, 0, 255), 2)
    # cv2.polylines(skeleton_effect, [B_points], False, (0, 0, 255), 2)
    # cv2.polylines(skeleton_effect, [C_points], False, (0, 0, 255), 2)
    #
    # cv2.imshow('skeleton_effect', skeleton_effect)
    # cv2.waitKey(0)

    # cluster algorithm
    skeleton_effect_gray = cv2.cvtColor(skeleton_effect, cv2.COLOR_BGR2GRAY)
    cnt_ske, _ = cv2.findContours(skeleton_effect_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    data = list()
    img_center_y, img_center_x = skeleton_effect_gray.shape
    img_center_y, img_center_x = img_center_y // 2, img_center_x // 2

    for i in range(len(cnt_ske)):
        for j in range(len(cnt_ske[i])):
            x, y = cnt_ske[i][j][0]
            # dis_A = np.sqrt((x - Ax) ** 2 + (y - Ay) ** 2)
            # dis_B = np.sqrt((x - Bx) ** 2 + (y - By) ** 2)
            # dis_C = np.sqrt((x - Cx) ** 2 + (y - Cy) ** 2)
            # dis_height = y - img_center_y
            data.append([x, y])

    data = np.asarray(data)
    # 標準化
    sd_data = StandardScaler().fit_transform(data)

    # sklearn KMeans
    # model = KMeans(n_clusters=3, n_init=10)
    # model.fit(sd_data)
    # y_pred = model.predict(sd_data)
    # centers = model.cluster_centers_
    # print(f'cluster centers: {centers}')
    # print(f'self centers: {center_points}')
    # plt.title('KMeans clustering result')
    # plt.xlabel('width')
    # plt.ylabel('height')
    # plt.scatter(sd_data[:, 0], sd_data[:, 1], c=y_pred, s=40, cmap='viridis', vmin=np.min(y_pred), vmax=np.max(y_pred))
    # plt.scatter(centers[:, 0], centers[:, 1], s=150, color='red')
    # plt.show()

    # DBSCAN
    # model = DBSCAN(eps=0.15).fit(sd_data)
    # y_pred = model.labels_
    # labels, count = np.unique(y_pred, return_counts=True)
    #
    # # 找出最大值的3個群後把骨架圖分類
    # label_top3 = labels[count.argsort()[::-1][0:3]]
    # center_list = list()
    #
    # kmeans_model = KMeans(n_clusters=1)
    # for label_index in label_top3:
    #     curr_data = data[y_pred == label_index]
    #     kmeans_model.fit_predict(curr_data)
    #     center_list.append(kmeans_model.cluster_centers_[0][1])
    #
    # old_center_list = center_list.copy()
    # center_list.sort()  # 小到大排序
    # index_list = list()  # 由上到下分別為 CBA 三個區段所對應的 label_top3 index
    # for cen in center_list:
    #     index = old_center_list.index(cen)
    #     index_list.append(index)
    #
    # C = data[y_pred == label_top3[index_list[0]]]
    # B = data[y_pred == label_top3[index_list[1]]]
    # A = data[y_pred == label_top3[index_list[2]]]
    #
    # cnt_pointA, fit_pointA = new_fitting(A, 3, 20)
    # cnt_pointB, fit_pointB = new_fitting(B, 3, 15)
    # cnt_pointC, fit_pointC = new_fitting(C, 3, 20)
    #
    # A_points = np.vstack([fit_pointA[0], fit_pointA[1]]).T.astype(np.int)
    # B_points = np.vstack([fit_pointB[0], fit_pointB[1]]).T.astype(np.int)
    # C_points = np.vstack([fit_pointC[0], fit_pointC[1]]).T.astype(np.int)
    #
    # fig, ax = plt.subplots(1, 3)
    # ax[0].set_title('A Region')
    # ax[0].set_xlabel('x')
    # ax[0].set_ylabel('y')
    # ax[0].scatter(cnt_pointA[0], cnt_pointA[1])
    # ax[0].scatter(fit_pointA[0], fit_pointA[1], color='black')
    # ax[0].plot(fit_pointA[0], fit_pointA[1], linewidth=1.5, color='red')
    #
    # ax[1].set_title('B Region')
    # ax[1].set_xlabel('x')
    # ax[1].set_ylabel('y')
    # ax[1].scatter(cnt_pointB[0], cnt_pointB[1])
    # ax[1].scatter(fit_pointB[0], fit_pointB[1], color='black')
    # ax[1].plot(fit_pointB[0], fit_pointB[1], linewidth=1.5, color='red')
    #
    # ax[2].set_title('C Region')
    # ax[2].set_xlabel('x')
    # ax[2].set_ylabel('y')
    # ax[2].scatter(cnt_pointC[0], cnt_pointC[1])
    # ax[2].scatter(fit_pointC[0], fit_pointC[1], color='black')
    # ax[2].plot(fit_pointC[0], fit_pointC[1], linewidth=1.5, color='red')
    #
    # plt.show()
    #
    # for i in range(len(fit_pointA[0])):
    #     cv2.circle(skeleton_effect, (int(fit_pointA[0][i]), int(fit_pointA[1][i])), 5, (0, 128, 255), -1)
    #     cv2.circle(skeleton_effect, (int(fit_pointA[0][i]), int(fit_pointA[1][i])), 5, (255, 255, 0), 2)
    #
    # for i in range(len(fit_pointB[0])):
    #     cv2.circle(skeleton_effect, (int(fit_pointB[0][i]), int(fit_pointB[1][i])), 5, (0, 128, 255), -1)
    #     cv2.circle(skeleton_effect, (int(fit_pointB[0][i]), int(fit_pointB[1][i])), 5, (255, 255, 0), 2)
    #
    # for i in range(len(fit_pointC[0])):
    #     cv2.circle(skeleton_effect, (int(fit_pointC[0][i]), int(fit_pointC[1][i])), 5, (0, 128, 255), -1)
    #     cv2.circle(skeleton_effect, (int(fit_pointC[0][i]), int(fit_pointC[1][i])), 5, (255, 255, 0), 2)
    #
    # cv2.polylines(skeleton_effect, [A_points], False, (0, 0, 255), 2)
    # cv2.polylines(skeleton_effect, [B_points], False, (0, 0, 255), 2)
    # cv2.polylines(skeleton_effect, [C_points], False, (0, 0, 255), 2)
    #
    # cv2.imshow('skeleton_effect', skeleton_effect)
    # cv2.waitKey(0)
    #
    # # vision
    # fig = plt.figure()
    # cluster = fig.add_subplot(121)
    # cluster.set_title('DBSCAN clustering result')
    # cluster.set_xlabel('width')
    # cluster.set_ylabel('height')
    # cluster_result = cluster.scatter(sd_data[:, 0], sd_data[:, 1], c=y_pred, s=40, cmap='viridis')
    # fig.colorbar(cluster_result, ax=cluster)
    #
    # amount = fig.add_subplot(122)
    # amount.set_title('num of clusters')
    # amount.set_xlabel('cluster')
    # amount.set_ylabel('amount')
    # amount.scatter(labels, count, s=40, color='blue')
    # amount.plot(labels, count, '-r', color='red')
    #
    # plt.show()

    # ----- 2. matching 骨架圖找出 key points Wait

    # 3. 根據 key points 找出 Valve 位置
    # 從 M-Mode 角度出發
    # 定義 MV 位置範圍
    # 點範圍
    B_dx = 75
    # mv_C_points = C_points[(C_points[:, 0] >= B_points[0, 0] - B_dx) & (C_points[:, 0] <= B_points[2, 0])]
    mv_B_points = B_points[:3]
    mv_A_points = A_points[(A_points[:, 0] >= B_points[0, 0] - B_dx) & (A_points[:, 0] <= B_points[2, 0])]

    # 矩形範圍
    mv_lx, mv_ly = min(mv_A_points[:, 0]), min(mv_B_points[:, 1]) - 10
    mv_rx, mv_ry = max(mv_B_points[:, 0]), max(mv_A_points[:, 1])
    # print(mv_lx, mv_ly, mv_rx, mv_ry)

    # 定義 LV 位置範圍
    # 點範圍
    lv_C_points = C_points[(C_points[:, 0] < B_points[0, 0])]
    lv_A_points = A_points[(A_points[:, 0] < B_points[0, 0] - B_dx)]

    # 矩形範圍
    # 採用四分位距Q50 (C 區段為主)
    center_point = lv_C_points[len(lv_C_points) // 2]
    lv_lx, lv_ly = center_point[0] - 30, min(lv_C_points[:, 1]) - 40
    lv_rx, lv_ry = center_point[0] + 30, max(lv_C_points[:, 1]) + 40

    # 定義 LA & Aortic 位置範圍
    la_B_points = B_points[3:]
    la_A_points = A_points[(A_points[:, 0] > B_points[2, 0])]
    la_C_points = C_points[(C_points[:, 0] >= B_points[0, 0])]

    # 矩形範圍(全採用)
    la_lx, la_ly = min(la_C_points[:, 0]), min(la_C_points[:, 1])
    la_rx, la_ry = max(la_B_points[:, 0]), max(la_B_points[:, 1])

    frame_list = list()
    while video.ret:
        frame = video.get_frame()

        if not video.ret:
            break

        frame[mask_roi != 255] = [0, 0, 0]
        frame_effect = frame[top:bottom, left:right]

        #

        # 繪製範圍位置
        # 圓心
        cv2.circle(frame, (ox, oy), 10, (255, 255, 0), -1)

        # MV
        for i in range(len(mv_A_points)):
            cv2.circle(frame_effect, (mv_A_points[i, 0], mv_A_points[i, 1]), 5, (0, 255, 255), -1)

        for i in range(len(mv_B_points)):
            cv2.circle(frame_effect, (mv_B_points[i][0], mv_B_points[i][1]), 5, (0, 255, 255), -1)

        # for i in range(len(mv_C_points)):
        #     cv2.circle(frame_effect, (mv_C_points[i][0], mv_C_points[i][1]), 5, (0, 255, 255), -1)

        cv2.rectangle(frame_effect, (mv_lx, mv_ly), (mv_rx, mv_ry), (0, 255, 255), 2)

        # LV
        for i in range(len(lv_C_points)):
            cv2.circle(frame_effect, (lv_C_points[i, 0], lv_C_points[i, 1]), 5, (0, 0, 255), -1)

        for i in range(len(lv_A_points)):
            cv2.circle(frame_effect, (lv_A_points[i][0], lv_A_points[i][1]), 5, (0, 0, 255), -1)

        cv2.rectangle(frame_effect, (lv_lx, lv_ly), (lv_rx, lv_ry), (0, 0, 255), 2)

        # LA & Aortic
        for i in range(len(la_B_points)):
            cv2.circle(frame_effect, (la_B_points[i, 0], la_B_points[i, 1]), 5, (255, 0, 255), -1)

        for i in range(len(la_A_points)):
            cv2.circle(frame_effect, (la_A_points[i][0], la_A_points[i][1]), 5, (255, 0, 255), -1)

        for i in range(len(la_C_points)):
            cv2.circle(frame_effect, (la_C_points[i][0], la_C_points[i][1]), 5, (255, 0, 255), -1)

        cv2.rectangle(frame_effect, (la_lx, la_ly), (la_rx, la_ry), (255, 0, 255), 2)

        frame[top:bottom, left:right] = frame_effect
        frame_list.append(frame)
        cv2.imshow('fe', frame_effect)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
    write_video(frame_list, './curr/' + file_name)
    # ----- 3.
