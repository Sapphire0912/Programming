import tensorflow as tf
import numpy as np
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

print(f'physical_devices:{physical_devices}')

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

# 減少資料量
x_train, y_train, x_test, y_test = x_train[:2000], y_train[:2000], x_test[:200], y_test[:200]
amount, col, row = x_train.shape
x_train = x_train.reshape([amount, col, row, 1]).astype(np.float32)
x_test = x_test.reshape([x_test.shape[0], col, row, 1]).astype(np.float32)
x_train /= 255
x_test /= 255

category = len(np.unique(y_train))
y_train_one_hot = tf.keras.utils.to_categorical(y_train, category)
y_test_one_hot = tf.keras.utils.to_categorical(y_test, category)

model = tf.keras.models.Sequential()

# CNN 步驟
model.add(
    tf.keras.layers.Conv2D(
        filters=28,
        kernel_size=(3, 3),
        padding="same",
        activation='relu',
        input_shape=(28, 28, 1)
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
try:
    with open('cnn_fashion_mnist.h5', 'r') as load_weights:
        model.load_weights('cnn_fashion_mnist.h5')

except IOError:
    pass

model.compile(
    optimizer=tf.keras.optimizers.Adam(lr=0.001),
    loss=tf.losses.categorical_crossentropy,
    metrics=['accuracy']
)

history = model.fit(
    x=x_train, y=y_train_one_hot,
    batch_size=1000,
    epochs=200,
    verbose=1
)

for step in range(400):
    cost = model.train_on_batch(x_train, y_train_one_hot)
    print(f'step:{step}, train cost:{cost}')

    # 每 20 次就儲存一次權重
    if step % 20 == 0:
        with open('cnn_fashion_mnist.json', 'w') as model_json:
            model_json.write(model.to_json())
        model.save_weights('cnn_fashion_mnist.h5')
