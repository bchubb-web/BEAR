import face_recognition
import cv2
from face_recognition.api import face_locations
import numpy as np
import os
import pymongo

def verify_friend(name):
    pass

async def unknown(encoding, collection):
    name = input("unrecognised face, please input full name: ")
    obj = {
        "name": name,
        "encoding":encoding
    }
    print(obj)
    #x = collection.insert_one(obj)



client = pymongo.MongoClient("mongodb://localhost:27017/")#connect to the mongodb
db = client["Bear"]#select database
collection = db["Bear_Friends"]#select collection (table) from the db

logged_face_encodings = []
logged_face_names = []

for document in collection.find():#look through each document
    name = document["name"]
    encoding = document["encoding"]
    logged_face_encodings.append(np.array(encoding))
    logged_face_names.append(name)
    #append the encoding and associated name to relevant lists
    print(f"encoding gathered from DB ~ [{name}]")

stream = cv2.VideoCapture(0)#init video stream through the bear's webcam


#init variables for main loop
real_face_locations = []
real_face_encodings = [] #array used for facial encodings
real_face_names = [] #array used to store names
process_this_frame = True #variable used to select every other frame 

while True:

    ret, frame = stream.read()#get a frame from video feed

    resized_frame = cv2.resize(frame,(0,0),fx = 0.25, fy=0.25)#resize to 1/4 for faster processing
    brg_resized_frame = resized_frame[:,:,::-1]#convert to the format used by opencv

    if process_this_frame: #process every other frame to save resources

        real_face_locations = face_recognition.face_locations(brg_resized_frame)
        real_face_encodings = face_recognition.face_encodings(brg_resized_frame,real_face_locations)

        real_face_names = []
        for current_encoding in real_face_encodings:

            matches = face_recognition.compare_faces(logged_face_encodings, current_encoding,0.8)
            name = "Not Regognised"#default 'name' placeholder

            real_face_distances = face_recognition.face_distance(logged_face_encodings,current_encoding)
            best_encoding_index = np.argmin(real_face_distances)#get the index of the selected face from the logged 'friends'
            if matches[best_encoding_index]:
                name = logged_face_names[best_encoding_index]
                #set the name placeholder to the encoding's related name
            
            real_face_names.append(name)
            #add the name to local names within the loop

    process_this_frame = not process_this_frame #invert boolean to skip every other frame

    #process and format frame
    for (top,right,bottom,left), name in zip(real_face_locations, real_face_names):
            
        #scale the processed image after facial detection has been run
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4


        boxColour = (0, 255, 0)
        if name == "Not Recognised":
            boxColour = (0, 0, 255)
            real_face_index = real_face_names.index(name)
            unknown_encoding = real_face_encodings[real_face_index]
            unknown("", collection)
        
        #sketch box around located face
        cv2.rectangle(frame,(left-8,top-8),(right+8,bottom+8),boxColour,2)
        #sketch rectangle for facial identifier
        cv2.rectangle(frame,(left,bottom-32),(right,bottom),boxColour,cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left+6, bottom-14), font, 0.6, (255, 255, 255), 1)

    #output formatted frame
    cv2.line(frame,(320,0),(320,480),(255,0,0),1)

    cv2.imshow("The Bear", frame)

    #if Q key pressed then stop program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#stop taking video input
stream.release()

#destroy the windows opened by opencv
cv2.destroyAllWindows()