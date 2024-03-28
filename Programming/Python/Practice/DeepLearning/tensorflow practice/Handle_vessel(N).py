import numpy as np
import cv2
import os
import tensorflow as tf
from PIL import Image
import tensorflow.keras.backend as K


def AllFiles(DirPath, ext):
    targetList = list()
    for root, dirs, files in os.walk(DirPath):
        for f in files:
            if f[-len(ext):].lower() == ext:
                targetList.append(os.path.join(root, f))
    return targetList


def DataGenerator(imgPath, GTPath=None, imgSize=512, mode='train', data_gen=0):
    num_data = len(imgPath) + data_gen * len(imgPath)
    x_data = np.empty((num_data, imgSize, imgSize, 3), np.float32)
    y_data = np.empty((num_data, imgSize, imgSize, 1), np.float32)

    generator = tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        rescale=1. / 255,
        fill_mode='nearest'
    )

    if mode != 'test':
        for i, (path, gt_path) in enumerate(zip(imgPath, GTPath)):
            img = cv2.imread(path)
            img = cv2.resize(img, (imgSize, imgSize))
            img = img / 255.

            index = data_gen * i + i
            x_data[index] = img

            y_img = np.array(Image.open(gt_path))   # opencv can not read gif file
            y_img = cv2.resize(y_img, (imgSize, imgSize))
            y_img = y_img / 255.

            y_data[index] = np.expand_dims(y_img, axis=-1)

            if data_gen > 0:
                img = img.reshape(1, imgSize, imgSize, 3)
                y_img = y_img.reshape(1, imgSize, imgSize, 1)

                x_batches = generator.flow(img, batch_size=20, shuffle=False)
                y_batches = generator.flow(y_img, batch_size=20, shuffle=False)

                for k, (x_aug, y_aug) in enumerate(zip(x_batches, y_batches)):
                    if k == data_gen:
                        break

                    x_augImg, y_augImg = x_aug[0], y_aug[0]
                    # x_augImg = x_augImg / 255.
                    # y_augImg = y_augImg / 255.
                    x_data[index + k] = x_augImg
                    y_data[index + k] = y_augImg

        return x_data, y_data

    else:
        for i, path in enumerate(imgPath):
            img = cv2.imread(path)
            img = cv2.resize(img, (imgSize, imgSize))
            img = img / 255.
            x_data[i] = img

        return x_data


# Customize Dice coefficient
def dice_coef(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + K.epsilon()) / (K.sum(y_true_f) + K.sum(y_pred_f) + K.epsilon())


trainDir = ".\\vessel-segmentation2\\train\\"
testDir = ".\\vessel-segmentation2\\test\\"
imgSize = 512

# read ground truth data
GroundTruthPath = AllFiles(trainDir, '_manual1.gif')

# read train data & split val data
trainPath = AllFiles(trainDir, '_training.tif')

valIndex = np.random.choice(len(trainPath), int(len(trainPath) * 0.4), replace=False)
x_valPath = [trainPath[i] for i in valIndex]
y_valPath = [GroundTruthPath[i] for i in valIndex]

x_trainPath, y_trainPath = list(), list()
for i in range(len(trainPath)):
    if i in valIndex:
        continue
    x_trainPath.append(trainPath[i])
    y_trainPath.append(GroundTruthPath[i])

# preprocess data
x_train, y_train = DataGenerator(
    imgPath=x_trainPath,
    GTPath=y_trainPath,
    imgSize=imgSize,
    mode='train',
    data_gen=3
)

x_val, y_val = DataGenerator(
    imgPath=x_valPath,
    GTPath=y_valPath,
    imgSize=imgSize,
    mode='val',
)
print(x_train.shape, y_train.shape, x_val.shape, y_val.shape)

# create test data
# testPath = AllFiles(testDir, '.tif')
# x_test = DataGenerator(imgPath=testPath, mode='test')
#
# # create model -- U-Net
# tf.keras.backend.clear_session()
#
# inputs = tf.keras.Input(shape=(imgSize, imgSize, 3))
#
# x = tf.keras.layers.Conv2D(
#     filters=32,
#     kernel_size=3,
#     strides=2,
#     padding="same"
# )(inputs)
# x = tf.keras.layers.BatchNormalization()(x)
# x = tf.keras.layers.Activation(tf.nn.relu)(x)
# previous_block_activation = x
#
# for filters in [64, 128, 256]:
#     x = tf.keras.layers.Activation(tf.nn.relu)(x)
#     x = tf.keras.layers.SeparableConv2D(filters, 3, padding="same")(x)
#     x = tf.keras.layers.BatchNormalization()(x)
#
#     x = tf.keras.layers.Activation(tf.nn.relu)(x)
#     x = tf.keras.layers.SeparableConv2D(filters, 3, padding="same")(x)
#     x = tf.keras.layers.BatchNormalization()(x)
#
#     x = tf.keras.layers.MaxPooling2D(3, strides=2, padding="same")(x)
#
#     residual = tf.keras.layers.Conv2D(filters, 1, strides=2, padding="same")(previous_block_activation)
#     x = tf.keras.layers.add([x, residual])
#     previous_block_activation = x
#
# for filters in [256, 128, 64, 32]:
#     x = tf.keras.layers.Activation(tf.nn.relu)(x)
#     x = tf.keras.layers.SeparableConv2D(filters, 3, padding="same")(x)
#     x = tf.keras.layers.BatchNormalization()(x)
#
#     x = tf.keras.layers.Activation(tf.nn.relu)(x)
#     x = tf.keras.layers.SeparableConv2D(filters, 3, padding="same")(x)
#     x = tf.keras.layers.BatchNormalization()(x)
#
#     x = tf.keras.layers.UpSampling2D(2)(x)
#
#     residual = tf.keras.layers.UpSampling2D(2)(previous_block_activation)
#     residual = tf.keras.layers.Conv2D(filters, 1, padding="same")(residual)
#     x = tf.keras.layers.add([x, residual])
#     previous_block_activation = x
#
# outputs = tf.keras.layers.Conv2D(1, 3, activation=tf.nn.sigmoid, padding="same")(x)
#
# model = tf.keras.Model(inputs, outputs)
# model.summary()
#
# model.compile(
#     optimizer='adam',
#     loss=tf.keras.losses.binary_crossentropy,
#     metrics=[dice_coef]
# )
#
# logs = model.fit(
#     x_train, y_train,
#     batch_size=1,
#     epochs=100,
#     validation_data=(x_val, y_val)
# )
