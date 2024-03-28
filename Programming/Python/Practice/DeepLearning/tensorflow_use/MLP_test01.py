import tensorflow as tf
import numpy as np

# MLP (Multi-Layers Perceptron)
# 1. prepare data
# 2. create model
# 3. compile
# 4. training
# 5. test(evaluation accuracy)
# 6. prediction

# step 1
x1 = np.random.random((500, 1))
x2 = np.random.random((500, 1)) + 1
x_train = np.concatenate((x1, x2))
# print(x_train.shape)  # (1000, 1)

y1 = np.zeros((500, ), dtype=np.int)
y2 = np.ones((500, ), dtype=np.int)
y_train = np.concatenate((y1, y2))
# print(y_train.shape)  # (1000,)

# step 2
# 建立類神經的模型
model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Dense(10, activation=tf.nn.relu, input_dim=1),  # 10個神經點, 輸入一維陣列
        tf.keras.layers.Dense(10, activation=tf.nn.relu),  # 10個神經點, 使用 relu 演算法
        tf.keras.layers.Dense(2, activation=tf.nn.softmax)  # 2 種答案, 用 softmax 演算法
    ]
)

# step 3
model.compile(
    optimizer='adam',  # 使用 adam 最佳化
    loss='sparse_categorical_crossentropy',  # 損失率的處理方式
    metrics=['accuracy']  # 設定編譯處理時的指標以正確率為主
)

# step 4
model.fit(
    x=x_train, y=y_train,
    epochs=20,  # 設定訓練次數(機器學習次數)
    batch_size=128  # 設定每次訓練的資料筆數
)

# step 5
x_test = np.array([[0.22], [0.31], [1.22], [1.33]])
y_test = np.array([0, 0, 1, 1])
score = model.evaluate(x_test, y_test, batch_size=128)  # 計算測試正確率
print("score: ", score)
# score:  [0.3035516142845154, 1.0] 代表 損失率為 0.303, 正確率為 1.0

# step 6
# predict method 1
predict = model.predict(x_test)
# print("predict: \n", predict)  # 第一筆資料為預測 0 的機率, 第二筆資料為預測 1 的機率
# [[0.7268085  0.2731915]
#  [0.7283009  0.27169907]
# [0.28033206 0.719668]
# [0.22609927 0.77390075]]
# 找最大值就可以找出最佳答案

for i in range(len(predict)):
    s = np.argmax(predict[i])
    print("Ans:", end=str(s) + ' ')
print()

# predict method 2
predict2 = model.predict_classes(x_test)  # 取得預測答案
print("predict_classes: ", predict2)
print("y_test: ", y_test)
print(y_test == predict2)
