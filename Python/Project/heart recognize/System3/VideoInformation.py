from skimage.morphology import skeletonize
import numpy as np
import cv2
import os


# 這裡未來要用 multi-processing 或 multi-threading 跑

class VideoInit(object):
    """
    Class name:
        VideoInit(object):
        處理影片的基本資訊
        目前: ROI、骨架圖、標準單位 及 BPM(測試階段)

    Initialization parameters:
        VideoPath: 輸入影片路徑, str
    """

    def __init__(self, VideoPath, OutputSkeletonDir):
        self.OutputSkeletonDir = OutputSkeletonDir
        self.extension_name = ["avi", "png"]

        self._Skeletonize(VideoPath)
        self.roi = self._ROI(VideoPath)

        # self.UnitCM = None
        # self.UnitBPM = None
        # self._Unit(VideoPath)

    def _AllFiles(self, InputDir):
        """
        method name:
            _AllFiles():
            讀取 FileDir 資料夾下的 DCM 及 AVI 檔案

        return:
            file_list: 回傳所有 DCM 和 AVI 檔案的列表
        """
        file_list = list()
        for root, dirs, files in os.walk(InputDir):
            for f in files:
                if f[-3:].lower() in self.extension_name:
                    file_list.append(os.path.join(root, f))
        return file_list

    def _ROI(self, Path):
        """
        method name:
            _ROI(Path):
            找到超音波影像的有效區域

        parameters:
            Path: 影片檔案路徑, str

        return:
            roi: 超音波有效區域二值化圖片, numpy.ndarray, 大小為 (height, width)

        attributes:
            self.ox, self.oy: ROI 扇形區域的中心點 x, y 軸座標, int
            self.radius: ROI 扇形的半徑, int
        """
        # ----- 1. 找出超音波影像有效區域
        target = cv2.VideoCapture(Path)
        _, first = target.read()

        # self._Unit(first)  # 處理標準單位 & BPM (測試階段)

        gray_first = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)

        # 疊加所有差幀結果
        mask_diff_all = np.zeros(gray_first.shape, np.uint8)

        while True:
            _ret, f = target.read()

            if not _ret:
                break

            gray_f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(gray_first, gray_f)

            diff[diff > 10] = 255
            diff[diff <= 10] = 0
            mask_diff_all += diff
            np.clip(mask_diff_all, 0, 255, out=mask_diff_all)

        mask_last = np.zeros(gray_first.shape, np.uint8)
        cnt, _ = cv2.findContours(mask_diff_all, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(mask_last, cnt, -1, (255, 255, 255), -1)

        kernel = np.ones((3, 3), np.uint8)
        erode = cv2.erode(mask_last, kernel, iterations=3)
        dilate = cv2.dilate(erode, kernel, iterations=2)

        mask_last_bound = np.zeros(gray_first.shape, np.uint8)
        cnt, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnt:
            if cv2.contourArea(c) >= 300:
                cv2.drawContours(mask_last_bound, [c], -1, (255, 255, 255), 2)
        cnt_last, _ = cv2.findContours(mask_last_bound, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # ----- mask ROI End.

        # ----- 2. 找出有效區域的圓心座標和半徑 & 繪製扇形 mask(避免有鋸齒或影像不完整導致 ROI 效果不好)
        roi = np.zeros(first.shape[:2], np.uint8)

        # 霍夫轉換找直線求兩線交點
        lines = cv2.HoughLinesP(
            mask_last_bound, 1, np.pi / 180,
            threshold=200,
            minLineLength=60,
            maxLineGap=130
        )

        x1_y1, x2_y2 = list(), list()
        lm_error, rm_error = 1, 1
        l_index, r_index = None, None  # 儲存兩條線最接近斜率為 -1, 1 的索引值

        try:
            for line_index in range(len(lines)):
                x1, y1, x2, y2 = lines[line_index][0]
                m = (y2 - y1) / ((x2 - x1) + 1e-08)  # 1e-08 避免分母為 0

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

            # 利用方程式求出圓心座標
            a1, b1 = x1_y1[l_index]
            a2, b2 = x2_y2[l_index]
            m1 = (b2 - b1) / (a2 - a1)

            A1, B1 = x1_y1[r_index]
            A2, B2 = x2_y2[r_index]
            m2 = (B2 - B1) / (A2 - A1)

            c0, c1 = m1 * a1 - b1, m2 * A1 - B1

            ox = np.round((c0 - c1) / (m1 - m2)).astype(np.int)
            oy = np.round(((m1 + m2) * ox - c0 - c1) / 2).astype(np.int)

            # 找半徑
            radius = 0
            for i in range(len(cnt_last)):
                for j in range(len(cnt_last[i])):
                    if radius < cnt_last[i][j][0][1]:
                        radius = cnt_last[i][j][0][1]
            radius = radius - oy
            cv2.ellipse(roi, (ox, oy), (radius, radius), 90, -45, 45, (255, 255, 255), -1)

        except TypeError:
            # 霍夫轉換找不到直線時, 拿 y 軸的最小值當圓心
            radius = 0
            ox, oy = 0, 600

            for i in range(len(cnt_last)):
                for j in range(len(cnt_last[i])):
                    if radius < cnt_last[i][j][0][1]:
                        radius = cnt_last[i][j][0][1]

                    if oy > cnt_last[i][j][0][1]:
                        ox, oy = cnt_last[i][j][0]
            radius = radius - oy
            cv2.ellipse(roi, (ox, oy), (radius, radius), 90, -45, 45, (255, 255, 255), -1)

        self.ox, self.oy, self.radius = ox, oy, radius
        return roi

    def _pixelVal(self, pix, r1, s1, r2, s2):
        if 0 <= pix <= r1:
            return (s1 / r1) * pix
        elif r1 < pix <= r2:
            return ((s2 - s1) / (r2 - r1)) * (pix - r1) + s1
        else:
            return ((255 - s2) / (255 - r2)) * (pix - r2) + s2

    def _filling_cnt(self, in_pic, target, min_area, max_area, mode):
        cnts, hier = cv2.findContours(in_pic, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            Area = cv2.contourArea(c)
            # 忽略太小的區域
            if min_area < Area < max_area:
                cv2.drawContours(target, [c], -1, (255, 255, 255), mode)

    def _Skeletonize(self, Path):
        target = cv2.VideoCapture(Path)
        FileName = Path.split('\\')[-1]

        if not os.path.isdir(self.OutputSkeletonDir):
            os.makedirs(self.OutputSkeletonDir)

        # FileName = FileName.replace('.avi', '.png')
        isExistOutputDir = self._AllFiles(self.OutputSkeletonDir)

        isExistFile = self.OutputSkeletonDir + FileName + '.png'
        if isExistFile in isExistOutputDir:
            print(f'{isExistFile}, 該骨架圖已存在於輸出資料夾 (可忽略此訊息)')
            pass

        else:
            all_frames = list()

            # 從這裡開始要用學長的程式
            while True:
                ret, frame = target.read()

                if not ret:
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.medianBlur(gray, 9)
                gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

                avg = sum(gray.ravel() / len(gray.ravel()))
                r1, r2 = (90, 180) if avg < 36 else (140, 190)

                pixelVal_vec = np.vectorize(self._pixelVal)  # vectorize data
                gray = pixelVal_vec(gray, r1, 0, r2, 255)  # contrast stretching

                grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
                grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

                abs_grad_x = cv2.convertScaleAbs(grad_x)
                abs_grad_y = cv2.convertScaleAbs(grad_y)

                grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
                sob = cv2.cvtColor(grad, cv2.COLOR_GRAY2BGR)
                self._filling_cnt(grad, sob, 0, 4000000, -1)
                _, sob = cv2.threshold(sob, 254, 255, cv2.THRESH_BINARY)

                skeleton = skeletonize(sob)
                skeleton = cv2.cvtColor(skeleton, cv2.COLOR_BGR2GRAY)

                contours, hierarchy = cv2.findContours(grad, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area >= 50:
                        all_frames.append(skeleton)

            all_frames = np.array(all_frames)
            frame_avr = np.sum(all_frames, axis=0)

            frame_avr = frame_avr / len(all_frames)
            frame_avr = cv2.convertScaleAbs(frame_avr)
            _, frame_avr = cv2.threshold(frame_avr, 5, 255, cv2.THRESH_BINARY)

            cv2.imwrite(isExistFile, frame_avr)

    def _UnitScore(self, src):
        def isWhiteArea(region):
            try:
                score = region[1][1]
            except IndexError:
                score = 0
            return score

        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        h, w = src.shape
        src = cv2.resize(src, (w * 4, h * 4), cv2.INTER_CUBIC)
        _, src_thres = cv2.threshold(src, 128, 255, cv2.THRESH_BINARY)
        cnt_src, _ = cv2.findContours(src_thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnt_src) == 1:
            return -1

        coordinate = list()
        for index, contour in enumerate(cnt_src):
            x1, y1, width, height = cv2.boundingRect(contour)
            coordinate.append([x1, y1, width, height])
            for i in range(0, index):
                if coordinate[i][0] < coordinate[index][0]:
                    coordinate[i], coordinate[index] = coordinate[index], coordinate[i]

        score_list = list()
        for index, coord in enumerate(coordinate):
            scale_w, scale_h = coord[2] // 2, coord[3] // 3
            cx, ucy, dcy = coord[0] + scale_w, coord[1] + scale_h, coord[1] + coord[3] - scale_h

            Upper_left = np.unique(src_thres[coord[1]:ucy, coord[0]:cx], return_counts=True)
            Center_left = np.unique(src_thres[ucy:dcy, coord[0]:cx], return_counts=True)
            Lower_left = np.unique(src_thres[dcy:coord[1] + coord[3], coord[0]:cx], return_counts=True)

            UL_score = isWhiteArea(Upper_left)
            CL_score = isWhiteArea(Center_left)
            LL_score = isWhiteArea(Lower_left)

            Upper_right = np.unique(src_thres[coord[1]:ucy, cx:coord[0] + coord[2]], return_counts=True)
            Center_right = np.unique(src_thres[ucy:dcy, cx:coord[0] + coord[2]], return_counts=True)
            Lower_right = np.unique(src_thres[dcy:coord[1] + coord[3], cx:coord[0] + coord[2]], return_counts=True)

            UR_score = isWhiteArea(Upper_right)
            CR_score = isWhiteArea(Center_right)
            LR_score = isWhiteArea(Lower_right)

            score_list.append([UL_score, CL_score, LL_score, UR_score, CR_score, LR_score])

        return score_list

    def _predict(self, ScoreList, isInfo):
        NoInfo_digit = {
            (0, 1): 0, (0, 4): 0, (5, 1): 0,
            (3, 2): 1,
            (2, 1): 2,
            (4, 1): 3,
            (5, 0): 4,
            (0, 3): 5,
            (1, 3): 6,
            (3, 5): 7,
            (1, 2): 8, (1, 5): 8, (1, 0): 8,
            (4, 2): 9
        }

        isInfo_digit = {
            (3, 2): 1, (4, 1, 0): 1, (3, 1, 0): 1,
            (2, 1): 2,
            (5, 0): 4, (4, 0): 4,
            (4, 3): 5, (0, 3): 5, (3, 1, 1): 5,
            (1, 2): 6, (1, 3): 6, (4, 5): 6,
            (3, 5): 7,
            (1, 5, 0): 0,
            (1, 5, 1): 8, (4, 2, 0): 8,
            (4, 2, 1): 9,
            (4, 1, 1): 3
        }

        if ScoreList == -1:
            return 'None'

        value = 0
        if isInfo:
            for index, val in enumerate(ScoreList):
                key = (ScoreList[index].index(max(ScoreList[index])), ScoreList[index].index(min(ScoreList[index])))
                if key == (3, 1):
                    # 1, 5 判斷(True -> 1, False -> 5)
                    key = (3, 1, 0) if int(sum(ScoreList[index]) / 6) < 70 else (3, 1, 1)

                elif key == (1, 5):
                    # 0, 8 判斷(True -> 0, False -> 8)
                    key = (1, 5, 0) if max(ScoreList[index]) - min(ScoreList[index]) < 30 else (1, 5, 1)

                elif key == (4, 2):
                    # 8, 9 判斷
                    if max(ScoreList[index]) - min(ScoreList[index]) > 50:
                        if int(sum(ScoreList[index]) / 6) > 155:
                            key = (4, 2, 0)  # 8
                        else:
                            key = (4, 2, 1)  # 9
                    else:
                        key = (4, 2, 0)  # 8

                elif key == (4, 1):
                    # 1, 3 判斷
                    if int(sum(ScoreList[index]) / 6) > 90:
                        if max(ScoreList[index]) - min(ScoreList[index]) > 160:
                            key = (4, 1, 0)  # 1
                        else:
                            key = (4, 1, 1)  # 3
                    else:
                        key = (4, 1, 0)  # 1

                value = isInfo_digit[key] * np.power(10, index) + value

        else:
            for index, val in enumerate(ScoreList):
                key = (ScoreList[index].index(max(ScoreList[index])), ScoreList[index].index(min(ScoreList[index])))
                value = NoInfo_digit[key] * np.power(10, index) + value

        return value

    def _Unit(self, Path):
        target = cv2.VideoCapture(Path)
        _, src = target.read()

        InfoRegion = src[40, 395]
        isInfo = 1 if InfoRegion[0] >= 50 else 0

        Unit_cm = src[75:93, 9:29]
        Unit_BPM = src[566:584, 725:757]

        Score_cm = self._UnitScore(Unit_cm)
        Score_BPM = self._UnitScore(Unit_BPM)

        Pred_cm = self._predict(Score_cm, isInfo)
        Pred_BPM = self._predict(Score_BPM, isInfo)

        self.UnitCM = Pred_cm
        self.UnitBPM = Pred_BPM
