import FileIO
import Preprocessing

from skimage.morphology import skeletonize
import numpy as np
import cv2


def ModifiedMeanFilter(src, ROI):
    """
    function:
        ModifiedMeanFilter(src): 對影像進行中值濾波, kernel size: 3x3 (self algorithm)

    parameters:
        src: original 3-channel image, np.ndarray.
        ROI: region of interest, binary image, np.ndarray.

    return:
        enhancedImg: enhanced image, gray scale.
        segmentImg: segmented image, binary scale.
    """

    y, x, _ = src.shape
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    gray = gray / 255

    enhancedImg = np.zeros(gray.shape, np.float)

    # convolution
    for i in range(1, x-1):
        for j in range(1, y-1):
            W = gray[j-1:j+2, i-1:i+2]
            avg = np.around(np.mean(W), decimals=6)

            if avg:
                alpha = W - avg  # reduce additive noise
                alpha[alpha <= 0] = 1  # avoid invalid value encountered in log10

                beta = np.log10(alpha) + avg  # reduce the multiplicative noise
                beta[beta == avg] = 0  # restore if alpha <= 0; log 1 = 0

                gamma = np.exp(beta)  # restore the original image
                gamma[gamma == 1] = 0  # restore if alpha <= 0; exp(0) = 1

                G_enhance = np.max(gamma)
                enhancedImg[j, i] = G_enhance

            else:
                enhancedImg[j, i] = 0

    # consider roi region
    _, roi_cnt = np.unique(ROI, return_counts=True)
    avg_enhanced = np.sum(enhancedImg) / roi_cnt[-1]
    print('avg_enhanced:', avg_enhanced)

    pre_segmentImg = enhancedImg.copy()
    pre_segmentImg[pre_segmentImg >= avg_enhanced] = 1
    pre_segmentImg[pre_segmentImg < avg_enhanced] = 0
    segmentImg = np.zeros(gray.shape, np.uint8)

    # convolution
    for i in range(1, x-1):
        for j in range(1, y-1):
            W_seg = pre_segmentImg[j-1:j+2, i-1:i+2]
            val, count = np.unique(W_seg, return_counts=True)

            if len(val) > 1:
                G_seg = 1 if count[1] > count[0] else 0
                segmentImg[j, i] = G_seg
            else:
                segmentImg[j, i] = 0

    segmentImg = segmentImg * 255
    enhancedImg = np.clip(enhancedImg * 255, 0, 255).astype(np.uint8)

    return enhancedImg, segmentImg


def ImageContrast(img, brightness=0, contrast=0):
    """
    ImageContrast(img, brightness=0, contrast=0):
        調整影像對比度 & 亮度

    parameters:
        img: 灰階圖像
        brightness: 亮度, 值越高整張圖片亮度越大否則反之, 默認 0
        contrast: 對比度, > 0 則對比越強烈, < 0 對比較不清晰, 默認 0
    """
    B = brightness / 255.0
    C = contrast / 255.0
    k = np.tan((45 + 44 * C) / 180 * np.pi)

    img = (img - 127.5 * (1 - B)) * k + 127.5 * (1 + B)
    img = np.clip(img, 0, 255).astype(np.uint8)
    return img


# load data
DirPath = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize2\\A4C TestData\\"
AVIPath = FileIO.AllFiles(DirPath + 'AVI Files', 'avi')

# find roi
roi, (ox, oy), radius = Preprocessing.ROI(AVIPath[0])

# use first video
# 1. image quality; current problem: enhanced image is not ideal result
video = cv2.VideoCapture(AVIPath[0])
# ret, frame = video.read()
# frame[roi != 255] = [0, 0, 0]
# enImg, segImg = ModifiedMeanFilter(frame, roi)
#
# cv2.imshow('enImg', enImg)
# cv2.imshow('segImg', segImg)
# cv2.imshow('frame', frame)
# cv2.waitKey(0)

enList, segList = list(), list()
contrastList = list()
medList, skeList = list(), list()

while True:
    ret, frame = video.read()

    if not ret:
        break

    frame[roi != 255] = [0, 0, 0]

    # handle speckle noise
    # 1. modified median blur
    # enImg, segImg = ModifiedMeanFilter(frame, roi)

    # enImg = cv2.cvtColor(enImg, cv2.COLOR_GRAY2BGR)
    # enList.append(enImg)
    # segImg = cv2.cvtColor(segImg, cv2.COLOR_GRAY2BGR)
    # segList.append(segImg)

    # 2. adjust contrast
    contrasted = ImageContrast(frame, 0, 70)
    gray = cv2.cvtColor(contrasted, cv2.COLOR_BGR2GRAY)
    med_blur = cv2.medianBlur(gray, ksize=5)

    # cv2.imshow('gray', gray)
    # cv2.imshow('med_blur', med_blur)

    _, thres = cv2.threshold(med_blur, 30, 255, cv2.THRESH_BINARY)
    thres_BGR = cv2.cvtColor(thres, cv2.COLOR_GRAY2BGR)

    skeleton = skeletonize(thres_BGR)
    skeleton = cv2.cvtColor(skeleton, cv2.COLOR_BGR2GRAY)

    skeleton[skeleton != 0] = 255
    skeleton = cv2.cvtColor(skeleton, cv2.COLOR_GRAY2BGR)
    skeList.append(skeleton)
    
    med_blur = cv2.cvtColor(med_blur, cv2.COLOR_GRAY2BGR)
    medList.append(med_blur)

    # cv2.imshow('thres', thres)
    # cv2.imshow('skeleton', skeleton)
    # cv2.waitKey(1000)
    # contrastList.append(contrasted2)
    pass

    # cv2.imshow('frame', frame)
    # cv2.imshow('enImg', enImg)
    # cv2.imshow('segImg', segImg)
    # cv2.waitKey(200)
    # pass

OutputPath = "E:\\MyProgramming\\Python\\Project\\implement\\heart recognize2\\A4C TestResult\\"

# FileIO.write_video(enList, DirPath + '_En.avi')
# FileIO.write_video(segList, DirPath + '_Seg.avi')
# FileIO.write_video(contrastList, OutputPath + '_contrast2.avi')
FileIO.write_video(skeList, OutputPath + "_ske.avi")
FileIO.write_video(medList, OutputPath + '_medblur.avi')
