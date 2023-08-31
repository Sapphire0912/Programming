import tensorflow as tf
import numpy as np
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

(xtrain, ytrain), (xtest, ytest) = tf.keras.datasets.mnist.load_data()
xvalid, xtrain = xtrain[:6000] / 255, xtrain[6000:] / 255
yvalid, ytrain = ytrain[:6000], ytrain[6000:]
xtest = xtest / 255

category = len(np.unique(ytrain))

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
model.add(tf.keras.layers.Dense(300, activation='relu'))
model.add(tf.keras.layers.Dense(100, activation='relu'))
model.add(tf.keras.layers.Dense(category, activation='softmax'))
# model.summary()

model.compile(
    optimizer=tf.keras.optimizers.SGD(lr=1e-3),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(xtrain, ytrain, epochs=30, validation_data=(xvalid, yvalid))

score = model.evaluate(xtest, ytest)
print(f'loss: {score[0]}, accuracy: {score[1]}')
