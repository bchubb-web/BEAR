import encodings
from time import strftime
from typing import Any
import pymongo
import requests
import face_recognition
import cv2
import numpy as np
import datetime



def post2server(x:int,w,student:str):
    #create form and insert formdata
    time = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    url = "http://127.0.0.1:3000/face"
    form = f"x={x}&w={w}&student={student}&time={time}"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #send request
    res = requests.request("POST", url,headers=headers,data=form)

        
def load_encodings(db):
    student_encodings = []
    student_names = []
    student_PID = []
    for encoding_doc in db["Bear_Encodings"].find():#find all encodings in collection

        #extract all data
        encoding = encoding_doc["encoding"]
        pid = encoding_doc["PID"]

        #add to arrays
        student_encodings.append(np.array(encoding))
        student_names.append(pid)
        student_PID.append(pid)
        print(f"encoding gathered from DB ~ [{pid}]")
    return student_encodings, student_names,student_PID
    
        
    


def insert_encoding(encoding:list,friends,register,encodings):

    #promt for required input
    name = input("enter the students firstname and lastname in the form 'first last':\n")
    yob = input("enter the students birth year in the form '20xx':\n")
    position = ""
    while position not in ["1", "0"]:
        position = input(f"is {name} a 'student' or 'staff:\n").lower()
        if position == "staff":
            position = "1"
        elif position == "student":
            position = "0"
    name_split = name.split() 

    #generate PID
    #position bit, 0=student 1=staff
    #first and last letters of the first name
    #first and last letters of the last name
    #filler 0
    #last 2 digits of year of birth
    pid = f"{position}{name_split[0][0]}{name_split[0][-1]}{name_split[1][0]}{name_split[1][-1]}0{yob[-2:]}"

    #generate objects
    friend_obj = {
        "name":name,
        "PID": pid,
        "position":position,
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
    query = {"PID":pid}
    if not friends.find(query):#if student doesmt exist
        print("student added to database")
        x = friends.insert_one(friend_obj)
        y = register.insert_one(reg_obj)

    z = encodings.insert_one(encoding_obj)
    print("student encodings refined")
    

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")#connect to the mongodb
db = client["Bear"]#select database
friends = db["Bear_Friends"]#select collection (table) from the db
register = db["Bear_register"]# select the register collection from the db
encodings = db["Bear_Encodings"]
settings = db["Bear_Settings"]
#select db and all tables

start_load = datetime.datetime.now()
student_encodings, student_names,student_PID = load_encodings(db)
end_load = datetime.datetime.now()
time_to_load = end_load - start_load
print("encodings collected in ["+str(round(time_to_load.total_seconds()*1000,3))+ "]ms")

setting = settings.find_one()
value = float(setting["sensitivity"])
print("initialising video stream...")

stream = cv2.VideoCapture(0)
#bear = cv2.VideoCapture(1)

every_other_frame = True


while True:
    ret,frame = stream.read()
    resized_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    brg_frame = resized_frame[:,:,::-1]
    #get image and format it for processing


    if every_other_frame:
        #skip avery other frame to save processing
        live_locations = face_recognition.face_locations(brg_frame)
        live_encodings = face_recognition.face_encodings(brg_frame, live_locations)
        #get locations and encodings for every face in the frame
        live_names = []
        for current_encoding in live_encodings:
            matches = face_recognition.compare_faces(student_encodings,current_encoding,value)
            name = "Not Recognised"
            #default name unless recognised
            live_distances = face_recognition.face_distance(student_encodings, current_encoding)
            best_encoding = np.argmin(live_distances)
            if matches[best_encoding]:
                name = student_names[best_encoding]
            live_names.append(name)
    every_other_frame = not every_other_frame
    for (top,right,bottom,left), name in zip(live_locations,live_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        box_colour = (0,255,0)
        if name == "Not Recognised":#if student ismt recognised
            box_colour = (0,0,255)
            current_index = live_names.index(name)
            unknown_encoding = live_encodings[current_index]
            unknown_encoding = unknown_encoding.tolist()#get encoding
            insert_encoding(unknown_encoding,friends,register,encodings)#insert encoding
            student_encodings, student_names,student_PID = load_encodings(db)#reload all encodings to include new ones
            continue
        else:
            post2server(left,right,name)#send data to server


        #generate the box and add student PID
        cv2.rectangle(frame,(left-8,top-8),(right+8,bottom+8),box_colour,2)
        cv2.rectangle(frame,(left,bottom-32),(right,bottom),box_colour,cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame,name,(left+6,bottom-14),font,0.6,(255,255,255),1)

    cv2.imshow("Automated Register System Video Feed", frame)#display frame

    if cv2.waitKey(1)&0xff == ord('q'):
        break#press Q to exit the program

stream.release()#stop video capture
cv2.destroyAllWindows()#close window




