import cv2
import numpy as np

#限制图片长宽像素
####################
frameWidth = 640
frameHeight = 480 
####################

img = cv2.imread(r'opencv 3-hours\Resources\Pic1_1.bmp')        #使用相对路径报错，在前面加r或者把\全部变成/
kernel = np.ones((5,5),np.uint8)   #定义一个5*5的矩阵 由8位无符号整数填充，范围为（0,255）
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #将图像转换为灰度图像
imgBlur = cv2.GaussianBlur(imgGray,(3,3),0)      #高斯模糊，参数选择只能为奇数(3,3)/(5,5)......
imgCanny = cv2.Canny(img,150,200)                #勾勒出边缘
imgDialation = cv2.dilate(imgCanny,kernel,iterations=1)    #在canny的基础上调整边缘厚度(膨胀)
imgEroded = cv2.erode(imgDialation,kernel,iterations=1)    #调整图像边缘厚度(腐蚀)

#引入sobel()算子，sobel算子是一种过滤器，特点是其带有方向性
x = cv2.Sobel(img,cv2.CV_16S,1,0) #Sobel函数求完导数后会有负值，还有会大于255的值。而原图像是uint8，即8位无符号数，所以Sobel建立的图像位数不够，会有截断。因此要使用16位有符号的数据类型，即cv2.CV_16S
y = cv2.Sobel(img,cv2.CV_16S,0,1)
 
absX = cv2.convertScaleAbs(x)    # 转回uint8，否则将无法显示图像，而只是一副灰色的窗口；convertScaleAbs()的原型为：dst = cv2.convertScaleAbs(src[, dst[, alpha[, beta]]])
absY = cv2.convertScaleAbs(y)
dst = cv2.addWeighted(absX,0.5,absY,0.5,0)  #因为sobel算子是在两个方向上进行计算的，所以还需要使用cv2.addWeight()函数将之组合起来，函数原型为dst = cv2.addWeighted(src1, alpha, src2, beta, gamma[, dst[, dtype]])

# #限制图像输出大小，引入frameWidth, frameHeight
# img2 = cv2.resize(imgCanny, (frameWidth, frameHeight))        
# img3 = cv2.resize(imgDialation, (frameWidth, frameHeight))
# img4 = cv2.resize(imgEroded, (frameWidth, frameHeight))
# img5 = cv2.resize(absX, (frameWidth, frameHeight))
# img6 = cv2.resize(absY, (frameWidth, frameHeight))
# img7 = cv2.resize(dst, (frameWidth, frameHeight))   #sobel算子
img1 = cv2.drawContours(img,imgCanny,color=(0,255,0))
cv2.imshow("color Image",img1)

#展示效果
# cv2.imshow("Gray Image",imgGray)
# cv2.imshow("Blur Image",imgBlur)
# cv2.imshow("Canny Image",imgCanny)
# cv2.imshow("Dialation Image",imgDialation)
# cv2.imshow("Eroded Image",imgEroded)
# cv2.imshow("Canny Image", img2)
# cv2.imshow("Dialation Image", img3)
# cv2.imshow("Eroded Image", img4)
# cv2.imshow("absX", img5)
# cv2.imshow("absY", img6)
# cv2.imshow("Sobel", img7)
cv2.waitKey(0)