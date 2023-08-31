import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf


def sigmoid(x):
    return 1/(1+np.exp(-x))


def tanh(x):
    return (2/(1+np.exp(-2*x))) - 1


def relu(x):
    return x if x > 0 else 0


# 激勵函式的數學公式:
# sigmoid: f(x) = 1/1+exp(-x)
# tanh: f(x) = (2/1+exp(-2x)) - 1
# ReLU: f(x) = x if x > 0 else 0

# upper = 6
# lower = -6
# nums = 100
#
# x = np.linspace(lower, upper, nums)
# val = np.empty((0, ), dtype=int)
#
# for data in x:
#     y = relu(data)
#     val = np.append(val, y)
#
# plt.title('ReLU')
# plt.plot(x, val, '.b')
# plt.show()

# MLP 計算公式
# y = f(sigma 0 to inf w.T * x + b)
