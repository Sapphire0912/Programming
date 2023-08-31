import cv2
import numpy as np
import FileIO
from MuscleSampling import SplitContour

import matplotlib.pyplot as plt


class CardiacCycle(object):
    def __init__(self, VideoPath, ROI, LeftValvePos, RightValvePos):
        self.Path = VideoPath
        self.roi, (self.ox, self.oy), self.radius = ROI

        self.LeftValve = LeftValvePos
        self.RightValve = RightValvePos
        self.ROI_dy = 0

    def _FindCenter(self):
        Left, Right = self.LeftValve, self.RightValve
        # print(f'Left: {Left}')
        # print(f'Right: {Right}')

        meanX, meanY = 0, 0
        Y_coordList = list()  # 儲存所有 y 軸的座標 <- 目的為了找 一維影像的 ROI 高度範圍

        for ind, val in enumerate(Left):
            x_coord = (val[0] + Right[ind][0]) // 2  # x coordinate
            y_coord = val[1]  # y coordinate

            meanX += x_coord
            meanY += y_coord
            Y_coordList.append(y_coord)
        meanX = meanX // len(Left)
        meanY = meanY // len(Left)

        self.ROI_dy = max(Y_coordList) - min(Y_coordList)
        return meanX, meanY

    def Wave(self):
        Video = cv2.VideoCapture(self.Path)
        XPoint, YPoint = self._FindCenter()
        # print(XPoint, YPoint)

        # -- 利用與 ROI 的 ox, oy 和 Center Points 的斜率來定義角度
        slope = (YPoint - self.oy) / (XPoint - self.ox)
        b = self.oy - slope * self.ox
        YEnd = self.oy + self.radius
        XEnd = int((YEnd - b) / slope)

        height, width = int(Video.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(Video.get(cv2.CAP_PROP_FRAME_WIDTH))
        maskLine = np.zeros((height, width), np.uint8)
        cv2.line(maskLine, (self.ox, self.oy), (XEnd, YEnd), (255, 255, 255), 1)

        # 只取二尖瓣附近的範圍, 其餘的都 mask 處理掉
        maskLine[:YPoint-self.ROI_dy * 3, :] = 0
        maskLine[YPoint+self.ROI_dy:, :] = 0
        # -- 利用與 ROI 的 ox, oy 和 Center Points 的斜率來定義角度 End.

        # -- 取出 1D 影像
        frameList = list()
        frame_count = 0
        imgList = list()
        while 1:
            ret, frame = Video.read()

            if not ret:
                break

            frame_cp = frame.copy()
            frame_count += 1

            cv2.line(frame_cp, (self.ox, self.oy), (XEnd, YEnd), (0, 255, 0), 2)
            cv2.circle(frame_cp, (XPoint, YPoint), 5, (0, 0, 255), -1)

            frame[maskLine != 255] = [0, 0, 0]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            imgList.append(gray[maskLine == 255])

            cv2.putText(frame_cp, f'frame_count: {frame_count}', (60, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (255, 255, 255), 1)
            frameList.append(frame_cp)
            # cv2.imshow('frame_cp', frame)
            #
            # if cv2.waitKey(0) == ord('n'):
            #     continue
            # elif cv2.waitKey(0) == ord('q'):
            #     break

        imgArray = np.asarray(imgList).T
        # cv2.imshow('imgArray', imgArray)
        # cv2.waitKey(0)
        # -- 取出 1D 影像 End.

        # -- handle 1D image
        h, w = imgArray.shape  # w 是 frame count, h 是透過 ROI_dy 取的範圍

        # - 把影像的每一列(column), 擴展 5 倍, 為了將影像放大時可以知道具體的 frame count
        newImg = np.zeros((h, w * 5), np.uint8)

        for i in range(w):
            regImg = imgArray[:, i].reshape(1, h).T
            regImg = np.hstack([regImg, regImg, regImg, regImg, regImg])
            newImg[:, i * 5:(i+1) * 5] = regImg
        # wPath = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\alpha period\\"
        # name = self.Path.split('\\')[-1].replace('avi', 'png')
        # cv2.imwrite(wPath+name, newImg)
        # End.

        # 抓 contours 的做法 必須在瓣膜很清楚的情況下
        img_cp = newImg.copy()
        avg = int(cv2.mean(newImg)[0]) + 1
        newImg[newImg < avg] = 0
        blur = cv2.blur(newImg, (5, 5))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        closing = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel, iterations=1)
        _, otsu = cv2.threshold(closing, avg, 255, cv2.THRESH_OTSU)

        # - 利用平均去除重複值
        whiteRegion = np.argwhere(otsu == 255)
        YIndex, XIndex = whiteRegion[:, 0], whiteRegion[:, 1]
        newX_sample = np.arange(np.min(XIndex), np.max(XIndex) + 1)
        # newX_sample = np.arange(0, 1024)
        newY_sample = np.zeros(newX_sample.shape, np.int)

        for i, newX in enumerate(newX_sample):
            currYIndex = YIndex[XIndex == newX]
            newY_sample[i] = int(np.mean(currYIndex)) if len(currYIndex) > 0 else 0

        newData = np.vstack([newX_sample, newY_sample]).T
        # plt.scatter(newX_sample, newY_sample, color='red', s=10)
        # plt.plot(newX_sample, newY_sample, color='blue')
        # plt.show()
        # - 利用平均去除重複值 End.

        # - 利用已知的 BPM 轉成 frame count/period 後找最高和最低點
        # 由於資料有擴展 5 倍, frame count 要 * 5
        # period_count = OriginalPeriod * 5
        # ESVList, EDVList = list(), list()
        # ESVValueList, EDVValueList = list(), list()
        #
        # for k in range(0, len(newX_sample), period_count):
        #     period_img = otsu[:, k:k + period_count]
        #     period_data = newData[k:k + period_count]
        #     ESV, EDV = (np.argmin(period_data[:, 1]) + k), (np.argmax(period_data[:, 1]) + k)
        #     ESVList.append(ESV)
        #     ESVValueList.append(newData[ESV, 1])
        #     EDVList.append(EDV)
        #     EDVValueList.append(newData[EDV, 1])
        #
        # plt.plot(newX_sample, newY_sample)
        # plt.scatter(ESVList, ESVValueList, color='red', s=50)
        # plt.scatter(EDVList, EDVValueList, color='green', s=50)
        # plt.show()
        #
        # EDVFrame = np.array(EDVList) // 5
        # ESVFrame = np.array(ESVList) // 5
        # print(f'EDVFrame: {EDVFrame}')
        # print(f'ESVFrame: {ESVFrame}')
        # - 利用已知的 BPM 轉成 frame count/period 後找最高和最低點 End.

        # - 對數位訊號做: 利用傅立葉變換取低頻的做法
        # 1. 水平切割成 x 等分
        # 確保每一等分一定同大小且 x 等分一定在中間
        # f: Original signal frequency
        # T: Period
        delta_y = (h % 7) // 2
        each_step = h // 7
        f, T = 30, 30 / len(newX_sample)
        N = len(newX_sample)

        for each in range(delta_y, h, each_step):
            print(f'partition: {each // each_step + 1}')

            maskY = (each <= newY_sample) & (newY_sample < (each + each_step))
            y_seq = newY_sample.copy()
            y_seq[~maskY] = each
            y_seq[y_seq != each] = each + each_step

            # 傅立葉變換
            fftData = np.fft.fft(y_seq)
            x_freq = np.linspace(0, 1//(2*T), N//2)
            y_mag = 2.0/N * np.abs(fftData)  # magnitude

            # check
            print('frame count: ', (f / x_freq[1:N//2]) / 5)
            # print('time period: ', (f / x_freq[1:N//2]) / 150)

            low_freq_index = np.argmax(y_mag[1:N//2])
            f_max_amp = x_freq[low_freq_index + 1]
            # print(f'f: {f}')
            print(f'f_max_amp: {f_max_amp}')

            points = f / f_max_amp if f_max_amp != 0 else 0
            frame_period = points / 5
            time_period = frame_period / 30
            print(f'frame period: {frame_period}')
            print(f'time period: {time_period}')

            # fig, ax = plt.subplots(3)
            # ax[0].set_title(f'Original signal')
            # ax[0].plot(newX_sample, newY_sample)
            # ax[0].set_facecolor('gray')
            # ax[1].set_title(f'current partition: from {each} to {each + each_step}')
            # ax[1].plot(newX_sample, y_seq, color='blue')
            # ax[1].set_facecolor('gray')
            #
            # ax[2].set_title(f'Fourier transform: T={f}/{len(newX_sample)}, the number of sample={N}')
            # ax[2].plot(x_freq[1:N//2], y_mag[1:N//2], color='cyan')
            # ax[2].set_facecolor('gray')
            # plt.show()
        # - 對數位訊號做: 利用傅立葉變換取低頻的做法 End.

        # - 對影像做: 利用傅立葉變換取低頻的做法
        # 1. 水平切割成 5 等分
        # 確保每一等分一定同大小且 5 等分一定在中間(頂多誤差 1)
        # delta_y = (h % 5) // 2
        # each_step = h // 5
        #
        # for each in range(delta_y, h, each_step):
        #     each_img = otsu[each:each+each_step]
        #     fft_img = np.fft.fft2(each_img)
        #     fft_shift = np.fft.fftshift(fft_img)
        #
        #     if fft_shift.any():
        #         magnitude_spectrum = 20 * np.log(np.abs(fft_shift))
        #         fig, ax = plt.subplots(2)
        #         ax[0].imshow(each_img, cmap='gray')
        #         ax[0].set_title(f'partition image: {each} to {each + each_step}')
        #         ax[1].imshow(magnitude_spectrum, cmap='gray')
        #         ax[1].set_title('fourier transform')
        #         plt.show()

        # - 利用兩點梯度差的做法
        # gradList = np.zeros(newX_sample.shape, np.int)
        # for i in range(1, len(newX_sample)):
        #     P1X, P1Y = newX_sample[i - 1], newY_sample[i - 1]
        #     P2X, P2Y = newX_sample[i], newY_sample[i]
        #
        #     gradient = (P2Y - P1Y) / (P2X - P1X)
        #     gradList[i] = gradient  # 第一個點會是 0
        # # print(f'gradient: {gradList}')
        #
        # # 梯度下降最大值是 ESV 的時候 (每個 ESV 區間是一個週期)
        # ESV_Index = np.argwhere(gradList < -10) + 1
        # ESV_Index = ESV_Index.reshape(len(ESV_Index))
        #
        # # 在 ESV 的區間找出 EDV(y 軸最大值), 以及計算週期
        # EDV_Index = np.zeros(len(ESV_Index) - 1, np.int)
        # cycle = list()
        # for i in range(1, len(ESV_Index)):
        #     _index = np.argmax(newY_sample[ESV_Index[i - 1]:ESV_Index[i]]) + ESV_Index[i - 1]
        #     EDV_Index[i - 1] = _index
        #     cycle.append((ESV_Index[i] - ESV_Index[i - 1]) // 5)  # 已轉成 frame count
        # # print(EDV_Index, ESV_Index)
        #
        # # 計算週期, 以及將 Index 轉成 frame count
        # EDV_frame_count = EDV_Index // 5  # 由於當時擴展 5 倍, 現在要換回來
        # ESV_frame_count = ESV_Index // 5
        # mean_period_count = sum(cycle) // len(cycle)
        # print(f'EDV frame count: {EDV_frame_count}')
        # print(f'ESV frame count: {ESV_frame_count}')
        # print(f'cycle: {cycle}')
        # print(f'mean period count: {mean_period_count}')
        # - 利用兩點梯度差的做法 End.

        # - 採取訊號取樣的做法
        # assume:
        # windows = 200
        # stride = 50
        #
        # for step in range(0, len(newX_sample), stride):
        #     currX_windows = newX_sample[step:step+windows]
        #     currY_windows = newY_sample[step:step+windows]
        #     currWindows = np.vstack([currX_windows, currY_windows]).T
        #
        #     for compare_step in range(0, len(newX_sample), stride):
        #         comX_windows = newX_sample[compare_step:compare_step+windows]
        #         comY_windows = newY_sample[compare_step:compare_step+windows]
        #         comWindows = np.vstack([comX_windows, comY_windows]).T
        # - 採取訊號取樣的做法 End.

        # cv2.imshow('newImg', newImg)
        # cv2.imshow('blur', blur)
        # cv2.imshow('img_cp', img_cp)
        # cv2.imshow('closing', closing)
        # cv2.imshow('otsu', otsu)

        # wPath = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\Unit EARatio\\"
        # wPath2 = wPath + ' v2 fps10 ' + self.Path.split('\\')[-1]
        # FileIO.write_video(frameList, wPath2, fps=10)
        # cv2.imwrite(wPath2, imgArray)
        # cv2.waitKey(0)

        pass
