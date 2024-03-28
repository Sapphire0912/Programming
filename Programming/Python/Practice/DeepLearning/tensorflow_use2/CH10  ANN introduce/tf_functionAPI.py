from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

housing = fetch_california_housing()
XtrainFull, Xtest, ytrainFull, ytest = train_test_split(housing.data, housing.target, test_size=0.2)
Xvalid, Xtrain, yvalid, ytrain = train_test_split(XtrainFull, ytrainFull)
# print(Xtrain.shape, Xvalid.shape)  # (4128, 8) (12384, 8)

scaler = StandardScaler()
Xtrain = scaler.fit_transform(Xtrain)
Xvalid = scaler.fit_transform(Xvalid)
Xtest = scaler.fit_transform(Xtest)

# use function API to create complicated model
# 用法: 就像是 function 傳入參數一樣, 下層的NN(要連接的NN)
# Input_ = tf.keras.layers.Input(shape=Xtrain.shape[1:])
# hidden1 = tf.keras.layers.Dense(30, activation=tf.nn.relu)(Input_)
# hidden2 = tf.keras.layers.Dense(30, activation=tf.nn.relu)(hidden1)
# concat = tf.keras.layers.Concatenate()([Input_, hidden2])
# Output = tf.keras.layers.Dense(1)(concat)
# model = tf.keras.Model(inputs=[Input_], outputs=[Output])
# model.summary()

# 假如若想要讓一組特徵子集合經過寬路徑, 不同子集合(可能重複)經過深路徑, 其中一種做法是使用多個輸入
InputA = tf.keras.layers.Input(shape=[5], name='Wide Input')
InputB = tf.keras.layers.Input(shape=[6], name='Deep Input')
hidden1 = tf.keras.layers.Dense(30, activation=tf.nn.relu)(InputB)
hidden2 = tf.keras.layers.Dense(30, activation=tf.nn.relu)(hidden1)
concat = tf.keras.layers.concatenate([InputA, hidden2])
# Output = tf.keras.layers.Dense(1, name='Output')(concat)
# model = tf.keras.Model(inputs=[InputA, InputB], outputs=[Output])

# 要注意的是, NN 的輸入有幾個就要分別對應
XtrainA, XtrainB = Xtrain[:, :5], Xtrain[:, 2:]  # (0 ~ 4), (2 ~ 7)
XvalidA, XvalidB = Xvalid[:, :5], Xvalid[:, 2:]
XtestA, XtestB = Xtest[:, :5], Xtest[:, 2:]
XnewA, XnewB = XtestA[:50], XtestB[:50]
# 之後可以設定方便一點的做法

# compile
# model.compile(
#     loss='mse',
#     optimizer=tf.keras.optimizers.SGD(lr=1e-3),
#     metrics=['mse']
# )

# train & evaluation model
# 可以建立字典來對應輸入參數 {'Wide Input': XtrainA, 'Deep Input': XtrainB}, 避免輸入太多會放錯
# history = model.fit((XtrainA, XtrainB), ytrain, epochs=20, validation_data=((XvalidA, XvalidB), yvalid))
# mse_test = model.evaluate((XtestA, XtestB), ytest)
# ypred = model.predict((XnewA, XnewB))
# plt.title('Use Function API to create complicated model')
# plt.xlabel('Data Count')
# plt.ylabel('Predict')
# plt.plot(range(0, 50), ypred)
# plt.plot(range(0, 50), ytest[:50], color='red')
# plt.legend(['pred', 'truth'])
# plt.show()

# 或許, 同一組資料要處理多個不同的任務(多任務分類), 可能同時要分類和回歸、或者多種分類等
# 另一種情況, 當成正則化使用(訓練約束, 目的是減少 Over fitting),
# 在 NN 結構中加入輔助輸出, 來確保網路底層自行學習有用的東西, 而不依靠網路其他部分
# 和上面例子相同, 僅改變輸出部分
Output = tf.keras.layers.Dense(1, name="main_Output")(concat)
aux_output = tf.keras.layers.Dense(1, name="aux_output")(hidden2)
model = tf.keras.Model(inputs=[InputA, InputB], outputs=[Output, aux_output])

# 每個輸出都有自己的 loss function, 因此在編譯模型的時候, loss 參數要傳入 list
model.compile(
    loss=['mse', 'mse'],
    loss_weights=[0.9, 0.1],  # 可以配置不同輸出的損失函數權重
    optimizer='sgd'
)

# 訓練模型時, 也必須提供各個輸出的標籤(即使一樣也是要使用 list 傳入)
history = model.fit([XtrainA, XtrainB], [ytrain, ytrain], epochs=20,
                    validation_data=([XvalidA, XvalidB], [yvalid, yvalid]))
total_loss, main_loss, aux_loss = model.evaluate([XtestA, XtestB], [ytest, ytest])
ypred_main, ypred_aux = model.predict([XnewA, XnewB])
print(f'Y prediction Main: {ypred_main[0]}')
print(f'Y prediction aux: {ypred_aux[0]}')
print(f'Truth: {ytest[0]}')
print(f'Total loss: {total_loss}')
print(f'Main loss: {main_loss}')
print(f'aux loss: {aux_loss}')
print(f'Total Calculate: {0.9 * main_loss + 0.1 * aux_loss}')  # 和 loss_weight 參數設定一樣, 最後相加
