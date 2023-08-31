import FileIO
import numpy as np
import cv2
import matplotlib.pyplot as plt


def BPMToFrame(BPM, FPS):
    period_time = (60 / BPM) * FPS / 30  # 換成 fps=30
    period_frame = (60 / BPM) * FPS
    return period_time, int(period_frame)


path = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize\\System2\\alpha period\\"
imgList = FileIO.AllFiles(path, 'png')
BPMList = [75, 73, 73]  # Dicom Data: Heart Rate
FPSList = [47, 47, 51]  # Dicom Data: Cine Rate

for i, imgPath in enumerate(imgList):
    newImg = cv2.imread(imgPath, 0)
    h, w = newImg.shape

    # Ground Truth
    OriginalTime, OriginalPeriod = BPMToFrame(BPMList[i], FPSList[i])
    print(f'Original period frame count: {OriginalPeriod}, period time: {round(OriginalTime, 3)} s.')
    # -----

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

    for j, newX in enumerate(newX_sample):
        currYIndex = YIndex[XIndex == newX]
        newY_sample[j] = int(np.mean(currYIndex)) if len(currYIndex) > 0 else 0

    newData = np.vstack([newX_sample, newY_sample]).T
    # plt.scatter(newX_sample, newY_sample, color='red', s=10)
    # plt.plot(newX_sample, newY_sample, color='blue')
    # plt.show()
    # - 利用平均去除重複值 End.

    # - 利用已知的 BPM 轉成 frame count/period 後找最高和最低點
    # 由於資料有擴展 5 倍, frame count 要 * 5
    period_count = OriginalPeriod * 5
    ESVList, EDVList = list(), list()
    ESVValueList, EDVValueList = list(), list()

    for k in range(0, len(newX_sample), period_count):
        period_img = otsu[:, k:k+period_count]
        period_data = newData[k:k+period_count]
        ESV, EDV = (np.argmin(period_data[:, 1]) + k), (np.argmax(period_data[:, 1]) + k)
        ESVList.append(ESV)
        ESVValueList.append(newData[ESV, 1])
        EDVList.append(EDV)
        EDVValueList.append(newData[EDV, 1])

    # demo_otsu = cv2.flip(otsu, 0)
    fig, ax = plt.subplots(2)
    ax[0].set_title('original image')
    ax[0].set_xlabel('frame count * 5')
    ax[0].imshow(otsu, cmap='gray')
    ax[1].plot(newX_sample, newY_sample)
    ax[1].set_title(f'BPM: {BPMList[i]}, FPS: {FPSList[i]}, period frame count: {OriginalPeriod}')
    ax[1].scatter(ESVList, ESVValueList, color='red', s=100)
    ax[1].scatter(EDVList, EDVValueList, color='green', s=100)
    ax[1].legend(['signal', 'ESV', 'EDV'])
    plt.show()

    EDVFrame = np.array(EDVList) // 5
    ESVFrame = np.array(ESVList) // 5
    print(f'EDVFrame: {EDVFrame}')
    print(f'ESVFrame: {ESVFrame}')
    # - 利用已知的 BPM 轉成 frame count/period 後找最高和最低點 End.

    # - 對數位訊號做: 利用傅立葉變換取低頻的做法
    # 1. 水平切割成 5 等分
    # 確保每一等分一定同大小且 5 等分一定在中間(頂多誤差 1)
    # delta_y = (h % 10) // 2
    # each_step = h // 10
    # f, T = 30, 30 / 1024
    # N = 1024
    #
    # for each in range(delta_y, h, each_step):
    #     print(f'partition: {each // each_step + 1}')
    #
    #     maskY = (each <= newY_sample) & (newY_sample < (each + each_step))
    #     y_seq = newY_sample.copy()
    #     y_seq[~maskY] = each
    #
    #     # 傅立葉變換
    #     fftData = np.fft.fft(y_seq)
    #     x_freq = np.linspace(0, 1//(2*T), N//2)
    #     y_mag = 2.0/N * np.abs(fftData)  # magnitude
    #
    #     low_freq_index = np.argmax(y_mag[1:N//2])
    #     f_max_amp = x_freq[low_freq_index]
    #     # print(f'low freq index: {low_freq_index}')
    #     print(f'f: {f}')
    #     # print(f'sampling f: {f_max_amp}')
    #
    #     points = f / f_max_amp if f_max_amp != 0 else 0
    #     frame_period = points // 5
    #     time_period = frame_period / 30
    #     # print(f'points: {points}')
    #     print(f'frame period: {frame_period}')
    #     print(f'time period: {time_period}')
    #
    #     fig, ax = plt.subplots(2)
    #     ax[0].set_title(f'Original signal (current partition: from {each} to {each + each_step})')
    #     ax[0].plot(newX_sample, y_seq, color='blue')
    #     ax[0].set_facecolor('gray')
    #
    #     ax[1].set_title(f'Fourier transform: T=1/{f}, the number of sample={N}')
    #     ax[1].plot(x_freq[1:N//2], y_mag[1:N//2], color='cyan')
    #     ax[1].set_facecolor('gray')
    #     plt.show()
    # - 對數位訊號做: 利用傅立葉變換取低頻的做法 End.

    # cv2.imshow('newImg', newImg)
    # cv2.imshow('blur', blur)
    # cv2.imshow('closing', closing)
    # cv2.imshow('otsu', otsu)
    # cv2.waitKey(0)

    pass
