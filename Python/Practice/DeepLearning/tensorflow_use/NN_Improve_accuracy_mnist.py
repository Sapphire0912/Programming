import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

# 注意: 不是每種資料集都可以 360 度旋轉或鏡像顛倒, 像手寫辨識這種有方向性的資料隨意旋轉反而會破壞原本的答案

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
amount, height, width = x_train.shape

samples = x_train.reshape(amount, height, width, 1)

datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=25,  # 旋轉正負 25 度
    width_shift_range=[-3, 3],  # 左右平移 3 %
    height_shift_range=[-3, 3],  # 上下平移 3 %
    zoom_range=0.3,  # 縮放 30%
    data_format='channels_last'
)

it = datagen.flow(
    samples,
    batch_size=1
)

# 產生 25 張圖片
# for i in range(25):
#     plt.subplot(5, 5, i + 1)
#     batch = it.next()
#     image = batch[0].astype(np.uint8)
#     print(f'Iterator image shape: {image.shape}')
#     image.reshape(28, 28)
#     plt.imshow(image, cmap=plt.cm.get_cmap('gray'))
# plt.show()

# 結合 CNN 演算法做預測
