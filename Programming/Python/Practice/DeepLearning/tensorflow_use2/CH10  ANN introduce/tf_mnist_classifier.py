import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

# load datasets
fashion_mnist = tf.keras.datasets.fashion_mnist
(Xtrain, Ytrain), (Xtest, Ytest) = fashion_mnist.load_data()

# Ground Truth class names(category = 10)
class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

# split validation data, and normalization [0, 1]
Xvalid, Xtrain = Xtrain[:5000] / 255.0, Xtrain[5000:] / 255.0
Yvalid, Ytrain = Ytrain[:5000], Ytrain[5000:]

# use Sequential to create the model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=[28, 28]))  # Convent data into 1D array
model.add(tf.keras.layers.Dense(300, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(len(class_names), activation=tf.nn.softmax))
# model.summary()

# tf.keras.utils.plot_model(model) install failed.

# model layer list
layer_list = model.layers
# print(f'Input Layer: {layer_list[0]}, Layer Name: {layer_list[0].name}')
# print(f'Hidden Layer1: {layer_list[1]}, Layer Name: {layer_list[1].name}')
# print(f'Hidden Layer2: {layer_list[2]}, Layer Name: {layer_list[2].name}')
# print(f'Output Layer: {layer_list[3]}, Layer Name: {layer_list[3].name}')

# get the weight, bias of each layer
w1, b1 = layer_list[1].get_weights()
# print(f'weight shape: {w1.shape}, bias shape: {b1.shape}')
# 連結權重矩陣在 ch11 提到, 更詳細的部分可以參考 https://keras.io/initializers/

# compile model
# One-Hot Encode 需要改成 categorical_crossentropy, 否則 sparse_categorical_crossentropy
model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer='sgd',
    metrics=['accuracy']
)

# train & evaluation model
history = model.fit(Xtrain, Ytrain, epochs=30, batch_size=1000, validation_data=(Xvalid, Yvalid))
# parameters:
# class_weight: 設定類別權重(假如資料不平均時, 可以讓少的有大權重, 多的低權重)
# sample_weight: 設定實例權重(假如有些實例是專家標記的, 有些是其他人標記的, 可以讓前者有較高的權重)
# 若提供上面這兩個參數, keras 裡面會將兩者相乘

score = model.evaluate(Xtest, Ytest)
print(f'loss: {score[0]}, accuracy: {score[1]}')

# draw image
# pd.DataFrame(history.history).plot(figsize=(8, 5))
# plt.grid(True)
# plt.gca().set_ylim(0, 1)  # set the Y axis between 0 and 1
# plt.show()

# predict
Xnew = Xtest[:3]
YProbability = model.predict(Xnew)
print(f'Probability: {YProbability}')
print(f'Predict Class: ', np.where((YProbability > 0.5).astype(np.int) == 1)[1])

