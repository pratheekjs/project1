import pandas as pd
import cv2
import urllib.request
import numpy as np
import os
from datetime import datetime
import face_recognition
from PIL import Image
import csv
from datetime import datetime
path = r'D:\COPY TEST\image_folder'
url='http://192.168.29.58/cam-hi.jpg'
##'''cam.bmp / cam-lo.jpg /cam-hi.jpg / cam.mjpeg '''
 
# if 'students.csv' in os.listdir(os.path.join(r'D:\testing')):
if os.path.exists('D:\\COPY TEST\\Students.csv'):
    print("there iss..")
    os.remove("Students.csv")
else:
    df=pd.DataFrame(list())
    df.to_csv("Students.csv")
    
 
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
 
 
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 
 
def detailStudents(name, reg_no, programee, course, batch):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        with open("Students.csv", "x") as f:
            f.write("name,reg_no,programme,course,batch,time\n")
    except FileExistsError:
        pass  # file already exists, do nothing

    # open the file for appending
    with open("Students.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow([name, reg_no, programee, course, batch,now])
    print("Student details added successfully!")

def get_current_student(matches, classNames, faceLoc, img):
    for matchIndex, match in enumerate(matches):
        if match:
            name = classNames[matchIndex].upper()
            reg_no = "12345"  # replace with actual registration number
            programee = "B.Tech"  # replace with actual program name
            course = "Computer Science"  # replace with actual course name
            batch = "2022"  # replace with actual batch year
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            return name, reg_no, programee, course, batch
    return None, None, None, None, None
 
encodeListKnown = findEncodings(images)
print('Encoding Complete')
 
#cap = cv2.VideoCapture(0)
 

while True:
    #success, img = cap.read()
    img_resp=urllib.request.urlopen(url)
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgnp,-1)
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgnp, -1)
    if img is not None and img.shape[0] > 0 and img.shape[1] > 0:
        cv2.imshow('Webcam', img)
        print(img.shape)
    else:
        print("Error reading image from URL")
# img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25) # type: ignore
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
 
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
 
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        print("Face Detected")
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            reg_no = "12345"  # replace with actual registration number
            programee = "B.Tech"  # replace with actual program name
            course = "Computer Science"  # replace with actual course name
            batch = "2022"  # replace with actual batch year
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            detailStudents(name, reg_no, programee, course, batch)

       
        else:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, "Intruder Alert", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Webcam', img)
    key=cv2.waitKey(5)
    if key==ord('q'):
        break
cv2.destroyAllWindows()
cv2.imread
