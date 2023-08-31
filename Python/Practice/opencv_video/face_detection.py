import cv2
import numpy as np


def init_camera(cap=0, width=640, high=480):
    camera = cv2.VideoCapture(cap)

    # 判斷影片是否打開
    if camera.isOpened():
        print("WebCamera was opened.")
    else:
        print("WebCamera was closed.")
        raise IOError("Camera is not open.")

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, high)

    return camera


path = "E:\\Programs\\pycharm_env\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(path)
cam = init_camera(0, 800, 600)

# 分類器不太行, 考慮 ASM 演算法
while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=2, minSize=(32, 32))
    print(faces)
    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
