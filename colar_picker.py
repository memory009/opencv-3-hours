import cv2
import numpy as np
#from numpy.core.shape_base import hstack

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)                     #获取电脑摄像头，10位亮度代号




def empty(a):
    pass


cv2.namedWindow("HSV")   #给调试窗口命名
cv2.resizeWindow("HSV",640,240)
cv2.createTrackbar("Hue Min","HSV",0,179,empty)   #定义H的值 ，创建窗口中的系数 
cv2.createTrackbar("Sat Min","HSV",110,255,empty) #定义S的值
cv2.createTrackbar("Val Min","HSV",153,255,empty) #定义V的值
cv2.createTrackbar("Hue Max","HSV",19,179,empty)
cv2.createTrackbar("Sat Max","HSV",240,255,empty)
cv2.createTrackbar("Val Max","HSV",255,255,empty)

while True:
    _, img = cap.read()
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)           #将图像颜色转换为HSV
    #imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)        #将图片转换为灰色的语法
    h_min = cv2.getTrackbarPos("Hue Min", "HSV")
    h_max = cv2.getTrackbarPos("Hue Max", "HSV")
    s_min = cv2.getTrackbarPos("Sat Min", "HSV")
    s_max = cv2.getTrackbarPos("Sat Max", "HSV")
    v_min = cv2.getTrackbarPos("Val Min", "HSV")
    v_max = cv2.getTrackbarPos("Val Max", "HSV")
    print(h_min,h_max,s_min,s_max,v_min,v_max)

    lower = np.array([h_min,s_min,v_min])           #定义lower数组
    upper = np.array([h_max,s_max,v_max])           #定义upper数组
    mask = cv2.inRange(imgHSV,lower,upper)
    result = cv2.bitwise_and(img,img,mask =mask)
    

    
    mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img,mask,result])


    # cv2.imshow("Original",img)
    # cv2.imshow("HSV",imgHSV)
    # cv2.imshow("Mask", mask)
    # cv2.imshow("Result", imgResult)

    cv2.imshow('Hoerizontal Stacking', hStack)
    if cv2.waitKey(1) & 0xFF == ord == ('q'):
        break

cap.release()
cap.destroyAllWindows()
