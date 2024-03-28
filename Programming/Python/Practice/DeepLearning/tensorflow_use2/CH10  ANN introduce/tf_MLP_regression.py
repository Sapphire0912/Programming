from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

# load data
housing = fetch_california_housing()
XtrainFull, Xtest, ytrainFull, ytest = train_test_split(housing.data, housing.target, test_size=0.2)
Xvalid, Xtrain, yvalid, ytrain = train_test_split(XtrainFull, ytrainFull)
# print(Xtrain.shape, Xvalid.shape)  # (4128, 8) (12384, 8)

# data preprocessing: avg & std(StandardScaler).
scaler = StandardScaler()
Xtrain = scaler.fit_transform(Xtrain)
Xvalid = scaler.fit_transform(Xvalid)
Xtest = scaler.fit_transform(Xtest)

# create NN model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(30, activation=tf.nn.relu, input_shape=Xtrain.shape[1:]))
model.add(tf.keras.layers.Dense(1))

# compile
model.compile(
    loss='mean_squared_error',
    optimizer='sgd',
    metrics=['mse']
)

# train & evaluation model
history = model.fit(Xtrain, ytrain, epochs=20, validation_data=(Xvalid, yvalid))
mse_test = model.evaluate(Xtest, ytest)
print(f'Test Data MSE: {mse_test}')

# predict
Xnew = Xtest[:50]
Ypred = model.predict(Xnew)
# print(f'Predict: {Ypred[0], Ypred[1]}')
# print(f'Ground Truth: {ytest[0], ytest[1]}')

# Regression plot 出來比較好觀察
plt.title('Use Sequential API to create complicated model')
plt.xlabel('Data Count')
plt.ylabel('Predict')
plt.plot(range(0, 50), Ypred)
plt.plot(range(0, 50), ytest[:50], color='red')
plt.legend(['pred', 'truth'])
plt.show()
