import matplotlib.pyplot as plt
from VideoInitialization import *
from sklearn.cluster import KMeans
import numpy as np
import cv2


def handle_bug(output_path, reason, img=None):
    txt_path = 'E:/MyProgramming/Python/Project/implement/heart recognize/Segmentation/A4C Valve All/' \
               'bug dir/bug_reason.txt'

    with open(txt_path, 'a+') as f:
        f.write(f'FileName: {FileName} \n')
        f.write(f'Reason: {reason} \n')

    if isinstance(img, np.ndarray):
        cv2.imwrite(output_path, img)


def write_video(frames_list, output_path):
    y, x, _ = frames_list[0].shape
    video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), 30, (x, y))
    for i in frames_list:
        video_writer.write(i)
    video_writer.release()


def anomaly_detection(ChamberDict, centroid):
    # 若一個腔室內大於一個點, 則找出所有點的中心點當成標準
    # 先用 ConvexHull 做, 不行再用 距離公式

    # - 處理同個腔室內多個點的情況
    not_exist = list()
    for Chamber in ChamberDict.keys():
        if len(ChamberDict[Chamber]) > 1:
            if len(ChamberDict[Chamber]) == 2:
                x1, y1 = ChamberDict[Chamber][0]
                x2, y2 = ChamberDict[Chamber][1]
                ChamberDict[Chamber] = ((x2 - x1) // 2 + x1, (y2 - y1) // 2 + y1)

            else:
                L = np.asarray(ChamberDict[Chamber])
                Hull = cv2.convexHull(L)
                Hull_M = cv2.moments(Hull)
                ChamberDict[Chamber] = (int(Hull_M["m10"] / Hull_M["m00"]), int(Hull_M["m01"] / Hull_M["m00"]))

        elif len(ChamberDict[Chamber]) == 1:
            ChamberDict[Chamber] = (ChamberDict[Chamber][0][0], ChamberDict[Chamber][0][1])

        else:
            not_exist.append(Chamber)
    # - 處理同個腔室內多個點的情況 End.

    # - 處理該腔室不存在問題(用質心點代替)
    for non_pos in not_exist:
        ChamberDict[non_pos] = centroid[non_pos]
    # - 處理該腔室不存在問題 End.

    # - 處理腔室中心點過於中心的問題
    # for near_pos in not_exist:
    #     if near_pos == "LA":
    #         LV_x, LV_y = ChamberDict["LV"]
    #         LA_x, LA_y = ChamberDict["LA"]
    #
    #         Centroid_LV_x, Centroid_LV_y = Centroid["LV"]
    #         LV_dis = np.sqrt((LV_x - Centroid_LV_x) ** 2 + (LV_y - Centroid_LV_y) ** 2)
    #         LA_LV_dis = np.sqrt((LV_x - LA_x) ** 2 + (LV_y - LA_y) ** 2)
    #         if LV_dis > LA_LV_dis * 0.25:
    #             ChamberDict["LV"] = (Centroid_LV_x, Centroid_LV_y)
    #
    #     elif near_pos == "LV":
    #         LV_x, LV_y = ChamberDict["LV"]
    #         LA_x, LA_y = ChamberDict["LA"]
    #
    #         Centroid_LA_x, Centroid_LA_y = Centroid["LA"]
    #         LA_dis = np.sqrt((LA_x - Centroid_LA_x) ** 2 + (LA_y - Centroid_LA_y) ** 2)
    #         LA_LV_dis = np.sqrt((LV_x - LA_x) ** 2 + (LV_y - LA_y) ** 2)
    #         if LA_dis > LA_LV_dis * 0.25:
    #             ChamberDict["LA"] = (Centroid_LA_x, Centroid_LA_y)
    #
    #     elif near_pos == "RV":
    #         RV_x, RV_y = ChamberDict["RV"]
    #         RA_x, RA_y = ChamberDict["RA"]
    #
    #         Centroid_RA_x, Centroid_RA_y = Centroid["RA"]
    #         RA_dis = np.sqrt((RA_x - Centroid_RA_x) ** 2 + (RA_y - Centroid_RA_y) ** 2)
    #         RA_RV_dis = np.sqrt((RV_x - RA_x) ** 2 + (RV_y - RA_y) ** 2)
    #         if RA_dis > RA_RV_dis * 0.25:
    #             ChamberDict["RA"] = (Centroid_RA_x, Centroid_RA_y)
    #
    #     elif near_pos == "RA":
    #         RV_x, RV_y = ChamberDict["RV"]
    #         RA_x, RA_y = ChamberDict["RA"]
    #
    #         Centroid_RV_x, Centroid_RV_y = Centroid["RV"]
    #         RV_dis = np.sqrt((RV_x - Centroid_RV_x) ** 2 + (RV_y - Centroid_RV_y) ** 2)
    #         RA_RV_dis = np.sqrt((RV_x - RA_x) ** 2 + (RV_y - RA_y) ** 2)
    #         if RV_dis > RA_RV_dis * 0.25:
    #             ChamberDict["RV"] = (Centroid_RV_x, Centroid_RV_y)
    # - 處理腔室中心點過於中心的問題 End.

    return ChamberDict


def handle_model(model_path):
    Model = cv2.imread(model_path)
    Model = cv2.cvtColor(Model, cv2.COLOR_BGR2GRAY)
    _, Model = cv2.threshold(Model, 180, 255, cv2.THRESH_BINARY)
    cnt_Model, _ = cv2.findContours(Model, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    left = np.min(cnt_Model[0][:, 0, 0])
    right = np.max(cnt_Model[0][:, 0, 0])
    upper = np.min(cnt_Model[0][:, 0, 1])
    lower = np.max(cnt_Model[0][:, 0, 1])

    cv2.imshow('Model', Model)
    pass


# InputDir
# InputDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\All Classification_avi" \
#            "\\0002_Apical Four Chamber\\"
InputDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\Segmentation\\A4C Test Video\\"

VideoPath = AllFiles(InputDir, 'avi')

SkeletonizeDir = 'E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\classified data_png' \
                 '\\0002_Apical Four Chamber\\'

ModelPath = "L:\\Lab_Data\\model\\0002_Apical four chamber.png"
# handle_model(ModelPath)

OutputDir = 'E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\Segmentation\\A4C semantic 1210\\'

OutputBugDir = 'E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\Segmentation\\A4C Valve 1207\\bug dir\\'
TextFont = cv2.FONT_HERSHEY_COMPLEX_SMALL

for path in VideoPath[0:1]:
    init = VideoInit(path)
    FileName = path.split('\\')[-1]
    print(f'FileName: {FileName}')

    # 讀取骨架圖
    x_bound, y_bound = list(), list()
    try:
        skeletonize_path = SkeletonizeDir + FileName + '.png'
        skeleton = cv2.imread(skeletonize_path)

    except cv2.error:
        rea = 'cv2.error: 沒有該檔案的骨架圖'
        handle_bug(OutputBugDir + FileName, reason=rea)
        continue

    gray_skeleton = cv2.cvtColor(skeleton, cv2.COLOR_BGR2GRAY)
    gray_skeleton[init.roi != 255] = 0

    cnt, _ = cv2.findContours(gray_skeleton, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(cnt)):
        for j in range(len(cnt[i])):
            x_bound.append(cnt[i][j][0][0])
            y_bound.append(cnt[i][j][0][1])

    try:
        x = (max(x_bound) + min(x_bound)) / 2
        y = (max(y_bound) + min(y_bound)) / 2
        rad_x = (max(x_bound) - min(x_bound)) / 2
        rad_y = (max(y_bound) - min(y_bound)) / 2

        radius = int(rad_x + 10 if rad_x > rad_y else rad_y + 10)
        center = (int(x), int(y))

        left_B = int(x) - radius
        top_B = int(y) + radius
        right_B = int(x) + radius
        bottom_B = int(y) - radius

        area_ADD = cv2.morphologyEx(gray_skeleton, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)))
        t = gray_skeleton.ravel()

        if t.max() < 100:
            continue

        else:
            cnt, _ = cv2.findContours(area_ADD, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            hull = list()

            for i in range(len(cnt)):
                for j in range(len(cnt[i])):
                    hull.append(cnt[i][j])

            hull = np.asarray(hull)
            hull = cv2.convexHull(hull)

            bound = np.zeros((600, 800), np.uint8)
            car_bound = np.zeros((600, 800), np.uint8)

            cv2.drawContours(bound, [hull], 0, (255, 255, 255), -1)
            bound = cv2.erode(bound, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)), iterations=9)
            cnt_B, _ = cv2.findContours(bound, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(car_bound, cnt_B, 0, (255, 255, 255), -1)
            cnt_car_bound, _ = cv2.findContours(car_bound, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            M = cv2.moments(cnt_car_bound[0])
            cb_cen_x, cb_cen_y = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            # print(f'cb cen x, cb cen y: {cb_cen_x, cb_cen_y}')

    except ValueError:
        rea = f'ValueError: 骨架圖可能為全黑的'
        cv2.putText(skeleton, 'The skeleton image may be completely black', (100, 100), TextFont, 1, (255, 255, 255), 1)
        handle_bug(OutputBugDir + FileName + '.png', reason=rea, img=skeleton)
        continue

    center_pts = list()
    mask_center = np.zeros((600, 800), np.uint8)

    while True:
        ret, frame = init.video.read()

        if not ret:
            break

        frame[init.roi != 255] = [0, 0, 0]
        median = cv2.medianBlur(frame, 19)
        img_bl = cv2.blur(frame, (17, 17))

        gray_median = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
        gray_median[init.roi != 255] = 0

        # handle
        # distance transform
        thres = cv2.adaptiveThreshold(gray_median, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 221, 7)
        thres[init.roi != 255] = 0
        _, thres_inv = cv2.threshold(thres, 120, 255, cv2.THRESH_BINARY_INV)
        thres_inv[init.roi != 255] = 0

        dist_cb = cv2.distanceTransform(thres_inv, cv2.DIST_L1, 3)
        dist_ms = cv2.distanceTransform(thres, cv2.DIST_L1, 3)

        cv2.normalize(dist_cb, dist_cb, 0, 1.0, cv2.NORM_MINMAX)
        cv2.normalize(dist_ms, dist_ms, 0, 1.0, cv2.NORM_MINMAX)

        _, dist = cv2.threshold(dist_cb, 0.6, 255, cv2.THRESH_BINARY)
        dist = np.uint8(dist)
        dist[car_bound != 255] = 0

        # cv2.circle(frame, (cb_cen_x, cb_cen_y), 5, (0, 0, 255), -1)

        # center
        cnt_center, _ = cv2.findContours(dist, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnt_center:
            area = cv2.contourArea(c)

            R = np.random.randint(120, 255)
            G = np.random.randint(120, 255)
            B = np.random.randint(120, 255)

            if area > 10:
                c_hull = cv2.convexHull(c)
                x, y, w, h = cv2.boundingRect(c_hull)
                cen_x, cen_y = int(x+w/2), int(y+h/2)

                # feature (新增特徵維度去解決分類問題)
                width_diff = cb_cen_x - cen_x
                height_diff = cb_cen_y - cen_y
                feature = [height_diff, width_diff, cen_x, cen_y]
                center_pts.append(feature)
                cv2.circle(median, (cen_x, cen_y), 5, (B, G, R), -1)
                cv2.circle(mask_center, (cen_x, cen_y), 5, (255, 255, 255), -1)

        # cv2.imshow('median', median)
        # cv2.imshow('frame', frame)
        # cv2.imshow('mask center', mask_center)
        # cv2.waitKey(10)

    # handle center data
    # use KMeans
    center_pts = np.asarray(center_pts)

    # 區分上下左右
    try:
        Xdata, Ydata = center_pts[:, :3], center_pts[:, 3]
        kmeans = KMeans(n_clusters=4, n_init=10)
        kmeans.fit(Xdata, Ydata)
        Ypred = kmeans.predict(Xdata)

    except IndexError:
        rea = 'IndexError: 統計腔室中心點有問題, 檢查該影片 distance transform 的過程'
        handle_bug(OutputBugDir + FileName, reason=rea)
        continue

    # visualize
    cluster_mask = np.zeros((600, 800, 3), np.uint8)
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (255, 255, 0)]
    for index, p in enumerate(Ypred):
        coord = center_pts[index][2:]
        cv2.circle(cluster_mask, (coord[0], coord[1]), 5, colors[p], -1)
    cv2.circle(cluster_mask, (cb_cen_x, cb_cen_y), 5, (255, 0, 255), -1)

    # position
    cluster_center = kmeans.cluster_centers_
    # print(f'cluster center: {cluster_center}')

    # 利用 質心中心 定位
    all_center = np.zeros((4, 2), np.int)
    for pos, cluster_c in enumerate(cluster_center):
        dy, dx, cluster_x = int(cluster_c[0]), int(cluster_c[1]), int(cluster_c[2])

        # 利用距離最小值找到最接近質心的點當成每個腔室的定位點
        minimum_dis = np.sqrt((center_pts[0][0] - dy) ** 2 + (center_pts[0][2] - cluster_x) ** 2)
        minimum_index = 0
        for i, feature in enumerate(center_pts):
            distance = np.sqrt((feature[0] - dy) ** 2 + (feature[2] - cluster_x) ** 2)
            if distance < minimum_dis:
                minimum_index = i
                minimum_dis = distance
        cluster_y = Ydata[minimum_index]

        cv2.circle(cluster_mask, (cluster_x, cluster_y), 10, colors[4], -1)
        all_center[pos] = [cluster_x, cluster_y]

    # 這裡先假設四個點一定在四個腔室
    # Q. 如果 Kmeans 分類的效果不好, 就會有問題; 要處理
    Centroid = {}
    try:
        RightChamber = all_center[np.where(all_center[:, 0] < cb_cen_x)[0]]
        LeftChamber = all_center[np.where(all_center[:, 0] > cb_cen_x)[0]]

        LA_center = LeftChamber[np.where(LeftChamber[:, 1] == np.max(LeftChamber[:, 1]))[0]][0]
        LV_center = LeftChamber[np.where(LeftChamber[:, 1] == np.min(LeftChamber[:, 1]))[0]][0]
        RA_center = RightChamber[np.where(RightChamber[:, 1] == np.max(RightChamber[:, 1]))[0]][0]
        RV_center = RightChamber[np.where(RightChamber[:, 1] == np.min(RightChamber[:, 1]))[0]][0]
        Centroid["LV"] = tuple(LV_center)
        Centroid["LA"] = tuple(LA_center)
        Centroid["RV"] = tuple(RV_center)
        Centroid["RA"] = tuple(RA_center)

    except ValueError:
        rea = 'ValueError: 無法找到四個腔室中心, 檢查 Kmeans 結果'
        cv2.putText(cluster_mask, 'Kmeans Result', (100, 100), TextFont, 1, (255, 255, 255), 1)
        handle_bug(OutputBugDir + FileName + ' cluster.png', reason=rea, img=cluster_mask)
        continue
    # cv2.putText(cluster_mask, f'{FileName}', (100, 100), TextFont, 1, (255, 255, 255), 1)

    # cv2.imshow('cluster', cluster_mask)
    # cv2.waitKey(500)
    # ----- 取得腔室的四個中心點位置

    # 再讀取一次影片
    re_video = cv2.VideoCapture(path)
    # 定義顏色
    ChamberColors = [(255, 0, 255), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # LV, LA, RV, RA
    frame_list = list()
    frame_count = 0

    Tot_ChamberCenter = {"LV": [], "LA": [], "RV": [], "RA": []}

    while True:
        ret, frame = re_video.read()

        if not ret:
            break

        frame_count += 1
        frame[init.roi != 255] = [0, 0, 0]
        frame_draw = frame.copy()  # 繪製文字需要

        median = cv2.medianBlur(frame, 19)
        img_bl = cv2.blur(frame, (17, 17))

        gray_median = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
        gray_median[init.roi != 255] = 0

        # handle
        # distance transform
        thres = cv2.adaptiveThreshold(gray_median, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 221, 7)
        thres[init.roi != 255] = 0
        _, thres_inv = cv2.threshold(thres, 120, 255, cv2.THRESH_BINARY_INV)
        thres_inv[init.roi != 255] = 0

        dist_cb = cv2.distanceTransform(thres_inv, cv2.DIST_L1, 3)
        dist_ms = cv2.distanceTransform(thres, cv2.DIST_L1, 3)

        cv2.normalize(dist_cb, dist_cb, 0, 1.0, cv2.NORM_MINMAX)
        cv2.normalize(dist_ms, dist_ms, 0, 1.0, cv2.NORM_MINMAX)

        _, dist = cv2.threshold(dist_cb, 0.6, 255, cv2.THRESH_BINARY)
        dist = np.uint8(dist)
        dist[car_bound != 255] = 0

        # center, 先暴力處理, 最後再優化
        cnt_center, _ = cv2.findContours(dist, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        curr_center = {"LV": [], "LA": [], "RV": [], "RA": []}

        for c in cnt_center:
            area = cv2.contourArea(c)

            if area > 10:
                c_hull = cv2.convexHull(c)
                x, y, w, h = cv2.boundingRect(c_hull)
                cen_x, cen_y = int(x+w/2), int(y+h/2)

                # 改用距離判斷
                LV_distance = np.sqrt((cen_x - LV_center[0]) ** 2 + (cen_y - LV_center[1]) ** 2)
                LA_distance = np.sqrt((cen_x - LA_center[0]) ** 2 + (cen_y - LA_center[1]) ** 2)
                RV_distance = np.sqrt((cen_x - RV_center[0]) ** 2 + (cen_y - RV_center[1]) ** 2)
                RA_distance = np.sqrt((cen_x - RA_center[0]) ** 2 + (cen_y - RA_center[1]) ** 2)
                dis_list = [LV_distance, LA_distance, RV_distance, RA_distance]
                min_i = dis_list.index(min(dis_list))

                if min_i == 0:
                    curr_center["LV"].append([cen_x, cen_y])

                elif min_i == 1:
                    curr_center["LA"].append([cen_x, cen_y])

                elif min_i == 2:
                    curr_center["RV"].append([cen_x, cen_y])

                elif min_i == 3:
                    curr_center["RA"].append([cen_x, cen_y])

        frame_line = frame.copy()
        frame_mv = frame.copy()

        # 異常檢測
        try:
            ChamberDicts = anomaly_detection(curr_center, Centroid)
            Tot_ChamberCenter["LV"].append(ChamberDicts["LV"])
            Tot_ChamberCenter["LA"].append(ChamberDicts["LA"])
            Tot_ChamberCenter["RV"].append(ChamberDicts["RV"])
            Tot_ChamberCenter["RA"].append(ChamberDicts["RA"])

        except ZeroDivisionError:
            rea = 'ZeroDivisionError: 異常檢測的 ConvexHull 求中心點座標狀況'
            handle_bug(OutputBugDir + FileName, reason=rea)
            continue

        cv2.putText(frame_draw, 'LV', ChamberDicts["LV"], TextFont, 1, ChamberColors[0], 1)
        cv2.putText(frame_draw, 'LA', ChamberDicts["LA"], TextFont, 1, ChamberColors[1], 1)
        cv2.putText(frame_draw, 'RV', ChamberDicts["RV"], TextFont, 1, ChamberColors[2], 1)
        cv2.putText(frame_draw, 'RA', ChamberDicts["RA"], TextFont, 1, ChamberColors[3], 1)
        cv2.putText(frame_draw, f'frame count: {frame_count}', (100, 100), TextFont, 1, (255, 255, 255), 1)
        frame_list.append(frame_draw)

    # 可視化 3D
    # print(Tot_ChamberCenter)
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # Colors = [
    #     ['red', 'blue', 'chocolate'],
    #     ['aqua', 'green', 'darkblue'],
    #     ['orange', 'purple', 'steelblue'],
    #     ['gray', 'violet', 'tomato']
    # ]
    #
    # for color_ind, keys in enumerate(Tot_ChamberCenter.keys()):
    #     Data = np.asarray(Tot_ChamberCenter[keys])
    #     X_Data, Y_Data = Data[:, 0], Data[:, 1]
    #     ax.scatter(X_Data, Y_Data, range(1, len(X_Data)+1),
    #                color=Colors[color_ind][0], s=10, label=keys + ' Curr Center')
    #     ax.plot(X_Data, Y_Data, range(1, len(X_Data)+1), color=Colors[color_ind][1], label=keys)
    #     ax.plot([Centroid[keys][0]] * len(X_Data), [Centroid[keys][1]] * len(X_Data), range(1, len(X_Data)+1),
    #             color=Colors[color_ind][2], label=keys + ' Centroid')
    #
    # plt.xlabel('X Coord')
    # plt.ylabel('Y Coord')
    # plt.title('Z: Frame Count')
    # plt.legend()
    # plt.savefig(OutputDir + FileName + ' .png')
    # plt.show()

        # # 最後找瓣膜位置(先處理 MV)
        # mask_line = np.zeros((600, 800), np.uint8)
        # mask_skeleton_line = np.zeros((600, 800), np.uint8)
        # skeleton_line = skeleton.copy()
        #
        # # LA, LV Line
        # cv2.line(frame_draw, ChamberDicts["LV"], ChamberDicts["LA"], (255, 0, 0), 2)
        # cv2.line(mask_line, ChamberDicts["LV"], ChamberDicts["LA"], (255, 255, 255), 1)
        #
        # frame_line[mask_line != 255] = [0, 0, 0]
        # gray_line = cv2.cvtColor(frame_line, cv2.COLOR_BGR2GRAY)
        #
        # # 找出灰階值最高的位置
        # # 限制搜索範圍(以高度來分四分位距, 不考慮距離)
        # la_cen_x, la_cen_y = ChamberDicts["LA"]
        # lv_cen_x, lv_cen_y = ChamberDicts["LV"]
        #
        # Q25 = (la_cen_y - lv_cen_y) // 4 + lv_cen_y
        # Q75 = la_cen_y - (la_cen_y - lv_cen_y) // 4
        # gray_line[:Q25, :] = 0
        # gray_line[Q75:, :] = 0
        # # print(f'Q25: {Q25}, Q75: {Q75}')
        #
        # # 之後可以換成先找最大值, 再用 np.where 來取座標
        # max_pos = np.argmax(gray_line)  # 線上最高點的位置 <- 1D
        # max_pos_y, max_pos_x = max_pos // 800 + 1, max_pos % 800  # 轉成 2D 座標(原本 1D 是水平展開, 因此除以 width)
        # # print(f'x, y: {max_pos_x, max_pos_y}')
        # cv2.circle(frame_draw, (max_pos_x, max_pos_y), 5, (255, 0, 255), -1)
        #
        # # 直線方程式, 找出垂直於 LA_LV 線的方程式
        # try:
        #     # 若分母為 0, 則該線為 90 度, 直接畫水平線即可
        #     mLA_LV = (la_cen_y - lv_cen_y) / (la_cen_x - lv_cen_x + 1e-8)
        #     m_vertical = - 1 / mLA_LV  # 負斜率
        #     # print(f'm: {mLA_LV}, x1, y1: {max_pos_x, max_pos_y}')
        #
        #     # 假設從 邊界開始畫(x=0, x=800)
        #     if m_vertical is np.nan:
        #         left_bound, right_bound = 0, 800
        #
        #     else:
        #         left_bound = int(m_vertical * (- max_pos_x) + max_pos_y)
        #         right_bound = int(m_vertical * (800 - max_pos_x) + max_pos_y)
        #
        #     # cv2.line(frame, (0, left_bound), (800, right_bound), (0, 255, 0), 2)
        #     cv2.line(mask_skeleton_line, (0, left_bound), (800, right_bound), (255, 255, 255), 1)
        #     cv2.line(skeleton_line, (0, left_bound), (800, right_bound), (0, 255, 0), 1)
        #     # cv2.line(skeleton_line, (lv_cen_x, lv_cen_y), (la_cen_x, la_cen_y), (0, 0, 255), 2)
        #
        # except ZeroDivisionError:
        #     cv2.line(mask_skeleton_line, (0, max_pos_y), (800, max_pos_y), (255, 255, 255), 1)
        #     cv2.line(skeleton_line, (0, max_pos_y), (800, max_pos_y), (0, 255, 0), 1)
        #
        # # 利用骨架圖找垂直線的邊界
        # gray_skeleton_line = cv2.cvtColor(skeleton_line, cv2.COLOR_BGR2GRAY)
        # gray_skeleton_line[gray_skeleton_line > 0] = 255
        #
        # kernel = np.ones((3, 3))
        # gray_skeleton_line = cv2.morphologyEx(gray_skeleton_line, cv2.MORPH_CLOSE, kernel, iterations=1)
        # # cv2.imshow('gray skeleton', gray_skeleton_line)
        #
        # gray_skeleton_line[mask_skeleton_line != 255] = 0
        # ske_pos_y, ske_pos_x = np.where(gray_skeleton_line == 255)
        #
        # # 找離中心點較近的點
        # left_nearest_distance, right_nearest_distance = 800, 800
        # left_nearest_index, right_nearest_index = 0, -1
        #
        # for n_index, n in enumerate(ske_pos_y):
        #     # left
        #     if ske_pos_x[n_index] < max_pos_x:
        #         left_distance = np.sqrt((max_pos_x - ske_pos_x[n_index]) ** 2 + (max_pos_y - n) ** 2)
        #
        #         # 至少大於 40 pixel
        #         if 40 < left_distance < left_nearest_distance:
        #             left_nearest_distance = left_distance
        #             left_nearest_index = n_index
        #
        #     # right
        #     if ske_pos_x[n_index] >= max_pos_x:
        #         right_distance = np.sqrt((max_pos_x - ske_pos_x[n_index]) ** 2 + (max_pos_y - n) ** 2)
        #
        #         # 至少大於 50 pixel
        #         if 50 < right_distance < right_nearest_distance:
        #             right_nearest_distance = right_distance
        #             right_nearest_index = n_index
        #
        # cv2.circle(skeleton_line, (ske_pos_x[left_nearest_index], ske_pos_y[left_nearest_index]), 5, (255, 0, 255), -1)
        # cv2.circle(skeleton_line, (ske_pos_x[right_nearest_index], ske_pos_y[right_nearest_index]), 5, (255, 0, 255), -1)
        # # cv2.circle(frame_draw, (ske_pos_x[left_nearest_index] - 12, ske_pos_y[left_nearest_index] - 5), 5, (255, 0, 255), -1)
        # # cv2.circle(frame_draw, (ske_pos_x[right_nearest_index] + 12, ske_pos_y[right_nearest_index] + 5), 5, (255, 0, 255), -1)
        #
        # mv_x = [min(ske_pos_x[left_nearest_index], ske_pos_x[right_nearest_index]),
        #         max(ske_pos_x[left_nearest_index], ske_pos_x[right_nearest_index])]
        # mv_y = [min(ske_pos_y[left_nearest_index], ske_pos_y[right_nearest_index]),
        #         max(ske_pos_y[left_nearest_index], ske_pos_y[right_nearest_index])]
        #
        # # 將矩形範圍抓出來做處理
        # # 先暫時用定值調整矩形框大小
        # mask_mv_bound = np.zeros(frame_mv.shape[:2], np.uint8)
        #
        # mv_x = [mv_x[0] - 12, mv_x[1] + 12]
        # mv_y = [mv_y[0] - 5, mv_y[1] + 5]
        #
        # if max(mv_y) - min(mv_y) < 20:
        #     # 若高度差距太小, 則再上下 10 pixel
        #     mv_y[0] -= 10
        #     mv_y[1] += 10
        #
        # cv2.rectangle(frame_draw, (mv_x[0], mv_y[0]), (mv_x[1], mv_y[1]), (255, 50, 200), 2)
        # frame_mv = frame_mv[mv_y[0]:mv_y[1], mv_x[0]:mv_x[1]]
        # mask_mv_bound[mv_y[0]:mv_y[1], mv_x[0]:mv_x[1]] = 255
        #
        # # 以平均值做二值化
        # try:
        #     gray_mv = cv2.cvtColor(frame_mv, cv2.COLOR_BGR2GRAY)
        #
        # except cv2.error:
        #     rea = 'cv2.error: 無法圈出矩形框, 檢查矩形範圍'
        #     cv2.putText(skeleton_line, f'frame count: {frame_count}', (100, 100), TextFont, 1, (255, 255, 255), 1)
        #     handle_bug(OutputBugDir + FileName + f' {frame_count}.png', reason=rea, img=skeleton_line)
        #     continue
        #
        # avg = cv2.mean(gray_mv)[0]
        # _, mv_thres = cv2.threshold(gray_mv, avg, 255, cv2.THRESH_BINARY)
        #
        # # 使用 np.polyfit() 找出擬合曲線
        # mv_pos_y_full, mv_pos_x_full = np.where(mv_thres == 255)
        # mv_pos_x_full += mv_x[0]
        # mv_pos_y_full += mv_y[0]
        #
        # fit_model = np.polyfit(mv_pos_x_full, mv_pos_y_full, 2)
        # fit_model = np.poly1d(fit_model)
        # x_new_pt = np.arange(mv_x[0], mv_x[1], 2)
        # y_new_pt = fit_model(x_new_pt)
        #
        # for pt_i in range(len(x_new_pt)):
        #     try:
        #         if mask_mv_bound[int(y_new_pt[pt_i]), int(x_new_pt[pt_i])] == 255:
        #             cv2.circle(frame_draw, (int(x_new_pt[pt_i]), int(y_new_pt[pt_i])), 2, (192, 255, 192), -1)
        #
        #     except IndexError:
        #         rea = 'IndexError: 擬合曲線時, x or y 超過圖像的範圍, 採用定值的影響'
        #         handle_bug(OutputBugDir + FileName, reason=rea)
        #         continue

            # cv2.imshow('mv_thres', mv_thres)
            # cv2.imshow('frame_mv', frame_mv)

        # frame_list.append(frame_draw)
        # cv2.imshow('frame', frame)
        # cv2.imshow('frame_draw', frame_draw)
        # cv2.imshow('skeleton', skeleton_line)
        # cv2.waitKey(1)

    OutputPath = OutputDir + 'v1' + FileName
    write_video(frame_list, OutputPath)
    pass