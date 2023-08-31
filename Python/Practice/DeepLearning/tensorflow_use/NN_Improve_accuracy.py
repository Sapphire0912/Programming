import tensorflow as tf
import numpy as np
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import cv2

output_dir = 'E:\\MyProgramming\\Python\\Practice\\DeepLearning\\tensorflow_use\\pic\\NN_improve\\Width Shift\\'

# 使用 tf.keras.preprocessing.image.ImageDataGenerator() 函式新增大量資料集

datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    rescale=1. / 255,
    fill_mode='nearest'
)

# datagen = tf.keras.preprocessing.image.ImageDataGenerator(
#     rotation_range=15,  # 旋轉 15 度
#     width_shift_range=0.1,  # 左右平移 10%
#     height_shift_range=0.1,  # 上下平移 10%
#     rescale=1./255,  # 調整數值差異(一定要加此行, 不然會出 bug)
#     shear_range=0.2,  # 減少 20%
#     zoom_range=0.2,  # 縮放 20%
#     brightness_range=(0.6, 1.4),  # 亮度
#     horizontal_flip=True,  # 左右鏡射
#     vertical_flip=True,  # 上下鏡射
#     fill_mode='nearest'  # 空白處理
# )

# img = tf.keras.preprocessing.image.load_img("D:\\pic\\hololive\\koyori.png", target_size=(496, 495))  # 讀取圖片
# data = tf.keras.preprocessing.image.img_to_array(img)  # 將資料轉成 numpy array

path2 = "E:\\MyProgramming\\Python\\Practice\\DeepLearning\\tensorflow practice\\vessel-segmentation2\\train\\22_training.tif"
data = cv2.imread(path2)
height, width, channel = data.shape

data = data.reshape(1, height, width, channel)

batchs = datagen.flow(
    data,
    batch_size=9,  # 產生 9 張圖片
    # save_to_dir=output_dir,
    # save_prefix='koyori',
    # save_format='png'
)

# 由於 batchs 是迭代器 iterator, 要執行以下程式才會儲存圖片到指定目錄
i = 1
for batch in batchs:
    augImage = batch[0]

    plt.subplot(330+i)
    plt.imshow(augImage)

    if i >= 9:
        break
    i += 1
plt.show()

# 水平移動(width shift)
# img = tf.keras.preprocessing.image.load_img("D:\\pic\\hololive\\koyori.png", target_size=(496, 495))
# data = tf.keras.preprocessing.image.img_to_array(img)
# height, width, channel = data.shape
# data = data.reshape(1, height, width, channel)
#
# datagen = tf.keras.preprocessing.image.ImageDataGenerator(
#     width_shift_range=[-20, 20],  # pixel
#     rescale=1 / 255
# )
# width_shift = datagen.flow(
#     data,
#     batch_size=9,
# )
#
# i = 1
# for batch in width_shift:
#     augImage = batch[0]
#     plt.subplot(330+i)
#     plt.imshow(augImage)
#
#     if i >= 9:
#         break
#     i += 1
# plt.show()
# 以下皆為參數改動而已
