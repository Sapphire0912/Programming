import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split as tts
import tensorflow as tf
import matplotlib.pyplot as plt

# 如何判斷要選哪種演算法, 將所有演算法的訓練歷史顯示出來就可以比較了

# datasets
iris = load_iris()
x, y = iris.data, iris.target

dim = x.shape[1]
category = len(np.unicode(y))

x_train, x_test, y_train, y_test = tts(x, y, test_size=0.2)

# One-Hot Encode
y_train2 = tf.keras.utils.to_categorical(y_train, num_classes=category)
y_test2 = tf.keras.utils.to_categorical(y_test, num_classes=category)

# create model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(10, tf.nn.relu, input_dim=dim))
model.add(tf.keras.layers.Dense(10, tf.nn.relu))
model.add(tf.keras.layers.Dense(category, tf.nn.softmax))

# all optimizers
learning_rate = 0.01
adam = tf.keras.optimizers.Adam(lr=learning_rate)
sgd = tf.keras.optimizers.SGD(lr=learning_rate)
rmsprop = tf.keras.optimizers.RMSprop(lr=learning_rate)
adagrad = tf.keras.optimizers.Adagrad(lr=learning_rate)
adadelta = tf.keras.optimizers.Adadelta(lr=learning_rate)
nadam = tf.keras.optimizers.Nadam(lr=learning_rate)
momentum = tf.keras.optimizers.SGD(lr=learning_rate, momentum=0.9)


# compile
def model_compile(optimizer):
    model.compile(
        optimizer=optimizer,
        loss=tf.keras.losses.categorical_crossentropy,
        metrics=['accuracy']
    )

    history = model.fit(x_train, y_train2, epochs=400, batch_size=16)
    return history


his_adam = model_compile(adam)
his_sgd = model_compile(sgd)
his_rmsprop = model_compile(rmsprop)
his_adagrad = model_compile(adagrad)
his_adadelta = model_compile(adadelta)
his_nadam = model_compile(nadam)
his_momentum = model_compile(momentum)

plt.title('All algorithm accuracy compare')
plt.xlabel('epoch')
plt.ylabel('acc')

plt.plot(his_adam.history['accuracy'])
plt.plot(his_sgd.history['accuracy'])
plt.plot(his_rmsprop.history['accuracy'])
plt.plot(his_adagrad.history['accuracy'])
plt.plot(his_adadelta.history['accuracy'])
plt.plot(his_nadam.history['accuracy'])
plt.plot(his_momentum.history['accuracy'])

plt.legend(['Adam', 'SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Nadam', 'Momentum'])
plt.show()
# Adadelta 演算法執行結果和書上的解釋不一致, 再多拿一些數據集測試