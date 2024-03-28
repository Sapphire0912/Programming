import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split as tts

x = np.random.random((900, 5))
y = np.sum(x, axis=1) * 12.36 + np.random.randint(0, 100)

x_train, x_test, y_train, y_test = tts(x, y, test_size=0.2)

model = tf.keras.models.Sequential()

model.add(
    tf.keras.layers.Dense(5, activation=tf.nn.relu, input_dim=5)
)

model.add(
    tf.keras.layers.Dense(15, activation=tf.nn.relu)
)

model.add(
    tf.keras.layers.Dense(1, activation=tf.nn.relu)
)

model.compile(
    optimizer='sgd',
    loss='MSE',
    metrics=['mse']
)

model.fit(x_train, y_train, epochs=100, batch_size=20)

score = model.evaluate(x_test, y_test, batch_size=50)
print('score: ', score)

pred = model.predict(x_test)
print('pred: ', np.argmax(pred[0]), np.argmax(pred[1]))
