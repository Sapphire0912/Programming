import cv2
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import model_from_json  # 匯入模型函式庫


def create_model():
    x_train, y_train, x_test, y_test = tf.keras.datasets.mnist.load_data()

    # json_file = open('model.json', 'r')
    # load_model_json = json_file.read()
    # json_file.close()
    #
    # model = model_from_json(load_model_json)
    # model.load_weights("model.h5")
    # model.compile(
    #     loss=tf.keras.losses.categorical_crossentropy,
    #     optimizer=tf.keras.optimizers.Adadelta(),
    #     metrics=['accuracy']
    # )


def init_camera(camera=0, width=640, high=480):
    cam = cv2.VideoCapture(camera)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, high)
    return cam


cap = init_camera(0, 800, 600)
create_model()

while True:
    ret, frame = cap.read()
    # frame 處理
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)
    _, thres = cv2.threshold(resized, 80, 255, cv2.THRESH_BINARY)
    inverte = cv2.bitwise_not(thres)

    now = time.ctime()
    cv2.putText(frame, now, (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (0, 0, 255), 1)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
