import cv2
import sys
if __name__ == '__main__':
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    while cap.isOpened():
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30),
            flags=cv2.ORB_HARRIS_SCORE
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if ret == True:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break

