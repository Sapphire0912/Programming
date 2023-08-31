from sklearn.model_selection import train_test_split
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)
gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
print(gpus)

# 下載資料集
with np.load('mnist_kaggle.npz', allow_pickle=True) as f:
    x_train, y_train = f['x_train'], f['y_train']
    x_test = f['x_test']
    print(x_train.shape, y_train.shape, x_test.shape)

# Define Parameters
num_classes = 10
img_size = 28

x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2)
print(x_train.shape, x_val.shape, x_train.shape, x_val.shape)

# Flatten img to a vector
x_train = x_train.reshape(x_train.shape[0], -1)
x_val = x_val.reshape(x_val.shape[0], -1)
x_test = x_test.reshape(x_test.shape[0], -1)

# normalize
x_train = x_train / 255.
x_val = x_val / 255.
x_test = x_test / 255.

# one hot encoding
y_train = tf.keras.utils.to_categorical(y_train, num_classes=num_classes)
y_val = tf.keras.utils.to_categorical(y_val, num_classes=num_classes)
# print(x_train.shape, x_val.shape, x_train.shape, x_val.shape)

# 建立模型
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(10, activation=tf.nn.relu, input_shape=(img_size * img_size, )),
    tf.keras.layers.Dense(units=10, activation=tf.nn.relu, kernel_initializer='normal'),
    tf.keras.layers.Dense(units=10, activation=tf.nn.softmax)
])
model.summary()

# 編譯 & 訓練模型
model.compile(
    optimizer=tf.keras.optimizers.Adam(lr=0.001),
    loss=tf.losses.categorical_crossentropy,
    metrics=['accuracy']
)

model.fit(
    x_train, y_train,
    batch_size=128,
    epochs=20,
    validation_data=(x_val, y_val)
)
