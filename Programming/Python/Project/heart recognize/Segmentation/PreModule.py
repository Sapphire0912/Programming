import numpy as np
import cv2
import os


def AllFiles(DirPath, extension_name='avi'):
    """
    DirPath: 影片目錄的資料夾路徑
    extension_name: 副檔名, 預設 avi
    """

    result = list()
    for root, dirs, files in os.walk(DirPath):
        for f in files:
            if f[-len(extension_name):] == extension_name:
                result.append(os.path.join(root, f))
    return result


class VideoInit(object):
    """
    影像處理 use AVI files
    2-1. 第一次讀取影片: <- 取得影像基本所需資訊
    A. 骨架化  -- unit finished
    B. 超音波影像 ROI  -- unit finished -> Integration finished
    C. 判斷是否有 Doppler, 有則輸出 Doppler 區域[3] 和 消除 Doppler 邊界和顏色(還原影像) 輸出 AVI file, 無跳過此步  -- unfinished
    D. 找標準單位 -- unit finished(if bpm is not exist, use self digital recognition)
    """

    def __init__(self, VideoPath):
        # 使用 cv2 讀取影片
        self.video = cv2.VideoCapture(VideoPath)

        if not self.video:
            raise FileNotFoundError('檔案路徑不存在或影片無法讀取')

        else:
            # _ROI 屬性
            self.roi = self._ROI(VideoPath)

            # _Unit 屬性(Test, 尚未完成)
            self._unit = None
            self._bpm = None

            # _isDoppler 屬性
            self._isDoppler(VideoPath)

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

    def _isDoppler(self, Path):
        pass

# 把有 Doppler 的影像還原, 並輸出 Doppler region 和 還原影像的部分
# 把還原影像寫到目標資料夾內且 + restore, 最後 self.video 讀取該 restore 的影片

# 輸出 Doppler 的顏色區域 暫時不管
# (未來這些東西要寫成多執行緒, 這樣才可以確保只花讀取一次影片但處理最長的時間)
# (現在是分段讀取 所以速度會慢上一倍)
