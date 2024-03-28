import tensorflow as tf
import numpy as np
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

# 使用 MNIST 資料集做 CNN 圖像辨識的資料前處理
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
amount, col, row, channel = x_train.shape
x_train = x_train.astype(np.float32)
x_test = x_test.astype(np.float32)
x_train /= 255
x_test /= 255

category = len(np.unique(y_train))
y_train_one_hot = tf.keras.utils.to_categorical(y_train, category)
y_test_one_hot = tf.keras.utils.to_categorical(y_test, category)

# CNN 步驟
model = tf.keras.models.Sequential()
model.add(
    tf.keras.layers.Conv2D(
        filters=28,
        kernel_size=(3, 3),
        padding="same",
        activation='relu',
        input_shape=(32, 32, 3)
    )
)

model.add(
    tf.keras.layers.Conv2D(
        filters=56,
        kernel_size=(2, 2),
        padding='same',
        activation='relu'
    )
)

model.add(
    tf.keras.layers.Dropout(rate=0.01)
)

model.add(
    tf.keras.layers.Flatten()
)

# MLP
model.add(
    tf.keras.layers.Dense(128, activation='relu')
)

model.add(
    tf.keras.layers.Dense(128, activation='relu')
)

model.add(
    tf.keras.layers.Dense(category, activation='softmax')
)

# 載入權重
# try:
#     with open('cnn_cifar10.h5', 'r') as load_weights:
#         model.load_weights('cnn_cifar10.h5')
#
# except IOError:
#     pass

model.compile(
    optimizer=tf.keras.optimizers.Adam(lr=0.001),
    loss=tf.losses.categorical_crossentropy,
    metrics=['accuracy']
)

history = model.fit(
    x=x_train, y=y_train_one_hot,
    batch_size=128,
    epochs=10,
    validation_data=(x_test, y_test_one_hot),
    verbose=1
)

# for step in range(400):
#     cost = model.train_on_batch(x_train, y_train_one_hot)
#     print(f'step:{step}, train cost:{cost}')

    # 每 20 次就儲存一次權重
    # if step % 20 == 0:
    #     with open('cnn_cifar10.json', 'w') as model_json:
    #         model_json.write(model.to_json())
    #     model.save_weights('cnn_cifar10.h5')
