import cv2
import os
import urllib
import urllib.request

#加载训练数据文件
recogizer=cv2.face.LBPHFaceRecognizer_create()
#导入数据训练中的yml文件
recogizer.read('trainer/trainer.yml')


#储存名称
names=[]
#警报全局变量
warningtime = 0

# #报警模块
# def warning():
#     return 0

def face_detect_demo(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    face_detector = cv2.CascadeClassifier("D:\opencv\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml")
    faces = face_detector.detectMultiScale(gray,1.1,4)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),color=(255,0,0),thickness=2)
        ids,confidence = recogizer.predict(gray[y:y+h,x:x+w])
        #confidence为置信评分
        if confidence > 80:
            global warningtime
            warningtime += 1
            if warningtime > 100:
                # warning()      报警模块的引用
                warningtime = 0
            cv2.putText(img,'unknow',(x+10,y-10),cv2.FONT_HERSHEY_COMPLEX,0.75,(0,255,0),1)
        else:
            cv2.putText(img,str(names[ids-1]),(x+10,y-10),cv2.FONT_HERSHEY_COMPLEX,0.75,(0,255,0),1)
        cv2.imshow('Result',img)

#名字标签
def name():
    path = './face_factory/text/'
    #names = []
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    for imagePath in imagePaths:
       name = str(os.path.split(imagePath)[1].split('.',2)[1])
       names.append(name)
cap=cv2.VideoCapture(0)
name()
while True:
    flag,frame=cap.read()
    if not flag:
        break
    face_detect_demo(frame)
    if ord(' ') == cv2.waitKey(10):
        break


