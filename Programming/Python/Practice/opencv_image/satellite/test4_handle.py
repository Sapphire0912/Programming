import cv2
import numpy as np


class Handle(object):
    def __init__(self, path):
        self.ori = cv2.imread(path)
        self.y, self.x, self.color = self.ori.shape
        self.preprocessed = None
        self.diff = None
        self.watershed = None

    def preprocess(self):
        gray = cv2.cvtColor(self.ori, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 0)

        cv2.imshow('blur', blur)
        self.preprocessed = blur

    def find_flatten(self):
        ori_cp = self.ori.copy()

        sobel = cv2.Sobel(self.preprocessed, ddepth=-1, dx=1, dy=1, ksize=5)
        scale = 8
        for y in range(0, self.y):
            for x in range(0, self.x):
                sobel[y, x] = ((sobel[y, x] + 1) // 8) * scale
        print(np.unique(sobel))
        pass

        # diff
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        erode = cv2.erode(self.preprocessed, kernel, iterations=1)
        dilate = cv2.dilate(self.preprocessed, kernel, iterations=1)
        diff = cv2.absdiff(erode, dilate)

        # watershed
        _, thres = cv2.threshold(self.preprocessed, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        morph = cv2.morphologyEx(thres, cv2.MORPH_OPEN, kernel, iterations=2)
        bg = cv2.dilate(morph, kernel, iterations=3)
        unknown = cv2.subtract(bg, diff)
        _, markers = cv2.connectedComponents(bg)
        markers = cv2.watershed(ori_cp, markers=markers)
        ori_cp[markers == -1] = [255, 0, 255]
        print(np.unique(markers))

        cv2.imshow('erode', erode)
        cv2.imshow('dilate', dilate)
        cv2.imshow('unknown', unknown)
        cv2.imshow('bg', bg)
        self.diff = diff
        self.watershed = ori_cp


if __name__ == '__main__':
    file = './test4.jpg'
    H = Handle(file)
    H.preprocess()

    H.find_flatten()
    cv2.imshow('diff', H.diff)
    cv2.imshow('watershed', H.watershed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

