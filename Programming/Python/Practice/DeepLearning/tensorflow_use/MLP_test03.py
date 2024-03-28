import numpy as np
import tensorflow as tf


def do():
    """測試 callbacks 參數"""
    print("do called.")


# 為了要驗證改善 MLP 的預測結果, 因此先做一個可以產生較複雜的資料集
def createDatasets(high, iNum, iArraySize):
    x = np.random.random((iNum, iArraySize)) * float(high)
    # 取整數當成標籤
    y = ((x[:iNum, 0] + x[:iNum, 1]) / 2).astype(int)
    y2 = tf.keras.utils.to_categorical(y, num_classes=high)
    return x, y, y2


# step1: prepare data
categorical = 10
dim = 2
x_train, y_train, y_train2 = createDatasets(categorical, 1000, dim)

# step2: create model
model = tf.keras.models.Sequential()
model.add(
    tf.keras.layers.Dense(10, activation=tf.nn.relu, input_dim=dim)
)
model.add(
    tf.keras.layers.Dense(100, activation=tf.nn.relu)
)
# 增加隱藏層的部分
model.add(
    tf.keras.layers.Dense(1000, activation=tf.nn.relu)
)
model.add(
    tf.keras.layers.Dense(100, activation=tf.nn.relu)
)

model.add(
    tf.keras.layers.Dense(categorical, activation=tf.nn.softmax)
)

# step3: compile
model.compile(
    optimizer='adam',
    loss=tf.keras.losses.categorical_crossentropy,
    metrics=['accuracy']
)

# step4: training
model.fit(
    x=x_train, y=y_train2,
    epochs=100, batch_size=1, verbose=1
)

# step5: test
x_test, y_test, y_test2 = createDatasets(categorical, 100, dim)
score = model.evaluate(x_test, y_test2, batch_size=128)
print('score: ', score)  # score 代表用 test 來 predict 的準確率
# 訓練次數少時, 其正確率只有 15% 因此需要將 MLP 類神經做一些調整
# 若調整 epochs 的訓練次數
# 在訓練  20 次時, loss: 2.0355 - accuracy: 0.2283
# score:  [2.0532400608062744, 0.23000000417232513]
# 在訓練 100 次時, loss: 1.5876 - accuracy: 0.3354
# score:  [1.5896215438842773, 0.2800000011920929]
# 在訓練 200 次時, loss: 0.7294 - accuracy: 0.8308
# score:  [0.7310946583747864, 0.8100000023841858]


# fit 函式有 18 個參數可以調整, 這裡只列出常用的
# tensorflow.keras.models.Model.fit(
# x, y, batch_size=32, epochs=1, verbose=1, callbacks=None, validation_split=0.0, **kwargs
# )
# epochs: 訓練次數
# batch_size: 每次梯度更新的樣本數(每次訓練的資料量)
# verbose: 訓練時顯示的訊息, 0: 不顯示, 1: 進度, 2: 詳細
# callbacks: 做完一次就呼叫指定函式
# validation_split: 拿多少的數據當成驗證資料, 0.3 則是 30%

# 若調整 batch_size
# batch_size=64:
# training: loss: 1.8392 - accuracy: 0.2424
# predict: loss: 1.8760 - accuracy: 0.2100
# batch_size=32
# training: loss: 1.6017 - accuracy: 0.3784
# predict: loss: 1.6616 - accuracy: 0.3800

# 若增加神經元數量
# 10個改成100個
# training: loss: 0.8514 - accuracy: 0.7054
# predict: loss: 0.7636 - accuracy: 0.8200
# 神經元增加是讓特徵值能依照神經元的權重能夠更有效的區分出分類資料

# 若增加隱藏層
# 增加一層
# training: loss: 1.5081 - accuracy: 0.3109
# predict:  loss: 1.5189 - accuracy: 0.2900
# 增加兩層
# training: loss: 1.4765 - accuracy: 0.3666
# predict: loss: 1.5144 - accuracy: 0.3300

# 增加訓練資料集
# 資料量變成 10 倍
# training: loss: 0.9715 - accuracy: 0.7475
# predict: loss: 0.8990 - accuracy: 0.7600

# Q. 如何達到 100% 正確率
# 將參數全部調整一定可以達到100%正確率, 若連時間和固定資料量大小及記憶體空間都考慮進去的話,
# 增加神經元數量和隱藏層數量, 並適當提高訓練次數(訓練次數越多時間越久)
# 實務上, 在模型已經是最適合的情況下, 比起不斷調整神經元, 增加資料量可能會是比較省成本的做法??
# 2021/09/27 A. 資料預處理可以優先過濾不重要的特徵，或抓取 ROI 的區域(特徵) 因此不見得要增加資料量
