from VideoInit_ROI import *
from Multi_Threshold import *
from sklearn.cluster import KMeans
from itertools import combinations
import numpy as np
import cv2
import time


# 最後寫成 class Kmeans 自成一類

def handle_bug(output_path, reason, img=None):
    txt_path = 'E:/MyProgramming/Python/Project/implement/heart recognize/Segmentation/A4C semantic 1210/' \
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


def KmeansCluster(ClusterData):
    if len(ClusterData) != 0:
        # First classification
        ClusterData = np.asarray(ClusterData)
        FeatureData, YData = ClusterData[:, :-1], ClusterData[:, -1]
        kmeans = KMeans(n_clusters=4, n_init=10)
        kmeans.fit(FeatureData, YData)
        YPred = kmeans.predict(FeatureData)

        # - 取出 Kmeans 的質心位置
        Cluster_Centers = kmeans.cluster_centers_

        Centroid_pts = list()
        for cluster_index, feature in enumerate(Cluster_Centers):
            dx, dy, angle, Xpoint = feature

            # 改用 dx, dy 去抓質心位置(沒有差太多, 而且相對來說角度較準)
            Xpt = int(cb_cen_x + dx)
            Ypt = int(cb_cen_y + dy)
            Centroid_pts.append((Xpt, Ypt))
        # - 取出 Kmeans 的質心位置 End.
    else:
        reason = 'IndexError: 統計腔室中心點有問題, 檢查該影片 distance transform 的過程'
        handle_bug(OutputBugDir + FileName, reason=reason)
        raise IndexError

    return KmeansAnomalyDetection(
        ClusterFeature=Cluster_Centers,
        CentroidList=Centroid_pts,
        OriginalData=ClusterData,
        firstPred=YPred
    )


def ReKmeans(data):
    xdata, ydata = data[:, :-1], data[:, -1]
    kmeans2 = KMeans(n_clusters=2, n_init=6)
    kmeans2.fit(xdata, ydata)
    ypred = kmeans2.predict(xdata)
    # --- 利用 Kmeans 區分四個腔室 End.

    # --- 定義質心位置
    Cluster_Centers2 = kmeans2.cluster_centers_

    Centroid_pts2 = list()
    for _feature in Cluster_Centers2:
        _dx, _dy, _angle, _ = _feature
        xpt = int(cb_cen_x + _dx)
        ypt = int(cb_cen_y + _dy)
        Centroid_pts2.append((xpt, ypt))

    # --- 定義質心位置
    return Centroid_pts2, ypred


