from face_recognition.api import face_distance, face_encodings
import pymongo
import face_recognition
import cv2
import numpy as np

face_locations = []
face_encodings = []
face_names = []
everyOtherFrame = True

face_found = False
stream = cv2.VideoCapture(0)

client = pymongo.MongoClient()
db = client["Bear"]
friends = db["Bear_Friends"]
register = db["Bear_register"]

def addToDB(encoding):
    name = input("enter the students firstname and lastname in the form 'first last' in all lowercase")
    yob = input("enter the students birth year in the form '20xx': ")
    name_split = name.split() 
    pid = "0"+name_split[0][0]+name_split[0][-1]+name_split[1][0]+name_split[1][-1]+"0"+yob[-2:]
    friend_obj = {
        "name":name,
        "PID": pid,
        "position":"student",
        "YOB": yob
    }
    reg_obj = {
        "name": name,
        "PID": pid,
        "attending": "NULL",
        "last": "NULL"
    }
    encoding_obj = {
        "PID": pid,
        "encoding": encoding
    }
    

while True:
    ret, frame = stream.read()

    resized_frame = cv2.resize(frame, (0,0), fx = 0.25, fy = 0.25)

    bgr_resized_frame = resized_frame[:, :, ::-1]

    if everyOtherFrame:

        face_locations = face_recognition.face_locations(bgr_resized_frame)
        face_encodings = face_recognition.face_encodings(bgr_resized_frame,face_locations)
        face_names = []
        
    everyOtherFrame = not everyOtherFrame

    for(top, right, bottom, left) in face_locations:

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, "Friend?..", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        if not face_found:
            toadd = input("is this the student youd like to add to the register? y/n")
            if toadd.lower() == "y":
                addToDB(face_encodings[0].tolist())
                face_found = True
    cv2.imshow("init new face", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
stream.release()
cv2.destroyAllWindows()
