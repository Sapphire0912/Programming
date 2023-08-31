import tensorflow as tf
import numpy as np

# 使用 MNIST 資料集
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
amount, col, row = x_train.shape
x_train = x_train.reshape([amount, col * row * 1]).astype(np.float32)
x_test = x_test.reshape([x_test.shape[0], col * row * 1]).astype(np.float32)

# 標準化 [0, 1] 之間
x_train /= 255
x_test /= 255

# 使用 One-Hot Encoding
category = len(np.unique(y_test))
y_train_one_hot = tf.keras.utils.to_categorical(y_train, category)
y_test_one_hot = tf.keras.utils.to_categorical(y_test, category)

# 使用 MLP 模型來做圖形辨識
model = tf.keras.models.Sequential()
model.add(
    tf.keras.layers.Dense(units=10, activation=tf.nn.relu, input_dim=col * row)
)
# 隱藏層 使用 normal distribution 常態分布的亂數定義
model.add(
    tf.keras.layers.Dense(units=10, activation=tf.nn.relu, kernel_initializer='normal')
)
# 輸出層
model.add(
    tf.keras.layers.Dense(units=10, activation=tf.nn.softmax)
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(lr=0.001),
    loss=tf.losses.categorical_crossentropy,
    metrics=['accuracy']
)

# model.summary()

# 訓練模型
model.fit(
    x_train, y_train_one_hot,
    batch_size=1000,
    epochs=200,
    verbose=1
)

# 測試
score = model.evaluate(x_test, y_test_one_hot, batch_size=128)
print(f'loss:{score[0]}, acc:{score[1]}')
predict = np.where((model.predict(x_test[80:100]) > 0.5).astype(np.int32) == 1)[1]
print(f'Predict:{predict}')
print(f"Ground Truth:{y_test[80:100]}")
