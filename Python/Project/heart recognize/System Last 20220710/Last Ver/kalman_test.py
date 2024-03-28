import numpy as np
import matplotlib.pyplot as plt
import random

class KalmanFilterModel:
    def __init__(self, X,Q,R):
        """
        :param X: 物件狀態，多維
        :var F: 狀態轉換矩陣
        :var P: 共異變數，計算Q、R權重
        :var Q: 預估值誤差
        :var R: 測量值誤差
        :var H: 測量值矩陣
        :var I: 用於扣除Kalman gain，來更新P
        """
        self.value_length = len(X)
        self.X = np.append(X, [0] * self.value_length)
        self.F = np.eye(self.value_length * 2) + np.diag([1] * self.value_length, self.value_length)
        self.P = np.diag([0.01] * (self.value_length * 2))
        self.Q = np.diag([Q] * (self.value_length * 2))
        self.R = np.diag([R] * self.value_length)
        self.H = np.zeros((self.value_length, self.value_length * 2)) # 測量值矩陣
        for i in range(self.value_length):
            self.H[i][i] = 1
        self.I = np.eye(self.value_length * 2)

    def predict(self):
        # X(k|k-1) = F X(k-1|k-1) + B U(k) ...(1) B、U 暫無設定
        return self.H.dot(self.F.dot(self.X))

    def update(self, Z):
        # 1. 預測
        self.R = abs(np.diag(self.predict() - Z))
        self.X = np.dot(self.F, self.X)
        # P(k|k-1) = F P(k-1|k-1) F.T + Q ...(2)
        self.P = self.F.dot(self.P.dot(self.F.T)) + self.Q
        # 2. 更新
        # Kg(k) = P(k|k-1) H.T / (H P(k|k-1) H.T + R) ...(4)
        Kg = self.P.dot(self.H.T).dot(np.linalg.inv(self.H.dot(self.P.dot(self.H.T)) + self.R))
        # X(k|k) = X(k|k-1) + Kg(k) (Z(k) - H X(k|k-1)) ...(3)
        self.X = self.X + Kg.dot(Z - self.H.dot(self.X))
        # P(k|k) = (I - Kg(k) H) P(k|k-1) ...(5)
        self.P = (self.I - Kg.dot(self.H)).dot(self.P)
        return self.H.dot(self.X)

# groundTruth = np.genfromtxt('data/groundTruth.csv', delimiter=',', skip_header=1)
# measurmens = np.genfromtxt('data/measurmens.csv', delimiter=',', skip_header=1)
# groundTruth = []
# kalman_result = []
# r = []

# for rr in r:
#     rr = KalmanFilterModel([0], Q=1, R=1)
#     r.append(rr)
#     # for i in range(100):
#     Z = [random.random(),random.random()]
#     # predict_result.append(rr.predict())
#     res = rr.update(Z)
#     print(Z, res)
#     kalman_result.append(res)
#     groundTruth.append(Z)
#
# kalman_result = np.array(kalman_result)
# groundTruth = np.array(groundTruth)
# predict_result = np.array(predict_result)

# plt.plot(groundTruth[:, 0], groundTruth[:, 1], color='#9D9D9D')
# plt.plot(kalman_result[:, 0], kalman_result[:, 1], color='#FF5500')
# plt.plot(measurmens[:, 0], measurmens[:, 1], color='#000079')
# plt.show()
#
# import cv2
# bx, by = None, None
# kx, ky = None, None
# rr = None
# drawing = False # 如果按下滑鼠，則為真
# c = 0
# out = None
# def draw_circle(event,x,y,flags,param):
#     global drawing, bx, by, kx, ky, rr, c, img, out
#     if event == cv2.EVENT_LBUTTONDOWN:
#
#         drawing = True
#         rr = KalmanFilterModel([x, y],1,10)#P,Q
#         # print(rr)
#         bx, by = x, y
#         kx, ky = x, y
#         # out = cv2.VideoWriter("test.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (960, 540))
#     elif event == cv2.EVENT_MOUSEMOVE:
#         if drawing:
#             c += 1
#             if c % 30 == 0:
#                 x, y = [x+ np.random.randint(-50, 50, 1)[0], y + np.random.randint(-50, 50, 1)[0]]
#
#             res = np.int32(rr.update([x, y]))
#             print(res)
#             cv2.line(img, (bx, by), (x, y), (200, 200, 200), 1)
#             cv2.line(img, (kx, ky), (res[0], res[1]), (255, 0, 0), 2)
#             kx, ky = res[0], res[1]
#             bx, by = x, y
#             # out.write(img)
#     elif event == cv2.EVENT_LBUTTONUP:
#         img = np.full((600, 800, 3), 255, np.uint8)
#         drawing = False
#         # print(drawing)
#         # out.release()
#
# img = np.full((600, 800, 3), 255, np.uint8)
# cv2.namedWindow('image')
# cv2.setMouseCallback('image', draw_circle)
#
# while(1):
#     cv2.imshow('image',img)
#     if cv2.waitKey(20) & 0xFF == 27:
#         break
# cv2.destroyAllWindows()
#
