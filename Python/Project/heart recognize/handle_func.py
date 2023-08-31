import numpy as np
import pandas as pd
import matplotlib as mpt
import matplotlib.pyplot as plt


def handle(df, x):
    # 將 nan 用 0 填入
    df = df.fillna(0)
    y = np.zeros(df.shape[0])
    print(y.dtype)
    for i in range(df.shape[0]):
        y[i] = np.sum(df.values[i][2:] * x) + df.values[i][1]

    return y


# --- input test data
x_input = 8
test = pd.DataFrame(
    np.random.rand(10, 11),
    columns=['rss', 'bias', 'w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9'],
    index=['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10']
)
test.rss[:] = 100000
test.w2[0] = np.nan
test.w3[0:2] = np.nan
test.w4[0:3] = np.nan
# ---
# call
res = handle(df=test, x=x_input)
print(test)
print(res)

# yy = [
#     88.13, 88.65, 89.17, 89.69, 90.21, 90.73, 91.25, 91.77, 92.29, 92.81, 93.33, 93.85, 94.37, 94.89, 95.41, 95.93,
#     96.45, 96.97, 97.49, 98.01, 98.53, 99.05, 99.57, 100.09, 100.61, 101.12, 101.64, 102.16, 102.68, 103.2, 103.72,
#     104.24, 104.76, 105.28, 105.8, 106.32, 106.84, 107.36, 107.88, 108.4
# ]
#
# plt.figure(1)
# plt.plot(range(0, 40), yy)
# plt.show()