def KmeansAnomalyDetection(ClusterFeature, CentroidList, OriginalData, firstPred):
    adjust_Centroid = {"LV": (), "LA": (), "RV": (), "RA": ()}
    FeatureDim = OriginalData.shape[1] - 1

    # 由於第一次分類是以 4 個特徵下去做, 接著分類時採用 3 個特徵組合 & 再一次 4 個特徵(緩)
    # FeatureCombine = list(combinations(range(0, FeatureDim), 3))
    # if len(FeatureCombine) > 0:
    #     FeatureCombine.append(tuple(range(0, FeatureDim)))  # 4 個特徵

    OutputPath = OutputDir + FileName
    mask_kmeans1 = np.zeros((600, 800, 3), np.uint8)
    mask_kmeans2 = np.zeros((600, 800, 3), np.uint8)

    # --- 根據 4 個質心位置 繪製四邊形找出四邊形中心
    CentroidList = np.asarray(CentroidList)
    quadrilateral = cv2.convexHull(CentroidList)
    quadM = cv2.moments(quadrilateral)
    quad_x, quad_y = int(quadM["m10"] / quadM["m00"]), int(quadM["m01"] / quadM["m00"])

    # - visualization
    # draw data
    # colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 192)]
    # for pred in firstPred:
    #     curr_cluster_data = OriginalData[firstPred == pred]
    #
    #     for index in range(len(curr_cluster_data[:, -2:])):
    #         coordX, coordY = curr_cluster_data[index][-2:].astype(np.int)
    #         cv2.circle(mask_kmeans1, (coordX, coordY), 5, colors[pred], -1)
    #
    # # line
    # cv2.drawContours(mask_kmeans1, [quadrilateral], -1, (255, 0, 255), 2)
    # for centroid in CentroidList:
    #     posX, posY = centroid
    #     cv2.putText(mask_kmeans1, f'({posX}, {posY})', (posX - 40, posY - 40), TextFont, 0.8, (255, 255, 255), 1)
    #     cv2.circle(mask_kmeans1, (posX, posY), 8, (255, 255, 0), -1)
    # cv2.circle(mask_kmeans1, (quad_x, quad_y), 8, (255, 0, 255), -1)
    # cv2.putText(mask_kmeans1, f'{FileName}', (100, 100), TextFont, 1, (255, 255, 255), 1)
    # cv2.line(mask_kmeans1, (0, quad_y), (800, quad_y), (192, 192, 192), 2)
    # cv2.line(mask_kmeans1, (quad_x, 0), (quad_x, 600), (216, 192, 130), 2)

    # cv2.imwrite(OutputPath + ' Kmeans1.png', mask_kmeans1)

    # --- 根據 4 個質心位置 繪製四邊形找出四邊形中心 End.

    # --- 區分以四邊形為中心點的左右資料
    left, left_index = len(np.where(CentroidList[:, 0] < quad_x)[0]), np.where(CentroidList[:, 0] < quad_x)[0]
    right, right_index = len(np.where(CentroidList[:, 0] >= quad_x)[0]), np.where(CentroidList[:, 0] >= quad_x)[0]
    # --- 區分以四邊形為中心點的左右資料 End.

    # --- 迴圈做 Kmeans 分類(迭代次數最大為 FeatureCombine 長度, 若全部嘗試過也無法正確分類, 則有問題的該腔室為空)
    if left != right:
        # for iteration in range(0, len(FeatureCombine)):
        if right > left:
            LeftData = OriginalData[firstPred == left_index]
            RightData = OriginalData[firstPred != left_index]

        else:
            LeftData = OriginalData[firstPred != right_index]
            RightData = OriginalData[firstPred == right_index]

        LeftCentroid, LeftPred = ReKmeans(LeftData)
        RightCentroid, RightPred = ReKmeans(RightData)

        # -- 判斷是否分錯(緩)
        # 看兩個質心點是否明顯存在上下關係(緩) 先看全部結果
        # leftC1, leftC2 = LeftCentroid[0], LeftCentroid[1]
        adjust_Centroid["RA"] = LeftCentroid[0] if LeftCentroid[0][1] > LeftCentroid[1][1] else LeftCentroid[1]
        adjust_Centroid["RV"] = LeftCentroid[1] if LeftCentroid[0][1] > LeftCentroid[1][1] else LeftCentroid[0]

        adjust_Centroid["LA"] = RightCentroid[0] if RightCentroid[0][1] > RightCentroid[1][1] else RightCentroid[1]
        adjust_Centroid["LV"] = RightCentroid[1] if RightCentroid[0][1] > RightCentroid[1][1] else RightCentroid[0]

        # - visualization
        Left_and_Right = LeftCentroid + RightCentroid
        Left_and_Right = np.asarray(Left_and_Right)
        quadrilateral = cv2.convexHull(Left_and_Right)

        quadM = cv2.moments(quadrilateral)
        quad_x, quad_y = int(quadM["m10"] / quadM["m00"]), int(quadM["m01"] / quadM["m00"])
        # - draw data
        # for pred in LeftPred:
        #     curr_cluster_data = LeftData[LeftPred == pred]
        #     for index in range(len(curr_cluster_data[:, -2:])):
        #         coordX, coordY = curr_cluster_data[index][-2:].astype(np.int)
        #         cv2.circle(mask_kmeans2, (coordX, coordY), 5, colors[pred], -1)
        #
        # RightPred += 2
        # for pred in RightPred:
        #     curr_cluster_data = RightData[RightPred == pred]
        #     for index in range(len(curr_cluster_data[:, -2:])):
        #         coordX, coordY = curr_cluster_data[index][-2:].astype(np.int)
        #         cv2.circle(mask_kmeans2, (coordX, coordY), 5, colors[pred], -1)

        # - draw line
        # cv2.drawContours(mask_kmeans2, [quadrilateral], -1, (255, 0, 255), 2)
        # for centroid in Left_and_Right:
        #     posX, posY = centroid
        #     cv2.putText(mask_kmeans2, f'({posX}, {posY})', (posX - 40, posY - 40), TextFont, 1, (255, 255, 255), 1)
        #     cv2.circle(mask_kmeans2, (posX, posY), 8, (255, 255, 0), -1)
        # cv2.circle(mask_kmeans2, (quad_x, quad_y), 8, (255, 0, 255), -1)
        # cv2.putText(mask_kmeans2, f'{FileName}', (100, 100), TextFont, 1, (255, 255, 255), 1)
        # cv2.line(mask_kmeans2, (0, quad_y), (800, quad_y), (192, 192, 192), 2)
        # cv2.line(mask_kmeans2, (quad_x, 0), (quad_x, 600), (216, 192, 130), 2)

        # cv2.imwrite(OutputPath + ' Kmeans2.png', mask_kmeans2)

    else:
        # 若位置正確, 按象限角分沒問題
        thetaData = ClusterFeature[:, 2]
        thetaSort = np.argsort(thetaData)

        adjust_Centroid["LA"] = tuple(CentroidList[thetaSort[0]])
        adjust_Centroid["RA"] = tuple(CentroidList[thetaSort[1]])
        adjust_Centroid["RV"] = tuple(CentroidList[thetaSort[2]])
        adjust_Centroid["LV"] = tuple(CentroidList[thetaSort[3]])

    return adjust_Centroid


