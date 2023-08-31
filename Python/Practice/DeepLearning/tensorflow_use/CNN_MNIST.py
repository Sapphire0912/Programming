import tensorflow as tf
import numpy as np
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

# 使用 MNIST 資料集做 CNN 圖像辨識的資料前處理
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
amount, col, row = x_train.shape
x_train = x_train.reshape([amount, col, row, 1]).astype(np.float32)
x_test = x_test.reshape([x_test.shape[0], col, row, 1]).astype(np.float32)
x_train /= 255
x_test /= 255

category = len(np.unique(y_train))
y_train_one_hot = tf.keras.utils.to_categorical(y_train, category)
y_test_one_hot = tf.keras.utils.to_categorical(y_test, category)

# 模型
model = tf.keras.models.Sequential()
# 透過多層的卷積提升辨識效果
# first layer: (28, 28, 1) -> (28, 28, 3)
model.add(
    tf.keras.layers.Conv2D(
        filters=3,
        kernel_size=(3, 3),
        padding='same',
        activation=tf.nn.relu,
        input_shape=(28, 28, 1)
    )
)
# second pooling: (28, 28, 3) -> (14, 14, 3)
model.add(
    tf.keras.layers.MaxPool2D(pool_size=(2, 2))
)
# third layer: (14, 14, 3) -> (14, 14, 9)
model.add(
    tf.keras.layers.Conv2D(
        filters=9,
        kernel_size=(2, 2),
        padding='same',
        activation=tf.nn.relu,
    )
)
# forth: 丟棄 5% 的圖後再卷積 (14, 14, 9) -> (14, 14, 6)
model.add(
    tf.keras.layers.Dropout(rate=0.05)
)
model.add(
    tf.keras.layers.Conv2D(
        filters=6,
        kernel_size=(2, 2),
        padding='same',
        activation=tf.nn.relu
    )
)
# fifth: 2D -> 1D
model.add(tf.keras.layers.Flatten())
model.add(
    tf.keras.layers.Dense(units=10, activation=tf.nn.relu)
)
model.add(
    tf.keras.layers.Dense(units=category, activation=tf.nn.softmax)
)
model.summary()

# 訓練
model.compile(
    optimizer=tf.keras.optimizers.Adam(lr=0.001),
    loss=tf.keras.losses.categorical_crossentropy,
    metrics=['accuracy']
)

history = model.fit(
    x_train, y_train_one_hot,
    batch_size=1000,
    epochs=200,
    verbose=1
)

score = model.evaluate(x_test, y_test_one_hot, batch_size=128)
print(f'loss:{score[0]}, acc:{score[1]}')
predict = np.where((model.predict(x_test) > 0.5).astype(np.int32) == 1)[1]
print(f'predict:{predict}')
print(f'Ground Truth:{y_test}')
