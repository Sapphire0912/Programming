import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import signal
import numpy as np
import scipy as sp
import glob as gb
import cv2


video_dir ="D:\\System\\Result\\demo\\"
video_paths = gb.glob(video_dir+"*.avi")

for path in video_paths:
    name = path.split("\\")[-1]

    cap = cv2.VideoCapture(path)
    FPS = int(cap.get(cv2.CAP_PROP_FPS))
    count = 0
    LV_vol = []

    while(cap.isOpened()):
        count += 1
        ret, frame = cap.read()

        if not ret:
            break
        frame_gr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, frame_thres = cv2.threshold(frame_gr, 50, 255, cv2.THRESH_BINARY)
        cnt, hierarchy = cv2.findContours(frame_thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.imshow("test",frame_thres)
        for c in cnt:

            area = cv2.contourArea(c)
            LV_vol.append(area)

        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:
            break
        elif key == ord(' '):
            while cv2.waitKey(1) != ord(' '):
                pass
    frame_cnt = [i for i in range(len(LV_vol))]
    # plt.plot(frame_cnt, LV_vol)

    y1 = sp.signal.medfilt(LV_vol, 7)
    # print(LV_size)
    sig_fft = fftpack.fft(y1)
    power = np.abs(sig_fft) ** 2

    # The corresponding frequencies
    sample_freq = fftpack.fftfreq(len(y1), d=7)
    pos_mask = np.where(sample_freq > 0)
    freqs = sample_freq[pos_mask]
    peak_freq = freqs[power[pos_mask].argmax()]
    np.allclose(peak_freq, 1. / 40)
    high_freq_fft = sig_fft.copy()
    high_freq_fft[np.abs(sample_freq) > (peak_freq * 1.7)] = 0
    filtered_sig = fftpack.ifft(high_freq_fft)
    plt.figure(figsize=(6, 5))
    plt.plot(frame_cnt, LV_vol, label='Original signal')
    plt.plot(frame_cnt, filtered_sig, linewidth=2, label='Filtered signal')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')

    plt.legend(loc='best')

    # plt.plot(frame_cnt, y1, linewidth=2, color='g')

    a = np.diff(np.sign(np.diff(filtered_sig))).nonzero()[0] + 1  # local min & max
    b = (np.diff(np.sign(np.diff(filtered_sig))) > 0).nonzero()[0] + 1  # local min
    c = (np.diff(np.sign(np.diff(filtered_sig))) < 0).nonzero()[0] + 1  # local max
    # +1 due to the fact that diff reduces the original index number

    # plot
    min_p = []
    max_p = []
    for i in range(0, len(frame_cnt), 1):
        min_p.append(None)
        max_p.append(None)

    for k in b:
        min_p[k] = filtered_sig[k]
    for q in c:
        max_p[q] = filtered_sig[q]

    plt.plot(frame_cnt, min_p, "o", label="min", color='b')
    plt.plot(frame_cnt, max_p, "o", label="max", color='r')

    plt.savefig("D:\\System\\demo\\" + name + ".png")
    print(min_p)
    print(max_p)
    plt.show()
    plt.clf()