def FrameCenterAnomalyDetection(HistoryCenters, CurrentCenters, Centroids):
    # -- 處理腔室多個點的情況
    not_exist = list()
    for pos in CurrentCenters.keys():
        if len(CurrentCenters[pos]) > 1:
            if len(CurrentCenters[pos]) == 2:
                x1, y1 = CurrentCenters[pos][0]
                x2, y2 = CurrentCenters[pos][1]
                CurrentCenters[pos] = ((x2 - x1) // 2 + x1, (y2 - y1) // 2 + y1)
                HistoryCenters[pos].append(((x2 - x1) // 2 + x1, (y2 - y1) // 2 + y1))

            else:
                L = np.asarray(CurrentCenters[pos])
                Hull = cv2.convexHull(L)
                Hull_M = cv2.moments(Hull)
                if Hull_M["m00"] != 0:
                    Cx, Cy = int(Hull_M["m10"] / Hull_M["m00"]), int(Hull_M["m01"] / Hull_M["m00"])
                    CurrentCenters[pos] = (Cx, Cy)
                    HistoryCenters[pos].append((Cx, Cy))

                else:
                    not_exist.append(pos)

        if len(CurrentCenters[pos]) == 1:
            CurrentCenters[pos] = CurrentCenters[pos][0]
            HistoryCenters[pos].append(tuple(CurrentCenters[pos]))

        if len(CurrentCenters[pos]) == 0:
            not_exist.append(pos)
    # -- 處理腔室多個點的情況  End.

    # -- 處理當前腔室不存在的問題
    # 利用歷史的中心點, 取正中心點 取代(預測)當前幀的中心
    for nan_pos in not_exist:
        history_pos = HistoryCenters[nan_pos]
        # 避免因為每次都是加入質心點或歷史座標, 而出現 convexHull 的 bug(即使長度 > 2, 但實質上只有一點, 無法成線和凸包)
        # 去除重複的部分, 再進行判斷; 但不影響 HistoryCenters 紀錄
        history_pos = set(history_pos)
        history_pos = list(history_pos)

        if len(history_pos) != 0:
            if len(history_pos) == 1:
                CurrentCenters[nan_pos] = HistoryCenters[nan_pos][0]
                HistoryCenters[nan_pos].append(HistoryCenters[nan_pos][0])

            if len(history_pos) == 2:
                x1, y1 = HistoryCenters[nan_pos][0]
                x2, y2 = HistoryCenters[nan_pos][1]
                CurrentCenters[nan_pos] = ((x2 - x1) // 2 + x1, (y2 - y1) // 2 + y1)
                HistoryCenters[nan_pos].append(((x2 - x1) // 2 + x1, (y2 - y1) // 2 + y1))

            if len(history_pos) > 2:
                L = np.asarray(HistoryCenters[nan_pos])
                Hull = cv2.convexHull(L)
                Hull_M = cv2.moments(Hull)
                if Hull_M["m00"] != 0:
                    Cx, Cy = int(Hull_M["m10"] / Hull_M["m00"]), int(Hull_M["m01"] / Hull_M["m00"])
                else:
                    Cx, Cy = Centroids[nan_pos]

                CurrentCenters[nan_pos] = (Cx, Cy)
                HistoryCenters[nan_pos].append((Cx, Cy))

        else:
            # 若無歷史紀錄, 則用質心點取代
            CurrentCenters[nan_pos] = Centroids[nan_pos]
            HistoryCenters[nan_pos].append(Centroids[nan_pos])
    # -- 處理當前腔室不存在的問題 End.

    # -- 處理腔室中心點過於中心區域及邊界的問題(這部分應該要對所有腔室做)
    for near_pos in CurrentCenters.keys():
        LVx, LVy = CurrentCenters["LV"]
        LAx, LAy = CurrentCenters["LA"]
        RVx, RVy = CurrentCenters["RV"]
        RAx, RAy = CurrentCenters["RA"]

        CentroidLVx, CentroidLVy = Centroids["LV"]
        CentroidLAx, CentroidLAy = Centroids["LA"]
        CentroidRVx, CentroidRVy = Centroids["RV"]
        CentroidRAx, CentroidRAy = Centroids["RA"]

        LeftYDiff = CentroidLAy - CentroidLVy
        RightYDiff = CentroidRAy - CentroidRVy

        UpXDiff = CentroidLVx - CentroidRVx
        DownXDiff = CentroidLAx - CentroidRAx

        if near_pos == "LA":
            up_limit = int(LeftYDiff * 0.35) + CentroidLVy
            down_limit = int(LeftYDiff * 0.65) + CentroidLVy
            left_limit = int(DownXDiff * 0.35) + CentroidRAx
            right_limit = int(DownXDiff * 0.65) + CentroidRAx

            isCenter = (up_limit <= LAy <= down_limit) or (left_limit <= LAx <= right_limit)

            if isCenter:
                CurrentCenters["LA"] = (CentroidLAx, CentroidLAy)
                HistoryCenters["LA"][-1] = (CentroidLAx, CentroidLAy)

        elif near_pos == "LV":
            up_limit = int(LeftYDiff) * 0.35 + CentroidLVy
            down_limit = int(LeftYDiff) * 0.65 + CentroidLVy
            left_limit = int(UpXDiff * 0.35) + CentroidRVx
            right_limit = int(UpXDiff * 0.65) + CentroidRVx

            isCenter = (up_limit <= LVy <= down_limit) or (left_limit <= LVx <= right_limit)

            if isCenter:
                CurrentCenters["LV"] = (CentroidLVx, CentroidLVy)
                HistoryCenters["LV"][-1] = (CentroidLVx, CentroidLVy)

        elif near_pos == "RV":
            up_limit = int(RightYDiff) * 0.35 + CentroidRVy
            down_limit = int(RightYDiff) * 0.65 + CentroidRVy
            left_limit = int(UpXDiff * 0.35) + CentroidRVx
            right_limit = int(UpXDiff * 0.65) + CentroidRVx

            isCenter = (up_limit <= RVy <= down_limit) or (left_limit <= RVx <= right_limit)

            if isCenter:
                CurrentCenters["RV"] = (CentroidRVx, CentroidRVy)
                HistoryCenters["RV"][-1] = (CentroidRVx, CentroidRVy)

        elif near_pos == "RA":
            up_limit = int(RightYDiff) * 0.35 + CentroidRVy
            down_limit = int(RightYDiff) * 0.65 + CentroidRVy
            left_limit = int(DownXDiff * 0.35) + CentroidRAx
            right_limit = int(DownXDiff * 0.65) + CentroidRAx

            isCenter = (up_limit <= RAy <= down_limit) or (left_limit <= RAx <= right_limit)

            if isCenter:
                CurrentCenters["RA"] = (CentroidRAx, CentroidRAy)
                HistoryCenters["RA"][-1] = (CentroidRAx, CentroidRAy)

    # - 處理腔室中心點過於中心的問題 End.

    return HistoryCenters, CurrentCenters


InputDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\Segmentation\\A4C Test Video\\"
VideoPath = AllFiles(InputDir, 'avi')

SkeletonizeDir = 'E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\classified data_png' \
                 '\\0002_Apical Four Chamber\\'

OutputDir = 'E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\Segmentation\\A4C Valve 1210\\'
OutputBugDir = 'E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\Segmentation\\A4C Valve 1210\\' \
               'bug dir\\'

TextFont = cv2.FONT_HERSHEY_COMPLEX_SMALL


for path in VideoPath:
    CurrVideoTimeStart = time.time()

    init = VideoInit(path)
    FileName = path.split('\\')[-1]
    print(f'FileName: {FileName}')

    # --- 處理骨架圖找腔室範圍
    try:
        SkeletonizePath = SkeletonizeDir + FileName + '.png'
        skeleton = cv2.imread(SkeletonizePath)

    except cv2.error:
        rea = 'cv2.error: 沒有該檔案的骨架圖'
        handle_bug(OutputBugDir + FileName, reason=rea)
        continue

    gray_skeleton = cv2.cvtColor(skeleton, cv2.COLOR_BGR2GRAY)
    gray_skeleton[init.roi != 255] = 0

    x_bound, y_bound = list(), list()
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

    except ValueError:
        rea = f'ValueError: 骨架圖可能為全黑的'
        cv2.putText(skeleton, 'The skeleton image may be completely black', (100, 100), TextFont, 1, (255, 255, 255), 1)
        handle_bug(OutputBugDir + FileName + '.png', reason=rea, img=skeleton)
        continue

    # --- 處理骨架圖找腔室範圍 End.

    # --- 距離變換取腔室中心點並統計 & 創建特徵
    CenterData = list()
    mask_center = np.zeros((600, 800, 3), np.uint8)

    while True:
        ret, frame = init.video.read()

        if not ret:
            break

        frame[init.roi != 255] = [0, 0, 0]
        median = cv2.medianBlur(frame, 19)
        img_bl = cv2.blur(frame, (17, 17))

        gray_median = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
        gray_median[init.roi != 255] = 0

        # - distance transform
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
        # - distance transform End.

        # -- 取出腔室中心點 & 創建特徵
        # - 取出腔室中心點
        cnt_center, _ = cv2.findContours(dist, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnt_center:
            area = cv2.contourArea(c)

            if area > 10:
                HullC = cv2.convexHull(c)
                x, y, w, h = cv2.boundingRect(HullC)
                CenterX, CenterY = int(x + w / 2), int(y + h / 2)
                # - 取出腔室中心點 End.

                # - 創建特徵
                diff_w, diff_h = CenterX - cb_cen_x, CenterY - cb_cen_y

                # 用角度做 (為了要和 象限 及 角度一致, 因此要先判斷方向)
                R = np.sqrt((CenterX - cb_cen_x) ** 2 + (CenterY - cb_cen_y) ** 2)
                theta = np.degrees(np.arccos((CenterX - cb_cen_x) / R))

                # 由於 numpy & math 角度亂轉, 要多一點判斷式子
                # 角度固定從 3 點鐘方向 順時針轉
                if theta > 90:
                    theta -= 90
                if abs(diff_h) > abs(diff_w):
                    theta = 90 - theta if theta < 45 else theta
                if abs(diff_w) > abs(diff_h):
                    theta = 90 - theta if theta > 45 else theta

                # LA 位置(+, +) 角度小於 90(不影響象限角)
                if diff_w >= 0 and diff_h <= 0:  # LV 位置 (+, -) 角度 270 ~ 360
                    theta = 360 - theta
                elif diff_w <= 0 and diff_h >= 0:  # RA 位置 (-, +) 角度 90 ~ 180
                    theta = 180 - theta
                elif diff_w <= 0 and diff_h <= 0:  # RV 位置 (-, -) 角度 180 ~ 270
                    theta = 180 + theta

                Feature = [diff_w, diff_h, theta, CenterX, CenterY]
                CenterData.append(Feature)
                # - 創建特徵 End.

                cv2.circle(mask_center, (CenterX, CenterY), 5, (255, 255, 255), -1)
        # -- 取出腔室中心點 & 創建特徵 End.

    # --- 利用 KMeans 區分四個腔室
    Centroid = KmeansCluster(CenterData)
    print(f'Last Centroid: {Centroid}')

    # --- 再讀取一次影片針對每幀做腔室定位
    re_video = cv2.VideoCapture(path)

    ChambersColors = [(255, 0, 255), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # LV, LA, RV, RA
    frame_list = list()
    frame_count = 0

    HistoryCenter = {"LV": [], "LA": [], "RV": [], "RA": []}
    while True:
        ret, frame = re_video.read()

        if not ret:
            break

        frame_count += 1
        frame[init.roi != 255] = [0, 0, 0]
        frame_draw = frame.copy()
        frame_valve = frame.copy()

        median = cv2.medianBlur(frame, 19)
        gray_median = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
        gray_median[init.roi != 255] = 0

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

        cnt_center, _ = cv2.findContours(dist, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        curr_center = {"LV": [], "LA": [], "RV": [], "RA": []}

        for c in cnt_center:
            area = cv2.contourArea(c)

            if area > 10:
                HullC = cv2.convexHull(c)
                x, y, w, h = cv2.boundingRect(HullC)
                CenterX, CenterY = int(x + w / 2), int(y + h / 2)

                # - 到這裡步驟和前面一致 End.

                # -- 利用距離判斷當前 Center 和 Centroid 的關係
                DisLV = np.sqrt((CenterX - Centroid["LV"][0]) ** 2 + (CenterY - Centroid["LV"][1]) ** 2)
                DisLA = np.sqrt((CenterX - Centroid["LA"][0]) ** 2 + (CenterY - Centroid["LA"][1]) ** 2)
                DisRV = np.sqrt((CenterX - Centroid["RV"][0]) ** 2 + (CenterY - Centroid["RV"][1]) ** 2)
                DisRA = np.sqrt((CenterX - Centroid["RA"][0]) ** 2 + (CenterY - Centroid["RA"][1]) ** 2)
                DisList = [DisLV, DisLA, DisRV, DisRA]
                MinDis = DisList.index(min(DisList))

                if MinDis == 0:
                    curr_center["LV"].append((CenterX, CenterY))
                elif MinDis == 1:
                    curr_center["LA"].append((CenterX, CenterY))
                elif MinDis == 2:
                    curr_center["RV"].append((CenterX, CenterY))
                elif MinDis == 3:
                    curr_center["RA"].append((CenterX, CenterY))
                # -- 利用距離判斷當前 Center 和 Centroid 的關係 End.

        # -- 針對每幀腔室的點做異常檢測
        HistoryCenter, curr_center = FrameCenterAnomalyDetection(
            HistoryCenters=HistoryCenter,
            CurrentCenters=curr_center,
            Centroids=Centroid
        )
        # -- 針對每幀腔室的點做異常檢測 End.
        cv2.putText(frame_draw, 'LV', curr_center["LV"], TextFont, 1, ChambersColors[0], 1)
        cv2.putText(frame_draw, 'LA', curr_center["LA"], TextFont, 1, ChambersColors[1], 1)
        cv2.putText(frame_draw, 'RV', curr_center["RV"], TextFont, 1, ChambersColors[2], 1)
        cv2.putText(frame_draw, 'RA', curr_center["RA"], TextFont, 1, ChambersColors[3], 1)
        cv2.putText(frame_draw, f'frame count: {frame_count}', (100, 100), TextFont, 1, (255, 255, 255), 1)
        # --- 再讀取一次影片針對每幀做腔室定位 End.

    # print(HistoryCenter)
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # Colors = [
    #     ['red', 'blue', 'chocolate'],
    #     ['aqua', 'green', 'darkblue'],
    #     ['orange', 'purple', 'steelblue'],
    #     ['gray', 'violet', 'tomato']
    # ]
    #
    # for color_ind, keys in enumerate(HistoryCenter.keys()):
    #     Data = np.asarray(HistoryCenter[keys])
    #     X_Data, Y_Data = Data[:, 0], Data[:, 1]
    #     ax.scatter(X_Data, Y_Data, range(1, len(X_Data) + 1),
    #                color=Colors[color_ind][0], s=10, label=keys + ' Curr Center')
    #     ax.plot(X_Data, Y_Data, range(1, len(X_Data) + 1), color=Colors[color_ind][1], label=keys)
    #     ax.plot([Centroid[keys][0]] * len(X_Data), [Centroid[keys][1]] * len(X_Data), range(1, len(X_Data) + 1),
    #             color=Colors[color_ind][2], label=keys + ' Centroid')
    #
    # plt.xlabel('X Coord')
    # plt.ylabel('Y Coord')
    # plt.title('Z: Frame Count')
    # plt.legend()
    # plt.savefig(OutputDir + FileName + ' .png')
    # plt.show()

        # --- 根據每幀抓取瓣膜位置
        # 利用 multi-threshold 試試看效果
        frame_valve_gray = cv2.cvtColor(frame_valve, cv2.COLOR_BGR2GRAY)
        multi = MultiThres(frame_valve_gray, init.roi, 40, 255)
        multi.SearchMax()
        Multi = multi.threshold()
        Multi_BGR = cv2.cvtColor(Multi, cv2.COLOR_GRAY2BGR)

        mask_region = np.zeros((600, 800), np.uint8)
        cnt_region = np.asarray(
            [curr_center["LV"], curr_center["LA"],
             curr_center["RA"], curr_center["RV"]]
        )
        cv2.drawContours(mask_region, [cnt_region], -1, (255, 255, 255), -1)

        # cv2.drawContours(Multi_BGR, [cnt_region], -1, (0, 255, 0), 2)
        # cv2.circle(Multi_BGR, curr_center["LV"], 8, (0, 0, 255), -1)
        # cv2.circle(Multi_BGR, curr_center["LA"], 8, (0, 0, 255), -1)
        # cv2.circle(Multi_BGR, curr_center["RV"], 8, (0, 0, 255), -1)
        # cv2.circle(Multi_BGR, curr_center["RA"], 8, (0, 0, 255), -1)

        mask_region = cv2.erode(mask_region, np.ones((3, 3)), iterations=15)
        # mask_bgr = cv2.cvtColor(mask_region, cv2.COLOR_GRAY2BGR)
        # ppt = cv2.addWeighted(mask_bgr, 0.7, Multi_BGR, 1, 1)
        # cv2.imshow('Ori multi', ppt)

        Multi[mask_region != 255] = 0

        cnt_Multi, _ = cv2.findContours(Multi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask_filter = np.zeros((600, 800), np.uint8)
        for cnt_index, cnt in enumerate(cnt_Multi):
            if cv2.contourArea(cnt) > 100:
                cv2.drawContours(mask_filter, [cnt], -1, (255, 255, 255), -1)
                cv2.drawContours(Multi_BGR, [cnt], -1, (0, 0, 255), -1)

        cnt_filter, _ = cv2.findContours(mask_filter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        HullFilter = list()

        for i in range(len(cnt_filter)):
            for j in range(len(cnt_filter[i])):
                HullFilter.append(cnt_filter[i][j])

        if len(HullFilter) != 0:
            HullFilter = np.asarray(HullFilter)
            HullFilter = cv2.convexHull(HullFilter)
            MFilter = cv2.moments(HullFilter)
            LeftPivotX, LeftPivotY = int(MFilter["m10"] / MFilter["m00"]), int(MFilter["m01"] / MFilter["m00"])

            cv2.line(frame_draw, curr_center["LV"], curr_center["LA"], (255, 0, 0), 2)  # 視覺化用(LV & LA 線段)
            cv2.line(Multi_BGR, curr_center["LV"], curr_center["LA"], (255, 0, 0), 2)  # 視覺化用(LV & LA 線段)

            # 計算左支點到腔室中心連線段的距離
            CenLVX, CenLVY = curr_center["LV"]
            CenLAX, CenLAY = curr_center["LA"]
            if CenLAX != CenLVX:
                slope_LVLA = (CenLAY - CenLVY) / (CenLAX - CenLVX)
                PivotDis = int((LeftPivotY - CenLVY + slope_LVLA * CenLVX) / slope_LVLA - LeftPivotX) + 2
            else:
                PivotDis = int(CenLVX - LeftPivotX) + 2
            RightPivotX = LeftPivotX + 2 * PivotDis

            _x, _y, _w, _h = cv2.boundingRect(HullFilter)
            cv2.drawContours(Multi_BGR, [HullFilter], -1, (0, 255, 0), 2)
            cv2.line(Multi_BGR, (LeftPivotX, LeftPivotY), (RightPivotX, LeftPivotY), (255, 255, 0), 2)
            cv2.rectangle(Multi_BGR, (_x, _y), (_x+_w, _y+_h), (255, 0, 0), 2)
            cv2.circle(Multi_BGR, (LeftPivotX, LeftPivotY), 10, (0, 255, 255), -1)
            cv2.circle(Multi_BGR, (RightPivotX, LeftPivotY), 10, (0, 255, 255), -1)

        #     cv2.drawContours(frame_draw, [HullFilter], -1, (0, 255, 0), 2)
        #     cv2.line(frame_draw, (LeftPivotX, LeftPivotY), (RightPivotX, LeftPivotY), (255, 255, 0), 2)
        #     cv2.rectangle(frame_draw, (_x, _y), (_x + _w, _y + _h), (255, 0, 0), 2)
        #     cv2.circle(frame_draw, (LeftPivotX, LeftPivotY), 10, (0, 255, 255), -1)
        #     cv2.circle(frame_draw, (RightPivotX, LeftPivotY), 10, (0, 255, 255), -1)
        # frame_list.append(frame_draw)

        cv2.imshow('bgr', Multi_BGR)
        # cv2.imshow('multi', Multi)
        # cv2.imshow('mask_filter', mask_filter)
        # cv2.imshow('frame draw', frame_draw)
        cv2.waitKey(100)

    # write_video(frame_list, OutputDir + FileName)
    CurrVideoTimeEnd = time.time()
    # print(f'Current Video Total Spend Time: {round(CurrVideoTimeEnd - CurrVideoTimeStart, 2)} sec.')
