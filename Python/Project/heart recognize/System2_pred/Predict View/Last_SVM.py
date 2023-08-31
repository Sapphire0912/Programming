import os
import cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def AllFiles(DirPath, ext):
    targetList = list()
    for root, dirs, files in os.walk(DirPath):
        for f in files:
            if f[-len(ext):] == ext:
                targetList.append(os.path.join(root, f))
    return targetList


def preprocess(PathList, GT_dict):
    # img resize to 80*60. flatten -> 4800
    xData = np.zeros((len(PathList), 4800), np.float32)
    yData = np.zeros(len(PathList), np.int)

    for i, p in enumerate(PathList):
        filename = str(p.split('\\')[-1])

        # resize img
        img = cv2.imread(p, 0)  # gray
        img = cv2.resize(img, (80, 60), cv2.INTER_AREA)
        img = img.ravel()
        xData[i] = img
        yData[i] = GT_dict[filename]

    return xData, yData


DatasetsDir = ".\\Train\\"
DatasetsPath = AllFiles(DatasetsDir, 'png')
# print(len(DatasetsPath))  # 6762

# split datasets
trainPath, testPath = train_test_split(DatasetsPath, test_size=0.2)
# print(len(trainPath), len(testPath))  # 5409 1353

# create ground truth label
GTDir = ".\\Ground Truth\\"
GTDict = dict()

GTPath = AllFiles(GTDir, 'png')
# print(len(GTPath))  # 6762

for path in GTPath:
    LabelName = int(str(path.split('\\')[2]).split('_')[0])
    FileName = str(path.split('\\')[-1])
    GTDict[FileName] = LabelName  # filename: label

# create train/test label and preprocess
print('Create train/test label and preprocess...')
xtrain, ytrain = preprocess(trainPath, GTDict)
xtest, ytest = preprocess(testPath, GTDict)
# print(xtrain.shape, ytrain.shape, xtest.shape, ytest.shape)  # (5409, 4800) (5409,) (1353, 4800), (1353,)

# create model
print('Create SVM model...')
svm = cv2.ml.SVM_create()
svm.setType(cv2.ml.SVM_C_SVC)
svm.setKernel(cv2.ml.SVM_LINEAR)

svm.trainAuto(xtrain, cv2.ml.ROW_SAMPLE, ytrain)

# save model
modelPath = ".\\last_svm.xml"
svm.save(modelPath)

# prediction and confusion matrix
print('Prediction...')
PredictDir = ".\\Predict\\"
model = cv2.ml.SVM_load(modelPath)
predict = np.zeros(len(testPath))
Confusion_matrix = np.zeros((9, 9), np.int)

for i, testData in enumerate(xtest):
    testData = np.array([testData], np.float32)
    prediction = int(model.predict(testData)[1][0][0])
    predict[i] = prediction

    FileName = str(testPath[i].split('\\')[-1])
    writePath = PredictDir + f'000{prediction}\\{FileName}'
    cv2.imwrite(writePath, cv2.imread(testPath[i]))

    Confusion_matrix[ytest[i] - 1, prediction - 1] += 1
# ytest is GT, predict is pred

ShowNameList = ["A5C", "A4C", "A2C", "ALA", "PSA (aortic valve)",
                "PSA (papillary muscle)", "PSA (near apex)", "PSA (mitral valve)", "PLA"]
sns.set()
sns.heatmap(Confusion_matrix, square=True, annot=True, cbar=True, fmt='d')
plt.title('confusion matrix')
plt.xlabel('Predictions')
plt.xticks(np.arange(0, 9), ShowNameList, rotation=90)
plt.ylabel('Ground Truth')
plt.yticks(np.arange(0, 9), ShowNameList, rotation=0)
plt.show()
