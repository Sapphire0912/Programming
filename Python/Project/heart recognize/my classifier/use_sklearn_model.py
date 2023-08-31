import os
import cv2
import numpy as np
import joblib


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


model = joblib.load("./sklearn_svc_model.xml")
target_dir = './original data/'
all_img = os.listdir(target_dir)

for file in all_img:
    img_path = target_dir + file

    ori = cv2.imread(img_path)
    data = adjust_img(ori, 0.1)
    feature = np.array([data], np.float32)
    label = model.predict(feature)[-1]

    write_path = './pred2/000%d' % label + '/' + file
    print('current writing path: ', write_path)
    cv2.imwrite(write_path, ori)
    pass
