import encodings
from time import strftime
import pymongo
import requests
import face_recognition
import cv2
import numpy as np
import datetime
import timeit


def post2server(x,w,student):
    time = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    url = "http://127.0.0.1:3000/face"
    form = f"x={x}&w={w}&student={student}"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.request("POST", url,headers=headers,data=form)

def load_encodings(collection):
    logged_face_encodings = []
    logged_face_names = []
    for document in collection.find():#look through each document
        name = document["name"]
        encoding = document["encoding"]
        logged_face_encodings.append(np.array(encoding))
        if name not in logged_face_names:
            print(f"encoding gathered from DB ~ [{name}]")
        logged_face_names.append(name)
        #append the encoding and associated name to relevant lists
    return logged_face_encodings, logged_face_names

def insert_encoding(encoding,friends,register,encodings):
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
    x = friends.insert_one(friend_obj)
    y = register.insert_one(reg_obj)
    z = encodings.insert_one(encoding_obj)
    

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")#connect to the mongodb
db = client["Bear"]#select database
friends = db["Bear_Friends"]#select collection (table) from the db
register = db["Bear_register"]# select the register collection from the db
encodings = db["Bear_Encodings"]

start_load = datetime.datetime.now()
student_encodings, student_names = load_encodings(encodings)
end_load = datetime.datetime.now()
time_to_load = end_load - start_load
print("encodings collected in ["+str(round(time_to_load.total_seconds()*1000,3))+ "]ms")

sensitivity = input("how high would you like your detection sensitivity? (high/medium/low): ")
if sensitivity.lower() == "high":
    value = 0.9
elif sensitivity.lower() == "med":
    value = 0.75
elif sensitivity.lower() == "low":
    value = 0.6

stream = cv2.VideoCapture(0)


every_other_frame = 0

while True:
    ret,frame = stream.read()
    resized_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    brg_frame = resized_frame[:,:,::-1]

    if every_other_frame:
        live_locations = face_recognition.face_locations(brg_frame)
        live_encodings = face_recognition.face_encodings(brg_frame, live_locations)
        live_names = []
        for current_encoding in live_encodings:
            matches = face_recognition.compare_faces(student_encodings,current_encoding)
            name = "Not Recognised"
            live_distances = face_recognition.face_distance(student_encodings, current_encoding)
            best_encoding = np.argmin(live_distances)
            if matches[best_encoding]:
                name = student_names[best_encoding]
            live_names.append(name)
    for (top,right,bottom,left), name in zip(live_locations,live_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        box_colour = (0,255,0)
        if name == "Not Recognised":
            print("student face not recognised")
            box_colour = (0,0,255)
            current_index = live_names.index(name)
            unknown_encoding = live_encodings[current_index]
            unknown_encoding = unknown_encoding.tolist()
            insert_encoding(unknown_encoding,friends,register,encodings)
            student_encodings,student_names = load_encodings(encodings)
            continue
        else:
            post2server(left,right,name)

        cv2.rectangle(frame,(left-8,top-8),(right+8,bottom+8),box_colour,2)
        cv2.rectangle(frame,(left,bottom-32),(right,bottom),box_colour,cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame,name,(left+6,bottom-14),font,0.6,(255,255,255),1)

    cv2.imshow("Automated Register System Video Feed", frame)

    if cv2.waitKey(1)&0xff == ord('q'):
        break
stream.release()
cv2.destroyAllWindows()



