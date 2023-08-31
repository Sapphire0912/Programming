from sklearn.model_selection import train_test_split as tts
from tensorflow.keras.datasets import boston_housing
from sklearn import preprocessing
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 波士頓房屋價格預測
# 載入資料集
(x_train, y_train), (x_test, y_test) = boston_housing.load_data()
# print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

# 創建每一個特徵值的名稱(從已知資料找的共 13 個)
# 另外 MEDV 為標準的答案
classes = [
    'CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT'
]

data = pd.DataFrame(x_train, columns=classes)
data['MEDV US$ * 1000'] = pd.Series(y_train)
# print(data.head())
# print(data.describe())

# 寫成 Excel 方便觀察
# writer = pd.ExcelWriter('boston_housing.xlsx')
# data.to_excel(writer, sheet_name='House Price Predict')
# writer.save()

# 顯示每個標籤互相的關聯性
# 最好的圖表應該是盡量呈對角線的樣子, 若是平均分布則兩者沒有甚麼關聯性
# sns.pairplot(data[['MEDV US$ * 1000', 'CRIM', 'AGE', 'DIS', 'TAX']], diag_kind='kde')
# 以下用等高線繪製
# g = sns.PairGrid(data[['MEDV US$ * 1000', 'CRIM', 'AGE', 'DIS', 'TAX']])
# g.map_diag(sns.kdeplot)
# g.map_offdiag(sns.kdeplot, cmap="Blues_d", n_levels=6)
# plt.show()

# 標準化
scale = preprocessing.MinMaxScaler()
x_train = scale.fit_transform(x_train)
x_test = scale.fit_transform(x_test)

model = tf.keras.models.Sequential()
model.add(
    tf.keras.layers.Dense(units=640, activation='relu', input_shape=[x_train.shape[1]])
)
model.add(
    tf.keras.layers.Dense(units=640, activation='relu')
)
model.add(
    tf.keras.layers.Dense(units=1)
)

learning_rate = 0.0001
opt1 = tf.keras.optimizers.Nadam(lr=learning_rate)
model.compile(loss='mse', optimizer=opt1, metrics=['mae'])
history = model.fit(x_train, y_train, epochs=40000, batch_size=100)
model.save_weights("boston model.h5")

print('start testing')
cost = model.evaluate(x_test, y_test)
print('test cost:', cost)

y_pred = model.predict(x_test)
print(y_pred[:10])
print(y_test[:10])
