import tensorflow as tf
import numpy as np

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
amount, col, row = x_train.shape
x_train = x_train.reshape([amount, col * row]).astype(np.float32)
x_test = x_test.reshape([x_test.shape[0], col * row]).astype(np.float32)

x_train /= 255
x_test /= 255

category = len(np.unique(y_train))
y_train_one_hot = tf.keras.utils.to_categorical(y_train, category)
y_test_one_hot = tf.keras.utils.to_categorical(y_test, category)

# 建立神經元
model = tf.keras.models.Sequential()
model.add(
    tf.keras.layers.Dense(units=100, activation=tf.nn.relu, input_dim=col * row)
)
model.add(
    tf.keras.layers.Dense(units=100, activation=tf.nn.relu)
)
model.add(
    tf.keras.layers.Dense(units=category, activation=tf.nn.softmax)
)
model.summary()

model.compile(
    optimizer=tf.keras.optimizers.Adam(lr=0.001),
    loss=tf.losses.categorical_crossentropy,
    metrics=['accuracy']
)

model.fit(
    x_train, y_train_one_hot,
    batch_size=500,
    epochs=500,
    verbose=1
)

score = model.evaluate(x_test, y_test_one_hot, batch_size=128)
print(f'loss:{score[0]}, acc:{score[1]}')

