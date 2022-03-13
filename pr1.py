import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)                     #获取电脑摄像头，10位亮度代号

#myColors = [[160,124,110,179,255,255]]
#myColorValues = [[0,0,255]]

myColors = [[133,56,0,159,156,255],
            # [90,48,0,118,255,255],
            [83,95,255,179,255,255],
            [0,107,230,57,255,255]]           
            #[81,77,255,179,240,255]该HSV值为colar_picker检测出的可乐瓶盖红色值
            #colar_picker输出值格式[HUE Min，SAT Min，VAL Min，HUE Max，SAT Max，VAL Max 需要几个颜色就写几行
            #一行myColars对应一行myColarValues，也就是说当检测到myColors的第1行颜色时会在屏幕中画出myColorValues列表中的第一行

myColorValues = [[255,0,255],
                #  [255,0,0],
                 [0,0,255],
                 [0,255,255]]                     # myColarValues需要和myColar对应    #此处为BGR值，需要哪个颜色在网上选哪个颜色
                                                #[0,0,255]为红色的BGR值
                                                #[255,0,0]为蓝色的BGR值
             
                
myPoints =  []  ## [x , y , colorId ]

def findColor(img,myColors,myColorValues):             #定义函数查找颜色
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])           
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),2,myColorValues[count],cv2.FILLED)       #count的值受到为则用myColarvalues第一行的颜色以此类推
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
        #cv2.imshow(str(color[0]),mask)
    return newPoints

def getContours(img):                     #参考ch8实现轮廓的寻找
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0             #未检测到需要返回值，故设置x，y，w，h的值
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)          框处边界轮廓
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):         #mypoint对应line23
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 5, myColorValues[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()                         #建立图片副本
    newPoints = findColor(img, myColors,myColorValues)
    if len(newPoints)!=0:             #判断，当newpointPoint不为0时，则需要迭代信号
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:              #判断，myPoint不为0，则绘制图像
        drawOnCanvas(myPoints,myColorValues)


    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break