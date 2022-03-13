import cv2

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)       #cv2.CAP_DHSHOW可以让警告消失

flag = 1
num = 1

while(cap.isOpened()):
    ret_flag,Vshow = cap.read()
    cv2.imshow("Capture_Test",Vshow)  #显示图像
    k = cv2.waitKey(1) & 0xFF         #按键判断
    if k == ord('s'):      #当按下s则保存图片,需要切换成英文输入法
        cv2.imwrite('face_factory/text/'+str(num)+'.brother'+'.jpg',Vshow)     #此处name需要根据录入者的不同更改为不同的名字
        print('success to save'+str(num)+'.jpg')
        print('-------------------------------')
        num += 1
    elif k == ord(' '):     #当输入空格则退出
        break 

    # #释放摄像头
    # cap.release()

    # #释放内存
    # cv2.destroyAllWindows()