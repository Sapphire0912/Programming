from sklearn.model_selection import train_test_split as tts
import os
import cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json


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

    # print('該類別的資料數量: ', len(curr_dir))
    # print('目前資料集的資料量: ', len(datasets))
    # print("當前類別標籤: %d " % (index + 1))

datasets = np.array(datasets, np.float32)
labels = np.array(labels, np.int32)

# print('dataset shape: ', datasets.shape)
# print('labels shape: ', labels.shape)
#
# # 訓練模型(採用 cv2 方式)
# # 拆分數據集(訓練 8, 測試 2)
x_train, x_test, y_train, y_test = tts(datasets, labels, test_size=0.2, random_state=76)
# print('訓練資料維度: ', x_train.shape)
# print('訓練標籤維度: ', y_train.shape)
# print('測試資料維度: ', x_test.shape)
# print('測試標籤維度: ', y_test.shape)
#
# svm = cv2.ml.SVM_create()
# svm.setType(cv2.ml.SVM_C_SVC)
# svm.setKernel(cv2.ml.SVM_LINEAR)
# svm.setC(0.1)
# svm.setGamma(1.0)
#
# st = time.time()
# svm.trainAuto(x_train, cv2.ml.ROW_SAMPLE, y_train)
# end = time.time()
#
# print('訓練模型時間: ', round(end - st, 2), '秒')
# print('使用模型類型: ', svm.getType())
# print('模型核心類型: ', svm.getKernelType())
# print('模型參數: ')
# print('C: ', svm.getC())
# print('Gamma: ', svm.getGamma())
#
model_path = './model_tts.xml'
# svm.save(model_path)

# 使用訓練好的模型
model = cv2.ml.SVM_load(model_path)

# 計算混淆矩陣
confusion_matrix = np.zeros((9, 9), np.int32)

# 計算拆分後的資料集每種類別的數量
curr_total_data = np.zeros(9, np.int32)
for i in y_test:
    curr_total_data[i - 1] += 1
print(curr_total_data)

for index in range(0, len(x_test)):
    feature = np.array([x_test[index]], np.float32)
    label = model.predict(feature)[1][0][0]

    true_label = y_test[index]
    confusion_matrix[true_label - 1, int(label) - 1] += 1


result = dict()
all_tp = 0
for c in range(0, len(confusion_matrix)):
    tp_fp = confusion_matrix[:, c]
    tp_fn = confusion_matrix[c, :]

    all_tp += confusion_matrix[c, c]
    accuracy = confusion_matrix[c, c] / curr_total_data[c]
    precision = confusion_matrix[c, c] / np.sum(tp_fp)
    recall = confusion_matrix[c, c] / np.sum(tp_fn)
    f1_score = 2 / (1 / precision + 1 / recall)

    result[str(c+1)] = {"Accuracy": accuracy, "Precision": precision, "Recall": recall, "F1Score": f1_score}

model_acc = all_tp / sum(curr_total_data)

with open('./cv2_svm_tts data pred_model_result_score.json', 'w+') as j:
    json.dump(result, j)

print('每個類別的資料: ', curr_total_data)
print("Result: \n", result)
print("模型正確率: ", model_acc)

# print("X 軸為預測標籤")
# print("Y 軸為實際標籤")
# print(confusion_matrix)
#
sns.set()
sns.heatmap(confusion_matrix, square=True, annot=True, cbar=True, fmt='d').invert_yaxis()
plt.title('tts confusion matrix')
plt.xlabel('predict value')
plt.ylabel('true value')
plt.show()


