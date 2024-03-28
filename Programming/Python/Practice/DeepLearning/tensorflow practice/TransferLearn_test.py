import tensorflow as tf
from tensorflow.keras import datasets, models, layers, utils, activations, losses, optimizers, metrics
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from glob import glob
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import pandas as pd


# Define Parameters
num_classes = 3
IMG_SIZE = 224

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)


def create_dataset(paths, img_size=IMG_SIZE, num_classes=num_classes, test=False):
    num_data = len(paths)
    x_data = np.empty((num_data, img_size, img_size, 3))
    y_data = np.empty((num_data))

    for i, path in enumerate(tqdm(paths)):
        # read image and preprocess
        img = cv2.imread(path)[:,:,::-1]
        img = cv2.resize(img, (img_size, img_size))

        # !!!!!!!!! Use model preprocessing function !!!!!!!!!!
        img = tf.keras.applications.efficientnet.preprocess_input(img)
        x_data[i] = img

        if not test:
            # read class label
            filename = os.path.split(path)[1]
            cls = int(filename.split('.')[0].split('_')[-1])  # '38200_left_0.jpeg' -> 0
            y_data[i] = cls
    if not test:
        y_data = utils.to_categorical(y_data, num_classes=num_classes)
        return x_data, y_data
    else:
        return x_data


paths = glob('retina-train/*.jpeg')
paths_test = sorted(glob('retina-test/*.jpeg'))

# split dataset
path_train, path_val = train_test_split(paths, test_size=0.2)
# print(len(path_train), len(path_val))

# create model(transfer learning)
tf.keras.backend.clear_session()  # clear graph

base_model = tf.keras.applications.EfficientNetB2(
            include_top=False,
            weights='imagenet',
            input_shape=(224, 224, 3)
        )

x = base_model.get_layer('block7a_expand_conv').output
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

# freeze layers
for l in base_model.layers:
    l.trainable = False

x_train, y_train = create_dataset(path_train)
x_val, y_val = create_dataset(path_val)
x_test = create_dataset(paths_test, test=True)
# print(x_train.shape, y_train.shape, x_val.shape, y_val.shape)

model.compile(
    optimizer='adam',
    loss=losses.categorical_crossentropy,
    metrics=[metrics.categorical_accuracy]
)


logs = model.fit(
    x_train, y_train,
    batch_size=32,
    epochs=20,
    validation_data=(x_val, y_val)
)

predictions = np.argmax(model.predict(x_test), axis=-1)

df = pd.DataFrame()
df['Id'] = [p.split(os.sep)[-1] for p in paths_test]
df['Category'] = predictions
df.to_csv('submission.csv', index=False)
