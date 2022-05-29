import cv2
import numpy as np
import sqlite3
import os


def insertOrUpdate(id, name, classr, age, msv):

    con = sqlite3.connect('E:/DACS/data.db')

    query = "SELECT * FROM people WHERE ID="+str(id)
    cursor = con.execute(query)

    isRecordExist = 0

    for row in cursor:
        isRecordExist = 1

    if(isRecordExist == 0):
        query = "INSERT INTO people(ID, Name, Class, Age, MSV) VALUES("+str(id)+",'"+str(name)+"','" + str(classr) + "','" + str(age) + "','" + str(msv) + "')"
    else:
        query = "UPDATE people SET Name='"+str(name)+"' , Class= '" + str(classr) + "' , Age= '" + str(age) + "', MSV= '" + str(msv) + "' WHERE ID="+str(id)

    con.execute(query)
    con.commit()
    con.close()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

#insert database

id = input("enter your ID: ")
name = input("enter your Name: ")
classr = input("enter class: ")
msv = input("emter your MSV: ")
age = input("enter your age: ")
insertOrUpdate(id, name, classr, age, msv)

sampleNum = 0

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

        if not os.path.exists('E:/DACS/dataSet'):
            os.makedirs('E:/DACS/dataSet')

        sampleNum +=1

        cv2.imwrite('E:/DACS/dataSet/User.' + str(id) + '.' + str(sampleNum)+ '.jpg', gray[y: y+ h, x: x+w])
        
    cv2.imshow('frame', frame)
    cv2.waitKey(1)

    if sampleNum > 200:
        break;

cap.release()
cv2.destroyAllWindows()        

   
