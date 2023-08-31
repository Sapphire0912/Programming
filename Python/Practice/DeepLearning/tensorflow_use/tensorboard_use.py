from time import time
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split as tts
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import model_from_json
import tensorflow as tf
import numpy as np


# 這裡的 main() 用來儲存類神經網路模型和權重
def main():
    """
    1. 準備資料(使用 iris datasets)
    2. 拆分成訓練和驗證集
    3. 轉成 One-Hot Encode
    (類別數量為標籤的類別數量)
    4. 創建模型
    (輸入層的維度是資料集的特徵數(維度)、輸出層的神經元數量是標籤的類別總數)
    5. 編譯模型
    (選擇最佳化演算法, 以及損失函式, 拿甚麼當指標(正確率))
    6. 創建 TensorBoard
    (選擇要放的路徑)
    7. 訓練模型
    (選擇訓練次數, 一次訓練多少, 顯示樣示, etc.)
    (這裡為了使用 tensorboard 所以使用 callbacks 參數)
    8. 測試資料
    9. 儲存模型以及訓練後的結果
    (模型: 類神經網路模型; 權重: 深度學習後的結果)
    9-2. 透過 Callback 可以在每次訓練就儲存一次權重
    (把 step 7 的參數裡面放入 即時更新權重的變數)
    """

    # step 1
    iris = load_iris()
    x, y = iris.data, iris.target

    dim = x.shape[1]
    categorical = len(np.unique(y))

    # step 2
    x_train, x_test, y_train, y_test = tts(x, y, test_size=0.2)

    # step 3
    y_train_onehot = tf.keras.utils.to_categorical(y_train, num_classes=categorical)
    y_test_onehot = tf.keras.utils.to_categorical(y_test, num_classes=categorical)

    # step 4
    model = tf.keras.Sequential()

    # input layer
    model.add(
        tf.keras.layers.Dense(10, activation=tf.nn.relu, input_dim=dim)
    )

    # hidden layer
    model.add(
        tf.keras.layers.Dense(10, activation=tf.nn.relu)
    )

    # output layer
    model.add(
        tf.keras.layers.Dense(categorical, activation=tf.nn.softmax)
    )

    # step 5
    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr=0.001),
        loss=tf.keras.losses.categorical_crossentropy,
        metrics=['accuracy']
    )

    # step 6
    path = '../logs'
    # tf_board = TensorBoard(log_dir=path)

    # step 7
    # history = model.fit(
    #     x=x_train, y=y_train_onehot,
    #     epochs=100, batch_size=20,
    #     callbacks=[tf_board],
    #     verbose=1
    # )

    # step 8
    score = model.evaluate(x_test, y_test_onehot, batch_size=20)
    print('main score: ', score)

    # step 9
    # 將模型儲存成 json 或者 yaml
    model_json = model.to_json()
    with open("model_json.json", "w") as json_file:
        json_file.write(model_json)

    # 模型權重則使用 h5py 模組來儲存成 .h5 檔案
    # model.save_weights("model.h5")

    # step 9-2
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        "model.h5",
        monitor='loss', verbose=1,
        save_best_only=True, mode='auto', period=1
    )

    # step 7 的參數調整
    history = model.fit(
        x=x_train, y=y_train_onehot,
        epochs=100, batch_size=20,
        callbacks=[checkpoint],
        verbose=1
    )


# 讀取 main() 儲存的模型和權重並轉回 tensorflow 的類神經模型
def use_model():
    # step 1
    iris = load_iris()
    x, y = iris.data, iris.target

    dim = x.shape[1]
    categorical = len(np.unique(y))

    # step 2
    x_train, x_test, y_train, y_test = tts(x, y, test_size=0.2)

    # step 3
    y_test_onehot = tf.keras.utils.to_categorical(y_test, num_classes=categorical)

    # 讀取模型系統架構
    json_file = open('model_json.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    # 將 json 轉成模型
    model = model_from_json(loaded_model_json)

    # 讀取模型權重
    model.load_weights("model.h5")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr=0.001),
        loss=tf.keras.losses.categorical_crossentropy,
        metrics=['accuracy']
    )

    # test
    score = model.evaluate(x_test, y_test_onehot, batch_size=20)
    print("load model score: ", score)


if __name__ == '__main__':
    main()
    use_model()



