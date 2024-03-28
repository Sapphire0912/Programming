from sklearn.model_selection import train_test_split
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

# 下載資料集
# with np.load('cifar10_kaggle.npz', allow_pickle=True) as f:
#     x_train, y_train = f['x_train'], f['y_train']
#     x_test = f['x_test']
#
#     print(x_train.shape, y_train.shape, x_test.shape)


# Q. 利用 MLP 訓練 cifar10 的資料集
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
img_size = 32
num_classes = 10

x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2)
# print(x_train.shape, y_train.shape, x_val.shape, y_val.shape)

# Flatten img to a vector
x_train = x_train.reshape(x_train.shape[0], -1)
x_val = x_val.reshape(x_val.shape[0], -1)
x_test = x_test.reshape(x_test.shape[0], -1)

# normalization to 0 ~ 1
x_train = x_train / 255.
x_val = x_val / 255.
x_test = x_test / 255.

# one hot encoding
y_train = tf.keras.utils.to_categorical(y_train, num_classes=num_classes)
y_val = tf.keras.utils.to_categorical(y_val, num_classes=num_classes)

# Build your own model
model = tf.keras.models.Sequential(
    [
        tf.keras.layers.InputLayer((img_size * img_size * 3)),
        tf.keras.layers.Dense(300, activation=tf.nn.relu),
        tf.keras.layers.Dense(100, activation=tf.nn.relu),
        tf.keras.layers.Dense(10, activation='softmax')
    ]
)

model.compile(
    loss=tf.keras.losses.categorical_crossentropy,  # loss function
    optimizer=tf.keras.optimizers.SGD(),
    metrics=['accuracy']
)

logs = model.fit(
    x_train, y_train,
    batch_size=128,
    epochs=10,
    validation_data=(x_val, y_val)
)

history = logs.history
# print(history)

plt.plot(history['accuracy'])
plt.plot(history['val_accuracy'])
plt.legend(['accuracy', 'val_accuracy'])
plt.title('accuracy')
plt.show()

