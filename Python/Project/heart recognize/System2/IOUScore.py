import FileIO

from scipy import fftpack
from scipy import signal
import scipy as sp
import numpy as np
import cv2
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


class LVEFInfo(object):
    def __init__(self, GroundTruthDir, Mode, UnitCM, Radius, fps, BPM):
        """
        parameters:
            GroundTruthDir: 當前病例的 GroundTruthDir 路徑, str
            Mode: GroundTruth 模式, all 代表每幀都有 ground truth,
            UnitCM: 超音波標準長度 (cm), int
            Radius: ROI 的半徑 (pixel), int
            fps: frames per second, int
            BPM: beats per minute, int
        """
        self.GroundTruthDir = GroundTruthDir
        self.UnitCM = UnitCM
        self.Radius = Radius
        self.fps = fps
        self.bpm = BPM

        # self._GroundTruthLVEF(mode=Mode)

    def HandleIOU(self, src, FrameCount, mask):
        """
        method:
            HandleIOU(self, src, FrameCount, mask): 計算 LV Volume 當前 frame 和 Ground Truth 的 IoU Score

        parameters:
            src: 當前的原始三通道圖象, np.ndarray
            FrameCount: 當前影像的幀數, int
            mask: 計算好結果的 mask 區域 (封閉實心 mask), 二值圖
            GroundTruthDir: 當前病例的 GroundTruthDir 路徑, str

        return:
            Score: IOU 的分數, float
            src: 繪製後的圖像, np.ndarray
        """
        GTPath = FileIO.AllFiles(self.GroundTruthDir, 'png')

        # 以每幀都畫 Ground Truth 的情況設計
        GTCountList = list()
        for path in GTPath:
            filename = path.split('\\')[-1][:-4]  # 去除副檔名
            count = int(filename.split('_')[-1])
            GTCountList.append(count)

        # 找出對應幀的 Ground Truth
        index = GTCountList.index(FrameCount)
        GroundTruth = cv2.imread(GTPath[index], 0)  # 灰階讀取

        # 計算 IOU
        IOUMask = np.zeros(mask.shape, np.uint8)
        cnt_GT, _ = cv2.findContours(GroundTruth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnt_GT) != 1:
            areaList = list()
            for cnt in cnt_GT:
                areaList.append(cv2.contourArea(cnt))
            cnt_index = areaList.index(max(areaList))
            cv2.drawContours(IOUMask, [cnt_GT[cnt_index]], -1, (255, 255, 255), -1)

        else:
            cv2.drawContours(IOUMask, cnt_GT, -1, (255, 255, 255), -1)

        intersection = cv2.bitwise_and(IOUMask, mask)
        union = cv2.bitwise_or(IOUMask, mask)

        cnt_intersection, _ = cv2.findContours(intersection, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt_union, _ = cv2.findContours(union, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        UnionArea = cv2.contourArea(cnt_union[0])
        InterSectionArea = cv2.contourArea(cnt_intersection[0])
        Score = round(InterSectionArea / UnionArea, 3)

        # 將 IOU & 結果 繪製在 frame 上面
        drawIOU = np.zeros(src.shape, np.uint8)
        cnt_draw, _ = cv2.findContours(IOUMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(drawIOU, cnt_draw, -1, (255, 255, 0), -1)
        src = cv2.addWeighted(src, 1, drawIOU, 0.3, 1)

        # 判斷結果好壞
        if Score > 0.85:
            cv2.putText(
                src,
                f'IoU score: {Score}, Excellent.',
                (70, 100),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1
            )
        elif Score > 0.65:
            cv2.putText(
                src,
                f'IoU score: {Score}, Good.',
                (70, 100),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 0), 1
            )
        else:
            cv2.putText(
                src,
                f'IoU score: {Score}, Poor.',
                (70, 100),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1
            )

        return Score, src

    def FindCycle(self):
        """
        description:
            找出週期後, 定義 EDV 和 ESV 的時間, 並取出各 5 幀.
            e.g: EDV 在 frame count = 19 的位置, 則取出 [17, 18, 19, 20, 21] 的 frame, ESV 同理.
        """

        pass

    def _GroundTruthLVEF(self, mode='all'):
        """
        description:
            按照學長之前的作法, 低通濾波找週期.
            利用 Ground Truth 做低通濾波找出週期.

        method:
            _GroundTruthLVEF(self): 計算 Ground Truth 的週期, 找出 ESV 和 EDV 的點, 計算 LVEF

        return:
            None;
        """
        GTPath = FileIO.AllFiles(self.GroundTruthDir, 'png')
        VolumeList = list()

        for Path in GTPath:
            GroundTruth = cv2.imread(Path, 0)  # 灰階讀取

            # 計算面積 Contour Area
            cnt_GT, _ = cv2.findContours(GroundTruth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(cnt_GT) != 1:
                areaList = list()
                for cnt in cnt_GT:
                    areaList.append(cv2.contourArea(cnt))
                area = max(areaList)
            else:
                area = cv2.contourArea(cnt_GT[0])

            VolumeList.append(area)

        # 低通濾波
        y1 = signal.medfilt(VolumeList, 7)
        sig_fft = fftpack.fft(y1)
        power = np.abs(sig_fft) ** 2

        sample_freq = fftpack.fftfreq(len(y1), d=7)
        pos_mask = np.where(sample_freq > 0)
        freqs = sample_freq[pos_mask]
        peak_freq = freqs[power[pos_mask].argmax()]
        np.allclose(peak_freq, 1. / 40)
        high_freq_fft = sig_fft.copy()
        high_freq_fft[np.abs(sample_freq) > (peak_freq * 1.7)] = 0
        filtered_sig = fftpack.ifft(high_freq_fft)

        x = np.arange(1, len(VolumeList) + 1, 1)
        a = np.diff(np.sign(np.diff(filtered_sig))).nonzero()[0] + 1  # local min & max
        b = (np.diff(np.sign(np.diff(filtered_sig))) > 0).nonzero()[0] + 1  # local min
        c = (np.diff(np.sign(np.diff(filtered_sig))) < 0).nonzero()[0] + 1  # local max
        # +1 due to the fact that diff reduces the original index number

        # plot
        # plt.figure(figsize=(6, 5))
        #
        # plt.plot(x, VolumeList, label='Original signal')
        # plt.plot(x, filtered_sig, linewidth=2, label='Filtered signal')
        # plt.xlabel('Time [s]')
        # plt.ylabel('Amplitude')
        # plt.legend(loc='best')
        #
        # min_p = []
        # max_p = []
        # for i in range(0, len(x), 1):
        #     min_p.append(None)
        #     max_p.append(None)
        #
        # for k in b:
        #     min_p[k] = filtered_sig[k]
        # for q in c:
        #     max_p[q] = filtered_sig[q]
        #
        # plt.plot(x, min_p, "o", label="min", color='b')
        # plt.plot(x, max_p, "o", label="max", color='r')
        # plt.show()

        # volumes = list()
        # for i in x:
        #     check_vol = self.calLVVolume(cv2.imread(GTPath[i-1], 0))
        #     volumes.append(check_vol)
        # print(volumes)
        # print('ESV frame: ', b)
        # print('EDV frame: ', c)

        # 計算 LVEF <- 都先取第一個週期的 EDV & ESV
        # 如果有 fps & bpm, 則直接採用; 否則用學長的做法
        if (self.fps is None) or (self.bpm is None):
            ESV = [self.calLVVolume(cv2.imread(GTPath[i-1], 0)) for i in b]
            EDV = [self.calLVVolume(cv2.imread(GTPath[i-1], 0)) for i in c]
            # index_len = min(len(ESV), len(EDV))

            # 取第一個週期的 EDV & ESV
            ESV, EDV = ESV[0], EDV[0]
            # for i in range(index_len):
            #     LVEF = 100 * (EDV[i] - ESV[i]) / EDV[i]
            #     print(f"LVEF: {round(LVEF, 2)}%")
            #     pass

        else:
            CycleCount = round(60 * self.fps / self.bpm)  # type <int>
            volumeList = [self.calLVVolume(cv2.imread(GTPath[i-1], 0)) for i in x]

            # 取第一個週期的 EDV & ESV 計算 LVEF
            target = volumeList[:CycleCount]
            ESV, EDV = min(target), max(target)
            print("ESV/EDV Index:", target.index(ESV), target.index(EDV))
            # cv2.imshow('ESV', cv2.imread(GTPath[target.index(ESV)]))
            # cv2.imshow('EDV', cv2.imread(GTPath[target.index(EDV)]))
            # cv2.waitKey(0)

        LVEF = round(100 * (EDV - ESV) / EDV, 1)

        # 判斷嚴重程度
        # Hyper dynamic: LVEF > 70%
        # Normal: 70% > LVEF >= 50%
        # Mild dysfunction: 50% > LVEF >= 40%
        # Moderate dysfunction: 40% > LVEF >= 30%
        # Severe dysfunction: LVEF < 30%

        Text = ["Hyper Dynamic", "Normal", "Mild", "Moderate", "Severe"]
        Degree = np.array([70, 49, 39, 29, 0])
        GT_Degree = Text[len(Degree[Degree > LVEF])]
        print(f'EDV: {EDV} cm\u00b3, ESV: {ESV} cm\u00b3')
        print(f'Ground Truth LVEF: {LVEF}%, Degree: {GT_Degree}')

    def calLVVolume(self, src):
        """
        parameters:
            src: 二值化圖像, np.ndarray.

        return:
            LVVolume: 左心室容積單位 cm^3(ml), float
        """

        mask_cnt = np.zeros(src.shape, np.uint8)
        mask_fill_cnt = np.zeros(src.shape, np.uint8)
        cnt, _ = cv2.findContours(src, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnt) != 1:
            areaList = list()
            for c in cnt:
                areaList.append(cv2.contourArea(c))
            cnt_index = areaList.index(max(areaList))
            cnt_target = cnt[cnt_index]
        else:
            cnt_target = cnt[0]

        cv2.drawContours(mask_cnt, [cnt_target], -1, (255, 255, 255), 1)
        cv2.drawContours(mask_fill_cnt, [cnt_target], -1, (255, 255, 255), -1)
        cnt_target = cnt_target.reshape(len(cnt_target), -1)  # coordinate: [x, y]

        # find Apex point
        uni_yaxis = np.unique(cnt_target[:, 1])
        apexY = uni_yaxis[0]
        xaxis = cnt_target[cnt_target[:, 1] == apexY]  # 找出最低點(y 最小值)的 x 數值
        apexX = int(np.mean(xaxis[:, 0]))

        # find left & right point
        leftPoints, rightPoints = cnt_target[cnt_target[:, 0] < apexX], cnt_target[cnt_target[:, 0] >= apexX]
        uni_yaxis = np.unique(leftPoints[:, 1])
        leftY = uni_yaxis[-1]
        xaxis = leftPoints[leftPoints[:, 1] == leftY]
        leftX = xaxis[-1, 0]

        uni_yaxis = np.unique(rightPoints[:, 1])
        rightY = uni_yaxis[-1]
        xaxis = rightPoints[rightPoints[:, 1] == rightY]
        rightX = xaxis[-1, 0]

        # 垂直點 & 切 20 等分, 計算 LVEF (由瓣膜位置往上到 Apex Point)
        slope_lr = (rightY - leftY) / (rightX - leftX)
        bias_lr = rightY - slope_lr * rightX
        # check = cv2.cvtColor(mask_cnt, cv2.COLOR_GRAY2BGR)
        LVVolume = 0  # cm^3

        if slope_lr != 0:
            slope_apex = - (1 / slope_lr)
            bias_apex = apexY - slope_apex * apexX

            midX = (bias_apex - bias_lr) / (slope_lr - slope_apex)
            midY = slope_lr * midX + bias_lr
            midX, midY = int(midX), int(midY)
            h = np.sqrt((apexX - midX) ** 2 + (apexY - midY) ** 2)
            dh = h / 20

            for i in range(0, 19):
                mask_line = np.zeros(src.shape, np.uint8)

                bias_lr -= dh
                # currX = (bias_apex - bias_lr) / (slope_lr - slope_apex)
                # currY = slope_lr * midX + bias_lr
                # currX, currY = int(currX), int(currY)

                lineY = slope_lr * 800 + bias_lr
                cv2.line(mask_line, (0, int(bias_lr)), (800, int(lineY)), (255, 255, 255), 1)
                mask_line[mask_fill_cnt != 255] = 0

                cnt_line, _ = cv2.findContours(mask_line, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnt_line = cnt_line[0].reshape(len(cnt_line[0]), -1)  # coordinate: [x, y]

                # 計算 LVEF Volume
                minX, maxX = np.min(cnt_line[:, 0]),  np.max(cnt_line[:, 0])
                scale_cm = self.Radius / self.UnitCM

                r = ((maxX - minX) / 2) / scale_cm
                dh_scale = dh / scale_cm
                volume = r ** 2 * np.pi * dh_scale  # cm^3, 1cm^3 = 1ml
                LVVolume += volume
                # print(volume, 'cm\u00b3')

                # check
                # cv2.circle(check, (currX, currY), 2, (0, 0, 255), -1)
                # cv2.line(check, (0, int(bias_lr)), (800, int(lineY)), (0, 255-i*10, 0), 1)
                # check[mask_fill_cnt != 255] = [0, 0, 0]

        else:
            dh = (leftY - apexY) / 20

            for i in range(0, 19):
                mask_line = np.zeros(src.shape, np.uint8)

                bias_lr -= dh
                cv2.line(mask_line, (0, int(bias_lr)), (800, int(bias_lr)), (255, 255, 255), 1)
                mask_line[mask_fill_cnt != 255] = 0

                cnt_line, _ = cv2.findContours(mask_line, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnt_line = cnt_line[0].reshape(len(cnt_line[0]), -1)  # coordinate: [x, y]

                # 計算 LVEF Volume
                minX, maxX = np.min(cnt_line[:, 0]),  np.max(cnt_line[:, 0])
                scale_cm = self.Radius / self.UnitCM

                r = ((maxX - minX) / 2) / scale_cm
                dh_scale = dh / scale_cm
                volume = r ** 2 * np.pi * dh_scale  # cm^3, 1cm^3 = 1ml
                LVVolume += volume

                # check
                # cv2.circle(check, (apexX, int(bias_lr)), 2, (0, 0, 255), -1)
                # cv2.line(check, (0, int(bias_lr)), (800, int(bias_lr)), (0, 255-i*10, 0), 1)
                # check[mask_fill_cnt != 255] = [0, 0, 0]

        # check
        # ori = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
        # cv2.circle(check, (apexX, apexY), 5, (0, 255, 0), -1)
        # cv2.circle(check, (leftX, leftY), 5, (0, 0, 255), -1)
        # cv2.circle(check, (rightX, rightY), 5, (255, 0, 0), -1)
        # cv2.circle(check, (midX, midY), 5, (255, 255, 0), -1)
        # cv2.line(check, (leftX, leftY), (rightX, rightY), (255, 0, 255), 2)
        # cv2.line(check, (apexX, apexY), (midX, midY), (0, 255, 255), 2)

        # cv2.imshow('ori', ori)
        # cv2.imshow('mask_cnt', mask_cnt)
        # cv2.imshow('mask_fill_cnt', mask_fill_cnt)
        # cv2.imshow('check', check)
        # cv2.waitKey(0)

        # LVVolume = round(LVVolume, 3)
        # print(LVVolume, 'cm\u00b3')

        return round(LVVolume, 1)


# use
GTDir = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\Ground Truth\\00004042_110428_0999\\"
# HandleIOU(FrameCount=2, mask=np.full((600, 800), 255), GroundTruthDir=GTDir)
# score, frame = HandleIOU(
#     src=curr_frame,
#     FrameCount=curr_frame_count,
#     mask=binary_mask,
#     GroundTruthDir=GTDir
# )

# test
ImgPath = GTDir + "00004042_110428_0999_01.png"
Img = cv2.imread(ImgPath, 0)
t = LVEFInfo(GTDir, UnitCM=17, Radius=495, fps=47, BPM=81)
