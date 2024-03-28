import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy as np

# 把 MLP_test 的程式用 keras 模組寫一次
x1 = np.random.random((500, 1))
x2 = np.random.random((500, 1)) + 1
x_train = np.concatenate((x1, x2))

y1 = np.zeros((500, ), np.int)
y2 = np.ones((500, ), np.int)
y_train = np.concatenate((y1, y2))

model = Sequential()
model.add(Dense(units=10, activation='relu', input_dim=1))
model.add(Dense(units=10, activation='relu'))
model.add(Dense(units=2, activation='softmax'))

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    x=x_train, y=y_train,
    epochs=20, batch_size=128
)

x_test = np.array([[0.22], [0.31], [1.22], [1.33]])
y_test = np.array([0, 0, 1, 1])
score = model.evaluate(x_test, y_test, batch_size=128)
print("score: ", score)

predict = model.predict(x_test)
print("predict: \n", predict)

# predict2 = model.predict_classes(x_test)
# print("predict result: ", predict2)
# print("y_test: ", y_test)
# print(y_test == predict2)
