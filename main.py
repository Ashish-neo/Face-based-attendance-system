from flask import Flask,request,render_template
import os
import cv2
import numpy as np
import face_recognition
import warnings
import streamlit as st
import pickle
from datetime import datetime
import smtplib
warnings.filterwarnings("ignore")



path = 'faces'
images = []
studentName = []
myList = os.listdir(path)
print(myList)
for ids in myList:
    current_img = cv2.imread(f'{path}/{ids}')
    images.append(current_img)
    studentName.append(os.path.splitext(ids)[0])
print(studentName)

def face_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = face_encodings(images)

print("Encoding Completed....")

# to marks the attendance
def attendance(name):
    with open("Attendance_List.csv", 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        # used to ingore repeated value
        if name not in nameList:
            time_now = datetime.now()
            time_str = time_now.strftime('%H:%M:%S')
            date_str = time_now.strftime('%d/%m/%Y')
            f.writelines(f'\n{name},{time_str},{date_str}')

app=Flask(__name__)

@app.route('/')
def home1():
    return render_template('home.html')

@app.route('/start',methods=['POST'])
def start():
    capture = cv2.VideoCapture(0)

    while True:
        react, frame = capture.read()
        face = cv2.resize(frame, (0, 0), None, 0.50, 0.50)
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

        face_current_frame = face_recognition.face_locations(face)
        encoders_current_frame = face_recognition.face_encodings(face, face_current_frame)

        for encodeFace, faceLoc in zip(encoders_current_frame, face_current_frame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            face_display = face_recognition.face_distance(encodeListKnown, encodeFace)

            match_index = np.argmin(face_display)

            if matches[match_index]:
                name = studentName[match_index].upper()
                print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, x1 * 4, y2 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 102, 255), 2)
                cv2.rectangle(frame, (x1, y2 - 40), (x2, y2), (200, 255, 255), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)

                # attendance function call
                attendance(name)

        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    capture.release()##when everything is done ,release the capture
    cv2.destroyAllWindows()
    return render_template('home.html')

# to send the attendance in mail id ::--
@app.route('/send',methods=['POST'])
def send():
    email = "zonemasti489@gmail.com"
    passcode = "Mastizone@23"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, passcode)
    print("login successfully")
    # sending email to the teachers on this time

    current_time = datetime.now()
    C_day = current_time.strftime("%A")
    C_time = datetime.now().strftime("%H:%M:%S")
    # given time manually
    t0 = '09:30:00'
    t1 = '10:30:00'
    t2 = '11:30:00'
    t3 = '12:30:00'
    t4 = "13:30:00"
    t5 = '14:30:00'
    t6 = '15:30:00'
    t7 = '16:30:00'
    t8 = '17:30:00'

    # message part
    subject = f'Sir,your {C_day} Class Attendance for Msc CS(AI)'
    body = 'hello Sir/Madam'
    msg = f'Subject:{subject}\n\n{body}'
    # print(C_time)
    # if the day is holiday then mail not send to anyone
    if C_day != 'Sunday' and C_day != 'Saturday':

        # if day is monday then given all the class time to every teacher and their email to send the attendance
        if C_day == 'Monday':
            if C_time > t1 and C_time < t2:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
            if C_time > t3 and C_time < t4:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
            if C_time > t5 and C_time < t7:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)

        # if day is tuesday then given all the class time to every teacher and their email to send the attendance

        if C_day == 'Tuesday':
            if C_time > t0 and C_time < t1:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
            if C_time > t1 and C_time < t2:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
            if C_time > t3 and C_time < t4:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)

        # if day is wednesday then given all the class time to every teacher and their email to send the attendance

        if C_day == 'Wednesday':
            if C_time > t2 and C_time < t3:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
            if C_time > t3 and C_time < t4:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
            if C_time > t5 and C_time < t6:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
            if C_time > t7 and C_time < t8:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)

        # if day is thursday then given all the class time to every teacher and their email to send the attendance

        if C_day == 'Thursday':
            if C_time > t2 and C_time < t3:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
            if C_time > t5 and C_time < t6:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
            if C_time > t6 and C_time < t7:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)

        # if day is friday then given all the class time to every teacher and their email to send the attendance

        if C_day == 'Friday':
            if C_time > t0 and C_time < t2:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
            if C_time > t2 and C_time < t4:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
            if C_time > t5 and C_time < t6:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
            if C_time > t6 and C_time < t7:
                server.sendmail(email, 'ashishneo66@gmail.com', msg)
    return render_template('home.html')

# to delete the all attendance from file after sending to mail::--
@app.route('/clear',methods=['POST'])
def clear():
    with open('Attendance_List.csv', 'r+') as f:
        next(f)
        f.truncate(0)
    return render_template('home.html')


#to run the flask app
if __name__=='__main__':
    app.run()