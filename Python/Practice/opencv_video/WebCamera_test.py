import cv2


camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = camera.read()
    # fps = camera.get(cv2.CAP_PROP_FPS)
    # print("current fps: ", fps)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # sobel = cv2.Sobel(gray, ddepth=-1, dx=1, dy=0, ksize=3)

    cv2.imshow("frame", frame)
    # cv2.imshow("threshold", thres)
    # cv2.imshow("gray", gray)
    # cv2.imshow("hsv", hsv)
    # cv2.imshow("sobel", sobel)

    if cv2.waitKey(1) == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
