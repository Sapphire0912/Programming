import os
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
import tensorflow as tf


os.environ["CUDA_VISIBLE_DEVICES"] = "0"
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)


def AllFiles(DirPath, ext):
    targetList = list()
    for root, dirs, files in os.walk(DirPath):
        for f in files:
            if f[-len(ext):].lower() == ext:
                targetList.append(os.path.join(root, f))
    return targetList


def PreprocessData(PathList, img_size, data_gen=2, mode='train'):
    num_data = len(PathList) + data_gen * len(PathList)
    x_data = np.empty((num_data, img_size, img_size, 3))
    y_data = np.empty(num_data)

    generator = tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        rescale=1. / 255,
        fill_mode='nearest'
    )

    for i, path in enumerate(PathList):
        img = cv2.imread(path)
        img = cv2.resize(img, (img_size, img_size))
        img = tf.keras.applications.efficientnet.preprocess_input(img)  # using Efficient model
        x_data[i + data_gen * i] = img

        if mode == 'train':
            filename = path.split('\\')[-1]
            label = filename.split('_')
            label = category.index(label[1]) if len(label) > 1 else 0
            y_data[i + data_gen * i] = label

            if data_gen > 0:
                img = img.reshape(1, IMG_SIZE, IMG_SIZE, 3)

                batchs = generator.flow(
                    img, batch_size=20
                )

                for k, aug in enumerate(batchs):
                    if k == data_gen:
                        break

                    augImage = aug[0]
                    augImage = tf.keras.applications.efficientnet.preprocess_input(augImage)
                    x_data[i + (data_gen * i) + k] = augImage
                    y_data[i + (data_gen * i) + k] = label

    # one-hot encoding
    if mode == 'train':
        y_data = tf.keras.utils.to_categorical(y_data, num_classes=num_classes)
        return x_data, y_data
    else:
        return x_data


trainDir = ".\\pneumonia\\train\\"
testDir = ".\\pneumonia\\test\\"

trainDatasets = AllFiles(trainDir, 'jpeg')
testDatasets = AllFiles(testDir, 'jpeg')
x_trainPath, x_valPath = train_test_split(trainDatasets, test_size=0.2)

category = ['normal', 'bacteria', 'virus']

# Data Parameters
num_classes = 3
IMG_SIZE = 200

x_train, y_train = PreprocessData(x_trainPath, IMG_SIZE, data_gen=2)
x_val, y_val = PreprocessData(x_valPath, IMG_SIZE, data_gen=0)
x_test = PreprocessData(testDatasets, IMG_SIZE, data_gen=0, mode='test')
# print(x_train.shape, y_train.shape)

# create model
tf.keras.backend.clear_session()

base_model = tf.keras.applications.EfficientNetB2(
    include_top=False,
    weights='imagenet',
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)


x = base_model.output
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dense(256, activation=tf.nn.relu)(x)
x = tf.keras.layers.Dropout(0.3)(x)
x = tf.keras.layers.Dense(256, activation=tf.nn.relu)(x)
x = tf.keras.layers.Dropout(0.3)(x)
x = tf.keras.layers.Dense(256, activation=tf.nn.relu)(x)
x = tf.keras.layers.Dropout(0.3)(x)
predictions = tf.keras.layers.Dense(3, activation=tf.nn.softmax)(x)
model = tf.keras.models.Model(base_model.input, predictions)
model.summary()

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.categorical_crossentropy,
    metrics=[tf.keras.metrics.categorical_accuracy]
)

logs = model.fit(
    x_train, y_train,
    batch_size=32,
    epochs=20,
    validation_data=(x_val, y_val)
)

# predictions = np.argmax(model.predict(x_test), axis=-1)
# df = pd.DataFrame()
# df['Id'] = [f'{i:05d}.jpeg' for i in range(len(x_test))]
# df['Category'] = predictions.astype(int)
# df.to_csv('submission.csv', index=False)
