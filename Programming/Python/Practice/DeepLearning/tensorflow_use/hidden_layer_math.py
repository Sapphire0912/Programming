import numpy as np
import matplotlib.pyplot as plt

# 假如要分類以下的資料
# plt.plot([0], [0], 'ro')
# plt.plot([0, 1, 1], [1, 1, 0], 'bo')
# plt.axis([-0.5, 1.5, -0.5, 1.5])


# 使用 線性回歸
# plt.xlabel('x2')
# plt.ylabel('x1')
# plt.text(0, 0.5, 'x1+x2-0.5=0')
# plt.plot([-0.5, 1], [1, -0.5], 'g-')

# 用感知器和激勵函式分類(最左下為0, 其他為1)


# def activation(v1):
#     if v1 >= 0:
#         return 1
#     return 0
#
#
# def Perception(a, x, b, y, c):
#     v1 = a*x + b*y + c
#     act1 = activation(v1)
#     print(act1)
#
#
# a = 1
# b = 1
# c = -0.5
# i = [0, 1, 1, 0]
# j = [0, 0, 1, 1]
#
# for t in range(len(i)):
#     Perception(a, i[t], b, j[t], c)


# MLP XOR Problem
# plt.plot([0, 1], [1, 0], 'bo')
# plt.plot([0, 1], [0, 1], 'ro')
# plt.axis([-0.5, 1.5, -0.5, 1.5])

# 若使用一般的線性分類無法很完美的分類
plt.title('MLP XOR Problem')
# plt.xlabel('x2')
# plt.ylabel('x1')
# plt.text(0, 0.5, 'x1+x2-0.5=0')
# plt.plot([-0.5, 1], [1, -0.5], 'g-')
# plt.text(0.5, 0.5, '0x1+x2-0.5=0')
# plt.plot([0.5, 0.5], [-2, 2], 'y--')

# 在神經網路中一條線無法區分, 就使用兩條, 即可解決 XOR 問題了
# plt.text(0, 0.5, 'x1+x2-0.5=0')
# plt.plot([-0.5, 1], [1, -0.5], 'g-')
# plt.text(0, 0.6, '+ + + +', {'color': 'green'})
# plt.text(-0.25, 0.4, '- - - -', {'color': 'green'})
#
# plt.text(1, 0.5, 'x1+x2-1.5=0')
# plt.plot([-0.5, 2], [2, -0.5], 'y--')
# plt.text(1, 0.6, '+ + + +', {'color': 'brown'})
# plt.text(0.75, 0.4, '- - - -', {'color': 'brown'})

# 使用感知器


def activation(v1):
    if v1 >= 0:
        return 1
    return 0


def Perception(n, a, x, b, y, c):
    v1 = a*x + b*y + c
    act1 = activation(v1)
    # print(n, act1)
    return act1


# print("h1(x):")
n = "h1"
a = 1
b = 1
c = -0.5
i = [0, 1, 1, 0]
j = [0, 0, 1, 1]
#
# for t in range(len(i)):
#     Perception(n, a, i[t], b, j[t], c)
#
# print("h2(x):")
n2 = "h2"
c2 = -1.5
#
# for t in range(len(i)):
#     Perception(n2, a, i[t], b, j[t], c2)


# 空間轉換
plt.subplot(2, 1, 1)
plt.title('MLP XOR Problem')
plt.plot([0, 1], [1, 0], 'bo')
plt.plot([0, 1], [0, 1], 'ro')
plt.axis([-0.5, 1.5, -0.5, 1.5])
plt.text(0, 0.5, 'x1+x2-0.5=0')
plt.plot([-0.5, 1], [1, -0.5], 'g-')
plt.text(0, 0.6, '+ + + +', {'color': 'green'})
plt.text(-0.25, 0.4, '- - - -', {'color': 'green'})
plt.text(1, 0.5, 'x1+x2-1.5=0')
plt.plot([-0.5, 2], [2, -0.5], 'y--')
plt.text(1, 0.6, '+ + + +', {'color': 'brown'})
plt.text(0.75, 0.4, '- - - -', {'color': 'brown'})
plt.axis([-0.5, 1.5, -0.5, 1.5])

plt.subplot(2, 1, 2)
plt.axis([-0.5, 1.5, -0.5, 1.5])
plt.plot([Perception(n, a, 0, b, 0, c), Perception(n, a, 1, b, 1, c)],
         [Perception(n2, a, 0, b, 0, c2), Perception(n2, a, 1, b, 1, c2)], 'ro')

plt.plot([Perception(n, a, 1, b, 0, c), Perception(n, a, 1, b, 0, c)],
         [Perception(n2, a, 0, b, 1, c2), Perception(n2, a, 0, b, 1, c2)], 'bo')
plt.xlabel('f(h2)')
plt.ylabel('f(h1)')
plt.text(0.25, 0.5, 'f(h1)-2f(h2)-0.5=0')
plt.plot([1.5, 0.25], [1, -0.5], 'g-')
plt.show()


