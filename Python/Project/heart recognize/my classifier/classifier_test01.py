from sklearn.model_selection import train_test_split as tts
from sklearn.svm import SVC
from sklearn.manifold import Isomap
from sklearn.metrics import confusion_matrix, accuracy_score
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import seaborn as sns


# 已分類資料夾的絕對路徑
def read_file():
    """
    function:
        read_file(): 讀取目標資料夾的檔案, 回傳資料集和標籤提供給機器學習模型訓練

    parameter:
        None

    return:
        datasets: 儲存圖片的資料夾, 類型為 numpy
        labels: 儲存圖片對應的標籤, 類型為 numpy
    """

    path = 'E:/MyProgramming/Python/Project/implement/heart recognize/classified data/'
    dir_list = os.listdir(path)

    labels = list()
    datasets = list()
    for label_index in range(0, len(dir_list)):
        # 讀取每個已分類好的資料夾底下的檔案
        curr_files = os.listdir(os.path.join(path, dir_list[label_index]))

        for file in curr_files:
            # 使用 opencv 讀取影像, 並且儲存成 資料集 和 標籤
            file_path = os.path.join(path, dir_list[label_index]) + '/' + file

            ori = cv2.imread(file_path)
            ori = cv2.resize(ori, (80, 60), cv2.INTER_AREA)
            gray = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
            dim1 = gray.ravel()

            datasets.append(dim1)
            labels.append(label_index)

    datasets = np.array(datasets, np.int32)
    labels = np.array(labels, np.int32)

    return datasets, labels


def model(datasets, labels):
    """
    function:
        model(datasets, labels): 訓練機器模型並且將模型打包成 xml

    parameter:
        datasets: 資料集
        labels: 標籤

    method:
        pre: 使用 train_test_split 拆分資料集
        1. manifold(Isomap)
        2. SVM(SVC)

        wait

    return:
        ml_model: 機器學習模型
    """

    dataset, labels = datasets, labels
    print("dataset shape: ", dataset.shape, "labels shape: ", labels.shape)
    # 降維
    # iso = Isomap(n_components=2)
    # iso.fit(datasets)
    # rd_datasets = iso.transform(datasets)
    # print(rd_datasets.shape)

    # 拆分資料集
    # x_train, x_test, y_train, y_test = tts(dataset, labels, test_size=0.2)
    # print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

    # 訓練模型
    ml_model = SVC(kernel='rbf', C=1, gamma='auto')
    ml_model.fit(dataset, labels)

    return ml_model


def predict(mods, labels):
    """
    function:
        predict(mod): 透過訓練好的模組來分類標籤

    parameter:
        mods: ML 訓練的模型
        labels: 實際的標籤

    return:
        None
    """
    target_path = 'E:/MyProgramming/Python/Project/implement/heart recognize/my classifier/original data/'
    target = os.listdir(target_path)

    datasets = list()
    for file in target:
        file_path = target_path + file
        ori = cv2.imread(file_path)
        ori = cv2.resize(ori, (80, 60), cv2.INTER_AREA)
        gray = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
        dim1 = gray.ravel()

        datasets.append(dim1)

    datasets = np.array(datasets)
    # iso = Isomap(n_components=2)
    # iso.fit(datasets)
    # rd_datasets = iso.transform(datasets)
    # print(rd_datasets.shape)

    pred = mods.predict(datasets)
    confusion_mat = confusion_matrix(pred, labels)
    print("Accuracy: ", accuracy_score(pred, labels))
    print(confusion_mat)

    TP, FP, TN, FN = 0, 0, 0, 0
    for index in range(0, len(confusion_mat)):
        TP += confusion_mat[index, index]

    print("Acc: ", TP / np.sum(confusion_mat))

    # 視覺化
    # sns.set()
    # sns.heatmap(confusion_mat, square=True, annot=True, cbar=True)
    # plt.title('Accuracy: {}'.format(accuracy_score(pred, labels)))
    # plt.xlabel('predicted value')
    # plt.ylabel('true value')
    # plt.show()
    pass


if __name__ == '__main__':
    data, label = read_file()
    mod = model(data, label)
    predict(mod, label)

