# main face recognition logic goes here
import cv2
import numpy as np
from datetime import datetime
import csv
import face_recognition as frecog
from utils import face_utils , db_utils
import sqlite3 as db


def start_attendance_system():
    vid_capture=cv2.VideoCapture(0)
    face_locations=[]
    face_encodings=[]
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    while True:
        _,frame=vid_capture.read()
        small_frame=cv2.resize(frame,(0,0),fx=1.0,fy=1.0)
        rgb_small_frame=cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)

        face_locations=frecog.face_locations(rgb_small_frame)
        face_encodings=frecog.face_encodings(rgb_small_frame, face_locations)
        kface_encodings,kface_names=face_utils.load_known_faces()
        students=kface_names.copy()

        for face_encoding in face_encodings:
            matches=frecog.compare_faces(kface_encodings,face_encoding)
            face_distance=frecog.face_distance(kface_encodings,face_encoding)
            best_match_index=np.argmin(face_distance)
            if(matches[best_match_index]):
                name=kface_names[best_match_index]
            if name in kface_names:
                font=cv2.FONT_HERSHEY_COMPLEX_SMALL
                bottomLeftCornerOfText=(10,100)
                fontScale=1.0
                fontColor=(144, 238, 144)
                thickness=2
                lineType=2
                cv2.putText(frame,name+" Present",bottomLeftCornerOfText,font,fontScale,fontColor,thickness,lineType)
                face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                face = face_classifier.detectMultiScale(rgb_small_frame, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
                for (x,y,w,h) in face:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(144,238,144),1)
                if name in students:
                    students.remove(name)
                    face_utils.mark_attendance(name)
        cv2.imshow("Attendance",frame)
        if cv2.waitKey(1) & 0xFF==ord("q"):
            break       
    vid_capture.release()
    cv2.destroyAllWindows()

