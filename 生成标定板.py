import cv2 as cv
import numpy as np
import time
import os


w = 12  # 棋盘格角点每行数量
h = 9  # 棋盘格角点每列数量
# 生成棋盘格三维坐标
obj_points = np.zeros(((w*h), 3), np.float32)
obj_points[:, :2] = np.mgrid[0:w, 0:h].T.reshape(-1, 2)  # 将纯0数组进行编码，编码代表每一个角点的位置信息，例如[0., 0., 0.],[1., 0., 0.]
obj_points = np.reshape(obj_points, (w*h, 1, 3))  # 将位置信息矩阵变为w*h个1行三列的矩阵
# 计算棋盘格内角点的三维坐标及其在图像中的二维坐标
all_obj_points = [] # 这两个空数组很关键，如果是一张图片进行标定代码测试，这个也需要创建，如果没有，会一直报错
all_points = []
file_path = 'question'  # 存图片的文件夹，但是这个读取方式有一个缺点，文件夹内只能有图片，不能有别的类型的文件，否则会报错
for file_name in os.listdir(file_path):
    img = cv.imread(file_path + '/' + file_name)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 转为灰度图
    begin = time.time()
    ret, corners1 = cv.findCirclesGrid(img_gray, (w, h))  # 寻找内角点
    if ret == True:  # 如果寻找到足够数量的内焦点
        _, corners2 = cv.find4QuadCornerSubpix(img_gray, corners1, (5, 5))  # 细化内角点
        end = time.time()
        print((end-begin)/60)
        img_h, img_w = img.shape[:2]  # 获取图像尺寸
        all_obj_points.append(obj_points)  # 计算三维坐标
        all_points.append(corners2)  # 计算二维坐标
    else:
        end = time.time()
        print((end-begin)/60)
        img_h, img_w = img.shape[:2]

ret, camara_matrix, distcoeffs, rvecs, tvecs = cv.calibrateCamera(all_obj_points, all_points,
                                                                      (img_w, img_h), None, None)
print("重投影参数：\n{}".format(ret))
print("内参矩阵: \n{}".format(camara_matrix))
print("畸变系数: \n{}".format(distcoeffs))
print("旋转向量：\n{}".format(rvecs))
print("平移向量：\n{}".format(tvecs))






