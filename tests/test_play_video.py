import cv2
import os
import time
 
cap = cv2.VideoCapture('result_baizhuang.mp4')
while cap.isOpened():
    ret, frame = cap.read()
    # 调整窗口大小
    cv2.namedWindow("frame", 0)  # 0可调大小，注意：窗口名必须imshow里面的一窗口名一直
    cv2.resizeWindow("frame", 800, 900)    # 设置长和宽
    cv2.imshow('frame', frame)
    time.sleep(0.04)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()