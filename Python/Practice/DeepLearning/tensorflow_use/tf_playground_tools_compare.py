import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# 模擬 tensorflow playground 的資料
x1 = np.random.random((100, 2)) * -4 - 1
x2 = np.random.random((100, 2)) * 4 + 1
x_train = np.concatenate((x1, x2))
y1 = np.zeros((100, ), dtype=int)
y2 = np.ones((100, ), dtype=int)
y_train = np.concatenate((y1, y2))
plt.plot(x1[:, 0], x1[:, 1], 'yo')
plt.plot(x2[:, 0], x2[:, 1], 'bo')
# plt.show()

# 透過 tensorflow playground 工具, 使用最少的隱藏層和神經元區分資料
# 僅用一個神經元和一個隱藏層

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(units=1, activation=tf.nn.tanh, input_dim=2))
model.add(tf.keras.layers.Dense(units=2, activation=tf.nn.softmax))

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(x_train, y_train, epochs=100, batch_size=32)
model.summary()

# 計算出 weight 權重, 和 bias 偏移量
# ax + by + c = 0; weight: a, b; bias: c
weights, biases = model.layers[0].get_weights()  # 第一個隱藏層
print(weights, biases)
# [[ 0.37757728]
# [-1.7398044 ]] [-0.09049916]

x = np.linspace(-5, 5, 100)
y = (-weights[0] * x-biases[0]) / weights[1]
plt.title("Graph of y=(%s+%s)/%s" % (-weights[0], -biases[0], weights[1]))
plt.xlabel('x', color='#1C2833')
plt.ylabel('y', color='#1C2833')
plt.axis([-5, 5, -5, 5])
plt.plot(x, y, '-r', label='No.1')
plt.legend(loc='upper left')
plt.grid()
plt.show()
