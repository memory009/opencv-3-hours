import cv2
import numpy as np


###################################
widthImg=540
heightImg =640
#####################################

cap = cv2.VideoCapture(0)
cap.set(10,150)


def preProcessing(img):                                 #定义预处理函数     可参考ch2
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)      #灰度处理
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)         #高斯模糊
    imgCanny = cv2.Canny(imgBlur,200,200)               #canny轮廓勾勒
    kernel = np.ones((5,5))                             #定义一个5*5的内核
    imgDial = cv2.dilate(imgCanny,kernel,iterations=2)  #膨胀，用法中需要加入内核参数
    imgThres = cv2.erode(imgDial,kernel,iterations=1)   #腐蚀
    return imgThres                                     #如果想得到canny形式的值，可以把kerbel，imgThres和imgDial注释掉，然后将返回值改为imgCanny

def getContours(img):                                   
    biggest = np.array([])
    maxArea = 0
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>5000:
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)                        #计算轮廓的周长
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)         #获取轮廓索引
            if area >maxArea and len(approx) == 4:                #确保框取的图像矩形边数为4
                biggest = approx                                  
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest

def reorder (myPoints):      #将纸上的点一一对应，一般按照顺时针方向将矩形的四个点定义为(0,1,2,3),描绘点的时候为了使框出来的图形是矩形所以要此函数    
    myPoints = myPoints.reshape((4,2))                     #把myPoints矩阵变成一个新的4行2列的矩阵
    myPointsNew = np.zeros((4,1,2),np.int32)
    add = myPoints.sum(axis=1)                             #.sum(axis=1) 是将一个矩阵的每一行向量相加
    #print("add", add)
    myPointsNew[0] = myPoints[np.argmin(add)]              #np.argmin为给出水平方向上最小值的坐标                          
                                                                                                                        #array([0,1],[2,3])        可以理解为([0,1],
                                                                                                                                                            #[2,3])
                                                                                                                        #np.diff(a,axis=0)         按列相减,输出为([[2,2]])
                                                                                                                        #np.diff(a,axis=1)         按行相减,输出为([[1],[1]])
    myPointsNew[3] = myPoints[np.argmax(add)]              #np.argman  给出水平方向上最大值的坐标
    diff = np.diff(myPoints,axis=1)                        ##当axis=1时按行相减，当axis=0时，按列相减。        
    myPointsNew[1]= myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    #print("NewPoints",myPointsNew)
    return myPointsNew

def getWarp(img,biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped,(widthImg,heightImg))

    return imgCropped


def stackImages(scale,imgArray):       #创建图像堆栈
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

while True:
    success, img = cap.read()
    img = cv2.resize(img,(widthImg,heightImg))        #调整图像输出的大小，widthImg,heightImg在前面定义过
    imgContour = img.copy()                           #赋值一个图层

    imgThres = preProcessing(img)                     #对于定义的函数 proProcessing
    biggest = getContours(imgThres)
    if biggest.size !=0:
        imgWarped=getWarp(img,biggest)
        # imageArray = ([img,imgThres],             
        #           [imgContour,imgWarped])
        imageArray = ([imgContour, imgWarped])          #给imageArray数组赋值
        cv2.imshow("ImageWarped", imgWarped)
    else:
        # imageArray = ([img, imgThres],
        #               [img, img])
        imageArray = ([imgContour, img])

    stackedImages = stackImages(0.6,imageArray)       #调用stackImages函数，详见line65
    cv2.imshow("WorkFlow", stackedImages)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break