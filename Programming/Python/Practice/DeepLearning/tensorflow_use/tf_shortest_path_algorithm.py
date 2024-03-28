import tensorflow as tf
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split as tts
import matplotlib.pyplot as plt

# 用 iris 數據集做測試
iris = load_iris()
x, y = iris.data, iris.target
# print(x.shape, y.shape)

x_train, x_test, y_train, y_test = tts(x, y, test_size=0.2)

category = len(np.unique(y))
dim = x.shape[1]  # feature 數量是 input layers dim

model = tf.keras.models.Sequential()
# input
model.add(
    tf.keras.layers.Dense(units=10, activation=tf.nn.relu, input_dim=dim)
)
# hidden
model.add(
    tf.keras.layers.Dense(units=10, activation=tf.nn.relu)
)
# output
model.add(
    tf.keras.layers.Dense(category, activation=tf.nn.softmax)
)

# model.compile(
#     optimizer='adam',
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )
#
# history = model.fit(
#     x_train, y_train,
#     epochs=100,
#     batch_size=64
# )

# 圖形化顯示訓練過程
# history.history['accuracy'] 顯示訓練時的正確率, loss 為損失率
# plt.title('iris datasets: model accuracy')
# plt.plot(history.history['accuracy'])
# plt.plot(history.history['loss'])
# plt.xlabel('epoch')
# plt.ylabel('acc & loss')
# plt.legend(['acc', 'loss'], loc='upper left')
# plt.show()


# 深度學習最佳化 最短路徑演算法(shortest-path algorithm)
# 調整 optimizer(優化器)參數, 常見的有:
# sgd, RMSprop, adagrad, adadelta, adam, adamax, nadam...etc
# 各演算法之間差別, 需要去參考其他資料或者找論文會有更詳細的解說

# 1. Adam
learning_rate = 0.01
# opt1 = tf.keras.optimizers.Adam(lr=learning_rate)
# model.compile(
#     optimizer=opt1,
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )
# history = model.fit(
#     x_train, y_train,
#     epochs=400,
#     batch_size=16
# )

# print(history.history.keys())
# plt.title('Adam model acc & loss')
# plt.xlabel('epoch')
# plt.ylabel('acc & loss')
# plt.plot(history.history['accuracy'])
# plt.plot(history.history['loss'])
# plt.legend(['acc', 'loss'], loc='lower right')
# plt.show()

# 2. SGD
# opt2 = tf.keras.optimizers.SGD(lr=learning_rate)
# model.compile(
#     optimizer=opt2,
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )
# history2 = model.fit(
#     x_train, y_train,
#     epochs=400,
#     batch_size=16
# )
# plt.title('SGD model acc & loss')
# plt.xlabel('epoch')
# plt.ylabel('acc & loss')
# plt.plot(history2.history['accuracy'])
# plt.plot(history2.history['loss'])
# plt.legend(['acc', 'loss'], loc='lower right')
# plt.show()

# 3. RMSprop
# opt3 = tf.keras.optimizers.RMSprop(lr=learning_rate)
# model.compile(
#     optimizer=opt3,
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )
# history3 = model.fit(
#     x_train, y_train,
#     epochs=400,
#     batch_size=16
# )
# plt.title('RMSprop model acc & loss')
# plt.xlabel('epoch')
# plt.ylabel('acc & loss')
# plt.plot(history3.history['accuracy'])
# plt.plot(history3.history['loss'])
# plt.legend(['acc', 'loss'], loc='lower right')
# plt.show()

# 4. Adagrad
# opt4 = tf.keras.optimizers.Adagrad(lr=learning_rate)
# model.compile(
#     optimizer=opt4,
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )
# history4 = model.fit(
#     x_train, y_train,
#     epochs=400,
#     batch_size=16
# )
# plt.title('Adagrad model acc & loss')
# plt.xlabel('epoch')
# plt.ylabel('acc & loss')
# plt.plot(history4.history['accuracy'])
# plt.plot(history4.history['loss'])
# plt.legend(['acc', 'loss'], loc='lower right')
# plt.show()

# 5. Adadelta (學習速度較差, 在這個數據集用將近10倍學習次數, 才達到相同的結果)
# opt5 = tf.keras.optimizers.Adadelta(lr=learning_rate)
# model.compile(
#     optimizer=opt5,
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )
# history5 = model.fit(
#     x_train, y_train,
#     epochs=400,
#     batch_size=16
# )
# plt.title('Adadelta model acc & loss')
# plt.xlabel('epoch')
# plt.ylabel('acc & loss')
# plt.plot(history5.history['accuracy'])
# plt.plot(history5.history['loss'])
# plt.legend(['acc', 'loss'], loc='lower right')
# plt.show()

# 6. Nadam
# opt6 = tf.keras.optimizers.Nadam(lr=learning_rate)
# model.compile(
#     optimizer=opt6,
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )
# history6 = model.fit(
#     x_train, y_train,
#     epochs=400,
#     batch_size=16
# )
# plt.title('Nadam model acc & loss')
# plt.xlabel('epoch')
# plt.ylabel('acc & loss')
# plt.plot(history6.history['accuracy'])
# plt.plot(history6.history['loss'])
# plt.legend(['acc', 'loss'], loc='lower right')
# plt.show()

# 7. Momentum(在 SGO 裡面的參數調整)
# opt7 = tf.keras.optimizers.SGD(lr=learning_rate, momentum=0.9)
# model.compile(
#     optimizer=opt7,
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy']
# )
# history7 = model.fit(
#     x_train, y_train,
#     epochs=400,
#     batch_size=16
# )
# plt.title('Momentum model acc & loss')
# plt.xlabel('epoch')
# plt.ylabel('acc & loss')
# plt.plot(history7.history['accuracy'])
# plt.plot(history7.history['loss'])
# plt.legend(['acc', 'loss'], loc='lower right')
# plt.show()


# 特徵值數據標準化、歸一化
# 歸一化(把數據轉換成 0~1 之間)
# 1. 線性變換 y = (x - min) / (max - min)
# 2. 對數轉換 y = log(x)
# 3. 反餘切 y = arctan(x) * 2 / pi
# 4. 等比例縮放 [-1, 1] 之間的值

# 標準化:
# 1. 平均值差異 y = (x - mean) / std
# 2. 線性變換 y = (x - min) / (max - min) * (new_max - new_min) + new_min
# 3. 小數規範化 y = x / 10^j
# 4. 羅吉斯模式 new = 1 / (1 + exp(-x))

# 或者使用 sklearn.preprocessing 的 MinMaxScalar()


# 最佳化-學習率
# learning rate 越小, 需要的訓練次數要越多; 學習率大小取決於標籤數字的差異性, 若差異小則學習率調小

# 編譯模型的 metrics 指標
# 迴歸 regression metric
# 均方誤差, 平均絕對誤差, 平均絕對百分比誤差, 餘弦相似度
# 分類 classification metric
# 二進制精度(acc, binary_accuracy), 分類準確度(acc, categorical_accuracy),
# 稀疏分類精度(sparse_categorical_accuracy), 前k個分類精度(top_k_categorical_accuracy),
# 稀疏的前k個分類精度(sparse_top_k_categorical_accuracy)