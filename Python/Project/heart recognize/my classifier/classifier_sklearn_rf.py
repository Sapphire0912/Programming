import os
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
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

# 訓練模型 採用 RandomForest 方法
st = time.time()
model = RandomForestClassifier()
print(model)
model.fit(datasets, labels)
end = time.time()
print('訓練模型時間: ', round(end - st, 2), '秒')
# joblib.dump(model, './sklearn_random forest_model.xml')

