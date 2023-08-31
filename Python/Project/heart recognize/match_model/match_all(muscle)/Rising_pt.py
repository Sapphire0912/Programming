import cv2
import numpy as np
import os

class Rising_pt(object):
    def __init__(self, C, I, R, A, S, sR, M):
        """
        C:  Center
        I:  Image
        R:  Radius
        A:  Angle
        S:  Standard Length
        sR: Score Radius
        M:  Mode
        """
        self.x      = C[0]
        self.y      = C[1]
        self.I = I
        self.R = R
        self.A = A
        self.S = S
        self.sR = sR
        self.M = M

    def search_pt(self):
        pt_lst = []
        div = int(360 / self.A)
        for i in range(0, div, 1):
            angle = self.A*i

            radians = np.radians(angle)
            sin = np.sin(radians)
            cos = np.cos(radians)

            div = self.R / self.S
            all_sc = []
            pt_temp= []
            for k in (0, div, 1):
                pt_x  = int(self.x + (self.S * k) * sin)
                pt_y  = int(self.y + (self.S * k) * cos)
                area_pixel = []
                for p in range(0, self.sR, 1):
                    x_p = self.sR-p
                    for q in range(0, x_p, 1):
                        area_pixel.append(self.I[pt_x + q][pt_y + p])
                        area_pixel.append(self.I[pt_x - q][pt_y + p])
                        area_pixel.append(self.I[pt_x - q][pt_y - p])
                        area_pixel.append(self.I[pt_x + q][pt_y - p])
                score = sum(area_pixel)
                all_sc.append(score)
                pt_temp.append((pt_x,pt_y))

            if self.M == 1:
                print(all_sc)
                add = all_sc.index(np.max(all_sc))
                pt_lst.append(pt_temp[add])
                print(pt_lst)
        return pt_lst


avi_path = list()
for root, dirs, file in os.walk('.\\test_video\\'):
    for f in file:
        avi_path.append('.\\test_video\\' + f)

for path in avi_path:
    video = cv2.VideoCapture(path)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cx, cy = width // 2, height // 2

    while True:
        ret, frame = video.read()

        if not ret:
            break

        TestClass = Rising_pt((cx, cy), frame, 180, 12, 18, 10, 1)
        test_list = TestClass.search_pt()
        print(test_list)
        cv2.waitKey(1000)


