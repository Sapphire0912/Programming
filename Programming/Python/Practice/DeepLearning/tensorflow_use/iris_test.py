import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn import datasets
from sklearn.model_selection import train_test_split as tts

# 使用 MLP 來對 iris 進行分類
# step1 prepare data
iris = datasets.load_iris()
x, y = iris.data, iris.target
# print(x.shape, y.shape)  # (150, 4) (150,)
# 有 150 筆資料, 4 個特徵

# 拿總數據的 20% 當測試資料
x_train, x_test, y_train, y_test = tts(x, y, test_size=0.2)

# 鳶尾花種類
category = len(np.unique(y))
# 特徵數
dim = x.shape[1]

# 獨熱編碼(所以 loss 要選擇 多分類損失函式)
y_train2 = tf.keras.utils.to_categorical(y_train, num_classes=category)
y_test2 = tf.keras.utils.to_categorical(y_test, num_classes=category)

# step2 create model
# assume layers = 3
model = tf.keras.models.Sequential()

# input layers
model.add(tf.keras.layers.Dense(10, activation=tf.nn.relu, input_dim=dim))

# hidden layers
model.add(tf.keras.layers.Dense(10, activation=tf.nn.relu))

# output layers
model.add(tf.keras.layers.Dense(category, activation=tf.nn.softmax))

# step3 compile
model.compile(
    optimizer='adam',
    loss=tf.keras.losses.categorical_crossentropy,
    metrics=['accuracy']
)

# step4 training
model.fit(x_train, y_train2, epochs=100, batch_size=12, verbose=1)

# step5 test
score = model.evaluate(x_test, y_test2, batch_size=12)
# print("score: ", score)

# step6 predict
prob = model.predict(x_test)
prob.astype(np.float)

pred = np.zeros(prob.shape, dtype=np.int)
for i in range(prob.shape[0]):
    index = np.argmax(prob[i])
    for j in range(prob.shape[1]):
        if j == index:
            pred[i, j] = 1
        else:
            pred[i, j] = 0

column = ['setosa', 'virginica', 'versicolor']

df_prob = pd.DataFrame(prob, columns=column, index=np.arange(1, 31))
df_pred = pd.DataFrame(pred, columns=column, index=np.arange(1, 31))
df_true = pd.DataFrame(y_test2, columns=column, index=np.arange(1, 31))
print("probability: \n", df_prob)
print("prediction: \n", df_pred)
print("true labels: \n", df_true)
