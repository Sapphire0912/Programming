import numpy as np
import tensorflow as tf

# 在 tensorflow 上, 使用 to_categorical 可以將 label 轉成 One-hot encoding
x1 = np.random.random((500, 1))
x2 = np.random.random((500, 1)) + 1
x_train = np.concatenate((x1, x2))

y1 = np.zeros((500, ), np.int)
y2 = np.ones((500, ), np.int)
y_train = np.concatenate((y1, y2))

# 將 訓練結果轉成獨熱編碼
y_train2 = tf.keras.utils.to_categorical(y_train, num_classes=2)
model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Dense(10, activation=tf.nn.relu, input_dim=1),  # 10個神經點, 輸入一維陣列
        tf.keras.layers.Dense(10, activation=tf.nn.relu),  # 10個神經點, 使用 relu 演算法
        tf.keras.layers.Dense(2, activation=tf.nn.softmax)  # 2 種答案, 用 softmax 演算法
    ]
)

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.categorical_crossentropy,  # 多分類別的損失函式(若使用獨熱編碼需要)
    metrics=['accuracy']
)

model.fit(
    x=x_train, y=y_train2,
    epochs=20, batch_size=128
)

x_test = np.array([[0.22], [0.31], [1.22], [1.33]])
y_test = np.array([0, 0, 1, 1])
y_test2 = tf.keras.utils.to_categorical(y_test, num_classes=2)  # 將測試結果轉成獨熱編碼

score = model.evaluate(x_test, y_test, batch_size=128)
print("score: ", score)

predict = model.predict(x_test)
print("predict: \n", predict)

