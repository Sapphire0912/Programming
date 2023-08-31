import os
import cv2
import numpy as np
from sklearn.svm import SVC
import joblib
import time


def adjust_img(img, scale=0.1):
    """
    function(img[, scale=0.1]):
        按照 scale 調整原始圖片的比例, 轉成灰階後展開為一維陣列

    return:
        gray.ravel()
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    y, x = gray.shape
    shape = (int(x * scale), int(y * scale))
    gray = cv2.resize(gray, shape, cv2.INTER_AREA)
    return gray.ravel()


# 建立資料集和標籤
path = 'E:/MyProgramming/Python/Project/implement/heart recognize/classified data/'
dir_list = os.listdir(path)

labels = list()
datasets = list()
for index in range(0, len(dir_list)):
    curr_dir = os.listdir(path + dir_list[index])

    for file in curr_dir:
        img_path = path + '/' + dir_list[index] + '/' + file
        ori = cv2.imread(img_path)
        data = adjust_img(ori, 0.1)
        datasets.append(data)
        labels.append(index + 1)

    print('該類別的資料數量: ', len(curr_dir))
    print('目前資料集的資料量: ', len(datasets))
    print("當前類別標籤: %d " % (index + 1))

datasets = np.array(datasets, np.float32)
labels = np.array(labels, np.int32)

print('dataset shape: ', datasets.shape)
print('labels shape: ', labels.shape)

# 訓練模型(採用 cv2 方式)
# svm = cv2.ml.SVM_create()
# svm.setType(cv2.ml.SVM_C_SVC)
# svm.setKernel(cv2.ml.SVM_LINEAR)
# svm.setC(0.1)
# svm.setGamma(1.0)
#
# st = time.time()
# svm.trainAuto(datasets, cv2.ml.ROW_SAMPLE, labels)
# end = time.time()
#
# print('訓練模型時間: ', round(end - st, 2), '秒')
# print('使用模型類型: ', svm.getType())
# print('模型核心類型: ', svm.getKernelType())
# print('模型參數: ')
# print('C: ', svm.getC())  # C:  62.5
# print('Gamma: ', svm.getGamma())
# model_path = './model.xml'
# svm.save(model_path)

# 訓練模型 採用 sklearn 方法
st = time.time()
model = SVC(kernel='linear', C=62.5, gamma=1)
print(model)
model.fit(datasets, labels)
end = time.time()
print('訓練模型時間: ', round(end - st, 2), '秒')
joblib.dump(model, './sklearn_svc_model.xml')

