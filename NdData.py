import cv2
import numpy as np 
import os
from PIL import Image
import sqlite3

# training hình ảnh và nhận diện khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read('E:/DACS/recoginzer/trainData.yml')
#lay du lieu tu database thoong qua id

def getprofile(id):
    conn = sqlite3.connect('E:/DACS/data.db')

    query = "SELECT * FROM people WHERE ID="+str(id)
    cursor = conn.execute(query)

    profile = None

    for rown in cursor:
        profile = rown

    conn.close()
    return profile    

cap = cv2.VideoCapture(0)
fontface = cv2.FONT_HERSHEY_SIMPLEX

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

        roi_gray = gray[y:y+h , x:x+w]  
        id,confidence = recognizer.predict(roi_gray)

        if confidence <40:
            profile = getprofile(id)

            if(profile != None):
                cv2.putText(frame, ""+str(profile[1]), (x+10, y+h+30) , fontface, 1, (0,255,0),2)
                cv2.putText(frame, "Class: "+str(profile[2]), (x+10, y+h+60), fontface, 1, (0,255,0), 2)
                cv2.putText(frame, "Age: "+str(profile[3]), (x+10, y+h+90), fontface, 1, (0,255,0), 2)
                cv2.putText(frame, "MSV: "+str(profile[4]), (x+10, y+h+120), fontface, 1, (0,255,0), 2)
        else:
            cv2.putText(frame, "KhongBiet", (x+10, y+h+30) , fontface, 1, (0,0,255),2)
    cv2.imshow('image',frame)
    if(cv2.waitKey(1) == ord('q')):
        break;      








cap.release()
cv2.destroyAllWindows()