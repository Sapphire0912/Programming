import cv2
import sys
import numpy as np

sys.path.append("..")
from alg import my_alg


def preprocessing(ori):
    cv2.imshow("ori", ori)
    ori_cp = ori.copy()

    blur = cv2.GaussianBlur(ori, (7, 7), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask_Gr = my_alg.colorRange(hsv, 'gray', optrange=None)
    mask_Bl = my_alg.colorRange(hsv, 'black', optrange=None)
    img_mask = mask_Gr + mask_Bl
    ori_cp[img_mask != 255] = [0, 0, 0]

    gray = cv2.cvtColor(ori_cp, cv2.COLOR_BGR2GRAY)

    sobel = cv2.Sobel(gray, ddepth=-1, dx=1, dy=1, ksize=3)
    # thres1, thres2, method = my_alg.adjust_threshold(
    #     img=sobel,
    #     name='adj thres',
    #     param1='thres1',
    #     param2='thres2',
    #     method=cv2.THRESH_BINARY
    # )
    thres1, thres2 = 90, 255
    method = cv2.THRESH_BINARY

    _, thres = cv2.threshold(sobel, thres1, thres2, method)
    houghsP = my_alg.adjust_HoughLineSP(
        ori=ori,
        img=sobel,
        name='adj hough',
        rho=1,
        theta=np.pi/180,
        line_thres=(0, 500),
        minLineLength=(0, 500),
        maxLineGap=(0, 100)
    )

    print(houghsP.shape)
    # mask = np.zeros(ori.shape[:2], np.uint8)
    # bgdModel = np.zeros((1, 65), np.float64)
    # fgdModel = np.zeros((1, 65), np.float64)
    #
    # rect = (50, 50, 450, 290)
    # cv2.grabCut(ori, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    #
    # mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    # ori = ori * mask2[:, :, np.newaxis]
    cv2.imshow("mask_ori", ori_cp)
    cv2.imshow('gray', gray)
    cv2.imshow('sobel', sobel)
    cv2.imshow('adj thres', thres)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    path = './hole01.jpg'
    file = cv2.imread(path)
    preprocessing(file)
